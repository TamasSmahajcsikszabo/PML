# Run v1_20261109T1155_all-features-train+extra

5-fold host-grouped CV on the training corpus (43255 URLs, 141 features). Blend = mean of xgboost, mlp, random_forest, isotonic-calibrated.
Operating threshold of every model: score at 1% FPR on out-of-fold legitimate URLs.

## Cross-validation (validation folds, mean ± sd) and train-fold AUC

| model | AUC | recall@1%FPR | avg precision | Brier | OOF AUC |
|---|---|---|---|---|---|
| log_reg | 0.9602 ± 0.0136 | 0.608 | 0.963 | 0.076 | 0.9600 |
| svm | 0.9598 ± 0.0137 | 0.607 | 0.963 | 0.081 | 0.9597 |
| naive_bayes | 0.8806 ± 0.0239 | 0.140 | 0.859 | 0.281 | 0.8780 |
| knn | 0.9562 ± 0.0148 | 0.556 | 0.957 | 0.085 | 0.9561 |
| decision_tree | 0.9418 ± 0.0103 | 0.374 | 0.935 | 0.092 | 0.9418 |
| adaboost | 0.9704 ± 0.0059 | 0.642 | 0.972 | 0.179 | 0.9702 |
| mlp | 0.9771 ± 0.0070 | 0.735 | 0.979 | 0.055 | 0.9769 |
| random_forest | 0.9761 ± 0.0067 | 0.686 | 0.977 | 0.062 | 0.9760 |
| xgboost | 0.9813 ± 0.0052 | 0.762 | 0.983 | 0.050 | 0.9812 |
| blend_top3_calibrated | - | nan | nan | nan | 0.9818 |

## test.csv and external_test.csv (reserved sets, scored once)

| model | test AUC | test recall | test FPR | test precision | ext AUC | ext recall | ext FPR | ext precision |
|---|---|---|---|---|---|---|---|---|
| log_reg | 0.9503 | 0.507 | 0.0042 | 0.992 | 0.9688 | 0.286 | 0.0000 | 1.000 |
| svm | 0.9492 | 0.516 | 0.0063 | 0.988 | 0.9702 | 0.311 | 0.0000 | 1.000 |
| naive_bayes | 0.8988 | 0.395 | 0.0217 | 0.948 | 0.8897 | 0.239 | 0.0049 | 0.980 |
| knn | 0.9594 | 0.494 | 0.0028 | 0.994 | 0.9622 | 0.383 | 0.0021 | 0.995 |
| decision_tree | 0.9480 | 0.445 | 0.0056 | 0.988 | 0.9723 | 0.239 | 0.0000 | 1.000 |
| adaboost | 0.9629 | 0.596 | 0.0077 | 0.987 | 0.9868 | 0.428 | 0.0000 | 1.000 |
| mlp | 0.9786 | 0.675 | 0.0049 | 0.993 | 0.9780 | 0.522 | 0.0014 | 0.997 |
| random_forest | 0.9765 | 0.714 | 0.0119 | 0.984 | 0.9645 | 0.468 | 0.0021 | 0.996 |
| xgboost | 0.9810 | 0.707 | 0.0084 | 0.988 | 0.9650 | 0.502 | 0.0014 | 0.997 |
| blend_top3 | 0.9814 | 0.745 | 0.0112 | 0.985 | 0.9785 | 0.515 | 0.0021 | 0.996 |
| blend_top3_calibrated | 0.9814 | 0.750 | 0.0112 | 0.985 | 0.9784 | 0.522 | 0.0028 | 0.995 |

## Feature importance

Permutation importance = mean drop in validation-fold ROC AUC when one feature is shuffled (3 repeats x 5 folds). Full tables: `feature_importance.csv` (per model, with native importance) and `feature_importance_wide.csv`.

### Consensus (mean rank over the nine models; mean positive AUC drop)

| feature | mean rank | mean AUC drop |
|---|---|---|
| www | 8.3 | 0.0177 |
| reg_log_rank | 9.4 | 0.0417 |
| url_legibility | 9.8 | 0.0109 |
| sw_phrase_url | 9.9 | 0.0097 |
| ext_php | 11.2 | 0.0085 |
| https | 11.6 | 0.0090 |
| ratio_nonalnum_url | 12.2 | 0.0127 |
| url_leet | 14.9 | 0.0065 |
| sw_kit_path | 15.6 | 0.0054 |
| ratio_delims_url | 17.4 | 0.0092 |
| tld_suspicious | 18.7 | 0.0038 |
| sw_kit_url | 18.7 | 0.0043 |
| n_hyphens_path | 21.1 | 0.0060 |
| host_digit_rate | 23.3 | 0.0051 |
| host_len | 23.9 | 0.0038 |
| seg_max_leet | 25.6 | 0.0023 |
| max_seg_len | 26.1 | 0.0063 |
| brand_in_path | 29.9 | 0.0023 |
| is_shortener | 30.8 | 0.0021 |
| n_seg | 31.1 | 0.0099 |

### Top 8 features per model

* **log_reg**: n_seg (0.050), ent_path (0.032), ratio_delims_url (0.030), ratio_nonalnum_url (0.028), max_seg_len (0.026), ext_php (0.025), ent_url (0.024), ratio_dot_url (0.021)
* **svm**: n_seg (0.027), url_legibility (0.020), ratio_nonalnum_url (0.020), ext_php (0.019), www (0.018), ratio_delims_url (0.018), reg_log_rank (0.017), n_dash_host (0.016)
* **naive_bayes**: sw_brand_url (0.019), sw_kit_path (0.017), sw_phrase_query (0.016), sw_phrase_host (0.016), sw_phrase_url (0.014), tld_suspicious (0.013), sw_phrase_path (0.012), n_amp_esc (0.012)
* **knn**: https (0.007), ratio_nonalnum_url (0.005), tld_suspicious (0.005), www (0.004), sw_kit_path (0.003), url_legibility (0.003), is_shortener (0.003), sw_kit_url (0.003)
* **decision_tree**: reg_log_rank (0.163), www (0.050), sw_phrase_url (0.032), n_hyphens_path (0.025), https (0.019), url_legibility (0.019), url_leet (0.017), n_sub (0.015)
* **adaboost**: reg_log_rank (0.049), www (0.026), url_legibility (0.013), https (0.010), sw_phrase_url (0.010), host_len (0.009), n_hyphens_path (0.008), sw_kit_path (0.008)
* **mlp**: reg_log_rank (0.052), ratio_nonalnum_url (0.034), www (0.018), ratio_delims_url (0.012), url_legibility (0.012), https (0.010), ext_php (0.010), host_len (0.008)
* **random_forest**: reg_log_rank (0.026), www (0.010), https (0.008), ratio_nonalnum_url (0.004), url_legibility (0.003), sw_phrase_url (0.003), url_leet (0.002), reg_popular (0.002)
* **xgboost**: reg_log_rank (0.043), www (0.013), ratio_nonalnum_url (0.012), https (0.008), url_legibility (0.007), sw_phrase_url (0.006), ratio_delims_url (0.006), ext_php (0.004)
