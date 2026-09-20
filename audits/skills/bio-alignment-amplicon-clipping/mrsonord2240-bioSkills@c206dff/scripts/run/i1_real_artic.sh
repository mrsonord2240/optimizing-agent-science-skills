#!/bin/bash
# Input 1 (Canonical): real ARTIC v5.3.2 nanopore BAM + primer BED, Skill's "Basic ampliconclip Workflow" verbatim
# (strand-aware soft-clip -> sort -n | fixmate -m | sort -> calmd -b -> index), run from the audit's copy.
set -u
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-amplicon-clipping/run
W=$R/out/i1; rm -rf $W; mkdir -p $W; cd $W
SC=$AFDATA/sarscov2
IN=$SC/sars-cov-2_v5.3.2.nanopore.bam; BED=$SC/v5.3.2.primer.bed; REF=$SC/MN908947.3.fasta

echo "== input: reads / soft-clipped-5prime-start reads"
samtools view -c $IN
samtools view $IN | awk '$6 ~ /^[0-9]+S/' | wc -l

echo "== SKILL step 1 (verbatim)"
samtools ampliconclip --strand --soft-clip -b $BED $IN -o clipped.bam 2> clip_stderr.txt
cat clip_stderr.txt
samtools view -c clipped.bam
echo "-- is raw ampliconclip output coordinate-sorted? (samtools index)"
samtools index clipped.bam && echo "index OK" || echo "index FAILED"
samtools view -H clipped.bam | grep -E '^@HD|^@PG' | cut -c1-200 | tail -3

echo "== SKILL step 2 (verbatim)"
samtools sort -n clipped.bam | samtools fixmate -m - - | samtools sort -o sorted.bam -
echo "== SKILL step 3 (verbatim)"
samtools calmd -b sorted.bam $REF > clipped_final.bam
samtools index clipped_final.bam && echo "final index OK"
samtools view -c clipped_final.bam
echo "-- tags present in final (first 20 distinct tag names)"
samtools view clipped_final.bam | cut -f12- | tr '\t' '\n' | cut -d: -f1 | sort | uniq -c
echo "-- tags present in INPUT"
samtools view $IN | cut -f12- | tr '\t' '\n' | cut -d: -f1 | sort | uniq -c
