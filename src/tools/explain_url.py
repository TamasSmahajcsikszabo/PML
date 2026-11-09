"""Break URLs down by the grammar and the rules applied after the parse.

    PYTHONPATH=src .venv/bin/python -m tools.explain_url [--n 25] [--seed 1] [--special 5] [--url URL ...] [--out docs/analysis/url_breakdown.md]

For every URL: (1) lexer tokens in their modes, (2) the parse tree (single-child chains collapsed), (3) the visitor rules that ran after the parse (host kind, platform lookup on the
parsed labels, suffix kind), (4) the resulting components and the host-level feature values. URLs come from data/train.csv as supplied (full, unaltered)."""
import argparse

import pandas as pd

import urlfeat
from antlr4 import CommonTokenStream, InputStream
from antlr4.tree.Tree import TerminalNode
from common import DATA
from urlfeat import structure
from urlfeat.visitor import UrlLexer, UrlParser

HOST_SHOW = ["host_platform", "sfx_platform", "sfx_platform_bare", "sfx_icann2", "n_sub", "www", "reg_len", "reg_popular", "reg_log_rank", "host_len"]


def tokens(url):
    lx = UrlLexer(InputStream(url))
    lx.removeErrorListeners()
    return [f"{lx.symbolicNames[t.type]}:{t.text!r}" for t in lx.getAllTokens()]


def tree_str(node, parser, cap=300):
    def rec(n):
        if isinstance(n, TerminalNode):
            return f"{parser.symbolicNames[n.symbol.type]}:{n.getText()!r}"
        name = parser.ruleNames[n.getRuleIndex()]
        kids = [c for c in n.getChildren() if not (isinstance(c, TerminalNode) and c.symbol.type == -1)]  # drop EOF
        if len(kids) == 1 and not isinstance(kids[0], TerminalNode):
            return name + ">" + rec(kids[0])
        return name + "(" + " ".join(rec(c) for c in kids) + ")"
    s = rec(node)
    return s if len(s) <= cap else s[:cap] + " ..."


def platform_rule(s, plats):
    """re-run the visitor's platform lookup on the parsed labels, to show what it did"""
    labels = s["subdomains"] + [s["reg"]] + s["suffix"].split(".") if s["suffix_kind"] not in ("platform", "platform_bare") else None
    if s["host_kind"] != "domain" and s["suffix_kind"] != "platform_bare":
        return f"host kind {s['host_kind']}: no platform lookup"
    if s["suffix_kind"] == "platform_bare":
        return f"the whole host '{s['host'].rstrip('.')}' is a listed platform -> bare platform (registrable = suffix = host)"
    if s["suffix_kind"] == "platform":
        return f"suffix '{s['suffix']}' is a listed platform (whole labels) -> tenant '{s['reg']}' is the registrable, sub-domains {s['subdomains']}"
    return f"no run of whole end labels of {labels} is a listed platform -> ordinary public suffix '{s['suffix']}' ({s['suffix_kind']})"


def explain(url, plats, X):
    lx = UrlLexer(InputStream(url))
    lx.removeErrorListeners()
    p = UrlParser(CommonTokenStream(lx))
    p.removeErrorListeners()
    tree = p.url()
    s = structure(url)
    out = [f"URL: {url}", f"  tokens : {' '.join(tokens(url))}", f"  parse  : {tree_str(tree, p)}"]
    if s is None:
        out.append("  rejected by the grammar -> no features")
        return "\n".join(out)
    out.append(f"  rule   : {platform_rule(s, plats)}")
    out.append(f"  parts  : scheme={s['scheme']!r} host={s['host']!r} subdomains={s['subdomains']} registrable={s['reg']!r} suffix={s['suffix']!r} ({s['suffix_kind']}) port={s['port']!r}")
    out.append(f"           path={s['path']!r} segments={s['segs']} query keys={s['qkeys']} values={s['qvals']} fragment={s['fragment']!r}")
    out.append("  host features: " + ", ".join(f"{c}={X[c]:.3g}" for c in HOST_SHOW))
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=25)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--special", type=int, default=5, help="how many of the n are platform hosts / hosts the old platform tokens cut wrongly")
    ap.add_argument("--url", nargs="*", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    from urlfeat import wordlists
    plats = wordlists.load().platforms
    if a.url:
        urls = a.url
    else:
        train = pd.read_csv(DATA / "train.csv")
        allu = train.url.tolist()
        rng = train.sample(frac=1, random_state=a.seed).url.tolist()
        marks = ("blogspot.com", "workers.dev", "github.io", "cloud.google.com", "com.secureupdate", "appspot.com", "herokuapp.com")
        special = [u for u in rng if any(m in u for m in marks)][:a.special]
        urls = special + [u for u in rng if u not in special][:a.n - len(special)]
    X = urlfeat.featurize(urls)
    txt = "\n\n".join(explain(u, plats, X.iloc[i]) for i, u in enumerate(urls))
    print(txt)
    if a.out:
        open(a.out, "w", encoding="utf-8").write("# URL breakdown (grammar + applied rules)\n\n```\n" + txt + "\n```\n")


if __name__ == "__main__":
    main()
