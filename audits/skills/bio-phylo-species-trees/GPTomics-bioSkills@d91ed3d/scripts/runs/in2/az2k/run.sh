#!/bin/bash
# Supplementary Input 2 stress test (2026-09-15, SYNTHETIC): does concatenation converge on the anomalous tree?
# Deeper anomaly zone (two 0.01-CU internodes), 2000 loci x 200 bp. Concatenation is run on the simulated loci;
# ASTRAL is run on the TRUE gene trees (estimating 2000 gene trees was not affordable on a shared machine).
A=/f/OpenScience/audits/bio-phylo-species-trees
X=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools/aster/ASTER-Windows/exe
PY=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/Scripts/python.exe
export PATH=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools/bin:$PATH PYTHONIOENCODING=utf-8
O=$A/runs/in2/az2k; cd $O
t0=$(date +%s); (cd $A/data && $PY make_data.py . az2k); echo "make_data az2k exit $? $(( $(date +%s)-t0 ))s"
echo "--- true gene-tree topology frequencies"; $PY $A/data/treetools.py freq $A/data/az2k/true_gene_trees.nwk $A/data/az2k/species_true.nwk
t0=$(date +%s); iqtree2 -s $A/data/az2k/concat.fasta -m HKY+G4 -B 1000 -T 4 --seed 12345 --prefix concat --quiet > concat.stdout 2>&1
echo "concat exit $? $(( $(date +%s)-t0 ))s"
$X/astral.exe -u 2 -i $A/data/az2k/true_gene_trees.nwk -o astral_true_u2.tre 2> astral.log; echo "astral exit $?"
echo "--- RF vs simulated species tree"; $PY $A/data/treetools.py rf $A/data/az2k/species_true.nwk concat.treefile astral_true_u2.tre
echo "--- concat splits (UFBoot)"; $PY $A/data/treetools.py splits concat.treefile
echo "--- astral -u 2 (true gene trees)"; $PY $A/data/treetools.py splits astral_true_u2.tre
echo DONE
