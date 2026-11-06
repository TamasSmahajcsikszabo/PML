# Run v3_20261106T1204_parts-corpus

Parts model on corpus (66187 URLs), combined with the parent run 20261104T1518_nine-models. 5-fold host-grouped CV (same folds as the parent); test.csv / external_test.csv scored once.
Deployed candidate: **xgboost+blend+parts_mean** (threshold 0.8284 on the raw mean = 1% out-of-fold FPR; calibrated 0.9220).

## AUC and recall at 1% FPR (threshold per candidate from out-of-fold legitimate scores)

```
                                   auc                   recall_at_1pct_fpr                  
set                      external_test    test train_oof      external_test    test train_oof
candidate                                                                                    
parts                           0.9915  0.9610    0.9700             0.9657  0.6753    0.6239
xgboost                         0.9840  0.9740    0.9821             0.7201  0.6963    0.7418
blend                           0.9858  0.9775    0.9837             0.7334  0.7124    0.7721
xgboost+parts_mean              0.9918  0.9721    0.9805             0.8852  0.6998    0.7193
blend+parts_mean                0.9924  0.9746    0.9818             0.8845  0.7208    0.7309
xgboost+blend+parts_mean        0.9913  0.9754    0.9828             0.8244  0.7082    0.7477
xgboost+parts_stack             0.9871  0.9744    0.9822             0.7439  0.6935    0.7408
blend+parts_stack               0.9884  0.9778    0.9839             0.7887  0.7173    0.7676
```

## At the 1%-FPR threshold

```
               candidate           set  recall   fpr  precision  accuracy
                   parts     train_oof   0.624 0.010      0.980     0.830
                   parts          test   0.621 0.003      0.996     0.809
                   parts external_test   0.425 0.001      0.998     0.712
                 xgboost     train_oof   0.742 0.010      0.983     0.882
                 xgboost          test   0.724 0.015      0.980     0.855
                 xgboost external_test   0.519 0.001      0.999     0.759
                   blend     train_oof   0.772 0.010      0.984     0.895
                   blend          test   0.768 0.018      0.977     0.875
                   blend external_test   0.570 0.001      0.998     0.784
      xgboost+parts_mean     train_oof   0.720 0.010      0.982     0.872
      xgboost+parts_mean          test   0.707 0.010      0.985     0.848
      xgboost+parts_mean external_test   0.528 0.001      0.999     0.763
        blend+parts_mean     train_oof   0.731 0.010      0.983     0.877
        blend+parts_mean          test   0.728 0.010      0.986     0.859
        blend+parts_mean external_test   0.542 0.001      0.999     0.770
xgboost+blend+parts_mean     train_oof   0.748 0.010      0.983     0.884
xgboost+blend+parts_mean          test   0.736 0.015      0.980     0.861
xgboost+blend+parts_mean external_test   0.540 0.001      0.999     0.770
     xgboost+parts_stack     train_oof   0.741 0.010      0.983     0.881
     xgboost+parts_stack          test   0.717 0.012      0.984     0.853
     xgboost+parts_stack external_test   0.514 0.001      0.999     0.756
       blend+parts_stack     train_oof   0.768 0.010      0.983     0.893
       blend+parts_stack          test   0.757 0.017      0.978     0.870
       blend+parts_stack external_test   0.563 0.001      0.998     0.781
```

## By URL shape

