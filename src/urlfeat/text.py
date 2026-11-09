"""Plain string helpers for the visit methods. No regular expressions anywhere in urlfeat: every pattern the old code matched with `re` is an explicit scanner here
(percent escapes, repeated characters, embedded IPv4 / host names / host:port, hex / UUID / base64-like runs, alphanumeric tokens, dotted names).
Each scanner documents the pattern it replaces; the rules follow the old regexes (left-most match, greedy, non-overlapping)."""
import math

DIGITS = frozenset("0123456789")
HEX = frozenset("0123456789abcdefABCDEF")
ALNUM = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
LABEL = ALNUM | {"-"}  # [a-z0-9-] (case-insensitive)
B64 = ALNUM | frozenset("+/_=-")
TOKEN = frozenset("abcdefghijklmnopqrstuvwxyz0123456789")  # [a-z0-9] on already lower-cased text


# ---------------------------------------------------------------- percent escapes   (%[0-9a-fA-F]{2})
def decode_pct(x):
    """%XX -> the ASCII character; escapes of code points >= 128 stay escaped."""
    out, i, n = [], 0, len(x)
    while i < n:
        if x[i] == "%" and i + 2 < n and x[i + 1] in HEX and x[i + 2] in HEX:
            v = int(x[i + 1:i + 3], 16)
            out.append(chr(v) if v < 128 else x[i:i + 3])
            i += 3
        else:
            out.append(x[i])
            i += 1
    return "".join(out)


def strip_pct(x):
    """x without its %XX escapes"""
    out, i, n = [], 0, len(x)
    while i < n:
        if x[i] == "%" and i + 2 < n and x[i + 1] in HEX and x[i + 2] in HEX:
            i += 3
        else:
            out.append(x[i])
            i += 1
    return "".join(out)


def count_pct(x):
    n = i = 0
    while i < len(x):
        if x[i] == "%" and i + 2 < len(x) and x[i + 1] in HEX and x[i + 2] in HEX:
            n += 1
            i += 3
        else:
            i += 1
    return n


# ---------------------------------------------------------------- numbers and repetition
def digit_rate(x):
    c = strip_pct(x)
    return sum("0" <= ch <= "9" for ch in c) / len(c) if c else 0.0


def longest_digit_run(x):
    best = cur = 0
    for ch in x:
        cur = cur + 1 if "0" <= ch <= "9" else 0
        best = max(best, cur)
    return best


def has_repeat(x, digits_only=False):
    """a character (case-insensitive) or, with digits_only, a digit repeated 3 or more times in a row   ((.)\\1{2,}  /  ([0-9])\\1{2,})"""
    run, prev = 0, None
    for ch in x:
        c = ch.lower()
        if c == prev and (not digits_only or "0" <= ch <= "9"):
            run += 1
            if run >= 3:
                return True
        else:
            prev, run = c, 1
    return False


def any_repeat(pieces, digits_only=False, skip_www=False):
    return any(has_repeat(strip_pct(p), digits_only) for p in pieces if not (skip_www and p.lower() == "www"))


def entropy(s):
    n = len(s)
    if n < 2:
        return 0.0
    c = {}
    for ch in s:
        c[ch] = c.get(ch, 0) + 1
    return -sum(v / n * math.log2(v / n) for v in c.values())


def norm_entropy(s):
    n = len(s)
    return entropy(s) / math.log2(n) if n >= 2 else 0.0


def count_in(s, chars):
    return sum(1 for ch in s if ch in chars)


# ---------------------------------------------------------------- tokens and dotted names
def alnum_tokens(s):
    """maximal runs of [a-z0-9] in lower-cased text   ([a-z0-9]+)"""
    out, i, n = [], 0, len(s)
    while i < n:
        if s[i] in TOKEN:
            j = i + 1
            while j < n and s[j] in TOKEN:
                j += 1
            out.append(s[i:j])
            i = j
        else:
            i += 1
    return out


def dotted_names(s):
    """names of two or more labels [a-z0-9-]+ joined by single dots, left-most, greedy, non-overlapping   ([a-z0-9-]+(?:\\.[a-z0-9-]+)+)"""
    out, i, n = [], 0, len(s)
    while i < n:
        if s[i] in LABEL:
            j = i + 1
            while j < n and s[j] in LABEL:
                j += 1
            e, groups = j, 0
            while e + 1 < n and s[e] == "." and s[e + 1] in LABEL:
                k = e + 2
                while k < n and s[k] in LABEL:
                    k += 1
                e, groups = k, groups + 1
            if groups:
                out.append(s[i:e])
            i = e
        else:
            i += 1
    return out


