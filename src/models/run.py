"""Train the nine models with 5-fold host-grouped CV, tune, assess, and save everything under models/results/{runID}/.

    python -m models.run [--name LABEL]        (about 1-2 hours on CPU)

Per run directory (the run id is {version}_{time}_{name}; LATEST is only moved with --set-latest):
  config.json            seeds, cleaning report, tuned parameters, blend members, threshold
  metrics_cv.csv         every metric, per model x fold x partition (train / validation)           [5-fold CV]
  metrics_summary.csv    CV mean/sd + test.csv + external_test.csv per model (threshold = out-of-fold FPR 1%)
  feature_importance.csv permutation importance (AUC drop on the validation folds) + native importance, per model x feature
  feature_importance_wide.csv / README.md   cross-model tables and a readable summary
  oof_predictions.csv    out-of-fold probabilities of all models, labels, host groups
  model.joblib           the deployable blend (top-3 models by CV AUC, isotonic-calibrated)
test.csv / external_test.csv are only read after the models, blend and threshold were fixed from train.csv."""
import argparse
import datetime
import itertools
import json
import warnings

import joblib
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.inspection import permutation_importance
from sklearn.isotonic import IsotonicRegression
from sklearn.metrics import accuracy_score, average_precision_score, brier_score_loss, f1_score, log_loss, precision_score, recall_score, roc_auc_score, roc_curve
from sklearn.model_selection import ParameterSampler, StratifiedGroupKFold

import urlfeat
from common import RESULTS, SEED, clean_train, host_group, load, load_corpus, load_train_plus_extra
from models.model import ZOO, inputs
from urlfeat.fingerprint import fingerprint

warnings.filterwarnings("ignore")
N_FOLDS, TOP_K, FPR_TARGET, TUNE_ROWS, PERM_ROWS = 5, 3, 0.01, 20000, 3000


def metrics(y, p, thr=0.5):
    pred = p >= thr
    neg = (y == 0).sum()
    fpr, tpr, _ = roc_curve(y, p)
    return {"auc": roc_auc_score(y, p), "average_precision": average_precision_score(y, p), "accuracy": accuracy_score(y, pred), "precision": precision_score(y, pred, zero_division=0),
            "recall": recall_score(y, pred), "f1": f1_score(y, pred), "fpr": ((pred) & (y == 0)).sum() / neg, "brier": brier_score_loss(y, p),
            "log_loss": log_loss(y, np.clip(p, 1e-6, 1 - 1e-6)), "recall_at_1pct_fpr": float(np.interp(FPR_TARGET, fpr, tpr))}


def fit_predict(make, Z, y, a, b):
    m = make().fit(Z.iloc[a], y[a])
    return m, m.predict_proba(Z.iloc[b])[:, 1]


def oof(make, Z, y, folds):
    p = np.full(len(y), np.nan)
    for a, b in folds:
        p[b] = fit_predict(make, Z, y, a, b)[1]
    return p


def native_importance(model, columns):
    est = model[-1] if hasattr(model, "steps") else model
    if hasattr(est, "feature_importances_"):
        v = est.feature_importances_
    elif hasattr(est, "coef_"):  # inputs were standardised, so |coef| is comparable across features
        v = np.abs(est.coef_).ravel()
    else:
        return pd.Series(np.nan, index=columns)
    return pd.Series(v / v.sum() if v.sum() else v, index=columns)


