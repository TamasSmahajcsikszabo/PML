"""Error analysis for the phishing classifier: where and why does it make mistakes?

Library (all functions take a frame with columns url, y [1 = phishing], p [probability]):
    load_csv(path)                       predictions saved by deliverables/predict.py --test (or any url + truth + probability csv)
    load_run_oof(run_id=None, model=..)  out-of-fold training predictions of a models.run run (urls re-derived from the cleaned train.csv)
    load_eval_set(name, run_id=None)     test / external_test scored with the deployed blend of a run
    summary(df, thr)                     confusion counts and rates
    subgroups(df, thr)                   error rates by scheme, path, length, popularity, TLD ... (shows where errors concentrate)
    feature_shift(df, thr)               standardised mean difference of every feature: false negatives vs caught phishing, false positives vs correct clean
    worst_errors(df, thr, k)             the most confident mistakes
    report(df, thr)                      all of the above as text

CLI (run from the repo root):
    PYTHONPATH=src .venv/bin/python -m tools.error_analysis deliverables/results/<file>.csv
    PYTHONPATH=src .venv/bin/python -m tools.error_analysis --oof            # training out-of-fold errors of the latest run
    PYTHONPATH=src .venv/bin/python -m tools.error_analysis --eval external_test
Options: --threshold T (default: the run's deployed threshold), --run RUN_ID, --out FILE.md (also write the report), --top K."""
import argparse
import json
import warnings

import joblib
import numpy as np
import pandas as pd

from common import host_group, load, load_corpus, run_dir
from models.model import inputs

warnings.filterwarnings("ignore")


# ---------------------------------------------------------------- loaders
def load_csv(path):
    d = pd.read_csv(path)
    truth = d["truth"] if "truth" in d else d["label"]
    y = truth if pd.api.types.is_numeric_dtype(truth) else truth.map({"phishing": 1, "clean": 0})
    return pd.DataFrame({"url": d["url"], "y": y.astype(int), "p": d["probability"].astype(float)})


def load_run_oof(run_id=None, model="blend_top3_calibrated"):
    train = load_corpus()
    oof = pd.read_csv(run_dir(run_id) / "oof_predictions.csv")
    assert len(oof) == len(train), "oof_predictions.csv does not match data/corpus.csv"
    return pd.DataFrame({"url": train.url.values, "y": oof["y"].values, "p": oof[model].values})


def load_eval_set(name, run_id=None):
    d, m = load(name), joblib.load(run_dir(run_id) / "model.joblib")
    raw = np.mean([e.predict_proba(inputs(d.url.values)[m["columns"]])[:, 1] for e in m["members"].values()], axis=0)
    return pd.DataFrame({"url": d.url.values, "y": d.label.values, "p": m["calibrator"].predict(raw)})


def deployed_threshold(run_id=None):
    return json.loads((run_dir(run_id) / "config.json").read_text())["threshold"]


# ---------------------------------------------------------------- analysis
def tag(df, thr):
    """Adds pred and outcome (TP / FP / FN / TN)."""
    d = df.copy()
    d["pred"] = (d.p >= thr).astype(int)
    d["outcome"] = np.select([(d.y == 1) & (d.pred == 1), (d.y == 0) & (d.pred == 1), (d.y == 1) & (d.pred == 0)], ["TP", "FP", "FN"], "TN")
    return d


def summary(df, thr):
    c = tag(df, thr).outcome.value_counts().reindex(["TP", "FP", "FN", "TN"], fill_value=0)
    tp, fp, fn, tn = c.TP, c.FP, c.FN, c.TN
    return {"n": len(df), "threshold": float(thr), **c.to_dict(), "recall": tp / max(tp + fn, 1), "fpr": fp / max(fp + tn, 1),
            "precision": tp / max(tp + fp, 1), "accuracy": (tp + tn) / len(df)}


