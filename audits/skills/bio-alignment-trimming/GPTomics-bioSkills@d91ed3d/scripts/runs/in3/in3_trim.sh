# Input 3 (Edge) -- SYNTHETIC unbalanced alignment: 30 shallow ingroup taxa + 3 distant outgroups, 1,000 nt DNA (AliSim + MAFFT).
# Skill: kpic failure mode on unbalanced datasets -> run kpic-smart-gap AND verify outgroup branch length, consider smart-gap.
set -u
export PATH=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools/bin:/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/Scripts:$PATH
cd "$(dirname "$0")"
cp ../../data/unbal33_linsi.fasta input.fasta
for m in kpic-smart-gap smart-gap; do
  clipkit input.fasta -m $m --log -o unbal_$m.fasta > clip_$m.out 2>&1; echo "clipkit $m exit $?"; grep -E "Number of sites kept|Percentage" clip_$m.out
done
iqtree2 -s input.fasta              -m MFP -B 1000 -T 4 --seed 1 --prefix untrimmed -redo -quiet; echo "untrimmed exit $?"
iqtree2 -s unbal_kpic-smart-gap.fasta -m MFP -B 1000 -T 4 --seed 1 --prefix kpic   -redo -quiet; echo "kpic exit $?"
iqtree2 -s unbal_smart-gap.fasta    -m MFP -B 1000 -T 4 --seed 1 --prefix smartgap -redo -quiet; echo "smartgap exit $?"
PYTHONIOENCODING=utf-8 python in3_report.py
