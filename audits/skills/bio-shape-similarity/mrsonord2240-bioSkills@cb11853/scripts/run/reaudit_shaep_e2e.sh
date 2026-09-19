#!/bin/bash
# Re-audit: run the fixed SKILL.md ShaEP example end-to-end, including the new
# obabel --gen3D SMILES->mol2 step, on a fresh molecule pair (not the fixer's
# acetanilide/fluoro pair -- use a different scaffold: ibuprofen vs naproxen-like).
set -e
cd "$(dirname "$0")"
OBABEL="/f/OpenScience/audit-envs/cheminformatics-hit-triage-analyst/Scripts/obabel.exe"
SHAEP="/f/OpenScience/audit-envs/cheminformatics-hit-triage-analyst/tools/shaep/shaep.exe"

echo "=== obabel --gen3D: query ==="
"$OBABEL" -:"CC(C)Cc1ccc(cc1)C(C)C(=O)O" -O query_shaep.mol2 --gen3D
echo "=== obabel --gen3D: target ==="
"$OBABEL" -:"COc1ccc2cc(ccc2c1)C(C)C(=O)O" -O target_shaep.mol2 --gen3D

echo "=== mol2 coordinate check (non-zero) ==="
grep -A3 "@<TRIPOS>ATOM" query_shaep.mol2 | tail -3
grep -A3 "@<TRIPOS>ATOM" target_shaep.mol2 | tail -3

echo "=== shaep ==="
"$SHAEP" -q query_shaep.mol2 target_shaep.mol2 -s aligned_hits_shaep.sdf similarity_shaep.txt
echo "=== similarity_shaep.txt ==="
cat similarity_shaep.txt
