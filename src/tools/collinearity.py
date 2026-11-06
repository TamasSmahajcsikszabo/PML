"""Correlation matrix and multicollinearity of the predictors on the training data (data/corpus.csv).

    PYTHONPATH=src .venv/bin/python src/tools/collinearity.py [--rows N]

Writes docs/collinearity/:
  correlation_spearman.csv   141 x 141 Spearman correlation of the model inputs (;-separated)
  high_pairs.csv             feature pairs with |r| >= 0.8 (r, group of each)
  vif.csv                    variance inflation factor of each non-constant feature (diagonal of the inverse Pearson correlation matrix); VIF > 10 = strongly collinear
  clusters.csv               groups of features linked by |r| >= 0.9 (connected components), with the most important member (from the latest run) marked
  correlation_heatmap.png    the matrix, features ordered by hierarchical clustering
Features are computed from the URLs exactly as stored (the values the models are trained on, log1p where the pipeline applies it)."""
import argparse

import numpy as np
import pandas as pd

from common import ADDITIONAL, ROOT, load_corpus
from models.model import inputs
from tools.feature_table import G

OUT = ROOT / "docs" / "collinearity"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=None, help="use a random sample of this many corpus rows")
    ap.add_argument("--sep", default=";")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    cache = ADDITIONAL / "corpus_features.pkl"
    if cache.exists():
        Z = pd.read_pickle(cache)
    else:
        Z = inputs(load_corpus().url.values)
        Z.to_pickle(cache)
    if a.rows:
        Z = Z.sample(a.rows, random_state=0)
    print(Z.shape, flush=True)
    group = {n: g for g, m in G.items() for n in m}
    const = [c for c in Z.columns if Z[c].nunique() <= 1]
    X = Z.drop(columns=const)
    print("constant columns (no variance, excluded):", const, flush=True)

    S = X.corr(method="spearman")
    S.to_csv(OUT / "correlation_spearman.csv", sep=a.sep, float_format="%.4f")

    iu = np.triu_indices(len(S), 1)
    pairs = pd.DataFrame({"feature_a": S.index[iu[0]], "feature_b": S.columns[iu[1]], "r": S.values[iu]})
    pairs = pairs[pairs.r.abs() >= 0.8].assign(group_a=lambda d: d.feature_a.map(group), group_b=lambda d: d.feature_b.map(group), abs_r=lambda d: d.r.abs()).sort_values("abs_r", ascending=False)
    pairs.drop(columns="abs_r").to_csv(OUT / "high_pairs.csv", sep=a.sep, index=False, float_format="%.4f")

    R = np.corrcoef(X.values.astype(np.float64), rowvar=False)
    vif = pd.Series(np.diag(np.linalg.pinv(R)), index=X.columns)
    pd.DataFrame({"feature": vif.index, "group": vif.index.map(group), "vif": vif.values}).sort_values("vif", ascending=False).to_csv(OUT / "vif.csv", sep=a.sep, index=False, float_format="%.2f")

    # clusters of features linked by |r| >= 0.9
    parent = {c: c for c in X.columns}

    def find(c):
        while parent[c] != c:
            parent[c] = parent[parent[c]]
            c = parent[c]
        return c
    for _, p in pairs[pairs.abs_r >= 0.9].iterrows():
        parent[find(p.feature_a)] = find(p.feature_b)
    comp = pd.Series({c: find(c) for c in X.columns})
    try:
        from tools.feature_table import run_dir
        fi = pd.read_csv(run_dir() / "feature_importance.csv").groupby("feature").permutation_auc_drop.mean()
    except Exception:
        fi = pd.Series(np.nan, index=X.columns)
    rows = []
    for k, members in comp.groupby(comp):
        if len(members) > 1:
            m = list(members.index)
            top = max(m, key=lambda c: fi.get(c, -1))
            rows.append({"cluster": f"C{len(rows) + 1}", "size": len(m), "features": ", ".join(sorted(m)), "most_important": top, "groups": "; ".join(sorted({group[c] for c in m}))})
    pd.DataFrame(rows).sort_values("size", ascending=False).to_csv(OUT / "clusters.csv", sep=a.sep, index=False)

    # heatmap, hierarchical order
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from scipy.cluster.hierarchy import leaves_list, linkage
    from scipy.spatial.distance import squareform
    D = 1 - S.abs().fillna(0).values
    order = leaves_list(linkage(squareform((D + D.T) / 2, checks=False), "average"))
    fig, ax = plt.subplots(figsize=(15, 13))
    im = ax.imshow(S.values[np.ix_(order, order)], cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(order)), S.columns[order], rotation=90, fontsize=5)
    ax.set_yticks(range(len(order)), S.index[order], fontsize=5)
    fig.colorbar(im, shrink=0.6, label="Spearman r")
    ax.set_title(f"Predictor correlations on the training data ({len(Z):,} URLs, {len(S)} non-constant features)")
    fig.tight_layout()
    fig.savefig(OUT / "correlation_heatmap.png", dpi=130)

    print(f"pairs |r|>=0.9: {(pairs.abs_r >= 0.9).sum()}, |r|>=0.8: {len(pairs)}; features with VIF>10: {(vif > 10).sum()}, VIF>5: {(vif > 5).sum()}, VIF inf/huge: {(vif > 1e6).sum()}")
    print("clusters (|r|>=0.9):", len(rows), "covering", sum(r['size'] for r in rows), "features")


if __name__ == "__main__":
    main()
