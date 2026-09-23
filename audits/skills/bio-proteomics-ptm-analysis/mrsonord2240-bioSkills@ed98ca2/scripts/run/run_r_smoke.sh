#!/usr/bin/env bash
# Run the saved R runtime control through the same mandated launcher as the skill.
set -uo pipefail
'F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/r.sh' r_smoke.R > r_smoke.out 2>&1
echo "R_SMOKE_EXIT=$?" >> r_smoke.out
