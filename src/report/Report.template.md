# Phishing detection from the URL: Results and Recommendation

## Overview
A machine learning pipeline has been built that judges a URL by its text, without visiting the page. {{training_sentence}} It separates phishing from legitimate URLs, such ason websites it has never seen it reaches an AUC of {{auc_unseen_test}}, and on an independent collection {{auc_ext}}. At the chosen threshold it catches {{recall_test_pct}}% of phishing on the test set but only {{recall_ext_pct}}% on the independent collection, so its recall depends heavily on where the URLs come from.

## Pipeline Details
The core of the solution is an ANTLR grammar for URLs. ANTLR (Another Tool for Language Recognition) is a formal language design toolset with the options to generate lexers, parsers, listeners and visitors for target implementation languages. In this case, an elaborate URL parsing grammar was created with resources generated in Python. 
Every URL is read, lexed and parsed (scheme, host, path, query and fragment), and the *URLVisitor* walks through the AST (abstract syntax tree) of these parts and computes all {{columns}} features along the way. The feature building design choice was that the ANTLR visitor bundles all feature building and parsing logic as a single source of feature extraction.
Each feature belongs to the part of the URL it describes, which makes every number traceable and easy to test, reflected by actual parsing grammar rules. Fixed vocabularies are part of the grammar or matched against whole parts of the host: the {{tld_literals}} official top-level domains are lexer tokens, and the {{platform_names}} hosting platforms like `blogspot.com` are kept as a list that is matched against whole labels of the host.[if we used known lists, reference it here]
For instance, a host such as `cloud.google.com` is read correctly as the service `cloud` on the domain `google.com`, and all of the {{urls_checked}} supplied URLs are parsed correctly and not rejected by the specifically built grammar ({{urls_rejected}} rejected). Computing the features takes about {{ms_per_url}} milliseconds per URL.

The actual pipeline is shown on the following graph:
```mermaid
flowchart TD
  U[URL string] --> L[grammar: split into parts] --> V[visitor: one pass]
  V --> F[{{columns}} URL features] --> C[near-duplicates dropped: {{kept_features}} kept] --> M[nine ML models, best 3 averaged]
  V --> H[host, path segment and query features] --> Q[parts model]
  M --> A[average + calibration]
  Q --> A --> O["label and probability"]
```
The parts model looks at a URL as a set of pieces rather than as one row of numbers. During the same pass, the visitor also describes the host on its own and every path segment, query key and query value separately. Three XGBoost models score these pieces: one for hosts, one for path segments and one for query keys and values. Because a URL can have any number of segments and parameters, their scores are summarised per URL by the mean, the highest and the lowest score, so that a single suspicious piece can raise the result. A logistic regression then combines the host score with these summaries into one probability. All parts are trained so that a URL is never scored by a model that saw its own website.

As an explainable baseline, a logistic regression was trained. It reached an AUC of {{auc_base_test}} on the test set {{base_ext_join}} {{auc_base_ext}} on the independent collection.
The final solution averages three scores: an XGBoost model, the average of the three best of nine classifiers ({{blend_members}}), and a *parts model* that scores the host, every path segment and every query parameter separately and then combines them. The parts model was added because the URL-level models summarise a whole URL in one row and make their mistakes where both classes look alike; judging each piece on its own leads to different mistakes, so the average is more robust on a new source. On its own it is weaker ({{auc_parts_oof}} AUC in cross-validation), but {{parts_gain_text}}. This combination lifted the AUC to {{auc_test}} on the test set and {{auc_ext}} on the independent collection.

## The data
The training file has {{train_rows}} rows, about half of them phishing. It has not been cleaned: {{repeated_url_rows}} rows repeat a URL that already appeared, and {{conflict_urls}} URLs appear once as phishing and once as legitimate. A handful of websites also dominate the file; `blogspot.com`, `duilawyeryork.com` and `appspot.com` alone account for {{top3_rows}} rows. The file was kept as supplied, but was always validated with whole websites held out, so that the same site, or a duplicate of a URL, can never sit on both sides of a test. Without this, our validation would have looked {{cv_opt}} AUC better than it really is.

{{extra_data_text}}

## Model Performance
The threshold decides when a score counts as phishing. It was set using the training data only: every training URL was scored by a model that had not seen its website, and the threshold was placed so that only 1% of the legitimate training URLs score above it. In other words, we accept that about one legitimate URL in a hundred is flagged, and the recall is whatever the model achieves at that point. A stricter threshold would flag fewer legitimate URLs but also catch less phishing; 1% was fixed in advance, before the evaluation files were scored. The table shows how the model performs at that threshold; the ranges in brackets are 95% intervals.

