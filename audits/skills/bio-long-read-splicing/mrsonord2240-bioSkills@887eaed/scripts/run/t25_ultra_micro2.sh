#!/bin/bash
# SKILL "Other routes": uLTRA 0.1 with an annotation containing the exon (uLTRA pipeline --isoseq | --ont, output uLTRA_out/reads.sam) on MY micro2 set (12 microexons 3-27 nt + 2 tandem pairs), two-way check.
R=/mnt/openscience/audits/bio-long-read-splicing/run; D=$R/data/micro2; O=$R/out/ultra_micro2; rm -rf $O; mkdir -p $O; cd $O; export PYTHONDONTWRITEBYTECODE=1
for P in hifi ontunstr drna; do
  if [ $P = hifi ]; then MODE=--isoseq; else MODE=--ont; fi
  ( micromamba run -n as-sqanti uLTRA pipeline $MODE --t 6 $D/chrM2.fa $D/ref_full.gtf $D/$P.fastq ultra_$P > ultra_$P.log 2>&1 ); echo "uLTRA $P rc=$? files: $(ls ultra_$P | tr '\n' ' ')"
  samtools sort -o ultra_$P.bam ultra_$P/reads.sam 2>/dev/null; samtools index ultra_$P.bam
  asenv as-lr python $R/micro2_eval.py ultra_$P.bam $D/truth_chains.tsv "$P uLTRA (annotation has the exon)"
done
