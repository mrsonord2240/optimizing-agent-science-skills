# AUDITOR CHECK for the Skill's trimming-accuracy claims: 10 SYNTHETIC replicate single protein genes (15 taxa, same
# true tree, AliSim indel rate 0.05) -> untrimmed vs ClipKIT smart-gap / kpic-smart-gap / trimAl 1.4.1 -strictplus / -gappyout.
# Fixed model LG+G4, 1 thread, no bootstrap (accuracy only).
set -u
export PATH=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools/bin:/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/Scripts:$PATH
TRIMAL=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools/trimal_v1.4.1/trimal.exe
cd "$(dirname "$0")"
for i in 01 02 03 04 05 06 07 08 09 10; do
  cp ../../data/reps/rep$i.aln.fasta rep$i.untrimmed.fasta
  clipkit rep$i.untrimmed.fasta -m smart-gap      -o rep$i.smartgap.fasta -q
  clipkit rep$i.untrimmed.fasta -m kpic-smart-gap -o rep$i.kpicsg.fasta -q
  clipkit rep$i.untrimmed.fasta -m kpi-smart-gap  -o rep$i.kpisg.fasta -q
  $TRIMAL -in rep$i.untrimmed.fasta -out rep$i.strictplus.fasta -strictplus
  $TRIMAL -in rep$i.untrimmed.fasta -out rep$i.gappyout.fasta -gappyout
  for m in untrimmed smartgap kpicsg kpisg strictplus gappyout; do
    iqtree2 -s rep$i.$m.fasta -m LG+G4 -T 1 --seed 1 --prefix t_rep$i.$m -redo -quiet
  done
done
PYTHONIOENCODING=utf-8 python reps_summary.py | tee reps_summary.out
