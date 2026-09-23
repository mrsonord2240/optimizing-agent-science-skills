#!/usr/bin/env bash
# Purpose: run the Phase 2 lineage-tracing dynamic inputs in their dedicated WSL environments.
# Usage: bash /mnt/openscience/audits/bio-single-cell-lineage-tracing/run/phase2_20260923/run_phase2.sh
set -euo pipefail
RUN=/mnt/openscience/audits/bio-single-cell-lineage-tracing/run/phase2_20260923
CASS=/mnt/openscience/audit-envs/bio-single-cell-lineage-tracing/conda-env/bin/python
COSPAR=/mnt/openscience/audit-envs/bio-single-cell-lineage-tracing/cospar-venv/bin/python
STARTLE=/mnt/openscience/audit-envs/bio-single-cell-lineage-tracing/startle-env/bin/startle
cd "$RUN"
"$CASS" input_1_2_tree_and_solvers.py | tee input_1_2_tree_and_solvers.out
"$CASS" input_3_raw_api.py | tee input_3_raw_api.out
MPLBACKEND=Agg "$COSPAR" input_4_cospar.py | tee input_4_cospar.out
"$CASS" input_5_mtdna.py | tee input_5_mtdna.out
"$CASS" input_6_startle_prepare.py | tee input_6_startle_prepare.out
PATH="$(dirname "$STARTLE"):$PATH" bash run_input_6_startle.sh | tee input_6_startle.out
