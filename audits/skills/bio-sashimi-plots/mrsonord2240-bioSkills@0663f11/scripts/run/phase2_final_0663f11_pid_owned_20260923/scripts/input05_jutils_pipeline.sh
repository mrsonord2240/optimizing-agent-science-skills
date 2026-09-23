#!/usr/bin/env bash
set -euo pipefail
R=/mnt/openscience/audits/bio-sashimi-plots/run/phase2_final_0663f11_pid_owned_20260923
AS=/mnt/openscience/audit-envs/alternative-splicing
S=$R/source_copy/scripts/jutils_pipeline.sh
W=$R/outputs/input05
mkdir -p "$W/rm"
cp /mnt/openscience/as-sashimi-scratch/p2/sc/ju/rm/*.MATS.J*.txt "$W/rm/"
cp /mnt/openscience/as-sashimi-scratch/p2/sc/ju/meta.tsv "$W/meta.tsv"
cp /mnt/openscience/as-sashimi-scratch/p2/sc/ju/bams.tsv "$W/bams.tsv"
asenv as-viz-gg34 bash "$S" "$AS/tools/src/Jutils" "$W/rm" "$W/meta.tsv" "$W/bams.tsv" "$AS/public-data/rnasplice/reference/genes_chrX.gtf" X:69508604-69510295 "$W/out"
test -s "$W/out/jutils_out/rmats_JC_results.tsv"
test -s "$W/out/sh/sashimi.pdf"
test -s "$W/out/vn/venn_diagram.png"
echo 'ASSERT jutils_convert_heatmap_sashimi_venn'
