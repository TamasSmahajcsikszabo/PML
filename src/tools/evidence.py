"""Evidence behind the decisions table of the report: everything that is measured here is re-measured from the code and the run, never copied.

    PYTHONPATH=src .venv/bin/python -m tools.evidence RUN_ID [--all-features-run RUN] [--out docs/report/comparisons.json]

RUN_ID is the promoted parts run (its parent run holds the filtered nine models). Measured:
  * cv_optimism        XGBoost on the parent's features: random stratified 5-fold CV vs host-grouped 5-fold CV (same seed)
  * filter_effect      CV AUC (out-of-fold) of every model with all 141 features vs with the correlation filter; trains the all-features run (`models.run --max-corr 0`) unless
                       --all-features-run names a finished one
  * parts_effect       AUC of the blend alone, the parts model alone and the deployed mean on the out-of-fold scores, test.csv and external_test.csv
  * platform_fix       train rows whose features differ from the frozen string-based extractor (data/additional/visitor_oracle) apart from the nested-URL column
  * label_cuts         URLs of the three files in which the lexer cut a host label in two (two label tokens without a dot between them)
  * speed              ms per URL for the 141 columns on test.csv
  * counts             number of columns, kept features, platform names, TLD literals"""
import argparse
import json
import pathlib
import subprocess
import sys
import time

import joblib
import numpy as np
import pandas as pd
from antlr4 import InputStream
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold, StratifiedKFold
from xgboost import XGBClassifier

import urlfeat
from common import ADDITIONAL, DATA, RESULTS, ROOT, host_group, run_dir, training_data
from urlfeat.visitor import UrlLexer

LABEL_TOKENS = {"LABEL", "TLD", "SLD", "WWW", "DIGITS", "PUNYCODE"}


def cv_optimism(parent):
    d = training_data(parent)
    cols = json.loads((run_dir(parent) / "config.json").read_text())["features"]
    X = urlfeat.featurize(d.url.tolist()).fillna(0)[list(cols)]
    y, g = d.label.values, d.url.map(host_group).values

    def cv(split):
        p = np.zeros(len(y))
        for tr, te in split:
            m = XGBClassifier(n_estimators=300, max_depth=4, learning_rate=0.1, subsample=0.8, colsample_bytree=0.8, n_jobs=2, random_state=0, verbosity=0).fit(X.iloc[tr], y[tr])
            p[te] = m.predict_proba(X.iloc[te])[:, 1]
        return float(roc_auc_score(y, p))
    r = cv(StratifiedKFold(5, shuffle=True, random_state=0).split(X, y))
    gr = cv(StratifiedGroupKFold(5, shuffle=True, random_state=0).split(X, y, g))
    return {"model": "xgboost (300 trees, depth 4)", "n_features": len(cols), "auc_random_folds": r, "auc_grouped_folds": gr, "optimism": r - gr}


def filter_effect(parent, all_run):
    if all_run is None:
        before = {p.name for p in RESULTS.glob("v1_*")}
        pc = json.loads((run_dir(parent) / "config.json").read_text())
        data = pc.get("data") or "train"
        ratio = (pc["corpus"]["rows"] - 8651) / 8651 if data == "train+extra" else 2.0
        subprocess.run([sys.executable, "-m", "models.run", "--data", data, "--extra-ratio", str(ratio), "--max-corr", "0", "--version", "v1",
                        "--name", "all-features" + ("" if data == "train" else f"-{data}")], check=True, cwd=ROOT,
                       env={**__import__("os").environ, "PYTHONPATH": str(ROOT / "src")})
        all_run = sorted({p.name for p in RESULTS.glob("v1_*")} - before)[-1]
    a = pd.read_csv(run_dir(all_run) / "metrics_summary.csv").set_index("model")
    b = pd.read_csv(run_dir(parent) / "metrics_summary.csv").set_index("model")
    cfg_a, cfg_b = (json.loads((run_dir(r) / "config.json").read_text()) for r in (all_run, parent))
    rows = {m: {"all_features": float(a.loc[m, "cv_auc_oof"]), "filtered": float(b.loc[m, "cv_auc_oof"])} for m in b.index if m in a.index}
    for m in rows:
        rows[m]["diff"] = rows[m]["filtered"] - rows[m]["all_features"]
    return {"all_features_run": all_run, "parent_run": parent, "n_all": cfg_a["n_features"], "n_filtered": cfg_b["n_features"], "models": rows,
            "model_bytes_all": (run_dir(all_run) / "model.joblib").stat().st_size, "model_bytes_filtered": (run_dir(parent) / "model.joblib").stat().st_size}


