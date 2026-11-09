"""One test per feature column on random URLs.

    PYTHONPATH=src .venv/bin/python src/tests/test_features.py [--n 400] [--seed 0] [--out docs/analysis/feature_tests.md]      (also collected by pytest if installed)

URLs are BUILT from known components (scheme, user info, sub-domains, registrable label, suffix, port, path segments, query pairs, fragment, injected IPs / host names / hex / UUID / base64 / repeats / escapes /
e-mails / nested URLs), so the expected value of a feature comes from the components or from a naive reference written here, not from the parser. Real URLs of the public unseen pool test the string features.
Each feature column is checked on every URL; the report lists pass counts per column and the first failures. Columns without an independent reference are marked `wiring` (they call a helper on the right text)."""
import argparse
import collections
import itertools
import math
import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np  # noqa: E402

import urlfeat  # noqa: E402
from urlfeat import obfuscation as OB, popularity, readability as RD, wordlists  # noqa: E402
from urlfeat.visitor import BINARY, COLUMNS, LEX_COLUMNS, LEX_LOG1P, LOG1P, PART_COLS, SUSPICIOUS_TLDS  # noqa: E402

L = wordlists.load()
HEXD = "0123456789abcdefABCDEF"
WORDS = ["secure", "login", "account", "update", "verify", "bank", "shop", "index", "images", "assets", "news", "blog", "product", "view", "page", "download", "support", "mail", "game",
         "paypal", "amazon", "apple", "microsoft", "google", "signin", "webscr", "confirm", "wp-content", "my-site", "data2", "info", "admin", "files"]
SUFFIXES = ["com", "net", "org", "co.uk", "de", "info", "tk", "io"]
INJECT = ["ip", "domain", "hex", "uuid", "b64", "rep", "pct", "email", "nested", "stray", "port", "digits"]


# ---------------------------------------------------------------- naive references (independent of urlfeat.text)
def entropy(s):
    n = len(s)
    if n < 2:
        return 0.0
    return -sum(c / n * math.log2(c / n) for c in collections.Counter(s).values())


def norm_entropy(s):
    return entropy(s) / math.log2(len(s)) if len(s) >= 2 else 0.0


def valid_pct(s, i):
    return s[i] == "%" and i + 2 < len(s) + 0 and all(c in HEXD for c in s[i + 1:i + 3]) and len(s[i + 1:i + 3]) == 2


def n_pct(s):
    return sum(1 for i in range(len(s)) if valid_pct(s, i))


def strip_pct(s):
    out, i = "", 0
    while i < len(s):
        if valid_pct(s, i):
            i += 3
        else:
            out += s[i]
            i += 1
    return out


def decode(s):
    out, i = "", 0
    while i < len(s):
        if valid_pct(s, i):
            v = int(s[i + 1:i + 3], 16)
            out += chr(v) if v < 128 else s[i:i + 3]
            i += 3
        else:
            out += s[i]
            i += 1
    return out


def digit_rate(s):
    c = strip_pct(s)
    return sum(ch in "0123456789" for ch in c) / len(c) if c else 0.0


def longest_run(s, pred=str.isdigit):
    return max((len(list(g)) for k, g in itertools.groupby(s, key=pred) if k), default=0)


def has_rep(pieces, digits=False, skip_www=False):
    for p in pieces:
        if skip_www and p.lower() == "www":
            continue
        for k, g in itertools.groupby(strip_pct(p).lower()):
            if len(list(g)) >= 3 and (not digits or k in "0123456789"):
                return True
    return False


def naive_find(words, text):
    """left-most, longest, non-overlapping occurrences"""
    ws = sorted(words, key=len, reverse=True)
    out, i = [], 0
    while i < len(text):
        for w in ws:
            if text.startswith(w, i):
                out.append(w)
                i += len(w)
                break
        else:
            i += 1
    return out


def tokens(s):
    return ["".join(g) for k, g in itertools.groupby(s, key=lambda c: c in "abcdefghijklmnopqrstuvwxyz0123456789") if k]


def words_in(group, text):
    ws = [l.split("\t")[0] for l in open(pathlib.Path(__file__).resolve().parents[1] / "lists" / "suspicious_words.tsv", encoding="utf-8")
          if "\t" in l and not l.startswith("#") and l.strip().split("\t")[1] == group]
    return len(set(naive_find(ws, text))) if text else 0


