#!/bin/bash
# Input 5c: same SYNTHETIC sim, but n=2 vs n=2 (A1,A2 vs B1,B2 truth; A1,A2 vs C1,C2 null) - the design the Skill routes to Shiba/leafcutter.
export PYTHONDONTWRITEBYTECODE=1
AS=/mnt/openscience/audit-envs/alternative-splicing
LC=$AS/tools/src/leafcutter
CORE="micromamba run -n as-core"; RL="micromamba run -n as-rleaf"; SH="micromamba run -n as-shiba"
R=/mnt/openscience/audits/bio-differential-splicing/run
S=$R/data/sim
W=$R/out/in5c; rm -rf $W; mkdir -p $W; cd $W
for cmp in AvB AvC; do
  g2=${cmp: -1}
  echo "$S/A1.bam,$S/A2.bam" > b1_$cmp.txt; echo "$S/${g2}1.bam,$S/${g2}2.bam" > b2_$cmp.txt
  mkdir -p rmats_$cmp/tmp rmats_$cmp/out
  $CORE rmats.py --b1 b1_$cmp.txt --b2 b2_$cmp.txt --gtf $S/sim.gtf -t single --readLength 50 --libType fr-unstranded --nthread 4 --od rmats_$cmp/out --tmp rmats_$cmp/tmp --novelSS --cstat 0.05 > rmats_$cmp.log 2>&1; echo "rMATS $cmp rc=$?"
done
mkdir -p lc; cd lc
cp $R/out/in5/lc/lc_perind_numers.counts.gz .
printf 'A1\tA\nA2\tA\nB1\tB\nB2\tB\n' > groups_AvB.txt; printf 'A1\tA\nA2\tA\nC1\tC\nC2\tC\n' > groups_AvC.txt
for cmp in AvB AvC; do
  $RL Rscript $LC/scripts/leafcutter_ds.R --num_threads 4 -i 2 -g 2 -o ds_$cmp lc_perind_numers.counts.gz groups_$cmp.txt > ds_$cmp.log 2>&1
  echo "leafcutter $cmp rc=$? tested $(grep -c Success ds_${cmp}_cluster_significance.txt)"
done
cd ..
for cmp in AvB AvC; do
  g2=${cmp: -1}; mkdir -p shiba_$cmp; cd shiba_$cmp
  { printf 'sample\tbam\tgroup\ttechnology\n'; for i in 1 2; do printf 'A%s\t%s/A%s.bam\tRef\tshort\n' $i $S $i; printf '%s%s\t%s/%s%s.bam\tAlt\tshort\n' $g2 $i $S $g2 $i; done; } > exp.tsv
  cat > config.yaml <<CFG
workdir: $W/shiba_$cmp/out
gtf: $S/sim_shiba.gtf
experiment_table: $W/shiba_$cmp/exp.tsv
unannotated: False
minimum_anchor_length: 6
minimum_intron_length: 50
maximum_intron_length: 500000
strand: XS
only_psi: False
only_psi_group: False
fdr: 0.05
delta_psi: 0.1
reference_group: Ref
alternative_group: Alt
minimum_reads: 10
individual_psi: True
ttest: False
excel: False
CFG
  $SH shiba.py -p 4 --mame config.yaml > shiba.log 2>&1; echo "shiba $cmp rc=$?"; cd ..
done
$CORE python $R/eval_sim.py $S/truth.tsv $W
