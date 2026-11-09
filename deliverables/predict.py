#!/usr/bin/env python3
"""Phishing URL prediction (contract of docs/task.md) as a library and a command-line tool.

    from predict import predict                    # from the deliverables/ folder
    predict("https://www.PayPal-secure.login.tk/webscr?cmd=x")   # {"label": "phishing", "probability": 0.96}

    python predict.py URL [URL ...]                # one JSON object per URL
    python predict.py --vote URL                   # every deployed model votes at its own threshold: majority label, calibrated blend probability, the individual votes
    python predict.py --best URL                   # only the best deployed model (highest cross-validated AUC): its raw probability and label
    python predict.py --test [-n N] [--seed S]     # random sample of N unseen URLs (default 50; 5% phishing, rest neutral); prints the results and saves them to results/

`label` is "phishing" or "clean" (threshold fixed on training data, see ../Report.md); `probability` is the calibrated model score in [0, 1].
Invalid input (not a string, empty, unparsable) returns {"label": "clean", "probability": 0.0}.
Model, features, grammar and word lists come from ../src/ (latest run in ../src/models/results/); nothing is trained or downloaded."""
import argparse
import csv
import datetime
import importlib.util
import json
import math
import pathlib
import random
import sys
import warnings

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE.parent / "src"
POOL = HERE / "data" / "unseen_pool.csv"
RESULTS = HERE / "results"
PHISHING_SHARE = 0.05  # --test samples 5% phishing (rounded up, at least 1: 5% of 50 is 2.5 -> 3), the rest neutral

warnings.filterwarnings("ignore")
sys.path.insert(0, str(SRC))
_spec = importlib.util.spec_from_file_location("src_predict", SRC / "predict.py")  # this file is also called predict.py, so load src's by path
_src = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_src)
predict, predict_vote, predict_best = _src.predict, _src.predict_vote, _src.predict_best


def run_test(n, seed, scorer=None, mode="blend"):
    """Random sample of n URLs from the unseen Kaggle pool: ceil(5% of n) phishing + the rest neutral; prints each prediction and a summary."""
    scorer = scorer or predict
    n_phish = max(1, math.ceil(PHISHING_SHARE * n))
    rows = list(csv.DictReader(open(POOL, encoding="utf-8")))
    phish, neutral = [r for r in rows if r["label"] == "1"], [r for r in rows if r["label"] == "0"]
    if n_phish > len(phish) or n - n_phish > len(neutral):
        sys.exit(f"-n {n} is too large for the pool ({len(phish)} phishing, {len(neutral)} neutral URLs)")
    rng = random.Random(seed)
    sample = rng.sample(phish, n_phish) + rng.sample(neutral, n - n_phish)
    rng.shuffle(sample)
    print(f"Mode: {mode}. Sample of {n} unseen URLs (Kaggle taruntiwarihp/phishing-site-urls; none in train/test/external), seed={seed}: {n_phish} phishing, {n - n_phish} neutral\n")
    print(f"{'truth':9s} {'prediction':10s} {'prob':>6s}  {'':3s} {'votes' if mode == 'vote' else 'model' if mode == 'best' else '':9s} url")
    tp = fp = fn = tn = 0
    saved = []
    for r in sample:
        p = scorer(r["url"])
        detail = f"{p['phishing_votes']}/{p['models']}" if mode == "vote" else (p["model"] or "-") if mode == "best" else ""
        truth, pred = ("phishing" if r["label"] == "1" else "clean"), p["label"]
        tp, fp, fn, tn = tp + (truth == pred == "phishing"), fp + (truth == "clean" and pred == "phishing"), fn + (truth == "phishing" and pred == "clean"), tn + (truth == pred == "clean")
        saved.append({"url": r["url"], "truth": truth, "prediction": pred, "probability": p["probability"], "correct": int(truth == pred), "detail": detail})
        print(f"{truth:9s} {pred:10s} {p['probability']:6.3f}  {'ok ' if truth == pred else 'ERR'}  {detail:9s} {r['url'][:90]}")
    print(f"\ncorrect {tp + tn}/{n} | phishing caught {tp}/{tp + fn} | neutral flagged as phishing {fp}/{fp + tn}")
    RESULTS.mkdir(exist_ok=True)
    stem = RESULTS / f"test_{datetime.datetime.now():%Y%m%dT%H%M%S}_n{n}_seed{seed}"
    with open(stem.with_suffix(".csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(saved[0]))
        w.writeheader()
        w.writerows(saved)
    stem.with_suffix(".json").write_text(json.dumps({"seed": seed, "n": n, "phishing": n_phish, "TP": tp, "FP": fp, "FN": fn, "TN": tn, "threshold": _src._load()[1], "mode": mode,
                                                       "run": _src.run_dir().name}, indent=2))
    print(f"saved: {stem.with_suffix('.csv').relative_to(HERE.parent)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("urls", nargs="*", help="URL(s) to classify")
    ap.add_argument("--test", action="store_true", help="classify a random sample of unseen URLs (5%% phishing, rest neutral), print and save the results")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--vote", action="store_true", help="run every deployed model: majority vote label + calibrated blend probability (+ the individual votes)")
    g.add_argument("--best", action="store_true", help="return only the best deployed model's prediction (raw probability, own threshold)")
    ap.add_argument("-n", type=int, default=50, help="sample size for --test (default: 50)")
    ap.add_argument("--seed", type=int, default=None, help="seed for --test (default: random)")
    a = ap.parse_args()
    scorer, mode = (predict_vote, "vote") if a.vote else (predict_best, "best") if a.best else (predict, "blend")
    if a.test:
        run_test(max(a.n, 2), a.seed if a.seed is not None else random.SystemRandom().randrange(10**6), scorer, mode)
    elif a.urls:
        for u in a.urls:
            r = scorer(u)
            print(json.dumps(r) if len(a.urls) == 1 else json.dumps({"url": u, **r}))
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
