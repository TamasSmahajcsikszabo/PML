"""Numbers of the report for one finished parts run (the deployed candidate): metrics at the fixed threshold with host-cluster bootstrap CIs, deployed precision at a 1/1000 prevalence,
seen vs unseen host AUC, calibration, and the baseline (logistic regression of the parent run).

    PYTHONPATH=src .venv/bin/python -m tools.report_numbers RUN_ID [--out docs/report/final_metrics.json] [--prevalence 0.001] [--boot 2000]

Everything is read from the run folder (scores_*.csv, config.json, model.joblib of the run and of its parent) and from data/*.csv; nothing is fitted here except the calibrator lookup (stored in model.joblib)."""
import argparse
import json

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

from common import DATA, host_group, norm_key, run_dir, training_data

SETS = {"train_oof": None, "test": "test", "external_test": "external_test"}


def rates(y, s, t):
    p = s >= t
    tp, fp, fn, tn = int((p & (y == 1)).sum()), int((p & (y == 0)).sum()), int((~p & (y == 1)).sum()), int((~p & (y == 0)).sum())
    rec, fpr = tp / max(tp + fn, 1), fp / max(fp + tn, 1)
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn, "recall": rec, "fpr": fpr, "precision": tp / max(tp + fp, 1), "accuracy": (tp + tn) / len(y)}


def prec_at(rec, fpr, prev):
    d = rec * prev + fpr * (1 - prev)
    return rec * prev / d if d > 0 else float("nan")


def recall_at_fpr(y, s, target=0.01):
    t = np.quantile(s[y == 0], 1 - target)
    return float((s[y == 1] > t).mean()), float(t)


def ece(y, p, bins=10):
    b = np.minimum((p * bins).astype(int), bins - 1)
    return float(sum(abs(y[b == k].mean() - p[b == k].mean()) * (b == k).mean() for k in range(bins) if (b == k).any()))


def boot(y, s, t, groups, B, prev, rng):
    """cluster bootstrap over hosts: AUC, recall, FPR, precision at `prev`"""
    g = pd.factorize(groups)[0]
    idx_by = [np.flatnonzero(g == k) for k in range(g.max() + 1)]
    out = []
    for _ in range(B):
        pick = rng.integers(0, len(idx_by), len(idx_by))
        i = np.concatenate([idx_by[k] for k in pick])
        yy, ss = y[i], s[i]
        if yy.min() == yy.max():
            continue
        r = rates(yy, ss, t)
        out.append((roc_auc_score(yy, ss), r["recall"], r["fpr"], prec_at(r["recall"], r["fpr"], prev)))
    a = np.array(out)
    return {k: [float(np.nanpercentile(a[:, j], 2.5)), float(np.nanpercentile(a[:, j], 97.5))] for j, k in enumerate(["auc", "recall", "fpr", "precision_at_prevalence"])}