def subgroups(df, thr, min_n=15):
    """Error rate per subgroup: false-negative rate among phishing, false-positive rate among clean URLs."""
    d = tag(df, thr)
    f = inputs(d.url.values)
    d["scheme"] = np.where(d.url.str.lower().str.startswith("https"), "https", np.where(d.url.str.lower().str.startswith("http://"), "http", np.where(d.url.str.contains("://"), "other scheme", "no scheme")))
    d["has path"] = np.where(f["has_path"].values > 0, "path", "no path")
    d["length"] = pd.cut(d.url.str.len(), [0, 25, 40, 70, 120, 10**6], labels=["<=25", "26-40", "41-70", "71-120", ">120"]).astype(str)
    d["popular domain"] = np.where(f["reg_popular"].values > 0, "popular", "not popular")
    d["www"] = np.where(f["www"].values > 0, "www", "no www")
    d["tld"] = d.url.map(lambda u: host_group(u).rsplit(".", 1)[-1])
    top_tld = d.tld.value_counts().index[:6]
    d["tld"] = np.where(d.tld.isin(top_tld), d.tld, "other")
    rows = []
    for col in ("scheme", "has path", "length", "popular domain", "www", "tld"):
        for v, g in d.groupby(col):
            pos, neg = g[g.y == 1], g[g.y == 0]
            rows.append({"by": col, "value": v, "n": len(g), "phishing": len(pos), "FN rate": (pos.pred == 0).mean() if len(pos) >= min_n else np.nan,
                         "clean": len(neg), "FP rate": (neg.pred == 1).mean() if len(neg) >= min_n else np.nan})
    return pd.DataFrame(rows)


def feature_shift(df, thr, top=12):
    """Standardised mean difference (Cohen's d) of every feature: FN vs TP among phishing, FP vs TN among clean. Large |d| = what sets mistakes apart."""
    d = tag(df, thr)
    F = inputs(d.url.values)
    out = {}
    for name, bad, good in (("false negatives vs caught phishing", "FN", "TP"), ("false positives vs correct clean", "FP", "TN")):
        a, b = F[(d.outcome == bad).values], F[(d.outcome == good).values]
        if len(a) < 3 or len(b) < 3:
            out[name] = pd.DataFrame(columns=["feature", "d", "mean_errors", "mean_correct"])
            continue
        sd = np.sqrt((a.var() * (len(a) - 1) + b.var() * (len(b) - 1)) / (len(a) + len(b) - 2)).replace(0, np.nan)
        t = pd.DataFrame({"d": (a.mean() - b.mean()) / sd, "mean_errors": a.mean(), "mean_correct": b.mean()}).dropna()
        out[name] = t.reindex(t.d.abs().sort_values(ascending=False).index).head(top).rename_axis("feature").reset_index()
    return out


def worst_errors(df, thr, k=10):
    """Most confident mistakes: false negatives with the lowest probability, false positives with the highest."""
    d = tag(df, thr)
    return {"false negatives (phishing scored lowest)": d[d.outcome == "FN"].nsmallest(k, "p")[["p", "url"]].assign(url=lambda t: t.url.str[:100]),
            "false positives (clean scored highest)": d[d.outcome == "FP"].nlargest(k, "p")[["p", "url"]].assign(url=lambda t: t.url.str[:100])}


def report(df, thr, top=10):
    s = summary(df, thr)
    out = [f"# Error analysis ({s['n']} URLs, threshold {thr:.3f})", "",
           f"TP {s['TP']}  FP {s['FP']}  FN {s['FN']}  TN {s['TN']}  | recall {s['recall']:.3f}  FPR {s['fpr']:.4f}  precision {s['precision']:.3f}  accuracy {s['accuracy']:.3f}", "",
           "## Error rate by subgroup (FN rate = missed phishing, FP rate = clean URLs flagged; blank = fewer than 15)", "", subgroups(df, thr).round(3).to_string(index=False), ""]
    for name, t in feature_shift(df, thr, top).items():
        out += [f"## Features that separate {name} (Cohen's d)", "", t.round(3).to_string(index=False) if len(t) else "(too few errors)", ""]
    for name, t in worst_errors(df, thr, top).items():
        out += [f"## {name}", "", t.round(3).to_string(index=False) if len(t) else "(none)", ""]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("csv", nargs="?", help="predictions csv (url, truth|label, probability)")
    ap.add_argument("--oof", action="store_true", help="out-of-fold training predictions of the run")
    ap.add_argument("--eval", choices=["test", "external_test"], help="score and analyse a reserved evaluation set")
    ap.add_argument("--run", default=None, help="run id (default: latest)")
    ap.add_argument("--threshold", type=float, default=None)
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--out", default=None, help="also write the report to this markdown file")
    a = ap.parse_args()
    df = load_csv(a.csv) if a.csv else load_run_oof(a.run) if a.oof else load_eval_set(a.eval, a.run) if a.eval else None
    if df is None:
        ap.error("give a predictions csv, --oof or --eval")
    text = report(df, a.threshold if a.threshold is not None else deployed_threshold(a.run), a.top)
    print(text)
    if a.out:
        open(a.out, "w").write(text + "\n")


if __name__ == "__main__":
    main()
