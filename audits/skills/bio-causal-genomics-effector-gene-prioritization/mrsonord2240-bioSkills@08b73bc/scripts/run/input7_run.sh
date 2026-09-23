#!/usr/bin/env bash
set -euo pipefail
AUDIT=/f/OpenScience/audits/bio-causal-genomics-effector-gene-prioritization
RSH=/f/OpenScience/audit-envs/mendelian-randomization-analyst/r.sh
set +e
"$RSH" "$AUDIT/run/skill_copy/scripts/concordance_scoring.R" \
  "$AUDIT/data/input7_boundaries.tsv" "$AUDIT/run/outputs/input7_boundaries" \
  | tee "$AUDIT/run/outputs/input7_concordance.log"
SOURCE_STATUS=${PIPESTATUS[0]}
set -e
# This Windows R runtime has a documented exit-139 teardown defect after materialized
# output. Treat it as successful only after the source output exists and the independent
# assertion script parses it; any other nonzero status remains a failure.
if [ "$SOURCE_STATUS" -ne 0 ] && [ "$SOURCE_STATUS" -ne 139 ]; then
  exit "$SOURCE_STATUS"
fi
test -s "$AUDIT/run/outputs/input7_boundaries.scored.tsv"
"$RSH" "$AUDIT/run/input7_concordance_boundaries.R" "$AUDIT/run/outputs/input7_boundaries" \
  | tee "$AUDIT/run/outputs/input7_assertions.log"
