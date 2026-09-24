#!/bin/bash
# NEW input (not in the pre-fix audit). The dedup pass moved a fact from usage-guide.md's deleted
# Tips section into SKILL.md's tool-list line: "Bio.Blast.Applications ... deprecated and removed
# in BioPython 1.85". Verify that specific version claim against the installed biopython, and
# confirm the wrapper wasn't silently broken by the dedup edit.
set -uo pipefail
PY="F:/OpenScience/audit-envs/database-access/Scripts/python.exe"
cd "F:/OpenScience/audits/bio-local-blast/run/work"
mkdir -p input9 && cd input9

echo "=== installed biopython version ==="
"$PY" -c "import Bio; print('Bio.__version__ =', Bio.__version__)"

echo
echo "=== does Bio.Blast.Applications exist on the installed version? ==="
"$PY" -c "
try:
    import Bio.Blast.Applications as A
    print('IMPORTED OK -- module still present:', A)
except Exception as e:
    print('IMPORT FAILED (expected if truly removed):', type(e).__name__, e)
"

echo
echo "=== gate 8 (shipped-means-present): do usage-guide.md's Tips-replacement section headings actually exist in SKILL.md? ==="
SKILL="F:/OpenScience/wt/db-blast/database-access/local-blast/SKILL.md"
for heading in "Database format: v5 vs v4" "Soft vs hard masking" "Output format reference" "Thread scaling" "Practice boundaries"; do
  if grep -qF "$heading" "$SKILL"; then
    echo "PRESENT: $heading"
  else
    echo "MISSING: $heading"
  fi
done

echo
echo "=== gate 8: all files usage-guide.md/SKILL.md point at actually exist ==="
ls -la "F:/OpenScience/wt/db-blast/database-access/local-blast/examples/"
