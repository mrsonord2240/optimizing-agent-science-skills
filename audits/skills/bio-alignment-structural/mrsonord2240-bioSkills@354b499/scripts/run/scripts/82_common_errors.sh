#!/bin/bash
# SKILL.md "Common Errors" table: reproduce the rows on synthetic degenerate inputs + real 1MBN. Judge by message and output.
source /mnt/openscience/audit-envs/alignment/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-structural/run; cd $R/work; rm -rf err; mkdir err; cd err
S=$R/data/real_pdb; Y=$R/data/synthetic
echo "== TMalign 1MBN vs one_residue (SYNTHETIC)"; TMalign $S/1MBN.pdb $Y/one_residue.pdb -outfmt 2 </dev/null 2>&1 | head -4; echo "rc=${PIPESTATUS[0]}"
echo "== TMalign 1MBN vs ligand_only (SYNTHETIC)"; TMalign $S/1MBN.pdb $Y/ligand_only.pdb -outfmt 2 </dev/null 2>&1 | head -4; echo "rc=${PIPESTATUS[0]}"
echo "== USalign 1MBN vs helix10 (SYNTHETIC)"; USalign $S/1MBN.pdb $Y/helix10.pdb -outfmt 2 </dev/null 2>&1 | head -4
echo "== foldseek easy-search with wrong DB path (SKILL: 'no hits: wrong database format')"
foldseek easy-search $S/1MBN.pdb /nonexistent/db r.m8 tmp -v 1 </dev/null > fs.log 2>&1; echo "rc=$? m8_exists=$([ -f r.m8 ] && echo yes || echo no)"; grep -a -iE "error|not exist|cannot|fail" fs.log | head -3
echo "== foldseek easy-search with one_residue query (SYNTHETIC) vs CATH50"
foldseek easy-search $Y/one_residue.pdb $ALN/public-data/foldseek-db/CATH50 r2.m8 tmp2 -v 1 </dev/null > fs2.log 2>&1; echo "rc=$? rows=$(wc -l < r2.m8 2>/dev/null)"; grep -a -iE "error|no |empty" fs2.log | head -3
echo "== foldmason with 1 structure"
foldmason easy-msa $S/1MBN.pdb fm1 tmpf -v 1 </dev/null > fm.log 2>&1; echo "rc=$?"; grep -a -iE "error|fail|at least" fm.log | head -3; ls fm1* 2>/dev/null
