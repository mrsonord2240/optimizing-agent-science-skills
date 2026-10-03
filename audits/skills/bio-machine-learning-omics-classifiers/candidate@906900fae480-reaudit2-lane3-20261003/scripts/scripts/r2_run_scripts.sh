#!/bin/bash
S=/f/OpenScience/wt/ml-lane3-normalize/skills/bio-machine-learning-omics-classifiers
PY=/f/OpenScience/audit-envs/cheminformatics-hit-triage-analyst/Scripts/python.exe
EV=/f/OpenScience/audits/bio-machine-learning-omics-classifiers/reaudit2-lane3-20261003/evidence
export PYTHONDONTWRITEBYTECODE=1
cd $S
for s in batch_checks calibration_check logistic_regression rf_xgboost_classifier; do
  t0=$SECONDS; $PY -W error::FutureWarning scripts/$s.py > $EV/script_$s.log 2>&1; echo "rc=$? wall=$((SECONDS-t0))s" >> $EV/script_$s.log
done
echo done > $EV/SCRIPTS_DONE
