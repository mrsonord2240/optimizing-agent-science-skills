#!/usr/bin/env bash
set -euo pipefail
R=/mnt/openscience/audits/bio-sashimi-plots/run/phase2_final_0663f11_pid_owned_20260923
J=/mnt/openscience/audit-envs/alternative-splicing/tools/src/Jutils/jutils.py
W=$R/outputs/input07
mkdir -p "$W"
asenv as-viz-gg34 python "$J" convert-results --leafcutter-dir /mnt/openscience/audit-envs/alternative-splicing/tools/src/Jutils/data/leafcutter --mntjulip-dir /mnt/openscience/audit-envs/alternative-splicing/tools/src/Jutils/data/mntjulip --majiq-dir /mnt/openscience/audit-envs/alternative-splicing/tools/src/Jutils/data/majiq --rmats-dir /mnt/openscience/audit-envs/alternative-splicing/tools/src/Jutils/data/rmats --out-dir "$W/out"
test -s "$W/out/leafcutter_results.tsv"
test -s "$W/out/majiq_results.tsv"
test -s "$W/out/mntjulip_DSR_results_raw.tsv"
test -s "$W/out/rmats_JunctionCountOnly_results.tsv"
echo 'ASSERT jutils_all_documented_converters'
