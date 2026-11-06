"""Offline batch training of the nine models on ALL of data/master_all.csv (7.8M URLs), detached from the terminal.

    PYTHONPATH=src .venv/bin/python -m models.batch_run --background [--name LABEL] [--workers N]
        starts the job in a background process (own session, no terminal) and returns at once, printing the run id.
        Follow it, if you want, through models/results/{runID}/status.json and train.log; it finishes by writing DONE (or FAILED with the traceback).

What the job does (everything is written to models/results/{runID}/):
  0. shards   featurizes any missing shard (models.shards); shards are random 1/32 samples of the corpus; a site (registrable host) always lies in one of 5 folds (crc32 % 5)
  1. tune     5-fold host-grouped CV with random search for every model on a ~80k-row subsample of the training folds (parallel over candidates x folds, joblib)
  2. cv       5-fold CV of the tuned models on the same subsample: train/validation metrics (metrics_cv.csv) and permutation importance (feature_importance*.csv)
  3. train    every model streams over all training shards (folds 1-4, Tranco homepages down-sampled to 25%), several models at once, each multi-threaded
  4. assess   hold-out = fold 0 (about 100k rows, never trained on): metrics, learning curves, per-source metrics; top-3 blend by hold-out AUC, isotonic calibration on one
              half of the hold-out hosts and the 1%-FPR threshold on the other half; then test.csv and external_test.csv are scored once
Files: config.json, metrics_cv.csv, metrics_summary.csv, metrics_by_source.csv, learning_curve.csv, feature_importance(.csv|_wide.csv), README.md, model.joblib (the blend), members/*.joblib."""
import argparse
import datetime
import json
import os
import subprocess
import sys
import time
import traceback

import joblib
import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from sklearn.isotonic import IsotonicRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import ParameterSampler, StratifiedGroupKFold
from sklearn.preprocessing import StandardScaler
from threadpoolctl import threadpool_limits

from common import RESULTS, SEED, load
from models import shards
from models.batch import BATCH_ZOO, THREADS
from models.model import inputs
from models.run import metrics, write_readme
from tools.build_master_all import PRIORITY

N_MINI, TRANCO, TOP_K, FPR = 4, PRIORITY.index("b_tranco"), 3, 0.01
A_SHARDS, A_STRIDE, PERM_ROWS = 6, 12, 2000
HOLD_STRIDE, B_JOBS = 15, 4


# ---------------------------------------------------------------- data
def shard_rows(i):
    """One shard after the Tranco down-sampling (3 of 4 bare homepages dropped, deterministically): X, y, src, grp."""
    X, y, src, grp = shards.load(i)
    keep = (src != TRANCO) | (np.arange(len(y)) % 4 == 0)
    return X[keep], y[keep], src[keep], grp[keep]


def holdout(ids):
    """Fold 0 (never trained on), every 15th row: X, y, src, grp."""
    parts = []
    for i in ids:
        X, y, src, grp = shard_rows(i)
        m = (grp % 5 == 0) & (np.arange(len(y)) % HOLD_STRIDE == 0)
        parts.append((X[m], y[m], src[m], grp[m]))
    return [np.concatenate(p) for p in zip(*parts)]


def subsample(ids):
    """Training-fold rows (every 12th) of the first shards: the subsample used for tuning and the 5-fold CV."""
    parts = []
    for i in ids[:A_SHARDS]:
        X, y, src, grp = shard_rows(i)
        m = (grp % 5 != 0) & (np.arange(len(y)) % A_STRIDE == 0)
        parts.append((X[m], y[m], src[m], grp[m]))
    return [np.concatenate(p) for p in zip(*parts)]


