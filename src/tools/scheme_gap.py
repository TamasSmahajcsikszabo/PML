"""The https vs http recall gap of the corpus run: where it comes from and two fixes that do not alter data.
(1) per-source scheme mix and per-scheme errors / AUC of the promoted run (out-of-fold),
(2) per-scheme thresholds (1% FPR inside each scheme group, fitted on out-of-fold scores) vs the global threshold, scored on out-of-fold, test.csv and external_test.csv,
(3) XGBoost on train.csv without the scheme (and scheme + www) columns.

    PYTHONPATH=src .venv/bin/python -m tools.scheme_gap [RUN_DIR]"""
import glob
import sys
import warnings

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold
from xgboost import XGBClassifier

import urlfeat
from common import ADDITIONAL, SEED, host_group, load
from models.model import inputs

warnings.filterwarnings("ignore")
K = "xgboost+blend+parts_mean"


def main():
    C = sys.argv[1] if len(sys.argv) > 1 else sorted(glob.glob("src/models/results/v3_*parts-corpus"))[-1]
    corp = pd.read_csv(ADDITIONAL / "corpus.csv")
    O = pd.read_csv(f"{C}/scores_oof.csv")
    assert (O.y.values == corp.label.values).all()
    d = corp.assign(p=O[K].values, scheme=np.where(corp.url.str.startswith("https"), "https", np.where(corp.url.str.startswith("http:"), "http", "none")))
    thr = np.quantile(d.p[d.label == 0], .99)
    d["pred"] = d.p >= thr
    print("== (1) per source and scheme (out-of-fold, global 1%-FPR threshold)")
    print(d.groupby(["source", "scheme"]).apply(lambda x: pd.Series({"n": len(x), "phish_share": x.label.mean(), "FN": (~x.pred[x.label == 1]).mean() if (x.label == 1).any() else np.nan,
          "FP": x.pred[x.label == 0].mean() if (x.label == 0).any() else np.nan, "auc": roc_auc_score(x.label, x.p) if 0 < x.label.sum() < len(x) else np.nan})).round(3).to_string())
    print(d.groupby("scheme").apply(lambda x: pd.Series({"n": len(x), "phish_share": x.label.mean(), "FN": (~x.pred[x.label == 1]).mean(), "FP": x.pred[x.label == 0].mean(),
          "auc": roc_auc_score(x.label, x.p)})).round(3).to_string())

    print("\n== (2) global vs per-scheme thresholds")
    sch = lambda u: np.where(pd.Series(u).str.startswith("https"), "https", "other")
    O["s"] = sch(O.url)
    s_thr = {s: np.quantile(O[(O.y == 0) & (O.s == s)][K], .99) for s in ["https", "other"]}
    print("global", round(thr, 3), "per scheme", {k: round(v, 3) for k, v in s_thr.items()})
    rows = []
    for name, df in (("oof (rule fitted here)", O), ("test", pd.read_csv(f"{C}/scores_test.csv")), ("external_test", pd.read_csv(f"{C}/scores_external_test.csv"))):
        df = df.assign(s=sch(df.url))
        for lab, pred in (("global", df[K] >= thr), ("per-scheme", df[K] >= df.s.map(s_thr).values)):
            pos, neg = df.y == 1, df.y == 0
            rows.append({"set": name, "rule": lab, "recall": pred[pos].mean(), "FPR": pred[neg].mean(), "recall_https": pred[pos & (df.s == "https")].mean(), "recall_other": pred[pos & (df.s == "other")].mean(),
                         "FPR_https": pred[neg & (df.s == "https")].mean(), "FPR_other": pred[neg & (df.s == "other")].mean()})
    print(pd.DataFrame(rows).round(3).to_string(index=False))

    print("\n== (3) XGBoost on train.csv without scheme columns")
    D = {n: load(n) for n in ["train", "test", "external_test"]}
    X = {n: inputs(x.url.values) for n, x in D.items()}
    y, g = D["train"].label.values, np.array([host_group(u) for u in D["train"].url])
    https_tr = D["train"].url.str.startswith("https").values
    mk = lambda: XGBClassifier(n_estimators=300, max_depth=6, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, n_jobs=-1, random_state=SEED)
    for name, drop in {"all": [], "without https/ftp (scheme)": ["https", "ftp"], "without scheme + www": ["https", "ftp", "www", "www_extra_label"]}.items():
        cs = [c for c in urlfeat.COLUMNS if c not in drop]
        oof = np.zeros(len(y))
        for a, b in StratifiedGroupKFold(5, shuffle=True, random_state=SEED).split(X["train"], y, g):
            oof[b] = mk().fit(X["train"].iloc[a][cs], y[a]).predict_proba(X["train"].iloc[b][cs])[:, 1]
        m = mk().fit(X["train"][cs], y)
        t = np.quantile(oof[y == 0], .99)
        res = []
        for n in ["test", "external_test"]:
            p, yy, hs = m.predict_proba(X[n][cs])[:, 1], D[n].label.values, D[n].url.str.startswith("https").values
            res.append(f"{n}: AUC {roc_auc_score(yy, p):.4f} recall {(p[yy == 1] >= t).mean():.3f} (https {(p[(yy == 1) & hs] >= t).mean():.3f}, http {(p[(yy == 1) & ~hs] >= t).mean():.3f}) FPR {(p[yy == 0] >= t).mean():.4f}")
        print(f"{name:30s} CV AUC {roc_auc_score(y, oof):.4f} | CV recall https {(oof[(y == 1) & https_tr] >= t).mean():.3f} http {(oof[(y == 1) & ~https_tr] >= t).mean():.3f} | " + " | ".join(res), flush=True)


if __name__ == "__main__":
    main()
