#!/bin/bash
R=/mnt/openscience/audits/bio-alignment-validation/run
PD=/mnt/openscience/audit-envs/alignment-files/public-data
export PYTHONIOENCODING=utf-8
mkdir -p $R/data/new
python $R/scripts/make_new_fixtures.py $PD $R/data/new