{{table_metrics}}

About half of the test set rows ({{seen_share_test_pct}}%) come from websites that also appear in training, and on those the model scores an AUC of {{auc_seen_test}}, compared with {{auc_unseen_test}} on websites it has not seen. We measured the overlap in several ways, from the strict to the loose:

{{table_overlap}}

The task's own rule for "the same page" misses pages that differ only in a query string, an ID number or a mirrored host name; the looser rows of the table show how much that adds. {{label_agreement_text}}

The independent collection shares no page with the training data and only {{seen_share_ext_pct}}% of its rows come from websites seen in training, which makes it the better guide to new traffic. On it, at our fixed threshold the model catches {{recall_ext_pct}}% of phishing, while a threshold set on this collection itself would catch {{recall_matched_ext_pct}}% at the same 1% false-alarm rate. The most likely reason is that every legitimate URL in it is a bare homepage (all use https and `www`, and none has a path), which looks quite different from the legitimate URLs we trained on.

**URL normalisation.** {{normalised_text}}

## Data Insights
Phishing URLs often live on free hosting platforms: {{plat_ph}}% of the phishing URLs in training do, against {{plat_lg}}% of legitimate ones. They also more often contain a second domain name inside the URL ({{emb_ph}}% against {{emb_lg}}%) or a typical phishing word such as "login" or "verify" ({{phrase_ph}}% against {{phrase_lg}}%).

The presence of a path depends more on the data source than on phishing itself. Most legitimate URLs in training and test have a path ({{path_lg_train}}% and {{path_lg_test}}%), but none of those in the independent collection do. This hurts: the model catches only {{recall_nopath_test_pct}}% of phishing URLs without a path on the test set, against {{recall_path_test_pct}}% of those with one.

{{mixed_domain_text}}

One common belief did not hold up. We expected phishing to hide on unknown domains, and in training that is true: {{pop_lg_train}}% of legitimate URLs but only {{pop_ph_train}}% of phishing URLs sit on a domain from the 50,000 most popular websites. In the independent collection the picture reverses, with {{pop_lg_ext}}% against {{pop_ph_ext}}%. Domain popularity is nevertheless the model's strongest feature, so part of what the model learned is specific to how these collections were put together. These are patterns of these datasets, not general rules about phishing.

## Threshold and Deployment
To estimate how the model would do in practice, we assumed that one URL in a thousand is phishing and that the detection and false-alarm rates measured on the test set carry over to real traffic. We cannot verify the second assumption, because neither evaluation file is a sample of real traffic. Under these assumptions, only about {{prec_test_pct}}% of the URLs the model flags would actually be phishing (somewhere between {{prec_test_lo}}% and {{prec_test_hi}}%). {{ext_fp_text}}

The evaluation sets are too small to pin down the false-alarm rate more precisely than {{fpr_factor_text}}, and at a prevalence of one in a thousand that rate decides almost everything. Blocking is therefore not justified. A warning to the user, or a ranking that sends the most suspicious URLs to a reviewer first, is a reasonable use. Before a wider rollout we would need a labelled sample of real incoming URLs (tens of thousands of legitimate ones), an evaluation on later data than the training data, and an agreement on what a missed phishing URL costs compared with a wrongly flagged one.

The function `predict(url)` returns a label and a probability. The probability is calibrated for a population that is half phishing, like our data, not for real traffic, where the true chance is far lower; it also shifts on other sources. Inputs that cannot be read as a URL (not text, empty, longer than {{max_len}} characters, or rejected by the grammar) return "clean" with probability 0, which means "no evidence", not "safe". A URL is labelled phishing when its returned probability is above about {{thr_cal}}.

## Key Decisions

{{table_decisions}}

## Limitations and next steps
The data has no dates, so we could not test whether the model holds up over time. The added public data may resemble the independent collection more than real traffic does. The strongest features, domain popularity and the `www` prefix, depend on how the collections were built. Some choices were made with the full training file in view (the removal of near-duplicate features), and the averaging of three models was chosen after earlier runs had shown their external scores, so the independent collection is not completely untouched. Not done yet: a model on the raw characters of the URL (an earlier version of it improved the independent results), adjusting the model to the real share of phishing, a variant that relies less on source-specific signals, and features that separate pages within one website (see the same-website analysis above).
