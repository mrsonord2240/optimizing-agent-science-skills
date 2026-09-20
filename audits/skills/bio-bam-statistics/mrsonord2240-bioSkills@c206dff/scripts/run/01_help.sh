#!/bin/bash
# Step: verify flags/claims against installed tool help (samtools 1.24, mosdepth, bcftools)
cd /mnt/openscience/audits/bio-bam-statistics/run
O=out/01_help.txt; : > $O
{
echo "### samtools version"; samtools --version | head -2
echo "### samtools depth (usage)"; samtools depth </dev/null 2>&1 | head -60
echo "### samtools coverage (usage)"; samtools coverage -h </dev/null 2>&1 | head -60
echo "### samtools flagstat (usage)"; samtools flagstat </dev/null 2>&1 | head -20
echo "### samtools stats (usage)"; samtools stats -h </dev/null 2>&1 | head -70
echo "### samtools mpileup (usage)"; samtools mpileup -h </dev/null 2>&1 | grep -E -- '-d|-x|overlap|depth' 
echo "### bcftools mpileup"; bcftools mpileup -h </dev/null 2>&1 | grep -E -- 'overlap|max-depth'
echo "### mosdepth"; mosdepth --help 2>&1 | head -50
echo "### samtools idxstats usage"; samtools idxstats </dev/null 2>&1 | head
echo "### plot-bamstats"; plot-bamstats -h </dev/null 2>&1 | head -30
} >> $O 2>&1
wc -l $O
