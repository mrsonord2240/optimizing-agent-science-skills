#!/bin/bash
set -euo pipefail
AUDIT=/f/OpenScience/audits/bio-data-visualization-network-visualization
ENV=/f/OpenScience/audit-envs/data-visualization
"$ENV/py.sh" "$AUDIT/run/build_report.py" 2>&1 | tee "$AUDIT/logs/build_report.log"
