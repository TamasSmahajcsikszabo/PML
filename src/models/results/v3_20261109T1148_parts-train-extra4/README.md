# Run v3_20261109T1148_parts-train-extra4

Parts model on train+extra (43255 URLs), combined with the parent run v2_20261109T1131_corr-filter-0.75-train+extra. 5-fold host-grouped CV (same folds as the parent); test.csv / external_test.csv scored once.
Deployed candidate: **xgboost+blend+parts_mean** (threshold 0.8947 on the raw mean = 1% out-of-fold FPR; calibrated 0.9436).

## AUC and recall at 1% FPR (threshold per candidate from out-of-fold legitimate scores)

```
                                   auc                   recall_at_1pct_fpr                  
set                      external_test    test train_oof      external_test    test train_oof
candidate                                                                                    
parts                           0.9917  0.9653    0.9666             0.9671  0.6795    0.6058
xgboost                         0.9631  0.9803    0.9806             0.6746  0.7054    0.7372
blend                           0.9758  0.9800    0.9816             0.6977  0.7292    0.7402
xgboost+parts_mean              0.9872  0.9784    0.9792             0.7978  0.7362    0.6827
blend+parts_mean                0.9899  0.9783    0.9797             0.8307  0.7320    0.7003
xgboost+blend+parts_mean        0.9853  0.9801    0.9812             0.7649  0.7467    0.7138
xgboost+parts_stack             0.9769  0.9805    0.9811             0.7117  0.7348    0.7316
blend+parts_stack               0.9815  0.9806    0.9819             0.7264  0.7453    0.7370
```

## At the 1%-FPR threshold

```
               candidate           set  recall   fpr  precision  accuracy
                   parts     train_oof   0.606 0.010      0.984     0.798
                   parts          test   0.603 0.003      0.995     0.800
                   parts external_test   0.374 0.000      1.000     0.687
                 xgboost     train_oof   0.737 0.010      0.987     0.864
                 xgboost          test   0.707 0.010      0.985     0.848
                 xgboost external_test   0.507 0.002      0.996     0.752
                   blend     train_oof   0.740 0.010      0.987     0.865
                   blend          test   0.728 0.010      0.987     0.859
                   blend external_test   0.527 0.001      0.997     0.763
      xgboost+parts_mean     train_oof   0.683 0.010      0.986     0.836
      xgboost+parts_mean          test   0.672 0.006      0.991     0.833
      xgboost+parts_mean external_test   0.475 0.001      0.999     0.737
        blend+parts_mean     train_oof   0.700 0.010      0.986     0.845
        blend+parts_mean          test   0.691 0.005      0.993     0.843
        blend+parts_mean external_test   0.490 0.001      0.999     0.745
xgboost+blend+parts_mean     train_oof   0.714 0.010      0.986     0.852
xgboost+blend+parts_mean          test   0.701 0.006      0.992     0.848
xgboost+blend+parts_mean external_test   0.509 0.001      0.999     0.754
     xgboost+parts_stack     train_oof   0.732 0.010      0.986     0.861
     xgboost+parts_stack          test   0.703 0.007      0.990     0.848
     xgboost+parts_stack external_test   0.502 0.002      0.996     0.750
       blend+parts_stack     train_oof   0.737 0.010      0.987     0.863
       blend+parts_stack          test   0.728 0.009      0.988     0.860
       blend+parts_stack external_test   0.510 0.001      0.997     0.754
```

## By URL shape

