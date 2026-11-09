"""Facts about the visitor's normalised view for the report: (1) how much the spelling of a URL changes the delivered model's answer; (2) cross-validated AUC of the nine models
trained on the task's normalised view against the same pipeline on the URLs as given (both on train.csv, same folds).

    PYTHONPATH=src .venv/bin/python -m tools.normalised_report [--normalised-run v2_20261109T1117_corr-filter-0.75-normalised] [--baseline v2_20261109T0949_corr-filter-0.75]
                                                             [--sample 300] [--out docs/report/normalised.json]

(1) `predict()` of the delivered (LATEST) run on a fixed sample of test.csv and external_test.csv URLs and on variants of each (reduced to the task's normal form; leading www. added
or removed; http and https swapped): share of labels that flip and mean change of the probability. (2) out-of-fold AUC per model from oof_predictions.csv of both runs (the normalised
run was stopped after cross-validation, when every model had come out lower; its CV files are complete). A model in the normalised view gives identical features for all these
variants by construction (src/tests/test_normalised.py)."""
import argparse
import json
import pathlib

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

from common import DATA, ROOT, run_dir

MODELS = ["log_reg", "svm", "naive_bayes", "knn", "decision_tree", "adaboost", "mlp", "random_forest", "xgboost"]


def variants():
    from urlfeat.visitor import URLVisitor
    v = URLVisitor()

    def www(u):
        s, sep, r = u.partition("://")
        if not sep:
            s, r = "", u
        return (s + "://" if sep else "") + (r[4:] if r.lower().startswith("www.") else "www." + r)

    def scheme(u):
        return "http://" + u[8:] if u.startswith("https://") else "https://" + u[7:] if u.startswith("http://") else u
    return {"normal_form": v.normal_form, "www": www, "scheme": scheme}


def sensitivity(n, seed=0):
    from predict import predict
    out = {}
    for name in ("test", "external_test"):
        urls = pd.read_csv(DATA / f"{name}.csv").url.sample(n, random_state=seed).tolist()
        base = [predict(u) for u in urls]
        out[name] = {}
        for k, f in variants().items():
            vv = [f(u) for u in urls]
            r = [predict(x) if x != u else b for x, u, b in zip(vv, urls, base)]
            ch = np.array([x != u for x, u in zip(vv, urls)])
            flip = np.array([p["label"] != q["label"] for p, q in zip(r, base)])
            dp = np.abs(np.array([p["probability"] for p in r]) - np.array([q["probability"] for q in base]))
            out[name][k] = {"changed": int(ch.sum()), "label_flips": int(flip[ch].sum()), "flip_share": float(flip[ch].mean()) if ch.any() else 0.0,
                            "mean_abs_dp": float(dp[ch].mean()) if ch.any() else 0.0}
    return out


def cv_compare(norm_run, base_run):
    a, b = pd.read_csv(run_dir(base_run) / "oof_predictions.csv"), pd.read_csv(run_dir(norm_run) / "oof_predictions.csv")
    assert (a.y.values == b.y.values).all() and (a.group.values == b.group.values).all(), "the two runs do not share their rows"
    return {m: {"as_given": float(roc_auc_score(a.y, a[m])), "normalised": float(roc_auc_score(b.y, b[m]))} for m in MODELS}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--normalised-run", default="v2_20261109T1117_corr-filter-0.75-normalised")
    ap.add_argument("--baseline", default="v2_20261109T0949_corr-filter-0.75")
    ap.add_argument("--sample", type=int, default=300)
    ap.add_argument("--out", default=str(ROOT / "docs" / "report" / "normalised.json"))
    a = ap.parse_args()
    delivered = (ROOT / "src" / "models" / "results" / "LATEST").read_text().strip()
    R = {"normalised_run": a.normalised_run, "baseline": a.baseline, "delivered_run": delivered, "sample": a.sample,
         "cv_auc": cv_compare(a.normalised_run, a.baseline), "sensitivity_of_delivered": sensitivity(a.sample)}
    pathlib.Path(a.out).write_text(json.dumps(R, indent=1))
    print(json.dumps(R["cv_auc"], indent=1))
    print(json.dumps(R["sensitivity_of_delivered"], indent=1))


if __name__ == "__main__":
    main()
