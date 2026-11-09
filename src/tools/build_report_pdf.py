"""Build Report.pdf from Report.md (pandoc + xelatex). The mermaid block is drawn with matplotlib from the same edge list (no browser or mermaid-cli needed).

    PYTHONPATH=src .venv/bin/python -m tools.build_report_pdf [--md Report.md] [--out Report.pdf]

Prints the number of pages (the report must stay within two to three pages)."""
import argparse
import pathlib
import re
import subprocess
import tempfile
import textwrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

from common import ROOT  # noqa: E402

NODE = re.compile(r'^\s*([A-Za-z0-9_]+)(?:\[\"?(.*?)\"?\]|\(\"?(.*?)\"?\))?\s*$')


def parse_mermaid(src):
    labels, edges, order = {}, [], []
    for line in src.splitlines():
        if line.strip().startswith(("flowchart", "graph")) or not line.strip():
            continue
        ids = []
        for tok in line.split("-->"):
            m = NODE.match(tok.strip())
            if not m:
                raise ValueError(f"cannot read mermaid node: {tok!r}")
            nid, lab = m.group(1), m.group(2) or m.group(3)
            if lab:
                labels[nid] = lab.replace("<br/>", "\n")
            labels.setdefault(nid, nid)
            if nid not in order:
                order.append(nid)
            ids.append(nid)
        edges += list(zip(ids, ids[1:]))
    return labels, edges, order


def draw(src, path_pdf, path_png):
    labels, edges, order = parse_mermaid(src)
    rank = {n: 0 for n in order}
    for _ in order:  # longest-path ranks
        for a, b in edges:
            rank[b] = max(rank[b], rank[a] + 1)
    cols = {}
    for n in order:
        cols.setdefault(rank[n], []).append(n)
    nr, nrow = max(rank.values()) + 1, max(len(v) for v in cols.values())
    W, H = 7.0, 0.62 * nrow + 0.5
    fig, ax = plt.subplots(figsize=(W, H))
    ax.set_xlim(0, nr)
    ax.set_ylim(0, nrow)
    ax.axis("off")
    pos = {}
    preds = {n: [a for a, b in edges if b == n] for n in order}
    for r in sorted(cols):
        ns = cols[r]
        for i, n in enumerate(ns):
            y = nrow - 0.5 - i - (nrow - len(ns)) / 2
            if len(ns) == 1 and len(preds[n]) == 1:  # a single box that follows one box stays on its line
                y = pos[preds[n][0]][1]
            pos[n] = (r + 0.5, y)
    bw, bh = 0.88, 0.8
    for n, (x, y) in pos.items():
        ax.add_patch(FancyBboxPatch((x - bw / 2, y - bh / 2), bw, bh, boxstyle="round,pad=0.01,rounding_size=0.06", fc="#eef2f7", ec="#33485c", lw=0.7))
        txt = "\n".join(textwrap.fill(p, 11) for p in labels[n].split("\n"))
        ax.text(x, y, txt, ha="center", va="center", fontsize=5.4, color="#111")
    for a, b in edges:
        (x0, y0), (x1, y1) = pos[a], pos[b]
        ax.annotate("", xy=(x1 - bw / 2, y1), xytext=(x0 + bw / 2, y0), arrowprops=dict(arrowstyle="-|>", lw=0.7, color="#33485c", shrinkA=0, shrinkB=0, connectionstyle="arc3,rad=0"))
    fig.savefig(path_pdf, bbox_inches="tight", pad_inches=0.02)
    fig.savefig(path_png, bbox_inches="tight", pad_inches=0.02, dpi=200)
    plt.close(fig)


HEADER = r"""
\usepackage{etoolbox}
\usepackage{graphicx}
\AtBeginEnvironment{longtable}{\footnotesize}
\usepackage{booktabs}
\renewcommand{\arraystretch}{1.12}
\setlength{\parskip}{0.35em}
\setlength{\parindent}{0pt}
\usepackage{titlesec}
\titlespacing*{\section}{0pt}{0.9em}{0.3em}
\titlespacing*{\subsection}{0pt}{0.6em}{0.2em}
\usepackage{fancyhdr}
\pagestyle{fancy}\fancyhf{}\fancyfoot[C]{\footnotesize\thepage}\renewcommand{\headrulewidth}{0pt}
"""


def build(md_path, out_pdf):
    md = pathlib.Path(md_path).read_text(encoding="utf-8")
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="report_pdf_"))
    m = re.search(r"```mermaid\n(.*?)```", md, re.S)
    if m:
        draw(m.group(1), tmp / "pipeline.pdf", tmp / "pipeline.png")
        md = md.replace(m.group(0), "```{=latex}\n\\begin{center}\\includegraphics[width=\\linewidth,height=0.22\\textheight,keepaspectratio]{" + str(tmp / "pipeline.pdf") + "}\\end{center}\n```\n")  # not a float: stays under its sentence, never wider than the text
    md = md.replace("<!-- predictors:start -->", "").replace("<!-- predictors:end -->", "")
    md = md.replace("| group | predictors (importance) |\n|---|---|", "| group | predictors (importance) |\n|-------|----------------------------------------|")
    (tmp / "header.tex").write_text(HEADER)
    (tmp / "in.md").write_text(md, encoding="utf-8")
    cmd = ["pandoc", str(tmp / "in.md"), "-f", "markdown+pipe_tables+tex_math_dollars-implicit_figures+implicit_figures", "-o", str(out_pdf), "--pdf-engine=xelatex", "-H", str(tmp / "header.tex"),
           "-V", "geometry:margin=1.7cm", "-V", "fontsize=10pt", "-V", "colorlinks=true", "-V", "linkcolor=black", "-V", "urlcolor=black", "-V", "mainfont=Latin Modern Roman",
           "-V", "monofont=Latin Modern Mono", "-V", "monofontoptions=Scale=0.92", "--wrap=preserve"]
    subprocess.run(cmd, check=True)
    return tmp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", default=str(ROOT / "Report.md"))
    ap.add_argument("--out", default=str(ROOT / "Report.pdf"))
    a = ap.parse_args()
    build(a.md, a.out)
    from pypdf import PdfReader
    r = PdfReader(a.out)
    print(f"{a.out}: {len(r.pages)} pages")


if __name__ == "__main__":
    main()
