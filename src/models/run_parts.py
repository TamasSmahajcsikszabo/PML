"""Parts model on train.csv (as supplied), alone and combined with the existing XGBoost / blend of a parent run, plus the frozen U model as a reference.

    PYTHONPATH=src .venv/bin/python -m models.run_parts [--parent v2_...] [--name parts]

Same reporting folds as models.run (5-fold StratifiedGroupKFold on host groups, seed 0), so out-of-fold scores of the parent run and of the parts model line up row by row.
Combination candidates are chosen on out-of-fold scores only; test.csv / external_test.csv are scored once at the end (threshold = 1% FPR of the out-of-fold legitimate scores).
Output in models/results/{version}_{time}_{name}/: metrics.csv, metrics_by_shape.csv, scores_{oof,test,external_test}.csv, model.joblib, config.json."""
import argparse
import datetime
import json
import re
import warnings

import joblib
import numpy as np
import pandas as pd
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.model_selection import StratifiedGroupKFold

from common import ADDITIONAL, RESULTS, SEED, host_group, load, load_corpus, run_dir
from models.parts_model import PartsModel, permutation_importance, subset
from urlfeat import parts as P_
from urlfeat.fingerprint import fingerprint

warnings.filterwarnings("ignore")
FPR = 0.01
logit = lambda p: np.log(np.clip(p, 1e-6, 1 - 1e-6) / (1 - np.clip(p, 1e-6, 1 - 1e-6)))


def fence(t):
    return "```\n" + t + "\n```"


def shape(urls):
    """path-less = nothing after the host except an optional '/' (a query or fragment makes it 'with path/query')"""
    return np.where([bool(re.fullmatch(r"(?:[a-z][a-z0-9+.-]*://)?[^/?#]*/?", u, re.I)) for u in urls], "path-less", "with path/query")


def tables(name, urls):
    cache = ADDITIONAL / f"parts_{name}_{fingerprint()[:12]}.pkl"
    if cache.exists():
        return joblib.load(cache)
    out = P_.tables(urls)
    joblib.dump(out, cache)
    return out