def mixed_domains(S, cand, thr):
    """rows on websites (host_group) that carry both labels in this set vs the rest; pairwise within-website ranking; pages (task key) with both labels"""
    S = S.assign(g=S.url.map(host_group), k=S.url.map(norm_key), s=S[cand])
    lab = S.groupby("g").y.nunique()
    mixed = S.g.isin(lab[lab == 2].index)
    o = {"n_domains": int((lab == 2).sum()), "n_rows": int(mixed.sum())}
    for key, x in (("mixed", S[mixed]), ("single", S[~mixed])):
        if x.y.nunique() == 2:
            r = rates(x.y.values.astype(int), x.s.values, thr)
            o[key] = {"n": len(x), "auc": float(roc_auc_score(x.y, x.s)), "recall": r["recall"], "fpr": r["fpr"]}
    ok = tot = 0
    for g, x in S[mixed].groupby("g"):
        a, b = x.s[x.y == 1].values[:, None], x.s[x.y == 0].values[None, :]
        ok += (a > b).sum() + 0.5 * (a == b).sum(); tot += a.size * b.size
        if x.y.nunique() == 2 and len(x) >= 10:
            r = rates(x.y.values.astype(int), x.s.values, thr)
            o.setdefault("largest", {})[g] = {"n": len(x), "auc": float(roc_auc_score(x.y, x.s)), "recall": r["recall"], "fpr": r["fpr"]}
    flag = S.s >= thr
    o["share_of_false_positives"] = float((flag & (S.y == 0) & mixed).sum() / max((flag & (S.y == 0)).sum(), 1))
    o["share_of_false_negatives"] = float((~flag & (S.y == 1) & mixed).sum() / max((~flag & (S.y == 1)).sum(), 1))
    o["share_of_rows"] = float(mixed.mean())
    o["pair_auc_within_domain"] = float(ok / tot) if tot else None
    if "largest" in o:
        o["largest"] = dict(sorted(o["largest"].items(), key=lambda kv: -kv[1]["n"]))
    kl = S.groupby("k").y.nunique()
    conf = S[S.k.isin(kl[kl == 2].index)]
    o["same_page_both_labels"] = int((kl == 2).sum())
    if len(conf):
        per = conf.groupby("k")
        o["same_page_phish_higher"] = float(per.apply(lambda z: z.s[z.y == 1].max() > z.s[z.y == 0].max()).mean())
        o["same_page_identical_score"] = float(per.s.nunique().eq(1).mean())
    return o


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("--out", default="docs/report/final_metrics.json")
    ap.add_argument("--prevalence", type=float, default=1e-3)
    ap.add_argument("--boot", type=int, default=2000)
    a = ap.parse_args()
    d = run_dir(a.run)
    cfg = json.loads((d / "config.json").read_text())
    cand, thr = cfg["deployed_candidate"], cfg["threshold_raw"]
    model = joblib.load(d / "model.joblib")
    parent = run_dir(cfg["parent"])
    rng = np.random.default_rng(0)
    train_hosts = set(training_data(a.run).url.map(host_group))  # websites of the rows the run was trained on
    R = {"run": a.run, "candidate": cand, "threshold_raw": thr, "threshold_calibrated": cfg["threshold"], "prevalence": a.prevalence, "sets": {}}
    for name, f in SETS.items():
        S = pd.read_csv(d / f"scores_{'oof' if name == 'train_oof' else name}.csv")
        y, s = S.y.values.astype(int), S[cand].values
        grp = S.url.map(host_group).values
        r = rates(y, s, thr)
        cal = np.clip(model["calibrator"].predict(s), 0, 1)
        rec1, t1 = recall_at_fpr(y, s)
        o = {"n": len(y), "auc": float(roc_auc_score(y, s)), **r, "precision_at_prevalence": prec_at(r["recall"], r["fpr"], a.prevalence),
             "recall_at_1pct_fpr_on_this_set": rec1, "ece_calibrated_vs_set": ece(y, cal), "ci": boot(y, s, thr, grp, a.boot, a.prevalence, rng)}
        if r["fp"] == 0:
            o["fpr_upper_95_rule_of_three"] = 3 / max(int((y == 0).sum()), 1)
            o["precision_at_prevalence_lower_bound"] = prec_at(r["recall"], o["fpr_upper_95_rule_of_three"], a.prevalence)
        if name != "train_oof":
            seen = np.array([g in train_hosts for g in grp])
            o["share_hosts_seen_in_train"] = float(seen.mean())
            o["auc_seen_hosts"] = float(roc_auc_score(y[seen], s[seen])) if len(set(y[seen])) == 2 else None
            o["auc_unseen_hosts"] = float(roc_auc_score(y[~seen], s[~seen])) if len(set(y[~seen])) == 2 else None
        for sh, g in S.groupby("shape"):
            if g.y.nunique() == 2:
                rr = rates(g.y.values.astype(int), g[cand].values, thr)
                o.setdefault("by_shape", {})[sh] = {"n": len(g), "auc": float(roc_auc_score(g.y, g[cand])), "recall": rr["recall"], "fpr": rr["fpr"], "share_phishing": float(g.y.mean())}
        o["mixed_domains"] = mixed_domains(S, cand, thr)
        R["sets"][name] = o
    # baseline = logistic regression of the parent run (its own threshold: 1% out-of-fold FPR)
    ms = pd.read_csv(parent / "metrics_summary.csv").set_index("model")
    R["parent_models"] = {m: {k: float(ms.loc[m, k]) for k in ("cv_auc_oof", "oof_threshold_1pct_fpr", "test_auc", "test_recall", "test_fpr", "external_test_auc", "external_test_recall", "external_test_fpr")
                              if k in ms.columns} for m in ms.index}
    json.dump(R, open(a.out, "w"), indent=1)
    print(f"candidate {cand}, raw threshold {thr:.4f} (calibrated {cfg['threshold']:.4f})")
    for n, o in R["sets"].items():
        c = o["ci"]
        print(f"{n:14s} AUC {o['auc']:.3f} {c['auc']}  recall {o['recall']:.3f} {c['recall']}  FPR {o['fpr']:.4f} {c['fpr']}  precision {o['precision']:.3f}  at 1/1000 {o['precision_at_prevalence']:.3f} {c['precision_at_prevalence']}")


if __name__ == "__main__":
    main()
