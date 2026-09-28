#!/bin/bash
set -euo pipefail
AUDIT=/f/OpenScience/audits/bio-data-visualization-network-visualization
ENV=/f/OpenScience/audit-envs/data-visualization
"$ENV/py.sh" "$AUDIT/run/check_outputs.py" | tee "$AUDIT/logs/artifact_checks.log"
"$ENV/py.sh" "$AUDIT/run/screenshot_html.py" | tee "$AUDIT/logs/html_screenshots.log"
"$ENV/py.sh" "$AUDIT/run/check_outputs.py" | tee "$AUDIT/logs/artifact_checks_after_html.log"
