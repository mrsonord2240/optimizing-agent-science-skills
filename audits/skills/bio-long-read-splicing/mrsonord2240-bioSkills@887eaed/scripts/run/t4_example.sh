#!/bin/bash
# Run the SHIPPED examples/longread_splicing_pipeline.sh (verbatim copy under run/skill_copy) end to end on MY planted reads, one platform.
# usage: t4_example.sh <hifi|ont|drna> [sj]   (sj = also pass SR_JUNCTIONS)
R=/mnt/openscience/audits/bio-long-read-splicing/run; D=$R/data/plant
PL=$1; SJ=${2:-}
case $PL in hifi) FQD=hifi;; ont) FQD=ontunstr;; drna) FQD=drna;; esac
O=$R/out/ex_${PL}${SJ}; rm -rf $O; mkdir -p $O; cd $O
export PYTHONDONTWRITEBYTECODE=1
cp $D/chrQ.fa reference.fa; cp $D/ref.gtf annotation.gtf; gzip -c $D/$FQD/ctrl1.fastq > ctrl1.fastq.gz
if [ -n "$SJ" ]; then export SR_JUNCTIONS=$D/SJ.out.tab; fi
PLATFORM=$PL REFERENCE=reference.fa GTF=annotation.gtf FASTQ=ctrl1.fastq.gz SAMPLE=ctrl1 THREADS=6 OUTPUT_DIR=$O/out \
  bash $R/skill_copy/examples/longread_splicing_pipeline.sh > example.log 2>&1
echo "example exit code: $?"
tail -8 example.log | cut -c1-240
