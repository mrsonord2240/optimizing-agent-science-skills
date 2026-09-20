#!/bin/bash
# Reproduce the audit (order matters). Run through F:/OpenScience/audit-envs/alignment-files/wsl_run.sh 'bash /mnt/openscience/audits/bio-alignment-validation/run/run_all.sh'
R=/mnt/openscience/audits/bio-alignment-validation/run
PD=/mnt/openscience/audit-envs/alignment-files/public-data
export PYTHONIOENCODING=utf-8 MPLBACKEND=Agg
bash $R/scripts/probe_help.sh > $R/out/probe_help.txt 2>&1
bash $R/scripts/probe_picard.sh > $R/out/probe_picard.txt 2>&1
python $R/scripts/extract_snippets.py
python $R/scripts/make_fixtures.py $PD $R/data            # SYNTHETIC planted-defect BAMs
bash $R/scripts/make_refs.sh                              # SYNTHETIC reference variants
python $R/scripts/matrix.py > $R/out/matrix_stdout.txt 2>&1
python $R/scripts/matrix_idx.py > $R/out/matrix_idx_stdout.txt 2>&1   # creates run/data/idx (delete afterwards)
bash $R/scripts/matrix_details.sh > $R/out/matrix_details.txt 2>&1
bash $R/scripts/test_snippets.sh > $R/out/test_snippets.txt 2>&1
bash $R/scripts/test_contam.sh > $R/out/test_contam.txt 2>&1
bash $R/scripts/test_validators.sh > $R/out/test_validators.txt 2>&1
python $R/scripts/test_py_snips.py > $R/out/test_py_snips.txt 2>&1
bash $R/scripts/test_plotbamstats2.sh >> $R/out/test_py_snips.txt 2>&1
bash $R/scripts/test_ignore.sh > $R/out/test_ignore.txt 2>&1
bash $R/scripts/test_misc.sh > $R/out/test_misc.txt 2>&1
# then (Windows python): summarize_matrix.py, build_report.py
