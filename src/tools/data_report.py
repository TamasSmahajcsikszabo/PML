"""Data inspection and overlap facts for the report (task: data issues, overlap with training under several definitions, URL characteristics per set and class).

    PYTHONPATH=src .venv/bin/python -m tools.data_report [--out docs/report/data_facts.json]

Reads data/train.csv, test.csv, external_test.csv as supplied (nothing is changed or written back). Prints markdown tables and writes all numbers to a json file."""
import argparse
import json
import pathlib
from urllib.parse import urlsplit

import numpy as np
import pandas as pd

import urlfeat

from common import DATA, host_group, norm_key, training_data

SETS = ["train", "test", "external_test"]


def parts(u):
    s = urlsplit(u if "://" in u else "//" + u)
    return s.scheme.lower(), (s.hostname or "").lower(), s.path, s.query, s.fragment


def keys(df):
    """the several 'same page' definitions, from strict to loose"""
    k = pd.DataFrame({"exact": df.url, "task_norm": df.url.map(norm_key)})
    pp = df.url.map(parts)
    host = pp.map(lambda t: t[1].removeprefix("www."))
    k["norm_no_query"] = [f"{h}{p.rstrip('/')}" for h, (s, _, p, q, f) in zip(host, pp)]  # task rule + query and fragment dropped
    k["host_first_segment"] = [f"{h}/{p.strip('/').split('/')[0]}" for h, (s, _, p, q, f) in zip(host, pp)]
    k["registrable_host"] = df.url.map(host_group)
    return k


def characteristics(df):
    pp = df.url.map(parts)
    out = {}
    for lab, name in ((1, "phishing"), (0, "legitimate")):
        m = (df.label == lab).values
        sub, p = df.url[m], pp[m]
        out[name] = {"n": int(m.sum()),
                     "https": float(np.mean([t[0] == "https" for t in p])),
                     "no_scheme": float(np.mean([t[0] == "" for t in p])),
                     "has_path": float(np.mean([t[2].strip("/") != "" for t in p])),
                     "has_query": float(np.mean([t[3] != "" for t in p])),
                     "www": float(np.mean([t[1].startswith("www.") for t in p])),
                     "ip_host": float(np.mean([t[1].replace(".", "").isdigit() for t in p])),
                     "median_len": float(sub.str.len().median()),
                     "p90_len": float(sub.str.len().quantile(0.9))}
    return out


FEATURE_SHARES = ["reg_popular", "https", "www", "host_ipv4", "tld_suspicious", "is_shortener", "sfx_platform", "emb_domain", "has_query"]


