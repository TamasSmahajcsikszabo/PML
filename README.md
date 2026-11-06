# URL-only phishing classifier

Task: `docs/task.md`. Report: `REPORT.md`. Data (`train.csv`, `test.csv`, `external_test.csv`) is **not** in the repo; put it in `data/`.

## Setup (Python 3.14 used; any 3.11+ should work)
```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt     # or: uv venv && uv pip install -r requirements.txt
```
No Java and no network are needed (pyspellchecker ships its dictionary). Java is only needed (the ANTLR 4.13.2 jar is in `src/grammar/`) to regenerate `src/urlfeat/parser/` from `src/grammar/*.g4`:
`cd src/grammar && java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor -Xexact-output-dir -o ../urlfeat/parser UrlLexer.g4 UrlParser.g4`

## Commands
```bash
PYTHONPATH=src .venv/bin/python -m models.run       # ~25 min CPU: clean, tune + 5-fold CV of nine models, importances, blend, calibrate -> models/results/{runID}/
PYTHONPATH=src .venv/bin/python src/evaluate.py         # deep-dive of the deployed blend (overlap, CIs, precision at 1/1000) + src/models/predictions.csv
PYTHONPATH=src .venv/bin/python src/ablation.py         # optional, ~5 min: feature-group drop-one/only analysis
PYTHONPATH=src .venv/bin/python -c "from predict import predict; print(predict('https://www.PayPal-secure.login.tk/webscr?cmd=x'))"
```
All Python code lives in `src/`; run it with `PYTHONPATH=src` (or `cd src`) so `from predict import predict` works. `src/predict.py` loads the latest run in `src/models/results/` (pointer file `LATEST`); nothing is trained or downloaded.

## Layout
| path | what |
|---|---|
| `src/urlfeat/` | features: `readability.py` (dictionary legibility / typo / leet, ported from the other repo), `structure.py` (ANTLR grammar -> 63 structural/text-value columns, Python port of url_grammar's `Features.java`, verified identical on 7,216 URLs), `lexical.py` (entropy, special characters, suspicious words, brand / look-alike, shorteners...), `obfuscation.py` (special-character ratios, homoglyph checks), `__init__.py` (140-column matrix) |
| `src/grammar/`, `src/urlfeat/parser/` | ANTLR grammar + `antlr-4.13.2-complete.jar` (same SHA-256 as url_grammar's) and the generated Python parser (do not edit the parser) |
| `src/lists/` | word lists; provenance in `CLAUDE.md` and in each file's header |
| `common.py` | cleaning, host grouping, paths |
| `src/models/model.py`, `src/models/run.py` | the nine classifiers + search spaces; training / CV / importance / results writer |
| `deliverables/` | `predict.py` CLI/library required by the task (`--test` runs 50 unseen URLs from a Kaggle dataset); see its README |
| `src/models/predictions.csv` | `url,probability` for every `test.csv` row (written by `src/evaluate.py`) |
| `src/models/results/{runID}/` | metrics, feature importances, OOF predictions, config, deployable model |
| `src/evaluate.py`, `src/predict.py`, `src/ablation.py`, `src/common.py` | deep-dive evaluation, single-URL prediction, feature-group ablation |
