"""URL -> numeric features: B (url_grammar) structure + text values + lexical, plus A (phishing_url_predictions) readability."""
import functools

import numpy as np
import pandas as pd

from . import lexical, obfuscation, popularity, readability
from .structure import structure

_FLAGS = {"https": ("scheme", "https"), "ftp": ("scheme", "ftp"), "host_ipv4": ("host_kind", "ipv4"),
          "host_platform": ("host_kind", "platform"), "host_other": ("host_kind", "other"),
          "sfx_platform": ("suffix_kind", "platform"), "sfx_platform_bare": ("suffix_kind", "platform_bare"),
          "sfx_icann2": ("suffix_kind", "icann2"), "has_ext": ("ext", None)}
_LOG1P = ["n_sub", "n_seg", "n_empty_seg", "n_pairs", "n_empty_val", "url_len", "host_len", "reg_len", "reg_hyphens",
          "reg_digits", "max_seg_len", "query_len", "frag_len", "max_label_len", "mean_seg_len", "max_qkey_len",
          "max_qval_len", "mean_qval_len", "longest_digit_run", "n_dash_host", "n_dash_url", "n_dots_host",
          "n_underscore", "n_at"]
_BINARY = ["userinfo", "www", "punycode", "has_query", "n_amp_esc", "n_nested", "n_email", "has_frag", "pct_total",
           "stray_pct", "rep_char_host", "rep_char_path", "rep_char_query", "rep_digit", "emb_ip", "emb_domain",
           "emb_hex", "emb_port", "non_ascii"]
_LEX_LOG1P = ("sc_", "sw_", "n_amp_url", "n_eq_url", "n_dots_path", "n_hyphens_path", "http_after_host",
              "www_after_host", "brand_in_sub", "brand_in_path", "brand_in_query", "www_extra_label")


@functools.cache
def _lists():
    return lexical.load_lists(500, 50000)


def _row(url):
    try:
        return _row_unsafe(url)
    except Exception:  # a pathological string must never stop a 7.8M-URL job: its features stay missing (read as 'invalid')
        return {}


def _row_unsafe(url):
    u = url = str(url)  # parsed and measured exactly as given: nothing is stripped, prefixed or normalised
    s = structure(url)
    if s is None:  # grammar rejected the string: leave every feature missing (xgboost handles NaN)
        return {}
    f = {}
    for k, (col, val) in _FLAGS.items():
        f[k] = float(s[col] == val) if val is not None else float(s[col] != "")
    nz = s["n_seg"] > 0
    f["port"] = float(s["port"] != "")
    f["has_path"] = float(nz)
    f["trailing_slash"] = float(s["trailing_slash"] > 0 and nz)
    f["path_len"] = np.log1p(s["path_len"] if nz else 0)
    for k in _BINARY:
        f[k] = float(s[k] > 0)
    for k in _LOG1P:
        f[k] = np.log1p(s[k])
    for k in ("mean_seg_len", "mean_qval_len", "host_digit_rate", "path_digit_rate", "query_digit_rate", "url_digit_rate"):
        f[k] = float(s[k])
    lex = lexical.url_features(url, s["host"], s["reg"], s["suffix"], s["host_kind"], _lists())
    for k in lexical.COLUMNS:
        f[k] = np.log1p(lex[k]) if k.startswith(_LEX_LOG1P) else float(lex[k])
    f.update(readability.readability(u, s, s["segs"], s["qvals"]))
    f.update(obfuscation.obfuscation(u, s, _lists().brands))
    f.update(popularity.popularity(s))
    return f


def featurize(urls):
    """DataFrame, one row per URL, fixed column order (rows the grammar rejects are all-NaN)."""
    df = pd.DataFrame([_row(u) for u in urls])
    return df.reindex(columns=COLUMNS).astype(float)


def _columns():
    df = pd.DataFrame([_row("https://www.example.com/a/b.html?x=1&y=2")])
    return list(df.columns)


COLUMNS = _columns()
