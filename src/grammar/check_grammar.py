"""Assertions for the grammar and the visitor (run after every grammar, list or visitor change):

    PYTHONPATH=src .venv/bin/python src/grammar/check_grammar.py

Every lexer / parser edge case that once went wrong gets an assertion here."""
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1]))
from urlfeat import extract, wordlists as W  # noqa: E402
from urlfeat.visitor import COLUMNS  # noqa: E402
from urlfeat import structure  # noqa: E402

n = 0


def check(cond, msg):
    global n
    n += 1
    assert cond, msg


s = structure("http://user:pw@www.sub.example.co.uk:8080/a/b.php?x=1&y=2#frag")
check(s["host_kind"] == "domain" and s["reg"] == "example" and s["suffix"] == "co.uk" and s["suffix_kind"] == "icann2", "co.uk is a two-level suffix, example the registrable label")
check(s["subdomains"] == ["www", "sub"] and s["port"] == "8080" and s["userinfo"], "subdomains, port, userinfo")
check(s["segs"] == ["a", "b.php"] and s["qkeys"] == ["x", "y"] and s["qvals"] == ["1", "2"] and s["fragment"] == "frag", "segments, query pairs, fragment")
check(structure("example.com/x")["scheme"] == "", "a URL without a scheme is parsed as given")
check(structure("http://192.168.0.1/x")["host_kind"] == "ipv4", "IPv4 host")
check(structure("https://evil.workers.dev/")["suffix_kind"] == "platform" and structure("https://evil.workers.dev/")["reg"] == "evil", "platform suffix: the tenant is the registrable label")
check(structure("http://localhost/")["host_kind"] == "other", "unknown host falls to otherHost")
check(structure("http://a.com/p?u=http://b.com/x")["nested"] == 1, "a nested URL in a query value is one NESTED_URL token")
check(structure("http://a.com/logo@2x.png")["email"] == 0, "logo@2x.png is not an e-mail (PATH_AT_WORD)")
check(structure("http://a.com/%41%zz")["pct"] == 1 and structure("http://a.com/%41%zz")["stray_pct"] == 1, "valid and stray percent escapes")
check(structure("http://xn--e1afmkfd.xn--p1ai/")["punycode"] >= 1, "punycode labels")
check(structure("http://a.com/?a=1&amp;b=2")["amp_esc"] == 1, "&amp; separates pairs")

pw = W.load()
check(pw.words["phrase"].find_all("my-login-secure") == ["login", "secure"], "phrase words found as substrings")
check(W.TOKENS.find_all("ab-c1_d") == ["ab", "c1", "d"], "alphanumeric tokens")
check(pw.brand_long.find_all("xpaypalx") == ["paypal"], "long brand as a substring")

X, H, P = extract(["http://www.a.com/x/y?k=v", "http://b.org"])
check(list(X.columns) == COLUMNS and len(X.columns) == 141, "141 columns, fixed order")
check(len(P[P.row == 0]) == 4 and len(P[P.row == 1]) == 0, "parts: 2 segments + 1 key + 1 value; none for a URL without parts")
check(extract(["http://" + "a" * 100])[0].notna().all(axis=None), "long host label parses")
print(f"{n} assertions passed")
