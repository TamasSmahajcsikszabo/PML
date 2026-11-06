"""Score URL files with the STORED model of the sibling project url_grammar ("U", frozen, never retrained) and write url, label, p_u to data/additional/u_scores_{set}.csv.
U's engine needs its own folder (grammar, lists, models); it is only read, never modified, and a copy is made in a scratch folder because its engine may regenerate files.

    PYTHONPATH=src .venv/bin/python -m tools.score_u --u-dir /path/to/url_grammar [--sets train test external_test]"""
import argparse
import pathlib
import shutil
import sys
import tempfile

import joblib
import numpy as np
import pandas as pd

from common import ADDITIONAL, DATA


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--u-dir", required=True)
    ap.add_argument("--sets", nargs="+", default=["train", "test", "external_test"])
    a = ap.parse_args()
    src = pathlib.Path(a.u_dir)
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="u_copy_"))
    for d in ("src", "grammar", "models"):
        shutil.copytree(src / d, tmp / d, ignore=shutil.ignore_patterns("archive", "output", "__pycache__", "*.jar"))
    sys.path[:0] = [str(tmp / "src/model"), str(tmp / "src/features")]
    import engine as E
    import estimators  # noqa: F401  (the pickle refers to its classes)
    sys.modules["__main__"].LinearSVCProba = estimators.LinearSVCProba
    model = joblib.load(tmp / "models/xgboost_parts.joblib")
    model = model["model"] if isinstance(model, dict) else model
    eng = E.Engine()
    ADDITIONAL.mkdir(exist_ok=True)
    for name in a.sets:
        d = pd.read_csv(DATA / f"{name}.csv")
        H, parts, agg, err = eng.table(list(d.url))
        err = np.asarray(err).astype(bool)
        p = np.full(len(d), np.nan)
        if not err.any():
            p = model.predict_proba_tables(H, parts, agg)[:, 1]
        else:  # rows the parser rejects get NaN; score the rest
            ok = ~err
            H2, parts2, agg2, _ = eng.table(list(d.url[ok]))
            p[ok] = model.predict_proba_tables(H2, parts2, agg2)[:, 1]
        pd.DataFrame({"url": d.url, "label": d.label, "p_u": p}).to_csv(ADDITIONAL / f"u_scores_{name}.csv", index=False)
        print(name, len(d), "rejected:", int(err.sum()))
    shutil.rmtree(tmp)


if __name__ == "__main__":
    main()
