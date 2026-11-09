"""Smoke test of the prediction contract of `predict.predict` (task item 3) on unusual inputs.

    PYTHONPATH=src .venv/bin/python src/tests/test_predict_contract.py        (also collected by pytest)

Every input must return exactly {"label": "phishing" | "clean", "probability": finite float in [0, 1]} and never raise; invalid inputs (not a str, empty / whitespace, longer than 8192
characters) must give {"label": "clean", "probability": 0.0}."""
import math
import sys
import time

from predict import MAX_LEN, predict

INVALID = ["", " ", "\n\t", None, 123, 1.5, b"http://a.com", [], {}, "x" * (MAX_LEN + 1), "http://" + "a" * 9000 + ".com"]
UNUSUAL = ["https://www.PayPal-secure.login.tk/webscr?cmd=x", "http://", "://", "http://[::1]/", "http://cloud.google.com/x", "cloud.google", "http://x.cloud.goog/", "http://blogspot.com",
           "http://" + "a." * 120 + "example.com/" + "a/" * 200, "http://exämple.com/ü?q=ö#ß", "http://xn--e1afmkfd.xn--p1ai/", "http://user:pw@host.com:99999/%zz%41?a=b&amp;c=d",
           "javascript:alert(1)", "HTTP://EXAMPLE.COM", "http://1.2.3.4:80/a", "\x00\x01http://a.com", "http://a.com/\n\t x", "example.com", "ftp://a.org/x.zip",
           "http://a.com/?u=http://b.com/x", "http://a.com/logo@2x.png", "http://" + "a" * 8000 + ".com"]


def valid(r):
    return (isinstance(r, dict) and set(r) == {"label", "probability"} and r["label"] in ("phishing", "clean") and isinstance(r["probability"], float)
            and math.isfinite(r["probability"]) and 0.0 <= r["probability"] <= 1.0)


def test_invalid_inputs():
    for x in INVALID:
        assert predict(x) == {"label": "clean", "probability": 0.0}, repr(x)[:60]


def test_unusual_inputs():
    for x in UNUSUAL:
        assert valid(predict(x)), repr(x)[:60]


def test_phishing_example_of_the_task():
    assert valid(predict("https://www.PayPal-secure.login.tk/webscr?cmd=x"))


if __name__ == "__main__":
    t, bad = time.time(), 0
    for name, cases, check in (("invalid", INVALID, lambda r: r == {"label": "clean", "probability": 0.0}), ("unusual", UNUSUAL, valid)):
        for x in cases:
            try:
                ok = check(predict(x))
            except Exception as e:  # noqa: BLE001
                ok = False
                print("RAISED", repr(x)[:60], e)
            bad += not ok
            if not ok:
                print("FAIL", name, repr(x)[:60])
    print(f"{len(INVALID) + len(UNUSUAL)} inputs, {bad} failures, {time.time() - t:.1f} s")
    sys.exit(1 if bad else 0)
