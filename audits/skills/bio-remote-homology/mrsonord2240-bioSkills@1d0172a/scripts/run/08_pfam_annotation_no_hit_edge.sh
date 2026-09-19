#!/bin/bash
# NEW input (not tested by original auditor or fixer): edge case -- run the FIXED
# examples/pfam_annotation.sh against a query that has NO real Pfam-A/PF00069 hit, to check the
# script degrades gracefully (no crash under set -euo pipefail) when hmmscan reports zero domains.
set -euo pipefail
WORK=/tmp/reaudit_rh
cd "$WORK"

cat > no_hit_query.fasta <<'EOF'
>synthetic_no_hit
MASHVAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
EOF

echo "=== Running fixed pfam_annotation.sh against a query with no expected Pfam hit ==="
set +e
bash examples/pfam_annotation.sh no_hit_query.fasta pfam_db
STATUS=$?
set -e
echo "script exit status: $STATUS"
echo
echo "=== raw domtbl ==="
grep -v '^#' query.domtbl || echo "(no hit lines, as expected)"