def feature_shares(df):
    """share of URLs with a property, by class, from the visitor's feature columns"""
    X = urlfeat.featurize(df.url.tolist())
    X["suspicious_phrase"] = X.sw_phrase_url > 0
    X["brand_in_path_or_query"] = (X.brand_in_path > 0) | (X.brand_in_query > 0)
    X["digit_rate_host_gt_0.1"] = X.host_digit_rate > 0.1
    X["two_or_more_subdomains"] = np.expm1(X.n_sub) >= 2
    cols = FEATURE_SHARES + ["suspicious_phrase", "brand_in_path_or_query", "digit_rate_host_gt_0.1", "two_or_more_subdomains"]
    return {("phishing" if l else "legitimate"): {c: float(X.loc[df.label.values == l, c].astype(float).mean()) for c in cols} for l in (1, 0)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="docs/report/data_facts.json")
    ap.add_argument("--run", default=None, help="overlap is measured against the rows this run was trained on (default: the promoted run)")
    a = ap.parse_args()
    D = {n: pd.read_csv(DATA / f"{n}.csv") for n in SETS}
    F = {"sets": {}, "train_issues": {}, "overlap": {}}
    for n, d in D.items():
        F["sets"][n] = {"rows": len(d), "phishing_share": float(d.label.mean()), **characteristics(d)}
    F["feature_shares"] = {n: feature_shares(d) for n, d in D.items()}
    tr = D["train"]
    kt = keys(tr)
    iss = F["train_issues"]
    iss["rows"] = len(tr)
    iss["exact_duplicate_rows"] = int(tr.duplicated(["url", "label"]).sum())
    iss["rows_repeating_an_earlier_url"] = int(tr.duplicated("url").sum())
    g = tr.groupby("url").label.nunique()
    iss["urls_with_conflicting_labels_exact"] = int((g > 1).sum())
    iss["rows_of_conflicting_urls_exact"] = int(tr.url.isin(g[g > 1].index).sum())
    gn = tr.assign(k=kt.task_norm).groupby("k").label.nunique()
    iss["keys_with_conflicting_labels_task_norm"] = int((gn > 1).sum())
    iss["rows_of_conflicting_keys_task_norm"] = int(tr.assign(k=kt.task_norm).k.isin(gn[gn > 1].index).sum())
    iss["extra_rows_duplicated_under_task_norm"] = int(kt.task_norm.duplicated().sum())
    iss["rows_without_scheme"] = int((~tr.url.str.contains("://")).sum())
    iss["hosts_in_train"] = int(kt.registrable_host.nunique())
    iss["largest_host_groups"] = kt.registrable_host.value_counts().head(5).to_dict()
    iss["rows_in_hosts_with_5_or_more_rows"] = int(kt.registrable_host.map(kt.registrable_host.value_counts()).ge(5).sum())
    trn = training_data(a.run)  # the rows the run was actually trained on (train.csv, or train.csv + extra public URLs)
    kr = keys(trn)
    F["training_rows"], F["training_sources"] = len(trn), trn.groupby("source").size().to_dict()
    for n in ("test", "external_test"):
        k, o = keys(D[n]), {}
        for defn in kt.columns:
            hit = k[defn].isin(set(kr[defn]))
            o[defn] = {"share_of_rows": float(hit.mean()), "phishing": float(hit[D[n].label == 1].mean()), "legitimate": float(hit[D[n].label == 0].mean())}
        # when a row matches a training row under the task's rule, do the labels agree?
        m = trn.assign(k=kr.task_norm).groupby("k").label.agg(lambda s: s.mode().iloc[0])
        hit = k.task_norm.isin(m.index)
        o["task_norm_label_agreement"] = float((D[n].label[hit].values == m.reindex(k.task_norm[hit]).values).mean()) if hit.any() else None
        F["overlap"][n] = o
    ke = keys(D["external_test"])
    kx = keys(D["test"])
    F["overlap"]["test_vs_external"] = {d: float(kx[d].isin(set(ke[d])).mean()) for d in kt.columns}
    pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    json.dump(F, open(a.out, "w"), indent=1)
    print(json.dumps(F["train_issues"], indent=1))
    print("\n| set | class | n | https | has path | has query | www | IP host | median len | p90 len |\n|---|---|---|---|---|---|---|---|---|---|")
    for n in SETS:
        for c in ("phishing", "legitimate"):
            r = F["sets"][n][c]
            print(f"| {n} | {c} | {r['n']} | {r['https']:.2f} | {r['has_path']:.2f} | {r['has_query']:.2f} | {r['www']:.2f} | {r['ip_host']:.3f} | {r['median_len']:.0f} | {r['p90_len']:.0f} |")
    print("\n| evaluation set | " + " | ".join(kt.columns) + " |\n|---|" + "---|" * len(kt.columns))
    for n in ("test", "external_test"):
        print(f"| {n} | " + " | ".join(f"{F['overlap'][n][d]['share_of_rows']:.3f}" for d in kt.columns) + " |")
    print("task-norm label agreement:", {n: F["overlap"][n]["task_norm_label_agreement"] for n in ("test", "external_test")})
    print("test vs external:", F["overlap"]["test_vs_external"])


if __name__ == "__main__":
    main()
