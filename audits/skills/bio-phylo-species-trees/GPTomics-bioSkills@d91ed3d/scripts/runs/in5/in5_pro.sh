#!/bin/bash
# Input 5 (SYNTHETIC fam set): multi-copy gene families -> ASTRAL-Pro, exactly as the Skill writes it, then with the
# gene->species mapping the Skill omits. Family trees come from `iqtree2 -S` (runs/genetrees.sh).
set -u
A=/f/OpenScience/audits/bio-phylo-species-trees
X=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools/aster/ASTER-Windows/exe
PY=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/Scripts/python.exe
export PYTHONIOENCODING=utf-8
cd $A/runs/in5 || exit 1
cp loci.treefile family_trees.nwk
echo "families: $(wc -l < family_trees.nwk)"
echo "single-copy families (no species label repeated): $($PY - <<'EOF'
import re
n = 0
for line in open("family_trees.nwk", encoding="utf-8"):
    sp = [g.rsplit("_", 1)[0] for g in re.findall(r"(Sp_[A-Z]_[12])", line)]
    n += len(sp) == len(set(sp))
print(n)
EOF
)"
echo "--- as written: astral-pro -i family_trees.nwk -o species_pro.tre"
$X/astral-pro.exe -i family_trees.nwk -o species_pro.tre 2> species_pro.log; echo "exit $?"
cat species_pro.tre; tail -3 species_pro.log
echo "--- with mapping: astral-pro -a gene2species.txt -i family_trees.nwk -o species_pro_map.tre"
$X/astral-pro.exe -a $A/data/fam/gene2species.txt -i family_trees.nwk -o species_pro_map.tre 2> species_pro_map.log
echo "exit $?"; cat species_pro_map.tre
echo "--- with mapping + -u 2"
$X/astral-pro.exe -u 2 -a $A/data/fam/gene2species.txt -i family_trees.nwk -o species_pro_map_u2.tre 2> species_pro_map_u2.log
echo "exit $?"
echo "--- RF vs simulated species tree (mapped run)"
$PY $A/data/treetools.py rf $A/data/fam/species_true.nwk species_pro_map.tre
$PY $A/data/treetools.py splits species_pro_map_u2.tre
