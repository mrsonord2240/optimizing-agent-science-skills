#!/usr/bin/env bash
set -euo pipefail
run_dir=/mnt/openscience/audits/bio-experimental-design-randomization-blocking/run
for script in \
  in1_experimental_unit_aggregation.R \
  in2_restricted_randomization.R \
  in3_rcbd_blocking.R \
  in4_splitplot_subplot.R \
  in5_factorial_blocked.R \
  in8_shipped_example_end_to_end.R \
  in9_independent_wholeplot_generalization.R \
  in11_latin_square.R \
  in12_seeded_determinism.R; do
  "$run_dir/run_isolated_r.sh" "$run_dir/$script" > "$run_dir/${script%.R}.log" 2>&1
  printf '%s=PASS\n' "$script"
done
