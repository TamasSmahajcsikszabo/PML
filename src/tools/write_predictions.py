"""Write deliverables/predictions.csv (url,probability): `predict.predict` called on every URL of data/test.csv, in order, exactly one row each.

    PYTHONPATH=src .venv/bin/python -m tools.write_predictions [--out deliverables/predictions.csv]

Also checks the contract on every row (finite probability in [0, 1], label from the stored threshold) and prints the confusion counts at that threshold."""
import argparse
import math

import numpy as np
import pandas as pd

from common import DATA, ROOT
from predict import predict


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "deliverables" / "predictions.csv"))
    a = ap.parse_args()
    t = pd.read_csv(DATA / "test.csv")
    r = [predict(u) for u in t.url]
    assert all(set(x) == {"label", "probability"} and math.isfinite(x["probability"]) and 0 <= x["probability"] <= 1 for x in r)
    P = pd.DataFrame({"url": t.url, "probability": [x["probability"] for x in r]})
    assert len(P) == len(t)
    P.to_csv(a.out, index=False)
    flag, y = np.array([x["label"] == "phishing" for x in r]), t.label.values
    print(f"{a.out}: {len(P)} rows; flagged {flag.sum()} (tp {(flag & (y == 1)).sum()}, fp {(flag & (y == 0)).sum()}); {P.probability.nunique()} distinct probabilities")


if __name__ == "__main__":
    main()
