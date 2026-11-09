"""Grammar-derived features (python port of url_grammar/src/features/Features.java).

The ANTLR lexer/parser (grammar/*.g4, generated into urlfeat/parser/) splits a URL into scheme, host
(IPv4 | subdomains + registrable + public suffix | platform), port, path segments, query pairs, fragment.
`structure(url)` returns the 63-column row of the Java tool (dict) or None when the grammar rejects the URL.
"""
import pathlib
import re
import sys

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "parser"))
from UrlLexer import UrlLexer  # noqa: E402
from UrlParser import UrlParser  # noqa: E402

LISTS = pathlib.Path(__file__).resolve().parents[2] / "lists"
TLDS = set(LISTS.joinpath("tlds.txt").read_text().split())
EXTS = set(LISTS.joinpath("exts.txt").read_text().split())

PCT = re.compile(r"%[0-9a-fA-F]{2}")
REP = re.compile(r"(.)\1{2,}", re.I)
REP_DIGIT = re.compile(r"([0-9])\1{2,}")
IPV4 = re.compile(r"(?<![0-9])(?:(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])(?![0-9])")
DOMAINLIKE = re.compile(r"(?<![a-z0-9-])[a-z0-9][a-z0-9-]*(?:\.[a-z0-9][a-z0-9-]*)+(?![a-z0-9-])", re.I)
HEX = re.compile(r"[0-9a-f]{16,}", re.I)
UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I)
HOSTPORT = re.compile(r"((?:[a-z0-9-]+\.)+[a-z0-9-]+|localhost):([0-9]{2,5})(?![0-9])", re.I)


class _Count(ErrorListener):
    n = 0

    def syntaxError(self, *a):
        self.n += 1


def _count(ts, ctx, ttype):
    if ctx is None or ctx.start is None or ctx.stop is None:
        return 0
    return sum(t.type == ttype for t in ts.tokens[ctx.start.tokenIndex:ctx.stop.tokenIndex + 1])


def _dec(x):  # %XX -> ASCII character, anything else stays escaped
    return PCT.sub(lambda m: chr(int(m.group()[1:], 16)) if int(m.group()[1:], 16) < 128 else m.group(), x)


def _clean(x):
    return PCT.sub("", x)


def _digit_rate(x):
    c = _clean(x)
    return sum("0" <= ch <= "9" for ch in c) / len(c) if c else 0.0


def _longest_digit_run(x):
    best = cur = 0
    for ch in x:
        cur = cur + 1 if "0" <= ch <= "9" else 0
        best = max(best, cur)
    return best


def _max_len(l):
    return max(map(len, l), default=0)


def _mean_len(l):
    return sum(map(len, l)) / len(l) if l else 0.0


def _any_rep(pieces, rx, skip_www=False):
    return any(rx.search(_clean(x)) for x in pieces if not (skip_www and x.lower() == "www"))


def _text_features(url, host, host_is_ip, path, query, frag, segs, qkeys, qvals):
    labels = [l for l in host.split(".") if l]
    qpieces = qkeys + qvals
    allp = labels + segs + qpieces + ([frag] if frag else [])
    emb = _dec(" ".join((path, query, frag)))
    dom = False
    for m in DOMAINLIKE.finditer(emb):
        g = m.group().lower()
        last = g.rpartition(".")[2]
        if last in TLDS and last not in EXTS and not IPV4.fullmatch(g):
            dom = True
            break
    hexv = bool(UUID.search(emb)) or any(any(c.isdigit() for c in g) and any(c in "abcdefABCDEF" for c in g)
                                         for g in (m.group() for m in HEX.finditer(emb)))
    port = False
    for m in HOSTPORT.finditer(emb):
        h = m.group(1).lower()
        last = h.rpartition(".")[2]
        if int(m.group(2)) <= 65535 and (h == "localhost" or IPV4.fullmatch(h) or (last in TLDS and last not in EXTS)):
            port = True
            break
    return {
        "max_label_len": _max_len(labels), "mean_seg_len": _mean_len(segs), "max_qkey_len": _max_len(qkeys),
        "max_qval_len": _max_len(qvals), "mean_qval_len": _mean_len(qvals),
        "host_digit_rate": _digit_rate(host), "path_digit_rate": _digit_rate(path),
        "query_digit_rate": _digit_rate(query), "url_digit_rate": _digit_rate(url),
        "longest_digit_run": _longest_digit_run(_clean(url)),
        "rep_char_host": int(_any_rep(labels, REP, True)), "rep_char_path": int(_any_rep(segs, REP)),
        "rep_char_query": int(_any_rep(qpieces, REP)), "rep_digit": int(_any_rep(allp, REP_DIGIT)),
        "emb_ip": int(bool(IPV4.search(emb)) or (not host_is_ip and bool(IPV4.search(host)))),
        "emb_domain": int(dom), "emb_hex": int(hexv), "emb_port": int(port),
        "n_dash_host": host.count("-"), "n_dash_url": url.count("-"), "n_dots_host": host.count("."),
        "n_underscore": url.count("_"), "n_at": url.count("@"), "non_ascii": int(any(ord(c) > 127 for c in url)),
    }


