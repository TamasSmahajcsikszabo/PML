# Run v3_20261106T1202_parts-train

Parts model on train (8651 URLs), combined with the parent run v2_20261104T1749_corr-filter-0.75. 5-fold host-grouped CV (same folds as the parent); test.csv / external_test.csv scored once.
Deployed candidate: **xgboost+blend+parts_mean** (threshold 0.8451 on the raw mean = 1% out-of-fold FPR; calibrated 0.9136).

## AUC and recall at 1% FPR (threshold per candidate from out-of-fold legitimate scores)

```
                                   auc                   recall_at_1pct_fpr                  
set                      external_test    test train_oof      external_test    test train_oof
candidate                                                                                    
parts                           0.9645  0.9722    0.9599             0.6781  0.6459    0.5554
xgboost                         0.9155  0.9810    0.9693             0.6788  0.7047    0.6501
blend                           0.9077  0.9794    0.9698             0.6760  0.6739    0.6575
xgboost+parts_mean              0.9653  0.9807    0.9710             0.6851  0.7173    0.6381
blend+parts_mean                0.9661  0.9798    0.9700             0.7068  0.7243    0.6301
xgboost+blend+parts_mean        0.9608  0.9814    0.9718             0.6928  0.7061    0.6540
xgboost+parts_stack             0.9420  0.9820    0.9710             0.6949  0.7236    0.6434
blend+parts_stack               0.9487  0.9813    0.9715             0.6935  0.6977    0.6370
u                               0.9762  0.8930    0.8865             0.6529  0.2960    0.3104
```

## At the 1%-FPR threshold

```
               candidate           set  recall   fpr  precision  accuracy
                   parts     train_oof   0.555 0.010      0.982     0.772
                   parts          test   0.620 0.008      0.988     0.806
                   parts external_test   0.348 0.000      1.000     0.674
                 xgboost     train_oof   0.650 0.010      0.985     0.820
                 xgboost          test   0.682 0.007      0.990     0.837
                 xgboost external_test   0.414 0.000      1.000     0.707
                   blend     train_oof   0.658 0.010      0.985     0.824
                   blend          test   0.716 0.015      0.980     0.851
                   blend external_test   0.404 0.000      1.000     0.702
      xgboost+parts_mean     train_oof   0.638 0.010      0.984     0.814
      xgboost+parts_mean          test   0.695 0.008      0.988     0.843
      xgboost+parts_mean external_test   0.409 0.000      1.000     0.705
        blend+parts_mean     train_oof   0.631 0.010      0.984     0.810
        blend+parts_mean          test   0.695 0.008      0.988     0.843
        blend+parts_mean external_test   0.402 0.000      1.000     0.701
xgboost+blend+parts_mean     train_oof   0.655 0.010      0.985     0.822
xgboost+blend+parts_mean          test   0.703 0.010      0.986     0.847
xgboost+blend+parts_mean external_test   0.421 0.000      1.000     0.710
     xgboost+parts_stack     train_oof   0.645 0.010      0.984     0.817
     xgboost+parts_stack          test   0.691 0.008      0.989     0.842
     xgboost+parts_stack external_test   0.406 0.000      1.000     0.703
       blend+parts_stack     train_oof   0.637 0.010      0.984     0.813
       blend+parts_stack          test   0.703 0.011      0.984     0.846
       blend+parts_stack external_test   0.405 0.000      1.000     0.703
                       u     train_oof   0.310 0.010      0.968     0.650
                       u          test   0.303 0.011      0.964     0.646
                       u external_test   0.316 0.000      1.000     0.658
```

## By URL shape

