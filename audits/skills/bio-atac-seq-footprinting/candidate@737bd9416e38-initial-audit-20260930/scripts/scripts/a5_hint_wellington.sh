#!/bin/bash
# A5: named-but-uncoded tools on real GM12878 ATAC chr1:10-13Mb (paired-end): HINT-ATAC; Wellington default vs -A (ATAC mode, documented nowhere in the Skill).
source /mnt/openscience/audits/bio-atac-seq-footprinting/initial-audit-20260930/scripts/common.sh
R=$W/a5; rm -rf $R; mkdir -p $R; cd $R
RD=/mnt/openscience/audit-envs/$P/rgtdata; export RGTDATA=$RD   # hand-built RGT data dir from the tooling pass (bioconda rgt ships none)
B=$D/encode/GM12878_rep1_filtered.chr1_1-30000000.bam
samtools view -b $B chr1:10000000-13000000 > w.bam; samtools index w.bam
zcat $D/encode/ENCFF346CZA.bed.gz | awk '$1=="chr1" && $2>10000000 && $3<13000000' | cut -f1-3 | head -60 > pk60.bed
mkdir -p hint_out wl_default wl_A
( time micromamba run -n $P-rgt rgt-hint footprinting --atac-seq --paired-end --organism=hg38 --output-location=hint_out --output-prefix=t w.bam pk60.bed ) > hint.log 2>&1; echo "hint rc=$?"
( time micromamba run -n $P-pydnase wellington_footprints.py pk60.bed w.bam wl_default ) > wl_default.log 2>&1; echo "wellington default rc=$?"
( time micromamba run -n $P-pydnase wellington_footprints.py -A pk60.bed w.bam wl_A ) > wl_A.log 2>&1; echo "wellington -A rc=$?"
wc -l hint_out/t.bed wl_default/*FDR*.bed wl_A/*FDR*.bed
head -3 hint_out/t.bed
