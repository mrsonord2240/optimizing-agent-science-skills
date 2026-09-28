#!/bin/bash
set -euo pipefail
AUDIT=/f/OpenScience/audits/bio-data-visualization-network-visualization
ENV=/f/OpenScience/audit-envs/data-visualization
"$ENV/py.sh" "$AUDIT/run/fresh_final_cases.py" \
  2>&1 | tee "$AUDIT/logs/fresh_final_cases.log"
