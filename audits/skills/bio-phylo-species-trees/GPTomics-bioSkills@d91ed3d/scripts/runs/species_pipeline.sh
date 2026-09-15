#!/bin/bash
# Auditor harness (2026-09-15): the Skill's "Estimate the Species Tree from Gene Trees" and
# "Compute and Read Concordance Factors" blocks, applied to one input's estimated gene trees.
# usage: species_pipeline.sh RUNDIR DATASET OUTGROUP
# SYNTHETIC data only. Deviations from the Skill text, each forced by this machine:
#   - contraction <10 uses data/treetools.py (nw_ed / Newick Utilities has no Windows build)
#   - `astral -t 8` is run as `astral -t 4` (4-thread cap on a shared machine)
set -u
R=$1; S=$2; OUT=$3
A=/f/OpenScience/audits/bio-phylo-species-trees
X=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools/aster/ASTER-Windows/exe
PY=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/Scripts/python.exe
export PATH=$X:/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools/bin:$PATH
export PYTHONIOENCODING=utf-8
cd "$R" || exit 1

$PY $A/data/treetools.py contract loci.treefile gene_trees.nwk 10
wc -l < gene_trees.nwk

wastral -i gene_trees.nwk -o species_wastral.tre 2> species_wastral.log;     echo "wastral exit $?"
astral -t 4 -i gene_trees.nwk -o species.tre 2> species.log;                 echo "astral -t 4 exit $?"
astral -u 2 -i gene_trees.nwk -o species_annot.tre 2> species_annot.log;     echo "astral -u 2 exit $?"
astral --root "$OUT" -i gene_trees.nwk -o species_rooted.tre 2> species_rooted.log; echo "astral --root exit $?"
astral -i loci.treefile -o species_uncontracted.tre 2> species_uncontracted.log;   echo "astral uncontracted exit $?"

echo "--- RF vs simulated species tree"
$PY $A/data/treetools.py rf $A/data/$S/species_true.nwk species_wastral.tre species.tre species_rooted.tre \
    species_uncontracted.tre concat.treefile

echo "--- Skill CF command as written"
iqtree2 -te species.tre --gcf gene_trees.nwk -s $A/data/$S/concat.fasta --scfl 100 --prefix cf -T 4 \
    > cf_aswritten.stdout 2>&1; echo "as-written exit $?"; tail -1 cf_aswritten.stdout
echo "--- adapted (split) CF commands"
iqtree2 -t species.tre --gcf gene_trees.nwk --prefix cf_g > cf_g.stdout 2>&1;  echo "gcf exit $?"
iqtree2 -te species.tre -s $A/data/$S/concat.fasta --scfl 100 -T 4 --seed 12345 --prefix cf_s > cf_s.stdout 2>&1
echo "scfl exit $?"
echo "--- species.tre splits (localPP)"; $PY $A/data/treetools.py splits species.tre
echo "--- concat.treefile splits (UFBoot)"; $PY $A/data/treetools.py splits concat.treefile
echo "--- gCF"; grep -v '^#' cf_g.cf.stat
echo "--- sCF"; grep -v '^#' cf_s.cf.stat
echo "--- -u 2 annotations"; $PY $A/data/treetools.py splits species_annot.tre
