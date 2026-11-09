"""One entry point, stages in order. After ANY code change the whole pipeline is rerun; the report is the last stage, so it always describes the code that ran.

    PYTHONPATH=src .venv/bin/python src/pipeline.py [--only STAGE | --from STAGE] [--dry-run] [--name NAME] [--parent RUN_ID] [--no-promote] [--all-features-run RUN_ID]

tests        grammar assertions, per-feature tests on random URLs, agreement with the frozen string-based extractor (docs/analysis/visitor_agreement.md)
features     parts tables (host frame + one row per segment / query key / value) of train.csv, test.csv, external_test.csv, cached under data/additional/ and keyed by the
             fingerprint of the grammar, the word lists and the feature VALUES of a fixed 200-URL sample (urlfeat.fingerprint); recomputed only when that changes
train        models.run on train.csv as supplied (correlation filter, tuning, 5-fold host-grouped CV, nine models, blend, threshold, test / external scored once), then models.run_parts
             (parts model + the deployed mean); --parent RUN_ID reuses a finished parent run instead of training one
verify       the stored artefacts are the evaluated objects: the model's fingerprint equals the code's; it reloads and reproduces its saved scores for test.csv from the raw URLs
             (max difference 0); the parent run's members reproduce the saved xgboost / blend scores; the fingerprint of the parent run (if recorded) is current
promote      the run just trained becomes LATEST (what predict.py loads); --no-promote skips it
smoke        predict() contract on invalid and unusual inputs (src/tests/test_predict_contract.py)
evidence     data inspection and overlap (tools.data_report), metrics with CIs (tools.report_numbers), the measurements behind the decisions table (tools.evidence; trains the
             all-features run unless --all-features-run is given)
predictions  deliverables/predictions.csv: predict() on every test.csv URL (tools.write_predictions)
report       Report.md from src/report/Report.template.md + the numbers above, predictor appendix, Report.pdf (tools.build_report)
The pipeline stops at the first failing stage. Logs of the parts run: src/models/results/{run}/pipeline_logs/."""
import argparse
import glob
import json
import pathlib
import subprocess
import sys
import time

import joblib
import numpy as np
import pandas as pd

from common import ADDITIONAL, RESULTS, ROOT, load, run_dir

STAGES = ["tests", "features", "train", "verify", "promote", "smoke", "evidence", "predictions", "report"]


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


def newest(prefix):
    return pathlib.Path(sorted(glob.glob(str(RESULTS / f"{prefix}*")), key=lambda d: pathlib.Path(d).stat().st_mtime)[-1])


def stage_tests(a):
    if not (ADDITIONAL / "visitor_oracle" / "train.pkl").exists():  # fresh checkout: freeze the old extractor's output from the shipped legacy code + the supplied files
        py("-m", "tools.legacy_oracle")
    py("src/grammar/check_grammar.py")
    py("src/tests/test_features.py", "--n", "1000", "--seed", "1")
    py("src/tests/test_normalised.py")
    py("-m", "tools.check_visitor", "--out", "docs/analysis/visitor_agreement.md")


def newest(prefix):
    return pathlib.Path(sorted(glob.glob(str(RESULTS / f"{prefix}*")), key=lambda d: pathlib.Path(d).stat().st_mtime)[-1])


def stage_train(a):
    if a.parent is None:
        py("-m", "models.run", "--data", a.data, "--extra-ratio", str(a.extra_ratio), "--max-corr", "0.75", "--version", "v2", *(["--normalised"] if a.normalised else []),
           "--name", "corr-filter-0.75" + ("" if a.data == "train" else f"-{a.data}") + ("-normalised" if a.normalised else ""))
        a.parent = newest("v2_").name  # the parts run combines with the parent trained just now
    py("-m", "models.run_parts", "--parent", a.parent, "--name", a.name, "--data", a.data, "--extra-ratio", str(a.extra_ratio))
    a.trained = newest("v3_").name  # verify, promote and the later stages use this run