def correlation_filter(Z, y, max_corr):
    """Pipeline step: from every group of near-duplicate features keep only one. Greedy, strongest first: features are ordered by univariate strength (|AUC - 0.5| against the
    label, on the training data) and a feature is dropped when its absolute Spearman correlation with an already kept feature is >= max_corr. Constant columns are dropped too.
    Returns the kept column names and a table (feature, strength, kept, reason, correlated_with, r)."""
    from scipy.stats import rankdata
    const = [c for c in Z.columns if Z[c].nunique() <= 1]
    X = Z.drop(columns=const)
    strength = pd.Series({c: abs(roc_auc_score(y, X[c]) - 0.5) for c in X.columns}).sort_values(ascending=False)
    R = np.abs(np.corrcoef(np.apply_along_axis(rankdata, 0, X[strength.index].values), rowvar=False))
    names, kept, rows = list(strength.index), [], []
    for i, c in enumerate(names):
        hit = max(kept, key=lambda j: R[i, j], default=None)
        if hit is not None and R[i, hit] >= max_corr:
            rows.append({"feature": c, "strength": strength[c], "kept": False, "reason": "correlated", "correlated_with": names[hit], "r": R[i, hit]})
        else:
            kept.append(i)
            rows.append({"feature": c, "strength": strength[c], "kept": True, "reason": "", "correlated_with": "", "r": np.nan})
    rows += [{"feature": c, "strength": 0.0, "kept": False, "reason": "constant", "correlated_with": "", "r": np.nan} for c in const]
    return [names[i] for i in kept], pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default="nine-models")
    ap.add_argument("--version", default="v1", help="version label, prefixed to the run id (v1 = all features)")
    ap.add_argument("--normalised", action="store_true", help="features of the task's normalised view of every URL (lower-case, no scheme, no leading www., no trailing slash)")
    ap.add_argument("--extra-ratio", type=float, default=2.0, help="with --data train+extra: extra URLs as a multiple of the size of train.csv")
    ap.add_argument("--data", choices=["corpus", "train", "train+extra"], default="corpus", help="training data: data/additional/corpus.csv or the task train.csv only, untouched")
    ap.add_argument("--select-from", default=None, metavar="RUN_ID", help="feature selection: keep the top --keep share of every feature group, ranked by the importance measured in this run")
    ap.add_argument("--keep", type=float, default=0.5)
    ap.add_argument("--max-corr", type=float, default=0.9, help="correlation filter: keep one feature of every group with |Spearman r| >= this (0 = off)")
    ap.add_argument("--set-latest", action="store_true", help="make this run the one predict.py uses (default: leave LATEST alone)")
    ap.add_argument("--smoke", action="store_true", help="tiny end-to-end check (4,000 URLs, one search candidate per model)")
    args = ap.parse_args()
    urlfeat.set_normalised(args.normalised)
    run_id = f"{args.version}_{datetime.datetime.now():%Y%m%dT%H%M}_{'smoke' if args.smoke else args.name}"
    out = RESULTS / run_id
    out.mkdir(parents=True)

    if args.data == "train":
        corpus = load("train").assign(source="task_train")  # train.csv exactly as supplied: duplicates and conflicting labels are intentional and kept
    elif args.data == "train+extra":
        corpus = load_train_plus_extra(args.extra_ratio)  # train.csv as supplied + extra public URLs (evaluation files excluded)
    else:
        corpus = load_corpus()
    if args.smoke:
        corpus = corpus.sample(4000, random_state=SEED).reset_index(drop=True)
    report = {"rows": len(corpus), "phishing": int(corpus.label.sum()), "by_source": corpus.groupby("source").label.agg(["size", "sum"]).rename(columns={"sum": "phishing"}).to_dict("index")}
    print("corpus:", report["rows"], "URLs,", report["phishing"], "phishing", flush=True)
    y, groups, source = corpus.label.values, corpus.url.map(host_group).values, corpus.source.values
    Z = inputs(corpus.url.values)  # features of the URLs exactly as stored
    selection = None
    if args.select_from:  # keep the more important half (or --keep) of every feature group
        from tools.feature_table import select_features
        selection = select_features(args.select_from, args.keep)
        selection.to_csv(out / "features_kept.csv", index=False, float_format="%.6g")
        Z = Z[selection.name[selection.kept].tolist()]
        print(f"features: {Z.shape[1]} of {len(selection)} kept ({args.keep:.0%} of every group, importance from {args.select_from})", flush=True)
    if args.max_corr:  # all features are computed; near-duplicates are removed here, using the training data only
        keep_cols, table = correlation_filter(Z, corpus.label.values, args.max_corr)
        table.to_csv(out / "correlation_filter.csv", index=False, float_format="%.6g")
        print(f"correlation filter (|r| >= {args.max_corr}): {Z.shape[1]} -> {len(keep_cols)} features", flush=True)
        Z = Z[sorted(keep_cols, key=list(Z.columns).index)]
    split = lambda idx, seed: [(idx[a], idx[b]) for a, b in StratifiedGroupKFold(N_FOLDS, shuffle=True, random_state=seed).split(idx, y[idx], groups[idx])]
    everyone = np.arange(len(y))
    folds = split(everyone, SEED)  # reporting folds: all rows
    assert not any(set(groups[a]) & set(groups[b]) for a, b in folds)
    tune_idx = np.sort(np.random.default_rng(SEED).choice(everyone, min(1500 if args.smoke else TUNE_ROWS, len(y)), replace=False))  # tuning on a random subset: much cheaper, same procedure
    tune_folds = split(tune_idx, SEED + 1)

    # 1. tune each model (random search, 5-fold grouped CV, AUC)
    best, tuning = {}, []
    for name, (make, n_iter, space) in ZOO.items():
        n_iter = 1 if args.smoke else n_iter
        default = roc_auc_score(y[tune_idx], oof(make, Z, y, tune_folds)[tune_idx])
        scored = [(roc_auc_score(y[tune_idx], oof(lambda: make(**kw), Z, y, tune_folds)[tune_idx]), kw) for kw in ParameterSampler(space, n_iter, random_state=SEED)]
        auc, kw = max(scored, key=lambda t: t[0])
        if auc <= default:
            auc, kw = default, {}
        best[name] = {k: (v.item() if hasattr(v, "item") else v) for k, v in kw.items()}
        tuning.append({"model": name, "default_cv_auc": default, "tuned_cv_auc": auc, "n_candidates": n_iter, "best_params": json.dumps(best[name])})
        print(f"{name:14s} default {default:.4f} tuned {auc:.4f} {best[name]}", flush=True)

    # 2. 5-fold CV of every tuned model: metrics on train and validation parts, permutation + native importance on the validation part
    rows, imp, P = [], [], {}
    for name, (make, _, _) in ZOO.items():
        mk = lambda: make(**best[name])
        p = np.zeros(len(y))
        for k, (a, b) in enumerate(folds):
            m, p[b] = fit_predict(mk, Z, y, a, b)
            for part, idx, pp in (("train", a, m.predict_proba(Z.iloc[a])[:, 1]), ("validation", b, p[b])):
                rows += [{"model": name, "fold": k, "partition": part, "metric": mt, "value": v} for mt, v in metrics(y[idx], pp).items()]
            pb = np.random.default_rng(SEED + k).choice(b, min(PERM_ROWS, len(b)), replace=False)
            pi = permutation_importance(m, Z.iloc[pb], y[pb], scoring="roc_auc", n_repeats=3, random_state=SEED, n_jobs=1)
            imp.append(pd.DataFrame({"model": name, "fold": k, "feature": Z.columns, "permutation_auc_drop": pi.importances_mean,
                                     "native": native_importance(m, Z.columns).values}))
        P[name] = p
        print(f"{name:14s} CV AUC {roc_auc_score(y, p):.4f}", flush=True)
    pd.DataFrame(rows).to_csv(out / "metrics_cv.csv", index=False, float_format="%.6g")
    imp = pd.concat(imp)
    fi = imp.groupby(["model", "feature"]).agg(permutation_auc_drop=("permutation_auc_drop", "mean"), permutation_sd=("permutation_auc_drop", "std"),
                                              native=("native", "mean")).reset_index()
    fi["rank"] = fi.groupby("model").permutation_auc_drop.rank(ascending=False)
    fi.to_csv(out / "feature_importance.csv", index=False, float_format="%.6g")
    wide = fi.pivot(index="feature", columns="model", values="permutation_auc_drop")
    wide["mean_rank"] = fi.pivot(index="feature", columns="model", values="rank").mean(axis=1)
    wide["mean_drop_top_models"] = wide[list(ZOO)].clip(lower=0).mean(axis=1)
    wide.sort_values("mean_rank").to_csv(out / "feature_importance_wide.csv", float_format="%.6g")

    # 3. blend of the TOP_K models by CV AUC, isotonic calibration on out-of-fold scores, threshold at 1% out-of-fold FPR
    cv_auc = {n: roc_auc_score(y, p) for n, p in P.items()}
    members = sorted(cv_auc, key=cv_auc.get, reverse=True)[:TOP_K]
    P["blend_top3"] = np.mean([P[m] for m in members], 0)
    iso = IsotonicRegression(out_of_bounds="clip", y_min=0, y_max=1).fit(P["blend_top3"], y)
    P["blend_top3_calibrated"] = iso.predict(P["blend_top3"])
    thr = {n: float(np.quantile(p[y == 0], 1 - FPR_TARGET)) for n, p in P.items()}
    pd.DataFrame({"y": y, "group": groups, **P}).to_csv(out / "oof_predictions.csv", index=False)

    # 3b. per-source diagnostics: out-of-fold metrics of every model inside each source, and leave-one-source-out for XGBoost
    by_source = []
    for name, p in P.items():
        for src in np.unique(source):
            m_ = source == src
            by_source.append({"model": name, "source": src, "n": int(m_.sum()), "phishing": int(y[m_].sum()),
                              "auc": roc_auc_score(y[m_], p[m_]) if 0 < y[m_].sum() < m_.sum() else np.nan,
                              "recall": float((p[m_ & (y == 1)] >= thr[name]).mean()) if (m_ & (y == 1)).any() else np.nan,
                              "fpr": float((p[m_ & (y == 0)] >= thr[name]).mean()) if (m_ & (y == 0)).any() else np.nan})
    pd.DataFrame(by_source).to_csv(out / "metrics_by_source.csv", index=False, float_format="%.6g")
    loso = []
    for src in np.unique(source):
        m_ = source == src
        if 0 < y[m_].sum() < m_.sum():
            est = ZOO["xgboost"][0](**best["xgboost"]).fit(Z[~m_], y[~m_])
            loso.append({"held_out_source": src, "n": int(m_.sum()), "xgboost_auc_trained_on_other_sources": roc_auc_score(y[m_], est.predict_proba(Z[m_])[:, 1])})
    pd.DataFrame(loso).to_csv(out / "metrics_leave_one_source_out.csv", index=False, float_format="%.6g")

    # 4. final fit on all cleaned training rows; first and only look at test.csv / external_test.csv
    final = {n: ZOO[n][0](**best[n]).fit(Z, y) for n in ZOO}
    summary = []
    for name in P:
        r = {"model": name, "cv_auc_oof": roc_auc_score(y, P[name]), "oof_threshold_1pct_fpr": thr[name]}
        v = pd.DataFrame(rows).query("model == @name and partition == 'validation'").groupby("metric").value.agg(["mean", "std"]) if name in ZOO else None
        if v is not None:
            r.update({f"cv_{m}_mean": v.loc[m, "mean"] for m in v.index})
            r.update({f"cv_{m}_sd": v.loc[m, "std"] for m in v.index})
        for ds in ("test", "external_test"):
            d = load(ds)
            Zd = inputs(d.url.values)[list(Z.columns)]
            if name == "blend_top3":
                s = np.mean([final[m].predict_proba(Zd)[:, 1] for m in members], 0)
            elif name == "blend_top3_calibrated":
                s = iso.predict(np.mean([final[m].predict_proba(Zd)[:, 1] for m in members], 0))
            else:
                s = final[name].predict_proba(Zd)[:, 1]
            r.update({f"{ds}_{m}": v_ for m, v_ in metrics(d.label.values, s, thr[name]).items()})
        summary.append(r)
        print(f"{name:22s} CV {r['cv_auc_oof']:.4f} test {r['test_auc']:.4f} external {r['external_test_auc']:.4f}", flush=True)
    summary = pd.DataFrame(summary).merge(pd.DataFrame(tuning), on="model", how="left")
    summary.to_csv(out / "metrics_summary.csv", index=False, float_format="%.6g")

    joblib.dump({"members": {m: final[m] for m in members}, "calibrator": iso, "columns": list(Z.columns)}, out / "model.joblib", compress=3)
    json.dump({"run_id": run_id, "normalised": bool(args.normalised), "seed": SEED, "n_folds": N_FOLDS, "corpus": report, "tuned_params": best, "blend_members": members,
               "threshold": thr["blend_top3_calibrated"], "threshold_rule": "calibrated blend score at the 99th percentile of out-of-fold legitimate URLs (validation FPR 1%)",
               "n_features": Z.shape[1], "version": args.version, "data": args.data, "parent_run_for_feature_selection": args.select_from,
               "fingerprint": fingerprint(), "feature_selection": f"top {args.keep:.0%} of every feature group by mean permutation importance of the parent run (features_kept.csv)" if args.select_from else "none (all features)",
               "correlation_filter_max_abs_spearman": args.max_corr or None, "features": list(Z.columns)}, open(out / "config.json", "w"), indent=2)
    write_readme(out, summary, wide, report, members)
    if args.set_latest:
        (RESULTS / "LATEST").write_text(run_id)
    print("->", out)


