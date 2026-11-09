"""Predictor table: group, name, definition, importance.  PYTHONPATH=src .venv/bin/python src/tools/feature_table.py [RUN_ID] [--out docs/features.md] [--csv docs/features.csv] [--sep ";"] [--report]

Importance = permutation importance (drop in validation ROC AUC when the feature is shuffled, mean of 5 folds) of every one of the nine models in the run;
the table gives its mean and standard deviation ACROSS the nine models, and the mean rank (1 = most important of 141). L = value is log1p-transformed."""
import argparse
import json

import pandas as pd

from common import ROOT, run_dir

G = {}  # group -> {name: definition}


def grp(name, **defs):
    G[name] = defs


T = lambda f, what: {f"{f}_{c}": f"{what} in the {c}" for c in ("url", "host", "path", "query")}
grp("1 Scheme and host (ANTLR grammar)", https="1 if the URL starts with https://", ftp="1 if the scheme is ftp", host_ipv4="1 if the host is an IPv4 address",
    host_platform="1 if the host is a bare hosting platform (e.g. s3.amazonaws.com, no tenant)", host_other="1 if the host has an unknown suffix (localhost, odd TLD)",
    userinfo="1 if the URL has user@ before the host", port="1 if an explicit port is given", sfx_platform="1 if the suffix is a hosting platform (tenant.workers.dev, blogspot.com...)",
    sfx_platform_bare="1 if the host is exactly a platform with no tenant", sfx_icann2="1 if the suffix has two labels (co.uk, com.br)", www="1 if the first host label is www",
    punycode="count of punycode (xn--) host labels", n_sub="number of subdomains (L)", host_len="host length (L)", reg_len="registrable-label length (L)",
    reg_hyphens="hyphens in the registrable label (L)", reg_digits="digits in the registrable label (L)")
grp("2 Path, query, fragment (ANTLR grammar)", url_len="URL length in characters (L)", has_path="1 if there is a path beyond the host", trailing_slash="1 if the path ends with /",
    n_seg="number of path segments (L)", n_empty_seg="empty path segments, e.g. // (L)", max_seg_len="longest path segment (L)", path_len="path length (L)",
    has_ext="1 if the last segment ends in a known file extension", has_query="1 if there is a query string", n_amp_esc="count of HTML-escaped &amp; separators",
    n_pairs="number of query key/value pairs (L)", n_empty_val="query pairs with an empty value (L)", query_len="query length (L)", n_nested="count of URLs embedded in the query",
    n_email="count of e-mail addresses in path/query/fragment", has_frag="1 if there is a #fragment", frag_len="fragment length (L)", pct_total="count of %XX escapes",
    stray_pct="count of invalid % signs")
grp("3 Text values (grammar pieces + scanners in text.py)", max_label_len="longest host label (L)", mean_seg_len="mean path-segment length", max_qkey_len="longest query key (L)",
    max_qval_len="longest query value (L)", mean_qval_len="mean query-value length", host_digit_rate="share of digits in the host", path_digit_rate="share of digits in the path",
    query_digit_rate="share of digits in the query", url_digit_rate="share of digits in the URL", longest_digit_run="longest run of consecutive digits (L)",
    rep_char_host="1 if a character repeats 3+ times in a host label (www ignored)", rep_char_path="1 if a character repeats 3+ times in a path segment",
    rep_char_query="1 if a character repeats 3+ times in a query piece", rep_digit="1 if a digit repeats 3+ times anywhere", emb_ip="1 if an IPv4 address is embedded in path/query/fragment or host",
    emb_domain="1 if a host name with a known TLD is embedded in path/query/fragment", emb_hex="1 if a 16+ hex string or a UUID is embedded", emb_port="1 if host:port is embedded",
    n_dash_host="hyphens in the host (L)", n_dash_url="hyphens in the URL (L)", n_dots_host="dots in the host (L)", n_underscore="underscores in the URL (L)", n_at="@ signs in the URL (L)",
    non_ascii="1 if any non-ASCII character")
grp("4 Entropy (lexical)", ent_url="Shannon entropy of the URL (bits/char)", ent_path="entropy of the path", ent_url_norm="URL entropy / log2(length)", ent_path_norm="path entropy / log2(length)",
    ent_reg="entropy of the registrable label (domain hosts only)", ent_max_seg="highest entropy of any path segment", ent_max_qval="highest entropy of any query value")