def tf(col, v):
    """the transform of a column (spec of visitor.BINARY / LOG1P / lexical log1p)"""
    if col in BINARY:
        return float(v > 0)
    if col in LOG1P or (col in LEX_COLUMNS and col.startswith(LEX_LOG1P)):
        return float(np.log1p(v))
    return float(v)


# ---------------------------------------------------------------- random URL with known components
def _is_sld(word):
    """the grammar reads this word as a second-level suffix (shop, com, ...): placed right before a TLD it would be taken as part of the suffix"""
    from antlr4 import InputStream
    from urlfeat.visitor import UrlLexer
    lx = UrlLexer(InputStream(word))
    lx.removeErrorListeners()
    toks = lx.getAllTokens()
    return len(toks) == 1 and toks[0].type == UrlLexer.SLD


NAME_WORDS = [w for w in WORDS if not _is_sld(w)]


def label(rng, words=None):
    w = rng.choice(words or WORDS)
    return w + rng.choice(["", "", "", str(rng.randint(0, 99)), "-" + rng.choice(["x", "2", "web"])])


def make_url(rng):
    t = {"inject": [x for x in INJECT if rng.random() < 0.18]}
    t["scheme"] = rng.choice(["http", "https", "ftp", ""] if rng.random() < .9 else ["http", "https"])
    t["userinfo"] = "user:pw" if rng.random() < .05 else None
    t["ipv4"] = rng.random() < .06
    t["subs"] = ([] if t["ipv4"] else ([rng.choice(["www", "www"] + WORDS)] if rng.random() < .5 else []) + [label(rng) for _ in range(rng.choice([0, 0, 1, 2]))])
    t["name"] = label(rng, NAME_WORDS)
    t["suffix"] = rng.choice(SUFFIXES)
    t["port"] = "8080" if rng.random() < .08 else None
    host = ".".join([str(rng.randint(1, 254)) for _ in range(4)]) if t["ipv4"] else ".".join(t["subs"] + [t["name"], t["suffix"]])
    t["host"] = host
    segs = [rng.choice(WORDS) + rng.choice(["", "", ".php", ".html", ".htm", ".asp", ".png"]) for _ in range(rng.choice([0, 0, 1, 2, 3, 4]))]
    t["segs"] = segs
    t["trailing"] = bool(segs) and rng.random() < .25
    t["empty_seg"] = len(segs) > 1 and rng.random() < .1
    pairs = [(rng.choice(["id", "q", "user", "ref", "token", "next"]), rng.choice([None, "", str(rng.randint(0, 999)), rng.choice(WORDS), "a=b"])) for _ in range(rng.choice([0, 0, 1, 2, 3]))]
    t["pairs"] = pairs
    t["amp_esc"] = len(pairs) > 1 and rng.random() < .1
    t["frag"] = rng.choice(WORDS) if rng.random() < .1 else None
    # injections go into the last query value / the last segment / a new pair
    inj = {"ip": "10.20.30.40", "domain": "login.evil-site.com", "hex": "0123456789abcdef0123", "uuid": "123e4567-e89b-12d3-a456-426614174000", "b64": "AbC1dEf2GhI3jKl4MnO5",
           "rep": "xaaaay", "pct": "%41%2fz", "email": "joe@mail.example.org", "nested": "http://evil.example.net/a", "stray": "50%zz", "port": "evil.com:8080", "digits": "77777"}
    for k in t["inject"]:
        if k in ("ip", "domain", "hex", "uuid", "b64", "rep", "port") and rng.random() < .5 and t["segs"]:
            t["segs"][-1] = inj[k] + "/z" if False else t["segs"][-1]
        pairs.append(("p", inj[k]))
    if t["inject"] and not t["pairs"]:
        t["pairs"] = pairs
    path = ""
    if t["segs"]:
        parts = list(t["segs"])
        if t["empty_seg"]:
            parts.insert(1, "")
        path = "/" + "/".join(parts) + ("/" if t["trailing"] else "")
    elif rng.random() < .3:
        path = "/"
    query = ""
    if t["pairs"]:
        sep = "&amp;" if t["amp_esc"] else "&"
        query = "?" + sep.join(k if v is None else f"{k}={v}" for k, v in t["pairs"])
    t["path"], t["query"] = path, query
    prefix = (t["scheme"] + "://") if t["scheme"] else ""
    auth = (t["userinfo"] + "@" if t["userinfo"] else "") + host + (":" + t["port"] if t["port"] else "")
    t["url"] = prefix + auth + path + query + ("#" + t["frag"] if t["frag"] else "")
    return t


