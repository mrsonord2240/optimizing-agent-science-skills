#!/usr/bin/env bash
set -euo pipefail
root="F:/OpenScience/audits/bio-causal-genomics-colocalization-analysis/run"
python "$root/assert_prior_inputs.py" > "$root/assert_prior_inputs_output.txt" 2>&1
python "$root/assert_fresh_inputs.py" > "$root/assert_fresh_inputs_output.txt" 2>&1
