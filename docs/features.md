# Predictors (141), run 20261104T1518_nine-models

Importance = drop in validation ROC AUC when the feature is shuffled (permutation importance, mean of 5 folds), taken for each of the nine models; **mean ± std across the nine models**, and the mean rank among all features (1 = most important). L = log1p-transformed. All features are computed from the URL exactly as given.

## 1 Scheme and host (ANTLR grammar)

| name | definition | importance (mean ± std) | mean rank |
|---|---|---|---|
| `www` | 1 if the first host label is www | 0.0163 ± 0.0112 | 8 |
| `https` | 1 if the URL starts with https:// | 0.0119 ± 0.0076 | 10 |
| `host_len` | host length (L) | 0.0044 ± 0.0050 | 31 |
| `n_sub` | number of subdomains (L) | 0.0013 ± 0.0018 | 58 |
| `sfx_icann2` | 1 if the suffix has two labels (co.uk, com.br) | 0.0012 ± 0.0010 | 46 |
| `sfx_platform` | 1 if the suffix is a hosting platform (tenant.workers.dev, blogspot.com...) | 0.0011 ± 0.0028 | 88 |
| `reg_len` | registrable-label length (L) | 0.0011 ± 0.0013 | 65 |
| `host_ipv4` | 1 if the host is an IPv4 address | 0.0008 ± 0.0020 | 91 |
| `reg_digits` | digits in the registrable label (L) | 0.0005 ± 0.0009 | 81 |
| `port` | 1 if an explicit port is given | 0.0004 ± 0.0006 | 71 |
| `host_other` | 1 if the host has an unknown suffix (localhost, odd TLD) | 0.0002 ± 0.0002 | 85 |
| `reg_hyphens` | hyphens in the registrable label (L) | 0.0002 ± 0.0003 | 90 |
| `punycode` | count of punycode (xn--) host labels | 0.0001 ± 0.0001 | 93 |
| `sfx_platform_bare` | 1 if the host is exactly a platform with no tenant | 0.0000 ± 0.0001 | 112 |
| `host_platform` | 1 if the host is a bare hosting platform (e.g. s3.amazonaws.com, no tenant) | 0.0000 ± 0.0001 | 112 |
| `ftp` | 1 if the scheme is ftp | 0.0000 ± 0.0000 | 115 |
| `userinfo` | 1 if the URL has user@ before the host | 0.0000 ± 0.0000 | 115 |

## 2 Path, query, fragment (ANTLR grammar)

| name | definition | importance (mean ± std) | mean rank |
|---|---|---|---|
| `n_seg` | number of path segments (L) | 0.0194 ± 0.0323 | 34 |
| `max_seg_len` | longest path segment (L) | 0.0088 ± 0.0126 | 34 |
| `url_len` | URL length in characters (L) | 0.0054 ± 0.0085 | 34 |
| `has_path` | 1 if there is a path beyond the host | 0.0037 ± 0.0062 | 69 |
| `n_amp_esc` | count of HTML-escaped &amp; separators | 0.0022 ± 0.0034 | 48 |
| `has_query` | 1 if there is a query string | 0.0019 ± 0.0031 | 75 |
| `trailing_slash` | 1 if the path ends with / | 0.0013 ± 0.0012 | 45 |
| `path_len` | path length (L) | 0.0012 ± 0.0012 | 59 |
| `query_len` | query length (L) | 0.0006 ± 0.0009 | 69 |
| `n_email` | count of e-mail addresses in path/query/fragment | 0.0006 ± 0.0017 | 89 |
| `n_empty_val` | query pairs with an empty value (L) | 0.0006 ± 0.0010 | 75 |
| `n_nested` | count of URLs embedded in the query | 0.0004 ± 0.0010 | 94 |
| `n_empty_seg` | empty path segments, e.g. // (L) | 0.0003 ± 0.0004 | 76 |
| `pct_total` | count of %XX escapes | 0.0002 ± 0.0002 | 76 |
| `has_ext` | 1 if the last segment ends in a known file extension | 0.0002 ± 0.0004 | 82 |
| `n_pairs` | number of query key/value pairs (L) | 0.0001 ± 0.0002 | 100 |
| `has_frag` | 1 if there is a #fragment | 0.0001 ± 0.0003 | 107 |
| `frag_len` | fragment length (L) | 0.0001 ± 0.0003 | 110 |
| `stray_pct` | count of invalid % signs | 0.0000 ± 0.0000 | 106 |

## 3 Text values (grammar pieces + regex)

