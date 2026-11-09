#!/bin/bash
# Older two-run chain (superseded by src/pipeline.py, which trains both runs and writes the report):
# train.csv as supplied: v2 = correlation filter |Spearman r| >= 0.75, then v1 = all features; 5-fold host-grouped CV, nine models. Logs go to logs/.
cd "$(dirname "$0")/.." || exit 1
export PYTHONPATH=src
mkdir -p logs
.venv/bin/python -u -m models.run --data train --version v2 --name corr-filter-0.75 --max-corr 0.75 > logs/run_v2.log 2>&1 || { echo FAILED_v2 >> logs/run_v2.log; exit 1; }
.venv/bin/python -u -m models.run --data train --version v1 --name all-features --max-corr 0 > logs/run_v1.log 2>&1 || { echo FAILED_v1 >> logs/run_v1.log; exit 1; }
echo finished > logs/train_chain.done