# ---------------------------------------------------------------- expected values: col -> fn(truth) -> raw value
def expected(t):
    url, host, path, query, frag = t["url"], t["host"], t["path"], t["query"], t["frag"] or ""
    rest = url.split("://", 1)[1] if t["scheme"] else url
    segs = [s for s in path.split("/") if s]
    pairs = t["pairs"]
    keys = [k for k, _ in pairs]
    vals = [v for _, v in pairs if v is not None]
    q = query[1:]
    dpath, dq, dfrag, drest = decode(path).lower(), decode(q).lower(), decode(frag).lower(), decode(rest).lower()
    after = " ".join(x for x in (dpath, dq, dfrag) if x)
    n = max(len(url), 1)
    ipv4, subs, name, suffix = t["ipv4"], t["subs"], t["name"], t["suffix"]
    reg = "" if ipv4 else name
    rs = f"{name}.{suffix}"
    popular = int(not ipv4 and rs in L.popular)
    labels = [l for l in host.split(".") if l]
    last_seg = segs[-1] if segs else ""
    ext = last_seg.rsplit(".", 1)[-1].lower() if "." in last_seg and not t["trailing"] else ""
    emb = decode(" ".join((path, query, frag)))
    tld = suffix.rsplit(".", 1)[-1]
    E = {}
    E["https"], E["ftp"] = t["scheme"] == "https", t["scheme"] == "ftp"
    E["host_ipv4"], E["host_platform"], E["host_other"] = ipv4, False, False
    E["sfx_platform"], E["sfx_platform_bare"], E["sfx_icann2"] = False, False, (not ipv4) and "." in suffix
    E["has_ext"] = ext != ""
    E["port"], E["userinfo"] = t["port"] is not None, t["userinfo"] is not None
    E["has_path"], E["trailing_slash"] = len(segs) > 0, t["trailing"] and len(segs) > 0
    E["path_len"] = len(path) if segs else 0
    E["www"] = bool(subs) and subs[0] == "www"
    E["punycode"] = 0
    E["has_query"], E["has_frag"] = bool(query), t["frag"] is not None
    E["n_amp_esc"] = query.count("&amp;")
    E["n_nested"] = sum(1 for v in vals if v.startswith("http://evil.example.net"))
    E["n_email"] = sum(1 for v in vals if "@" in v)
    E["pct_total"] = n_pct(url)
    E["stray_pct"] = url.count("%") - n_pct(url)
    E["rep_char_host"], E["rep_char_path"] = has_rep(labels, skip_www=True), has_rep(segs)
    E["rep_char_query"] = has_rep(keys + vals)
    E["rep_digit"] = has_rep(labels + segs + keys + vals + ([frag] if frag else []), digits=True)
    E["emb_ip"] = "ip" in t["inject"] or (not ipv4 and False)
    E["emb_domain"] = "domain" in t["inject"] or "port" in t["inject"] or "email" in t["inject"] or "nested" in t["inject"]
    E["emb_hex"] = "hex" in t["inject"] or "uuid" in t["inject"]
    E["emb_port"] = "port" in t["inject"]
    E["non_ascii"] = any(ord(c) > 127 for c in url)
    E["n_sub"], E["n_seg"] = len(subs), len(segs)
    E["n_empty_seg"] = 1 if t["empty_seg"] else 0
    E["n_pairs"], E["n_empty_val"] = len(pairs), sum(1 for _, v in pairs if v == "")
    E["url_len"], E["host_len"], E["reg_len"] = len(url), len(host), len(reg)
    E["reg_hyphens"], E["reg_digits"] = reg.count("-"), sum(c.isdigit() for c in reg)
    E["max_seg_len"] = max(map(len, segs), default=0)
    E["query_len"], E["frag_len"] = len(query), (len(frag) + 1) if t["frag"] is not None else 0
    E["max_label_len"] = max(map(len, labels), default=0)
    E["mean_seg_len"] = sum(map(len, segs)) / len(segs) if segs else 0.0
    E["max_qkey_len"], E["max_qval_len"] = max(map(len, keys), default=0), max(map(len, vals), default=0)
    E["mean_qval_len"] = sum(map(len, vals)) / len(vals) if vals else 0.0
    E["longest_digit_run"] = longest_run(strip_pct(url))
    E["n_dash_host"], E["n_dash_url"], E["n_dots_host"] = host.count("-"), url.count("-"), host.count(".")
    E["n_underscore"], E["n_at"] = url.count("_"), url.count("@")
    E["host_digit_rate"], E["path_digit_rate"], E["query_digit_rate"], E["url_digit_rate"] = digit_rate(host), digit_rate(path), digit_rate(query), digit_rate(url)
    E["ent_url"], E["ent_path"], E["ent_url_norm"], E["ent_path_norm"] = entropy(rest), entropy(path), norm_entropy(rest), norm_entropy(path)
    E["ent_reg"] = entropy(reg) if not ipv4 else 0.0
    E["ent_max_seg"] = max((entropy(s) for s in segs), default=0.0)
    E["ent_max_qval"] = max((entropy(v) for v in vals), default=0.0)
    delims, other = set("~`!^*()[]{}\"';:,><|"), set("+$=&.:#%")
    for nm, txt in (("url", rest), ("host", host), ("path", path), ("query", q)):
        E[f"sc_delims_{nm}"], E[f"sc_other_{nm}"] = sum(c in delims for c in txt), sum(c in other for c in txt)
    for nm, txt in (("url", drest), ("host", host), ("path", dpath), ("query", dq)):
        E[f"sw_phrase_{nm}"] = words_in("phrase", txt)
    E["sw_brand_url"], E["sw_host_url"] = words_in("brand", drest), words_in("host", drest)
    kit = {l.split("\t")[0] for l in open(pathlib.Path(__file__).resolve().parents[1] / "lists" / "suspicious_words.tsv", encoding="utf-8") if "\t" in l and not l.startswith("#") and l.strip().split("\t")[1] == "kit"}
    E["sw_kit_url"], E["sw_kit_path"] = len(set(tokens(drest)) & kit), len(set(tokens(dpath)) & kit)
    off = popular or ipv4
    subdom = ".".join(subs).lower()
    E["brand_in_sub"] = 0 if off else len({x for x in tokens(subdom) if x in L.brands and x != reg})
    E["brand_in_reg"] = 0 if off else int(reg.lower() not in L.brands and any(b in reg.lower() for b in L.brands if len(b) >= 6))
    E["brand_wrong_tld"] = 0 if off else int(reg.lower() in L.brands)
    E["brand_typo"] = 0 if off else int(L.near_brand(reg.lower()))

    def brands_in(txt):
        if popular or not txt:
            return 0
        found = {x for x in tokens(txt) if x in L.brands} | {b for b in L.brands if len(b) >= 6 and b in txt}
        found.discard(reg.lower())
        return len(found)
    E["brand_in_path"], E["brand_in_query"] = brands_in(dpath), brands_in(dq)
    E["reg_popular"] = popular
    E["is_shortener"] = int(any(".".join(host.lower().split(".")[i:]) in L.shorteners for i in range(len(host.split(".")))))
    E["amp_gt_eq"], E["n_amp_url"], E["n_eq_url"] = rest.count("&") > rest.count("="), rest.count("&"), rest.count("=")
    E["n_dots_path"], E["n_hyphens_path"] = path.count("."), path.count("-")
    E["http_after_host"], E["www_after_host"] = after.count("http"), after.count("www")
    E["www_extra_label"] = sum(1 for l in host.split(".")[1:] if l.startswith("www"))
    E["ratio_delims_url"], E["ratio_other_url"] = sum(c in delims for c in url) / n, sum(c in other for c in url) / n
    E["ratio_nonalnum_url"], E["ratio_nonalnum_host"] = sum(not c.isalnum() for c in url) / n, sum(not c.isalnum() for c in host) / max(len(host), 1)
    E["ratio_hyphen_url"], E["ratio_dot_url"] = url.count("-") / n, url.count(".") / n
    E["tld_suspicious"], E["tld_cc"], E["tld_has_digit"] = (tld in SUSPICIOUS_TLDS) and not ipv4, len(tld) == 2 and not ipv4, False
    for e in ("php", "html", "htm", "asp", "aspx", "jsp", "exe", "zip"):
        E[f"ext_{e}"] = ext == e
    E["host_n_scripts"] = 1 if any(c.isalpha() for c in host) else 0
    E["host_mixed_script"], E["host_confusable_chars"] = False, sum(c in OB.CONFUSABLE for c in host.lower() if not c.isdigit())
    E["reg_log_rank"] = popularity.log_rank(rs if not ipv4 else host)
    E["host_digit_in_word"] = any(any(c.isdigit() for c in tk) and any(c.isalpha() for c in tk) for tk in [x for lab in host.split(".") for x in lab.replace("_", "-").split("-") if x])
    # wiring: helpers called on the right text
    for nm, txt in (("url", url), ("host", host), ("sld", reg)):
        lg, ty = RD.spelling(txt)
        E[f"{nm}_legibility"], E[f"{nm}_typo_rate"], E[f"{nm}_leet"] = lg, ty, RD.leet(txt)
    E["sld_vowel_ratio"], E["sld_consonant_run"] = RD.vowel_ratio(reg), RD.consonant_run(reg)
    sp = [RD.spelling(s) for s in segs] or [(1.0, 0.0)]
    vp = [RD.spelling(v) for v in vals] or [(1.0, 0.0)]
    E["seg_min_legibility"], E["seg_max_typo"] = min(a for a, _ in sp), max(b for _, b in sp)
    E["qval_min_legibility"], E["qval_max_typo"] = min(a for a, _ in vp), max(b for _, b in vp)
    E["seg_max_leet"], E["seg_consonant_run"] = max((RD.leet(s) for s in segs), default=0.0), max((RD.consonant_run(s) for s in segs), default=0)
    E["brand_lookalike_reg"] = (OB.deconfuse(reg.split(".")[0]) in L.brands and reg.split(".")[0] not in L.brands) if reg else False
    E["brand_lookalike_host"] = len(({OB.deconfuse(x) for lab in host.split(".") for x in lab.replace("_", "-").split("-") if x} & L.brands) - {x for lab in host.split(".") for x in lab.replace("_", "-").split("-") if x}) > 0
    E["shortener_in_url"] = None  # not tested here: needs a shortener host inside the path / query (see targeted tests)
    return {c: (tf(c, v) if v is not None else None) for c, v in E.items()}


