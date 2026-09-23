#!/usr/bin/env bash
# Assert that the shared audit environment has the same package state before and after audit runs.
# Usage: bash verify_env_unchanged.sh <output-dir>
set -euo pipefail
out_dir="$1"
diff -u "$out_dir/pre_pip_freeze.txt" "$out_dir/post_pip_freeze.txt"
diff -u "$out_dir/pre_r_packages.txt" "$out_dir/post_r_packages.txt"
printf 'shared_environment_mutation=none\n' >"$out_dir/environment_comparison.txt"