| name | definition | importance (mean ± std) | mean rank |
|---|---|---|---|
| `host_digit_rate` | share of digits in the host | 0.0064 ± 0.0055 | 22 |
| `n_dash_host` | hyphens in the host (L) | 0.0053 ± 0.0079 | 29 |
| `longest_digit_run` | longest run of consecutive digits (L) | 0.0021 ± 0.0030 | 45 |
| `emb_domain` | 1 if a host name with a known TLD is embedded in path/query/fragment | 0.0021 ± 0.0037 | 46 |
| `mean_seg_len` | mean path-segment length | 0.0018 ± 0.0018 | 39 |
| `emb_hex` | 1 if a 16+ hex string or a UUID is embedded | 0.0016 ± 0.0034 | 64 |
| `n_dash_url` | hyphens in the URL (L) | 0.0016 ± 0.0024 | 62 |
| `n_at` | @ signs in the URL (L) | 0.0016 ± 0.0020 | 46 |
| `url_digit_rate` | share of digits in the URL | 0.0010 ± 0.0006 | 42 |
| `path_digit_rate` | share of digits in the path | 0.0008 ± 0.0013 | 66 |
| `rep_char_host` | 1 if a character repeats 3+ times in a host label (www ignored) | 0.0007 ± 0.0015 | 89 |
| `max_label_len` | longest host label (L) | 0.0007 ± 0.0006 | 57 |
| `n_dots_host` | dots in the host (L) | 0.0006 ± 0.0008 | 70 |
| `max_qval_len` | longest query value (L) | 0.0005 ± 0.0006 | 65 |
| `mean_qval_len` | mean query-value length | 0.0005 ± 0.0010 | 72 |
| `n_underscore` | underscores in the URL (L) | 0.0004 ± 0.0006 | 68 |
| `rep_char_query` | 1 if a character repeats 3+ times in a query piece | 0.0004 ± 0.0007 | 92 |
| `rep_char_path` | 1 if a character repeats 3+ times in a path segment | 0.0003 ± 0.0003 | 84 |
| `max_qkey_len` | longest query key (L) | 0.0002 ± 0.0003 | 78 |
| `query_digit_rate` | share of digits in the query | 0.0001 ± 0.0003 | 83 |
| `rep_digit` | 1 if a digit repeats 3+ times anywhere | 0.0001 ± 0.0003 | 98 |
| `emb_ip` | 1 if an IPv4 address is embedded in path/query/fragment or host | 0.0000 ± 0.0000 | 104 |
| `non_ascii` | 1 if any non-ASCII character | 0.0000 ± 0.0001 | 108 |
| `emb_port` | 1 if host:port is embedded | 0.0000 ± 0.0000 | 115 |

## 4 Entropy (lexical)

| name | definition | importance (mean ± std) | mean rank |
|---|---|---|---|
| `ent_path` | entropy of the path | 0.0117 ± 0.0227 | 55 |
| `ent_url` | Shannon entropy of the URL (bits/char) | 0.0112 ± 0.0214 | 52 |
| `ent_url_norm` | URL entropy / log2(length) | 0.0029 ± 0.0051 | 63 |
| `ent_path_norm` | path entropy / log2(length) | 0.0015 ± 0.0020 | 61 |
| `ent_max_seg` | highest entropy of any path segment | 0.0010 ± 0.0012 | 53 |
| `ent_reg` | entropy of the registrable label (domain hosts only) | 0.0004 ± 0.0004 | 73 |
| `ent_max_qval` | highest entropy of any query value | 0.0004 ± 0.0003 | 60 |

## 5 Special characters (lexical)

| name | definition | importance (mean ± std) | mean rank |
|---|---|---|---|
| `sc_other_query` | count of + $ = & . : # % (paper F4 set; L) in the query | 0.0020 ± 0.0036 | 78 |
| `sc_delims_query` | count of the characters ~`!^*()[]{}"';:,><| (paper F3 set; L) in the query | 0.0017 ± 0.0034 | 66 |
| `sc_delims_url` | count of the characters ~`!^*()[]{}"';:,><| (paper F3 set; L) in the url | 0.0015 ± 0.0020 | 60 |
| `sc_other_url` | count of + $ = & . : # % (paper F4 set; L) in the url | 0.0012 ± 0.0021 | 64 |
| `sc_other_host` | count of + $ = & . : # % (paper F4 set; L) in the host | 0.0006 ± 0.0008 | 80 |
| `sc_other_path` | count of + $ = & . : # % (paper F4 set; L) in the path | 0.0004 ± 0.0005 | 73 |
| `sc_delims_host` | count of the characters ~`!^*()[]{}"';:,><| (paper F3 set; L) in the host | 0.0004 ± 0.0006 | 84 |
| `sc_delims_path` | count of the characters ~`!^*()[]{}"';:,><| (paper F3 set; L) in the path | -0.0000 ± 0.0002 | 114 |

