# Predictors (88), run v2_20261109T0949_corr-filter-0.75

Importance = drop in validation ROC AUC when the feature is shuffled (permutation importance, mean of 5 folds), taken for each of the nine models; **mean ± std across the nine models**, and the mean rank among all features (1 = most important). L = log1p-transformed. All features are computed from the URL exactly as given.

## 1 Scheme and host (ANTLR grammar)

| name | definition | importance (mean ± std) | mean rank |
|---|---|---|---|
| `www` | 1 if the first host label is www | 0.0345 ± 0.0231 | 4 |
| `sfx_platform` | 1 if the suffix is a hosting platform (tenant.workers.dev, blogspot.com...) | 0.0029 ± 0.0071 | 53 |
| `host_len` | host length (L) | 0.0028 ± 0.0015 | 19 |
| `n_sub` | number of subdomains (L) | 0.0020 ± 0.0033 | 38 |
| `reg_digits` | digits in the registrable label (L) | 0.0013 ± 0.0024 | 48 |
| `sfx_icann2` | 1 if the suffix has two labels (co.uk, com.br) | 0.0010 ± 0.0009 | 34 |
| `https` | 1 if the URL starts with https:// | 0.0002 ± 0.0011 | 72 |
| `reg_hyphens` | hyphens in the registrable label (L) | 0.0001 ± 0.0001 | 55 |
| `port` | 1 if an explicit port is given | 0.0001 ± 0.0001 | 65 |
| `punycode` | count of punycode (xn--) host labels | 0.0000 ± 0.0001 | 69 |

## 2 Path, query, fragment (ANTLR grammar)

| name | definition | importance (mean ± std) | mean rank |
|---|---|---|---|
| `n_seg` | number of path segments (L) | 0.0085 ± 0.0097 | 19 |
| `query_len` | query length (L) | 0.0026 ± 0.0040 | 25 |
| `trailing_slash` | 1 if the path ends with / | 0.0019 ± 0.0017 | 30 |
| `n_empty_val` | query pairs with an empty value (L) | 0.0006 ± 0.0009 | 55 |
| `pct_total` | count of %XX escapes | 0.0004 ± 0.0003 | 46 |
| `n_empty_seg` | empty path segments, e.g. // (L) | 0.0001 ± 0.0001 | 62 |
| `stray_pct` | count of invalid % signs | 0.0000 ± 0.0000 | 67 |
| `has_frag` | 1 if there is a #fragment | -0.0001 ± 0.0004 | 76 |

## 3 Text values (grammar pieces + scanners in text.py)

| name | definition | importance (mean ± std) | mean rank |
|---|---|---|---|
| `host_digit_rate` | share of digits in the host | 0.0054 ± 0.0031 | 12 |
| `n_at` | @ signs in the URL (L) | 0.0034 ± 0.0044 | 28 |
| `emb_hex` | 1 if a 16+ hex string or a UUID is embedded | 0.0030 ± 0.0081 | 47 |
| `emb_domain` | 1 if a host name with a known TLD is embedded in path/query/fragment | 0.0022 ± 0.0031 | 31 |
| `n_dash_host` | hyphens in the host (L) | 0.0020 ± 0.0017 | 25 |
| `longest_digit_run` | longest run of consecutive digits (L) | 0.0016 ± 0.0024 | 33 |
| `rep_char_query` | 1 if a character repeats 3+ times in a query piece | 0.0012 ± 0.0035 | 56 |
| `n_underscore` | underscores in the URL (L) | 0.0012 ± 0.0010 | 33 |
| `rep_char_host` | 1 if a character repeats 3+ times in a host label (www ignored) | 0.0005 ± 0.0010 | 52 |
| `rep_char_path` | 1 if a character repeats 3+ times in a path segment | 0.0004 ± 0.0009 | 60 |
| `rep_digit` | 1 if a digit repeats 3+ times anywhere | 0.0002 ± 0.0007 | 63 |
| `non_ascii` | 1 if any non-ASCII character | 0.0001 ± 0.0001 | 63 |
| `emb_ip` | 1 if an IPv4 address is embedded in path/query/fragment or host | 0.0001 ± 0.0001 | 65 |

