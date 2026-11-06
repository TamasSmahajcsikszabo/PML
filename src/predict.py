"""Single-URL prediction.  from predict import predict;  predict("https://www.PayPal-secure.login.tk/webscr?cmd=x")

Returns {"label": "phishing" | "clean", "probability": float in [0, 1]}.
Invalid input (not a str, empty / whitespace only, longer than 8192 characters, or nothing the grammar can read) never raises: it returns
{"label": "clean", "probability": 0.0} -- "no evidence", not a verdict. See REPORT.md."""
import functools
import json
import math
import warnings

import joblib
import numpy as np
import pandas as pd

from common import run_dir
from models.model import inputs

MAX_LEN = 8192  # longer strings are rejected as invalid, never truncated (the longest URL in the data is far shorter; keeps latency bounded)


@functools.cache
def _load():
    d = run_dir()  # latest run under models/results/
    cfg = json.loads((d / "config.json").read_text())
    S = pd.read_csv(d / "metrics_summary.csv").set_index("model")
    model = joblib.load(d / "model.joblib")
    from urlfeat.fingerprint import fingerprint
    if cfg.get("fingerprint") and cfg["fingerprint"] != fingerprint():
        warnings.warn(f"run {d.name}: the feature code, grammar or word lists changed since this model was fitted; retrain it (models.run)")
    members = list(model["members"]) + (["parts"] if "parts" in model else [])
    per_model = {m: float(S.loc[m, "oof_threshold_1pct_fpr"]) for m in members}  # each model's own 1%-FPR threshold on raw probabilities
    best = max(members, key=lambda m: S.loc[m, "cv_auc_oof"])  # best deployed model by cross-validated AUC
    return model, cfg["threshold"], per_model, best, cfg.get("threshold_raw")


def _invalid():
    return {"label": "clean", "probability": 0.0}


def _score(url):
    """-> (raw probability of every deployed model, calibrated probability, raw ensemble score), or None for invalid input.
    A run with a parts model (v3) scores mean[xgboost, mean(members), parts]; older runs score the mean of the members."""
    if not isinstance(url, str) or not url.strip() or len(url) > MAX_LEN:
        return None
    model = _load()[0]  # a missing / incompatible model must fail loudly, not look like an invalid URL
    try:
        Z = inputs([url])
        if Z.eq(0).all(axis=None):  # grammar rejected the string (all features missing)
            return None
        Z = Z[model["columns"]]  # a run may use a subset of the features
        probs = {m: float(est.predict_proba(Z)[0, 1]) for m, est in model["members"].items()}
        raw = float(np.mean(list(probs.values())))
        if "parts" in model:
            from urlfeat import parts as parts_features
            H, P = parts_features.tables([url])
            probs["parts"] = float(model["parts"].predict_proba(H, P)[0])
            raw = float(np.mean([probs["xgboost"], raw, probs["parts"]]))
        p = float(np.clip(model["calibrator"].predict([raw])[0], 0.0, 1.0))
        return (probs, p, raw) if math.isfinite(p) else None
    except Exception:  # last-resort guard: a bad string must not take the caller down
        return None


def predict(url):
    """Task contract: the calibrated blend of the deployed models; label by the blend threshold."""
    s = _score(url)
    if s is None:
        return _invalid()
    thr_raw = _load()[4]
    return {"label": "phishing" if (s[2] >= thr_raw if thr_raw is not None else s[1] >= _load()[1]) else "clean", "probability": s[1]}


def predict_vote(url):
    """Every deployed model votes at its own 1%-FPR threshold; label = majority vote, probability = calibrated blend probability (the P-value of the blend)."""
    s = _score(url)
    if s is None:
        return {**_invalid(), "votes": {}, "phishing_votes": 0, "models": 0}
    probs, p, _ = s
    per_model = _load()[2]
    votes = {m: {"label": "phishing" if q >= per_model[m] else "clean", "probability": q} for m, q in probs.items()}
    k = sum(v["label"] == "phishing" for v in votes.values())
    return {"label": "phishing" if 2 * k > len(votes) else "clean", "probability": p, "votes": votes, "phishing_votes": k, "models": len(votes)}


def predict_best(url):
    """Only the best deployed model (highest cross-validated AUC): its raw probability (not calibrated) and its label at its own 1%-FPR threshold."""
    s = _score(url)
    if s is None:
        return {**_invalid(), "model": None}
    best, per_model = _load()[3], _load()[2]
    q = s[0][best]
    return {"label": "phishing" if q >= per_model[best] else "clean", "probability": q, "model": best}