```
               candidate           set           shape     n  phishing   auc  recall   fpr
                   parts     train_oof       path-less  8928      4478 0.907   0.319 0.009
                   parts     train_oof with path/query 34327     17154 0.976   0.681 0.010
                   parts          test       path-less   844       273 0.906   0.275 0.002
                   parts          test with path/query  2014      1156 0.983   0.681 0.003
                   parts external_test       path-less  2447      1018 0.991   0.264 0.000
                 xgboost     train_oof       path-less  8928      4478 0.959   0.638 0.016
                 xgboost     train_oof with path/query 34327     17154 0.985   0.763 0.008
                 xgboost          test       path-less   844       273 0.953   0.520 0.012
                 xgboost          test with path/query  2014      1156 0.988   0.751 0.009
                 xgboost external_test       path-less  2447      1018 0.955   0.420 0.002
                   blend     train_oof       path-less  8928      4478 0.959   0.654 0.018
                   blend     train_oof with path/query 34327     17154 0.986   0.763 0.008
                   blend          test       path-less   844       273 0.953   0.637 0.016
                   blend          test with path/query  2014      1156 0.988   0.750 0.006
                   blend external_test       path-less  2447      1018 0.971   0.454 0.001
      xgboost+parts_mean     train_oof       path-less  8928      4478 0.947   0.444 0.018
      xgboost+parts_mean     train_oof with path/query 34327     17154 0.985   0.745 0.008
      xgboost+parts_mean          test       path-less   844       273 0.945   0.403 0.007
      xgboost+parts_mean          test with path/query  2014      1156 0.988   0.736 0.006
      xgboost+parts_mean external_test       path-less  2447      1018 0.985   0.378 0.001
        blend+parts_mean     train_oof       path-less  8928      4478 0.947   0.481 0.018
        blend+parts_mean     train_oof with path/query 34327     17154 0.985   0.758 0.008
        blend+parts_mean          test       path-less   844       273 0.944   0.495 0.007
        blend+parts_mean          test with path/query  2014      1156 0.988   0.738 0.003
        blend+parts_mean external_test       path-less  2447      1018 0.989   0.403 0.001
xgboost+blend+parts_mean     train_oof       path-less  8928      4478 0.953   0.528 0.018
xgboost+blend+parts_mean     train_oof with path/query 34327     17154 0.986   0.763 0.008
xgboost+blend+parts_mean          test       path-less   844       273 0.950   0.509 0.007
xgboost+blend+parts_mean          test with path/query  2014      1156 0.989   0.747 0.005
xgboost+blend+parts_mean external_test       path-less  2447      1018 0.983   0.425 0.001
     xgboost+parts_stack     train_oof       path-less  8928      4478 0.956   0.606 0.018
     xgboost+parts_stack     train_oof with path/query 34327     17154 0.986   0.764 0.008
     xgboost+parts_stack          test       path-less   844       273 0.952   0.495 0.007
     xgboost+parts_stack          test with path/query  2014      1156 0.988   0.753 0.007
     xgboost+parts_stack external_test       path-less  2447      1018 0.972   0.413 0.002
       blend+parts_stack     train_oof       path-less  8928      4478 0.957   0.621 0.018
       blend+parts_stack     train_oof with path/query 34327     17154 0.986   0.767 0.008
       blend+parts_stack          test       path-less   844       273 0.952   0.623 0.014
       blend+parts_stack          test with path/query  2014      1156 0.989   0.753 0.006
       blend+parts_stack external_test       path-less  2447      1018 0.978   0.431 0.001
```

## Predictor importance of the parts model (AUC drop when shuffled, mean over folds; top 20)

```
component         feature  auc_drop     sd  native_gain
     host    reg_log_rank    0.0567 0.0023       0.1334
     host           https    0.0149 0.0021       0.0804
     host             www    0.0146 0.0015       0.1363
      seg       sw_phrase    0.0118 0.0015       0.1131
     host        host_len    0.0112 0.0011       0.0321
      seg             len    0.0106 0.0019       0.0211
      seg         hyphens    0.0100 0.0015       0.1244
     host host_legibility    0.0082 0.0019       0.0323
      seg          sw_kit    0.0080 0.0014       0.1768
      seg            leet    0.0055 0.0016       0.0414
     host host_digit_rate    0.0051 0.0014       0.0759
     host           n_sub    0.0044 0.0014       0.0809
      seg      legibility    0.0038 0.0015       0.0228
     host  tld_suspicious    0.0032 0.0005       0.0831
      seg      digit_rate    0.0030 0.0018       0.0815
      seg        ent_norm    0.0030 0.0003       0.0123
      seg   consonant_run    0.0029 0.0018       0.0151
      seg        brand_in    0.0026 0.0009       0.0826
      seg            dots    0.0023 0.0009       0.0291
      seg      alpha_rate    0.0018 0.0013       0.0208
```

## Combiner weights (log-odds)

* host: +0.901
* seg_mean: -0.555
* seg_max: +1.228
* seg_min: +0.876
* qry_mean: +0.476
* qry_max: +0.201
* qry_min: +0.831
* intercept: -0.594

Files: metrics.csv, metrics_by_shape.csv, parts_importance.csv, errors_*.csv (misclassified URLs with all candidate scores), error_analysis.md, scores_*.csv, metrics_by_source.csv (corpus), metrics_summary.csv, model.joblib, config.json, pipeline_logs/.
