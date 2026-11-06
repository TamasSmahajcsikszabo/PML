"""Fingerprint of everything that decides what the feature columns mean: grammar files, the urlfeat code, the word lists and the spell-checker version (adapted from U's engine.fingerprint).
A stored model records it; predict.py warns when the code that makes its inputs has changed since it was fitted."""
import functools
import hashlib
import importlib.metadata
import pathlib

SRC = pathlib.Path(__file__).resolve().parents[1]


@functools.cache
def fingerprint():
    h = hashlib.sha256()
    files = sorted(SRC.glob("grammar/*.g4")) + sorted(p for p in (SRC / "urlfeat").glob("*.py") if p.name != "fingerprint.py") + sorted((SRC / "lists").iterdir())
    for p in files:
        h.update(p.name.encode())
        h.update(p.read_bytes())
    h.update(importlib.metadata.version("pyspellchecker").encode())
    return h.hexdigest()
