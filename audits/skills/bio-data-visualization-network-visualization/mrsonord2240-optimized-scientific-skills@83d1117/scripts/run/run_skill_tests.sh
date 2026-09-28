#!/bin/bash
set -euo pipefail
AUDIT=/f/OpenScience/audits/bio-data-visualization-network-visualization
ENV=/f/OpenScience/audit-envs/data-visualization
cd "$AUDIT/run/skill"
"$ENV/py.sh" tests/test_network_recipes.py 2>&1 | tee "$AUDIT/logs/skill_tests.log"
