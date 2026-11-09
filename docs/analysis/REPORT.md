# Analysis of 2026-11-06: ANTLR reliance, errors of the promoted model, the https gap

Model analysed: `v3_20261106T1204_parts-corpus` (mean of xgboost, blend, parts; threshold = 1% out-of-fold FPR). Raw outputs: `antlr_reliance.txt`, `scheme_gap.txt` (this folder); code: `src/tools/antlr_reliance.py`, `src/tools/scheme_gap.py`; error tables in the run folder (`errors_*.csv`, `error_analysis.md`).

## 1. How much, and where, the pipeline relies on ANTLR

> Update 2026-11-06 (later the same day): this section describes the extractor BEFORE the `URLVisitor` refactor. Now one visit of the parse tree (`urlfeat/visitor.py`, a child of the generated visitor) builds all features and the parts rows, there is no regex in `src/urlfeat/`, `split_url` is gone, and the word lists are generated ANTLR lexers. Measured after the refactor: `docs/analysis/visitor_agreement.md`.

**Where it is used.** One place: `urlfeat/structure.py::structure(url)`. It lexes and parses the raw string (modes: authority, path, query, fragment; vocabularies of TLDs, second-level suffixes, hosting platforms and file extensions are tokens compiled into `UrlVocab.g4`), walks the tree and returns scheme, host kind (IPv4 / domain / platform / other), subdomains, registrable label, public suffix, port, userinfo, path segments (+ extension), query keys and values, fragment, `%XX`, e-mail and nested-URL tokens. Everything else (`featurize`, `parts.tables`, `predict`) calls it; the models never see the tree, only numbers. A string the grammar rejects gives an all-NaN row, and `predict` then answers `clean, 0.0`. Runtime needs only the `antlr4-python3-runtime` package; Java/the jar is needed only to regenerate the parser.

**Cost.** Per URL (3,000 URLs): lexer 0.19 ms, lexer+parser 0.74 ms, `structure()` 0.88 ms, all 141 features 1.27 ms. ANTLR (incl. the tree walk) is about 69% of feature time. Parts features add about 0.85 ms per URL with the second parse; no URL of train/test/external (14,367) is rejected.

**Which columns depend on it** (141 full-URL columns, classification by data flow):

| origin | columns | share of permutation importance (run 20261104T1518 / v2) |
|---|---|---|
| read straight from the tree or its tokens (scheme, host kind, suffix kind, subdomains, path/query/fragment counts, ports, `%`, e-mail, nested) | 35 | 24% / 24% |
| computed from strings but fed by the tree's pieces (host text, registrable, suffix, extension, segments, query keys/values: brand rules, `reg_popular`, `reg_log_rank`, readability of host/sld/segments, TLD flags, ...) | 67 | 30% / 40% |
| string only (entropy, special characters, ratios, URL-wide word counts) | 39 | 46% / 37% |

The two top predictors (`reg_log_rank`, `reg_popular`) and `www` depend on the grammar's registrable/suffix split, so the strongest signals rest on ANTLR's public-suffix logic indirectly. The parts model uses the tree for the segment/key/value lists and the host frame.

**What happens without it** (XGBoost, train.csv, host-grouped CV; test and external fitted on all train):

| columns | CV AUC | test | external |
|---|---|---|---|
| all 141 | 0.9700 | 0.9807 | 0.9042 |
| without the 35 direct tree columns | 0.9635 | 0.9744 | 0.8788 |
| tree + tree-fed columns only (102) | 0.9658 | 0.9783 | 0.9180 |
| string-only (39) | 0.9309 | 0.9537 | 0.8318 |
| 35 direct tree columns only | 0.9084 | 0.9439 | 0.9119 |

So the parse is worth about 0.04 CV AUC against pure string features; its direct columns alone are worth about 0.006 once the rest remain. On external, string-only features are the weakest and the tree-only columns are not worse than everything (0.912 vs 0.904): string features carry the most source-specific signal.

**Two implementations of one decomposition.** `lexical.split_url` re-implements the path/query/fragment split by string rules. It agrees with the tree on all 14,367 URLs (0 differences in path, query, fragment lengths); a grammar change would need both updated.

**Risks.** (a) Vocabulary is frozen in the grammar (platform entries can cut real domains: 17 known collisions; unknown suffix falls to `other` silently; 267 of the first 3,000 train hosts are platform-hosted, so this matters); (b) a rejected string is scored "clean, 0.0" with no alarm; (c) the features that dominate the model depend on the split.

## 2. Errors of the promoted model, and improvement options (not implemented)

