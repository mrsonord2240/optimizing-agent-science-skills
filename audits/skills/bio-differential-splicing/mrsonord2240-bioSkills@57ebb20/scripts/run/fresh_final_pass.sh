#!/usr/bin/env bash
# Run the two fresh final-pass inputs after the archived regressions.
set -euo pipefail
ROOT=/mnt/openscience/audits/bio-differential-splicing/run
/home/sci/.local/bin/micromamba run -n as-core python "$ROOT/fresh_coverage_filter.py" "$ROOT/skill"
/home/sci/.local/bin/micromamba run -n as-core python "$ROOT/fresh_recall_filter.py" "$ROOT/skill" "$ROOT/out/in5/n6/rmats_AvB/out/SE.MATS.JC.txt"
/home/sci/.local/bin/micromamba run -n as-rleaf Rscript "$ROOT/fresh_empty_leafcutter_guard.R" "$ROOT/out/fresh_empty"
