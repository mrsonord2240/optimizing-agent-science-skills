#!/bin/bash
# Input 7 cont.: is a wrong primer BED caught by the shipped example reliably? Three wrong BEDs on the real v5.3.2 nanopore BAM.
#  W1 v3.0.0 scheme (different scheme version), W2 v5.3.2 coordinates shifted +9 bp (wrong build/offset), W3 v3.0.0 with CLIP_OPTS=--strand.
set -u
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-amplicon-clipping/run; W=$R/out/i7b; rm -rf $W; mkdir -p $W; cd $W
cp -r $R/skill $W/skillcopy; EX=$W/skillcopy/examples/ampliconclip_workflow.sh
SC=$AFDATA/sarscov2; ART=$SC/sars-cov-2_v5.3.2.nanopore.bam; V5=$SC/v5.3.2.primer.bed; V3=$SC/v3.0.0.primer.bed
awk 'BEGIN{FS=OFS="\t"} {$2=$2+9; $3=$3+9; print}' $V5 > shift9.bed
try() { name=$1; bed=$2; shift 2; env "$@" bash $EX $ART $bed $SC/MN908947.3.fasta $W/$name.bam > $name.out 2>&1; rc=$?
  echo "$name: example rc=$rc | $(grep -aE 'TOTAL CLIPPED|NOT CLIPPED' $name.out | tr '\n' ' ') | $(grep -aE "5' end inside" $name.out | cut -c1-110)"; }
try W1_v3 $V3 CLIP_OPTS="--both-ends --strand"
try W2_shift9 $W/shift9.bed CLIP_OPTS="--both-ends --strand"
try W3_v3_strandonly $V3 CLIP_OPTS="--strand"
try CONTROL_v5 $V5 CLIP_OPTS="--both-ends --strand"