```
               candidate           set           shape     n  phishing   auc  recall   fpr
                   parts     train_oof       path-less 13119      6045 0.916   0.352 0.014
                   parts     train_oof with path/query 53068     22886 0.979   0.696 0.009
                   parts          test       path-less   844       273 0.900   0.341 0.000
                   parts          test with path/query  2014      1156 0.983   0.687 0.005
                   parts external_test       path-less  2447      1018 0.994   0.331 0.001
                 xgboost     train_oof       path-less 13119      6045 0.961   0.637 0.016
                 xgboost     train_oof with path/query 53068     22886 0.986   0.769 0.009
                 xgboost          test       path-less   844       273 0.944   0.608 0.018
                 xgboost          test with path/query  2014      1156 0.984   0.752 0.013
                 xgboost external_test       path-less  2447      1018 0.981   0.439 0.001
                   blend     train_oof       path-less 13119      6045 0.967   0.705 0.016
                   blend     train_oof with path/query 53068     22886 0.987   0.790 0.009
                   blend          test       path-less   844       273 0.951   0.678 0.025
                   blend          test with path/query  2014      1156 0.986   0.789 0.014
                   blend external_test       path-less  2447      1018 0.985   0.496 0.001
      xgboost+parts_mean     train_oof       path-less 13119      6045 0.948   0.544 0.018
      xgboost+parts_mean     train_oof with path/query 53068     22886 0.986   0.766 0.008
      xgboost+parts_mean          test       path-less   844       273 0.931   0.568 0.012
      xgboost+parts_mean          test with path/query  2014      1156 0.986   0.740 0.009
      xgboost+parts_mean external_test       path-less  2447      1018 0.992   0.441 0.001
        blend+parts_mean     train_oof       path-less 13119      6045 0.954   0.580 0.020
        blend+parts_mean     train_oof with path/query 53068     22886 0.987   0.771 0.008
        blend+parts_mean          test       path-less   844       273 0.937   0.612 0.016
        blend+parts_mean          test with path/query  2014      1156 0.987   0.755 0.007
        blend+parts_mean external_test       path-less  2447      1018 0.993   0.463 0.001
xgboost+blend+parts_mean     train_oof       path-less 13119      6045 0.957   0.626 0.019
xgboost+blend+parts_mean     train_oof with path/query 53068     22886 0.987   0.781 0.008
xgboost+blend+parts_mean          test       path-less   844       273 0.941   0.630 0.019
xgboost+blend+parts_mean          test with path/query  2014      1156 0.987   0.761 0.012
xgboost+blend+parts_mean external_test       path-less  2447      1018 0.991   0.458 0.001
     xgboost+parts_stack     train_oof       path-less 13119      6045 0.958   0.622 0.018
     xgboost+parts_stack     train_oof with path/query 53068     22886 0.986   0.773 0.008
     xgboost+parts_stack          test       path-less   844       273 0.942   0.601 0.014
     xgboost+parts_stack          test with path/query  2014      1156 0.985   0.745 0.010
     xgboost+parts_stack external_test       path-less  2447      1018 0.986   0.432 0.001
       blend+parts_stack     train_oof       path-less 13119      6045 0.965   0.688 0.018
       blend+parts_stack     train_oof with path/query 53068     22886 0.987   0.789 0.008
       blend+parts_stack          test       path-less   844       273 0.950   0.663 0.023
       blend+parts_stack          test with path/query  2014      1156 0.987   0.779 0.013
       blend+parts_stack external_test       path-less  2447      1018 0.988   0.488 0.001
```

## Predictor importance of the parts model (AUC drop when shuffled, mean over folds; top 20)

```
component         feature  auc_drop     sd  native_gain
     host    reg_log_rank    0.0539 0.0049       0.1208
     host           https    0.0162 0.0013       0.0905
     host             www    0.0137 0.0018       0.1329
      seg             len    0.0133 0.0018       0.0194
      seg       sw_phrase    0.0106 0.0011       0.1303
     host        host_len    0.0097 0.0025       0.0338
      seg         hyphens    0.0091 0.0013       0.1234
     host host_legibility    0.0080 0.0008       0.0376
      seg          sw_kit    0.0070 0.0008       0.1799
      seg            leet    0.0055 0.0015       0.0416
     host           n_sub    0.0046 0.0019       0.0594
      seg      alpha_rate    0.0044 0.0014       0.0476
     host host_digit_rate    0.0042 0.0019       0.0876
      seg      legibility    0.0040 0.0013       0.0256
      seg            dots    0.0037 0.0009       0.0372
      seg   consonant_run    0.0033 0.0015       0.0159
      seg        brand_in    0.0028 0.0006       0.0864
      seg        ent_norm    0.0027 0.0005       0.0120
     host  tld_suspicious    0.0026 0.0003       0.0949
     host         reg_len    0.0015 0.0002       0.0085
```

## Combiner weights (log-odds)

* host: +0.920
* seg_mean: -0.531
* seg_max: +1.282
* seg_min: +0.820
* qry_mean: +0.576
* qry_max: +0.360
* qry_min: +0.844
* intercept: -0.371

Files: metrics.csv, metrics_by_shape.csv, bootstrap_delta.csv (tools.bootstrap_delta), parts_importance.csv, errors_*.csv (misclassified URLs with all candidate scores), error_analysis.md, scores_*.csv, metrics_by_source.csv (corpus), metrics_summary.csv, model.joblib, config.json, pipeline_logs/.
