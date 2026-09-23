#!/usr/bin/env bash
# Fresh final-pass execution of the shipped fusion_twas.sh copied from audited tip.
set -euo pipefail
AUDIT='F:/OpenScience/audits/bio-causal-genomics-transcriptome-wide-association'
SCRATCH='F:/OpenScience/audit-scratch/twas-final-pass-20260923'
SRC="$AUDIT/run/skill-src/scripts/fusion_twas.sh"
DATA="$AUDIT/data/fusion"
cd "$SCRATCH/fusion_patched"
RSCRIPT='F:/OpenScience/audit-envs/mendelian-randomization-analyst/r.sh' \
  "$SRC" "$DATA/gwas.sumstats" "$DATA/weights.pos" "$DATA/wgt" "$DATA/ld/EUR." \
  "$DATA/finalpass" '1'
test -s "$DATA/finalpass_chr1.dat"
test -s "$DATA/finalpass_all.dat"
test -s "$DATA/finalpass_joint_chr1.dat.joint_included.dat"
test -s "$DATA/finalpass_joint_chr1.dat.joint_dropped.dat"
awk -F'\t' 'NR==1 || $3 == "GENE1" || $3 == "GENE2"' "$DATA/finalpass_chr1.dat"
cat "$DATA/finalpass_joint_chr1.dat.joint_included.dat"
cat "$DATA/finalpass_joint_chr1.dat.joint_dropped.dat"
