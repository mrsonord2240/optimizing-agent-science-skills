#!/bin/bash
# Input 6 (scope boundary): trimming / reliability tools that SKILL.md only ROUTES to. REAL Pfam seed as FASTA.
source /mnt/openscience/audit-envs/alignment/wsl_env.sh
cd /mnt/openscience/audits/bio-alignment-msa-parsing/run/data
IN=pfam_PF00042_seed_from_real.fasta
echo "== trimal version"; trimal --version < /dev/null 2>&1 | head -2
echo "== trimal -gappyout -colnumbering (SKILL routing table: HMM profile / preserve column mapping)"
trimal -in $IN -out in6_trimal_gappyout.fa -gappyout -colnumbering < /dev/null > in6_trimal_colnumbering.txt 2>&1
head -c 400 in6_trimal_colnumbering.txt; echo
echo "== clipkit kpic-smart-gap (SKILL routing table: phylogenetic input)"
clipkit $IN -m kpic-smart-gap -o in6_clipkit_kpic.fa -l < /dev/null 2>&1 | tail -8
echo "== muscle 5 ensemble flags (SKILL: 'MUSCLE5 ensemble to get per-column confidence')"
muscle 2>&1 < /dev/null | grep -i "stratified\|diversified\|letterconf\|maxcc" | head -8
echo "== guidance2 present?"
which guidance guidance.pl 2>&1 | head -2 || true
echo "(exit above is expected: GUIDANCE2 not installable, see TOOLS.md Blocked)"
