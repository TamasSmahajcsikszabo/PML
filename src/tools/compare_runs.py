"""Paired cluster bootstrap (resampling host groups) of the AUC difference between a score column of run B and the same column of run A (same rows: both runs from models.run_parts on the same data).

    PYTHONPATH=src .venv/bin/python -m tools.compare_runs RUN_A RUN_B [--cols parts xgboost+blend+parts_mean] [--n 1000]       (A = baseline; delta = B - A)"""
import argparse

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

from common import host_group


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("--cols", nargs="+", default=["parts", "xgboost+blend+parts_mean"])
    ap.add_argument("--n", type=int, default=1000)
    a = ap.parse_args()
    rng, rows = np.random.default_rng(0), []
    for s in ("oof", "test", "external_test"):
        A, B = (pd.read_csv(f"{r}/scores_{s}.csv") for r in (a.a, a.b))
        assert (A.url == B.url).all() and (A.y == B.y).all()
        codes, uniq = pd.factorize(A.url.map(host_group))
        idx = [np.flatnonzero(codes == i) for i in range(len(uniq))]
        for c in a.cols:
            d = []
            for _ in range(a.n):
                ii = np.concatenate([idx[i] for i in rng.integers(0, len(idx), len(idx))])
                y = A.y.values[ii]
                if y.min() != y.max():
                    d.append(roc_auc_score(y, B[c].values[ii]) - roc_auc_score(y, A[c].values[ii]))
            rows.append({"set": s, "column": c, "auc_A": roc_auc_score(A.y, A[c]), "auc_B": roc_auc_score(B.y, B[c]), "delta": roc_auc_score(B.y, B[c]) - roc_auc_score(A.y, A[c]),
                         "ci_low": np.quantile(d, .025), "ci_high": np.quantile(d, .975)})
    R = pd.DataFrame(rows)
    print(R.round(4).to_string(index=False))
    return R


if __name__ == "__main__":
    main()
