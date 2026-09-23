#!/bin/bash
set -euo pipefail
WORK=/tmp/reaudit_rh
cd "$WORK"
# Run the shipped toy script fresh, from its own examples/data fixture bundle -- not the
# audit-env cache -- to confirm what actually ships with the Skill reproduces the true hit.
rm -f examples/data/PF00069.hmm.h3*
bash examples/pfam_annotation_toy.sh
