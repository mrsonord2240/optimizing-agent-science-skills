#!/usr/bin/env bash
# Fresh Phase 2 regression suite for the exact audited tip.  Run from WSL science.
set -euo pipefail
RUN_DIR="/mnt/openscience/audits/bio-experimental-design-batch-design/run/phase2-corrective-20260923"
RUNTIME="/mnt/openscience/audit-envs/crispr-screen-analyst/tools/designit-linux-runtime/r-designit-sva-linux.sh"
cd "$RUN_DIR"
"$RUNTIME" runtime_probe.R > in00_runtime_probe.out 2>&1
"$RUNTIME" make_inputs.R > in0_make_inputs.out 2>&1
"$RUNTIME" scripts/assign_batches.R samples24.csv 3 8 condition,sex layout24.csv 10000 17 > in1_assign_canonical.out 2>&1
"$RUNTIME" scripts/bridge_layout.R samples60.csv 4 16 16 condition,site layout60.csv 10000 17 > in2_bridge_canonical.out 2>&1
"$RUNTIME" test_sva_missing.R > in3_sva_na.out 2>&1
"$RUNTIME" check_balance_cases.R > in4_balance_cases.out 2>&1
"$RUNTIME" test_combat_design_claims.R > in5_combat_claims.out 2>&1
"$RUNTIME" scripts/assign_batches.R samples24.csv 3 8 condition,sex layout24_repeat.csv 10000 17 > in6_determinism.out 2>&1
cmp layout24.csv layout24_repeat.csv
echo "PASS: same seed produced byte-identical layout CSV." >> in6_determinism.out
if "$RUNTIME" scripts/assign_batches.R missing_sex.csv 3 8 condition,sex should_not_exist.csv 100 17 > in7_missing_covariate.out 2>&1; then
  echo "FAIL: missing covariate was accepted" >> in7_missing_covariate.out
  exit 1
fi
echo "PASS: missing covariate was rejected." >> in7_missing_covariate.out
if "$RUNTIME" scripts/assign_batches.R samples60.csv 3 8 condition,site should_not_exist.csv 100 17 > in8_over_capacity.out 2>&1; then
  echo "FAIL: over-capacity design was accepted" >> in8_over_capacity.out
  exit 1
fi
echo "PASS: over-capacity design was rejected." >> in8_over_capacity.out
if "$RUNTIME" scripts/bridge_layout.R samples60.csv 4 16 17 condition,site invalid_reserved.csv 10000 17 > in9_invalid_reserved_channel.out 2>&1; then
  echo "FAIL: out-of-range reserved channel was accepted" >> in9_invalid_reserved_channel.out
  exit 1
fi
echo "PASS: out-of-range reserved channel was rejected." >> in9_invalid_reserved_channel.out
"$RUNTIME" parse_sources.R > parse_sources.out 2>&1
echo "PASS: all nine fresh inputs and source parsing completed under the isolated WSL runtime."
