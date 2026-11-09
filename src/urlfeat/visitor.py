"""URLVisitor: ONE visit of the ANTLR parse tree builds every feature of a URL (and the rows of its parts: path segments, query keys, query values, host labels).

    v = URLVisitor();  r = v.run(url)      ->  r.row (141 columns, urlfeat.COLUMNS), r.host (the host frame), r.parts (rows of path segments, query keys, query values) or None when the grammar rejects the URL

The class is a child of the visitor generated from UrlParser.g4. Every `visit*` method records what its rule contains and computes the features that belong to it:
    visitUrl            scheme, then (after the children) the features of the whole string and of several parts together
    visitAuthority      userinfo, port
    visitHost           host kind and the features of the host text; visitDomain (subdomains, registrable, suffix, hosting platform from platforms.txt) and visitOtherHost: its pieces
    visitPath           features of the path (+ its segments: visitSegment, visitFileExt)
    visitQuery          features of the query (+ visitPair, visitKey, visitValue)
    visitFragmentPart   fragment
    visitTerminal       token counts per component (%XX, stray %, punycode, &amp;, nested URL, e-mail)
No regular expressions: patterns are tokens of the grammars (UrlLexer.g4 for the URL, the generated Words* lexers for the word lists) or scanners in `text.py`.
The URL string is read as given; decoded or lower-cased copies are made for matching only."""
import functools
import pathlib
import sys
from dataclasses import dataclass

import numpy as np
from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "parser"))
from UrlLexer import UrlLexer  # noqa: E402
from UrlParser import UrlParser  # noqa: E402
from UrlParserVisitor import UrlParserVisitor  # noqa: E402

from . import obfuscation as OB  # noqa: E402
from . import popularity, readability as RD, text as T, wordlists  # noqa: E402

LISTS = pathlib.Path(__file__).resolve().parents[1] / "lists"
SUSPICIOUS_TLDS = {w for l in LISTS.joinpath("suspicious_tlds.txt").read_text().splitlines() if l.strip() and not l.startswith("#") for w in l.split()}
# column groups of the lexical features (names only; the values come from the visit methods; used by the feature table)
DELIMS = set("~`!^*()[]{}\"';:,><|")   # the paper's F3 set
OTHER = set("+$=&.:#%")                # the paper's F4 set
LEXICAL_GROUPS = {
    "entropy": ["ent_url", "ent_path", "ent_url_norm", "ent_path_norm", "ent_reg", "ent_max_seg", "ent_max_qval"],
    "special_chars": [f"sc_{k}_{c}" for k in ("delims", "other") for c in ("url", "host", "path", "query")],
    "suspicious_words": ["sw_phrase_url", "sw_phrase_host", "sw_phrase_path", "sw_phrase_query", "sw_brand_url", "sw_host_url", "sw_kit_url", "sw_kit_path"],
    "brand": ["brand_in_sub", "brand_in_reg", "brand_wrong_tld", "brand_typo", "brand_in_path", "brand_in_query", "reg_popular"],
    "shortener": ["is_shortener", "shortener_in_url"],
    "amp_eq": ["n_amp_url", "n_eq_url", "amp_gt_eq"],
    "path_counts": ["n_dots_path", "n_hyphens_path"],
    "http_www": ["http_after_host", "www_after_host", "www_extra_label"],
}
LEXICAL_COLUMNS = [c for g in LEXICAL_GROUPS.values() for c in g]
EXT_FLAGS = ["php", "html", "htm", "asp", "aspx", "jsp", "exe", "zip"]

