"""Consolidate EVERY collection into one file in url_grammar's master.csv format (two columns: url,phishing), uncapped.

    PYTHONPATH=src .venv/bin/python src/tools/build_master_all.py --raw DIR      (streaming, low memory; about 10-20 minutes)

Writes data/master_all.csv        url,phishing                 (1 = phishing)
       data/master_all.sources.csv   source                       (one line per row of master_all.csv, same order: which collection the row came from)
       data/master_all.json          provenance and counts per source
Inputs and sources as in tools/build_corpus.py (task train.csv, Ebbu2017, three Kaggle collections incl. all 61 files of the 65-lakh set, the Malibari benign half,
B's master.csv split into feeds (phishing) and Tranco homepages (neutral), B's Common Crawl sample).
URL strings are written exactly as read (rows with CR / LF / TAB / NUL or no text are dropped). Removed: every URL whose task-normalised key is in test.csv,
external_test.csv or the `--test` pool; keys listed with both labels (anywhere); and repeats of a key (the first source in PRIORITY keeps it).
Two passes over the sources: pass 1 only hashes the normalised keys (64-bit) to decide what to keep, pass 2 writes the kept rows."""
import argparse
import glob
import json
import pathlib

import numpy as np
import pandas as pd

from common import ADDITIONAL, ROOT, load

PRIORITY = ["task_train", "ebbu2017", "hari_kaggle", "malibari_benign", "kaggle_d1", "lakh_kaggle", "b_commoncrawl", "b_feeds", "b_tranco"]
BAD = "\r|\n|\t|\x00"
CHUNK = 500_000


def keys(urls):
    """Task-normalised key (lower-case, no scheme, no leading www., no trailing slash) as a 64-bit hash; identical to common.norm_key."""
    k = urls.str.strip().str.lower().str.replace(r"^[a-z][a-z0-9+.\-]*://", "", regex=True).str.replace(r"^www\.", "", regex=True).str.rstrip("/")
    return pd.util.hash_pandas_object(k, index=False).values


