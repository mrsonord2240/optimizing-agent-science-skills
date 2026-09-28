#!/bin/bash
set -euo pipefail
AUDIT=/f/OpenScience/audits/bio-data-visualization-network-visualization
ENV=/f/OpenScience/audit-envs/data-visualization
export PYTHONDONTWRITEBYTECODE=1
"$ENV/py.sh" "$AUDIT/run/targeted_round2_cases.py" \
  2>&1 | tee "$AUDIT/logs/round2_targeted.log"
