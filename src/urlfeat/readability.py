"""Readability / randomness helpers (ported from phishing_url_predictions; the visit methods call them): dictionary-word segmentation
("legibility"), one-edit misspellings ("typo_rate"), leet digits, vowel share, consonant runs, TLD and
file-extension flags. English dictionary only (pyspellchecker); other languages count as unreadable."""
import functools
import pathlib

from spellchecker import SpellChecker

LISTS = pathlib.Path(__file__).resolve().parents[1] / "lists"
_read = lambda n: [l.strip() for l in (LISTS / n).read_text().splitlines() if l.strip() and not l.startswith("#")]
WEB_WORDS = {w for l in _read("web_words.txt") for w in l.split()}
SUSPICIOUS_TLDS = {w for l in _read("suspicious_tlds.txt") for w in l.split()}
BRANDS = {l.split("\t")[0] for l in _read("brands.txt")}
EXTS = ["php", "html", "htm", "asp", "aspx", "jsp", "exe", "zip"]
VOWELS = set("aeiou")


@functools.cache
def _dict():
    spell = SpellChecker(language="en", distance=1)
    words = {w for w in spell.word_frequency.dictionary if len(w) >= 3 and w.isalpha()} | WEB_WORDS | BRANDS
    return spell, frozenset(words)


def _runs(text):
    run = []
    for ch in text.lower() + " ":
        if ch.isalpha():
            run.append(ch)
        elif run:
            yield "".join(run)
            run = []


@functools.lru_cache(maxsize=200_000)
def _uncovered(run):
    _, words = _dict()
    best = [0] * (len(run) + 1)
    for i in range(1, len(run) + 1):
        best[i] = best[i - 1] + 1
        for j in range(max(0, i - 24), i - 2):
            if run[j:i] in words:
                best[i] = min(best[i], best[j])
    return best[-1]


@functools.lru_cache(maxsize=100_000)
def _is_typo(run):
    if not 5 <= len(run) <= 20 or _uncovered(run) == 0:
        return False
    spell, _ = _dict()
    return bool(spell.unknown([run])) and spell.candidates(run) is not None


def spelling(text):
    letters = covered = typo = 0
    for r in _runs(text):
        letters += len(r)
        covered += len(r) - _uncovered(r)
        typo += len(r) * _is_typo(r)
    return (covered / letters, typo / letters) if letters else (0.0, 0.0)


def leet(s):
    return sum(c.isdigit() and ((i > 0 and s[i - 1].isalpha()) or (i + 1 < len(s) and s[i + 1].isalpha())) for i, c in enumerate(s)) / max(len(s), 1)


def vowel_ratio(s):
    L = [c for c in s.lower() if c.isalpha()]
    return sum(c in VOWELS for c in L) / len(L) if L else 0.0


def consonant_run(s):
    best = run = 0
    for ch in s.lower():
        run = run + 1 if ch.isalpha() and ch not in VOWELS else 0
        best = max(best, run)
    return best
