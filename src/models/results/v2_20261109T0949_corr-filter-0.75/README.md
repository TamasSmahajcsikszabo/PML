# Run v2_20261109T0949_corr-filter-0.75

5-fold host-grouped CV on the training corpus (8651 URLs, 88 features). Blend = mean of xgboost, random_forest, adaboost, isotonic-calibrated.
Operating threshold of every model: score at 1% FPR on out-of-fold legitimate URLs.

## Cross-validation (validation folds, mean ± sd) and train-fold AUC

| model | AUC | recall@1%FPR | avg precision | Brier | OOF AUC |
|---|---|---|---|---|---|
| log_reg | 0.9550 ± 0.0181 | 0.596 | 0.958 | 0.079 | 0.9557 |
| svm | 0.9550 ± 0.0179 | 0.591 | 0.957 | 0.095 | 0.9564 |
| naive_bayes | 0.8944 ± 0.0247 | 0.160 | 0.879 | 0.208 | 0.8927 |
| knn | 0.9373 ± 0.0275 | 0.508 | 0.941 | 0.113 | 0.9370 |
| decision_tree | 0.9353 ± 0.0124 | 0.289 | 0.928 | 0.091 | 0.9359 |
| adaboost | 0.9610 ± 0.0141 | 0.625 | 0.963 | 0.182 | 0.9620 |
| mlp | 0.9573 ± 0.0173 | 0.603 | 0.958 | 0.074 | 0.9588 |
| random_forest | 0.9646 ± 0.0115 | 0.587 | 0.964 | 0.074 | 0.9655 |
| xgboost | 0.9681 ± 0.0115 | 0.636 | 0.970 | 0.063 | 0.9690 |
| blend_top3_calibrated | - | nan | nan | nan | 0.9703 |

## test.csv and external_test.csv (reserved sets, scored once)

| model | test AUC | test recall | test FPR | test precision | ext AUC | ext recall | ext FPR | ext precision |
|---|---|---|---|---|---|---|---|---|
| log_reg | 0.9635 | 0.595 | 0.0091 | 0.985 | 0.8673 | 0.403 | 0.0007 | 0.998 |
| svm | 0.9609 | 0.616 | 0.0098 | 0.984 | 0.8848 | 0.439 | 0.0000 | 1.000 |
| naive_bayes | 0.9041 | 0.495 | 0.0203 | 0.961 | 0.8874 | 0.337 | 0.0063 | 0.982 |
| knn | 0.9609 | 0.611 | 0.0154 | 0.975 | 0.9348 | 0.430 | 0.0049 | 0.989 |
| decision_tree | 0.9500 | 0.412 | 0.0049 | 0.988 | 0.8682 | 0.232 | 0.0000 | 1.000 |
| adaboost | 0.9697 | 0.629 | 0.0105 | 0.984 | 0.8815 | 0.412 | 0.0007 | 0.998 |
| mlp | 0.9730 | 0.388 | 0.0021 | 0.995 | 0.9408 | 0.266 | 0.0000 | 1.000 |
| random_forest | 0.9784 | 0.696 | 0.0119 | 0.983 | 0.8941 | 0.348 | 0.0000 | 1.000 |
| xgboost | 0.9809 | 0.670 | 0.0084 | 0.988 | 0.9129 | 0.408 | 0.0000 | 1.000 |
| blend_top3 | 0.9807 | 0.716 | 0.0112 | 0.985 | 0.9012 | 0.402 | 0.0000 | 1.000 |
| blend_top3_calibrated | 0.9804 | 0.717 | 0.0112 | 0.985 | 0.9003 | 0.404 | 0.0000 | 1.000 |

## Feature importance

Permutation importance = mean drop in validation-fold ROC AUC when one feature is shuffled (3 repeats x 5 folds). Full tables: `feature_importance.csv` (per model, with native importance) and `feature_importance_wide.csv`.

### Consensus (mean rank over the nine models; mean positive AUC drop)

| feature | mean rank | mean AUC drop |
|---|---|---|
| www | 4.2 | 0.0345 |
| sw_kit_path | 5.4 | 0.0127 |
| reg_log_rank | 6.2 | 0.0439 |
| url_legibility | 6.7 | 0.0132 |
| n_hyphens_path | 6.8 | 0.0118 |
| url_leet | 10.6 | 0.0097 |
| host_digit_rate | 12.1 | 0.0054 |
| sw_phrase_url | 13.3 | 0.0056 |
| ent_path_norm | 15.8 | 0.0065 |
| ent_url | 16.4 | 0.0055 |
| ent_max_seg | 18.7 | 0.0053 |
| n_seg | 19.3 | 0.0085 |
| host_len | 19.4 | 0.0028 |
| ext_php | 19.6 | 0.0052 |
| tld_suspicious | 21.4 | 0.0037 |
| ratio_nonalnum_url | 23.2 | 0.0023 |
| is_shortener | 23.4 | 0.0027 |
| n_dash_host | 25.3 | 0.0020 |
| query_len | 25.4 | 0.0026 |
| brand_in_path | 27.5 | 0.0020 |

### Top 8 features per model

* **log_reg**: www (0.038), reg_log_rank (0.034), url_legibility (0.027), url_leet (0.022), sw_kit_path (0.021), n_hyphens_path (0.018), n_seg (0.017), ent_url (0.013)
* **svm**: www (0.028), reg_log_rank (0.023), n_hyphens_path (0.021), sw_kit_path (0.018), url_legibility (0.016), ent_url (0.009), url_leet (0.008), ext_php (0.007)
* **naive_bayes**: sw_kit_path (0.032), emb_hex (0.025), sw_phrase_host (0.022), sfx_platform (0.021), ext_php (0.017), sw_phrase_url (0.014), query_len (0.013), n_at (0.013)
* **knn**: www (0.015), n_hyphens_path (0.012), sw_kit_path (0.010), tld_suspicious (0.010), sw_phrase_host (0.007), url_legibility (0.007), ext_php (0.005), brand_in_sub (0.005)
* **decision_tree**: reg_log_rank (0.133), www (0.088), n_seg (0.027), url_leet (0.024), url_legibility (0.021), n_hyphens_path (0.018), ent_path_norm (0.018), sc_other_url (0.013)
* **adaboost**: reg_log_rank (0.063), www (0.036), url_leet (0.013), url_legibility (0.010), ent_path_norm (0.009), n_hyphens_path (0.009), sw_kit_path (0.008), ent_max_seg (0.008)
* **mlp**: reg_log_rank (0.043), www (0.042), url_legibility (0.020), n_seg (0.018), sw_kit_path (0.013), ent_path_norm (0.012), n_hyphens_path (0.012), url_leet (0.009)
* **random_forest**: reg_log_rank (0.040), www (0.026), sw_kit_path (0.005), url_legibility (0.004), n_hyphens_path (0.004), ent_max_seg (0.004), url_leet (0.003), sw_phrase_url (0.003)
* **xgboost**: reg_log_rank (0.052), www (0.033), url_legibility (0.009), sw_phrase_url (0.007), sw_kit_path (0.005), n_seg (0.005), ent_max_seg (0.005), n_hyphens_path (0.005)
