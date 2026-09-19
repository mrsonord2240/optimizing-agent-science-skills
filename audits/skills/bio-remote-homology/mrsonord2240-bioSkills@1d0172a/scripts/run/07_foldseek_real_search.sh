#!/bin/bash
# NEW input (not run by the fixer, who only verified the version-check command): exercise the
# actual Foldseek structure-search pipeline end to end -- fetch a real PDB structure, build a
# foldseek DB, and self-search it, per SKILL.md's "Foldseek search against AlphaFoldDB" pattern
# (scaled down: self-DB instead of the multi-GB AlphaFoldDB Swiss-Prot download, same as TOOLS.md's
# own approach, but this auditor fetches and runs it independently rather than reusing that output).
set -euo pipefail
WORK=/tmp/reaudit_rh
cd "$WORK"
mkdir -p foldseek_ws && cd foldseek_ws

echo "=== Fetch 1ATP (cAMP-dependent protein kinase catalytic subunit) from RCSB ==="
curl -sS -o 1atp.pdb https://files.rcsb.org/download/1ATP.pdb
wc -l 1atp.pdb

echo
echo "=== Build foldseek DB and self-search ==="
mkdir -p db tmp
foldseek createdb 1atp.pdb db/1atp
foldseek easy-search 1atp.pdb db/1atp result.m8 tmp \
    --format-output query,target,fident,alnlen,evalue,bits,prob,qtmscore,ttmscore

echo
echo "=== result.m8 ==="
cat result.m8
