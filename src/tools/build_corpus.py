"""Build the training corpus data/additional/corpus.csv (url,label,source) from the task's train.csv plus public collections.

    PYTHONPATH=src .venv/bin/python src/tools/build_corpus.py --raw DIR      (about 2 minutes)

DIR must hold the downloads (see CLAUDE.md for the URLs):
    kaggle_d1/phishing_site_urls.csv        Kaggle taruntiwarihp/phishing-site-urls (Jalil et al. D1; ExpertFusion TR-3)       URL,Label (bad/good)
    ds/somanshumahajan_65-lakh-.../urls_*.csv   Kaggle somanshumahajan/65-lakh-urls-labelled-as-1-and-0 (ExpertFusion footnote)   url,label (1 = phishing)
    ds/harisudhan411_.../new_data_urls.csv  Kaggle harisudhan411/phishing-and-legitimate-urls (hybrid-paper dataset 6)          url,status (0 = phishing, 1 = legitimate)
    ds/samahsadiq_.../balanced_urls.csv     Kaggle samahsadiq/benign-and-malicious-urls (hybrid-paper dataset 5), BENIGN rows only  url,label,result
    ds/ebbu/data_{phishing_37175,legitimate_36400}.json   Ebbu2017 (github.com/ebubekirbbr/pdd; Jalil et al. D6)
    ../url_grammar/data/master.csv + data/neutral/*_sample.txt   B's consolidation: PhishTank / OpenPhish / Phishing.Database feeds (phishing),
                                                                  Tranco homepages and a Common Crawl sample (neutral)
URL strings are never edited (rows with CR / LF / TAB / NUL or no text are dropped). Removed before sampling: every URL whose task-normalised key appears in
test.csv, external_test.csv or deliverables/data/unseen_pool.csv (the `--test` demo pool); duplicates across sources (first source in PRIORITY wins) and URLs listed with both labels.
Each source contributes at most CAP URLs per class (Tranco homepages fewer: they are bare homepages and would teach "no path = clean")."""
import argparse
import glob
import json
import pathlib

import pandas as pd

from common import ADDITIONAL, ROOT, clean_train, host_group, load, norm_key

CAP, SEED = 5000, 0
CAPS = {"b_tranco": 3000}
PRIORITY = ["task_train", "ebbu2017", "hari_kaggle", "malibari_benign", "kaggle_d1", "lakh_kaggle", "b_commoncrawl", "b_feeds", "b_tranco"]
BAD = ("\r", "\n", "\t", "\x00")


def read_sources(raw, b_root):
    S = {}
    S["task_train"] = clean_train(load("train"))[0][["url", "label"]]
    d = pd.read_csv(raw / "kaggle_d1" / "phishing_site_urls.csv")
    S["kaggle_d1"] = pd.DataFrame({"url": d.URL, "label": (d.Label == "bad").astype(int)})
    files = sorted(glob.glob(str(raw / "ds" / "somanshumahajan*" / "urls_*.csv")))[:8]  # 800k rows is plenty for a 5,000-per-class sample
    d = pd.concat([pd.read_csv(f, usecols=["url", "label"]) for f in files])
    S["lakh_kaggle"] = pd.DataFrame({"url": d.url, "label": d.label.astype(int)})
    d = pd.read_csv(glob.glob(str(raw / "ds" / "harisudhan*" / "new_data_urls.csv"))[0])
    S["hari_kaggle"] = pd.DataFrame({"url": d.url, "label": (d.status == 0).astype(int)})  # status 0 = phishing
    d = pd.read_csv(glob.glob(str(raw / "ds" / "samahsadiq*" / "balanced_urls.csv"))[0])
    S["malibari_benign"] = pd.DataFrame({"url": d.url[d.label == "benign"], "label": 0})  # the malicious half mixes phishing, malware and defacement
    ph = json.load(open(raw / "ds" / "ebbu" / "data_phishing_37175.json"))
    lg = json.load(open(raw / "ds" / "ebbu" / "data_legitimate_36400.json"))
    S["ebbu2017"] = pd.DataFrame({"url": ph + lg, "label": [1] * len(ph) + [0] * len(lg)})
    m = pd.read_csv(b_root / "data" / "master.csv", dtype={"url": str})
    m = m.rename(columns={"phishing": "label"})
    S["b_feeds"] = m[m.label == 1]
    S["b_tranco"] = m[m.label == 0]
    S["b_commoncrawl"] = pd.DataFrame({"url": [l.rstrip("\n") for p in sorted(glob.glob(str(b_root / "data" / "neutral" / "*_sample.txt"))) for l in open(p, encoding="utf-8")], "label": 0})
    return S


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True, type=pathlib.Path)
    ap.add_argument("--b-root", type=pathlib.Path, default=ROOT.parent / "url_grammar")
    a = ap.parse_args()
    S = read_sources(a.raw, a.b_root)

    pool = pd.read_csv(ROOT / "deliverables" / "data" / "unseen_pool.csv")
    reserved = {n: set(load(n).url.map(norm_key)) for n in ("test", "external_test")} | {"unseen_pool": set(pool.url.map(norm_key))}
    reserved_keys = set().union(*reserved.values())
    eval_hosts = set(pd.concat([load("test"), load("external_test")]).url.map(host_group))

    seen, parts, report = set(), [], {}
    for name in PRIORITY:
        d = S[name].dropna(subset=["url"]).astype({"url": str})
        d = d[d.url.str.strip().ne("") & ~d.url.str.contains("|".join(BAD), regex=True)]
        d = d.assign(key=d.url.map(norm_key))
        n0 = len(d)
        d = d[~d.key.isin(reserved_keys)]
        n_reserved = n0 - len(d)
        conflict = d.groupby("key").label.transform("nunique") > 1
        d = d[~conflict].drop_duplicates("key")
        n_cross = int(d.key.isin(seen).sum())
        d = d[~d.key.isin(seen)]
        cap = CAPS.get(name, CAP)
        d = pd.concat([g.sample(min(len(g), cap), random_state=SEED) if name != "task_train" else g for _, g in d.groupby("label")])
        seen |= set(d.key)
        parts.append(d.assign(source=name))
        report[name] = {"rows_read": n0, "removed_overlap_with_test_external_pool": n_reserved, "removed_label_conflicts": int(conflict.sum()), "removed_duplicate_of_earlier_source": n_cross,
                        "phishing": int((d.label == 1).sum()), "neutral": int((d.label == 0).sum()), "share_with_scheme": float(d.url.str.contains("://").mean())}
        print(name, report[name], flush=True)
    corpus = pd.concat(parts)[["url", "label", "source"]].sample(frac=1, random_state=SEED).reset_index(drop=True)
    corpus.to_csv(ADDITIONAL / "corpus.csv", index=False)
    info = {"rows": len(corpus), "phishing": int(corpus.label.sum()), "sources": report, "cap_per_class": CAP, "caps_override": CAPS, "seed": SEED,
            "corpus_hosts_also_in_test_or_external": float(corpus.url.map(host_group).isin(eval_hosts).mean())}
    json.dump(info, open(ADDITIONAL / "corpus.json", "w"), indent=2)
    print(json.dumps({k: v for k, v in info.items() if k != "sources"}, indent=1))


if __name__ == "__main__":
    main()