WIRING = {"url_legibility", "url_typo_rate", "url_leet", "host_legibility", "host_typo_rate", "host_leet", "sld_legibility", "sld_typo_rate", "sld_leet", "sld_vowel_ratio", "sld_consonant_run",
          "seg_min_legibility", "seg_max_typo", "qval_min_legibility", "qval_max_typo", "seg_max_leet", "seg_consonant_run", "brand_lookalike_reg", "brand_lookalike_host", "reg_log_rank"}


def run(n=400, seed=0, pool=300):
    rng = random.Random(seed)
    ts = [make_url(rng) for _ in range(n)]
    X = urlfeat.featurize([t["url"] for t in ts])
    stats = {c: [0, 0, []] for c in COLUMNS}
    for i, t in enumerate(ts):
        exp = expected(t)
        for c, v in exp.items():
            if v is None:
                continue
            got = X.iloc[i][c]
            ok = abs(got - v) <= 1e-9 * max(1.0, abs(v))
            stats[c][0] += ok
            stats[c][1] += 1
            if not ok and len(stats[c][2]) < 3:
                stats[c][2].append((t["url"][:100], v, got))
    return stats, ts


def targeted():
    """cases the generator does not reach: platform hosts, punycode, mixed scripts, shorteners, www labels, hlabel rows, TLD lookups"""
    out = []

    def check(name, cond):
        out.append((name, bool(cond)))
    f = lambda u: urlfeat.featurize([u]).iloc[0]
    X, H, P = urlfeat.extract(host_labels=True, urls=["http://foo.blogspot.com/x", "http://xn--e1afmkfd.xn--p1ai/", "http://bit.ly/abc", "http://www.www2.example.com/a", "http://pаypal.com/", "http://1.2.3.4/x", "http://localhost/y"])
    check("sfx_platform for a hosting platform suffix (blogspot.com), tenant is the registrable label", X.iloc[0].sfx_platform == 1 and X.iloc[0].reg_len == np.log1p(3))
    check("punycode labels counted", X.iloc[1].punycode == 1)
    check("is_shortener for bit.ly", X.iloc[2].is_shortener == 1)
    check("www_extra_label counts www2", X.iloc[3].www_extra_label == np.log1p(1))
    check("host_mixed_script for a Cyrillic letter in a Latin host", X.iloc[4].host_mixed_script == 1 and X.iloc[4].host_n_scripts == 2)
    check("host_ipv4 and no registrable label", X.iloc[5].host_ipv4 == 1 and X.iloc[5].reg_len == 0)
    check("unknown host falls to host_other", X.iloc[6].host_other == 1)
    check("shortener_in_url: a shortener domain inside a query value", f("http://a.com/p?u=bit.ly/xyz").shortener_in_url == 1 and f("http://a.com/p?u=example.org/xyz").shortener_in_url == 0)
    hl = P[P.kind == "hlabel"].groupby("row").size().to_dict()
    check("hlabel rows: non-www sub-domains + registrable (row 3: www skipped, www2 + example = 2)", hl.get(3) == 2 and hl.get(0) == 1 and 5 not in hl)
    from urlfeat.visitor import is_tld_label
    tl = set(open(pathlib.Path(__file__).resolve().parents[1] / "lists" / "tlds.txt").read().split())
    ex = set(open(pathlib.Path(__file__).resolve().parents[1] / "lists" / "exts.txt").read().split())
    check("is_tld_label (grammar lexer) equals the old lists (tlds.txt minus exts.txt) on every listed label", all(is_tld_label(x) == (x in tl and x not in ex) for x in sorted(tl | ex)))
    check("is_tld_label rejects non-TLDs", not is_tld_label("notatld") and not is_tld_label("php"))
    return out


