"""Build the small unseen-URL pool used by `deliverables/predict.py --test` from the Kaggle dataset
taruntiwarihp/phishing-site-urls (Jalil et al. 2023's "D1"; 549,346 URLs, `URL,Label` with Label good/bad, ODbL licence, URLs have no scheme).

    PYTHONPATH=src .venv/bin/python src/tools/build_unseen_pool.py PATH/TO/phishing_site_urls.csv

Steps: drop rows whose task-normalised URL (lower-case, no scheme, no leading www., no trailing slash) appears in train.csv, test.csv or
external_test.csv; drop duplicates and URLs listed with both labels; then draw a seeded random pool (phishing = "bad" -> 1, neutral = "good" -> 0).
Writes deliverables/data/unseen_pool.csv (url,label) and deliverables/data/unseen_pool.json (provenance and the overlap measured)."""
import json
import sys

import pandas as pd

from common import ROOT, host_group, load, norm_key

N_PHISH, N_NEUTRAL, SEED = 1000, 4000, 0
raw = pd.read_csv(sys.argv[1]).rename(columns={"URL": "url", "Label": "label"})
raw["label"] = (raw.label == "bad").astype(int)
raw["key"] = raw.url.map(norm_key)

known = {n: load(n) for n in ("train", "test", "external_test")}
known_keys = {n: set(d.url.map(norm_key)) for n, d in known.items()}
known_hosts = set().union(*[set(d.url.map(host_group)) for d in known.values()])
overlap = {n: int(raw.key.isin(k).sum()) for n, k in known_keys.items()}

d = raw[~raw.key.isin(set().union(*known_keys.values()))]
conflict = d.groupby("key").label.transform("nunique") > 1
d = d[~conflict].drop_duplicates("key")
pool = pd.concat([d[d.label == 1].sample(N_PHISH, random_state=SEED), d[d.label == 0].sample(N_NEUTRAL, random_state=SEED)]).sample(frac=1, random_state=SEED)
pool[["url", "label"]].to_csv(ROOT / "deliverables" / "data" / "unseen_pool.csv", index=False)
info = {"source": "https://www.kaggle.com/datasets/taruntiwarihp/phishing-site-urls (ODbL)", "source_rows": len(raw), "source_phishing": int(raw.label.sum()),
        "removed_overlap_with_supplied_sets": overlap, "removed_label_conflicts": int(conflict.sum()), "unique_after_cleaning": len(d),
        "pool_phishing": N_PHISH, "pool_neutral": N_NEUTRAL, "seed": SEED,
        "pool_hosts_also_in_supplied_sets": {"phishing": float(pool[pool.label == 1].url.map(host_group).isin(known_hosts).mean()),
                                              "neutral": float(pool[pool.label == 0].url.map(host_group).isin(known_hosts).mean())}}
json.dump(info, open(ROOT / "deliverables" / "data" / "unseen_pool.json", "w"), indent=2)
print(json.dumps(info, indent=2))
