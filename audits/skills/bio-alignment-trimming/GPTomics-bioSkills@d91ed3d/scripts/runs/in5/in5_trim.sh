# Input 5 (Stress) -- SYNTHETIC deep protein supermatrix: 16 taxa x 12 genes (LG+G4, long terminal branches 0.4-1.0),
# AliSim + MAFFT L-INS-i. Compare every trimmer the Skill recommends for this case, apply the 20%/40% rule and the 0.7 cap,
# then check trees against the true tree.
set -u
export PATH=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools/bin:/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/Scripts:$PATH
T=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools
TRIMAL=$T/trimal_v1.4.1/trimal.exe
cd "$(dirname "$0")"
cp ../../data/deep_super/supermatrix.fasta input.fasta
for m in kpic-smart-gap smart-gap kpic-gappy kpi-smart-gap; do
  clipkit input.fasta -m $m -o clip_$m.fasta -q; echo "clipkit $m exit $?"
done
for m in strictplus automated1 gappyout strict; do
  $TRIMAL -in input.fasta -out trimal_$m.fasta -$m; echo "trimal -$m exit $?"
done
echo "== BMGE 1.12, Skill deep-prokaryotic setting -h 0.4 -g 0.2"
java -jar $T/BMGE112.jar -i input.fasta -t AA -of bmge112_h04.fasta -h 0.4 -g 0.2 > bmge112_h04.out 2>&1; echo "exit $?"
echo "== BMGE 1.12, Skill AA command -h 0.5 -g 0.2"
java -jar $T/BMGE112.jar -i input.fasta -t AA -of bmge112_h05.fasta -h 0.5 -g 0.2 > bmge112_h05.out 2>&1; echo "exit $?"
echo "== BMGE 2.0, Skill AA command as written"
java -jar $T/BMGE200.jar -i input.fasta -t AA -of bmge200_skill.fasta -h 0.4 -g 0.2 > bmge200_skill.out 2>&1; echo "exit $? ; output exists: $(test -s bmge200_skill.fasta && echo yes || echo NO)"
echo "== BMGE 2.0 adapted (-e 0.4 -g 0.2, default BLOSUM30)"
java -jar $T/BMGE200.jar -i input.fasta -t AA -of bmge200_e04.fasta -e 0.4 -g 0.2 > bmge200_e04.out 2>&1; echo "exit $?"
echo "== Gblocks: no Windows build obtainable (download host unreachable) -> not executed"
PYTHONIOENCODING=utf-8 python in5_retention.py
for f in input clip_kpic-smart-gap clip_smart-gap clip_kpic-gappy clip_kpi-smart-gap trimal_strictplus trimal_automated1 trimal_gappyout bmge112_h04 bmge112_h05 bmge200_e04; do
  iqtree2 -s $f.fasta -m LG+G4 -B 1000 -T 4 --seed 1 --prefix tree_$f -redo -quiet; echo "iqtree $f exit $?"
done
PYTHONIOENCODING=utf-8 python in5_trees.py
