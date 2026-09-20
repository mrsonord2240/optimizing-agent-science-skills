#!/bin/bash
# Input 2 (Variant A): Skill workflow on SYNTHETIC paired-end amplicon data with planted truth, all flag modes,
# plus the shipped example script run from the copy of the Skill.
set -u
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-amplicon-clipping/run
D=$R/data; W=$R/out/i2; rm -rf $W; mkdir -p $W; cd $W
BED=$D/synth_primers.bed; REF=$D/synth.fa; IN=$D/synth_pe.bam

pipeline() {  # SKILL steps 2-3 verbatim
  samtools sort -n $1.raw.bam | samtools fixmate -m - - | samtools sort -o $1.sorted.bam -
  samtools calmd -b $1.sorted.bam $REF > $1.final.bam 2> $1.calmd.err
  samtools index $1.final.bam
}
for spec in "default:" "strand:--strand" "both:--both-ends" "both_strand:--both-ends --strand" "hard:--strand --hard-clip"; do
  tag=${spec%%:*}; flags=${spec#*:}
  echo "== mode $tag [$flags]"
  samtools ampliconclip $flags -b $BED $IN -o $tag.raw.bam 2>&1 | grep -E 'FORWARD|REVERSE|BOTH|NOT CLIPPED|WRITTEN'
  pipeline $tag
done
echo "== SHIPPED EXAMPLE (from copy): bash skill/examples/ampliconclip_workflow.sh in.bam bed ref out.bam"
cp -r $R/skill $W/skillcopy
( cd $W/skillcopy/examples && bash ampliconclip_workflow.sh $IN $BED $REF $W/example_out.bam ) 2>&1 | tail -8
echo "example rc=$?  out records: $(samtools view -c $W/example_out.bam)"
echo "== markdup on raw amplicon BAM (Skill claim: ~everything marked duplicate)"
samtools sort -n -o n.bam $IN; samtools fixmate -m n.bam f.bam; samtools sort -o s.bam f.bam
samtools markdup -s s.bam md.bam 2>&1 | grep -E 'DUPLICATE|EXAMINED|WRITTEN'
samtools flagstat md.bam | grep -E 'duplicates'
