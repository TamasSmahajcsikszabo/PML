"""Graded popularity of the registrable domain: log10 of its rank in the Tranco top 500,000 (list in lists/tranco_top500k.txt.gz, rank = line number);
domains outside the list get log10(1,000,000) = 6. Replaces the earlier yes/no "in the top 50,000" flag as a graded signal (the flag stays for the brand rules)."""
import functools
import gzip
import math
import pathlib

LIST = pathlib.Path(__file__).resolve().parents[2] / "lists" / "tranco_top500k.txt.gz"
ABSENT = math.log10(1_000_000)


@functools.cache
def _ranks():
    with gzip.open(LIST, "rt", encoding="utf-8") as f:
        return {d.strip(): i for i, d in enumerate(f, 1)}


def popularity(s):
    """s: structure() row."""
    rs = f"{s['reg']}.{s['suffix']}" if s["reg"] and s["suffix"] else s["host"]
    rank = _ranks().get(rs.lower())
    return {"reg_log_rank": math.log10(rank) if rank else ABSENT}