def current(a):
    """the run the later stages describe: the one trained in this invocation, else the promoted one"""
    return getattr(a, "trained", None) or (RESULTS / "LATEST").read_text().strip()


def stage_promote(a):
    if a.no_promote:
        print("not promoted (--no-promote)")
        return
    (RESULTS / "LATEST").write_text(current(a))
    print("LATEST =", current(a))


def stage_smoke(a):
    py("src/tests/test_predict_contract.py")


def stage_evidence(a):
    run = current(a)
    py("-m", "tools.data_report")
    py("-m", "tools.report_numbers", run)
    py("-m", "tools.evidence", run, *(["--all-features-run", a.all_features_run] if a.all_features_run else []))
    parent = json.loads((RESULTS / run / "config.json").read_text())["parent"]
    if json.loads((RESULTS / parent / "config.json").read_text()).get("data") == "train+extra":  # the extra public data: what it changed against train.csv alone
        py("-m", "tools.extra_data_report", run)
    if (RESULTS / "v2_20261109T1117_corr-filter-0.75-normalised").exists():  # the normalised-view experiment + how spelling changes the delivered model's answer
        py("-m", "tools.normalised_report")


def stage_predictions(a):
    py("-m", "tools.write_predictions")


def stage_report(a):
    py("-m", "tools.build_report", current(a))


def latest(prefix="v3_"):
    """the promoted run (LATEST) when it is a parts run, else the newest one"""
    promoted = (RESULTS / "LATEST").read_text().strip()
    return str(RESULTS / promoted) if promoted.startswith(prefix) else sorted(glob.glob(str(RESULTS / f"{prefix}*")))[-1]


def stage_verify(a):
    from models.run import fit_predict  # noqa: F401  (import check)
    from models.model import inputs
    from models.run_parts import tables
    from urlfeat.fingerprint import fingerprint
    d = str(RESULTS / current(a))
    m = joblib.load(f"{d}/model.joblib")
    assert m["fingerprint"] == fingerprint(), "stored parts model was fitted with other feature code / grammar / lists"
    import urlfeat
    urlfeat.set_normalised(json.loads(open(f"{d}/config.json").read()).get("normalised", False))  # verify in the view the run was trained on
    te = pd.read_csv(f"{d}/scores_test.csv")
    H, P = tables("test", load("test").url.tolist())
    again = m["parts"].predict_proba(H, P)
    diff = float(np.abs(again - te.parts.values).max())
    assert diff < 1e-9, f"parts model does not reproduce its saved test scores (max diff {diff})"
    print(f"parts model reproduces its saved test.csv scores, max diff {diff:.1e}")
    cfg = json.loads((run_dir(json.loads(open(f'{d}/config.json').read())['parent']) / "config.json").read_text())
    pm = joblib.load(run_dir(json.loads(open(f"{d}/config.json").read())["parent"]) / "model.joblib")
    assert cfg.get("normalised", False) == urlfeat.get_visitor().normalised, "parts run and parent run use different views of the URL"
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
    ap.add_argument("--parent", default=None, help="reuse this finished parent run (default: train a new one)")
    ap.add_argument("--name", default="parts")
    ap.add_argument("--no-promote", action="store_true")
    ap.add_argument("--data", choices=["train", "train+extra"], default="train", help="training data (train+extra: train.csv + --extra-ratio x its size of extra public URLs)")
    ap.add_argument("--extra-ratio", type=float, default=2.0)
    ap.add_argument("--normalised", action="store_true", help="features of the task's normalised view of every URL (the parts run follows its parent)")
    ap.add_argument("--skip", nargs="*", default=[], choices=STAGES, help="stages to leave out")
    ap.add_argument("--all-features-run", default=None)
    a = ap.parse_args()
    todo = [s for s in ([a.only] if a.only else STAGES[STAGES.index(a.start):] if a.start else STAGES) if s not in a.skip]
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
