# Run v2_20261104T1749_corr-filter-0.75

5-fold host-grouped CV on the training corpus (8651 URLs, 88 features). Blend = mean of xgboost, random_forest, adaboost, isotonic-calibrated.
Operating threshold of every model: score at 1% FPR on out-of-fold legitimate URLs.

## Cross-validation (validation folds, mean ± sd) and train-fold AUC

| model | AUC | recall@1%FPR | avg precision | Brier | OOF AUC |
|---|---|---|---|---|---|
| log_reg | 0.9548 ± 0.0180 | 0.589 | 0.958 | 0.080 | 0.9558 |
| svm | 0.9553 ± 0.0177 | 0.589 | 0.958 | 0.095 | 0.9567 |
| naive_bayes | 0.8944 ± 0.0248 | 0.161 | 0.879 | 0.208 | 0.8928 |
| knn | 0.9374 ± 0.0272 | 0.508 | 0.941 | 0.112 | 0.9371 |
| decision_tree | 0.9362 ± 0.0109 | 0.288 | 0.929 | 0.090 | 0.9370 |
| adaboost | 0.9628 ± 0.0107 | 0.605 | 0.964 | 0.184 | 0.9632 |
| mlp | 0.9563 ± 0.0153 | 0.551 | 0.956 | 0.074 | 0.9564 |
| random_forest | 0.9649 ± 0.0107 | 0.599 | 0.965 | 0.078 | 0.9659 |
| xgboost | 0.9684 ± 0.0116 | 0.641 | 0.970 | 0.062 | 0.9693 |
| blend_top3_calibrated | - | nan | nan | nan | 0.9708 |

## test.csv and external_test.csv (reserved sets, scored once)

| model | test AUC | test recall | test FPR | test precision | ext AUC | ext recall | ext FPR | ext precision |
|---|---|---|---|---|---|---|---|---|
| log_reg | 0.9629 | 0.592 | 0.0084 | 0.986 | 0.8722 | 0.418 | 0.0000 | 1.000 |
| svm | 0.9606 | 0.610 | 0.0091 | 0.985 | 0.8845 | 0.436 | 0.0000 | 1.000 |
| naive_bayes | 0.9041 | 0.495 | 0.0203 | 0.961 | 0.8870 | 0.339 | 0.0084 | 0.976 |
| knn | 0.9609 | 0.615 | 0.0161 | 0.975 | 0.9348 | 0.434 | 0.0049 | 0.989 |
| decision_tree | 0.9501 | 0.412 | 0.0049 | 0.988 | 0.8683 | 0.232 | 0.0000 | 1.000 |
| adaboost | 0.9715 | 0.632 | 0.0098 | 0.985 | 0.8883 | 0.399 | 0.0007 | 0.998 |
| mlp | 0.9756 | 0.475 | 0.0035 | 0.993 | 0.9403 | 0.296 | 0.0007 | 0.998 |
| random_forest | 0.9752 | 0.692 | 0.0147 | 0.979 | 0.9003 | 0.375 | 0.0000 | 1.000 |
| xgboost | 0.9810 | 0.682 | 0.0070 | 0.990 | 0.9155 | 0.414 | 0.0000 | 1.000 |
| blend_top3 | 0.9794 | 0.716 | 0.0147 | 0.980 | 0.9077 | 0.404 | 0.0000 | 1.000 |
| blend_top3_calibrated | 0.9782 | 0.748 | 0.0154 | 0.980 | 0.9062 | 0.435 | 0.0000 | 1.000 |

## Feature importance

Permutation importance = mean drop in validation-fold ROC AUC when one feature is shuffled (3 repeats x 5 folds). Full tables: `feature_importance.csv` (per model, with native importance) and `feature_importance_wide.csv`.

### Consensus (mean rank over the nine models; mean positive AUC drop)

| feature | mean rank | mean AUC drop |
|---|---|---|
| www | 4.2 | 0.0345 |
| sw_kit_path | 5.4 | 0.0125 |
| reg_log_rank | 6.0 | 0.0430 |
| n_hyphens_path | 6.6 | 0.0117 |
| url_legibility | 7.0 | 0.0123 |
| url_leet | 10.7 | 0.0089 |
| host_digit_rate | 12.2 | 0.0052 |
| sw_phrase_url | 13.3 | 0.0053 |
| ent_path_norm | 14.9 | 0.0076 |
| ent_url | 16.3 | 0.0051 |
| ent_max_seg | 18.4 | 0.0046 |
| n_seg | 19.2 | 0.0054 |
| ext_php | 19.7 | 0.0051 |
| host_len | 21.0 | 0.0027 |
| tld_suspicious | 22.2 | 0.0037 |
| ratio_nonalnum_url | 22.6 | 0.0024 |
| is_shortener | 24.5 | 0.0026 |
| n_dash_host | 24.9 | 0.0019 |
| query_len | 25.2 | 0.0026 |
| brand_in_path | 27.1 | 0.0020 |

### Top 8 features per model

* **log_reg**: www (0.034), reg_log_rank (0.029), url_legibility (0.021), sw_kit_path (0.020), n_hyphens_path (0.019), url_leet (0.013), n_seg (0.010), ent_url (0.009)
* **svm**: www (0.027), reg_log_rank (0.023), n_hyphens_path (0.020), sw_kit_path (0.018), url_legibility (0.016), ent_url (0.009), url_leet (0.008), ext_php (0.007)
* **naive_bayes**: sw_kit_path (0.032), emb_hex (0.025), sw_phrase_host (0.022), sfx_platform (0.021), ext_php (0.017), sw_phrase_url (0.014), query_len (0.013), n_at (0.012)
* **knn**: www (0.015), n_hyphens_path (0.012), sw_kit_path (0.010), tld_suspicious (0.010), sw_phrase_host (0.007), url_legibility (0.006), ext_php (0.005), brand_in_sub (0.005)
* **decision_tree**: reg_log_rank (0.134), www (0.088), ent_path_norm (0.034), url_leet (0.027), url_legibility (0.021), n_hyphens_path (0.016), sc_other_url (0.013), ent_url (0.012)
* **adaboost**: reg_log_rank (0.062), www (0.042), url_leet (0.011), ent_path_norm (0.010), sw_kit_path (0.009), n_hyphens_path (0.009), url_legibility (0.008), sw_phrase_url (0.008)
* **mlp**: reg_log_rank (0.040), www (0.040), url_legibility (0.021), n_seg (0.017), n_hyphens_path (0.012), sw_kit_path (0.012), ent_path_norm (0.010), url_leet (0.010)
* **random_forest**: reg_log_rank (0.040), www (0.025), sw_kit_path (0.005), url_legibility (0.004), ent_max_seg (0.004), n_hyphens_path (0.004), url_leet (0.003), sw_phrase_url (0.002)
* **xgboost**: reg_log_rank (0.053), www (0.034), url_legibility (0.009), sw_phrase_url (0.007), sw_kit_path (0.005), ent_max_seg (0.005), n_seg (0.005), n_hyphens_path (0.005)