def domain_like(s):
    """host-like names: labels start with [a-z0-9], are not preceded or followed by a label character, at least two labels
    ((?<![a-z0-9-])[a-z0-9][a-z0-9-]*(?:\\.[a-z0-9][a-z0-9-]*)+(?![a-z0-9-]), case-insensitive)"""
    out, i, n = [], 0, len(s)
    while i < n:
        if s[i] in ALNUM and (i == 0 or s[i - 1] not in LABEL):
            j = i + 1
            while j < n and s[j] in LABEL:
                j += 1
            e, groups = j, 0
            while e + 1 < n and s[e] == "." and s[e + 1] in ALNUM:
                k = e + 2
                while k < n and s[k] in LABEL:
                    k += 1
                e, groups = k, groups + 1
            if groups:
                out.append(s[i:e])
                i = e
            else:
                i = j
        else:
            i += 1
    return out


# ---------------------------------------------------------------- IPv4   ((?<![0-9])(octet\.){3}octet(?![0-9]) with octet = 25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])
def _octet_lengths(s, i):
    n = len(s)
    c = s[i] if i < n else ""
    out = []
    if c == "2" and i + 2 < n and s[i + 1] == "5" and s[i + 2] in "012345":
        out.append(3)
    if c == "2" and i + 2 < n and s[i + 1] in "01234" and s[i + 2] in DIGITS:
        out.append(3)
    if c == "1" and i + 2 < n and s[i + 1] in DIGITS and s[i + 2] in DIGITS:
        out.append(3)
    if c != "" and c in "123456789" and i + 1 < n and s[i + 1] in DIGITS:
        out.append(2)
    if c != "" and c in DIGITS:
        out.append(1)
    return out


def _ipv4_from(s, i, full):
    n = len(s)

    def rec(pos, k):
        for length in _octet_lengths(s, pos):
            end = pos + length
            if k == 3:
                if (end == n) if full else (end >= n or s[end] not in DIGITS):
                    return True
            elif end < n and s[end] == "." and rec(end + 1, k + 1):
                return True
        return False
    return rec(i, 0)


def has_ipv4(s):
    return any(s[i] in DIGITS and (i == 0 or s[i - 1] not in DIGITS) and _ipv4_from(s, i, False) for i in range(len(s)))


def is_ipv4(s):
    return bool(s) and _ipv4_from(s, 0, True)


# ---------------------------------------------------------------- hex, uuid, base64-like
def hex_runs(s, min_len=16):
    """maximal runs of hexadecimal digits of at least min_len   ([0-9a-f]{16,})"""
    out, i, n = [], 0, len(s)
    while i < n:
        if s[i] in HEX:
            j = i + 1
            while j < n and s[j] in HEX:
                j += 1
            if j - i >= min_len:
                out.append(s[i:j])
            i = j
        else:
            i += 1
    return out


_UUID = (8, 4, 4, 4, 12)


def has_uuid(s):
    """8-4-4-4-12 hexadecimal digits separated by hyphens, anywhere"""
    for i in range(len(s) - 35):
        pos, ok = i, True
        for k, length in enumerate(_UUID):
            if k:
                if s[pos] != "-":
                    ok = False
                    break
                pos += 1
            seg = s[pos:pos + length]
            if len(seg) != length or any(c not in HEX for c in seg):
                ok = False
                break
            pos += length
        if ok:
            return True
    return False


def base64_runs(s, min_len=16):
    """maximal runs of [A-Za-z0-9+/_=-] of at least min_len"""
    out, i, n = [], 0, len(s)
    while i < n:
        if s[i] in B64:
            j = i + 1
            while j < n and s[j] in B64:
                j += 1
            if j - i >= min_len:
                out.append(s[i:j])
            i = j
        else:
            i += 1
    return out


# ---------------------------------------------------------------- host:port   (((?:[a-z0-9-]+\.)+[a-z0-9-]+|localhost):([0-9]{2,5})(?![0-9]), case-insensitive)
def host_ports(s):
    """(host text, port) of every `name:digits` with a dotted name or `localhost` before a colon and 2-5 digits after it"""
    out, n, lo = [], len(s), 0
    i = 0
    while i < n:
        if s[i] not in LABEL and s[i] != ".":
            i += 1
            continue
        j = i
        while j < n and (s[j] in LABEL or s[j] == "."):
            j += 1
        run_start = max(i, lo)
        i = j
        if j >= n or s[j] != ":" or run_start >= j:
            continue
        d = j + 1
        while d < n and s[d] in DIGITS:
            d += 1
        if not 2 <= d - (j + 1) <= 5:
            continue
        run = s[run_start:j]
        parts = run.split(".")
        k = len(parts)
        while k > 0 and parts[k - 1] != "":
            k -= 1
        block = parts[k:]  # trailing non-empty labels
        host = None
        if len(block) >= 2:
            host = ".".join(block)
        else:
            tail = run[-9:]
            if len(run) >= 9 and tail.lower() == "localhost":
                host = tail
        if host is not None:
            out.append((host, int(s[j + 1:d])))
            lo = d
            i = d
    return out
