"""Lexical URL features: entropy, special characters, suspicious words, brand / look-alike rules, shorteners,
`&` vs `=`, path dots and hyphens, http / www after the host (vendored from url_grammar, extra_features.py).
Pure functions of the URL string plus the grammar-derived host columns."""
import functools, math, pathlib, re

LISTS_DIR = pathlib.Path(__file__).resolve().parents[1] / "lists"
DELIMS = set("~`!^*()[]{}\"';:,><|")   # the paper's F3 set
OTHER = set("+$=&.:#%")                # the paper's F4 set
GROUPS = {  # column groups, used by common.extra_matrix
    "entropy": ["ent_url", "ent_path", "ent_url_norm", "ent_path_norm", "ent_reg", "ent_max_seg", "ent_max_qval"],
    "special_chars": [f"sc_{k}_{c}" for k in ("delims", "other") for c in ("url", "host", "path", "query")],
    "suspicious_words": ["sw_phrase_url", "sw_phrase_host", "sw_phrase_path", "sw_phrase_query", "sw_brand_url", "sw_host_url", "sw_kit_url", "sw_kit_path"],
    "brand": ["brand_in_sub", "brand_in_reg", "brand_wrong_tld", "brand_typo", "brand_in_path", "brand_in_query", "reg_popular"],
    "shortener": ["is_shortener", "shortener_in_url"],
    "amp_eq": ["n_amp_url", "n_eq_url", "amp_gt_eq"],
    "path_counts": ["n_dots_path", "n_hyphens_path"],
    "http_www": ["http_after_host", "www_after_host", "www_extra_label"],
}
COLUMNS = [c for g in GROUPS.values() for c in g]
_PCT = re.compile(r"%([0-9a-fA-F]{2})")
_TOKEN = re.compile(r"[a-z0-9]+")
_DOMAINISH = re.compile(r"[a-z0-9-]+(?:\.[a-z0-9-]+)+")

# ---------------------------------------------------------------- lists
class Lists:
    """words: {"phrase": [...], "brand": [...], "host": [...], "kit": [...]}; brands: set of labels; popular: set of domains; shorteners: set of domains."""
    def __init__(self, words, brands, popular, shorteners):
        self.sub_rx = {g: re.compile("|".join(sorted(map(re.escape, words[g]), key=len, reverse=True))) if words.get(g) else None for g in ("phrase", "brand", "host")}
        self.kit = set(words.get("kit", []))
        self.brands, self.popular, self.shorteners = set(brands), set(popular), set(shorteners)
        self.brand_long = sorted((b for b in self.brands if len(b) >= 6), key=len, reverse=True)
        self.brand_long_rx = re.compile("|".join(map(re.escape, self.brand_long))) if self.brand_long else None
        self.typo_brands = [b for b in self.brands if len(b) >= 5]
        self.typo_idx = {}
        for b in self.typo_brands:
            for k in {b} | _deletes(b): self.typo_idx.setdefault(k, set()).add(b)
        self.near_brand = functools.lru_cache(maxsize=None)(self._near_brand)

    def _near_brand(self, w):
        if len(w) < 5 or w in self.brands: return False
        for k in {w} | _deletes(w):
            for b in self.typo_idx.get(k, ()):
                if b != w and _within_one(w, b): return True
        return False

def _deletes(w): return {w[:i] + w[i + 1:] for i in range(len(w))}

def _within_one(a, b):
    """Damerau-Levenshtein distance <= 1 (one substitution, insertion, deletion or adjacent swap)."""
    if a == b: return True
    la, lb = len(a), len(b)
    if abs(la - lb) > 1: return False
    if la == lb:
        d = [i for i in range(la) if a[i] != b[i]]
        return len(d) == 1 or (len(d) == 2 and d[1] == d[0] + 1 and a[d[0]] == b[d[1]] and a[d[1]] == b[d[0]])
    s, l = (a, b) if la < lb else (b, a)
    i = 0
    while i < len(s) and s[i] == l[i]: i += 1
    return s[i:] == l[i + 1:]

def read_list(path):
    return [l.strip() for l in open(path, encoding="utf-8") if l.strip() and not l.startswith("#")]

def load_lists(brand_top_n=500, popular_top_n=50000):
    words = {}
    for l in read_list(LISTS_DIR / "suspicious_words.tsv")[1:]:
        w, g = l.split("\t"); words.setdefault(g, []).append(w)
    stop = set(read_list(LISTS_DIR / "brand_stoplist.txt"))
    brands = {l.split("\t")[0] for l in read_list(LISTS_DIR / "brands.txt") if int(l.split("\t")[1]) <= brand_top_n} - stop
    popular = set(read_list(LISTS_DIR / "popular_top50k.txt")[:popular_top_n])
    return Lists(words, brands, popular, set(read_list(LISTS_DIR / "shorteners.txt")))

# ---------------------------------------------------------------- pure helpers
def decode(s): return _PCT.sub(lambda m: chr(int(m.group(1), 16)) if int(m.group(1), 16) < 128 else m.group(0), s)

def split_url(url):
    """(after_scheme, authority, path, query, fragment) following the grammar's modes: the authority ends at the first of / ? #, the fragment is everything after the first #,
    the query everything after the first ? before it."""
    i = url.find("://"); rest = url[i + 3:] if i >= 0 else url
    a = next((k for k, ch in enumerate(rest) if ch in "/?#"), len(rest))
    auth, tail = rest[:a], rest[a:]
    frag = query = ""
    h = tail.find("#")
    if h >= 0: tail, frag = tail[:h], tail[h + 1:]
    q = tail.find("?")
    if q >= 0: tail, query = tail[:q], tail[q + 1:]
    return rest, auth, tail, query, frag

