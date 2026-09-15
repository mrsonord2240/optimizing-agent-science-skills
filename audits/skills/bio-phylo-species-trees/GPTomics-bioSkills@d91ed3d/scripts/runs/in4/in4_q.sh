#!/bin/bash
# Input 4 (SYNTHETIC intro set): ILS vs introgression reading from ASTER quartet frequencies.
# Skill: `astral -u 2` gives q1/q2/q3; read q2 ~ q3 as ILS, q2 != q3 as introgression.
# Auditor addition: `-u 3` writes freqQuad.csv, which names the topology behind each of q1/q2/q3 (the -u 2 label does not),
# run on estimated AND true gene trees; locus_origin.txt gives the simulated truth (30% introgressed from C into (D,E)).
set -u
A=/f/OpenScience/audits/bio-phylo-species-trees
X=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools/aster/ASTER-Windows/exe
cd $A/runs/in4 || exit 1
echo "--- simulated locus origin"; sort $A/data/intro/locus_origin.txt | uniq -c
mkdir -p est true
( cd est  && $X/astral.exe -u 3 -i ../gene_trees.nwk -o sp_u3.tre 2> u3.log; echo "est -u 3 exit $?" )
( cd true && $X/astral.exe -u 3 -i $A/data/intro/true_gene_trees.nwk -o sp_u3.tre 2> u3.log; echo "true -u 3 exit $?" )
for d in est true; do
  echo "--- freqQuad.csv ($d gene trees)"; ls $d
  f=$(ls $d/*freqQuad* 2>/dev/null | head -1); [ -n "$f" ] && cat "$f"
done
