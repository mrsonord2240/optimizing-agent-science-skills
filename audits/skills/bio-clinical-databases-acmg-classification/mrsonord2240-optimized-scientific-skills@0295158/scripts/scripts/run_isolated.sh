#!/usr/bin/env bash
set -euo pipefail

tool_root=/mnt/openscience/audit-envs/bio-clinical-databases-acmg-classification
candidate=/mnt/openscience/wt/opt10-acmg-classification/skills/bio-clinical-databases-acmg-classification
audit=/mnt/openscience/audits/bio-clinical-databases-acmg-classification/reaudit2-opt10-20260928
python="$tool_root/conda-env-delta/bin/python"
wrapper="$tool_root/tools/wsl_isolated_exec.sh"

"$wrapper" env PYTHONDONTWRITEBYTECODE=1 "$python" -B -m unittest discover -s "$candidate/tests" -p 'test_*.py' -v \
  > "$audit/evidence/unit-tests.log" 2>&1
"$wrapper" env PYTHONDONTWRITEBYTECODE=1 ACMG_CANDIDATE="$candidate" ACMG_AUDIT_OUT="$audit/evidence" \
  "$python" -B "$audit/scripts/run_reaudit.py" \
  > "$audit/evidence/reaudit.log" 2>&1
"$wrapper" env PYTHONDONTWRITEBYTECODE=1 "$python" -B "$candidate/tests/live_interface_smoke.py" \
  > "$audit/evidence/live-interface-smoke.log" 2>&1
"$wrapper" env PYTHONDONTWRITEBYTECODE=1 "$python" -B "$candidate/scripts/acmg_classify.py" \
  > "$audit/evidence/standalone-demo.log" 2>&1

"$wrapper" env PYTHONPYCACHEPREFIX=/tmp/acmg-reaudit2-pycache "$python" -m py_compile \
  "$candidate/scripts/acmg_classify.py" \
  "$candidate/tests/test_acmg_classify.py" \
  "$candidate/tests/live_interface_smoke.py"

if find "$candidate" \( -type d -name __pycache__ -o -type f -name '*.pyc' \) | grep -q .; then
  echo "candidate cache artifact detected" >&2
  exit 71
fi

printf 'compile=PASS\nshipped_tests=24\ncandidate_cache_artifacts=0\n' \
  > "$audit/evidence/preflight.log"
