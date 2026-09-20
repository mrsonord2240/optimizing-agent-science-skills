#!/bin/bash
# END-TO-END on MY planted HiFi 3v3 design (60 genes, 20 planted DTU): the SKILL's FLAIR block runs VERBATIM on the merged BAM of 6 samples
# (correct -> collapse -> quantify -> diffSplice --test). Then rMATS-long block verbatim on the 6 per-sample BAMs.
R=/mnt/openscience/audits/bio-long-read-splicing/run; D=$R/data/plant; B=$R/out/blocks; O=$R/out/hifi6; rm -rf $O; mkdir -p $O; cd $O
export PYTHONDONTWRITEBYTECODE=1
gffread $D/ref.gtf --bed -o annotation.bed12
S="ctrl1 ctrl2 ctrl3 trt1 trt2 trt3"
for s in $S; do
  minimap2 -ax splice:hq --secondary=no --junc-bed annotation.bed12 -t 8 $D/chrQ.fa $D/hifi/$s.fastq 2>/dev/null | samtools sort -o $s.bam - 2>/dev/null; samtools index $s.bam
done
samtools merge -f aligned.bam $(for s in $S; do echo $s.bam; done); samtools index aligned.bam
cp $D/chrQ.fa reference.fa; cp $D/ref.gtf gencode.v45.annotation.gtf; cp $D/SJ.out.tab SJ.out.tab
for s in $S; do cat $D/hifi/$s.fastq; done | gzip > sample.fastq.gz
: > reads_manifest.tsv; for s in $S; do c=${s%%[0-9]*}; printf '%s\t%s\tb0\t%s\n' $s $c $D/hifi/$s.fastq >> reads_manifest.tsv; done
cat reads_manifest.tsv
echo "########## FLAIR block VERBATIM (merged BAM)"
bash $B/flair-workflow-correct-collapse-quantify_1.sh > flair_block.log 2>&1; echo "rc=$?"
grep -a -E "Traceback|Error|exec failed|took" flair_block.log | head -8
echo "corrected reads $(wc -l < flair_corrected_all_corrected.bed), inconsistent $(wc -l < flair_corrected_all_inconsistent.bed), collapsed isoforms $(grep -c '>' flair_collapsed.isoforms.fa)"
head -2 flair_quantified.counts.tsv | cut -c1-200; ls flair_diffsplice
echo "########## rMATS-long block VERBATIM (6 per-sample BAMs named ctrl1..trt3, GTF annotation.gtf, samples.tsv prepared)"
mkdir -p rl; cd rl
for s in $S; do cp ../$s.bam ../$s.bam.bai .; done
cp $D/ref.gtf annotation.gtf
for s in $S; do printf '%s\talignment_info/%s.tsv\n' $s $s; done > samples.tsv
bash $B/rmats-long-for-differential-isoform-anal_1.sh > rmatslong_block.log 2>&1; echo "rc=$?"
grep -a -i -E "error|Traceback|No such" rmatslong_block.log | head -8
ls rmats_long_output 2>/dev/null | head -20
