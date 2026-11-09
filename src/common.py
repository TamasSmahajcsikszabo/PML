"""Shared data handling for train / evaluate."""
import hashlib
import pathlib
import re

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]  # repo root (this file lives in src/)
DATA = ROOT / "data"  # holds only train.csv, test.csv, external_test.csv
ADDITIONAL = DATA / "additional"  # everything derived or downloaded: corpus, master_all, shards, caches
RESULTS = ROOT / "src" / "models" / "results"
SEED = 0


def norm_key(url):
    """The task's own 'same page' key: lower-case, no scheme, no leading www., no trailing slash."""
    return re.sub(r"^www\.", "", re.sub(r"^[a-z][a-z0-9+.-]*://", "", str(url).strip().lower())).rstrip("/")


def host_group(url):
    """Registrable-domain-like group so one site never sits on both sides of a split."""
    host = re.sub(r"^[a-z][a-z0-9+.-]*://", "", str(url).strip().lower()).split("/")[0].split("?")[0].split("#")[0]
    host = host.rsplit("@", 1)[-1].split(":")[0].removeprefix("www.")
    lab = host.split(".")
    if len(lab) >= 3 and len(lab[-1]) == 2 and lab[-2] in {"co", "com", "org", "net", "gov", "ac", "edu"}:
        return ".".join(lab[-3:])
    return ".".join(lab[-2:])


def load(name):
    return pd.read_csv(DATA / f"{name}.csv")


def clean_train(df):
    """Drop conflicting-label keys entirely, then keep one row per normalised url. Returns (clean, report)."""
    d = df.assign(key=df.url.map(norm_key))
    exact_dup = int(d.url.duplicated().sum())
    conflict = d.groupby("key").label.transform("nunique") > 1
    d = d[~conflict]
    dup = int(d.key.duplicated().sum())
    out = d.drop_duplicates("key").drop(columns="key").reset_index(drop=True)
    return out, {"rows": len(df), "exact_duplicate_rows": exact_dup, "conflicting_label_rows": int(conflict.sum()),
                 "same_label_duplicates_after_conflicts_removed": dup, "kept": len(out)}


def sha256(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def run_dir(run_id=None):
    """models/results/{run_id}; the latest run if run_id is None."""
    return RESULTS / (run_id or (RESULTS / "LATEST").read_text().strip())


def load_train_plus_extra(ratio=2.0, seed=SEED):
    """train.csv exactly as supplied + ratio x its size of extra public URLs from data/additional/corpus.csv (its public sources only, not its cleaned copy of train.csv),
    half phishing and half legitimate, sampled with a fixed seed. Extra rows that repeat a train.csv URL under the task's normalisation are dropped first; the corpus builder already
    removed everything in test.csv / external_test.csv / the --test pool, and that is asserted again here."""
    tr = load("train").assign(source="task_train")
    c = load_corpus()
    c = c[c.source != "task_train"]
    c = c[~c.url.map(norm_key).isin(set(tr.url.map(norm_key)))]
    held_out = set(pd.concat([load("test").url, load("external_test").url]).map(norm_key))
    assert not c.url.map(norm_key).isin(held_out).any(), "extra data overlaps an evaluation file"
    per_class = int(round(ratio * len(tr))) // 2
    extra = pd.concat([c[c.label == lab].sample(per_class, random_state=seed) for lab in (0, 1)])
    return pd.concat([tr, extra[["url", "label", "source"]]]).reset_index(drop=True)


def training_data(run_id=None):
    """The rows a run was trained on (url, label, source), rebuilt from its config: train.csv as supplied, or train.csv + extra public URLs (same seed, same ratio)."""
    import json
    d = run_dir(run_id)
    cfg = json.loads((d / "config.json").read_text())
    if cfg.get("parent"):  # a parts run: its parent holds the training data
        cfg = json.loads((run_dir(cfg["parent"]) / "config.json").read_text())
    data = cfg.get("data", "train")
    if data == "train":
        return load("train").assign(source="task_train")
    if data == "train+extra":
        rows = cfg["corpus"]["rows"]
        return load_train_plus_extra((rows - len(load("train"))) / len(load("train")))
    return load_corpus()


def load_corpus():
    """Training corpus built by tools/build_corpus.py: url, label, source (train.csv + public collections, evaluation sets excluded)."""
    return pd.read_csv(ADDITIONAL / "corpus.csv")
