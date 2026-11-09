# Run v2_20261109T1131_corr-filter-0.75-train+extra

5-fold host-grouped CV on the training corpus (43255 URLs, 98 features). Blend = mean of xgboost, mlp, random_forest, isotonic-calibrated.
Operating threshold of every model: score at 1% FPR on out-of-fold legitimate URLs.

## Cross-validation (validation folds, mean ± sd) and train-fold AUC

| model | AUC | recall@1%FPR | avg precision | Brier | OOF AUC |
|---|---|---|---|---|---|
| log_reg | 0.9557 ± 0.0134 | 0.587 | 0.959 | 0.081 | 0.9554 |
| svm | 0.9555 ± 0.0136 | 0.585 | 0.959 | 0.084 | 0.9553 |
| naive_bayes | 0.8951 ± 0.0175 | 0.185 | 0.883 | 0.294 | 0.8948 |
| knn | 0.9547 ± 0.0156 | 0.561 | 0.955 | 0.084 | 0.9544 |
| decision_tree | 0.9402 ± 0.0108 | 0.409 | 0.933 | 0.093 | 0.9404 |
| adaboost | 0.9691 ± 0.0065 | 0.637 | 0.971 | 0.178 | 0.9689 |
| mlp | 0.9787 ± 0.0058 | 0.730 | 0.980 | 0.054 | 0.9783 |
| random_forest | 0.9768 ± 0.0067 | 0.688 | 0.977 | 0.061 | 0.9766 |
| xgboost | 0.9807 ± 0.0054 | 0.752 | 0.982 | 0.051 | 0.9806 |
| blend_top3_calibrated | - | nan | nan | nan | 0.9818 |

## test.csv and external_test.csv (reserved sets, scored once)

| model | test AUC | test recall | test FPR | test precision | ext AUC | ext recall | ext FPR | ext precision |
|---|---|---|---|---|---|---|---|---|
| log_reg | 0.9431 | 0.483 | 0.0035 | 0.993 | 0.9677 | 0.295 | 0.0007 | 0.998 |
| svm | 0.9425 | 0.502 | 0.0049 | 0.990 | 0.9689 | 0.321 | 0.0007 | 0.998 |
| naive_bayes | 0.8830 | 0.155 | 0.0000 | 1.000 | 0.9140 | 0.091 | 0.0000 | 1.000 |
| knn | 0.9598 | 0.482 | 0.0042 | 0.991 | 0.9703 | 0.406 | 0.0035 | 0.991 |
| decision_tree | 0.9492 | 0.431 | 0.0063 | 0.986 | 0.9739 | 0.243 | 0.0000 | 1.000 |
| adaboost | 0.9616 | 0.611 | 0.0175 | 0.972 | 0.9834 | 0.449 | 0.0000 | 1.000 |
| mlp | 0.9739 | 0.664 | 0.0084 | 0.988 | 0.9688 | 0.540 | 0.0035 | 0.994 |
| random_forest | 0.9766 | 0.689 | 0.0105 | 0.985 | 0.9672 | 0.464 | 0.0014 | 0.997 |
| xgboost | 0.9803 | 0.707 | 0.0105 | 0.985 | 0.9631 | 0.507 | 0.0021 | 0.996 |
| blend_top3 | 0.9800 | 0.728 | 0.0098 | 0.987 | 0.9758 | 0.527 | 0.0014 | 0.997 |
| blend_top3_calibrated | 0.9799 | 0.762 | 0.0154 | 0.980 | 0.9756 | 0.561 | 0.0028 | 0.995 |

## Feature importance

Permutation importance = mean drop in validation-fold ROC AUC when one feature is shuffled (3 repeats x 5 folds). Full tables: `feature_importance.csv` (per model, with native importance) and `feature_importance_wide.csv`.

### Consensus (mean rank over the nine models; mean positive AUC drop)

| feature | mean rank | mean AUC drop |
|---|---|---|
| reg_log_rank | 1.9 | 0.0517 |
| www | 3.7 | 0.0203 |
| sw_phrase_url | 5.9 | 0.0150 |
| url_legibility | 7.0 | 0.0124 |
| https | 7.2 | 0.0109 |
| sw_kit_url | 7.4 | 0.0118 |
| n_hyphens_path | 7.7 | 0.0146 |
| host_len | 11.4 | 0.0089 |
| ratio_nonalnum_url | 12.9 | 0.0115 |
| ext_php | 13.3 | 0.0059 |
| ratio_delims_url | 17.0 | 0.0098 |
| tld_suspicious | 18.0 | 0.0032 |
| n_seg | 19.1 | 0.0067 |
| url_leet | 20.0 | 0.0058 |
| host_digit_rate | 20.2 | 0.0046 |
| n_dash_host | 23.7 | 0.0043 |
| mean_seg_len | 23.7 | 0.0031 |
| ratio_dot_url | 24.4 | 0.0076 |
| seg_max_leet | 25.0 | 0.0016 |
| brand_in_path | 25.9 | 0.0016 |

### Top 8 features per model

* **log_reg**: reg_log_rank (0.029), url_legibility (0.027), sw_phrase_url (0.023), ratio_dot_url (0.021), www (0.021), n_hyphens_path (0.020), sw_kit_url (0.020), ratio_delims_url (0.019)
* **svm**: reg_log_rank (0.032), url_legibility (0.024), ratio_dot_url (0.024), www (0.021), ratio_delims_url (0.021), sw_phrase_url (0.020), n_hyphens_path (0.019), sw_kit_url (0.018)
* **naive_bayes**: reg_log_rank (0.061), n_hyphens_path (0.035), query_len (0.016), www (0.014), sw_kit_url (0.013), https (0.010), sw_phrase_url (0.010), seg_consonant_run (0.009)
* **knn**: sw_kit_url (0.012), https (0.010), tld_suspicious (0.009), n_hyphens_path (0.009), www (0.008), ext_php (0.007), ratio_nonalnum_url (0.006), brand_in_sub (0.005)
* **decision_tree**: reg_log_rank (0.164), www (0.051), sw_phrase_url (0.037), n_hyphens_path (0.028), url_legibility (0.020), https (0.019), url_leet (0.016), n_sub (0.016)
* **adaboost**: reg_log_rank (0.048), www (0.023), sw_phrase_url (0.014), url_legibility (0.013), https (0.012), host_len (0.010), sw_kit_url (0.010), n_hyphens_path (0.009)
* **mlp**: reg_log_rank (0.042), ratio_nonalnum_url (0.034), n_seg (0.024), host_len (0.022), ratio_delims_url (0.022), www (0.020), ratio_dot_url (0.016), url_legibility (0.011)
* **random_forest**: reg_log_rank (0.040), www (0.012), https (0.010), sw_phrase_url (0.007), ratio_nonalnum_url (0.005), url_legibility (0.004), mean_seg_len (0.004), n_hyphens_path (0.004)
* **xgboost**: reg_log_rank (0.046), ratio_nonalnum_url (0.015), www (0.014), sw_phrase_url (0.009), https (0.008), ratio_delims_url (0.008), url_legibility (0.006), host_len (0.006)