def metrics(y, p, thr):
    fpr, tpr, _ = roc_curve(y, p)
    pred = p >= thr
    return {"auc": roc_auc_score(y, p), "recall_at_1pct_fpr": float(np.interp(FPR, fpr, tpr)), "threshold": thr, "recall": pred[y == 1].mean(), "fpr": pred[y == 0].mean(),
            "precision": y[pred].mean() if pred.any() else np.nan, "accuracy": (pred == y).mean()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", choices=["train", "corpus"], default="train", help="training data: train.csv as supplied, or the 66k corpus (data/additional/corpus.csv)")
    ap.add_argument("--parent", default="v2_20261104T1749_corr-filter-0.75", help="run whose out-of-fold scores and fitted members are combined (same data!)")
    ap.add_argument("--set-latest", action="store_true", help="make this run the one predict.py uses")
    ap.add_argument("--name", default="parts")
    ap.add_argument("--version", default="v3")
    ap.add_argument("--max-corr", type=float, default=0.75)
    a = ap.parse_args()
    out = RESULTS / f"{a.version}_{datetime.datetime.now():%Y%m%dT%H%M}_{a.name}"
    out.mkdir(parents=True)
    D = {"train": load("train") if a.data == "train" else load_corpus(), "test": load("test"), "external_test": load("external_test")}
    T = {n: tables(n if n != "train" else a.data, d.url.tolist()) for n, d in D.items()}
    y, urls = D["train"].label.values, D["train"].url.values
    groups = np.array([host_group(u) for u in urls])
    folds = [(a_, b_) for a_, b_ in StratifiedGroupKFold(5, shuffle=True, random_state=SEED).split(np.arange(len(y)), y, groups)]  # same folds as models.run

    # 1. parts model: nested cross-fitting inside every outer fold, out-of-fold score of every training URL
    H, P = T["train"]
    oof_parts, imp = np.zeros(len(y)), []
    for k, (tr, va) in enumerate(folds):
        m = PartsModel(a.max_corr).fit(H.iloc[tr].reset_index(drop=True), subset(P, tr), y[tr], groups[tr])
        oof_parts[va] = m.predict_proba(H.iloc[va].reset_index(drop=True), subset(P, va))
        print(f"fold {k}: parts AUC {roc_auc_score(y[va], oof_parts[va]):.4f}", flush=True)
        imp.append(permutation_importance(m, H.iloc[va].reset_index(drop=True), subset(P, va), y[va]).assign(fold=k))
    final = PartsModel(a.max_corr).fit(H, P, y, groups)
    print("combiner weights:", {k: round(v, 3) for k, v in final.combiner_weights.items()}, flush=True)

    # 2. parent run: out-of-fold scores and test / external scores of its members
    pm = joblib.load(run_dir(a.parent) / "model.joblib")
    oofp = pd.read_csv(run_dir(a.parent) / "oof_predictions.csv")
    assert (oofp.y.values == y).all(), "parent run was trained on other rows"
    S = {"oof": pd.DataFrame({"url": urls, "y": y, "parts": oof_parts, "xgboost": oofp.xgboost.values, "blend": oofp.blend_top3.values})}
    from models.model import inputs
    for n in ("test", "external_test"):
        d = D[n]
        Z = inputs(d.url.values)[pm["columns"]]
        pr = {k: e.predict_proba(Z)[:, 1] for k, e in pm["members"].items()}
        S[n] = pd.DataFrame({"url": d.url.values, "y": d.label.values, "parts": final.predict_proba(*T[n]), "xgboost": pr["xgboost"], "blend": np.mean(list(pr.values()), 0)})
    for n in S:  # frozen U (tools.score_u): reference only
        f = ADDITIONAL / f"u_scores_{'train' if n == 'oof' else n}.csv"
        S[n]["u"] = pd.read_csv(f).p_u.values if a.data == "train" and f.exists() else np.nan

    # 3. combinations: mean of probabilities, and a 2-input logistic stack (honest out-of-fold estimate by grouped CV on the out-of-fold scores)
    def stack_oof(cols):
        X, o = logit(S["oof"][cols].values), np.zeros(len(y))
        for tr, va in StratifiedGroupKFold(5, shuffle=True, random_state=SEED + 1).split(X, y, groups):
            o[va] = LogisticRegression().fit(X[tr], y[tr]).predict_proba(X[va])[:, 1]
        return o
    combos = {"xgboost+parts_mean": ["xgboost", "parts"], "blend+parts_mean": ["blend", "parts"], "xgboost+blend+parts_mean": ["xgboost", "blend", "parts"]}
    for n, cols in combos.items():
        for k in S:
            S[k][n] = S[k][cols].mean(axis=1)
    stacks = {"xgboost+parts_stack": ["xgboost", "parts"], "blend+parts_stack": ["blend", "parts"]}
    for n, cols in stacks.items():
        lr = LogisticRegression().fit(logit(S["oof"][cols].values), y)
        S["oof"][n] = stack_oof(cols)
        for k in ("test", "external_test"):
            S[k][n] = lr.predict_proba(logit(S[k][cols].values))[:, 1]
    names = ["parts", "xgboost", "blend", *combos, *stacks] + (["u"] if a.data == "train" else [])

    # 4. metrics (threshold per candidate = 1% FPR of its out-of-fold legitimate scores; U has no out-of-fold, its threshold is taken on train.csv, where it was never trained)
    rows, shp = [], []
    shapes = {n: shape(S[n].url.values) for n in S}
    for nm in names:
        thr = float(np.quantile(S["oof"].loc[S["oof"].y == 0, nm], 1 - FPR))
        for n, d in S.items():
            yy, p = d.y.values, d[nm].values
            rows.append({"candidate": nm, "set": "train_oof" if n == "oof" else n, **metrics(yy, p, thr)})
            for sh in ("path-less", "with path/query"):
                mk = shapes[n] == sh
                if mk.sum() and 0 < yy[mk].sum() < mk.sum():
                    shp.append({"candidate": nm, "set": "train_oof" if n == "oof" else n, "shape": sh, "n": int(mk.sum()), "phishing": int(yy[mk].sum()), "auc": roc_auc_score(yy[mk], p[mk]),
                                "recall": float((p[mk & (yy == 1)] >= thr).mean()), "fpr": float((p[mk & (yy == 0)] >= thr).mean())})
    M, SH = pd.DataFrame(rows), pd.DataFrame(shp)
    M.to_csv(out / "metrics.csv", index=False, float_format="%.5g")
    SH.to_csv(out / "metrics_by_shape.csv", index=False, float_format="%.5g")
    for n, d in S.items():
        d.assign(shape=shapes[n]).to_csv(out / f"scores_{n}.csv", index=False)

    # 5. deployable predictor = mean of [xgboost, blend (mean of the parent's members), parts], isotonic-calibrated on out-of-fold scores, label threshold = 1% out-of-fold FPR (taken on the raw mean:
    #    isotonic steps are flat, a quantile of calibrated scores would tie)
    DEPLOY = "xgboost+blend+parts_mean"
    oo = S["oof"]
    iso = IsotonicRegression(out_of_bounds="clip", y_min=0, y_max=1).fit(oo[DEPLOY], y)
    thr_raw = float(np.quantile(oo.loc[oo.y == 0, DEPLOY], 1 - FPR))
    parent_cfg = json.loads((run_dir(a.parent) / "config.json").read_text())
    member_oof = {m: oofp[m].values for m in pm["members"]}
    per_model = {**{m: float(np.quantile(v[y == 0], 1 - FPR)) for m, v in member_oof.items()}, "parts": float(np.quantile(oo.parts[oo.y == 0], 1 - FPR))}
    cv_auc = {**{m: roc_auc_score(y, v) for m, v in member_oof.items()}, "parts": roc_auc_score(y, oo.parts)}
    pd.DataFrame({"model": list(per_model), "oof_threshold_1pct_fpr": list(per_model.values()), "cv_auc_oof": [cv_auc[m] for m in per_model]}).to_csv(out / "metrics_summary.csv", index=False)
    joblib.dump({"members": pm["members"], "parts": final, "calibrator": iso, "columns": pm["columns"], "fingerprint": fingerprint()}, out / "model.joblib", compress=3)

    # 6. predictor importance of the parts model (permutation, validation folds; native = XGBoost gain of the final components) and errors
    imp = pd.concat(imp).groupby(["component", "feature"]).auc_drop.agg(["mean", "std"]).rename(columns={"mean": "auc_drop", "std": "sd"}).reset_index()
    nat = pd.DataFrame([{"component": c, "feature": f, "native_gain": g} for c, (m, cols) in final.comps.items() for f, g in zip(cols, m.feature_importances_)])
    imp = imp.merge(nat, on=["component", "feature"], how="left").sort_values("auc_drop", ascending=False)
    imp.to_csv(out / "parts_importance.csv", index=False, float_format="%.5g")
    from tools import error_analysis as EA
    rep = []
    for n, d in S.items():
        sc = d[DEPLOY].values
        pred = sc >= thr_raw
        bad = d.assign(shape=shapes[n], outcome=np.where(pred & (d.y == 1), "TP", np.where(pred, "FP", np.where(d.y == 1, "FN", "TN"))))
        bad[bad.outcome.isin(["FP", "FN"])].drop(columns=[c for c in ["TP"] if c in bad]).to_csv(out / f"errors_{n}.csv", index=False)
        rep.append(f"# {n}\n\n" + EA.report(pd.DataFrame({"url": d.url, "y": d.y, "p": sc}), thr_raw))
    (out / "error_analysis.md").write_text("\n\n".join(rep))
    src_rows = []
    if "source" in D["train"]:
        for nm in ["parts", "xgboost", "blend", DEPLOY]:
            thr = float(np.quantile(oo.loc[oo.y == 0, nm], 1 - FPR))
            for sname in D["train"].source.unique():
                mk = (D["train"].source == sname).values
                if 0 < y[mk].sum() < mk.sum():
                    src_rows.append({"candidate": nm, "source": sname, "n": int(mk.sum()), "auc": roc_auc_score(y[mk], oo[nm].values[mk]), "recall": float((oo[nm].values[mk & (y == 1)] >= thr).mean()),
                                     "fpr": float((oo[nm].values[mk & (y == 0)] >= thr).mean())})
        pd.DataFrame(src_rows).to_csv(out / "metrics_by_source.csv", index=False, float_format="%.5g")
    cfg = {"run_id": out.name, "parent": a.parent, "max_corr": a.max_corr, "fingerprint": fingerprint(), "data": a.data, "rows": len(y), "combiner_weights": final.combiner_weights,
           "component_columns": final.columns, "deployed_candidate": DEPLOY, "blend_members": list(pm["members"]), "threshold_raw": thr_raw, "threshold": float(iso.predict([thr_raw])[0]),
           "threshold_rule": "1% FPR of the out-of-fold legitimate scores of the raw mean [xgboost, blend, parts]; probability = isotonic calibration of that mean",
           "per_model_thresholds": per_model, "folds": "StratifiedGroupKFold(5, shuffle, seed 0) on host groups, as models.run"}
    json.dump(cfg, open(out / "config.json", "w"), indent=2, default=float)

    wide = M.pivot(index="candidate", columns="set", values=["auc", "recall_at_1pct_fpr"]).reindex(names)
    print(fence(wide.round(4).to_string()))
    md = [f"# Run {out.name}", "", f"Parts model on {a.data} ({len(y)} URLs), combined with the parent run {a.parent}. 5-fold host-grouped CV (same folds as the parent); test.csv / external_test.csv scored once.",
          f"Deployed candidate: **{DEPLOY}** (threshold {thr_raw:.4f} on the raw mean = 1% out-of-fold FPR; calibrated {cfg['threshold']:.4f}).", "",
          "## AUC and recall at 1% FPR (threshold per candidate from out-of-fold legitimate scores)", "", fence(wide.round(4).to_string()), "", "## At the 1%-FPR threshold", "",
          fence(M[["candidate", "set", "recall", "fpr", "precision", "accuracy"]].round(3).to_string(index=False)), "", "## By URL shape", "", fence(SH.round(3).to_string(index=False)), "",
          "## Predictor importance of the parts model (AUC drop when shuffled, mean over folds; top 20)", "", fence(imp.head(20).round(4).to_string(index=False)), "",
          "## Combiner weights (log-odds)", "", "\n".join(f"* {k}: {v:+.3f}" for k, v in final.combiner_weights.items()), "",
          "Files: metrics.csv, metrics_by_shape.csv, bootstrap_delta.csv (tools.bootstrap_delta), parts_importance.csv, errors_*.csv (misclassified URLs with all candidate scores), error_analysis.md, scores_*.csv, "
          "metrics_by_source.csv (corpus), metrics_summary.csv, model.joblib, config.json, pipeline_logs/."]
    (out / "README.md").write_text("\n".join(md) + "\n")
    if a.set_latest:
        (RESULTS / "LATEST").write_text(out.name)
    print("->", out)


if __name__ == "__main__":
    main()
