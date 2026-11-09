"""Word lists for the visit methods (brands, suspicious words, shorteners, popular domains).
Substring and whole-token searches are ANTLR lexers generated from the lists (`src/grammar/gen_words.py`): the WORD tokens of a text are its matches, left-most and longest at each
position (the old compiled alternations did the same). The popular-domain set (50k), the shorteners (1.4k) and the Tranco ranks (500k) are plain lookups on the registrable domain or host."""
import functools
import pathlib
import sys

from antlr4 import InputStream

LISTS_DIR = pathlib.Path(__file__).resolve().parents[1] / "lists"
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "parser"))
from WordsBrand import WordsBrand  # noqa: E402
from WordsBrandLong import WordsBrandLong  # noqa: E402
from WordsHost import WordsHost  # noqa: E402
from WordsPhrase import WordsPhrase  # noqa: E402
from WordsToken import WordsToken  # noqa: E402


class WordLexer:
    """find_all(text) = the WORD tokens of `text` in order (non-overlapping, left-most, longest)"""
    def __init__(self, lexer_cls, words=None):
        self.cls = lexer_cls
        self.words = tuple(words) if words and len(words) <= 64 else None  # small lists: a quick substring test decides whether the lexer is needed at all

    def find_all(self, text):
        if not text or (self.words is not None and not any(w in text for w in self.words)):
            return []
        lx = self.cls(InputStream(text))
        lx.removeErrorListeners()
        word = self.cls.WORD
        return [t.text for t in lx.getAllTokens() if t.type == word]


TOKENS = WordLexer(WordsToken)  # whole [a-z0-9] tokens of lower-cased text


def _deletes(w):
    return {w[:i] + w[i + 1:] for i in range(len(w))}


def within_one(a, b):
    """Damerau-Levenshtein distance <= 1 (one substitution, insertion, deletion or adjacent swap)"""
    if a == b:
        return True
    la, lb = len(a), len(b)
    if abs(la - lb) > 1:
        return False
    if la == lb:
        d = [i for i in range(la) if a[i] != b[i]]
        return len(d) == 1 or (len(d) == 2 and d[1] == d[0] + 1 and a[d[0]] == b[d[1]] and a[d[1]] == b[d[0]])
    s, l = (a, b) if la < lb else (b, a)
    i = 0
    while i < len(s) and s[i] == l[i]:
        i += 1
    return s[i:] == l[i + 1:]


def _read(name):
    return [l.strip() for l in open(LISTS_DIR / name, encoding="utf-8") if l.strip() and not l.startswith("#")]


class Lists:
    def __init__(self, words, brands, popular, shorteners, platforms=()):
        self.words = {g: WordLexer(cls, words.get(g)) for g, cls in (("phrase", WordsPhrase), ("brand", WordsBrand), ("host", WordsHost))}  # lexers generated from the same lists
        self.kit = set(words.get("kit", []))
        self.brands, self.popular, self.shorteners = set(brands), set(popular), set(shorteners)
        self.platforms = frozenset(platforms)  # hosting-platform suffixes (PSL private section + dynamic DNS), matched on whole labels at the end of a parsed host
        self.brand_long = WordLexer(WordsBrandLong)
        self.typo_idx = {}
        for b in (b for b in self.brands if len(b) >= 5):
            for k in {b} | _deletes(b):
                self.typo_idx.setdefault(k, set()).add(b)
        self.near_brand = functools.lru_cache(maxsize=None)(self._near_brand)

    def _near_brand(self, w):
        if len(w) < 5 or w in self.brands:
            return False
        for k in {w} | _deletes(w):
            for b in self.typo_idx.get(k, ()):
                if b != w and within_one(w, b):
                    return True
        return False


@functools.cache
def load(brand_top_n=500, popular_top_n=50000):
    words = {}
    for l in _read("suspicious_words.tsv")[1:]:
        w, g = l.split("\t")
        words.setdefault(g, []).append(w)
    stop = set(_read("brand_stoplist.txt"))
    brands = {l.split("\t")[0] for l in _read("brands.txt") if int(l.split("\t")[1]) <= brand_top_n} - stop
    popular = set(_read("popular_top50k.txt")[:popular_top_n])
    return Lists(words, brands, popular, set(_read("shorteners.txt")), _read("platforms.txt"))
