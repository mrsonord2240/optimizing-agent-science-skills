#!/bin/bash
# Input 1c: the four flag combinations the Skill talks about, on the real ARTIC BAM. Prints ampliconclip's own stats.
set -u
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
W=/mnt/openscience/audits/bio-alignment-amplicon-clipping/run/out/i1; cd $W
SC=$AFDATA/sarscov2
IN=$SC/sars-cov-2_v5.3.2.nanopore.bam; BED=$SC/v5.3.2.primer.bed
run() { tag=$1; shift; echo "== $tag: samtools ampliconclip $* "; samtools ampliconclip "$@" -b $BED $IN -o m_$tag.bam 2>&1 | grep -E 'TOTAL CLIPPED|FORWARD|REVERSE|BOTH|NOT CLIPPED|WRITTEN'; }
run default
run strand --strand
run both --both-ends
run both_strand --both-ends --strand
run hard --strand --hard-clip
for t in default strand both both_strand hard; do
  echo "$t: H ops=$(samtools view m_$t.bam | awk '$6 ~ /H/' | wc -l)  reads=$(samtools view -c m_$t.bam)"
done
# ivar again for the both-ends comparison
samtools sort -o ivar_sorted.bam ivar_trim.bam
for t in strand both; do
  samtools ampliconclip $( [ $t = strand ] && echo --strand || echo --both-ends ) --clipped -b $BED $IN 2>/dev/null | samtools view - | awk '{print $1"\t"$2"\t"$4"\t"$6}' | sort > ac_$t.tsv
  echo "vs ivar [$t --clipped]: n=$(wc -l < ac_$t.tsv) identical(name,flag,pos,cigar)=$(comm -12 ivar.tsv ac_$t.tsv | wc -l)"
done
