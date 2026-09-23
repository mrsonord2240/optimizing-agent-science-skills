#!/bin/bash
# INPUT 1 (Canonical, REAL data): "Get alignment statistics and coverage from my BAM" on the real human chr22-slice PE BAM and the real 1000G BAM
export LC_ALL=C PYTHONIOENCODING=utf-8
R=/mnt/openscience/audits/bio-bam-statistics/run; D=/mnt/openscience/audit-envs/alignment-files/public-data
H=$D/human/test.paired_end.sorted.bam; G=$D/1000g/HG00349.chr20_1400000-1500000.bam
cd $R/work
samtools --version | head -1
for B in $H $G; do
echo "################ $B"
echo "--- block 002/004 flagstat"; samtools flagstat $B
echo "--- flagstat -O tsv vs record-flag truth"; python $R/t1_check.py $B
echo "--- idxstats (block 006)"; samtools idxstats $B | head -5
echo "--- block 010 stats SN"; samtools stats $B | grep '^SN' | cut -f 2-5 | egrep 'raw total|reads mapped|properly paired|insert size average|bases mapped|error rate|inward|outward|other orient|average length'
echo "--- block 023 coverage"; samtools coverage $B | cut -f1-9 | awk 'NR<=3'
echo "--- block 005 summary table (verbatim, run in a dir holding only this BAM)"
rm -rf $R/work/sum && mkdir -p $R/work/sum && cp $B $R/work/sum/ && (cd $R/work/sum && bash <(sed -n '1,$p' $R/blocks/005_bash.sh) ; column -t summary.tsv)
done
echo "--- MT/X/Y idxstats recipes (block 008) on a chr22-only BAM: must exit 1 with a message, not print 0"
bash $R/rb.sh 8 $H
