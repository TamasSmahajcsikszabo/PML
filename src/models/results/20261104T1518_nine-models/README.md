# Run 20261104T1518_nine-models

5-fold host-grouped CV on the training corpus (66187 URLs, 141 features). Blend = mean of xgboost, mlp, random_forest, isotonic-calibrated.
Operating threshold of every model: score at 1% FPR on out-of-fold legitimate URLs.

## Cross-validation (validation folds, mean ± sd) and train-fold AUC

| model | AUC | recall@1%FPR | avg precision | Brier | OOF AUC |
|---|---|---|---|---|---|
| log_reg | 0.9609 ± 0.0074 | 0.590 | 0.954 | 0.075 | 0.9605 |
| svm | 0.9604 ± 0.0081 | 0.591 | 0.954 | 0.078 | 0.9601 |
| naive_bayes | 0.8752 ± 0.0142 | 0.109 | 0.820 | 0.225 | 0.8746 |
| knn | 0.9610 ± 0.0065 | 0.572 | 0.952 | 0.078 | 0.9608 |
| decision_tree | 0.9467 ± 0.0071 | 0.397 | 0.926 | 0.088 | 0.9471 |
| adaboost | 0.9722 ± 0.0019 | 0.656 | 0.966 | 0.175 | 0.9722 |
| mlp | 0.9807 ± 0.0030 | 0.757 | 0.977 | 0.051 | 0.9805 |
| random_forest | 0.9789 ± 0.0042 | 0.714 | 0.974 | 0.058 | 0.9789 |
| xgboost | 0.9821 ± 0.0030 | 0.748 | 0.979 | 0.050 | 0.9821 |
| blend_top3_calibrated | - | nan | nan | nan | 0.9839 |

## test.csv and external_test.csv (reserved sets, scored once)

| model | test AUC | test recall | test FPR | test precision | ext AUC | ext recall | ext FPR | ext precision |
|---|---|---|---|---|---|---|---|---|
| log_reg | 0.9403 | 0.526 | 0.0084 | 0.984 | 0.9691 | 0.301 | 0.0000 | 1.000 |
| svm | 0.9366 | 0.533 | 0.0119 | 0.978 | 0.9704 | 0.314 | 0.0007 | 0.998 |
| naive_bayes | 0.8936 | 0.455 | 0.0231 | 0.952 | 0.8876 | 0.274 | 0.0077 | 0.973 |
| knn | 0.9587 | 0.530 | 0.0070 | 0.987 | 0.9644 | 0.421 | 0.0014 | 0.997 |
| decision_tree | 0.9291 | 0.327 | 0.0049 | 0.985 | 0.9623 | 0.213 | 0.0000 | 1.000 |
| adaboost | 0.9570 | 0.628 | 0.0203 | 0.969 | 0.9868 | 0.432 | 0.0000 | 1.000 |
| mlp | 0.9731 | 0.747 | 0.0182 | 0.976 | 0.9719 | 0.604 | 0.0035 | 0.994 |
| random_forest | 0.9749 | 0.719 | 0.0140 | 0.981 | 0.9734 | 0.498 | 0.0035 | 0.993 |
| xgboost | 0.9740 | 0.724 | 0.0147 | 0.980 | 0.9840 | 0.519 | 0.0007 | 0.999 |
| blend_top3 | 0.9775 | 0.768 | 0.0182 | 0.977 | 0.9858 | 0.570 | 0.0014 | 0.998 |
| blend_top3_calibrated | 0.9774 | 0.780 | 0.0224 | 0.972 | 0.9858 | 0.586 | 0.0014 | 0.998 |

## Feature importance

Permutation importance = mean drop in validation-fold ROC AUC when one feature is shuffled (3 repeats x 5 folds). Full tables: `feature_importance.csv` (per model, with native importance) and `feature_importance_wide.csv`.

### Consensus (mean rank over the nine models; mean positive AUC drop)

| feature | mean rank | mean AUC drop |
|---|---|---|
| reg_log_rank | 5.7 | 0.0480 |
| www | 7.8 | 0.0163 |
| sw_phrase_url | 8.9 | 0.0117 |
| https | 10.0 | 0.0119 |
| url_legibility | 11.3 | 0.0103 |
| ratio_nonalnum_url | 13.2 | 0.0155 |
| ratio_delims_url | 16.9 | 0.0179 |
| tld_suspicious | 17.7 | 0.0045 |
| url_leet | 17.9 | 0.0061 |
| sw_kit_url | 20.4 | 0.0040 |
| n_hyphens_path | 21.0 | 0.0066 |
| sw_kit_path | 21.2 | 0.0046 |
| host_digit_rate | 21.8 | 0.0064 |
| brand_in_path | 24.7 | 0.0029 |
| n_dash_host | 28.7 | 0.0053 |
| sw_brand_url | 28.7 | 0.0049 |
| seg_max_leet | 30.2 | 0.0019 |
| host_len | 30.9 | 0.0044 |
| max_seg_len | 33.5 | 0.0088 |
| n_seg | 34.0 | 0.0194 |

### Top 8 features per model

* **log_reg**: n_seg (0.070), ratio_delims_url (0.053), ent_url (0.044), ent_path (0.043), ratio_dot_url (0.040), ratio_nonalnum_url (0.036), max_seg_len (0.032), reg_log_rank (0.027)
* **svm**: n_seg (0.080), ratio_delims_url (0.060), ent_path (0.059), ent_url (0.053), ratio_dot_url (0.046), ratio_nonalnum_url (0.040), reg_log_rank (0.031), max_seg_len (0.028)
* **naive_bayes**: sw_brand_url (0.017), tld_suspicious (0.016), sw_kit_path (0.014), sw_phrase_url (0.014), sw_phrase_query (0.013), sw_phrase_path (0.012), emb_domain (0.012), sw_phrase_host (0.012)
* **knn**: https (0.007), tld_suspicious (0.007), ratio_nonalnum_url (0.006), www (0.004), brand_in_path (0.003), sw_kit_path (0.003), sw_phrase_path (0.003), sw_kit_url (0.003)
* **decision_tree**: reg_log_rank (0.159), www (0.041), https (0.031), sw_phrase_url (0.030), n_hyphens_path (0.029), url_legibility (0.019), host_digit_rate (0.017), url_leet (0.012)
* **adaboost**: reg_log_rank (0.057), www (0.020), sw_phrase_url (0.013), https (0.013), url_legibility (0.012), host_len (0.011), ratio_delims_url (0.009), n_hyphens_path (0.009)
* **mlp**: reg_log_rank (0.072), ratio_nonalnum_url (0.035), ratio_delims_url (0.023), ratio_dot_url (0.021), n_seg (0.020), www (0.018), host_len (0.014), url_legibility (0.012)
* **random_forest**: reg_log_rank (0.029), https (0.010), www (0.009), ratio_nonalnum_url (0.004), sw_phrase_url (0.003), url_legibility (0.003), reg_popular (0.002), tld_suspicious (0.002)
* **xgboost**: reg_log_rank (0.044), www (0.015), https (0.009), url_legibility (0.007), sw_phrase_url (0.007), ratio_nonalnum_url (0.006), ratio_delims_url (0.005), host_len (0.003)
