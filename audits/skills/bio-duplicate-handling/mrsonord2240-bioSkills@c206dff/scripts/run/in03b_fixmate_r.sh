#!/bin/bash
# Input 3 (part b): SKILL.md "Remove Secondary/Unmapped: samtools fixmate -r -m" and markdup -f/--json flags, real human BAM (2 secondary, 2 unmapped)
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
source /mnt/openscience/audits/bio-duplicate-handling/run/common.sh
cd $W; rm -rf in03b; mkdir in03b; cd in03b
H=$D/test.paired_end.sorted.bam
echo "input: $(samtools view -c $H) records; secondary $(samtools view -c -f 256 $H); unmapped $(samtools view -c -f 4 $H)"
samtools sort -n -o ns.bam $H; samtools fixmate -r -m ns.bam fr.bam
echo "fixmate -r -m output: $(samtools view -c fr.bam) records; secondary $(samtools view -c -f 256 fr.bam); unmapped $(samtools view -c -f 4 fr.bam)"
samtools sort -o fr.cs.bam fr.bam; samtools markdup -s fr.cs.bam fr.m.bam 2>&1 | grep -E 'EXCLUDED|EXAMINED|DUPLICATE TOTAL'
echo "flagged: $(samtools view -c -f 1024 fr.m.bam)  (without -r: 1656)"
samtools markdup --json fr.cs.bam j.bam 2>&1 | head -5
