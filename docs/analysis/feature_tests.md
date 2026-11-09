# Feature tests on 1000 random URLs (seed 2)

140 of 141 feature columns have a reference (20 of them `wiring`: a helper called on the right text); 140 pass on every URL, 0 fail on at least one.

Not covered by the random generator: shortener_in_url


Part features (segment / key / value / host label), 1500 random strings: 29 of 29 columns pass on every string.

Targeted cases:
* ok   sfx_platform for a hosting platform suffix (blogspot.com), tenant is the registrable label
* ok   punycode labels counted
* ok   is_shortener for bit.ly
* ok   www_extra_label counts www2
* ok   host_mixed_script for a Cyrillic letter in a Latin host
* ok   host_ipv4 and no registrable label
* ok   unknown host falls to host_other
* ok   shortener_in_url: a shortener domain inside a query value
* ok   hlabel rows: non-www sub-domains + registrable (row 3: www skipped, www2 + example = 2)
* ok   is_tld_label (grammar lexer) equals the old lists (tlds.txt minus exts.txt) on every listed label
* ok   is_tld_label rejects non-TLDs
