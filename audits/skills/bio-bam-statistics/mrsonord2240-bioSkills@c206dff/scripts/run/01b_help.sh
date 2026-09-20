#!/bin/bash
# Verify samtools mpileup / bcftools mpileup / plot-bamstats / depth flags claimed by the Skill
cd /mnt/openscience/audits/bio-bam-statistics/run
O=out/01b_help.txt; : > $O
{
echo "### samtools mpileup -d/-x lines"; samtools mpileup </dev/null 2>&1 | grep -E -i -- 'max-depth|overlap|-x,'
echo "### bcftools mpileup overlap lines"; bcftools mpileup </dev/null 2>&1 | grep -E -i -- 'overlap|max-depth'
echo "### samtools depth --max-depth attempt"; samtools depth -d 10 /mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.sorted.bam 2>&1 | head -3
echo "### samtools depth --max-depth long"; samtools depth --max-depth 10 /mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.sorted.bam 2>&1 | head -3
echo "### plot-bamstats -h"; plot-bamstats -h 2>&1 | head -30
echo "### samtools stats SN keys (human bam)"; samtools stats /mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.sorted.bam | grep '^SN' | cut -f2-3
} >> $O 2>&1
