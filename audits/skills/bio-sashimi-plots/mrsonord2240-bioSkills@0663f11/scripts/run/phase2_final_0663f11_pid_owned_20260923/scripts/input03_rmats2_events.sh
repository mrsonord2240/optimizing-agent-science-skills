#!/usr/bin/env bash
set -euo pipefail
R=/mnt/openscience/audits/bio-sashimi-plots/run/phase2_final_0663f11_pid_owned_20260923
P=/mnt/openscience/audit-envs/alternative-splicing/public-data/planted
S=$R/source_copy/scripts/rmats2sashimiplot_events.sh
E=/mnt/openscience/audits/bio-sashimi-plots/run/data/rmats_planted/SE.MATS.JC.txt
W=$R/outputs/input03_happy
mkdir -p "$W"
bash "$S" "$E" SE "$W/plots" "$P/G1_rep1.bam,$P/G1_rep2.bam,$P/G1_rep3.bam" "$P/G2_rep1.bam,$P/G2_rep2.bam,$P/G2_rep3.bam" Control Treatment
test "$(find "$W/plots/Sashimi_plot" -name '*.pdf' -size +1000c | wc -l)" -gt 0
printf 'ASSERT rmats_pdf_count=%s\n' "$(find "$W/plots/Sashimi_plot" -name '*.pdf' -size +1000c | wc -l)"
