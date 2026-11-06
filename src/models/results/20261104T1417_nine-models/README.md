# Run 20261104T1417_nine-models

5-fold host-grouped CV on cleaned train.csv (8325 rows, 140 features). Blend = mean of mlp, xgboost, random_forest, isotonic-calibrated.
Operating threshold of every model: score at 1% FPR on out-of-fold legitimate URLs.

## Cross-validation (validation folds, mean ± sd) and train-fold AUC

| model | AUC | recall@1%FPR | avg precision | Brier | OOF AUC |
|---|---|---|---|---|---|
| log_reg | 0.9628 ± 0.0150 | 0.621 | 0.962 | 0.076 | 0.9631 |
| svm | 0.9610 ± 0.0168 | 0.617 | 0.961 | 0.081 | 0.9614 |
| naive_bayes | 0.8919 ± 0.0134 | 0.157 | 0.873 | 0.232 | 0.8869 |
| knn | 0.9482 ± 0.0218 | 0.501 | 0.946 | 0.107 | 0.9479 |
| decision_tree | 0.9239 ± 0.0242 | 0.343 | 0.912 | 0.109 | 0.9232 |
| adaboost | 0.9614 ± 0.0187 | 0.596 | 0.959 | 0.158 | 0.9617 |
| mlp | 0.9694 ± 0.0141 | 0.627 | 0.965 | 0.068 | 0.9692 |
| random_forest | 0.9634 ± 0.0180 | 0.572 | 0.960 | 0.078 | 0.9639 |
| xgboost | 0.9684 ± 0.0165 | 0.640 | 0.967 | 0.068 | 0.9686 |
| blend_top3_calibrated | - | nan | nan | nan | 0.9718 |

## test.csv and external_test.csv (reserved sets, scored once)

| model | test AUC | test recall | test FPR | test precision | ext AUC | ext recall | ext FPR | ext precision |
|---|---|---|---|---|---|---|---|---|
| log_reg | 0.9622 | 0.612 | 0.0147 | 0.977 | 0.8851 | 0.411 | 0.0007 | 0.998 |
| svm | 0.9616 | 0.602 | 0.0126 | 0.979 | 0.9003 | 0.415 | 0.0007 | 0.998 |
| naive_bayes | 0.8914 | 0.476 | 0.0315 | 0.938 | 0.8735 | 0.346 | 0.0091 | 0.974 |
| knn | 0.9607 | 0.612 | 0.0126 | 0.980 | 0.9283 | 0.351 | 0.0000 | 1.000 |
| decision_tree | 0.9413 | 0.253 | 0.0021 | 0.992 | 0.8136 | 0.083 | 0.0000 | 1.000 |
| adaboost | 0.9649 | 0.623 | 0.0077 | 0.988 | 0.8827 | 0.369 | 0.0000 | 1.000 |
| mlp | 0.9727 | 0.645 | 0.0119 | 0.982 | 0.9317 | 0.416 | 0.0000 | 1.000 |
| random_forest | 0.9739 | 0.640 | 0.0077 | 0.988 | 0.8970 | 0.298 | 0.0000 | 1.000 |
| xgboost | 0.9777 | 0.656 | 0.0063 | 0.990 | 0.9125 | 0.403 | 0.0000 | 1.000 |
| blend_top3 | 0.9774 | 0.679 | 0.0112 | 0.984 | 0.9131 | 0.393 | 0.0000 | 1.000 |
| blend_top3_calibrated | 0.9773 | 0.691 | 0.0112 | 0.984 | 0.9091 | 0.403 | 0.0000 | 1.000 |

## Feature importance

Permutation importance = mean drop in validation-fold ROC AUC when one feature is shuffled (3 repeats x 5 folds). Full tables: `feature_importance.csv` (per model, with native importance) and `feature_importance_wide.csv`.

### Consensus (mean rank over the nine models; mean positive AUC drop)

| feature | mean rank | mean AUC drop |
|---|---|---|
| reg_popular | 5.7 | 0.0299 |
| www | 6.0 | 0.0284 |
| url_leet | 7.2 | 0.0114 |
| sw_kit_path | 10.2 | 0.0068 |
| url_legibility | 10.9 | 0.0097 |
| sw_phrase_url | 12.2 | 0.0066 |
| host_digit_rate | 15.0 | 0.0062 |
| n_hyphens_path | 22.8 | 0.0030 |
| max_seg_len | 24.8 | 0.0065 |
| seg_consonant_run | 25.0 | 0.0051 |
| sw_kit_url | 25.9 | 0.0032 |
| host_legibility | 26.1 | 0.0021 |
| brand_in_path | 31.1 | 0.0022 |
| is_shortener | 31.3 | 0.0027 |
| tld_suspicious | 31.9 | 0.0025 |
| ratio_hyphen_url | 32.4 | 0.0014 |
| url_digit_rate | 33.1 | 0.0016 |
| seg_max_leet | 34.0 | 0.0018 |
| trailing_slash | 34.1 | 0.0012 |
| ent_max_seg | 34.8 | 0.0024 |

### Top 8 features per model

* **log_reg**: reg_popular (0.037), www (0.025), seg_consonant_run (0.014), sw_kit_path (0.012), url_leet (0.011), max_seg_len (0.010), n_seg (0.010), host_digit_rate (0.009)
* **svm**: reg_popular (0.039), www (0.030), seg_consonant_run (0.016), url_leet (0.014), sw_kit_path (0.012), host_digit_rate (0.012), max_seg_len (0.010), ent_path_norm (0.009)
* **naive_bayes**: sw_phrase_host (0.023), sw_phrase_query (0.022), emb_hex (0.018), sfx_platform (0.017), sw_kit_path (0.017), host_digit_rate (0.015), sc_delims_query (0.014), url_leet (0.013)
* **knn**: www (0.008), reg_popular (0.006), url_legibility (0.005), tld_suspicious (0.004), sw_phrase_host (0.004), sw_kit_path (0.004), sw_phrase_path (0.003), sw_kit_url (0.003)
* **decision_tree**: www (0.088), reg_popular (0.081), url_leet (0.042), seg_min_legibility (0.029), url_legibility (0.029), max_seg_len (0.025), sc_other_url (0.023), ent_url (0.011)
* **adaboost**: reg_popular (0.034), www (0.032), sw_phrase_url (0.013), url_leet (0.013), url_legibility (0.011), host_digit_rate (0.006), ent_url (0.006), sw_kit_path (0.005)
* **mlp**: reg_popular (0.026), www (0.025), url_legibility (0.010), seg_consonant_run (0.008), sw_kit_path (0.007), n_dash_host (0.007), n_seg (0.005), host_digit_rate (0.005)
* **random_forest**: www (0.017), reg_popular (0.014), url_legibility (0.005), sw_phrase_url (0.003), url_leet (0.003), sw_kit_path (0.002), sw_kit_url (0.001), url_digit_rate (0.001)
* **xgboost**: www (0.028), reg_popular (0.027), url_legibility (0.010), sw_phrase_url (0.009), host_digit_rate (0.004), url_leet (0.003), ratio_nonalnum_url (0.003), sw_kit_path (0.003)
