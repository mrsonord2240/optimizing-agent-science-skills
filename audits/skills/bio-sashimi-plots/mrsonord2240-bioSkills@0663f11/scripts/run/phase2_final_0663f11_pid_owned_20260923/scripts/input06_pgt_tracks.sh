#!/usr/bin/env bash
set -euo pipefail
R=/mnt/openscience/audits/bio-sashimi-plots/run/phase2_final_0663f11_pid_owned_20260923
P=/mnt/openscience/audit-envs/alternative-splicing/public-data/planted
S=$R/source_copy/scripts/pgt_tracks.sh
W=$R/outputs/input06
mkdir -p "$W"
asenv as-core bash "$S" "$W/out" "$P/G1_rep1.bam,$P/G1_rep2.bam,$P/G1_rep3.bam" "$P/G2_rep1.bam,$P/G2_rep2.bam,$P/G2_rep3.bam"
test -s "$W/out/junctions.bedpe"
cp /mnt/openscience/as-sashimi-scratch/p2/sc/pg/tracks.ini "$W/tracks.ini"
cp /mnt/openscience/audit-envs/alternative-splicing/public-data/planted/planted.gtf "$W/annotation.gtf"
sed -i "s#file = ctrl.bedgraph#file = $W/out/ctrl.bedgraph#; s#file = trt.bedgraph#file = $W/out/trt.bedgraph#; s#file = junctions.bedpe#file = $W/out/junctions.bedpe#" "$W/tracks.ini"
asenv as-viz-gg34 pyGenomeTracks --tracks "$W/tracks.ini" --region chrP:1-1200 -o "$W/figure.png"
test -s "$W/figure.png"
echo 'ASSERT pgt_bedpe_and_render'
