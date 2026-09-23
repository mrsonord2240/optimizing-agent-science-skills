#!/usr/bin/env bash
# Invoke the dedicated QIIME2 environment without changing its shared installation state.
set -euo pipefail
micromamba run -n qiime2-amplicon-2024.10 bash /mnt/openscience/audits/bio-microbiome-taxonomy-assignment/run/2026-09-23-final-pass/run_qiime2_end_to_end.sh