grp("5 Special characters (lexical)", **{**T("sc_delims", "count of the characters ~`!^*()[]{}\"';:,><| (paper F3 set; L)"), **T("sc_other", "count of + $ = & . : # % (paper F4 set; L)")})
grp("6 Suspicious words (lexical)", **T("sw_phrase", "distinct phishing phrases (login, secure, verify, account, ...; L)") | {
    "sw_brand_url": "distinct brand words from the paper list in the URL (L)", "sw_host_url": "distinct free-hosting words (webhostapp...) in the URL (L)",
    "sw_kit_url": "distinct CMS/kit words (wp, content, includes, themes, admin...) as whole tokens in the URL (L)", "sw_kit_path": "distinct CMS/kit words as whole tokens in the path only (L)"})
grp("7 Brand rules (lexical, Tranco top-500 brands)", brand_in_sub="distinct brand names in subdomains (L)", brand_in_reg="brand + extra characters in the registrable label",
    brand_wrong_tld="brand label on a different suffix (paypal.tk)", brand_typo="registrable label one edit from a brand (typosquat)", brand_in_path="distinct brands in the path (L)",
    brand_in_query="distinct brands in the query (L)", reg_popular="1 if the registrable domain is in the Tranco top 50,000")
grp("8 Shorteners and misc URL counts (lexical)", is_shortener="1 if the host is a URL shortener", shortener_in_url="1 if a shortener domain appears inside the URL",
    n_amp_url="count of & (L)", n_eq_url="count of = (L)", amp_gt_eq="1 if there are more & than = (paper F2)", n_dots_path="dots in the path (L)", n_hyphens_path="hyphens in the path (L)",
    http_after_host="occurrences of 'http' after the host (L)", www_after_host="occurrences of 'www' after the host (L)", www_extra_label="host labels after the first that start with www (L)")
grp("9 Readability (from the other repo; English dictionary)", url_legibility="share of URL letters covered by dictionary words", host_legibility="share of host letters covered by dictionary words", sld_legibility="share of registrable-label letters covered by dictionary words",
    url_typo_rate="share of URL letters in unreadable runs within one edit of a word", host_typo_rate="share of host letters in unreadable runs within one edit of a word", sld_typo_rate="share of registrable-label letters in unreadable runs within one edit of a word",
    url_leet="share of characters that are digits next to letters (g00gle)", host_leet="share of host characters that are digits next to letters", sld_leet="share of registrable-label characters that are digits next to letters", sld_vowel_ratio="vowel share of registrable-label letters",
    sld_consonant_run="longest consonant run in the registrable label", seg_min_legibility="lowest legibility of any path segment", seg_max_typo="highest typo rate of any path segment",
    qval_min_legibility="lowest legibility of any query value", qval_max_typo="highest typo rate of any query value", seg_max_leet="highest leet share of any path segment",
    seg_consonant_run="longest consonant run in any path segment", tld_suspicious="1 if the TLD is on the abused list (tk, ml, xyz, top...)", tld_cc="1 if the TLD is a 2-letter country code",
    tld_has_digit="1 if the TLD contains a digit", **{f"ext_{e}": f"1 if the file extension is .{e}" for e in ("php", "html", "htm", "asp", "aspx", "jsp", "exe", "zip")})
grp("10 Obfuscation (research papers)", ratio_delims_url="F3-set characters / URL length", ratio_other_url="F4-set characters / URL length", ratio_nonalnum_url="non-alphanumeric characters / URL length",
    ratio_nonalnum_host="non-alphanumeric characters / host length", ratio_hyphen_url="hyphens / URL length", ratio_dot_url="dots / URL length",
    host_n_scripts="number of Unicode scripts among host letters", host_mixed_script="1 if the host mixes scripts (Latin + Cyrillic...)", host_confusable_chars="look-alike non-Latin characters in the host",
    brand_lookalike_reg="registrable label equals a brand only after mapping look-alikes (0->o, rn->m, Cyrillic a)", brand_lookalike_host="a host token equals a brand only after that mapping",
    host_digit_in_word="1 if a host token mixes letters and digits")
grp("11 Popularity", reg_log_rank="log10 of the registrable domain's Tranco rank (top 500k; 6 if absent)")