COLUMNS = ['https', 'ftp', 'host_ipv4', 'host_platform', 'host_other', 'sfx_platform', 'sfx_platform_bare', 'sfx_icann2', 'has_ext', 'port', 'has_path', 'trailing_slash', 'path_len', 'userinfo', 'www',
           'punycode', 'has_query', 'n_amp_esc', 'n_nested', 'n_email', 'has_frag', 'pct_total', 'stray_pct', 'rep_char_host', 'rep_char_path', 'rep_char_query', 'rep_digit', 'emb_ip', 'emb_domain',
           'emb_hex', 'emb_port', 'non_ascii', 'n_sub', 'n_seg', 'n_empty_seg', 'n_pairs', 'n_empty_val', 'url_len', 'host_len', 'reg_len', 'reg_hyphens', 'reg_digits', 'max_seg_len', 'query_len',
           'frag_len', 'max_label_len', 'mean_seg_len', 'max_qkey_len', 'max_qval_len', 'mean_qval_len', 'longest_digit_run', 'n_dash_host', 'n_dash_url', 'n_dots_host', 'n_underscore', 'n_at',
           'host_digit_rate', 'path_digit_rate', 'query_digit_rate', 'url_digit_rate', 'ent_url', 'ent_path', 'ent_url_norm', 'ent_path_norm', 'ent_reg', 'ent_max_seg', 'ent_max_qval',
           'sc_delims_url', 'sc_delims_host', 'sc_delims_path', 'sc_delims_query', 'sc_other_url', 'sc_other_host', 'sc_other_path', 'sc_other_query', 'sw_phrase_url', 'sw_phrase_host',
           'sw_phrase_path', 'sw_phrase_query', 'sw_brand_url', 'sw_host_url', 'sw_kit_url', 'sw_kit_path', 'brand_in_sub', 'brand_in_reg', 'brand_wrong_tld', 'brand_typo', 'brand_in_path',
           'brand_in_query', 'reg_popular', 'is_shortener', 'shortener_in_url', 'n_amp_url', 'n_eq_url', 'amp_gt_eq', 'n_dots_path', 'n_hyphens_path', 'http_after_host', 'www_after_host',
           'www_extra_label', 'url_legibility', 'url_typo_rate', 'url_leet', 'host_legibility', 'host_typo_rate', 'host_leet', 'sld_legibility', 'sld_typo_rate', 'sld_leet', 'sld_vowel_ratio',
           'sld_consonant_run', 'seg_min_legibility', 'seg_max_typo', 'qval_min_legibility', 'qval_max_typo', 'seg_max_leet', 'seg_consonant_run', 'tld_suspicious', 'tld_cc', 'tld_has_digit',
           'ext_php', 'ext_html', 'ext_htm', 'ext_asp', 'ext_aspx', 'ext_jsp', 'ext_exe', 'ext_zip', 'ratio_delims_url', 'ratio_other_url', 'ratio_nonalnum_url', 'ratio_nonalnum_host',
           'ratio_hyphen_url', 'ratio_dot_url', 'host_n_scripts', 'host_mixed_script', 'host_confusable_chars', 'brand_lookalike_reg', 'brand_lookalike_host', 'host_digit_in_word', 'reg_log_rank']

# how a raw count / measurement becomes the column value (the transform each column has always had)
BINARY = {"userinfo", "www", "punycode", "has_query", "n_amp_esc", "n_nested", "n_email", "has_frag", "pct_total", "stray_pct", "rep_char_host", "rep_char_path", "rep_char_query", "rep_digit",
          "emb_ip", "emb_domain", "emb_hex", "emb_port", "non_ascii"}  # 1 when the count is above 0
LOG1P = {"path_len", "n_sub", "n_seg", "n_empty_seg", "n_pairs", "n_empty_val", "url_len", "host_len", "reg_len", "reg_hyphens", "reg_digits", "max_seg_len", "query_len", "frag_len", "max_label_len",
         "max_qkey_len", "max_qval_len", "longest_digit_run", "n_dash_host", "n_dash_url", "n_dots_host", "n_underscore", "n_at"}
LEX_LOG1P = ("sc_", "sw_", "n_amp_url", "n_eq_url", "n_dots_path", "n_hyphens_path", "http_after_host", "www_after_host", "brand_in_sub", "brand_in_path", "brand_in_query", "www_extra_label")
LEX_COLUMNS = {"ent_url", "ent_path", "ent_url_norm", "ent_path_norm", "ent_reg", "ent_max_seg", "ent_max_qval", "sc_delims_url", "sc_delims_host", "sc_delims_path", "sc_delims_query",
               "sc_other_url", "sc_other_host", "sc_other_path", "sc_other_query", "sw_phrase_url", "sw_phrase_host", "sw_phrase_path", "sw_phrase_query", "sw_brand_url", "sw_host_url",
               "sw_kit_url", "sw_kit_path", "brand_in_sub", "brand_in_reg", "brand_wrong_tld", "brand_typo", "brand_in_path", "brand_in_query", "reg_popular", "is_shortener", "shortener_in_url",
               "n_amp_url", "n_eq_url", "amp_gt_eq", "n_dots_path", "n_hyphens_path", "http_after_host", "www_after_host", "www_extra_label"}

HOST_COLS = ["https", "ftp", "host_ipv4", "host_platform", "host_other", "sfx_platform", "sfx_platform_bare", "sfx_icann2", "port", "userinfo", "www", "punycode", "rep_char_host",
             "n_sub", "host_len", "reg_len", "reg_hyphens", "reg_digits", "max_label_len", "n_dash_host", "n_dots_host", "host_digit_rate", "ent_reg", "sc_delims_host", "sc_other_host",
             "sw_phrase_host", "brand_in_sub", "brand_in_reg", "brand_wrong_tld", "brand_typo", "reg_popular", "is_shortener", "www_extra_label", "host_legibility", "host_typo_rate",
             "host_leet", "sld_legibility", "sld_typo_rate", "sld_leet", "sld_vowel_ratio", "sld_consonant_run", "tld_suspicious", "tld_cc", "tld_has_digit", "ratio_nonalnum_host",
             "host_n_scripts", "host_mixed_script", "host_confusable_chars", "brand_lookalike_reg", "brand_lookalike_host", "host_digit_in_word", "reg_log_rank"]
