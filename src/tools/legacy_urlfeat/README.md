Frozen copy (2026-11-06) of the feature extractor BEFORE the URLVisitor refactor: `structure()` + `featurize` + `parts.tables` with their own generated parser and the original regexes.
Reference for `tools/check_visitor.py` and the source of the frozen outputs in `data/additional/visitor_oracle/`. Do not edit. Do not import it in the same process as `urlfeat`
(both put a module called `UrlLexer` on the path); `tools/legacy_oracle.py` runs it in its own process.
