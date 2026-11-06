"""Paired cluster bootstrap (resampling host groups) of the AUC difference between candidates and a baseline, per score set of a models.run_parts run.

    PYTHONPATH=src .venv/bin/python -m tools.bootstrap_delta RUN_DIR [--baseline blend] [--n 1000]"""
import argparse

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

from common import host_group


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("--baseline", default="blend")
    ap.add_argument("--n", type=int, default=1000)
    a = ap.parse_args()
    rng, rows = np.random.default_rng(0), []
    for n in ("oof", "test", "external_test"):
        d = pd.read_csv(f"{a.run}/scores_{n}.csv")
        g = d.url.map(host_group)
        codes, uniq = pd.factorize(g)
        idx = [np.flatnonzero(codes == i) for i in range(len(uniq))]
        cands = [c for c in d.columns if c not in ("url", "y", "shape", a.baseline) and d[c].notna().all()]
        deltas = {c: [] for c in cands}
        for _ in range(a.n):
            ii = np.concatenate([idx[i] for i in rng.integers(0, len(idx), len(idx))])
            y = d.y.values[ii]
            if y.min() == y.max():
                continue
            base = roc_auc_score(y, d[a.baseline].values[ii])
            for c in cands:
                deltas[c].append(roc_auc_score(y, d[c].values[ii]) - base)
        for c in cands:
            v = np.array(deltas[c])
            rows.append({"set": n, "candidate": c, "auc": roc_auc_score(d.y, d[c]), "delta_vs_" + a.baseline: roc_auc_score(d.y, d[c]) - roc_auc_score(d.y, d[a.baseline]),
                         "ci_low": np.quantile(v, .025), "ci_high": np.quantile(v, .975)})
    R = pd.DataFrame(rows)
    R.to_csv(f"{a.run}/bootstrap_delta.csv", index=False, float_format="%.5g")
    print(R.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