```
               candidate           set           shape    n  phishing   auc  recall   fpr
                   parts     train_oof       path-less 2399       790 0.910   0.208 0.004
                   parts     train_oof with path/query 6252      3540 0.970   0.633 0.014
                   parts          test       path-less  844       273 0.923   0.264 0.002
                   parts          test with path/query 2014      1156 0.982   0.704 0.012
                   parts external_test       path-less 2447      1018 0.952   0.208 0.000
                 xgboost     train_oof       path-less 2399       790 0.935   0.397 0.005
                 xgboost     train_oof with path/query 6252      3540 0.976   0.706 0.013
                 xgboost          test       path-less  844       273 0.956   0.440 0.004
                 xgboost          test with path/query 2014      1156 0.986   0.739 0.009
                 xgboost external_test       path-less 2447      1018 0.882   0.280 0.000
                   blend     train_oof       path-less 2399       790 0.938   0.370 0.002
                   blend     train_oof with path/query 6252      3540 0.976   0.723 0.015
                   blend          test       path-less  844       273 0.953   0.480 0.007
                   blend          test with path/query 2014      1156 0.985   0.772 0.020
                   blend external_test       path-less 2447      1018 0.871   0.258 0.000
      xgboost+parts_mean     train_oof       path-less 2399       790 0.933   0.352 0.004
      xgboost+parts_mean     train_oof with path/query 6252      3540 0.979   0.702 0.014
      xgboost+parts_mean          test       path-less  844       273 0.952   0.403 0.002
      xgboost+parts_mean          test with path/query 2014      1156 0.986   0.764 0.013
      xgboost+parts_mean external_test       path-less 2447      1018 0.952   0.272 0.000
        blend+parts_mean     train_oof       path-less 2399       790 0.932   0.322 0.002
        blend+parts_mean     train_oof with path/query 6252      3540 0.978   0.700 0.015
        blend+parts_mean          test       path-less  844       273 0.948   0.399 0.002
        blend+parts_mean          test with path/query 2014      1156 0.986   0.765 0.013
        blend+parts_mean external_test       path-less 2447      1018 0.953   0.261 0.000
xgboost+blend+parts_mean     train_oof       path-less 2399       790 0.936   0.372 0.003
xgboost+blend+parts_mean     train_oof with path/query 6252      3540 0.979   0.718 0.014
xgboost+blend+parts_mean          test       path-less  844       273 0.954   0.432 0.004
xgboost+blend+parts_mean          test with path/query 2014      1156 0.986   0.767 0.014
xgboost+blend+parts_mean external_test       path-less 2447      1018 0.945   0.283 0.000
     xgboost+parts_stack     train_oof       path-less 2399       790 0.934   0.365 0.004
     xgboost+parts_stack     train_oof with path/query 6252      3540 0.978   0.707 0.014
     xgboost+parts_stack          test       path-less  844       273 0.954   0.410 0.002
     xgboost+parts_stack          test with path/query 2014      1156 0.987   0.758 0.012
     xgboost+parts_stack external_test       path-less 2447      1018 0.919   0.267 0.000
       blend+parts_stack     train_oof       path-less 2399       790 0.937   0.344 0.002
       blend+parts_stack     train_oof with path/query 6252      3540 0.978   0.703 0.015
       blend+parts_stack          test       path-less  844       273 0.954   0.443 0.004
       blend+parts_stack          test with path/query 2014      1156 0.986   0.765 0.016
       blend+parts_stack external_test       path-less 2447      1018 0.928   0.261 0.000
                       u     train_oof       path-less 2399       790 0.900   0.165 0.006
                       u     train_oof with path/query 6252      3540 0.899   0.343 0.013
                       u          test       path-less  844       273 0.902   0.158 0.011
                       u          test with path/query 2014      1156 0.909   0.337 0.012
                       u external_test       path-less 2447      1018 0.980   0.229 0.000
```

## Predictor importance of the parts model (AUC drop when shuffled, mean over folds; top 20)

```
component         feature  auc_drop     sd  native_gain
     host    reg_log_rank    0.0485 0.0110       0.0905
     host             www    0.0359 0.0127       0.4474
      seg         hyphens    0.0118 0.0041       0.1501
     host host_legibility    0.0093 0.0043       0.0200
     host        host_len    0.0093 0.0046       0.0214
     host host_digit_rate    0.0081 0.0030       0.0482
      seg          sw_kit    0.0069 0.0013       0.1864
      seg             len    0.0064 0.0030       0.0227
      seg       sw_phrase    0.0060 0.0011       0.0675
      seg            leet    0.0042 0.0027       0.0543
      seg      legibility    0.0038 0.0015       0.0453
      seg   consonant_run    0.0034 0.0015       0.0232
      seg        ent_norm    0.0027 0.0020       0.0210
     host    is_shortener    0.0027 0.0013       0.0337
     host           https    0.0025 0.0018       0.0346
      seg      digit_rate    0.0024 0.0024       0.0511
     host           n_sub    0.0021 0.0009       0.0364
     host  tld_suspicious    0.0020 0.0013       0.0366
     host  sw_phrase_host    0.0019 0.0012       0.0406
      seg      ext_script    0.0017 0.0006       0.0520
```

## Combiner weights (log-odds)

* host: +0.895
* seg_mean: -0.093
* seg_max: +1.038
* seg_min: +0.448
* qry_mean: +1.316
* qry_max: -0.228
* qry_min: -0.427
* intercept: -1.007

Files: metrics.csv, metrics_by_shape.csv, bootstrap_delta.csv (tools.bootstrap_delta), parts_importance.csv, errors_*.csv (misclassified URLs with all candidate scores), error_analysis.md, scores_*.csv, metrics_by_source.csv (corpus), metrics_summary.csv, model.joblib, config.json, pipeline_logs/.
