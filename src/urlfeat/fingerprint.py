"""Fingerprint of what the feature columns MEAN: the grammar files, the word lists, the spell-checker version and the feature VALUES (full-URL row, host frame, part rows) of a fixed sample of
200 URLs (`fingerprint_urls.txt`, URLs of the public unseen pool). A refactor that keeps the values keeps the fingerprint; any change of a feature, a list, the grammar or the dictionary changes it.
A stored model records it; predict.py warns when it no longer matches."""
import functools
import hashlib
import importlib.metadata
import pathlib

import numpy as np

SRC = pathlib.Path(__file__).resolve().parents[1]
SAMPLE = pathlib.Path(__file__).resolve().parent / "fingerprint_urls.txt"


@functools.cache
def fingerprint():
    from .visitor import URLVisitor  # imported here: the package imports this module's siblings
    h = hashlib.sha256()
    for p in sorted(SRC.glob("grammar/*.g4")) + sorted((SRC / "lists").iterdir()):
        h.update(p.name.encode())
        h.update(p.read_bytes())
    h.update(importlib.metadata.version("pyspellchecker").encode())
    urls = [l.strip() for l in SAMPLE.read_text().splitlines() if l.strip() and not l.startswith("#")]
    X, H, P = URLVisitor().extract(urls)  # always the URL as given, whatever view the shared visitor is set to
    for frame in (X, H, P.drop(columns=["kind"])):
        h.update(",".join(map(str, frame.columns)).encode())
        h.update(np.round(frame.to_numpy(dtype=float), 9).tobytes())
    h.update("|".join(P.kind).encode())
    return h.hexdigest()
