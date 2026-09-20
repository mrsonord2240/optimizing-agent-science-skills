#!/bin/bash
# in03 side check: does `samtools sort -T <missing dir>` fail when it has to spill (SKILL.md Common Errors row 5 says collate/sort -T)?
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
source /mnt/openscience/audits/bio-duplicate-handling/run/common.sh
cd $W/in03
samtools sort -n -m 1M -T nodir/sort -o o5.bam $D/HG00349.chr20_1400000-1500000.bam 2> e5c.txt; echo "sort -n -m 1M -T nodir/sort exit=$? : $(head -2 e5c.txt | tr '\n' ' ')"
samtools sort -m 1M -T nodir/sort -o o5.bam $D/HG00349.chr20_1400000-1500000.bam 2> e5d.txt; echo "sort -m 1M -T nodir/sort exit=$? : $(head -2 e5d.txt | tr '\n' ' ')"
