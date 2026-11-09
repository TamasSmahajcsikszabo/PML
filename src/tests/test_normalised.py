"""The visitor's normalised view (task.md's "same page" rule: case, scheme, leading www., trailing slashes).

    PYTHONPATH=src .venv/bin/python src/tests/test_normalised.py        (also collected by pytest)

(1) URLVisitor.normal_form equals common.norm_key on every supplied URL; (2) with the view switched on, a URL and its variants (scheme flipped or removed, www. added or removed,
case changed, trailing slash toggled) get identical features; (3) the default view (URL as given) is unchanged by the option existing."""
import random
import sys

import numpy as np
import pandas as pd

from common import DATA, norm_key
from urlfeat.visitor import URLVisitor


def variants(u):
    rest = u.split("://", 1)[1] if "://" in u else u
    host_rest = rest[4:] if rest.lower().startswith("www.") else rest
    out = {u, "http://" + rest, "https://" + rest, rest, "http://www." + host_rest, "https://" + host_rest, u.upper(), u.rstrip("/") + "/", u.rstrip("/")}
    return sorted(out)


def check_keys():
    urls = pd.concat([pd.read_csv(DATA / f"{n}.csv").url for n in ("train", "test", "external_test")]).tolist()
    v = URLVisitor()
    bad = [u for u in urls if v.normal_form(u) != norm_key(u)]
    return len(urls), bad


def check_invariance(n=300, seed=1):
    urls = random.Random(seed).sample(pd.read_csv(DATA / "train.csv").url.tolist(), n)
    v = URLVisitor(normalised=True)
    bad = []
    for u in urls:
        vs = variants(u)
        X = v.featurize(vs).to_numpy()
        if not (np.isclose(X, X[0], equal_nan=True).all()):
            bad.append(u)
    return n, bad


def test_normal_form_equals_task_key():
    n, bad = check_keys()
    assert not bad, bad[:5]


def test_variants_get_identical_features():
    n, bad = check_invariance(100)
    assert not bad, bad[:5]


if __name__ == "__main__":
    n, bad = check_keys()
    print(f"normal_form == norm_key on {n - len(bad)} of {n} supplied URLs", *(f"\n  differs: {u!r}" for u in bad[:5]))
    m, bad2 = check_invariance()
    print(f"identical features for all variants of {m - len(bad2)} of {m} training URLs", *(f"\n  differs: {u!r}" for u in bad2[:5]))
    sys.exit(1 if bad or bad2 else 0)