def select_features(run_id=None, keep=0.5):
    """Keep the more important `keep` share of the features inside every group. Importance = mean permutation importance over the nine models of the given run
    (ties: lower mean rank). Returns a DataFrame group, name, importance, rank_in_group, kept; a group of n features keeps ceil(keep * n)."""
    import math
    fi = pd.read_csv(run_dir(run_id) / "feature_importance.csv")
    st = fi.groupby("feature").agg(importance=("permutation_auc_drop", "mean"), rank=("rank", "mean"))
    rows = []
    for g, m in G.items():
        d = st.loc[list(m)].sort_values(["importance", "rank"], ascending=[False, True])
        for i, (n, r) in enumerate(d.iterrows(), 1):
            rows.append({"group": g, "name": n, "importance": r.importance, "rank_in_group": i, "kept": i <= math.ceil(keep * len(m))})
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run", nargs="?", default=None)
    ap.add_argument("--out", default=str(ROOT / "docs" / "features.md"))
    ap.add_argument("--csv", default=str(ROOT / "docs" / "features.csv"))
    ap.add_argument("--sep", default=";", help="field separator of the csv (default: semicolon; fields that contain it are quoted)")
    ap.add_argument("--report", action="store_true", help="also put a compact table into Report.md as an appendix (off: the report has no appendix)")
    a = ap.parse_args()
    d = run_dir(a.run)
    src = d if (d / "feature_importance.csv").exists() else run_dir(json.loads((d / "config.json").read_text())["parent"])  # a parts run keeps the importances in its parent run
    fi = pd.read_csv(src / "feature_importance.csv")
    st = fi.groupby("feature").agg(mean=("permutation_auc_drop", "mean"), std=("permutation_auc_drop", "std"), rank=("rank", "mean"))
    defs = {n: (g, t) for g, m in G.items() for n, t in m.items()}
    missing = set(st.index) - set(defs)
    assert not missing, missing  # every feature of the run needs a definition (features dropped by the correlation filter are simply not listed)
    rows = [{"group": defs[n][0], "name": n, "definition": defs[n][1], "log1p": any(t in defs[n][1] for t in ("(L)", "; L)")), "importance_mean": st.loc[n, "mean"], "importance_std": st.loc[n, "std"],
             "mean_rank": st.loc[n, "rank"]} for n in st.index]
    pd.DataFrame(rows).sort_values(["group", "importance_mean"], ascending=[True, False]).to_csv(a.csv, index=False, sep=a.sep, float_format="%.6g")
    lines = [f"# Predictors ({len(st)}), run {src.name}", "",
             "Importance = drop in validation ROC AUC when the feature is shuffled (permutation importance, mean of 5 folds), taken for each of the nine models; **mean ± std across the nine models**, "
             "and the mean rank among all features (1 = most important). L = log1p-transformed. All features are computed from the URL exactly as given.", ""]
    for g, m in G.items():
        m = {n: v for n, v in m.items() if n in st.index}
        if not m:
            continue
        lines += [f"## {g}", "", "| name | definition | importance (mean ± std) | mean rank |", "|---|---|---|---|"]
        for n in sorted(m, key=lambda n: -st.loc[n, "mean"]):
            lines.append(f"| `{n}` | {m[n]} | {st.loc[n, 'mean']:.4f} ± {st.loc[n, 'std']:.4f} | {st.loc[n, 'rank']:.0f} |")
        lines.append("")
    import pathlib
    pathlib.Path(a.out).write_text("\n".join(lines) + "\n")
    if a.report:  # (re)place the table between markers in Report.md; first time: appended as the Appendix
        import re
        cells = []
        for g, m in G.items():
            m = sorted((n for n in m if n in st.index), key=lambda n: -st.loc[n, "mean"])
            if m:
                cells.append(f"| {re.sub(r' [(].*$', '', re.sub(r'^[0-9]+ ', '', g))} | " + ", ".join(f"`{n}` {st.loc[n, 'mean']:.3f}" for n in m) + " |")
        block = (f"<!-- predictors:start -->\n## Appendix: predictors\n\nThe {len(st)} predictors kept by the correlation filter, by group, with their permutation importance (drop in validation AUC when shuffled, mean over the nine models); "
                 "definitions in `docs/features.md`.\n\n| group | predictors (importance) |\n|---|---|\n" + "\n".join(cells) + "\n<!-- predictors:end -->\n")
        rp = ROOT / "Report.md"
        txt = rp.read_text()
        if "<!-- predictors:start -->" in txt:
            txt = txt[:txt.index("<!-- predictors:start -->")] + block + txt[txt.index("<!-- predictors:end -->") + len("<!-- predictors:end -->\n"):]
        else:
            txt = txt.rstrip("\n") + "\n\n" + block
        rp.write_text(txt)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