## 6 Suspicious words (lexical)

| name | definition | importance (mean ± std) | mean rank |
|---|---|---|---|
| `sw_phrase_url` | distinct phishing phrases (login, secure, verify, account, ...; L) in the url | 0.0117 ± 0.0087 | 9 |
| `sw_brand_url` | distinct brand words from the paper list in the URL (L) | 0.0049 ± 0.0053 | 29 |
| `sw_kit_path` | distinct CMS/kit words as whole tokens in the path only (L) | 0.0046 ± 0.0044 | 21 |
| `sw_kit_url` | distinct CMS/kit words (wp, content, includes, themes, admin...) as whole tokens in the URL (L) | 0.0040 ± 0.0033 | 20 |
| `sw_phrase_path` | distinct phishing phrases (login, secure, verify, account, ...; L) in the path | 0.0019 ± 0.0039 | 54 |
| `sw_host_url` | distinct free-hosting words (webhostapp...) in the URL (L) | 0.0017 ± 0.0017 | 52 |
| `sw_phrase_query` | distinct phishing phrases (login, secure, verify, account, ...; L) in the query | 0.0016 ± 0.0045 | 82 |
| `sw_phrase_host` | distinct phishing phrases (login, secure, verify, account, ...; L) in the host | 0.0015 ± 0.0038 | 69 |

## 7 Brand rules (lexical, Tranco top-500 brands)

| name | definition | importance (mean ± std) | mean rank |
|---|---|---|---|
| `brand_in_path` | distinct brands in the path (L) | 0.0029 ± 0.0031 | 25 |
| `reg_popular` | 1 if the registrable domain is in the Tranco top 50,000 | 0.0019 ± 0.0023 | 59 |
| `brand_in_sub` | distinct brand names in subdomains (L) | 0.0014 ± 0.0025 | 53 |
| `brand_in_reg` | brand + extra characters in the registrable label | 0.0006 ± 0.0010 | 67 |
| `brand_in_query` | distinct brands in the query (L) | 0.0002 ± 0.0005 | 99 |
| `brand_typo` | registrable label one edit from a brand (typosquat) | 0.0000 ± 0.0001 | 112 |
| `brand_wrong_tld` | brand label on a different suffix (paypal.tk) | -0.0002 ± 0.0006 | 105 |

## 8 Shorteners and misc URL counts (lexical)

| name | definition | importance (mean ± std) | mean rank |
|---|---|---|---|
| `n_hyphens_path` | hyphens in the path (L) | 0.0066 ± 0.0088 | 21 |
| `n_eq_url` | count of = (L) | 0.0030 ± 0.0045 | 53 |
| `is_shortener` | 1 if the host is a URL shortener | 0.0015 ± 0.0012 | 37 |
| `n_dots_path` | dots in the path (L) | 0.0013 ± 0.0011 | 44 |
| `http_after_host` | occurrences of 'http' after the host (L) | 0.0009 ± 0.0017 | 69 |
| `www_after_host` | occurrences of 'www' after the host (L) | 0.0008 ± 0.0023 | 97 |
| `n_amp_url` | count of & (L) | 0.0007 ± 0.0009 | 73 |
| `amp_gt_eq` | 1 if there are more & than = (paper F2) | 0.0006 ± 0.0010 | 82 |
| `www_extra_label` | host labels after the first that start with www (L) | 0.0001 ± 0.0001 | 102 |
| `shortener_in_url` | 1 if a shortener domain appears inside the URL | 0.0000 ± 0.0001 | 105 |

## 9 Readability (from the other repo; English dictionary)

