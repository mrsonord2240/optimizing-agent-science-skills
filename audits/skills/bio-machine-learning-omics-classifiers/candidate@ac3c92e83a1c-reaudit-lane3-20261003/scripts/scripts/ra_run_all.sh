#!/bin/bash
# Run every shipped script and every SKILL.md block as instructed (cwd = Skill dir), FutureWarning as error.
PY=/f/OpenScience/audit-envs/cheminformatics-hit-triage-analyst/Scripts/python.exe
SK=/f/OpenScience/wt/ml-lane3-normalize/skills/bio-machine-learning-omics-classifiers
R=/f/OpenScience/audits/bio-machine-learning-omics-classifiers/reaudit-lane3-20261003/evidence
D=/f/OpenScience/audit-envs/cheminformatics-hit-triage-analyst/derived/omics-classifiers-claims
export PYTHONDONTWRITEBYTECODE=1
cd $SK
for s in batch_checks logistic_regression rf_xgboost_classifier calibration_check; do T0=$SECONDS
  timeout 900 $PY -W error::FutureWarning scripts/$s.py > $R/script_$s.out 2> $R/script_$s.err; echo "$s rc=$? wall=$((SECONDS-T0))s" >> $R/script_rc.txt
done
timeout 900 $PY -W error::FutureWarning $D/run_snippets.py "$(pwd -W)" golub > $R/snippets_golub.out 2>&1; echo "snip golub rc=$?" >> $R/script_rc.txt
timeout 900 $PY -W error::FutureWarning $D/run_snippets.py "$(pwd -W)" synthetic > $R/snippets_synth.out 2>&1; echo "snip synth rc=$?" >> $R/script_rc.txt