PART_COLS = ["len", "alpha_rate", "digit_rate", "upper_rate", "hyphens", "underscores", "dots", "ent", "ent_norm", "hex16", "uuid", "b64", "pct", "has_at", "domainlike", "rep",
             "legibility", "typo", "leet", "vowel_ratio", "consonant_run", "ext_script", "ext_doc", "ext_img", "ext_arch", "sw_phrase", "sw_kit", "brand_in", "is_val"]
HL_STATS = [c for c in PART_COLS if c != "is_val"]
HL_COLS = [f"hlabel_{c}_{s}" for c in HL_STATS for s in ("mean", "max", "min")]  # optional host columns: mean / max / min of the part features over the host's labels
SCRIPT_EXT, DOC_EXT, IMG_EXT, ARCH_EXT = {"php", "asp", "aspx", "jsp", "cgi", "pl"}, {"html", "htm", "shtml", "xhtml"}, {"jpg", "jpeg", "png", "gif", "svg", "ico", "webp", "css", "js"}, {"zip", "rar", "exe", "apk", "7z"}


class _Count(ErrorListener):
    n = 0

    def syntaxError(self, *a):
        self.n += 1


@dataclass
class Result:
    row: dict      # the 141 columns, by name
    host: dict     # HOST_COLS
    parts: list    # dicts: kind (seg / qkey / qval) + PART_COLS


@functools.lru_cache(maxsize=None)
def is_tld_label(label):
    """True when the grammar itself reads `label` as one TLD / SLD token (authority mode) and NOT as a file-extension token (path mode): the vocabulary is the grammar's, not a list"""
    lx = UrlLexer(InputStream(label))
    lx.removeErrorListeners()
    toks = lx.getAllTokens()
    if len(toks) != 1 or toks[0].type not in (UrlLexer.TLD, UrlLexer.SLD):
        return False
    px = UrlLexer(InputStream("/x." + label))
    px.removeErrorListeners()
    return px.getAllTokens()[-1].type != UrlLexer.EXT


def _max_len(l):
    return max(map(len, l), default=0)


def _mean_len(l):
    return sum(map(len, l)) / len(l) if l else 0.0