# ---------------------------------------------------------------- training
def fit_batches(est, scaler, chunks, n_chunks, callback=None):
    """Stream (X, y) batches into a model; chunks is a function returning a fresh iterator."""
    est.scaler = scaler
    if est.sample_rows:
        per = -(-est.sample_rows // n_chunks)
        parts = [(X[:per], y[:per]) for X, y in chunks()]
        est.fit_sample(np.concatenate([p[0] for p in parts]), np.concatenate([p[1] for p in parts]))
        return est
    updates = 0
    for ep in range(est.epochs):
        for k, (X, y) in enumerate(chunks()):
            if est.max_updates and updates >= est.max_updates:
                break
            est.update(X, y)
            updates += 1
            if callback and ep == est.epochs - 1:
                callback(k + 1, est)
    return est


def fit_subsample(name, params, X, y, tr):
    est = BATCH_ZOO[name][0](**params)
    sc = StandardScaler().fit(X[tr])
    parts = np.array_split(tr, N_MINI)
    return fit_batches(est, sc, lambda: ((X[c], y[c]) for c in parts), N_MINI)


def cv_task(name, params, X, y, tr, va):
    with threadpool_limits(THREADS):
        return va, fit_subsample(name, params, X, y, tr).predict_proba(X[va])[:, 1]


def cv_full_task(name, params, X, y, tr, va, seed):
    """One CV fold with the tuned model: train/validation probabilities, permutation importance on a validation subsample, native importance."""
    with threadpool_limits(THREADS):
        est = fit_subsample(name, params, X, y, tr)
        pv, pt = est.predict_proba(X[va])[:, 1], est.predict_proba(X[tr])[:, 1]
        rng = np.random.default_rng(seed)
        pb = rng.choice(len(va), min(PERM_ROWS, len(va)), replace=False)
        Xb, yb = X[va][pb], y[va][pb]
        base, drop = roc_auc_score(yb, est.predict_proba(Xb)[:, 1]), np.zeros(X.shape[1])
        for j in range(X.shape[1]):
            for _ in range(2):
                Xp = Xb.copy()
                Xp[:, j] = rng.permutation(Xp[:, j])
                drop[j] += (base - roc_auc_score(yb, est.predict_proba(Xp)[:, 1])) / 2
        return va, tr, pv, pt, drop, est.importance(X.shape[1])


def train_full(name, params, ids, scaler, hold, out):
    """Stage 3 job: stream every training shard through one model; learning curve on the hold-out; the model is saved to members/."""
    t0 = time.time()
    with threadpool_limits(THREADS):
        est, curve, seen = BATCH_ZOO[name][0](**params), [], [0]

        def chunks():
            for i in ids:
                X, y, _, grp = shard_rows(i)
                m = grp % 5 != 0
                seen[0] += int(m.sum())
                yield X[m], y[m]

        def cb(k, e):
            if k % 4 == 0 or k == len(ids):
                curve.append({"model": name, "shards_seen": k, "rows_seen_all_passes": seen[0], "holdout_auc": roc_auc_score(hold[1], e.predict_proba(hold[0])[:, 1])})

        est.scaler = scaler
        fit_batches(est, scaler, chunks, len(ids), cb)
        p = est.predict_proba(hold[0])[:, 1]
        joblib.dump(est, out / "members" / f"{name}.joblib", compress=3)
    return name, p, curve, time.time() - t0


# ---------------------------------------------------------------- driver
def run(out, a):
    def status(stage, **kw):
        (out / "status.json").write_text(json.dumps({"stage": stage, "time": f"{datetime.datetime.now():%H:%M:%S}", **kw}, indent=1))
        print(f"[{datetime.datetime.now():%H:%M:%S}] {stage} {kw}", flush=True)

    (out / "members").mkdir(exist_ok=True)
    status("shards")
    shards.build(a.workers, only=a.only_shards)
    ids = shards.available()[:a.only_shards] if a.only_shards else shards.available()
    n_jobs = min(a.workers, os.cpu_count())

    # ---- 1. tuning on the subsample
    Xa, ya, sa, ga = subsample(ids)
    status("tune", subsample_rows=len(ya), shards=len(ids))
    split = lambda seed: list(StratifiedGroupKFold(5, shuffle=True, random_state=seed).split(Xa, ya, ga))
    tune_folds, folds = split(SEED + 1), split(SEED)
    best, tuning = {}, []
    for name, (make, n_iter, space) in BATCH_ZOO.items():
        t0 = time.time()
        cands = [{}] + [{k: (v.item() if hasattr(v, "item") else v) for k, v in p.items()} for p in ParameterSampler(space, 1 if a.smoke else n_iter, random_state=SEED)]
        res = Parallel(n_jobs=n_jobs)(delayed(cv_task)(name, p, Xa, ya, tr, va) for p in cands for tr, va in tune_folds)
        aucs = []
        for c in range(len(cands)):
            part = res[c * 5:(c + 1) * 5]
            aucs.append(roc_auc_score(ya[np.concatenate([r[0] for r in part])], np.concatenate([r[1] for r in part])))
        k = int(np.argmax(aucs))
        best[name] = cands[k]
        tuning.append({"model": name, "default_cv_auc": aucs[0], "tuned_cv_auc": aucs[k], "n_candidates": len(cands) - 1, "best_params": json.dumps(cands[k], default=str)})
        status("tune", model=name, default=round(aucs[0], 4), tuned=round(aucs[k], 4), params=cands[k], seconds=round(time.time() - t0))

    # ---- 2. 5-fold CV of the tuned models: metrics and importances
    status("cv")
    rows, imp, oof = [], [], {}
    for name in BATCH_ZOO:
        res = Parallel(n_jobs=n_jobs)(delayed(cv_full_task)(name, best[name], Xa, ya, tr, va, SEED + k) for k, (tr, va) in enumerate(folds))
        p = np.full(len(ya), np.nan)
        for k, (va, tr, pv, pt, drop, nat) in enumerate(res):
            p[va] = pv
            for part, idx, pp in (("train", tr, pt), ("validation", va, pv)):
                rows += [{"model": name, "fold": k, "partition": part, "metric": m, "value": v} for m, v in metrics(ya[idx], pp).items()]
            imp.append(pd.DataFrame({"model": name, "fold": k, "feature": _columns(), "permutation_auc_drop": drop, "native": nat if nat is not None else np.nan}))
        oof[name] = p
        status("cv", model=name, auc=round(roc_auc_score(ya, p), 4))
    pd.DataFrame(rows).to_csv(out / "metrics_cv.csv", index=False, float_format="%.6g")
    fi = pd.concat(imp).groupby(["model", "feature"]).agg(permutation_auc_drop=("permutation_auc_drop", "mean"), permutation_sd=("permutation_auc_drop", "std"), native=("native", "mean")).reset_index()
    fi["rank"] = fi.groupby("model").permutation_auc_drop.rank(ascending=False)
    fi.to_csv(out / "feature_importance.csv", index=False, float_format="%.6g")
    wide = fi.pivot(index="feature", columns="model", values="permutation_auc_drop")
    wide["mean_rank"] = fi.pivot(index="feature", columns="model", values="rank").mean(axis=1)
    wide["mean_drop_top_models"] = wide[list(BATCH_ZOO)].clip(lower=0).mean(axis=1)
    wide.sort_values("mean_rank").to_csv(out / "feature_importance_wide.csv", float_format="%.6g")
    cv = pd.DataFrame(rows).query("partition == 'validation'").groupby(["model", "metric"]).value.agg(["mean", "std"]).unstack()

    # ---- 3. streaming training on all training shards
    status("scaler")
    scaler = StandardScaler()
    for i in ids:
        X, _, _, grp = shard_rows(i)
        scaler.partial_fit(X[grp % 5 != 0])
    hold = holdout(ids)
    status("train", holdout_rows=len(hold[1]), models=len(BATCH_ZOO))
    done = Parallel(n_jobs=min(B_JOBS, n_jobs))(delayed(train_full)(name, best[name], ids, scaler, hold, out) for name in BATCH_ZOO)
    P = {n: p for n, p, _, _ in done}
    pd.DataFrame([r for _, _, c, _ in done for r in c]).to_csv(out / "learning_curve.csv", index=False)
    seconds = {n: round(s) for n, _, _, s in done}
    status("assess", train_seconds=seconds)

    # ---- 4. hold-out: blend, calibration, threshold; then the reserved sets
    Xh, yh, sh, gh = hold
    half = (gh // 5) % 2  # 0: calibrate, 1: threshold + report
    auc = {n: roc_auc_score(yh, p) for n, p in P.items()}
    members = sorted(auc, key=auc.get, reverse=True)[:TOP_K]
    P["blend_top3"] = np.mean([P[m] for m in members], 0)
    iso = IsotonicRegression(out_of_bounds="clip", y_min=0, y_max=1).fit(P["blend_top3"][half == 0], yh[half == 0])
    P["blend_top3_calibrated"] = iso.predict(P["blend_top3"])
    thr = {n: float(np.quantile(p[(half == 1) & (yh == 0)], 1 - FPR)) for n, p in P.items()}
    est = {n: joblib.load(out / "members" / f"{n}.joblib") for n in members}
    rep = []
    for name, p in P.items():
        r = {"model": name, "holdout_auc": roc_auc_score(yh, p), "cv_auc_oof": roc_auc_score(ya, oof[name]) if name in oof else np.nan, "oof_threshold_1pct_fpr": thr[name]}
        if name in BATCH_ZOO:
            r.update({f"cv_{m}_{s}": cv.loc[name, (s, m)] for m in cv.columns.levels[1] for s in ("mean", "std")})
            r = {k.replace("_std", "_sd"): v for k, v in r.items()}
        for k, v in metrics(yh[half == 1], p[half == 1], thr[name]).items():
            r[f"holdout_{k}"] = v
        for ds in ("test", "external_test"):
            d = load(ds)
            Z = inputs(d.url.values)
            if name.startswith("blend"):
                s = np.mean([est[m].predict_proba(Z)[:, 1] for m in members], 0)
                s = iso.predict(s) if name.endswith("calibrated") else s
            else:
                s = joblib.load(out / "members" / f"{name}.joblib").predict_proba(Z)[:, 1]
            r.update({f"{ds}_{m}": v for m, v in metrics(d.label.values, s, thr[name]).items()})
        rep.append(r)
        status("assess", model=name, holdout=round(r["holdout_auc"], 4), test=round(r["test_auc"], 4), external=round(r["external_test_auc"], 4))
    S = pd.DataFrame(rep).merge(pd.DataFrame(tuning), on="model", how="left")
    S.to_csv(out / "metrics_summary.csv", index=False, float_format="%.6g")
    by_source = [{"model": n, "source": PRIORITY[s], "n": int((sh == s).sum()), "phishing": int(yh[sh == s].sum()),
                  "auc": roc_auc_score(yh[sh == s], p[sh == s]) if 0 < yh[sh == s].sum() < (sh == s).sum() else np.nan,
                  "recall": float((p[(sh == s) & (yh == 1)] >= thr[n]).mean()) if ((sh == s) & (yh == 1)).any() else np.nan,
                  "fpr": float((p[(sh == s) & (yh == 0)] >= thr[n]).mean()) if ((sh == s) & (yh == 0)).any() else np.nan}
                 for n, p in P.items() for s in np.unique(sh)]
    pd.DataFrame(by_source).to_csv(out / "metrics_by_source.csv", index=False, float_format="%.6g")
    joblib.dump({"members": est, "calibrator": iso, "columns": _columns()}, out / "model.joblib", compress=3)
    json.dump({"run_id": out.name, "seed": SEED, "batch": True, "shards": len(ids), "rows_in_shards": int(sum(len(shards.load(i)[1]) for i in ids)), "tuned_params": best,
               "blend_members": members, "threshold": thr["blend_top3_calibrated"], "threshold_rule": "calibrated blend score at the 99th percentile of legitimate hold-out URLs (hold-out host half B; calibrator fitted on half A)",
               "n_features": len(_columns()), "tuning_subsample_rows": len(ya), "holdout_rows": len(yh), "training_seconds": seconds,
               "notes": "models trained on folds 1-4 only (fold 0 is the hold-out); Tranco homepages down-sampled to 25%"},
              open(out / "config.json", "w"), indent=2, default=str)
    write_readme(out, S, wide, {"rows": len(ya)}, members)
    txt = (out / "README.md").read_text().replace("5-fold host-grouped CV on the training corpus", f"BATCH run: all {len(ids)} shards (7.8M URLs) streamed through each model; tuning and the 5-fold host-grouped CV below use a random subsample of")
    lc = pd.read_csv(out / "learning_curve.csv")
    txt += "\n## Hold-out and learning curve\n\nHold-out AUC (fold 0, never trained on) and metrics at the 1%-FPR threshold are in `metrics_summary.csv` (`holdout_*`); `learning_curve.csv` has the hold-out AUC after every 4 shards.\n\n" + \
           "```\n" + lc.groupby("model").holdout_auc.agg(first="first", last="last").round(4).to_string() + "\n```\n"
    (out / "README.md").write_text(txt)
    (RESULTS / "LATEST").write_text(out.name)


def _columns():
    import urlfeat
    return urlfeat.COLUMNS


def main():
    ap = argparse.ArgumentParser(description="Offline batch training of the nine models on all data")
    ap.add_argument("--background", action="store_true", help="detach: run in a background process and return immediately")
    ap.add_argument("--run-id", default=None, help=argparse.SUPPRESS)
    ap.add_argument("--name", default="batch-nine-models")
    ap.add_argument("--workers", type=int, default=6, help="processes for featurizing and for parallel tuning/CV (default 6)")
    ap.add_argument("--smoke", action="store_true", help="tiny end-to-end check (needs --only-shards)")
    ap.add_argument("--only-shards", type=int, default=None, help="use only the first K shards")
    a = ap.parse_args()
    run_id = a.run_id or f"{datetime.datetime.now():%Y%m%dT%H%M}_{'smoke' if a.smoke else a.name}"
    out = RESULTS / run_id
    out.mkdir(parents=True, exist_ok=True)
    if a.background:
        cmd = [sys.executable, "-u", "-m", "models.batch_run", "--run-id", run_id, "--workers", str(a.workers), "--name", a.name] + (["--smoke"] if a.smoke else []) + (["--only-shards", str(a.only_shards)] if a.only_shards else [])
        with open(out / "train.log", "w") as log:
            subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, start_new_session=True)
        print(f"started {run_id}\n  log:    {out / 'train.log'}\n  status: {out / 'status.json'}   (DONE or FAILED appears in the folder when it ends)")
        return
    try:
        run(out, a)
        (out / "DONE").write_text(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}\n")
    except BaseException:
        (out / "FAILED").write_text(traceback.format_exc())
        raise


if __name__ == "__main__":
    main()
