#!/bin/bash
# Input 1b: cross-check samtools ampliconclip against iVar trim (second, independent tool) on the real ARTIC BAM.
set -u
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
W=/mnt/openscience/audits/bio-alignment-amplicon-clipping/run/out/i1; cd $W
SC=$AFDATA/sarscov2
IN=$SC/sars-cov-2_v5.3.2.nanopore.bam; BED=$SC/v5.3.2.primer.bed
# iVar needs a sorted+indexed input, has quality trim on by default; disable (-q 0) and keep min length 1 so only primer logic differs
ivar trim -i $IN -b $BED -p ivar_trim -q 0 -m 1 2>&1 | tail -8
samtools sort -o ivar_sorted.bam ivar_trim.bam
samtools ampliconclip --strand --clipped -b $BED $IN -o ac_clipped_only.bam 2>&1 | grep -E 'WRITTEN|FILTERED|NOT'
samtools sort -o ac_sorted.bam ac_clipped_only.bam
echo "records: ivar=$(samtools view -c ivar_sorted.bam) ampliconclip --clipped=$(samtools view -c ac_sorted.bam)"
# per-read comparison: pos + cigar
samtools view ivar_sorted.bam | awk '{print $1"\t"$2"\t"$4"\t"$6}' | sort > ivar.tsv
samtools view ac_sorted.bam   | awk '{print $1"\t"$2"\t"$4"\t"$6}' | sort > ac.tsv
echo "identical (name,flag,pos,cigar) lines: $(comm -12 ivar.tsv ac.tsv | wc -l) of ivar=$(wc -l < ivar.tsv) ac=$(wc -l < ac.tsv)"
echo "only-in-ivar: $(comm -23 ivar.tsv ac.tsv | wc -l)  only-in-ampliconclip: $(comm -13 ivar.tsv ac.tsv | wc -l)"
comm -23 ivar.tsv ac.tsv | head -3; comm -13 ivar.tsv ac.tsv | head -3
# compare on (name,flag,pos) only, ignoring CIGAR text
cut -f1-3 ivar.tsv > a.t; cut -f1-3 ac.tsv > b.t
echo "same (name,flag,pos): $(comm -12 a.t b.t | wc -l)"
