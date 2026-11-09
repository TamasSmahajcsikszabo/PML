# Run v3_20261109T0956_visitor-platform

Parts model on train (8651 URLs), combined with the parent run v2_20261109T0949_corr-filter-0.75. 5-fold host-grouped CV (same folds as the parent); test.csv / external_test.csv scored once.
Deployed candidate: **xgboost+blend+parts_mean** (threshold 0.8463 on the raw mean = 1% out-of-fold FPR; calibrated 0.9355).

## AUC and recall at 1% FPR (threshold per candidate from out-of-fold legitimate scores)

```
                                   auc                   recall_at_1pct_fpr                  
set                      external_test    test train_oof      external_test    test train_oof
candidate                                                                                    
parts                           0.9642  0.9726    0.9596             0.6760  0.6445    0.5561
xgboost                         0.9129  0.9809    0.9690             0.6753  0.6914    0.6490
blend                           0.9012  0.9807    0.9695             0.6753  0.6984    0.6425
xgboost+parts_mean              0.9647  0.9808    0.9705             0.6907  0.7061    0.6383
blend+parts_mean                0.9624  0.9808    0.9699             0.6886  0.7152    0.6388
xgboost+blend+parts_mean        0.9568  0.9819    0.9714             0.6851  0.7019    0.6522
xgboost+parts_stack             0.9393  0.9821    0.9705             0.6865  0.7152    0.6316
blend+parts_stack               0.9386  0.9824    0.9711             0.6893  0.7236    0.6473
u                               0.9762  0.8930    0.8865             0.6529  0.2960    0.3104
```

## At the 1%-FPR threshold

```
               candidate           set  recall   fpr  precision  accuracy
                   parts     train_oof   0.556 0.010      0.982     0.773
                   parts          test   0.628 0.008      0.987     0.810
                   parts external_test   0.342 0.000      1.000     0.671
                 xgboost     train_oof   0.649 0.010      0.985     0.819
                 xgboost          test   0.670 0.008      0.988     0.831
                 xgboost external_test   0.408 0.000      1.000     0.704
                   blend     train_oof   0.643 0.010      0.984     0.816
                   blend          test   0.716 0.011      0.985     0.852
                   blend external_test   0.402 0.000      1.000     0.701
      xgboost+parts_mean     train_oof   0.639 0.010      0.984     0.814
      xgboost+parts_mean          test   0.697 0.009      0.987     0.844
      xgboost+parts_mean external_test   0.411 0.000      1.000     0.705
        blend+parts_mean     train_oof   0.640 0.010      0.984     0.815
        blend+parts_mean          test   0.715 0.009      0.987     0.853
        blend+parts_mean external_test   0.414 0.000      1.000     0.707
xgboost+blend+parts_mean     train_oof   0.653 0.010      0.985     0.821
xgboost+blend+parts_mean          test   0.706 0.010      0.985     0.848
xgboost+blend+parts_mean external_test   0.418 0.000      1.000     0.709
     xgboost+parts_stack     train_oof   0.633 0.010      0.984     0.811
     xgboost+parts_stack          test   0.676 0.006      0.992     0.835
     xgboost+parts_stack external_test   0.396 0.000      1.000     0.698
       blend+parts_stack     train_oof   0.648 0.010      0.985     0.819
       blend+parts_stack          test   0.716 0.010      0.986     0.853
       blend+parts_stack external_test   0.409 0.000      1.000     0.705
                       u     train_oof   0.310 0.010      0.968     0.650
                       u          test   0.303 0.011      0.964     0.646
                       u external_test   0.316 0.000      1.000     0.658
```

## By URL shape

