"""Facts about the extra public training data for the report: the run trained on train.csv + extra URLs (`pipeline.py --data train+extra`) against the run trained on train.csv only.

    PYTHONPATH=src .venv/bin/python -m tools.extra_data_report RUN_ID [--baseline v3_20261109T0956_visitor-platform] [--out docs/report/extra_data.json]

Writes: rows per source and class of the extra data; overlap checks of the extra URLs with test.csv / external_test.csv (identical after the task's normalisation, and same registrable
website); rows the corpus builder removed for overlap (data/additional/corpus.json); and the comparison with the baseline on identical URLs: out-of-fold AUC and recall at 1% FPR on the
train.csv rows, AUC and recall at a 1% false-positive rate on test / external with a paired cluster bootstrap over websites (1,000 draws), plus each run's metrics at its own threshold
(tools.report_numbers, to docs/report/final_metrics_extra.json and final_metrics_baseline.json)."""
import argparse
import json
import pathlib
import subprocess
import sys

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

from common import ADDITIONAL, ROOT, host_group, load, norm_key, run_dir, training_data


def rec_at(y, s, fpr=0.01):
    t = np.quantile(s[y == 0], 1 - fpr)
    return float((s[y == 1] > t).mean())


def paired(a, b, cand_a, cand_b, B=1000, seed=0):
    y, sa, sb = a.y.values, a[cand_a].values, b[cand_b].values
    g = pd.factorize(a.url.map(host_group))[0]
    idx = [np.flatnonzero(g == k) for k in range(g.max() + 1)]
    rng, da, dr = np.random.default_rng(seed), [], []
    for _ in range(B):
        i = np.concatenate([idx[k] for k in rng.integers(0, len(idx), len(idx))])
        if y[i].min() == y[i].max():
            continue
        da.append(roc_auc_score(y[i], sb[i]) - roc_auc_score(y[i], sa[i]))
        dr.append(rec_at(y[i], sb[i]) - rec_at(y[i], sa[i]))
    ci = lambda v: [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]
    return {"auc": [float(roc_auc_score(y, sa)), float(roc_auc_score(y, sb))], "auc_diff_ci": ci(da),
            "recall_at_1pct_fpr": [rec_at(y, sa), rec_at(y, sb)], "recall_diff_ci": ci(dr)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("--baseline", default="v3_20261109T0956_visitor-platform", help="the parts run trained on train.csv only")
    ap.add_argument("--out", default=str(ROOT / "docs" / "report" / "extra_data.json"))
    a = ap.parse_args()
    d = training_data(a.run)
    extra = d[d.source != "task_train"]
    ev = {n: load(n) for n in ("test", "external_test")}
    keys = set(pd.concat([e.url for e in ev.values()]).map(norm_key))
    hosts_train, hosts_all = set(load("train").url.map(host_group)), set(d.url.map(host_group))
    corpus = json.loads((ADDITIONAL / "corpus.json").read_text())
    env = {**__import__("os").environ, "PYTHONPATH": str(ROOT / "src")}
    out = pathlib.Path(a.out)
    for r, name in ((a.run, "final_metrics_extra.json"), (a.baseline, "final_metrics_baseline.json")):
        subprocess.run([sys.executable, "-m", "tools.report_numbers", r, "--out", str(out.with_name(name))], check=True, cwd=ROOT, env=env, stdout=subprocess.DEVNULL)
    ca, cb = (json.loads((run_dir(r) / "config.json").read_text())["deployed_candidate"] for r in (a.baseline, a.run))
    oa, ob = pd.read_csv(run_dir(a.baseline) / "scores_oof.csv"), pd.read_csv(run_dir(a.run) / "scores_oof.csv")
    tr = load("train")
    obt = ob.iloc[:len(tr)]
    assert (obt.url.values == tr.url.values).all() and (oa.url.values == tr.url.values).all(), "train.csv rows are not the first rows of both runs"
    cmp = {"train_csv_rows_oof": {"auc": [float(roc_auc_score(oa.y, oa[ca])), float(roc_auc_score(obt.y, obt[cb]))],
                                  "recall_at_1pct_fpr": [rec_at(oa.y.values, oa[ca].values), rec_at(obt.y.values, obt[cb].values)]}}
    for n in ("test", "external_test"):
        sa, sb = pd.read_csv(run_dir(a.baseline) / f"scores_{n}.csv"), pd.read_csv(run_dir(a.run) / f"scores_{n}.csv")
        assert (sa.url == sb.url).all()
        cmp[n] = paired(sa, sb, ca, cb)
    R = {"run": a.run, "baseline": a.baseline, "rows": len(d), "train_rows": int((d.source == "task_train").sum()), "extra_rows": len(extra),
         "ratio": len(extra) / int((d.source == "task_train").sum()), "extra_phishing_share": float(extra.label.mean()),
         "extra_by_source": extra.groupby("source").size().to_dict(), "n_sources": int(extra.source.nunique()),
         "extra_rows_matching_an_evaluation_url": int(extra.url.map(norm_key).isin(keys).sum()),
         "corpus_rows_removed_for_overlap": sum(s.get("removed_overlap_with_test_external_pool", 0) for k, s in corpus["sources"].items() if k != "task_train"),
         "host_share": {n: {"train_only": float(e.url.map(host_group).isin(hosts_train).mean()), "train_plus_extra": float(e.url.map(host_group).isin(hosts_all).mean())}
                        for n, e in ev.items()},
         "comparison": cmp, "metrics_file": str(out.with_name("final_metrics_extra.json")), "baseline_metrics_file": str(out.with_name("final_metrics_baseline.json"))}
    out.write_text(json.dumps(R, indent=1))
    print(json.dumps({k: v for k, v in R.items() if k not in ("extra_by_source",)}, indent=1)[:2500])


if __name__ == "__main__":
    main()
