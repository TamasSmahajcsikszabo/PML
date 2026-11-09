"""The parts model (architecture adapted from url_grammar "U", trained here on our own features and data): three XGBoosts, each judging ONE kind of part
(host/scheme columns; one row per path segment; one row per query key or value), and a logistic regression that combines
[host logit, segment mean/max/min, query mean/max/min] (0, 0, 0 where a URL has no such part: the absence of a part is never a value).
A part inherits the label of its URL. The combiner is fitted on out-of-fold component scores (cross-fitting), the components are then refitted on all rows.
The collinearity filter (|Spearman r| >= max_corr) runs on every component, on its training rows only."""
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedGroupKFold
from xgboost import XGBClassifier

from common import SEED

_logit = lambda p: np.log(np.clip(p, 1e-6, 1 - 1e-6) / (1 - np.clip(p, 1e-6, 1 - 1e-6)))
KINDS = {"seg": ["seg"], "qry": ["qkey", "qval"]}


def _xgb():
    return XGBClassifier(n_estimators=300, max_depth=4, learning_rate=0.1, n_jobs=-1, random_state=SEED)


def subset(P, idx):
    """parts of the URLs `idx` (positions in the table), their row numbers renumbered 0..len(idx)-1"""
    pos = pd.Series(np.arange(len(idx)), index=np.asarray(idx))
    S = P[P.row.isin(pos.index)].copy()
    S["row"] = pos.loc[S.row].values
    return S.reset_index(drop=True)


def _frame(P, kind):
    S = P[P.kind.isin(KINDS[kind])].reset_index(drop=True)
    return S.row.values, S.drop(columns=["row", "kind"]).astype(float)


def _agg(rows, logits, n):
    out = np.zeros((n, 3))
    if len(rows):
        g = pd.Series(logits).groupby(rows).agg(["mean", "max", "min"])
        out[g.index.values.astype(int)] = g.values
    return out


def host_matrix(H, P, use_hlabel=True):
    """host frame, one row per URL. With use_hlabel it keeps the `hlabel_{col}_{stat}` columns the visitor built (mean / max / min of the part features of the host's labels; NaN where a host
    has none: IPv4, bare platform), otherwise it drops them. The frame must come from `urlfeat.tables(..., host_labels=True)` to have them."""
    H = H.reset_index(drop=True)
    if use_hlabel:
        assert any(c.startswith("hlabel_") for c in H.columns), "use_hlabel needs a host frame built with host_labels=True"
        return H
    return H[[c for c in H.columns if not c.startswith("hlabel_")]]


class PartsModel:
    def __init__(self, max_corr=0.75, n_inner=5, use_hlabel=False):
        self.max_corr, self.n_inner, self.use_hlabel = max_corr, n_inner, use_hlabel

    def _host(self, H, P):
        return host_matrix(H, P, getattr(self, "use_hlabel", False))

    def _fit_components(self, H, P, y):
        from models.run import correlation_filter
        comps = {}
        Hf = H.fillna(0)
        cols, _ = correlation_filter(Hf, y, self.max_corr) if self.max_corr else (list(Hf.columns), None)
        comps["host"] = (_xgb().fit(Hf[cols], y), cols)
        for kind in KINDS:
            rows, F = _frame(P, kind)
            yp = y[rows]
            cols, _ = correlation_filter(F, yp, self.max_corr) if self.max_corr else (list(F.columns), None)
            comps[kind] = (_xgb().fit(F[cols], yp), cols)
        return comps

    @staticmethod
    def _levels(comps, H, P):
        n = len(H)
        m, cols = comps["host"]
        parts = [_logit(m.predict_proba(H.fillna(0)[cols])[:, 1])[:, None]]
        for kind in KINDS:
            rows, F = _frame(P, kind)
            m, cols = comps[kind]
            parts.append(_agg(rows, _logit(m.predict_proba(F[cols])[:, 1]) if len(rows) else [], n))
        return np.hstack(parts)

    def fit(self, H, P, y, groups):
        y, n = np.asarray(y), len(H)
        HM = self._host(H, P)
        L = np.zeros((n, 7))
        for a, b in StratifiedGroupKFold(self.n_inner, shuffle=True, random_state=SEED).split(np.zeros(n), y, groups):
            comps = self._fit_components(HM.iloc[a].reset_index(drop=True), subset(P, a), y[a])
            L[b] = self._levels(comps, HM.iloc[b].reset_index(drop=True), subset(P, b))
        self.comb = LogisticRegression(max_iter=1000).fit(L, y)
        self.comps = self._fit_components(HM, P, y)
        self.columns = {k: v[1] for k, v in self.comps.items()}
        self.combiner_weights = dict(zip(["host", "seg_mean", "seg_max", "seg_min", "qry_mean", "qry_max", "qry_min", "intercept"], [*self.comb.coef_[0], self.comb.intercept_[0]]))
        return self

    def levels(self, H, P):
        return self._levels(self.comps, self._host(H, P), P)

    def predict_proba(self, H, P):
        return self.comb.predict_proba(self.levels(H, P))[:, 1]


def permutation_importance(model, H, P, y, n_repeats=3, seed=SEED):
    """Drop in URL-level AUC of the whole parts model when one input column of one component is shuffled (rows of H, or part rows of the segment / query frame).
    Returns a frame (component, feature, auc_drop, sd); a negative drop is noise."""
    from sklearn.metrics import roc_auc_score
    rng, Hm = np.random.default_rng(seed), model._host(H, P)
    base_levels = model.levels(H, P)
    base = roc_auc_score(y, model.comb.predict_proba(base_levels)[:, 1])
    n, rows = len(Hm), []
    blocks = {"host": slice(0, 1), "seg": slice(1, 4), "qry": slice(4, 7)}
    Hf = Hm.fillna(0)
    for comp, (m, cols) in model.comps.items():
        if comp == "host":
            for c in cols:
                drops = []
                for _ in range(n_repeats):
                    X = Hf[cols].copy()
                    X[c] = rng.permutation(X[c].values)
                    L = base_levels.copy()
                    L[:, 0] = _logit(m.predict_proba(X)[:, 1])
                    drops.append(base - roc_auc_score(y, model.comb.predict_proba(L)[:, 1]))
                rows.append({"component": comp, "feature": c, "auc_drop": np.mean(drops), "sd": np.std(drops)})
        else:
            prow, F = _frame(P, comp)
            for c in cols:
                drops = []
                for _ in range(n_repeats):
                    X = F[cols].copy()
                    X[c] = rng.permutation(X[c].values)
                    L = base_levels.copy()
                    L[:, blocks[comp]] = _agg(prow, _logit(m.predict_proba(X)[:, 1]) if len(prow) else [], n)
                    drops.append(base - roc_auc_score(y, model.comb.predict_proba(L)[:, 1]))
                rows.append({"component": comp, "feature": c, "auc_drop": np.mean(drops), "sd": np.std(drops)})
    return pd.DataFrame(rows)
