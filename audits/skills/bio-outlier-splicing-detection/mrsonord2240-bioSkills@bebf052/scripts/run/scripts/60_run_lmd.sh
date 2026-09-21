#!/bin/bash
# SKILL.md LeafcutterMD bash block (blocks/03_bash.sh) run verbatim in lmd/, except the one substitution
# `python leafcutter_cluster_regtools.py` -> wrapper of the same script on PATH (the script lives in the leafcutter repo).
export PATH=/mnt/openscience/audit-envs/alternative-splicing/tools/bin:$PATH
export PYTHONDONTWRITEBYTECODE=1
cd /mnt/openscience/audits/bio-outlier-splicing-detection/run/lmd
rm -f *.junc juncfiles.txt leafcutter_* patient_outlier_*
sed 's#python leafcutter_cluster_regtools.py#leafcutter_cluster_regtools.py#' ../blocks/03_bash.sh > ../blocks/03_bash_lmd_run.sh
cat ../blocks/03_bash_lmd_run.sh
bash ../blocks/03_bash_lmd_run.sh
ls -la patient_outlier_* leafcutter_perind*
