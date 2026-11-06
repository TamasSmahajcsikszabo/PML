#!/bin/bash
# train.csv only, as supplied (duplicates and conflicting labels kept): v2 = correlation filter |Spearman r| >= 0.75, then v1 = all features (baseline); 5-fold host-grouped CV, nine models
cd /var/home/tamas/repos/phishing_ML
export PYTHONPATH=src
.venv/bin/python -u -m models.run --data train --version v2 --name corr-filter-0.75 --max-corr 0.75 > run_v2.log 2>&1 || { echo FAILED_v2 >> run_v2.log; exit 1; }
.venv/bin/python -u -m models.run --data train --version v1 --name all-features --max-corr 0 > run_v1.log 2>&1 || { echo FAILED_v1 >> run_v1.log; exit 1; }
echo finished > train_chain.done