def part_tests(n=1500, seed=0):
    """the 29 part features (segment / query key / query value / host label rows) on random strings, against naive references"""
    rng = random.Random(seed)
    bits = WORDS + ["", "A1", "x_y", "-", "a.b", "%41", "50%zz", "me@x.org", "0123456789abcdef0123", "123e4567-e89b-12d3-a456-426614174000", "AbC1dEf2GhI3jKl4MnO5", "aaaa", "77777", "file.php", "logo.png",
                    "evil.com", "x.zip", "page.html", "Q", "ÄÖ"]
    from urlfeat.visitor import URLVisitor, SCRIPT_EXT, DOC_EXT, IMG_EXT, ARCH_EXT
    v = URLVisitor()
    v.with_parts = True
    kit = {l.split("\t")[0] for l in open(pathlib.Path(__file__).resolve().parents[1] / "lists" / "suspicious_words.tsv", encoding="utf-8") if "\t" in l and not l.startswith("#") and l.strip().split("\t")[1] == "kit"}
    stats = {c: [0, 0, []] for c in PART_COLS}
    for _ in range(n):
        t = "".join(rng.choice(bits) for _ in range(rng.choice([1, 1, 2, 3])))
        kind = rng.choice(["seg", "qkey", "qval", "hlabel"])
        got = v._part(t, kind)
        d = decode(t).lower()
        m = max(len(t), 1)
        lg, ty = RD.spelling(t)
        ext = t.rsplit(".", 1)[-1].lower() if "." in t else ""
        runs = ["".join(g) for k, g in itertools.groupby(t, key=lambda c: c in HEXD) if k]
        b64 = ["".join(g) for k, g in itertools.groupby(t, key=lambda c: c.isascii() and (c.isalnum() or c in "+/_=-")) if k]
        phrase = [l.split("\t")[0] for l in open(pathlib.Path(__file__).resolve().parents[1] / "lists" / "suspicious_words.tsv", encoding="utf-8") if "\t" in l and not l.startswith("#") and l.strip().split("\t")[1] == "phrase"]
        exp = {"len": len(t), "alpha_rate": sum(c.isalpha() for c in t) / m, "digit_rate": sum(c.isdigit() for c in t) / m, "upper_rate": sum(c.isupper() for c in t) / m,
               "hyphens": t.count("-"), "underscores": t.count("_"), "dots": t.count("."), "ent": entropy(t), "ent_norm": norm_entropy(t),
               "hex16": float(any(len(r) >= 16 for r in runs)), "uuid": float(any(t[i:i + 36].count("-") == 4 and len(t[i:i + 36]) == 36 and all(c in HEXD or c == "-" for c in t[i:i + 36]) and
                                                                                      [len(x) for x in t[i:i + 36].split("-")] == [8, 4, 4, 4, 12] for i in range(len(t)))),
               "b64": float(any(len(r) >= 16 and any(c.isdigit() for c in r) and any(c.isupper() for c in r) and any(c.islower() for c in r) for r in b64)),
               "pct": n_pct(t), "has_at": float("@" in t), "domainlike": float(any(a and b and a[0].isalnum() and b[0].isalnum() and a.isascii() and b.isascii() for chunk in
                                                                                           ["".join(g) for k, g in itertools.groupby(d, key=lambda c: c.isascii() and (c.isalnum() or c in "-.")) if k] for a, b in zip(chunk.split("."), chunk.split(".")[1:]))), "rep": float(has_rep([t])), "legibility": lg, "typo": ty, "leet": RD.leet(t), "vowel_ratio": RD.vowel_ratio(t), "consonant_run": RD.consonant_run(t),
               "ext_script": float(ext in SCRIPT_EXT), "ext_doc": float(ext in DOC_EXT), "ext_img": float(ext in IMG_EXT), "ext_arch": float(ext in ARCH_EXT),
               "sw_phrase": len(set(naive_find(phrase, d))) if d else 0, "sw_kit": len(set(tokens(d)) & kit), "brand_in": len({x for x in tokens(d) if x in L.brands}), "is_val": float(kind == "qval")}
        for c, e in exp.items():
            ok = abs(got[c] - e) <= 1e-9 * max(1.0, abs(e))
            stats[c][0] += ok
            stats[c][1] += 1
            if not ok and len(stats[c][2]) < 3:
                stats[c][2].append((t, e, got[c]))
    return stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=400)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    stats, ts = run(a.n, a.seed)
    tested = {c: s for c, s in stats.items() if s[1]}
    bad = {c: s for c, s in tested.items() if s[0] != s[1]}
    md = [f"# Feature tests on {a.n} random URLs (seed {a.seed})", "", f"{len(tested)} of {len(COLUMNS)} feature columns have a reference ({len([c for c in tested if c in WIRING])} of them `wiring`: a helper called on the right text); "
          f"{len(tested) - len(bad)} pass on every URL, {len(bad)} fail on at least one.", "", "Not covered by the random generator: " + ", ".join(sorted(set(COLUMNS) - set(tested))), ""]
    for c in sorted(bad):
        s = bad[c]
        md.append(f"* FAIL `{c}`: {s[0]}/{s[1]}; e.g. " + "; ".join(f"{u!r}: expected {e:.5g}, got {g:.5g}" for u, e, g in s[2]))
    ps = part_tests()
    pbad = {c: x for c, x in ps.items() if x[0] != x[1]}
    md += ["", f"Part features (segment / key / value / host label), {max(x[1] for x in ps.values())} random strings: {len(ps) - len(pbad)} of {len(ps)} columns pass on every string."]
    md += [f"* FAIL part `{c}`: {x[0]}/{x[1]}; e.g. " + "; ".join(f"{u!r}: expected {e:.5g}, got {g:.5g}" for u, e, g in x[2]) for c, x in pbad.items()]
    md += ["", "Targeted cases:"] + [f"* {'ok  ' if ok else 'FAIL'} {name}" for name, ok in targeted()]
    text = "\n".join(md)
    print(text)
    if a.out:
        open(a.out, "w").write(text + "\n")
    return len(bad) + len(pbad) + sum(not ok for _, ok in targeted())


def test_features():
    stats, _ = run(200, 1)
    assert all(s[0] == s[1] for s in stats.values())


def test_parts():
    assert all(x[0] == x[1] for x in part_tests(500, 1).values())


def test_targeted():
    assert all(ok for _, ok in targeted())


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