def parts_effect(run):
    d = run_dir(run)
    cand = json.loads((d / "config.json").read_text())["deployed_candidate"]
    out = {"candidate": cand}
    for name, f in (("train_oof", "scores_oof.csv"), ("test", "scores_test.csv"), ("external_test", "scores_external_test.csv")):
        S = pd.read_csv(d / f)
        out[name] = {c: float(roc_auc_score(S.y, S[c])) for c in ("blend", "xgboost", "parts", cand)}
    return out


def platform_fix():
    o = joblib.load(ADDITIONAL / "visitor_oracle" / "train.pkl")
    X = urlfeat.featurize(o["urls"])
    a, b = o["features"].values.astype(float), X.values.astype(float)
    bad = ~((np.isnan(a) & np.isnan(b)) | (np.abs(np.nan_to_num(a) - np.nan_to_num(b)) <= 1e-12))
    keep = [i for i, c in enumerate(X.columns) if c != "ent_max_qval"]  # the 3 rows with a nested :// differ for another reason
    return {"train_rows": len(X), "rows_changed": int(bad[:, keep].any(axis=1).sum()), "rows_n_sub_changed": int(bad[:, list(X.columns).index("n_sub")].sum())}


def label_cuts():
    names, n, cuts = UrlLexer.symbolicNames, 0, 0
    for f in ("train", "test", "external_test"):
        for u in pd.read_csv(DATA / f"{f}.csv").url:
            n += 1
            lx = UrlLexer(InputStream(u))
            lx.removeErrorListeners()
            prev = None
            for t in lx.getAllTokens():
                nm = names[t.type]
                if nm in ("SLASH", "QMARK", "HASH", "COLON"):
                    break
                if nm == "AT":
                    prev = None
                    continue
                if prev in LABEL_TOKENS and nm in LABEL_TOKENS:
                    cuts += 1
                    break
                prev = None if nm == "SCHEME_PREFIX" else nm
    return {"urls_checked": n, "urls_with_a_cut_label": cuts}


def speed():
    urls = pd.read_csv(DATA / "test.csv").url.tolist()
    urlfeat.featurize(urls[:50])
    t = time.perf_counter()
    urlfeat.featurize(urls)
    return {"ms_per_url_columns": (time.perf_counter() - t) / len(urls) * 1000, "urls": len(urls)}


def counts(parent):
    lex = (ROOT / "src" / "grammar" / "UrlVocab.g4").read_text(encoding="utf-8")
    tld = lex[lex.index("fragment TLD_NAMES"):]
    tld = tld[:tld.index("\n    ;")]
    return {"columns": len(urlfeat.COLUMNS), "kept_features": json.loads((run_dir(parent) / "config.json").read_text())["n_features"],
            "platform_names": sum(1 for l in (ROOT / "src" / "lists" / "platforms.txt").read_text(encoding="utf-8").splitlines() if l.strip()), "tld_literals": tld.count("'") // 2}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("--all-features-run", default=None)
    ap.add_argument("--out", default=str(ROOT / "docs" / "report" / "comparisons.json"))
    a = ap.parse_args()
    parent = json.loads((run_dir(a.run) / "config.json").read_text())["parent"]
    R = {"run": a.run, "parent": parent}
    for k, f in (("cv_optimism", lambda: cv_optimism(parent)), ("filter_effect", lambda: filter_effect(parent, a.all_features_run)), ("parts_effect", lambda: parts_effect(a.run)),
                 ("platform_fix", platform_fix), ("label_cuts", label_cuts), ("speed", speed), ("counts", lambda: counts(parent))):
        t = time.time()
        R[k] = f()
        print(f"{k}: {json.dumps(R[k])[:200]}  ({time.time() - t:.0f} s)", flush=True)
    pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.out).write_text(json.dumps(R, indent=1))


if __name__ == "__main__":
    main()
