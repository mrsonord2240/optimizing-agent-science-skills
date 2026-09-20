#!/bin/bash
# Related-Skills pointer in SKILL.md line 157: "pileup-generation - mpileup flags for amplicon (-aa -A -d 600000 -B)". Is that valid for samtools / bcftools mpileup?
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-amplicon-clipping/run; D=$R/data
echo "samtools mpileup:"; samtools mpileup -aa -A -d 600000 -B -f $D/synth.fa -r amp1:300-305 $D/synth_pe.bam 2>&1 | head -3 | cut -c1-100
echo "bcftools mpileup:"; bcftools mpileup -aa -A -d 600000 -B -f $D/synth.fa -r amp1:300-305 $D/synth_pe.bam 2>&1 | head -3 | cut -c1-140
