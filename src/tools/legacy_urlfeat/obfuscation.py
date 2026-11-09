"""Features suggested by the research papers: special-character ratios (hybrid CNN/Transformer paper, Table 1) and
homoglyph / look-alike detection (same paper: text models "neglect homoglyph attacks unless specifically targeted")."""
import unicodedata

from .lexical import DELIMS, OTHER

# characters that imitate ASCII letters; applied to the host before comparing it with the brand list
CONFUSABLE = {"0": "o", "1": "l", "3": "e", "4": "a", "5": "s", "7": "t", "8": "b", "$": "s", "!": "i", "|": "l",
              "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "х": "x", "у": "y", "і": "i", "ѕ": "s", "ԁ": "d", "ɡ": "g", "ο": "o", "α": "a"}


def deconfuse(text):
    out = "".join(CONFUSABLE.get(c, c) for c in text.lower())
    return out.replace("vv", "w").replace("rn", "m")


def n_scripts(text):
    """Number of distinct Unicode scripts among the letters (first word of the character name: LATIN, CYRILLIC, GREEK...)."""
    return len({unicodedata.name(c, "?").split()[0] for c in text if c.isalpha()})


def obfuscation(url, s, brands):
    """s: structure() row; brands: set of brand labels (lexical.Lists.brands)."""
    host, reg = s["host"], s["reg"]
    n = max(len(url), 1)
    f = {"ratio_delims_url": sum(c in DELIMS for c in url) / n, "ratio_other_url": sum(c in OTHER for c in url) / n,
         "ratio_nonalnum_url": sum(not c.isalnum() for c in url) / n, "ratio_nonalnum_host": sum(not c.isalnum() for c in host) / max(len(host), 1),
         "ratio_hyphen_url": url.count("-") / n, "ratio_dot_url": url.count(".") / n}
    tokens = [t for lab in host.split(".") for t in lab.replace("_", "-").split("-") if t]
    fixed = {deconfuse(t) for t in tokens}
    raw = set(tokens)
    f["host_n_scripts"] = n_scripts(host)
    f["host_mixed_script"] = float(f["host_n_scripts"] > 1)
    f["host_confusable_chars"] = sum(c in CONFUSABLE for c in host.lower() if not c.isdigit())
    # a brand appears only after mapping look-alike characters (paypa1, g00gle, rnicrosoft, cyrillic a/o)
    f["brand_lookalike_reg"] = float(deconfuse(reg.split(".")[0]) in brands and reg.split(".")[0] not in brands)
    f["brand_lookalike_host"] = float(len((fixed & brands) - raw) > 0)
    f["host_digit_in_word"] = float(any(any(c.isdigit() for c in t) and any(c.isalpha() for c in t) for t in tokens))
    return f
