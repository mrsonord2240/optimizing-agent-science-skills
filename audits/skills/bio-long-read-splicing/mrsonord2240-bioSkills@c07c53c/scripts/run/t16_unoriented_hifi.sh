#!/bin/bash
# SKILL claim: unoriented HiFi + `splice:hq -uf` -> ~29% of reads with a false junction. Make my planted HiFi ctrl1 reads UNORIENTED (each read reverse-complemented with p=0.5)
# and align with/without -uf (with --junc-bed as in the recipe).
R=/mnt/openscience/audits/bio-long-read-splicing/run; D=$R/data/plant; O=$R/out/uf; cd $O; export PYTHONDONTWRITEBYTECODE=1
asenv as-lr python - <<PY
import random
rnd = random.Random(7); comp = str.maketrans("ACGT", "TGCA")
out = open("hifi_unoriented.fastq", "w"); L = open("$D/hifi/ctrl1.fastq").read().split("\n")
for i in range(0, len(L) - 3, 4):
    s = L[i + 1]
    if rnd.random() < 0.5: s = s.translate(comp)[::-1]
    out.write("%s\n%s\n+\n%s\n" % (L[i], s, L[i + 3]))
PY
ev() { asenv as-lr python $R/eval_bam.py "$1" $D/truth_chains.tsv "$2"; }
minimap2 -ax splice:hq --secondary=no --junc-bed annotation.bed12 -t 8 $D/chrQ.fa hifi_unoriented.fastq 2>/dev/null | samtools sort -o hu_nouf.bam - 2>/dev/null; samtools index hu_nouf.bam
minimap2 -ax splice:hq -uf --secondary=no --junc-bed annotation.bed12 -t 8 $D/chrQ.fa hifi_unoriented.fastq 2>/dev/null | samtools sort -o hu_uf.bam - 2>/dev/null; samtools index hu_uf.bam
ev hu_nouf.bam "unoriented HiFi splice:hq (no -uf)"; ev hu_uf.bam "unoriented HiFi splice:hq -uf"
echo "orientation check on the no--uf alignment: $(samtools view -F 2308 hu_nouf.bam | awk '{for(i=12;i<=NF;i++) if($i ~ /^ts:A:/){n++; if($i=="ts:A:+") p++}} END{printf "%.3f\n", p/n}')"
rm -f hifi_unoriented.fastq
