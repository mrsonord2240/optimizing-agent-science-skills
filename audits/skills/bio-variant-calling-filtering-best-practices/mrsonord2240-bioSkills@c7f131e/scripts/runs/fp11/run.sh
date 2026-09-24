#!/bin/bash
# Fresh final-pass input 11: execute the exact-current cyvcf2 predicate body
# against an audit stub, including zero-valued and missing INFO states.
set -eu
source ../env.sh
SKILL=/f/OpenScience/worktrees/bio-variant-calling-filtering-best-practices-finalpass/variant-calling/filtering-best-practices/SKILL.md
$PY check_predicate.py "$(cygpath -w "$SKILL")"