```
               candidate           set           shape    n  phishing   auc  recall   fpr
                   parts     train_oof       path-less 2399       790 0.910   0.204 0.003
                   parts     train_oof with path/query 6252      3540 0.970   0.635 0.014
                   parts          test       path-less  844       273 0.922   0.275 0.002
                   parts          test with path/query 2014      1156 0.983   0.712 0.013
                   parts external_test       path-less 2447      1018 0.952   0.194 0.000
                 xgboost     train_oof       path-less 2399       790 0.935   0.395 0.005
                 xgboost     train_oof with path/query 6252      3540 0.976   0.706 0.013
                 xgboost          test       path-less  844       273 0.956   0.436 0.004
                 xgboost          test with path/query 2014      1156 0.985   0.725 0.012
                 xgboost external_test       path-less 2447      1018 0.879   0.274 0.000
                   blend     train_oof       path-less 2399       790 0.936   0.385 0.005
                   blend     train_oof with path/query 6252      3540 0.976   0.701 0.013
                   blend          test       path-less  844       273 0.955   0.513 0.007
                   blend          test with path/query 2014      1156 0.986   0.764 0.014
                   blend external_test       path-less 2447      1018 0.862   0.259 0.000
      xgboost+parts_mean     train_oof       path-less 2399       790 0.933   0.348 0.004
      xgboost+parts_mean     train_oof with path/query 6252      3540 0.978   0.704 0.014
      xgboost+parts_mean          test       path-less  844       273 0.951   0.414 0.002
      xgboost+parts_mean          test with path/query 2014      1156 0.986   0.764 0.014
      xgboost+parts_mean external_test       path-less 2447      1018 0.951   0.272 0.000
        blend+parts_mean     train_oof       path-less 2399       790 0.932   0.341 0.002
        blend+parts_mean     train_oof with path/query 6252      3540 0.977   0.707 0.015
        blend+parts_mean          test       path-less  844       273 0.950   0.443 0.002
        blend+parts_mean          test with path/query 2014      1156 0.987   0.779 0.014
        blend+parts_mean external_test       path-less 2447      1018 0.948   0.274 0.000
xgboost+blend+parts_mean     train_oof       path-less 2399       790 0.936   0.368 0.004
xgboost+blend+parts_mean     train_oof with path/query 6252      3540 0.978   0.716 0.014
xgboost+blend+parts_mean          test       path-less  844       273 0.955   0.440 0.004
xgboost+blend+parts_mean          test with path/query 2014      1156 0.987   0.769 0.015
xgboost+blend+parts_mean external_test       path-less 2447      1018 0.940   0.281 0.000
     xgboost+parts_stack     train_oof       path-less 2399       790 0.935   0.352 0.003
     xgboost+parts_stack     train_oof with path/query 6252      3540 0.978   0.695 0.014
     xgboost+parts_stack          test       path-less  844       273 0.955   0.407 0.000
     xgboost+parts_stack          test with path/query 2014      1156 0.987   0.740 0.009
     xgboost+parts_stack external_test       path-less 2447      1018 0.916   0.257 0.000
       blend+parts_stack     train_oof       path-less 2399       790 0.936   0.363 0.003
       blend+parts_stack     train_oof with path/query 6252      3540 0.978   0.711 0.014
       blend+parts_stack          test       path-less  844       273 0.957   0.451 0.004
       blend+parts_stack          test with path/query 2014      1156 0.987   0.779 0.014
       blend+parts_stack external_test       path-less 2447      1018 0.914   0.267 0.000
                       u     train_oof       path-less 2399       790 0.900   0.165 0.006
                       u     train_oof with path/query 6252      3540 0.899   0.343 0.013
                       u          test       path-less  844       273 0.902   0.158 0.011
                       u          test with path/query 2014      1156 0.909   0.337 0.012
                       u external_test       path-less 2447      1018 0.980   0.229 0.000
```

## Predictor importance of the parts model (AUC drop when shuffled, mean over folds; top 20)

```
component         feature  auc_drop     sd  native_gain
     host    reg_log_rank    0.0473 0.0104       0.0949
     host             www    0.0355 0.0136       0.4087
      seg         hyphens    0.0118 0.0044       0.1501
     host        host_len    0.0093 0.0055       0.0220
     host host_legibility    0.0092 0.0045       0.0210
     host host_digit_rate    0.0085 0.0030       0.0560
      seg          sw_kit    0.0069 0.0013       0.1864
      seg             len    0.0064 0.0029       0.0227
      seg       sw_phrase    0.0062 0.0013       0.0675
      seg            leet    0.0043 0.0029       0.0543
      seg      legibility    0.0040 0.0016       0.0453
      seg   consonant_run    0.0037 0.0018       0.0232
      seg        ent_norm    0.0029 0.0020       0.0210
     host           https    0.0027 0.0027       0.0311
     host    is_shortener    0.0026 0.0013       0.0367
      seg      digit_rate    0.0024 0.0025       0.0511
     host           n_sub    0.0023 0.0008       0.0435
     host  tld_suspicious    0.0019 0.0010       0.0373
     host  sw_phrase_host    0.0018 0.0013       0.0383
      seg      ext_script    0.0017 0.0006       0.0520
```

## Combiner weights (log-odds)

* host: +0.886
* seg_mean: -0.131
* seg_max: +1.063
* seg_min: +0.466
* qry_mean: +1.189
* qry_max: -0.185
* qry_min: -0.342
* intercept: -0.993

Files: metrics.csv, metrics_by_shape.csv, bootstrap_delta.csv (tools.bootstrap_delta), parts_importance.csv, errors_*.csv (misclassified URLs with all candidate scores), error_analysis.md, scores_*.csv, metrics_by_source.csv (corpus), metrics_summary.csv, model.joblib, config.json, pipeline_logs/.