def write_readme(out, S, wide, report, members):
    names = [n for n in S.model if n in ZOO]
    cols = ["cv_auc_mean", "cv_recall_at_1pct_fpr_mean", "cv_average_precision_mean", "cv_brier_mean"]
    cv = S.set_index("model").loc[names + ["blend_top3_calibrated"]]
    md = [f"# Run {out.name}", "", f"5-fold host-grouped CV on the training corpus ({report['rows']} URLs, {wide.shape[0]} features). Blend = mean of {', '.join(members)}, isotonic-calibrated.",
          "Operating threshold of every model: score at 1% FPR on out-of-fold legitimate URLs.", "", "## Cross-validation (validation folds, mean ± sd) and train-fold AUC", "",
          "| model | AUC | recall@1%FPR | avg precision | Brier | OOF AUC |", "|---|---|---|---|---|---|"]
    for m, r in cv.iterrows():
        a = f"{r['cv_auc_mean']:.4f} ± {r['cv_auc_sd']:.4f}" if m in ZOO else "-"
        md.append(f"| {m} | {a} | {r.get('cv_recall_at_1pct_fpr_mean', np.nan):.3f} | {r.get('cv_average_precision_mean', np.nan):.3f} | {r.get('cv_brier_mean', np.nan):.3f} | {r['cv_auc_oof']:.4f} |")
    md += ["", "## test.csv and external_test.csv (reserved sets, scored once)", "", "| model | test AUC | test recall | test FPR | test precision | ext AUC | ext recall | ext FPR | ext precision |", "|---|---|---|---|---|---|---|---|---|"]
    for _, r in S.iterrows():
        md.append(f"| {r.model} | {r.test_auc:.4f} | {r.test_recall:.3f} | {r.test_fpr:.4f} | {r.test_precision:.3f} | {r.external_test_auc:.4f} | {r.external_test_recall:.3f} | {r.external_test_fpr:.4f} | {r.external_test_precision:.3f} |")
    md += ["", "## Feature importance", "", "Permutation importance = mean drop in validation-fold ROC AUC when one feature is shuffled (3 repeats x 5 folds). Full tables: `feature_importance.csv` (per model, with native importance) and `feature_importance_wide.csv`.", "",
           "### Consensus (mean rank over the nine models; mean positive AUC drop)", "", "| feature | mean rank | mean AUC drop |", "|---|---|---|"]
    top = wide.sort_values("mean_rank").head(20)
    md += [f"| {f} | {r.mean_rank:.1f} | {r.mean_drop_top_models:.4f} |" for f, r in top.iterrows()]
    md += ["", "### Top 8 features per model", ""]
    for n in names:
        t = wide[n].sort_values(ascending=False).head(8)
        md.append(f"* **{n}**: " + ", ".join(f"{f} ({v:.3f})" for f, v in t.items()))
    (out / "README.md").write_text("\n".join(md) + "\n")


if __name__ == "__main__":
    main()