def structure(url):
    lx = UrlLexer(InputStream(url))
    lx.removeErrorListeners()
    ts = CommonTokenStream(lx)
    p = UrlParser(ts)
    p.removeErrorListeners()
    errs = _Count()
    p.addErrorListener(errs)
    u = p.url()
    if errs.n:
        return None
    au = u.authority()
    h = au.host()
    hk = "ipv4" if h.ipv4() else "domain" if h.domain() else "platform" if h.platformHost() else "other"
    host_txt = h.getText().lower()
    nsub = nlab = 0
    sk = suf = reg = first = ""
    www = False
    if h.domain():
        d = h.domain()
        subs = d.subdomain()
        nsub = len(subs)
        ps = d.publicSuffix()
        sk = "platform" if ps.PLATFORM() else "icann2" if ps.SLD() and ps.tld() else "tld"
        suf, reg = ps.getText().lower(), d.registrable().getText().lower()
        nlab = nsub + 1 + (1 if ps.PLATFORM() else len(suf.split(".")))
        first = subs[0].getText().lower() if nsub else reg
        www = nsub > 0 and subs[0].getText().lower() == "www"
    elif h.platformHost():
        nlab, sk, suf, reg, first = 2, "platform_bare", host_txt, host_txt, host_txt
    elif h.otherHost():
        nlab, reg = len(h.otherHost().hostLabel()), host_txt

    pa, q, fr = u.path(), u.query(), u.fragmentPart()
    nseg = trail = nempty = maxseg = plen = 0
    ext = ""
    segs = []
    if pa:
        sl = pa.segment()
        segs = [s.getText() for s in sl]
        nseg, pt = len(sl), pa.getText()
        plen, trail = len(pt), int(pt.endswith("/"))
        nempty = len(pa.SLASH()) - nseg - trail
        maxseg = _max_len(segs)
        if nseg and sl[-1].fileExt() and pt.endswith(sl[-1].getText()):
            ext = sl[-1].fileExt().getText().lower()
    npairs = nev = 0
    qkeys, qvals = [], []
    if q:
        pairs = q.pair()
        npairs = len(pairs)
        for pr in pairs:
            if pr.EQ() and not pr.value().getText():
                nev += 1
            qkeys.append(pr.key().getText())
            if pr.EQ():
                qvals.append(pr.value().getText())
    pct = sum(t.type == UrlLexer.PCT for t in ts.tokens)
    stray = sum(t.type == UrlLexer.STRAY_PCT for t in ts.tokens)
    row = {
        "url_len": len(url), "scheme": u.SCHEME_PREFIX().getText()[:-3].lower() if u.SCHEME_PREFIX() else "", "host_kind": hk, "userinfo": int(au.userinfo() is not None),
        "port": au.port().getText() if au.port() else "", "n_sub": nsub, "n_labels": nlab, "suffix_kind": sk, "suffix": suf,
        "reg": reg, "first_label": first, "www": int(www), "punycode": _count(ts, au.host(), UrlLexer.PUNYCODE),
        "host_len": len(host_txt), "reg_len": len(reg), "reg_hyphens": reg.count("-"), "reg_digits": sum(c.isdigit() for c in reg),
        "has_path": int(pa is not None), "n_seg": nseg, "trailing_slash": trail, "n_empty_seg": nempty, "max_seg_len": maxseg,
        "path_len": plen, "ext": ext, "pct_total": pct, "stray_pct": stray, "has_query": int(q is not None),
        "n_amp_esc": _count(ts, q, UrlLexer.AMP_ESC), "n_pairs": npairs, "n_empty_val": nev, "query_len": len(q.getText()) if q else 0,
        "n_nested": _count(ts, q, UrlLexer.NESTED_URL),
        "n_email": _count(ts, pa, UrlLexer.EMAIL) + _count(ts, q, UrlLexer.EMAIL) + _count(ts, fr, UrlLexer.EMAIL),
        "has_frag": int(fr is not None), "frag_len": len(fr.getText()) if fr else 0, "host": host_txt,
        "segs": segs, "qvals": qvals, "qkeys": qkeys,
    }
    row.update(_text_features(url, host_txt, hk == "ipv4", pa.getText() if pa else "", q.getText() if q else "",
                              fr.getText()[1:] if fr else "", segs, qkeys, qvals))
    return row
