#!/bin/bash
# END-TO-END on MY planted HiFi 3v3 design (60 genes, 20 planted DTU): the SKILL's FLAIR block runs VERBATIM on the merged BAM of 6 samples
# (correct -> collapse -> quantify -> diffSplice --test). The SKILL says --test needs an Rscript with DRIMSeq/argparse/data.table: a wrapper on PATH points at env as-lr-drim.
R=/mnt/openscience/audits/bio-long-read-splicing/run; D=$R/data/plant; B=$R/out/blocks; O=$R/out/hifi6; rm -rf $O; mkdir -p $O; cd $O
export PYTHONDONTWRITEBYTECODE=1
mkdir -p /tmp/drimbin; printf '#!/bin/bash
exec /home/sci/micromamba/envs/as-lr-drim/bin/Rscript "$@"
' > /tmp/drimbin/Rscript; chmod +x /tmp/drimbin/Rscript; export PATH=/tmp/drimbin:$PATH
which Rscript
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
