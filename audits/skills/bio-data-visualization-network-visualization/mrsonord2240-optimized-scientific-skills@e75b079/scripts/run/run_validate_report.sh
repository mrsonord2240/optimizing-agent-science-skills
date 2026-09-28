#!/usr/bin/env bash
set -euo pipefail
AUDIT=/f/OpenScience/audits/bio-data-visualization-network-visualization
ENV=/f/OpenScience/audit-envs/data-visualization
"$ENV/py.sh" "$AUDIT/run/validate_report.py" 2>&1 | tee "$AUDIT/logs/report_validation.log"
