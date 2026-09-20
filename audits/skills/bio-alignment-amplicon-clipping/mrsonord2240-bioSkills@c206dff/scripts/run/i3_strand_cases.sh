#!/bin/bash
# Input 3 (Edge/semantics): what do --strand and --both-ends really do? (SYNTHETIC reads, planted geometry)
set -u
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-amplicon-clipping/run; D=$R/data; W=$R/out/i3; rm -rf $W; mkdir -p $W; cd $W
python $R/i3_strand_cases.py
for spec in "default:" "strand:--strand" "both:--both-ends" "both_strand:--both-ends --strand"; do
  tag=${spec%%:*}; flags=${spec#*:}
  samtools ampliconclip $flags -b $D/synth_primers.bed $D/strand_cases.bam 2>/dev/null | samtools view - | awk '{print $1"\t"$2"\t"$4"\t"$6}' | sort > $tag.tsv
done
echo "read | flag | orig(start,len) | default | --strand | --both-ends | --both-ends --strand   (pos:cigar, pos is 1-based)"
samtools view $D/strand_cases.bam | awk '{print $1"\t"$2"\t"$4":"$6}' | sort > orig.tsv
paste orig.tsv <(cut -f3,4 default.tsv | tr '\t' ':') <(cut -f3,4 strand.tsv | tr '\t' ':') <(cut -f3,4 both.tsv | tr '\t' ':') <(cut -f3,4 both_strand.tsv | tr '\t' ':')
echo
echo "== E1: Skill's own BED example is 5-column with strand in col 5 (chr1 100 125 primer_1_F +). Same primers, strand moved to col 5:"
awk 'BEGIN{OFS="\t"}{print $1,$2,$3,$4,$6}' $D/synth_primers.bed > $D/synth_primers_5col.bed
head -2 $D/synth_primers_5col.bed
samtools ampliconclip --strand -b $D/synth_primers_5col.bed $D/synth_pe.bam -o e1.bam 2>&1 | tail -12; echo "exit=${PIPESTATUS[0]}"
samtools view e1.bam 2>/dev/null | awk '$6 ~ /S/' | wc -l
