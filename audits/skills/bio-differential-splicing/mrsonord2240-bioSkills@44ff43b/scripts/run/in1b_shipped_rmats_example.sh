#!/bin/bash
# Input 1b: run the shipped examples/diff_splicing_rmats.sh from a COPY, on the real chrX 2v2 paired-end data (75 nt, GRCh37).
# Run (i) exactly as shipped (READ_LENGTH=150) and (ii) with READ_LENGTH=75 only.
export PYTHONDONTWRITEBYTECODE=1
AS=/mnt/openscience/audit-envs/alternative-splicing
D=$AS/public-data/rnasplice
R=/mnt/openscience/audits/bio-differential-splicing/run
for v in shipped fixedlen; do
  W=$R/out/in1b_$v; rm -rf $W; mkdir -p $W; cd $W
  cp $R/skill/examples/diff_splicing_rmats.sh run.sh
  cp $D/reference/genes_chrX.gtf annotation.gtf
  echo "$D/bam/ERR188383.Aligned.out.bam,$D/bam/ERR188428.Aligned.out.bam" > condition1_bams.txt
  echo "$D/bam/ERR188454.Aligned.out.bam,$D/bam/ERR204916.Aligned.out.bam" > condition2_bams.txt
  [ $v = fixedlen ] && sed -i 's/^READ_LENGTH=150/READ_LENGTH=75/' run.sh
  echo "=== $v"
  grep -n '^READ_LENGTH' run.sh
  PATH=$AS/tools/bin:$PATH bash run.sh > run.log 2>&1; echo "rc=$?"
  tail -22 run.log | cut -c1-200
  echo "SE rows: $(($(wc -l < rmats_output/SE.MATS.JC.txt 2>/dev/null)-1))"
done
