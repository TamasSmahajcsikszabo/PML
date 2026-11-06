"""Features of the PARTS of a URL (idea and column set adapted from url_grammar "U", engine.py): one row per path segment, per query key and per query value, plus the
host-level columns (a subset of the full-URL features). Parts are measured exactly as written in the URL; the absence of a part is never a feature value (no part -> no row)."""
import math
import re

from . import _lists, featurize, lexical, readability
from .structure import DOMAINLIKE, HEX, PCT, REP, UUID, structure

# host/scheme-level columns of urlfeat.COLUMNS (functions of the scheme and host only)
HOST_COLS = ["https", "ftp", "host_ipv4", "host_platform", "host_other", "sfx_platform", "sfx_platform_bare", "sfx_icann2", "port", "userinfo", "www", "punycode", "rep_char_host",
             "n_sub", "host_len", "reg_len", "reg_hyphens", "reg_digits", "max_label_len", "n_dash_host", "n_dots_host", "host_digit_rate", "ent_reg", "sc_delims_host", "sc_other_host",
             "sw_phrase_host", "brand_in_sub", "brand_in_reg", "brand_wrong_tld", "brand_typo", "reg_popular", "is_shortener", "www_extra_label", "host_legibility", "host_typo_rate",
             "host_leet", "sld_legibility", "sld_typo_rate", "sld_leet", "sld_vowel_ratio", "sld_consonant_run", "tld_suspicious", "tld_cc", "tld_has_digit", "ratio_nonalnum_host",
             "host_n_scripts", "host_mixed_script", "host_confusable_chars", "brand_lookalike_reg", "brand_lookalike_host", "host_digit_in_word", "reg_log_rank"]
B64 = re.compile(r"[A-Za-z0-9+/_=-]{16,}")
SCRIPT_EXT, DOC_EXT, IMG_EXT, ARCH_EXT = {"php", "asp", "aspx", "jsp", "cgi", "pl"}, {"html", "htm", "shtml", "xhtml"}, {"jpg", "jpeg", "png", "gif", "svg", "ico", "webp", "css", "js"}, {"zip", "rar", "exe", "apk", "7z"}
PART_COLS = ["len", "alpha_rate", "digit_rate", "upper_rate", "hyphens", "underscores", "dots", "ent", "ent_norm", "hex16", "uuid", "b64", "pct", "has_at", "domainlike", "rep",
             "legibility", "typo", "leet", "vowel_ratio", "consonant_run", "ext_script", "ext_doc", "ext_img", "ext_arch", "sw_phrase", "sw_kit", "brand_in", "is_val"]


def part_row(t, kind):
    n = max(len(t), 1)
    dec = lexical.decode(t).lower()
    L = _lists()
    ext = t.rsplit(".", 1)[-1].lower() if "." in t else ""
    leg, typo = readability.spelling(t)
    toks = lexical._TOKEN.findall(dec)
    return {"len": len(t), "alpha_rate": sum(c.isalpha() for c in t) / n, "digit_rate": sum(c.isdigit() for c in t) / n, "upper_rate": sum(c.isupper() for c in t) / n,
            "hyphens": t.count("-"), "underscores": t.count("_"), "dots": t.count("."), "ent": lexical.entropy(t), "ent_norm": lexical.norm_entropy(t),
            "hex16": float(bool(HEX.search(t))), "uuid": float(bool(UUID.search(t))),
            "b64": float(any(any(c.isdigit() for c in m) and any(c.isupper() for c in m) and any(c.islower() for c in m) for m in B64.findall(t))),
            "pct": len(PCT.findall(t)), "has_at": float("@" in t), "domainlike": float(bool(DOMAINLIKE.search(dec))), "rep": float(bool(REP.search(t))),
            "legibility": leg, "typo": typo, "leet": readability.leet(t), "vowel_ratio": readability.vowel_ratio(t), "consonant_run": readability.consonant_run(t),
            "ext_script": float(ext in SCRIPT_EXT), "ext_doc": float(ext in DOC_EXT), "ext_img": float(ext in IMG_EXT), "ext_arch": float(ext in ARCH_EXT),
            "sw_phrase": len(set(L.sub_rx["phrase"].findall(dec))) if L.sub_rx["phrase"] else 0, "sw_kit": len(set(toks) & L.kit), "brand_in": len({x for x in toks if x in L.brands}),
            "is_val": float(kind == "qval")}


def url_parts(url):
    """list of (kind, text) for one URL, kind in seg / qkey / qval; [] when the grammar rejects the URL"""
    s = structure(url)
    if s is None:
        return None
    return [("seg", x) for x in s["segs"]] + [("qkey", x) for x in s["qkeys"]] + [("qval", x) for x in s["qvals"]]


def tables(urls):
    """(H, parts): H = host-level feature frame, one row per URL (rows the grammar rejects = NaN); parts = long frame (row, kind, + PART_COLS), no row for a URL without parts."""
    import pandas as pd
    urls = list(urls)
    H = featurize(urls)[HOST_COLS]
    rows = []
    for i, u in enumerate(urls):
        for kind, t in (url_parts(u) or []):
            rows.append({"row": i, "kind": kind, **part_row(t, kind)})
    return H, pd.DataFrame(rows, columns=["row", "kind"] + PART_COLS)
