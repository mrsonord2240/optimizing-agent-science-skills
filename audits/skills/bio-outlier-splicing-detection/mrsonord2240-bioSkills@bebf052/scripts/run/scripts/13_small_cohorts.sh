#!/bin/bash
# SKILL.md FRASER block verbatim (10_block_fraser.R) on patient + (n-1) controls subsets of cohort A, FRASER 2.6.1 (as-drop)
# usage: 13_small_cohorts.sh <n>
n=$1
R=/mnt/openscience/audits/bio-outlier-splicing-detection/run
D=$R/in3_n$n; rm -rf $D; mkdir -p $D/bams
cp $R/in1_drop/bams/PATIENT_001.bam* $D/bams/
k=$((n-1)); c=0
for f in $(ls $R/in1_drop/bams/S*.bam | sort); do
  [ $c -ge $k ] && break
  cp $f $f.bai $D/bams/; c=$((c+1))
done
ls $D/bams/*.bam | wc -l
cd $R; export PYTHONDONTWRITEBYTECODE=1
micromamba run -n as-drop Rscript scripts/10_block_fraser.R $D $R/blocks/01_r.R $R/data/synth small_n$n > logs/13_small_n$n.log 2>&1
grep -n "block finished\|small_n\|DETECTED\|not detected\|non-planted\|Error\|error" logs/13_small_n$n.log | cut -c1-200
