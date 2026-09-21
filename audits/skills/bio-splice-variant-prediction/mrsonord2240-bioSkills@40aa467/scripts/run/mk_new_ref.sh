#!/bin/bash
# build hg38 chr7+chr17 upper-case FASTA and GENCODE v45 GTF subsets for the NEW inputs (reaudit scratch)
S=/mnt/openscience/as-spvp-reaudit-scratch; G=/mnt/openscience/as-spvp-scratch/g38
cd $S
zcat chr7.fa.gz | awk '/^>/{print;next}{print toupper($0)}' > hg38_chr7_chr17.upper.fa
awk '/^>chr17$/{p=1} p&&/^>chrX$/{p=0} p{print}' $G/hg38_chr17_chrX.upper.fa >> hg38_chr7_chr17.upper.fa
grep '^>' hg38_chr7_chr17.upper.fa
micromamba run -n as-spvp python -c "
from pyfaidx import Fasta
f=Fasta('hg38_chr7_chr17.upper.fa'); print({k:len(f[k]) for k in f.keys()})"
zcat $G/gencode.v45.annotation.gtf.gz | awk '/^#/||$1=="chr7"||$1=="chr17"' > gencode.v45.chr7_17.gtf
zcat $G/gencode.v45.annotation.gtf.gz | awk '/^#/||(($1=="chr7"||$1=="chr17")&&/tag "basic"/)||(($1=="chr7"||$1=="chr17")&&$3=="gene")' > gencode.v45.chr7_17.basic.gtf
wc -l gencode.v45.chr7_17.gtf gencode.v45.chr7_17.basic.gtf
