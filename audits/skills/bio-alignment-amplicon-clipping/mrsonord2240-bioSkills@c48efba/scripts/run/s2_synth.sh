#!/bin/bash
# Input 2 (Variant A): SYNTHETIC paired-end amplicon panel with planted truth (data/, made by make_synth.py).
# (a) Skill steps 1-3 for every flag set, (b) the shipped example from a COPY with CLIP_OPTS default / --strand / --both-ends,
# (c) planted-truth checker s2_check.py, (d) markdup claim (710 of 800), (e) claim "--strand alone: 200/800 3' residual".
set -u
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-amplicon-clipping/run
D=$R/data; W=$R/out/i2; rm -rf $W; mkdir -p $W; cd $W
BED=$D/synth_primers.bed; REF=$D/synth.fa; IN=$D/synth_pe.bam
pipeline() {  # SKILL steps 2-3 (sort -n | fixmate -m | sort ; calmd -b)
  samtools sort -n $1.raw.bam | samtools fixmate -m - - | samtools sort -o $1.sorted.bam -
  samtools calmd -b $1.sorted.bam $REF > $1.final.bam 2> $1.calmd.err
  samtools index $1.final.bam
}
for spec in "default:" "strand:--strand" "both:--both-ends" "both_strand:--both-ends --strand" "hard:--strand --hard-clip"; do
  tag=${spec%%:*}; flags=${spec#*:}
  echo "== mode $tag [$flags]"
  samtools ampliconclip $flags -b $BED $IN -o $tag.raw.bam 2>&1 | grep -E 'TOTAL CLIPPED|NOT CLIPPED|WRITTEN' | tr '\n' ' '; echo
  pipeline $tag
done
cp -r $R/skill $W/skillcopy; EX=$W/skillcopy/examples/ampliconclip_workflow.sh
echo "== SHIPPED EXAMPLE default CLIP_OPTS"
bash $EX $IN $BED $REF $W/ex_default.bam > ex_default.out 2>&1; echo "rc=$?"; tail -4 ex_default.out | cut -c1-150
echo "== SHIPPED EXAMPLE CLIP_OPTS=--strand"
CLIP_OPTS=--strand bash $EX $IN $BED $REF $W/ex_strand.bam > ex_strand.out 2>&1; echo "rc=$?"; tail -3 ex_strand.out | cut -c1-150
echo "== SHIPPED EXAMPLE CLIP_OPTS=--both-ends"
CLIP_OPTS=--both-ends bash $EX $IN $BED $REF $W/ex_both.bam > ex_both.out 2>&1; echo "rc=$?"; tail -3 ex_both.out | cut -c1-150
echo "== planted-truth check"
python $R/s2_check.py
echo "== checker on UNCLIPPED synthetic BAM (must flag; expect rc=1)"
python $W/skillcopy/examples/check_primer_residual.py $IN $BED --three-prime; echo "rc=$?"
echo "== markdup on raw amplicon BAM (Skill claim: 710 of 800)"
samtools sort -n -o n.bam $IN; samtools fixmate -m n.bam f.bam; samtools sort -o s.bam f.bam
samtools markdup -s s.bam md.bam 2>&1 | grep -E 'DUPLICATE PAIR|EXAMINED|WRITTEN'
