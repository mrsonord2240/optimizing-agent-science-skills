#!/bin/bash
# Auditor chain (2026-09-15): per-locus gene trees exactly as the Skill writes them
#   iqtree2 -S loci_dir -m MFP -B 1000 -T AUTO --prefix loci
# with -T AUTO replaced by -T 4 (shared machine, 4-thread cap), plus a concatenated ML contrast per dataset.
# All inputs are SYNTHETIC (data/make_data.py).
export PATH=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools/bin:$PATH
A=/f/OpenScience/audits/bio-phylo-species-trees
declare -A IN=( [rad]=in1 [az]=in2 [short]=in3 [intro]=in4 [fam]=in5 )
for s in rad az short intro fam; do
  o=$A/runs/${IN[$s]}
  t0=$(date +%s)
  iqtree2 -S $A/data/$s/loci -m MFP -B 1000 -T 4 --seed 12345 --prefix $o/loci --quiet > $o/loci.stdout 2>&1
  echo "$s gene trees exit $? $(( $(date +%s) - t0 ))s" >> $A/runs/genetrees.log
done
for s in rad az short intro; do
  o=$A/runs/${IN[$s]}
  t0=$(date +%s)
  iqtree2 -s $A/data/$s/concat.fasta -m MFP -B 1000 -T 4 --seed 12345 --prefix $o/concat --quiet > $o/concat.stdout 2>&1
  echo "$s concat exit $? $(( $(date +%s) - t0 ))s" >> $A/runs/genetrees.log
done
echo DONE >> $A/runs/genetrees.log