def entropy(s):
    n = len(s)
    if n < 2: return 0.0
    c = {}
    for ch in s: c[ch] = c.get(ch, 0) + 1
    return -sum(v / n * math.log2(v / n) for v in c.values())

def norm_entropy(s):
    n = len(s)
    return entropy(s) / math.log2(n) if n >= 2 else 0.0   # relative to the maximum possible for that length

def count_in(s, chars): return sum(1 for ch in s if ch in chars)

def _suffix_hit(token, domains):
    p = token.split(".")
    return any(".".join(p[i:]) in domains for i in range(len(p)))

# ---------------------------------------------------------------- the features
def url_features(url, host, reg, suffix, host_kind, L):
    """All new features of one URL. host, reg, suffix, host_kind are the grammar-derived columns of features.tsv (lower-case host text, registrable label, suffix, host kind)."""
    rest, auth, path, query, frag = split_url(url)
    host = host.lower()
    dpath, dquery, dfrag, drest = decode(path).lower(), decode(query).lower(), decode(frag).lower(), decode(rest).lower()
    segs = [s for s in path.split("/") if s]
    qvals = [p.split("=", 1)[1] for p in query.split("&") if "=" in p]
    f = {}
    # entropy (bits per character; _norm = divided by log2(length), i.e. relative to the maximum for that length)
    f["ent_url"], f["ent_path"] = entropy(rest), entropy(path)
    f["ent_url_norm"], f["ent_path_norm"] = norm_entropy(rest), norm_entropy(path)
    f["ent_reg"] = entropy(reg) if host_kind in ("domain",) else 0.0
    f["ent_max_seg"] = max((entropy(s) for s in segs), default=0.0)
    f["ent_max_qval"] = max((entropy(v) for v in qvals), default=0.0)
    # special characters: the paper's delimiter set (F3) and "other" set (F4), per component
    for name, text in (("url", rest), ("host", host), ("path", path), ("query", query)):
        f[f"sc_delims_{name}"], f[f"sc_other_{name}"] = count_in(text, DELIMS), count_in(text, OTHER)
    # suspicious words: distinct words found (substring for phrase/brand/host groups, whole tokens for the generic "kit" group)
    def sub(g, text): return len(set(L.sub_rx[g].findall(text))) if L.sub_rx[g] and text else 0
    def kit(text): return len(set(_TOKEN.findall(text)) & L.kit) if text else 0
    f["sw_phrase_url"], f["sw_phrase_host"], f["sw_phrase_path"], f["sw_phrase_query"] = sub("phrase", drest), sub("phrase", host), sub("phrase", dpath), sub("phrase", dquery)
    f["sw_brand_url"], f["sw_host_url"], f["sw_kit_url"], f["sw_kit_path"] = sub("brand", drest), sub("host", drest), kit(drest), kit(dpath)
    # brand and look-alike rules (all off for a registrable domain that is itself popular); sub-domain = host without reg.suffix
    rs = f"{reg}.{suffix}" if reg and suffix else ""
    popular = int(bool(rs) and rs in L.popular); f["reg_popular"] = popular
    off = popular or host_kind == "ipv4"
    subdom = host[: -(len(rs) + 1)] if rs and host.endswith("." + rs) else ""
    f["brand_in_sub"] = 0 if off else len({t for t in _TOKEN.findall(subdom) if t in L.brands and t != reg})
    f["brand_in_reg"] = 0 if off or host_kind != "domain" else int(reg not in L.brands and any(b in reg for b in L.brand_long))
    f["brand_wrong_tld"] = 0 if off or host_kind not in ("domain", "platform_bare") else int(reg in L.brands)
    f["brand_typo"] = 0 if off or host_kind != "domain" else int(L.near_brand(reg))
    def brands_in(text):
        if popular or not text: return 0
        found = {t for t in _TOKEN.findall(text) if t in L.brands}
        if L.brand_long_rx: found |= set(L.brand_long_rx.findall(text))
        found.discard(reg); return len(found)
    f["brand_in_path"], f["brand_in_query"] = brands_in(dpath), brands_in(dquery)
    # URL shorteners: the host (or a parent domain of it) is listed; or a listed domain appears inside the path / query
    f["is_shortener"] = int(_suffix_hit(host, L.shorteners)) if host else 0
    inner = " ".join(x for x in (dpath, dquery, dfrag) if x)
    f["shortener_in_url"] = int(any(_suffix_hit(t, L.shorteners) for t in _DOMAINISH.findall(inner))) if "." in inner else 0
    # & versus = (paper F2), dots and hyphens in the path, http / www after the host (paper F7)
    f["n_amp_url"], f["n_eq_url"] = rest.count("&"), rest.count("=")
    f["amp_gt_eq"] = int(f["n_amp_url"] > f["n_eq_url"])
    f["n_dots_path"], f["n_hyphens_path"] = path.count("."), path.count("-")
    after = " ".join(x for x in (dpath, dquery, dfrag) if x)
    f["http_after_host"], f["www_after_host"] = after.count("http"), after.count("www")
    f["www_extra_label"] = sum(1 for l in host.split(".")[1:] if l.startswith("www"))
    return f

