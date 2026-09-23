#!/usr/bin/env bash
set -euo pipefail
R=/mnt/openscience/audits/bio-sashimi-plots/run/phase2_final_0663f11_pid_owned_20260923
P=/mnt/openscience/audit-envs/alternative-splicing/public-data/planted
LC=/mnt/openscience/audit-envs/alternative-splicing/tools/src/leafcutter
S=$R/source_copy/scripts/leafviz_run.sh
W=$R/outputs/input04
mkdir -p "$W"
cp /mnt/openscience/as-sashimi-scratch/p2/sc/lf/leafcutter_perind_numers.counts.gz "$W/counts.gz"
cp /mnt/openscience/as-sashimi-scratch/p2/sc/lf/ds_results_cluster_significance.txt "$W/ds_cluster_significance.txt"
cp /mnt/openscience/as-sashimi-scratch/p2/sc/lf/ds_results_effect_sizes.txt "$W/ds_effect_sizes.txt"
printf 'G1_rep1\tG1\nG1_rep2\tG1\nG1_rep3\tG1\nG2_rep1\tG2\nG2_rep2\tG2\nG2_rep3\tG2\n' > "$W/groups.txt"
LAUNCH=0 asenv as-rleaf bash "$S" "$LC" "$P/planted.gtf" "$W/groups.txt" "$W/counts.gz" "$W/ds" "$W/leafviz.RData"
test -s "$W/leafviz.RData"
test -s "$W/annot_all_exons.txt.gz"
echo 'ASSERT leafviz_rdata_and_annotation'
