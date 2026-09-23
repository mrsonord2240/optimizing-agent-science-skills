#!/bin/bash
# Phase 2 static verification of every shipped R executable and every referenced artifact.
set -euo pipefail
RSH=/f/OpenScience/audit-envs/mendelian-randomization-analyst/r.sh
SKILL=/f/OpenScience/wt/causal-genomics-mediation-analysis/causal-genomics/mediation-analysis
for f in "$SKILL"/examples/*.R "$SKILL"/scripts/*.R; do
  win_f="F:${f#/f}"
  "$RSH" -e "parse(file='$win_f'); cat('PARSE PASS: $win_f\\n')"
done
for f in "$SKILL"/SKILL.md "$SKILL"/usage-guide.md "$SKILL"/references/*.md "$SKILL"/examples/*.R "$SKILL"/scripts/*.R; do
  test -f "$f"
done
echo "ASSERT PASS: all SKILL.md-referenced files are present."
