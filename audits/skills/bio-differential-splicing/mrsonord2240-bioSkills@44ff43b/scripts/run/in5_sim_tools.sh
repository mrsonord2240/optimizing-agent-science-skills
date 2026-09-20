#!/bin/bash
# Input 5 (stress): SYNTHETIC 120-gene exon-skipping simulation, 3v3, truth in data/sim/truth.tsv.
# Comparisons: A vs B (30 planted DS genes) and A vs C (null: no planted change). Tools run with the Skill's documented settings:
#   rMATS-turbo: -t single --readLength 50 --novelSS --cstat 0.05 (SKILL.md flags; single-end because the sim is single-end)
#   leafcutter: regtools -a 8 -m 50 -s XS -> leafcutter_cluster_regtools.py -m 50 -l 500000 -k True -> leafcutter_ds.R -i 3
export PYTHONDONTWRITEBYTECODE=1
AS=/mnt/openscience/audit-envs/alternative-splicing
LC=$AS/tools/src/leafcutter
CORE="micromamba run -n as-core"
RL="micromamba run -n as-rleaf"
R=/mnt/openscience/audits/bio-differential-splicing/run
S=$R/data/sim
W=$R/out/in5; rm -rf $W; mkdir -p $W; cd $W
for cmp in AvB AvC; do
  g1=A; g2=${cmp: -1}
  mkdir -p rmats_$cmp/tmp rmats_$cmp/out
  echo "=== rMATS $cmp"
  $CORE rmats.py --b1 $S/b_$g1.txt --b2 $S/b_$g2.txt --gtf $S/sim.gtf -t single --readLength 50 --libType fr-unstranded --nthread 4 --od rmats_$cmp/out --tmp rmats_$cmp/tmp --novelSS --cstat 0.05 > rmats_$cmp.log 2>&1
  echo "rc=$? SE rows: $(($(wc -l < rmats_$cmp/out/SE.MATS.JC.txt)-1))"
done
echo "=== leafcutter: junctions + clustering (all 9 BAMs)"
mkdir -p lc; cd lc
for s in A1 A2 A3 B1 B2 B3 C1 C2 C3; do $CORE regtools junctions extract -a 8 -m 50 -s XS $S/$s.bam -o $s.junc > /dev/null 2>&1; done
ls *.junc > juncfiles.txt
$CORE python $LC/clustering/leafcutter_cluster_regtools.py -j juncfiles.txt -o lc -m 50 -l 500000 -k True > cl.log 2>&1; echo "cluster rc=$?"
echo "intron rows: $(zcat lc_perind_numers.counts.gz | tail -n +2 | wc -l)"
printf 'A1\tA\nA2\tA\nA3\tA\nB1\tB\nB2\tB\nB3\tB\n' > groups_AvB.txt
printf 'A1\tA\nA2\tA\nA3\tA\nC1\tC\nC2\tC\nC3\tC\n' > groups_AvC.txt
for cmp in AvB AvC; do
  $RL Rscript $LC/scripts/leafcutter_ds.R --num_threads 4 -i 3 -o ds_$cmp lc_perind_numers.counts.gz groups_$cmp.txt > ds_$cmp.log 2>&1
  echo "leafcutter_ds $cmp rc=$?; clusters tested: $(grep -c Success ds_${cmp}_cluster_significance.txt); not tested: $(grep -vc Success ds_${cmp}_cluster_significance.txt)"
done
echo "--- status values in AvB:"; cut -f1 ds_AvB_cluster_significance.txt | sort | uniq -c
cd ..
echo "=== evaluate against truth"
$CORE python $R/eval_sim.py $S/truth.tsv $W
