"""Shuffle data/master_all.csv into shards and featurize every URL (all 7.8M, nothing capped), resumable.

    PYTHONPATH=src .venv/bin/python -m models.shards [--workers 6] [--only K]

1. scatter: every row goes to a random shard (seeded), so each shard is a random 1/N sample of the whole corpus -> data/shards/raw_XX.csv
2. featurize: shard by shard, in parallel (forked workers share the already loaded lists and parser) -> data/shards/shard_XX.npz with
   X (float32, one row per URL, the 141 features of urlfeat computed from the URL exactly as stored), y (phishing), src (index into build_master_all.PRIORITY),
   grp (crc32 of the registrable host: fold = grp % 5, so a site always sits in one fold, whatever shard it landed in).
Finished shards are skipped on restart. Disk: about 4.5 GB. load(i) reads one shard."""
import argparse
import multiprocessing as mp
import zlib

import numpy as np
import pandas as pd

import urlfeat
from common import ADDITIONAL, SEED, host_group
from tools.build_master_all import PRIORITY

SHARDS = ADDITIONAL / "shards"
N_SHARDS, TASK, CHUNK = 32, 4000, 500_000


def _work(urls):
    X = urlfeat.featurize(urls).fillna(0).values.astype(np.float32)
    return X, np.array([zlib.crc32(host_group(u).encode()) for u in urls], dtype=np.uint32)


def scatter():
    SHARDS.mkdir(exist_ok=True)
    for i in range(N_SHARDS):
        (SHARDS / f"raw_{i:02d}.csv").write_text("url,phishing,source\n")
    rng = np.random.default_rng(SEED)
    master = pd.read_csv(ADDITIONAL / "master_all.csv", chunksize=CHUNK, dtype={"url": str}, keep_default_na=False)
    sources = pd.read_csv(ADDITIONAL / "master_all.sources.csv", chunksize=CHUNK, dtype=str)
    for k, (m, s) in enumerate(zip(master, sources)):
        m["source"] = s.source.map(PRIORITY.index).values
        sid = rng.integers(0, N_SHARDS, len(m))
        for i in range(N_SHARDS):
            m[sid == i].to_csv(SHARDS / f"raw_{i:02d}.csv", mode="a", header=False, index=False)
        print(f"scattered {(k + 1) * CHUNK:,} rows", flush=True)


def featurize_shard(i, pool):
    raw = pd.read_csv(SHARDS / f"raw_{i:02d}.csv", dtype={"url": str}, keep_default_na=False)
    urls = raw.url.tolist()
    out = pool.map(_work, [urls[j:j + TASK] for j in range(0, len(urls), TASK)])
    tmp = SHARDS / f"tmp_{i:02d}.npz"
    np.savez(tmp, X=np.concatenate([o[0] for o in out]), y=raw.phishing.values.astype(np.int8), src=raw.source.values.astype(np.int8), grp=np.concatenate([o[1] for o in out]))
    tmp.rename(SHARDS / f"shard_{i:02d}.npz")
    (SHARDS / f"raw_{i:02d}.csv").unlink()
    print(f"shard {i:02d}: {len(urls):,} URLs", flush=True)


def build(workers=6, only=None):
    todo = [i for i in range(N_SHARDS if only is None else only) if not (SHARDS / f"shard_{i:02d}.npz").exists()]
    if todo and not all((SHARDS / f"raw_{i:02d}.csv").exists() or (SHARDS / f"shard_{i:02d}.npz").exists() for i in range(N_SHARDS)):
        scatter()
    _work(["https://www.example.com/a/b.html?x=1"])  # load grammar, lists and dictionaries once, before forking
    with mp.get_context("fork").Pool(workers) as pool:
        for i in todo:
            featurize_shard(i, pool)


def available():
    return sorted(int(p.stem.split("_")[1]) for p in SHARDS.glob("shard_*.npz"))


def load(i):
    d = np.load(SHARDS / f"shard_{i:02d}.npz")
    return d["X"], d["y"], d["src"], d["grp"]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--only", type=int, default=None, help="featurize only the first K shards (smoke tests)")
    a = ap.parse_args()
    build(a.workers, a.only)