| name | definition | importance (mean ± std) | mean rank |
|---|---|---|---|
| `url_legibility` | share of URL letters covered by dictionary words | 0.0103 ± 0.0069 | 11 |
| `url_leet` | share of characters that are digits next to letters (g00gle) | 0.0061 ± 0.0048 | 18 |
| `tld_suspicious` | 1 if the TLD is on the abused list (tk, ml, xyz, top...) | 0.0045 ± 0.0044 | 18 |
| `seg_max_leet` | highest leet share of any path segment | 0.0019 ± 0.0012 | 30 |
| `host_leet` | share of host characters that are digits next to letters | 0.0017 ± 0.0029 | 62 |
| `seg_consonant_run` | longest consonant run in any path segment | 0.0013 ± 0.0010 | 46 |
| `tld_cc` | 1 if the TLD is a 2-letter country code | 0.0012 ± 0.0013 | 47 |
| `host_legibility` | share of host letters covered by dictionary words | 0.0010 ± 0.0006 | 44 |
| `sld_legibility` | share of registrable-label letters covered by dictionary words | 0.0008 ± 0.0010 | 65 |
| `seg_min_legibility` | lowest legibility of any path segment | 0.0005 ± 0.0004 | 59 |
| `sld_leet` | share of registrable-label characters that are digits next to letters | 0.0003 ± 0.0004 | 88 |
| `qval_min_legibility` | lowest legibility of any query value | 0.0002 ± 0.0004 | 81 |
| `seg_max_typo` | highest typo rate of any path segment | 0.0002 ± 0.0003 | 81 |
| `sld_consonant_run` | longest consonant run in the registrable label | 0.0001 ± 0.0001 | 95 |
| `url_typo_rate` | share of URL letters in unreadable runs within one edit of a word | 0.0001 ± 0.0001 | 104 |
| `sld_vowel_ratio` | vowel share of registrable-label letters | 0.0000 ± 0.0001 | 108 |
| `host_typo_rate` | share of host letters in unreadable runs within one edit of a word | 0.0000 ± 0.0002 | 112 |
| `sld_typo_rate` | share of registrable-label letters in unreadable runs within one edit of a word | 0.0000 ± 0.0001 | 112 |
| `tld_has_digit` | 1 if the TLD contains a digit | 0.0000 ± 0.0000 | 111 |
| `qval_max_typo` | highest typo rate of any query value | 0.0000 ± 0.0001 | 104 |
| `ext_php` | 1 if the file extension is .php | 0.0000 ± 0.0000 | 115 |
| `ext_html` | 1 if the file extension is .html | 0.0000 ± 0.0000 | 115 |
| `ext_htm` | 1 if the file extension is .htm | 0.0000 ± 0.0000 | 115 |
| `ext_asp` | 1 if the file extension is .asp | 0.0000 ± 0.0000 | 115 |
| `ext_aspx` | 1 if the file extension is .aspx | 0.0000 ± 0.0000 | 115 |
| `ext_jsp` | 1 if the file extension is .jsp | 0.0000 ± 0.0000 | 115 |
| `ext_exe` | 1 if the file extension is .exe | 0.0000 ± 0.0000 | 115 |
| `ext_zip` | 1 if the file extension is .zip | 0.0000 ± 0.0000 | 115 |

## 10 Obfuscation (research papers)

| name | definition | importance (mean ± std) | mean rank |
|---|---|---|---|
| `ratio_delims_url` | F3-set characters / URL length | 0.0179 ± 0.0230 | 17 |
| `ratio_nonalnum_url` | non-alphanumeric characters / URL length | 0.0155 ± 0.0163 | 13 |
| `ratio_dot_url` | dots / URL length | 0.0126 ± 0.0184 | 38 |
| `ratio_hyphen_url` | hyphens / URL length | 0.0024 ± 0.0032 | 39 |
| `host_digit_in_word` | 1 if a host token mixes letters and digits | 0.0017 ± 0.0025 | 67 |
| `ratio_nonalnum_host` | non-alphanumeric characters / host length | 0.0014 ± 0.0019 | 59 |
| `ratio_other_url` | F4-set characters / URL length | 0.0008 ± 0.0010 | 62 |
| `host_n_scripts` | number of Unicode scripts among host letters | 0.0008 ± 0.0020 | 87 |
| `brand_lookalike_host` | a host token equals a brand only after that mapping | 0.0000 ± 0.0000 | 104 |
| `brand_lookalike_reg` | registrable label equals a brand only after mapping look-alikes (0->o, rn->m, Cyrillic a) | 0.0000 ± 0.0000 | 110 |
| `host_mixed_script` | 1 if the host mixes scripts (Latin + Cyrillic...) | 0.0000 ± 0.0000 | 115 |
| `host_confusable_chars` | look-alike non-Latin characters in the host | 0.0000 ± 0.0000 | 115 |

## 11 Popularity

| name | definition | importance (mean ± std) | mean rank |
|---|---|---|---|
| `reg_log_rank` | log10 of the registrable domain's Tranco rank (top 500k; 6 if absent) | 0.0480 ± 0.0471 | 6 |

