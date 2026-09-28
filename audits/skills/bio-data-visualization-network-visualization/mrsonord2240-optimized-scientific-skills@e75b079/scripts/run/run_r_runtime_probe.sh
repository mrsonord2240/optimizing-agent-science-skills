#!/bin/bash
set -uo pipefail
AUDIT=/f/OpenScience/audits/bio-data-visualization-network-visualization
ENV=/f/OpenScience/audit-envs/data-visualization
set +e
"$ENV/r.sh" "$AUDIT/run/r_runtime_probe.R" 2>&1 | tee "$AUDIT/logs/r_runtime_probe.log"
status=${PIPESTATUS[0]}
set -e
echo "runtime_probe_status=$status" | tee "$AUDIT/logs/r_runtime_probe_status.log"
set +e
"$ENV/r.sh" "$AUDIT/run/r_package_probe.R" 2>&1 | tee "$AUDIT/logs/r_package_probe.log"
package_status=${PIPESTATUS[0]}
set -e
echo "package_probe_status=$package_status" | tee "$AUDIT/logs/r_package_probe_status.log"
exit 0
