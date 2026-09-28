#!/usr/bin/env bash
# Reproduce the full re-audit.  All scripts, logs, plots and tables remain in
# the live audit folder.  The shared Windows R runtime returns status 1 after
# otherwise successful runs, so R completion is asserted from explicit success
# markers plus the expected parseable outputs rather than process status alone.
set -u

ROOT='/f/OpenScience/audits/bio-data-visualization-statistical-annotation'
RUN="$ROOT/run"
OUT="$RUN/output"
PY='/f/OpenScience/audit-envs/data-visualization/py.sh'
R="$RUN/run_r.sh"

mkdir -p "$OUT/example"

"$PY" "$RUN/generate_new_data.py" >"$OUT/generate_new_data.log" 2>&1 || exit 10
"$PY" "$RUN/audit_python.py" >"$OUT/audit_python.log" 2>&1 || exit 11

"$PY" "$RUN/skill-copy/tests/regression.py" >"$OUT/regression_python.log" 2>&1 || exit 17

"$R" "$RUN/audit_r.R" >"$OUT/audit_r.log" 2>&1
R_AUDIT_STATUS=$?
grep -q 'R re-audit assertions passed' "$OUT/audit_r.log" || exit 12
test -s "$OUT/r_metrics.txt" || exit 13

"$R" "$RUN/skill-copy/tests/regression.R" >"$OUT/regression_r.log" 2>&1
R_REGRESSION_STATUS=$?
grep -q 'R regression checks passed' "$OUT/regression_r.log" || exit 18

"$R" "$RUN/skill-copy/examples/statanno_phd.R" \
  "$ROOT/data/three_group.csv" \
  "$ROOT/data/paired.csv" \
  "$ROOT/data/nested.csv" \
  "$OUT/example" >"$OUT/example.log" 2>&1
R_EXAMPLE_STATUS=$?
for expected in pairwise-adjusted.png ggsignif-adjusted.png paired-adjusted.png nested-lmm.png; do
  test -s "$OUT/example/$expected" || exit 14
done

"$PY" "$RUN/verify_outputs.py" >"$OUT/verify_outputs.log" 2>&1 || exit 15
"$PY" "$RUN/make_contact_sheets.py" >"$OUT/make_contact_sheets.log" 2>&1 || exit 16

{
  echo 'python_generation_status=0'
  echo 'python_audit_status=0'
  echo 'python_regression_status=0'
  echo "r_audit_wrapper_status=$R_AUDIT_STATUS"
  echo 'r_audit_completion_marker=true'
  echo "r_regression_wrapper_status=$R_REGRESSION_STATUS"
  echo 'r_regression_completion_marker=true'
  echo "r_example_wrapper_status=$R_EXAMPLE_STATUS"
  echo 'r_example_expected_outputs=true'
  echo 'verification_status=0'
  echo 'contact_sheet_status=0'
} >"$RUN/execution_status.txt"

echo 'Full re-audit completed and verified'
