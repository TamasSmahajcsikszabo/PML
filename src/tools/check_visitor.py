"""Compare URLVisitor output with the frozen output of the legacy extractor (data/additional/visitor_oracle/, made by tools.legacy_oracle) and time the extraction.

    PYTHONPATH=src .venv/bin/python -m tools.check_visitor [--sets train test external_test corpus_sample] [--examples 3] [--out docs/analysis/visitor_agreement.md]

Per feature column: number of URLs whose value differs (|diff| > 1e-12 or NaN mismatch), mean |diff| over the differing URLs, example URLs with both values.
Per part column: the same on the parts tables (rows aligned by URL row and order within the URL); a different number of parts for a URL counts as one differing URL."""
import argparse
import time

import joblib
import numpy as np
import pandas as pd

import urlfeat
from common import ADDITIONAL

OUT = ADDITIONAL / "visitor_oracle"


def diff_columns(old, new, urls, examples):
    rows = []
    for c in old.columns:
        a, b = old[c].values.astype(float), new[c].values.astype(float)
        bad = ~((np.isnan(a) & np.isnan(b)) | (np.abs(np.nan_to_num(a) - np.nan_to_num(b)) <= 1e-12))
        if bad.any():
            idx = np.flatnonzero(bad)
            rows.append({"column": c, "n_differ": int(bad.sum()), "share": bad.mean(), "mean_abs_diff": float(np.nanmean(np.abs(a[idx] - b[idx]))),
                         "examples": [(urls[i][:90], round(float(a[i]), 5), round(float(b[i]), 5)) for i in idx[:examples]]})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sets", nargs="+", default=["train", "test", "external_test", "corpus_sample"])
    ap.add_argument("--examples", type=int, default=3)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    md, tot = [], {"n": 0, "t": 0.0}
    for name in [n for n in a.sets if (OUT / f"{n}.pkl").exists()]:  # corpus_sample only exists where the corpus was built
        o = joblib.load(OUT / f"{name}.pkl")
        urls = o["urls"]
        assert list(o["features"].columns) == urlfeat.COLUMNS, "column names / order differ from the legacy extractor"
        t = time.perf_counter()
        X, H, P = urlfeat.extract(urls, host_labels=True)
        dt = time.perf_counter() - t
        tot["n"] += len(urls)
        tot["t"] += dt
        md.append(f"## {name} ({len(urls)} URLs, {dt / len(urls) * 1000:.2f} ms per URL for features + host frame + parts)")
        rows = diff_columns(o["features"], X, urls, a.examples)
        rows += [dict(r, column="host:" + r["column"]) for r in diff_columns(o["host"], H, urls, a.examples)]
        # parts: align by (row, order inside the URL)
        hl = P[P.kind == "hlabel"]  # host-label rows are new: the legacy extractor has none
        po, pn = o["parts"].copy(), P[P.kind != "hlabel"].copy()
        for d in (po, pn):
            d["k"] = d.groupby("row").cumcount()
        m = po.merge(pn, on=["row", "k"], how="outer", suffixes=("_old", "_new"), indicator=True)
        n_count_diff = int((m._merge != "both").groupby(m.row).any().sum())
        md.append(f"parts rows: legacy {len(po)}, visitor {len(pn)} (+ {len(hl)} host-label rows, new); URLs with a different number of parts: {n_count_diff}")
        both = m[m._merge == "both"]
        for c in ["kind"] + urlfeat.PART_COLS:
            x, y = both[c + "_old"], both[c + "_new"]
            bad = (x != y) if c == "kind" else ~((np.abs(x.astype(float) - y.astype(float)) <= 1e-12))
            if bad.any():
                bi = both.index[bad][:a.examples]
                rows.append({"column": "part:" + c, "n_differ": int(bad.sum()), "share": float(bad.mean()), "mean_abs_diff": np.nan,
                             "examples": [(urls[int(both.loc[i, 'row'])][:90], both.loc[i, c + "_old"], both.loc[i, c + "_new"]) for i in bi]})
        if not rows and not n_count_diff:
            md.append("**all columns and all parts identical**")
        for r in sorted(rows, key=lambda r: -r["n_differ"]):
            md.append(f"* `{r['column']}`: {r['n_differ']} differ ({r['share']:.3%}), mean |diff| {r['mean_abs_diff']:.4g}; e.g. " + "; ".join(f"{u!r}: {x} -> {y}" for u, x, y in r["examples"]))
        md.append("")
    md.append(f"overall: {tot['n']} URLs, {tot['t'] / tot['n'] * 1000:.2f} ms per URL")
    text = "\n".join(md)
    print(text)
    if a.out:
        open(a.out, "w").write(text + "\n")


if __name__ == "__main__":
    main()
