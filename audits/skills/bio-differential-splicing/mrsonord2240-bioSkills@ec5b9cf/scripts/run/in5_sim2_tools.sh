#!/bin/bash
# INPUT 5 (stress, NEW data): SYNTHETIC sim2 (100 genes; SE + A5SS + A3SS; 28 strong / 8 moderate / 6 weak planted; null incl. overdispersed and low-coverage genes),
# 6 replicates per group. Designs n = 1, 2, 3, 4, 6 per group, A vs B (planted truth) and A vs C (NULL, independent replicates of A).
# Tools with the FIXED Skill's settings: rMATS (-t single --readLength 50 --novelSS --cstat 0.05, Skill coverage filter), leafcutter (-i n -g n -c 10, -k True),
# Shiba (n = 2, 4, 6; Skill config keys, XS). Also: leafcutter at 6v6 with the Skill's rule (-i 6 -g 6) vs the shipped example's cap (-i 5 -g 5) vs defaults.
source /mnt/openscience/audits/bio-differential-splicing/run/common.sh
S=$R/data/sim2
W=$R/out/in5; rm -rf $W; mkdir -p $W; cd $W

echo "=== leafcutter clustering on all 18 BAMs (regtools -a 8 -m 50 -s XS; clustering -m 50 -l 500000 -k True)"
mkdir -p lc_all; cd lc_all
for s in A1 A2 A3 A4 A5 A6 B1 B2 B3 B4 B5 B6 C1 C2 C3 C4 C5 C6; do PATH=$R/bin:$PATH regtools junctions extract -a 8 -m 50 -s XS $S/$s.bam -o $s.junc > /dev/null 2>&1; done
ls *.junc > juncfiles.txt
PATH=$R/bin:$PATH python $LC/clustering/leafcutter_cluster_regtools.py -j juncfiles.txt -o lc -m 50 -l 500000 -k True > cl.log 2>&1; echo "cluster rc=$? intron rows: $(zcat lc_perind_numers.counts.gz | tail -n +2 | wc -l)"
cd ..

lst() { local g=$1 n=$2 pre=$3; local o=""; for i in $(seq 1 $n); do o="$o,$pre$g$i${4}"; done; echo "${o#,}"; }

run_n() {
  local n=$1
  local N=$W/n$n; mkdir -p $N
  for cmp in AvB AvC; do
    local g2=${cmp: -1}
    mkdir -p $N/rmats_$cmp/tmp $N/rmats_$cmp/out
    lst A $n "$S/" .bam > $N/rmats_$cmp/b1.txt; lst $g2 $n "$S/" .bam > $N/rmats_$cmp/b2.txt
    micromamba run -n as-core rmats.py --b1 $N/rmats_$cmp/b1.txt --b2 $N/rmats_$cmp/b2.txt --gtf $S/sim.gtf -t single --readLength 50 --libType fr-unstranded --nthread 3 --od $N/rmats_$cmp/out --tmp $N/rmats_$cmp/tmp --novelSS --cstat 0.05 > $N/rmats_$cmp.log 2>&1
    echo "n=$n rMATS $cmp rc=$? SE rows $(($(wc -l < $N/rmats_$cmp/out/SE.MATS.JC.txt)-1)) A5SS $(($(wc -l < $N/rmats_$cmp/out/A5SS.MATS.JC.txt)-1)) A3SS $(($(wc -l < $N/rmats_$cmp/out/A3SS.MATS.JC.txt)-1))"
  done
  if [ $n -ge 2 ]; then
    mkdir -p $N/lc; cp $W/lc_all/lc_perind_numers.counts.gz $N/lc/
    for cmp in AvB AvC; do
      local g2=${cmp: -1}
      { for i in $(seq 1 $n); do printf 'A%s\tA\n' $i; done; for i in $(seq 1 $n); do printf '%s%s\t%s\n' $g2 $i $g2; done; } > $N/lc/groups_$cmp.txt
      local ig=$n; [ $n -gt 6 ] && ig=6
      micromamba run -n as-rleaf Rscript $LC/scripts/leafcutter_ds.R --num_threads 3 -i $ig -g $ig -c 10 -o $N/lc/ds_$cmp $N/lc/lc_perind_numers.counts.gz $N/lc/groups_$cmp.txt > $N/lc/ds_$cmp.log 2>&1
      echo "n=$n leafcutter $cmp (-i $ig -g $ig -c 10) rc=$? tested $(grep -c Success $N/lc/ds_${cmp}_cluster_significance.txt 2>/dev/null)"
    done
  fi
  if [ $n -eq 2 ] || [ $n -eq 4 ] || [ $n -eq 6 ]; then
    for cmp in AvB AvC; do
      local g2=${cmp: -1}
      mkdir -p $N/shiba_$cmp;
      { printf 'sample\tbam\tgroup\ttechnology\n'; for i in $(seq 1 $n); do printf 'A%s\t%s/A%s.bam\tRef\tshort\n' $i $S $i; done; for i in $(seq 1 $n); do printf '%s%s\t%s/%s%s.bam\tAlt\tshort\n' $g2 $i $S $g2 $i; done; } > $N/shiba_$cmp/exp.tsv
      cat > $N/shiba_$cmp/config.yaml <<CFG
workdir: $N/shiba_$cmp/out
gtf: $S/sim_shiba.gtf
experiment_table: $N/shiba_$cmp/exp.tsv
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
      ( cd $N/shiba_$cmp; micromamba run -n as-shiba shiba.py -p 3 --mame config.yaml > shiba.log 2>&1; echo "n=$n Shiba $cmp rc=$? files: $(ls out/results/splicing 2>/dev/null | wc -l)" )
    done
  fi
}
for n in 1 2 3 4 6; do run_n $n > $W/log_n$n.txt 2>&1 & done
wait
cat $W/log_n*.txt

echo "=== leafcutter 6v6: Skill rule (-i 6 -g 6 -c 10) vs shipped-example cap (-i 5 -g 5 -c 10) vs defaults (-i 5 -g 3 -c 20)"
N=$W/n6/lc
for cfg in "6 6 10" "5 5 10" "5 3 20"; do set -- $cfg
  for cmp in AvB AvC; do
    micromamba run -n as-rleaf Rscript $LC/scripts/leafcutter_ds.R --num_threads 6 -i $1 -g $2 -c $3 -o $N/x_${1}_${2}_${3}_$cmp $N/lc_perind_numers.counts.gz $N/groups_$cmp.txt > $N/x_${1}_${2}_${3}_$cmp.log 2>&1
    echo "6v6 -i $1 -g $2 -c $3 $cmp rc=$? clusters tested: $(ntested $N/x_${1}_${2}_${3}_${cmp}_cluster_significance.txt)  p.adjust<0.05: $(nsig $N/x_${1}_${2}_${3}_${cmp}_cluster_significance.txt)"
  done
done
echo "=== score against truth"
$CORE python $R/eval_sim2.py $S/truth.tsv $W 1 2 3 4 6 > $W/eval.txt 2>&1; cat $W/eval.txt