def stream(raw, b_root):
    """Yield (source, DataFrame[url, label]) chunks in PRIORITY order; cleaned the same way in both passes."""
    def clean(d):
        d = d.dropna(subset=["url"]).astype({"url": str})
        return d[d.url.str.strip().ne("") & ~d.url.str.contains(BAD, regex=True)][["url", "label"]]

    yield "task_train", clean(load("train"))
    ph, lg = (json.load(open(raw / "ds" / "ebbu" / f)) for f in ("data_phishing_37175.json", "data_legitimate_36400.json"))
    yield "ebbu2017", clean(pd.DataFrame({"url": ph + lg, "label": [1] * len(ph) + [0] * len(lg)}))
    for c in pd.read_csv(glob.glob(str(raw / "ds" / "harisudhan*" / "new_data_urls.csv"))[0], chunksize=CHUNK):
        yield "hari_kaggle", clean(pd.DataFrame({"url": c.url, "label": (c.status == 0).astype(int)}))  # status 0 = phishing
    for c in pd.read_csv(glob.glob(str(raw / "ds" / "samahsadiq*" / "balanced_urls.csv"))[0], chunksize=CHUNK):
        c = c[c.label == "benign"]  # the malicious half mixes phishing, malware and defacement
        yield "malibari_benign", clean(pd.DataFrame({"url": c.url, "label": 0}))
    for c in pd.read_csv(raw / "kaggle_d1" / "phishing_site_urls.csv", chunksize=CHUNK):
        yield "kaggle_d1", clean(pd.DataFrame({"url": c.URL, "label": (c.Label == "bad").astype(int)}))
    for f in sorted(glob.glob(str(raw / "ds" / "somanshumahajan*" / "urls_*.csv")), key=lambda p: int(pathlib.Path(p).stem.split("_")[1])):
        for c in pd.read_csv(f, usecols=["url", "label"], chunksize=CHUNK):
            yield "lakh_kaggle", clean(pd.DataFrame({"url": c.url, "label": c.label.astype(int)}))  # 1 = phishing
    cc = [l.rstrip("\n") for p in sorted(glob.glob(str(b_root / "data" / "neutral" / "*_sample.txt"))) for l in open(p, encoding="utf-8")]
    yield "b_commoncrawl", clean(pd.DataFrame({"url": cc, "label": 0}))
    feeds, tranco = [], []
    for c in pd.read_csv(b_root / "data" / "master.csv", chunksize=CHUNK, dtype={"url": str}):
        c = c.rename(columns={"phishing": "label"})
        yield "b_feeds", clean(c[c.label == 1])
    for c in pd.read_csv(b_root / "data" / "master.csv", chunksize=CHUNK, dtype={"url": str}):
        c = c.rename(columns={"phishing": "label"})
        yield "b_tranco", clean(c[c.label == 0])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True, type=pathlib.Path)
    ap.add_argument("--b-root", type=pathlib.Path, default=ROOT.parent / "url_grammar")
    a = ap.parse_args()

    reserved = np.unique(np.concatenate([keys(load("test").url), keys(load("external_test").url), keys(pd.read_csv(ROOT / "deliverables" / "data" / "unseen_pool.csv").url)]))
    H, L, S = [], [], []
    for src, d in stream(a.raw, a.b_root):  # pass 1
        H.append(keys(d.url)); L.append(d.label.values.astype(np.int8)); S.append(np.full(len(d), PRIORITY.index(src), dtype=np.int8))
    H, L, S = np.concatenate(H), np.concatenate(L), np.concatenate(S)
    print("pass 1:", len(H), "rows read", flush=True)
    t = pd.DataFrame({"h": H, "l": L})
    is_reserved = np.isin(H, reserved)
    conflict = (t.groupby("h").l.transform("nunique") > 1).values
    dup = t.assign(skip=is_reserved | conflict).loc[~(is_reserved | conflict)].duplicated("h", keep="first")
    keep = np.zeros(len(H), dtype=bool)
    keep[dup.index[~dup.values]] = True
    del t
    report = {}
    for i, name in enumerate(PRIORITY):
        m = S == i
        report[name] = {"rows_read": int(m.sum()), "removed_overlap_with_test_external_pool": int((m & is_reserved).sum()), "removed_label_conflicts": int((m & conflict & ~is_reserved).sum()),
                        "removed_duplicates_of_earlier_rows": int((m & ~is_reserved & ~conflict & ~keep).sum()), "kept_phishing": int((m & keep & (L == 1)).sum()), "kept_neutral": int((m & keep & (L == 0)).sum())}
        print(name, report[name], flush=True)

    out = ADDITIONAL
    pos = 0
    with open(out / "master_all.csv", "w", encoding="utf-8", newline="") as fm, open(out / "master_all.sources.csv", "w", encoding="utf-8") as fs:
        fm.write("url,phishing\n"); fs.write("source\n")
        first = True
        for src, d in stream(a.raw, a.b_root):  # pass 2
            k = keep[pos:pos + len(d)]; pos += len(d)
            d = d[k]
            d.rename(columns={"label": "phishing"}).to_csv(fm, header=False, index=False)
            fs.write(("\n".join([src] * len(d)) + "\n") if len(d) else "")
    assert pos == len(H), "the two passes read different row counts"
    info = {"rows": int(keep.sum()), "phishing": int((keep & (L == 1)).sum()), "neutral": int((keep & (L == 0)).sum()), "rows_read": int(len(H)), "sources": report,
            "format": "url,phishing (as url_grammar/data/master.csv); sources in master_all.sources.csv, same row order"}
    json.dump(info, open(out / "master_all.json", "w"), indent=2)
    print(json.dumps({k: v for k, v in info.items() if k != "sources"}, indent=1))


if __name__ == "__main__":
    main()
