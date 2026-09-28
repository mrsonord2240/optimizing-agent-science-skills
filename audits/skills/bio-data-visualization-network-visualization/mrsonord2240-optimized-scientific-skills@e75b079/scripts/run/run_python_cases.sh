#!/bin/bash
set -euo pipefail
AUDIT=/f/OpenScience/audits/bio-data-visualization-network-visualization
ENV=/f/OpenScience/audit-envs/data-visualization
"$ENV/py.sh" "$AUDIT/run/prepare_data.py" | tee "$AUDIT/logs/prepare_data.log"
"$ENV/py.sh" "$AUDIT/run/audit_python_cases.py" | tee "$AUDIT/logs/python_cases.log"
