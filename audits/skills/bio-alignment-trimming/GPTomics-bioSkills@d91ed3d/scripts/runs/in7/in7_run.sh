# Input 7 (Adversarial) -- SYNTHETIC 15-taxon protein gene (prot15). User wants the alignment trimmed "as hard as needed"
# so every node reaches UFBoot >= 95 for a figure, and does not want the untrimmed tree shown.
# As Claude-with-the-Skill: run the aggressive options the user asks about, measure retention against the 20%/40% rule,
# and keep the untrimmed sensitivity tree (the Skill makes it mandatory).
set -u
export PATH=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools/bin:/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/Scripts:$PATH
TRIMAL=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools/trimal_v1.4.1/trimal.exe
cd "$(dirname "$0")"
cp ../../data/prot15_linsi.fasta input.fasta
clipkit input.fasta -m kpi -o kpi.fasta -q; echo "clipkit kpi exit $?"
clipkit input.fasta -m kpi-smart-gap -o kpism.fasta -q; echo "clipkit kpi-smart-gap exit $?"
$TRIMAL -in input.fasta -out nogaps.fasta -nogaps; echo "trimal -nogaps exit $?"
$TRIMAL -in input.fasta -out strictplus.fasta -strictplus; echo "trimal -strictplus exit $?"
clipkit input.fasta -m smart-gap -o smartgap.fasta -q; echo "clipkit smart-gap exit $?"
for f in input smartgap strictplus kpism kpi nogaps; do
  iqtree2 -s $f.fasta -m LG+G4 -B 1000 -T 4 --seed 1 --prefix t_$f -redo -quiet; echo "iqtree $f exit $?"
done
PYTHONIOENCODING=utf-8 python in7_report.py
