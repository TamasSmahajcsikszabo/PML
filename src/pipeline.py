"""One entry point, stages in order (structure adapted from url_grammar's pipeline.py):  features -> train -> verify.

    PYTHONPATH=src .venv/bin/python pipeline.py [--only STAGE | --from STAGE] [--dry-run] [--parent RUN_ID] [--name NAME] [--train-parent]

features  parts tables (host frame + one row per segment / query key / value) of train.csv, test.csv, external_test.csv, cached under data/additional/ and keyed by the
          fingerprint of grammar + urlfeat code + word lists (urlfeat.fingerprint); recomputed only when that changes
train     models.run_parts: parts model (nested cross-fitting, 0.75 collinearity filter on every component) + combinations with the parent run's XGBoost / blend;
          with --train-parent the parent run (models.run --data train --max-corr 0.75, about 25 minutes) is trained first
verify    the stored artefacts are the evaluated objects: the model's fingerprint equals the code's; it reloads and reproduces its saved scores for test.csv from the raw URLs
          (max difference 0); the parent run's members reproduce the saved xgboost / blend scores; the fingerprint of the parent run (if recorded) is current
The pipeline stops at the first failing stage. Logs: src/models/results/{run}/pipeline_logs/ (the latest v3 run)."""
import argparse
import glob
import json
import subprocess
import sys
import time

import joblib
import numpy as np
import pandas as pd

from common import RESULTS, ROOT, load, run_dir

STAGES = ["features", "train", "verify"]


def py(*args):
    cmd = [sys.executable, *args]
    print("$", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True, cwd=ROOT, env={**__import__("os").environ, "PYTHONPATH": str(ROOT / "src")})


def stage_features(a):
    from models.run_parts import tables
    for n in ("train", "test", "external_test"):
        t = time.time()
        H, P = tables(n, load(n).url.tolist())
        print(f"{n}: host frame {H.shape}, {len(P)} parts ({time.time() - t:.0f} s)", flush=True)


def stage_train(a):
    if a.train_parent:
        py("-m", "models.run", "--data", "train", "--max-corr", "0.75", "--version", "v2", "--name", "corr-filter-0.75")
    py("-m", "models.run_parts", "--parent", a.parent, "--name", a.name)


def latest(prefix="v3_"):
    return sorted(glob.glob(str(RESULTS / f"{prefix}*")))[-1]


def stage_verify(a):
    from models.run import fit_predict  # noqa: F401  (import check)
    from models.model import inputs
    from models.run_parts import tables
    from urlfeat.fingerprint import fingerprint
    d = latest()
    m = joblib.load(f"{d}/model.joblib")
    assert m["fingerprint"] == fingerprint(), "stored parts model was fitted with other feature code / grammar / lists"
    te = pd.read_csv(f"{d}/scores_test.csv")
    H, P = tables("test", load("test").url.tolist())
    again = m["parts"].predict_proba(H, P)
    diff = float(np.abs(again - te.parts.values).max())
    assert diff < 1e-9, f"parts model does not reproduce its saved test scores (max diff {diff})"
    print(f"parts model reproduces its saved test.csv scores, max diff {diff:.1e}")
    cfg = json.loads((run_dir(json.loads(open(f'{d}/config.json').read())['parent']) / "config.json").read_text())
    pm = joblib.load(run_dir(json.loads(open(f"{d}/config.json").read())["parent"]) / "model.joblib")
    Z = inputs(load("test").url.values)[pm["columns"]]
    pr = {k: e.predict_proba(Z)[:, 1] for k, e in pm["members"].items()}
    dx, db = np.abs(pr["xgboost"] - te.xgboost.values).max(), np.abs(np.mean(list(pr.values()), 0) - te.blend.values).max()
    assert max(dx, db) < 1e-6  # xgboost scores were saved as float32, f"parent members do not reproduce saved scores ({dx}, {db})"
    print(f"parent run members reproduce the saved xgboost / blend scores (max diff {max(dx, db):.1e})")
    if cfg.get("fingerprint"):
        assert cfg["fingerprint"] == fingerprint(), "parent run was fitted with other feature code"
    else:
        print("note: the parent run predates the fingerprint (no staleness check possible for it)")
    for n in ("test", "external_test"):  # the verify stage never trains; stored scores of the combined candidates must be consistent with their parts
        s = pd.read_csv(f"{d}/scores_{n}.csv")
        assert np.allclose(s["blend+parts_mean"], s[["blend", "parts"]].mean(axis=1))
    print("verify OK")


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--only", choices=STAGES)
    g.add_argument("--from", dest="start", choices=STAGES)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--parent", default="v2_20261104T1749_corr-filter-0.75")
    ap.add_argument("--name", default="parts")
    ap.add_argument("--train-parent", action="store_true")
    a = ap.parse_args()
    todo = [a.only] if a.only else STAGES[STAGES.index(a.start):] if a.start else STAGES
    print("stages:", " -> ".join(todo))
    if a.dry_run:
        return
    for s in todo:
        t = time.time()
        print(f"== {s}", flush=True)
        globals()[f"stage_{s}"](a)
        print(f"== {s} done in {time.time() - t:.0f} s", flush=True)


if __name__ == "__main__":
    main()
