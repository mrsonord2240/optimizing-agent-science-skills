#!/bin/bash
# Regression fixtures: the first auditor's generator (make_fixtures.py, make_refs.sh), re-run unchanged.
R=/mnt/openscience/audits/bio-alignment-validation/run
PD=/mnt/openscience/audit-envs/alignment-files/public-data
export PYTHONIOENCODING=utf-8 MPLBACKEND=Agg
python $R/scripts/make_fixtures.py $PD $R/data
bash $R/scripts/make_refs.sh
python $R/scripts/extract_snippets.py
