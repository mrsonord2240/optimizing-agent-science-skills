#!/bin/bash
export LC_ALL=C PYTHONIOENCODING=utf-8
R=/mnt/openscience/audits/bio-bam-statistics/run; cd $R/work; cp $AFDATA/human/test.rna.paired_end.sorted.bam rna5.bam; samtools index rna5.bam
python $R/n5_real_region.py 2>&1
echo "=== recipe block 017 (-aa) vs samtools coverage on the REAL RNA BAM and the 1000G slice region"
RN=$AFDATA/human/test.rna.paired_end.sorted.bam
sed "s#input.bam#$RN#" $R/blocks/017_bash.sh | bash; samtools coverage $RN | cut -f1-7
sed "s#input.bam#$AFDATA/1000g/HG00349.chr20_1400000-1500000.bam#; s#samtools depth -aa#samtools depth -a -r chr20:1400001-1500000#" $R/blocks/017_bash.sh | bash
samtools coverage -r chr20:1400001-1500000 $AFDATA/1000g/HG00349.chr20_1400000-1500000.bam | cut -f1-7
