#!/bin/bash
# Input 5 add-on: SKILL.md tag table says MD:Z / NM:i are "Not needed by bcftools mpileup or mapDamage (output identical
# with MD/NM stripped)". mpileup is covered in regress/in5.py; this checks mapDamage 2.2.2 (side env) on the real human BAM.
cd /mnt/openscience/audits/bio-sam-bam-basics/run
D=$AFDATA/human
W=data/md
rm -rf $W; mkdir -p $W
samtools view -h -x MD -x NM $D/test.paired_end.sorted.bam | samtools view -b -o $W/stripped.bam -
echo "MD/NM tags left in stripped BAM: $(samtools view $W/stripped.bam | grep -c 'MD:Z')  (original: $(samtools view $D/test.paired_end.sorted.bam | grep -c 'MD:Z'))"
mapDamage -i $D/test.paired_end.sorted.bam -r $D/genome.fasta -d $W/orig --no-stats > $W/orig.log 2>&1; echo "orig rc=$?"
mapDamage -i $W/stripped.bam -r $D/genome.fasta -d $W/strip --no-stats > $W/strip.log 2>&1; echo "stripped rc=$?"
tail -2 $W/orig.log; tail -2 $W/strip.log
ls $W/orig | head -5
for f in misincorporation.txt dnacomp.txt lgdistribution.txt; do
  a=$(grep -v '^#' $W/orig/$f | md5sum | cut -d' ' -f1); b=$(grep -v '^#' $W/strip/$f | md5sum | cut -d' ' -f1)
  n=$(grep -vc '^#' $W/orig/$f)
  echo "$f body rows=$n md5 orig=$a stripped=$b same=$([ "$a" = "$b" ] && echo yes || echo NO)"
done
rm -rf $W
