"""URL -> numeric features. The single entry point is `visitor.URLVisitor`: one ANTLR parse and one visit per URL builds the 141 columns of `COLUMNS`, the host frame and the rows of the
path segments / query keys / query values (/ host labels). Module-level shortcuts use one shared visitor:
    featurize(urls)   DataFrame, one row per URL, columns COLUMNS (rows the grammar rejects are all NaN)
    extract(urls)     (features, host frame, part rows) from the same single pass over the URLs; with_parts=False skips the part rows; host_labels=True adds the hlabel columns
    tables(urls)      (host frame, part rows) for the parts model
    structure(url)    the parsed parts of one URL as a dict"""
from .visitor import COLUMNS, HOST_COLS, HL_COLS, PART_COLS, URLVisitor, extract, featurize, get_visitor, set_normalised, structure, tables  # noqa: F401
