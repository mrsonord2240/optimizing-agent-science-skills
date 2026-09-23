#!/usr/bin/env bash
# Phase 2 executable check for the exact ModelTest-NG commands documented by the Skill.
# Inputs are written by phase2_regression.py. Run from /mnt/openscience/audits/bio-alignment-msa-statistics.
set -euo pipefail
source /mnt/openscience/audit-envs/alignment/wsl_env.sh
mkdir -p work_phase2_modeltest
cp data/modeltest_nt.fasta work_phase2_modeltest/alignment_nt.fasta
cp data/modeltest_aa.fasta work_phase2_modeltest/alignment_aa.fasta
pushd work_phase2_modeltest >/dev/null
modeltest-ng -i alignment_nt.fasta -d nt -t ml -p 4 > nt.log 2>&1
grep -Eq 'Best model|K80|TPM|GTR' nt.log
echo MODELTEST_NT_OK
modeltest-ng -i alignment_aa.fasta -d aa -t ml -p 4 > aa.log 2>&1
grep -Eq 'Best model|DAYHOFF|LG|WAG' aa.log
echo MODELTEST_AA_OK
popd >/dev/null