## 4 Entropy (lexical)

| name | definition | importance (mean ± std) | mean rank |
|---|---|---|---|
| `ent_path_norm` | path entropy / log2(length) | 0.0065 ± 0.0060 | 16 |
| `ent_url` | Shannon entropy of the URL (bits/char) | 0.0055 ± 0.0045 | 16 |
| `ent_max_seg` | highest entropy of any path segment | 0.0053 ± 0.0039 | 19 |
| `ent_reg` | entropy of the registrable label (domain hosts only) | 0.0012 ± 0.0008 | 35 |
| `ent_url_norm` | URL entropy / log2(length) | 0.0003 ± 0.0006 | 54 |

## 5 Special characters (lexical)

| name | definition | importance (mean ± std) | mean rank |
|---|---|---|---|
| `sc_other_url` | count of + $ = & . : # % (paper F4 set; L) in the url | 0.0021 ± 0.0041 | 37 |
| `sc_delims_query` | count of the characters ~`!^*()[]{}"';:,><| (paper F3 set; L) in the query | 0.0015 ± 0.0034 | 50 |
| `sc_other_path` | count of + $ = & . : # % (paper F4 set; L) in the path | 0.0009 ± 0.0011 | 41 |
| `sc_delims_url` | count of the characters ~`!^*()[]{}"';:,><| (paper F3 set; L) in the url | 0.0009 ± 0.0020 | 52 |
| `sc_other_host` | count of + $ = & . : # % (paper F4 set; L) in the host | 0.0007 ± 0.0012 | 48 |
| `sc_delims_path` | count of the characters ~`!^*()[]{}"';:,><| (paper F3 set; L) in the path | -0.0001 ± 0.0005 | 73 |

## 6 Suspicious words (lexical)

| name | definition | importance (mean ± std) | mean rank |
|---|---|---|---|
| `sw_kit_path` | distinct CMS/kit words as whole tokens in the path only (L) | 0.0127 ± 0.0092 | 5 |
| `sw_phrase_url` | distinct phishing phrases (login, secure, verify, account, ...; L) in the url | 0.0056 ± 0.0038 | 13 |
| `sw_phrase_host` | distinct phishing phrases (login, secure, verify, account, ...; L) in the host | 0.0034 ± 0.0073 | 39 |
| `sw_brand_url` | distinct brand words from the paper list in the URL (L) | 0.0025 ± 0.0033 | 30 |
| `sw_phrase_path` | distinct phishing phrases (login, secure, verify, account, ...; L) in the path | 0.0021 ± 0.0026 | 31 |
| `sw_phrase_query` | distinct phishing phrases (login, secure, verify, account, ...; L) in the query | 0.0016 ± 0.0037 | 54 |
| `sw_host_url` | distinct free-hosting words (webhostapp...) in the URL (L) | 0.0010 ± 0.0010 | 41 |

## 7 Brand rules (lexical, Tranco top-500 brands)

| name | definition | importance (mean ± std) | mean rank |
|---|---|---|---|
| `brand_in_sub` | distinct brand names in subdomains (L) | 0.0026 ± 0.0033 | 28 |
| `brand_in_path` | distinct brands in the path (L) | 0.0020 ± 0.0021 | 28 |
| `brand_in_reg` | brand + extra characters in the registrable label | 0.0004 ± 0.0004 | 48 |
| `brand_in_query` | distinct brands in the query (L) | 0.0001 ± 0.0002 | 65 |
| `brand_wrong_tld` | brand label on a different suffix (paypal.tk) | -0.0000 ± 0.0000 | 73 |
| `brand_typo` | registrable label one edit from a brand (typosquat) | -0.0000 ± 0.0000 | 73 |

## 8 Shorteners and misc URL counts (lexical)

| name | definition | importance (mean ± std) | mean rank |
|---|---|---|---|
| `n_hyphens_path` | hyphens in the path (L) | 0.0118 ± 0.0059 | 7 |
| `is_shortener` | 1 if the host is a URL shortener | 0.0027 ± 0.0021 | 23 |
| `n_amp_url` | count of & (L) | 0.0013 ± 0.0031 | 55 |
| `amp_gt_eq` | 1 if there are more & than = (paper F2) | 0.0008 ± 0.0010 | 49 |
| `http_after_host` | occurrences of 'http' after the host (L) | 0.0004 ± 0.0009 | 64 |
| `www_after_host` | occurrences of 'www' after the host (L) | 0.0002 ± 0.0005 | 64 |
| `www_extra_label` | host labels after the first that start with www (L) | 0.0001 ± 0.0002 | 64 |
| `shortener_in_url` | 1 if a shortener domain appears inside the URL | -0.0000 ± 0.0000 | 70 |

## 9 Readability (from the other repo; English dictionary)

| name | definition | importance (mean ± std) | mean rank |
|---|---|---|---|
| `url_legibility` | share of URL letters covered by dictionary words | 0.0132 ± 0.0083 | 7 |
| `url_leet` | share of characters that are digits next to letters (g00gle) | 0.0097 ± 0.0084 | 11 |
| `ext_php` | 1 if the file extension is .php | 0.0052 ± 0.0052 | 20 |
| `tld_suspicious` | 1 if the TLD is on the abused list (tk, ml, xyz, top...) | 0.0037 ± 0.0041 | 21 |
| `seg_min_legibility` | lowest legibility of any path segment | 0.0021 ± 0.0029 | 37 |
| `seg_max_leet` | highest leet share of any path segment | 0.0015 ± 0.0021 | 35 |
| `ext_html` | 1 if the file extension is .html | 0.0009 ± 0.0012 | 42 |
| `host_legibility` | share of host letters covered by dictionary words | 0.0009 ± 0.0012 | 48 |
| `seg_max_typo` | highest typo rate of any path segment | 0.0004 ± 0.0010 | 56 |
| `tld_cc` | 1 if the TLD is a 2-letter country code | 0.0004 ± 0.0005 | 48 |
| `ext_htm` | 1 if the file extension is .htm | 0.0003 ± 0.0004 | 54 |
| `url_typo_rate` | share of URL letters in unreadable runs within one edit of a word | 0.0003 ± 0.0006 | 55 |
| `ext_asp` | 1 if the file extension is .asp | 0.0003 ± 0.0006 | 62 |
| `sld_vowel_ratio` | vowel share of registrable-label letters | 0.0002 ± 0.0004 | 61 |
| `qval_max_typo` | highest typo rate of any query value | 0.0002 ± 0.0004 | 65 |
| `host_typo_rate` | share of host letters in unreadable runs within one edit of a word | 0.0002 ± 0.0005 | 64 |
| `ext_aspx` | 1 if the file extension is .aspx | 0.0000 ± 0.0001 | 69 |
| `ext_jsp` | 1 if the file extension is .jsp | 0.0000 ± 0.0001 | 70 |
| `sld_consonant_run` | longest consonant run in the registrable label | -0.0000 ± 0.0001 | 71 |

## 10 Obfuscation (research papers)

| name | definition | importance (mean ± std) | mean rank |
|---|---|---|---|
| `ratio_nonalnum_url` | non-alphanumeric characters / URL length | 0.0023 ± 0.0011 | 23 |
| `host_n_scripts` | number of Unicode scripts among host letters | 0.0008 ± 0.0018 | 55 |
| `ratio_nonalnum_host` | non-alphanumeric characters / host length | 0.0007 ± 0.0006 | 38 |
| `ratio_dot_url` | dots / URL length | 0.0004 ± 0.0004 | 51 |
| `brand_lookalike_host` | a host token equals a brand only after that mapping | -0.0000 ± 0.0000 | 70 |

## 11 Popularity

| name | definition | importance (mean ± std) | mean rank |
|---|---|---|---|
| `reg_log_rank` | log10 of the registrable domain's Tranco rank (top 500k; 6 if absent) | 0.0439 ± 0.0392 | 6 |

