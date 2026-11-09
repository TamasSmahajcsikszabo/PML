"""Freeze the output of the legacy extractor (tools/legacy_urlfeat, the code before the URLVisitor refactor) for a fixed URL set:
train.csv, test.csv, external_test.csv (14,367 URLs) + 5,000 random corpus URLs (seed 0).  Writes data/additional/visitor_oracle/{name}.pkl = (features DataFrame, host frame, parts frame).
Run in its own process (it loads the OLD parser):   PYTHONPATH=src .venv/bin/python -m tools.legacy_oracle"""
import joblib
import numpy as np
import pandas as pd

from common import ADDITIONAL, load, load_corpus
from tools.legacy_urlfeat import featurize, COLUMNS
from tools.legacy_urlfeat import parts as P

OUT = ADDITIONAL / "visitor_oracle"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sets = {n: load(n).url.tolist() for n in ("train", "test", "external_test")}
    if (ADDITIONAL / "corpus.csv").exists():  # optional: the corpus is not shipped (data/ is git-ignored); the three supplied files are enough
        sets["corpus_sample"] = load_corpus().url.sample(5000, random_state=0).tolist()
    for name, urls in sets.items():
        X = featurize(urls)
        H, parts = P.tables(urls)
        joblib.dump({"urls": urls, "features": X, "host": H, "parts": parts, "columns": COLUMNS}, OUT / f"{name}.pkl")
        print(name, len(urls), X.shape, H.shape, parts.shape, "rejected:", int(X.isna().all(axis=1).sum()), flush=True)


if __name__ == "__main__":
    main()
