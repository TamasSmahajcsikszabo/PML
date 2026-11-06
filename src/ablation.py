"""Which feature groups earn their place?  python ablation.py   (about 5 min)

Drop-one-group and group-alone XGBoost (default settings), host-grouped CV on the training corpus, then test / external AUC.
Keep rule: a group is kept if removing it costs >= 0.002 CV AUC (same folds), or lowers external AUC; otherwise it is a candidate to drop.
Writes models/results/ablation.csv."""
import warnings

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold

import urlfeat
from common import RESULTS, SEED, host_group, load, load_corpus
from models.model import ZOO
xgb = ZOO["xgboost"][0]
from urlfeat import lexical


def oof(make, X, y, folds):
    p = np.zeros(len(y))
    for a, b in folds:
        p[b] = make().fit(X.iloc[a], y[a]).predict_proba(X.iloc[b])[:, 1]
    return p


warnings.filterwarnings("ignore")
tr = load_corpus()
y, g = tr.label.values, tr.url.map(host_group).values
D = {"train": tr, "test": load("test"), "external": load("external_test")}
X = {k: urlfeat.featurize(d.url).fillna(0) for k, d in D.items()}
cols = list(X["train"].columns)
GROUPS = {f"lexical:{k}": v for k, v in lexical.GROUPS.items()}
GROUPS["readability:spelling"] = [c for c in cols if "legibility" in c or "typo" in c]
GROUPS["readability:leet/vowel/consonant"] = [c for c in cols if "leet" in c or "vowel" in c or "consonant" in c]
GROUPS["readability:tld/ext flags"] = [c for c in cols if c.startswith(("tld_", "ext_"))]
used = {c for v in GROUPS.values() for c in v}
text_cols = ["max_label_len", "mean_seg_len", "max_qkey_len", "max_qval_len", "mean_qval_len", "host_digit_rate", "path_digit_rate", "query_digit_rate",
             "url_digit_rate", "longest_digit_run", "rep_char_host", "rep_char_path", "rep_char_query", "rep_digit", "emb_ip", "emb_domain", "emb_hex",
             "emb_port", "n_dash_host", "n_dash_url", "n_dots_host", "n_underscore", "n_at", "non_ascii"]
GROUPS["text_values"] = [c for c in text_cols if c in cols]
GROUPS["structure"] = [c for c in cols if c not in used and c not in text_cols]
folds = list(StratifiedGroupKFold(5, shuffle=True, random_state=SEED).split(y, y, g))


def run(keep):
    keep = [c for c in cols if c in set(keep)]
    cv = roc_auc_score(y, oof(xgb, X["train"][keep], y, folds))
    m = xgb().fit(X["train"][keep], y)
    return {"n_features": len(keep), "cv_auc": cv, **{f"{k}_auc": roc_auc_score(D[k].label, m.predict_proba(X[k][keep])[:, 1]) for k in ("test", "external")}}


rows = [{"setting": "all features", **run(cols)}]
for name, c in GROUPS.items():
    rows.append({"setting": f"drop {name}", **run([x for x in cols if x not in c])})
    rows.append({"setting": f"only {name}", **run(c)})
out = pd.DataFrame(rows)
base = out.iloc[0]
out["d_cv"] = out.cv_auc - base.cv_auc
out["d_external"] = out.external_auc - base.external_auc
out.to_csv(RESULTS / "ablation.csv", index=False)
print(out.round(4).to_string(index=False))
