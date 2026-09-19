#!/bin/bash
# Regression test: run the fixed examples/pfam_annotation.sh END TO END (not just the awk line)
# against the real P17612 vs PF00069 fixture, faking the PFAM_DIR pre-press so it doesn't try to
# download the full 1.7GB Pfam-A.hmm.
set -euo pipefail
WORK=/tmp/reaudit_rh
cd "$WORK"
mkdir -p pfam_db
cp PF00069.hmm pfam_db/Pfam-A.hmm
cp PF00069.hmm.h3f pfam_db/Pfam-A.hmm.h3f
cp PF00069.hmm.h3i pfam_db/Pfam-A.hmm.h3i
cp PF00069.hmm.h3m pfam_db/Pfam-A.hmm.h3m
cp PF00069.hmm.h3p pfam_db/Pfam-A.hmm.h3p

echo "=== Running shipped examples/pfam_annotation.sh unmodified ==="
bash examples/pfam_annotation.sh P17612.fasta pfam_db
echo
echo "=== raw domtbl (ground truth) ==="
grep -v '^#' query.domtbl
