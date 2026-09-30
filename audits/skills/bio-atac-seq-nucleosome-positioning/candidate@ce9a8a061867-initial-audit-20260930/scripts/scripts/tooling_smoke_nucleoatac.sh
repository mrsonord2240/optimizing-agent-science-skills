#!/bin/bash
# Skill recipe (method-reference "+1 nucleosome"): bedtools slop -l 200 -r 1000 on TSS BED -> nucleoatac run (shared atac-nucleo py2.7, read-only).
# Input: GM12878 rep1+rep2 merged (chr1:1-30Mb), GENCODE v29 protein-coding TSS chr1 10-20 Mb.
D=$ATACDATA; W=$NP/work/nucleoatac; mkdir -p $W; cd $W; rm -rf run1; mkdir run1; cd run1
samtools merge -f -@4 merged.bam $D/encode/GM12878_rep1_filtered.chr1_1-30000000.bam $D/encode/GM12878_rep2_filtered.chr1_1-30000000.bam && samtools index merged.bam
awk '$2>10000000 && $2<20000000' $D/annotation/gencode_v29_protein_coding_tss.chr1.bed | cut -f1-3 > tss.bed
echo "TSS: $(wc -l < tss.bed)"
bedtools slop -i tss.bed -g $D/reference/hg38.chr1.chrom.sizes -l 200 -r 1000 | sort -k1,1 -k2,2n | bedtools merge -i - > regions.bed
echo "regions: $(wc -l < regions.bed); min/max len: $(awk '{print $3-$2}' regions.bed | sort -n | sed -n '1p;$p' | tr '\n' ' ')"
export PATH=$SHARED/tools/bin:$PATH
( time nucleoatac run --bed regions.bed --bam merged.bam --fasta $D/reference/hg38.chr1.fa --out out --cores 8 ) > run.log 2>&1
echo "rc=$?"; tail -4 run.log | cut -c1-200
for f in out.*.gz; do echo "$f $(zcat $f | wc -l)"; done
