#!/usr/bin/env bash
# RE-AUDIT Input 3 (Edge, NEW): verify the receptor-prep fix generalizes to a
# second, independent insertion-code-bearing structure: porcine pancreatic
# elastase, PDB 1EAI, chain A (icodes 36A/36B/36C, 65A, 99A/99B, 170A/170B,
# 188A, 217A, 221A -- denser and differently-patterned than 3PTB's 184A/188A/221A).
set -ex
ENV="F:/OpenScience/audit-envs/cheminformatics-hit-triage-analyst"

curl -s -o 1EAI.pdb "https://files.rcsb.org/download/1EAI.pdb"
awk '($1=="ATOM" && substr($0,22,1)=="A") || $1=="END"' 1EAI.pdb > elastase_chainA.pdb

"$ENV/tools/pdb2pqr-venv/Scripts/pdb2pqr.exe" --ff=AMBER --with-ph=7.4 \
  --pdb-output elastase_pH7.4.pdb elastase_chainA.pdb elastase_pH7.4.pqr

# OLD (pre-fix) documented route -- expected to crash on insertion codes:
"$ENV/Scripts/mk_prepare_receptor.exe" --read_pqr elastase_pH7.4.pqr -o receptor_old_route -p || true

# NEW (fixed) route -- expected to succeed:
"$ENV/Scripts/mk_prepare_receptor.exe" --read_pdb elastase_pH7.4.pdb -o receptor_elastase -p