class URLVisitor(UrlParserVisitor):
    def __init__(self, normalised=False):
        self.L = wordlists.load()
        self.normalised = normalised  # True: features of the task's "same page" view (see normal_form); the input string itself is never changed

    def normal_form(self, url):
        """The task's "same page" key, read with the grammar's own tokens: lower-cased, without the scheme token (SCHEME_PREFIX), without a leading `www.` label (WWW DOT)
        and without trailing slashes. Equal to common.norm_key on every supplied URL (src/tests/test_normalised.py). URLs that differ only in these respects get identical features."""
        s = url.strip().lower()
        lx = UrlLexer(InputStream(s))
        lx.removeErrorListeners()
        toks = lx.getAllTokens()
        i = 1 if toks and toks[0].type == UrlLexer.SCHEME_PREFIX else 0
        if len(toks) > i + 1 and toks[i].type == UrlLexer.WWW and toks[i + 1].type == UrlLexer.DOT:
            i += 2
        return (s[toks[i].start:] if i < len(toks) else "").rstrip("/")

    # ------------------------------------------------------------------ entry point
    def run(self, url, parts=True, host_labels=False):
        """parse + one visit; None when the grammar rejects the string (or anything goes wrong): such a URL has no features.
        parts=False skips the 29 features of every segment / key / value that only the parts model uses (the row does not need them); host_labels=True adds one part row per host label
        (kind `hlabel`, not `www`), used by the optional host-label aggregates of the parts model (they did not help, see CLAUDE.md)."""
        try:
            if self.normalised:
                url = self.normal_form(url)
            lx = UrlLexer(InputStream(url))
            lx.removeErrorListeners()
            p = UrlParser(CommonTokenStream(lx))
            p.removeErrorListeners()
            errs = _Count()
            p.addErrorListener(errs)
            tree = p.url()
            if errs.n:
                return None
            self._reset(url)
            self.with_parts, self.host_labels = parts, host_labels
            self.visit(tree)
            row = {c: self.f[c] for c in COLUMNS}
            host = {c: row[c] for c in HOST_COLS}
            if parts and host_labels:
                host.update(self._hlabel_aggregates())
            return Result(row, host, (self.seg_rows + self.key_rows + self.val_rows + self.hl_rows) if parts else [])
        except Exception:
            return None

    def _hlabel_aggregates(self):
        """mean / max / min of the part features over the host's labels (NaN where the host has none: IPv4, bare platform)"""
        if not self.hl_rows:
            return dict.fromkeys(HL_COLS, np.nan)
        M = np.array([[r[c] for c in HL_STATS] for r in self.hl_rows], dtype=float)
        return {f"hlabel_{c}_{s}": float(f(M[:, j])) for j, c in enumerate(HL_STATS) for s, f in (("mean", np.mean), ("max", np.max), ("min", np.min))}

    def _reset(self, url):
        self.url, self.rest = url, url
        self.f = dict.fromkeys(COLUMNS, 0.0)
        self.f["seg_min_legibility"] = self.f["qval_min_legibility"] = 1.0
        self.scheme = ""
        self.userinfo, self.port = False, ""
        self.kind, self.host, self.subs, self.reg, self.suffix, self.sfx_kind = "", "", [], "", "", ""
        self.popular, self.rs = 0, ""
        self.path, self.query, self.frag = "", "", ""  # query WITH '?', fragment WITHOUT '#'
        self.segs, self.qkeys, self.qvals = [], [], []
        self.n_slash, self.n_pairs, self.n_empty_val = 0, 0, 0
        self.seg_rows, self.key_rows, self.val_rows, self.hl_rows = [], [], [], []
        self._last_seg, self._last_ext, self._cur_ext = "", "", ""
        self.pct = self.stray = self.puny = self.amp_esc = self.nested = self.email = 0
        self._comp = ""

    def _set(self, col, v):
        """store a measurement under its column, with the transform that column has"""
        if col in BINARY:
            self.f[col] = float(v > 0)
        elif col in LOG1P:
            self.f[col] = float(np.log1p(v))
        elif col in LEX_COLUMNS and col.startswith(LEX_LOG1P):
            self.f[col] = float(np.log1p(v))
        else:
            self.f[col] = float(v)

    def _words(self, group, txt):
        return len(set(self.L.words[group].find_all(txt))) if txt else 0

    def _brands_in(self, txt):
        """distinct brands in a decoded lower-cased text: whole tokens that are brands, plus long brands as substrings; the page's own registrable label does not count"""
        if self.popular or not txt:
            return 0
        found = {t for t in wordlists.TOKENS.find_all(txt) if t in self.L.brands} | set(self.L.brand_long.find_all(txt))
        found.discard(self.reg)
        return len(found)

    # ------------------------------------------------------------------ url
    def visitUrl(self, ctx):
        sp = ctx.SCHEME_PREFIX()
        if sp:
            self.scheme = sp.getText()[:-3].lower()
            self.rest = self.url[len(sp.getText()):]
        self._set("https", self.scheme == "https")
        self._set("ftp", self.scheme == "ftp")
        self.visitChildren(ctx)
        self._finish()

    def _finish(self):
        """features of the whole string and of several parts together (they need the children's results)"""
        url, rest, host = self.url, self.rest, self.host
        dpath, dquery, dfrag = T.decode_pct(self.path).lower(), T.decode_pct(self.query[1:]).lower(), T.decode_pct(self.frag).lower()
        drest = T.decode_pct(rest).lower()
        n = max(len(url), 1)
        self._set("url_len", len(url))
        self._set("url_digit_rate", T.digit_rate(url))
        self._set("longest_digit_run", T.longest_digit_run(T.strip_pct(url)))
        self._set("n_dash_url", url.count("-"))
        self._set("n_underscore", url.count("_"))
        self._set("n_at", url.count("@"))
        self._set("non_ascii", sum(ord(c) > 127 for c in url) > 0)
        self._set("pct_total", self.pct)
        self._set("stray_pct", self.stray)
        self._set("n_email", self.email)
        # entropy, special characters, & versus =
        self._set("ent_url", T.entropy(rest))
        self._set("ent_url_norm", T.norm_entropy(rest))
        self._set("sc_delims_url", T.count_in(rest, DELIMS))
        self._set("sc_other_url", T.count_in(rest, OTHER))
        self._set("n_amp_url", rest.count("&"))
        self._set("n_eq_url", rest.count("="))
        self._set("amp_gt_eq", rest.count("&") > rest.count("="))
        # suspicious words in the whole decoded string; http / www after the host
        self._set("sw_phrase_url", self._words("phrase", drest))
        self._set("sw_brand_url", self._words("brand", drest))
        self._set("sw_host_url", self._words("host", drest))
        self._set("sw_kit_url", len(set(wordlists.TOKENS.find_all(drest)) & self.L.kit) if drest else 0)
        after = " ".join(x for x in (dpath, dquery, dfrag) if x)
        self._set("http_after_host", after.count("http"))
        self._set("www_after_host", after.count("www"))
        self._set("shortener_in_url", int(any(self._suffix_hit(t) for t in T.dotted_names(after))) if "." in after else 0)
        # readability of the whole string; ratios
        leg, typo = RD.spelling(url)
        self._set("url_legibility", leg)
        self._set("url_typo_rate", typo)
        self._set("url_leet", RD.leet(url))
        self._set("ratio_delims_url", sum(c in DELIMS for c in url) / n)
        self._set("ratio_other_url", sum(c in OTHER for c in url) / n)
        self._set("ratio_nonalnum_url", sum(not c.isalnum() for c in url) / n)
        self._set("ratio_hyphen_url", url.count("-") / n)
        self._set("ratio_dot_url", url.count(".") / n)
        # repeated digits anywhere; embedded IP / host name / hex / host:port in path, query and fragment
        labels = [l for l in host.split(".") if l]
        self._set("rep_digit", T.any_repeat(labels + self.segs + self.qkeys + self.qvals + ([self.frag] if self.frag else []), digits_only=True))
        emb = T.decode_pct(" ".join((self.path, self.query, self.frag)))
        self._set("emb_ip", T.has_ipv4(emb) or (self.kind != "ipv4" and T.has_ipv4(host)))
        self._set("emb_domain", any(self._is_host_name(g.lower()) for g in T.domain_like(emb)))
        self._set("emb_hex", T.has_uuid(emb) or any(any(c.isdigit() for c in g) and any(c in "abcdefABCDEF" for c in g) for g in T.hex_runs(emb)))
        self._set("emb_port", any(p <= 65535 and (h.lower() == "localhost" or T.is_ipv4(h.lower()) or self._is_host_name(h.lower())) for h, p in T.host_ports(emb)))

    @staticmethod
    def _is_host_name(g):
        """ends in a TLD of the grammar's vocabulary that is not also a file extension, and is not an IPv4 address"""
        return is_tld_label(g.rpartition(".")[2]) and not T.is_ipv4(g)

    def _suffix_hit(self, token):
        p = token.split(".")
        return any(".".join(p[i:]) in self.L.shorteners for i in range(len(p)))

    # ------------------------------------------------------------------ authority and host
    def visitAuthority(self, ctx):
        self.userinfo = ctx.userinfo() is not None
        port = ctx.port()
        self.port = port.getText() if port else ""
        self._set("userinfo", self.userinfo)
        self._set("port", self.port != "")
        return self.visitChildren(ctx)

    def visitHost(self, ctx):
        self._comp = "host"
        self.kind = "ipv4" if ctx.ipv4() else "domain" if ctx.domain() else "other"
        self.visitChildren(ctx)
        if self.sfx_kind == "platform_bare":  # the host is a platform name itself (set by visitDomain)
            self.kind = "platform"
        self._comp = ""
        host = self.host = ctx.getText().lower()
        if self.kind == "platform":
            self.reg = self.suffix = host
        elif self.kind == "other":
            self.reg = host
        reg, suffix, L = self.reg, self.suffix, self.L
        self._set("host_ipv4", self.kind == "ipv4")
        self._set("host_platform", self.kind == "platform")
        self._set("host_other", self.kind == "other")
        self._set("sfx_platform", self.sfx_kind == "platform")
        self._set("sfx_platform_bare", self.sfx_kind == "platform_bare")
        self._set("sfx_icann2", self.sfx_kind == "icann2")
        self._set("n_sub", len(self.subs))
        self._set("www", len(self.subs) > 0 and self.subs[0] == "www")
        self._set("punycode", self.puny)
        self._set("host_len", len(host))
        self._set("reg_len", len(reg))
        self._set("reg_hyphens", reg.count("-"))
        self._set("reg_digits", sum(c.isdigit() for c in reg))
        labels = [l for l in host.split(".") if l]
        self._set("max_label_len", _max_len(labels))
        self._set("host_digit_rate", T.digit_rate(host))
        self._set("rep_char_host", T.any_repeat(labels, skip_www=True))
        self._set("n_dash_host", host.count("-"))
        self._set("n_dots_host", host.count("."))
        self._set("sc_delims_host", T.count_in(host, DELIMS))
        self._set("sc_other_host", T.count_in(host, OTHER))
        self._set("sw_phrase_host", self._words("phrase", host))
        self._set("ent_reg", T.entropy(reg) if self.kind == "domain" else 0.0)
        # popularity and brand rules (all off for a popular registrable domain)
        self.rs = f"{reg}.{suffix}" if reg and suffix else ""
        self.popular = int(bool(self.rs) and self.rs in L.popular)
        self._set("reg_popular", self.popular)
        self._set("reg_log_rank", popularity.log_rank(self.rs if self.rs else host))
        off = self.popular or self.kind == "ipv4"
        subdom = host[: -(len(self.rs) + 1)] if self.rs and host.endswith("." + self.rs) else ""
        self._set("brand_in_sub", 0 if off else len({t for t in wordlists.TOKENS.find_all(subdom) if t in L.brands and t != reg}))
        self._set("brand_in_reg", 0 if off or self.kind != "domain" else int(reg not in L.brands and any(L.brand_long.find_all(reg))))
        self._set("brand_wrong_tld", 0 if off or self.kind != "domain" else int(reg in L.brands))
        self._set("brand_typo", 0 if off or self.kind != "domain" else int(L.near_brand(reg)))
        self._set("is_shortener", int(self._suffix_hit(host)) if host else 0)
        self._set("www_extra_label", sum(1 for l in host.split(".")[1:] if l.startswith("www")))
        # readability of host and registrable label; TLD flags
        leg, typo = RD.spelling(host)
        self._set("host_legibility", leg)
        self._set("host_typo_rate", typo)
        self._set("host_leet", RD.leet(host))
        leg, typo = RD.spelling(reg)
        self._set("sld_legibility", leg)
        self._set("sld_typo_rate", typo)
        self._set("sld_leet", RD.leet(reg))
        self._set("sld_vowel_ratio", RD.vowel_ratio(reg))
        self._set("sld_consonant_run", RD.consonant_run(reg))
        tld = suffix.rsplit(".", 1)[-1]
        self._set("tld_suspicious", tld in SUSPICIOUS_TLDS)
        self._set("tld_cc", len(tld) == 2 and tld.isalpha())
        self._set("tld_has_digit", any(c.isdigit() for c in tld))
        # look-alike characters, scripts
        tokens = [t for lab in host.split(".") for t in lab.replace("_", "-").split("-") if t]
        fixed, raw = {OB.deconfuse(t) for t in tokens}, set(tokens)
        first = reg.split(".")[0]
        self._set("ratio_nonalnum_host", sum(not c.isalnum() for c in host) / max(len(host), 1))
        self._set("host_n_scripts", OB.n_scripts(host))
        self._set("host_mixed_script", OB.n_scripts(host) > 1)
        self._set("host_confusable_chars", sum(c in OB.CONFUSABLE for c in host.lower() if not c.isdigit()))
        self._set("brand_lookalike_reg", OB.deconfuse(first) in L.brands and first not in L.brands)
        self._set("brand_lookalike_host", len((fixed & L.brands) - raw) > 0)
        self._set("host_digit_in_word", any(any(c.isdigit() for c in t) and any(c.isalpha() for c in t) for t in tokens))

    def visitIpv4(self, ctx):
        return self.visitChildren(ctx)

    def visitDomain(self, ctx):
        """subdomains, registrable, public suffix. A hosting platform (platforms.txt) is the longest run of whole labels at the end of the host that is listed: the label before it is
        the tenant (registrable), the labels before that are subdomains, and a host that is a platform name itself is `platform_bare`. Platforms are not lexer tokens (a literal such as
        cloud.goog would cut the label google of cloud.google.com in two)."""
        subs = [s.getText().lower() for s in ctx.subdomain()]
        reg = ctx.registrable().getText().lower()
        suffix = ctx.publicSuffix().getText().lower()
        labels = subs + [reg] + suffix.split(".")
        plats = self.L.platforms
        cut = next((i for i in range(len(labels) - 1) if ".".join(labels[i:]) in plats), None)
        if cut is None:
            self.subs, self.reg, self.suffix = subs, reg, suffix
            self.sfx_kind = "icann2" if ctx.publicSuffix().SLD() and ctx.publicSuffix().tld() else "tld"
        elif cut == 0:
            self.sfx_kind = "platform_bare"  # reg / suffix = the whole host: visitHost
        else:
            self.subs, self.reg, self.suffix = labels[:cut - 1], labels[cut - 1], ".".join(labels[cut:])
            self.sfx_kind = "platform"
        if cut != 0:
            for s in self.subs + [self.reg]:
                self._host_label(s)
        return self.visitChildren(ctx)

    def _host_label(self, text):
        """a label of the host is a part of its own (kind `hlabel`; `www` is not a label worth scoring)"""
        if self.with_parts and self.host_labels and text.lower() != "www":
            self.hl_rows.append(self._part(text, "hlabel"))

    def visitOtherHost(self, ctx):
        for label in ctx.hostLabel():
            self._host_label(label.getText())
        return self.visitChildren(ctx)

    # ------------------------------------------------------------------ path
    def visitPath(self, ctx):
        self._comp = "path"
        path = self.path = ctx.getText()
        self.n_slash = len(ctx.SLASH())
        self.visitChildren(ctx)
        self._comp = ""
        segs, L = self.segs, self.L
        n_seg, trailing = len(segs), int(path.endswith("/"))
        ext = self._last_ext.lower() if n_seg and self._last_ext and path.endswith(self._last_seg) else ""
        dpath = T.decode_pct(path).lower()
        self._set("has_path", n_seg > 0)
        self._set("trailing_slash", trailing > 0 and n_seg > 0)
        self._set("path_len", len(path) if n_seg > 0 else 0)
        self._set("n_seg", n_seg)
        self._set("n_empty_seg", self.n_slash - n_seg - trailing)
        self._set("max_seg_len", _max_len(segs))
        self._set("mean_seg_len", _mean_len(segs))
        self._set("path_digit_rate", T.digit_rate(path))
        self._set("rep_char_path", T.any_repeat(segs))
        self._set("n_dots_path", path.count("."))
        self._set("n_hyphens_path", path.count("-"))
        self._set("ent_path", T.entropy(path))
        self._set("ent_path_norm", T.norm_entropy(path))
        self._set("ent_max_seg", max((T.entropy(s) for s in segs), default=0.0))
        self._set("sc_delims_path", T.count_in(path, DELIMS))
        self._set("sc_other_path", T.count_in(path, OTHER))
        self._set("sw_phrase_path", self._words("phrase", dpath))
        self._set("sw_kit_path", len(set(wordlists.TOKENS.find_all(dpath)) & L.kit) if dpath else 0)
        self._set("brand_in_path", self._brands_in(dpath))
        self._set("has_ext", ext != "")
        for e in EXT_FLAGS:
            self._set(f"ext_{e}", ext.lstrip(".") == e)
        if self.seg_rows:
            self._set("seg_min_legibility", min(r["legibility"] for r in self.seg_rows))
            self._set("seg_max_typo", max(r["typo"] for r in self.seg_rows))
            self._set("seg_max_leet", max(r["leet"] for r in self.seg_rows))
            self._set("seg_consonant_run", max(r["consonant_run"] for r in self.seg_rows))

    def visitSegment(self, ctx):
        t = ctx.getText()
        self.segs.append(t)
        ext = ctx.fileExt()
        self._last_seg, self._last_ext = t, ext.getText() if ext else ""
        self.seg_rows.append(self._part(t, "seg"))
        return self.visitChildren(ctx)

    def visitFileExt(self, ctx):
        return self.visitChildren(ctx)

    # ------------------------------------------------------------------ query
    def visitQuery(self, ctx):
        self._comp = "query"
        q = self.query = ctx.getText()  # with the leading '?'
        self.visitChildren(ctx)
        self._comp = ""
        qk, qv, L = self.qkeys, self.qvals, self.L
        dquery = T.decode_pct(q[1:]).lower()
        self._set("has_query", True)
        self._set("query_len", len(q))
        self._set("n_pairs", self.n_pairs)
        self._set("n_empty_val", self.n_empty_val)
        self._set("max_qkey_len", _max_len(qk))
        self._set("max_qval_len", _max_len(qv))
        self._set("mean_qval_len", _mean_len(qv))
        self._set("query_digit_rate", T.digit_rate(q))
        self._set("rep_char_query", T.any_repeat(qk + qv))
        self._set("ent_max_qval", max((T.entropy(v) for v in qv), default=0.0))
        self._set("sc_delims_query", T.count_in(q[1:], DELIMS))
        self._set("sc_other_query", T.count_in(q[1:], OTHER))
        self._set("sw_phrase_query", self._words("phrase", dquery))
        self._set("brand_in_query", self._brands_in(dquery))
        self._set("n_amp_esc", self.amp_esc)
        self._set("n_nested", self.nested)
        if self.val_rows:
            self._set("qval_min_legibility", min(r["legibility"] for r in self.val_rows))
            self._set("qval_max_typo", max(r["typo"] for r in self.val_rows))

    def visitPair(self, ctx):
        self.n_pairs += 1
        if ctx.EQ() and not ctx.value().getText():
            self.n_empty_val += 1
        return self.visitChildren(ctx)

    def visitKey(self, ctx):
        t = ctx.getText()
        self.qkeys.append(t)
        self.key_rows.append(self._part(t, "qkey"))
        return self.visitChildren(ctx)

    def visitValue(self, ctx):
        t = ctx.getText()
        self.qvals.append(t)
        self.val_rows.append(self._part(t, "qval"))
        return self.visitChildren(ctx)

    # ------------------------------------------------------------------ fragment and tokens
    def visitFragmentPart(self, ctx):
        self._comp = "frag"
        self.frag = ctx.getText()[1:]
        self.visitChildren(ctx)
        self._comp = ""
        self._set("has_frag", True)
        self._set("frag_len", len(self.frag) + 1)

    def visitTerminal(self, node):
        t = node.symbol.type
        if t == UrlLexer.PCT:
            self.pct += 1
        elif t == UrlLexer.STRAY_PCT:
            self.stray += 1
        elif t == UrlLexer.PUNYCODE:
            self.puny += self._comp == "host"
        elif t == UrlLexer.AMP_ESC:
            self.amp_esc += self._comp == "query"
        elif t == UrlLexer.NESTED_URL:
            self.nested += self._comp == "query"
        elif t == UrlLexer.EMAIL:
            self.email += self._comp in ("path", "query", "frag")

    # ------------------------------------------------------------------ one part (segment, query key or value)
    def _part(self, t, kind):
        if not self.with_parts:  # only what the full-URL row aggregates over the parts
            leg, typo = RD.spelling(t)
            return {"legibility": leg, "typo": typo, "leet": RD.leet(t), "consonant_run": RD.consonant_run(t)}
        n = max(len(t), 1)
        dec = T.decode_pct(t).lower()
        L = self.L
        ext = t.rsplit(".", 1)[-1].lower() if "." in t else ""
        leg, typo = RD.spelling(t)
        toks = wordlists.TOKENS.find_all(dec)
        return {"kind": kind, "len": len(t), "alpha_rate": sum(c.isalpha() for c in t) / n, "digit_rate": sum(c.isdigit() for c in t) / n, "upper_rate": sum(c.isupper() for c in t) / n,
                "hyphens": t.count("-"), "underscores": t.count("_"), "dots": t.count("."), "ent": T.entropy(t), "ent_norm": T.norm_entropy(t),
                "hex16": float(bool(T.hex_runs(t))), "uuid": float(T.has_uuid(t)),
                "b64": float(any(any(c.isdigit() for c in m) and any(c.isupper() for c in m) and any(c.islower() for c in m) for m in T.base64_runs(t))),
                "pct": T.count_pct(t), "has_at": float("@" in t), "domainlike": float(bool(T.domain_like(dec))), "rep": float(T.has_repeat(t)),
                "legibility": leg, "typo": typo, "leet": RD.leet(t), "vowel_ratio": RD.vowel_ratio(t), "consonant_run": RD.consonant_run(t),
                "ext_script": float(ext in SCRIPT_EXT), "ext_doc": float(ext in DOC_EXT), "ext_img": float(ext in IMG_EXT), "ext_arch": float(ext in ARCH_EXT),
                "sw_phrase": len(set(L.words["phrase"].find_all(dec))) if dec else 0, "sw_kit": len(set(toks) & L.kit), "brand_in": len({x for x in toks if x in L.brands}),
                "is_val": float(kind == "qval")}

    # ------------------------------------------------------------------ batch entry points (the only ones: nothing outside this module builds features)
    def extract(self, urls, with_parts=True, host_labels=False):
        """(features, host frame, part rows) for a list of URLs from one visit each; rows the grammar rejects are NaN / have no part rows.
        Every URL is parsed and measured exactly as given: nothing is stripped, prefixed or normalised. host_labels=True adds the `hlabel_*` columns to the host frame (and the hlabel part rows)."""
        import pandas as pd
        rows, hosts, parts = [], [], []
        for i, u in enumerate(urls):
            r = self.run(str(u), with_parts, host_labels)
            rows.append(r.row if r else {})
            hosts.append(r.host if r else {})
            if r:
                parts.extend({"row": i, **p} for p in r.parts)
        X = pd.DataFrame(rows).reindex(columns=COLUMNS).astype(float)
        H = pd.DataFrame(hosts).reindex(columns=HOST_COLS + (HL_COLS if with_parts and host_labels else [])).astype(float)
        P = pd.DataFrame(parts, columns=["row", "kind"] + PART_COLS)
        return X, H, P

    def featurize(self, urls):
        """DataFrame of the 141 columns, one row per URL"""
        return self.extract(urls, with_parts=False)[0]

    def tables(self, urls, host_labels=False):
        """(H, parts): the host frame and the long frame of segment / query key / query value (/ host label) rows, for the parts model"""
        _, H, P = self.extract(urls, host_labels=host_labels)
        return H, P

    def structure(self, url):
        """the parsed parts of one URL as a dict (host split, platform, path segments, query keys / values, counts); None when the grammar rejects it"""
        if self.run(url) is None:
            return None
        return {"scheme": self.scheme, "host_kind": self.kind, "host": self.host, "reg": self.reg, "suffix": self.suffix, "suffix_kind": self.sfx_kind, "subdomains": list(self.subs),
                "port": self.port, "userinfo": self.userinfo, "path": self.path, "segs": list(self.segs),
                "file_ext": self._last_ext if self.segs and self.path.endswith(self._last_seg) else "", "query": self.query, "qkeys": list(self.qkeys), "qvals": list(self.qvals),
                "fragment": self.frag, "pct": self.pct, "stray_pct": self.stray, "punycode": self.puny, "amp_esc": self.amp_esc, "nested": self.nested, "email": self.email}


@functools.cache
def get_visitor():
    return URLVisitor()


def set_normalised(flag):
    """switch the shared visitor between the URL as given (False, the default) and the task's normalised view (True); a run records its choice in config.json"""
    get_visitor().normalised = bool(flag)


def extract(urls, with_parts=True, host_labels=False):
    return get_visitor().extract(urls, with_parts, host_labels)


def featurize(urls):
    return get_visitor().featurize(urls)


def tables(urls, host_labels=False):
    return get_visitor().tables(urls, host_labels)


def structure(url):
    return get_visitor().structure(url)
