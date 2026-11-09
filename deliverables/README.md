# deliverables/

`predict.py` is the prediction CLI / function required by `docs/task.md`. It uses the model, features, grammar and word lists from `../src/`
(latest run in `../src/models/results/`); nothing is trained or downloaded.

```bash
cd deliverables
../.venv/bin/python predict.py "https://www.PayPal-secure.login.tk/webscr?cmd=x"   # {"label": "phishing", "probability": 0.9565...}
../.venv/bin/python predict.py URL1 URL2                                            # one JSON object per URL (with the url)
../.venv/bin/python predict.py --test [-n N] [--seed S]                             # N random unseen URLs (default 50; 5% phishing, rest neutral); prints each prediction and a summary and saves them to results/
../.venv/bin/python -c "from predict import predict; print(predict('http://example.com'))"   # library use
```
`--vote` and `--best` change what is returned (they combine with `--test`):
* `--vote`: every deployed model (currently XGBoost, MLP, random forest) votes at its own 1%-FPR threshold; `label` is the majority vote, `probability` is the calibrated blend probability, and `votes` lists each model's label and raw probability (`phishing_votes` of `models`).
* `--best`: only the best deployed model by cross-validated AUC (currently XGBoost): its raw probability (not calibrated) and label at its own threshold, plus `"model"`.
The two flags are mutually exclusive.

Invalid input (not a string, empty, longer than 8192 characters, unparsable) returns `{"label": "clean", "probability": 0.0}`. `label` uses the threshold 0.939 fixed on out-of-fold training data.

## `--test` data
`data/unseen_pool.csv` (5,000 URLs: 1,000 phishing, 4,000 neutral; `url,label`, 1 = phishing) is a seeded random subset of the Kaggle dataset
**taruntiwarihp/phishing-site-urls** (https://www.kaggle.com/datasets/taruntiwarihp/phishing-site-urls, ODbL; 549,346 URLs; the "D1" set of Jalil et al. 2023, which
the research papers in this project cite). It is *unseen*: before sampling, every URL whose task-normalised form (lower-case, no scheme, no leading `www.`, no trailing slash)
appears in `train.csv` (434 URLs), `test.csv` (140) or `external_test.csv` (13) was removed, as were 6 URLs with conflicting labels and duplicates (501,069 unique left).
Host overlap with the supplied sets is not zero (phishing 3.9%, neutral 27.3% of pool rows share a registrable domain). Provenance: `data/unseen_pool.json`;
rebuild with `PYTHONPATH=src .venv/bin/python src/tools/build_unseen_pool.py phishing_site_urls.csv`.
Each `--test` run draws `-n` URLs (default 50) at random: ceil(5% of n) phishing (3 for 50) and the rest neutral; `--seed` makes it repeatable.

Caveats: the URLs have **no scheme**; they are parsed and measured exactly as written (the grammar accepts URLs without a scheme; nothing is prefixed or normalised). "good" means Common-Crawl-like ordinary pages, and 50 URLs are too few to estimate rates. On the whole 5,000-URL pool at the deployed threshold: AUC 0.942, recall 0.71, false-positive rate 4.7%, precision 0.79 (at the pool's 20% phishing share).
The false-positive rate is much higher than the ~1% seen on `test.csv`: another sign that the model's scores shift with the data source (Report.md).

## `results/`
Every `--test` run writes `results/test_<timestamp>_n<N>_seed<S>.csv` (`url,truth,prediction,probability,correct`) and a `.json` with the counts, the seed, the threshold and the model run used.
Analyse them with the error-analysis module: `PYTHONPATH=src ../.venv/bin/python -m tools.error_analysis results/<file>.csv` (see `../src/tools/error_analysis.py`).
