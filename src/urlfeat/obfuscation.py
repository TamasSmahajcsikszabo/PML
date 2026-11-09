"""Features suggested by the research papers: special-character ratios (hybrid CNN/Transformer paper, Table 1) and
homoglyph / look-alike detection (same paper: text models "neglect homoglyph attacks unless specifically targeted")."""
import unicodedata


# characters that imitate ASCII letters; applied to the host before comparing it with the brand list
CONFUSABLE = {"0": "o", "1": "l", "3": "e", "4": "a", "5": "s", "7": "t", "8": "b", "$": "s", "!": "i", "|": "l",
              "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "х": "x", "у": "y", "і": "i", "ѕ": "s", "ԁ": "d", "ɡ": "g", "ο": "o", "α": "a"}


def deconfuse(text):
    out = "".join(CONFUSABLE.get(c, c) for c in text.lower())
    return out.replace("vv", "w").replace("rn", "m")


def n_scripts(text):
    """Number of distinct Unicode scripts among the letters (first word of the character name: LATIN, CYRILLIC, GREEK...)."""
    return len({unicodedata.name(c, "?").split()[0] for c in text if c.isalpha()})