At the 1%-FPR threshold: out-of-fold recall 0.748 / FPR 0.010; test.csv recall 0.736 / FPR 0.0147; external recall 0.540 / FPR 0.0007.

**Missed phishing (false negatives)** look like ordinary sites. FN rate: URLs of at most 25 characters 0.44 (test 0.52), 26-40 characters 0.39-0.46, no path 0.37, popular registrable domain 0.51 (out-of-fold), `www` 0.33-0.38; on external `www` 0.77 and at most 25 characters 0.82. Separating features: low entropy, few digits, no suspicious word (`sw_phrase_*` d -0.5 to -0.7), no hex, short. Most confident misses: `www.autolikesfree.net/access-token.php`, `geocities.ws/steamcom/`, `nationwide-com.com/nationwide-log-in/...` (brand plus TLD glued with a hyphen), `officialliker.co/`.

**False alarms** cluster on platform-hosted sites (`sfx_platform` d 2.6-2.8: blogspot, blogfa, mihanblog), non-`www`, `http` (FP 0.026 vs 0.004 for https), leet/hex-like parts, shorteners and long URLs with login words. By source, `task_train` is the hardest (out-of-fold FPR 0.023 at the pooled threshold, AUC 0.966; others 0.979-0.991), which is why test.csv sits at FPR 0.0147 instead of 1%. A few "false positives" look like real phishing (`back.dog/auth/login`, `cyb-sys.com/jietg/Upue`), so label noise exists; its size is not measured.

**Improvement options**, ordered by my expectation of value (all hypotheses until tried):
1. **Character n-gram model** as a further member (earlier variant: +0.007 CV AUC, +0.03 external). Targets glued/odd names (`nationwide-com`, `steamcom`).
2. **Glue-and-brand features**: TLD word inside a registrable/segment label (`-com`, `com` suffix text), brand edit distance over a larger brand list, host-label parts for the parts model (U's `hlabel` aggregates).
3. **Platform handling**: tenant-level features for platform hosts (legibility/typo of the tenant, platform identity as a category), and the 17 collision fix; aims at the blogspot-type false alarms.
4. **Threshold for task-like data**: take the 1%-FPR threshold from `task_train` out-of-fold rows (or weight them), because the pooled threshold is too loose there (test FPR 0.0147).
5. **Less source dependence**: source-balanced sample weights, source-held-out and time-split evaluation (leave-one-source-out already shows 0.957-0.987), downweighting `www`/`reg_popular`/`reg_log_rank` through monotone constraints or by training without them as a robustness check.
6. **Parts model**: tune the three XGBoosts inside the folds, separate head/tail handling instead of mean/max/min, a path-less specialist.
7. **Label audit** of the top confident errors to size label noise before tuning further.
8. Homepage-style phishing is basically indistinguishable by URL alone; only non-URL evidence (domain age, DNS, certificate, page content) would separate it, which is outside the task.

## 3. The https gap (open item)

Out-of-fold, the promoted model misses 34% of https phishing but 20% of http phishing, and flags 0.4% of https vs 2.6% of http legitimate URLs.

* **It is a base-rate and threshold effect, not worse ranking.** Within each scheme the AUC is the same (http 0.978, https 0.982). The corpus is 65% phishing among http URLs but 26% among https, so https phishing gets lower scores. The mix depends on the source: `lakh_kaggle` has 8.7% phishing among https, `ebbu2017` 5.3%, the task data 43% (train.csv, test.csv and the feeds' https share are very different). train.csv-only models show no such gap (test recall 0.711 https vs 0.694 http).
* **Removing the scheme feature does not help** (train.csv, XGBoost: CV AUC 0.9695 vs 0.9700, recalls unchanged); the scheme is encoded elsewhere. Removing scheme and `www` costs 0.004 CV AUC.
* **Per-scheme thresholds** (1% FPR inside https and inside other), fitted on out-of-fold scores: they equalise the FPR by construction and shift recall from other to https, with no overall gain. Out-of-fold recall 0.748 -> 0.728 at FPR 0.010; test 0.736 -> 0.731 while FPR falls from 0.0147 to 0.0107; external 0.540 -> 0.557 (https 0.775 -> 0.863, other 0.328 -> 0.280).
* **Conclusion:** no change made. The gap reflects what the training sources contain, so the remedy is in the data mix (source-balanced weighting; more https phishing), not the model or a threshold. If a fairer operating point per scheme is wanted, use the per-scheme thresholds in `tools/scheme_gap.py` (the cost is the loss of recall for non-https URLs).
