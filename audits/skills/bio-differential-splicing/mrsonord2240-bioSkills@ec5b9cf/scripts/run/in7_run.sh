#!/bin/bash
# INPUT 7 (adversarial, NEW data): batch-confounded design on SYNTHETIC sim2b: S1-S4 (group 0) vs S5-S8 (group 1), batch = 1,1,1,2 | 1,2,2,2 (imbalanced),
# 20 null SE genes carry a +-2.0 logit batch shift in batch 2 (batch-driven false-positive candidates), 16 SE + 12 A5/A3 planted true DS genes, RIN random.
# WSL part: rMATS 4v4 and 3v3 (S1,S2,S4 vs S5,S6,S8), leafcutter without covariates / with batch column / with batch = group column.
# The statistics (Skill's logit_psi ~ group + C(batch) + RIN snippet run verbatim, aliasing check, PCA) are in in7_analyze.py (Windows venv, statsmodels 0.15.0).
source /mnt/openscience/audits/bio-differential-splicing/run/common.sh
S=$R/data/sim2b
W=$R/out/in7; rm -rf $W; mkdir -p $W; cd $W
for d in 4v4 3v3; do
  mkdir -p rmats_$d/tmp rmats_$d/out
  if [ $d = 4v4 ]; then echo "$S/S1.bam,$S/S2.bam,$S/S3.bam,$S/S4.bam" > rmats_$d/b1.txt; echo "$S/S5.bam,$S/S6.bam,$S/S7.bam,$S/S8.bam" > rmats_$d/b2.txt
  else echo "$S/S1.bam,$S/S2.bam,$S/S4.bam" > rmats_$d/b1.txt; echo "$S/S5.bam,$S/S6.bam,$S/S8.bam" > rmats_$d/b2.txt; fi
  $CORE rmats.py --b1 rmats_$d/b1.txt --b2 rmats_$d/b2.txt --gtf $S/sim.gtf -t single --readLength 50 --libType fr-unstranded --nthread 6 --od rmats_$d/out --tmp rmats_$d/tmp --novelSS --cstat 0.05 > rmats_$d.log 2>&1
  echo "rMATS $d rc=$? SE rows $(($(wc -l < rmats_$d/out/SE.MATS.JC.txt)-1))"
done
echo "=== leafcutter"
mkdir -p lc; cd lc
for s in S1 S2 S3 S4 S5 S6 S7 S8; do PATH=$R/bin:$PATH regtools junctions extract -a 8 -m 50 -s XS $S/$s.bam -o $s.junc > /dev/null 2>&1; done
ls *.junc > juncfiles.txt
PATH=$R/bin:$PATH python $LC/clustering/leafcutter_cluster_regtools.py -j juncfiles.txt -o lc -m 50 -l 500000 -k True > cl.log 2>&1; echo "cluster rc=$?"
# groups files: col1 sample, col2 group, col3 covariate (b1/b2 labels as the Skill says for categorical variables)
printf 'S1\tG0\tb1\nS2\tG0\tb1\nS3\tG0\tb1\nS4\tG0\tb2\nS5\tG1\tb1\nS6\tG1\tb2\nS7\tG1\tb2\nS8\tG1\tb2\n' > groups_batch.txt
cut -f1,2 groups_batch.txt > groups_plain.txt
printf 'S1\tG0\tb1\nS2\tG0\tb1\nS3\tG0\tb1\nS4\tG0\tb1\nS5\tG1\tb2\nS6\tG1\tb2\nS7\tG1\tb2\nS8\tG1\tb2\n' > groups_conf.txt
printf 'S1	G0	0
S2	G0	0
S3	G0	0
S4	G0	0
S5	G1	1
S6	G1	1
S7	G1	1
S8	G1	1
' > groups_confnum.txt   # batch == group as a numeric 0/1 column
for v in plain batch conf confnum; do
  $RL Rscript $LC/scripts/leafcutter_ds.R --num_threads 4 -i 4 -g 4 -c 10 -o ds_$v lc_perind_numers.counts.gz groups_$v.txt > ds_$v.log 2>&1
  echo "leafcutter [$v] rc=$? tested $(ntested ds_${v}_cluster_significance.txt); p.adjust<0.05: $(nsig ds_${v}_cluster_significance.txt); warnings: $(grep -aci 'warn' ds_$v.log)"
  tail -2 ds_$v.log | cut -c1-200
done
cd ..
echo "=== statistics (Windows venv, statsmodels 0.15.0)"
