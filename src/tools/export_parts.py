"""Write the parsed parts of sampled train.csv URLs to a csv (one row per URL, URLs as supplied).

    PYTHONPATH=src .venv/bin/python -m tools.export_parts [--n 50] [--seed 1] [--out docs/analysis/url_parts_50.csv]

Half phishing, half legitimate. List-valued parts are joined with ' | '."""
import argparse

import pandas as pd

from common import DATA
from urlfeat import structure


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=50)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--out", default="docs/analysis/url_parts_50.csv")
    a = ap.parse_args()
    t = pd.read_csv(DATA / "train.csv")
    s = pd.concat([g.sample(a.n // 2, random_state=a.seed) for _, g in t.groupby("label")]).sample(frac=1, random_state=a.seed)
    rows = []
    for url, label in zip(s.url, s.label):
        p = structure(url)
        if p is None:
            rows.append({"url": url, "label": label, "rejected_by_grammar": True})
            continue
        j = " | ".join
        rows.append({"url": url, "label": label, "scheme": p["scheme"], "userinfo": p["userinfo"], "host": p["host"], "host_kind": p["host_kind"], "subdomains": j(p["subdomains"]),
                     "registrable": p["reg"], "suffix": p["suffix"], "suffix_kind": p["suffix_kind"], "port": p["port"], "path": p["path"], "segments": j(p["segs"]),
                     "file_ext": p["file_ext"], "query": p["query"], "query_keys": j(p["qkeys"]), "query_values": j(p["qvals"]),
                     "fragment": p["fragment"], "pct_escapes": p["pct"], "stray_pct": p["stray_pct"], "punycode_labels": p["punycode"], "amp_escapes": p["amp_esc"],
                     "nested_urls": p["nested"], "emails": p["email"], "rejected_by_grammar": False})
    pd.DataFrame(rows).to_csv(a.out, index=False)
    print(len(rows), "rows ->", a.out)


if __name__ == "__main__":
    main()
