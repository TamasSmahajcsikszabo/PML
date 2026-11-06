"""Deep-dive on the deployable blend: overlap with train, bootstrap CIs, deployed precision at 1/1000, calibration.
    python evaluate.py [RUN_ID]      (default: latest run in models/results/)

Writes src/models/predictions.csv (url,probability for test.csv), src/models/results/{RUN_ID}/evaluation.json and prints the tables used in REPORT.md."""
import json

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

from common import RESULTS, host_group, load, load_corpus, norm_key, run_dir
from models.model import inputs

PREVALENCE, B, rng = 1e-3, 2000, np.random.default_rng(0)
import sys
RUN = run_dir(sys.argv[1] if len(sys.argv) > 1 else None)
model = joblib.load(RUN / "model.joblib")
thr = json.loads((RUN / "config.json").read_text())["threshold"]


def score(urls):
    """Every member's probability, and the calibrated mean (the blend)."""
    Z = inputs(list(urls))[model["columns"]]
    S = {m: est.predict_proba(Z)[:, 1] for m, est in model["members"].items()}
    raw = np.mean(list(S.values()), axis=0)
    return {**S, "blend_raw": raw, "blend": model["calibrator"].predict(raw)}


def rates(y, p, t):
    pred = p >= t
    tp, fp = (pred & (y == 1)).sum(), (pred & (y == 0)).sum()
    rec, fpr = tp / (y == 1).sum(), fp / (y == 0).sum()
    return {"recall": rec, "fpr": fpr, "precision": tp / max(tp + fp, 1), "ppv_at_1_in_1000": rec * PREVALENCE / (rec * PREVALENCE + fpr * (1 - PREVALENCE))}


def ece(y, p, bins=10):
    """Expected calibration error against a 50/50 population (equal-width bins)."""
    b = np.minimum((p * bins).astype(int), bins - 1)
    return float(sum(abs(y[b == k].mean() - p[b == k].mean()) * (b == k).mean() for k in range(bins) if (b == k).any()))


def ci(y, p, t, groups=None):
    """95% bootstrap interval of every metric (rows resampled; whole hosts if groups is given)."""
    idx_by_g = pd.Series(np.arange(len(y))).groupby(groups).apply(np.array).values if groups is not None else None
    out = []
    for _ in range(B):
        i = (np.concatenate(idx_by_g[rng.integers(0, len(idx_by_g), len(idx_by_g))]) if groups is not None
             else rng.integers(0, len(y), len(y)))
        out.append({**rates(y[i], p[i], t), "auc": roc_auc_score(y[i], p[i])})
    d = pd.DataFrame(out)
    return {k: [float(d[k].quantile(.025)), float(d[k].quantile(.975))] for k in d}


train = load_corpus()  # the training corpus (train.csv + public collections)
tr_exact, tr_norm = set(train.url), set(train.url.map(norm_key))
tr_hosts = set(train.url.map(host_group))
result = {"threshold": thr}
for name in ("test", "external_test"):
    d = load(name)
    y, urls, S = d.label.values, d.url.values, score(d.url.values)
    g = d.url.map(host_group)
    seen = g.isin(tr_hosts).values
    r = {"n": len(d), "overlap_with_train": {"exact_url": float(d.url.isin(tr_exact).mean()),
                                              "task_normalised_url": float(d.url.map(norm_key).isin(tr_norm).mean()),
                                              "registrable_host_seen_in_train": float(seen.mean()),
                                              "host_seen_share_legit": float(seen[y == 0].mean()), "host_seen_share_phish": float(seen[y == 1].mean())},
         "models": {}}
    for m, p in S.items():
        r["models"][m] = {"auc": roc_auc_score(y, p)}
    p = S["blend"]
    r["calibration"] = {k: {"brier": float(np.mean((S[k] - y) ** 2)), "ece_10_bins": ece(y, S[k])} for k in ("blend_raw", "blend")}
    r["blend_at_threshold"] = rates(y, p, thr)
    n_neg = int((y == 0).sum())  # zero observed false positives still allows FPR up to ~3/n (rule of three, 95%)
    fpr_hi = max(r["blend_at_threshold"]["fpr"], 3 / n_neg)
    rec = r["blend_at_threshold"]["recall"]
    r["blend_ppv_at_1_in_1000_with_fpr_upper_bound"] = {"fpr_upper": fpr_hi, "ppv": rec * PREVALENCE / (rec * PREVALENCE + fpr_hi * (1 - PREVALENCE))}
    r["blend_ci95"] = ci(y, p, thr, groups=g.values)
    r["blend_auc_host_seen_vs_unseen"] = {k: (float(roc_auc_score(y[m], p[m])) if len(set(y[m])) == 2 else None) for k, m in (("seen", seen), ("unseen", ~seen))}
    r["blend_at_threshold_matching_1pct_fpr_on_this_set"] = rates(y, p, float(np.quantile(p[y == 0], .99)))
    r["threshold_table"] = {f"{t:.2f}": rates(y, p, t) for t in (0.5, 0.7, 0.8, 0.88, 0.93, 0.97, 0.99)}
    if name == "test":
        pd.DataFrame({"url": urls, "probability": p}).to_csv(RESULTS.parent / "predictions.csv", index=False)
    result[name] = r
json.dump(result, open(RUN / "evaluation.json", "w"), indent=2, default=float)
print(json.dumps(result, indent=1, default=lambda x: round(float(x), 4)))
