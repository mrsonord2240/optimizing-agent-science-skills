#!/bin/bash
# independent check of the Skill's "WRONG" pipe statement (harness in t04 mis-parsed PIPESTATUS)
cd /mnt/openscience/audits/bio-pileup-generation/run
set -o pipefail
samtools mpileup -f data/syn.fa data/syn.bam 2>/dev/null | bcftools call -mv > work/wrong.out 2> work/wrong.err
echo "pipeline rc=$?"; echo "stdout bytes: $(wc -c < work/wrong.out)"; echo "stderr:"; cat work/wrong.err
bcftools mpileup -f data/syn.fa data/syn.bam 2>/dev/null | bcftools call -mv 2>/dev/null | grep -vc '^#' | sed 's/^/RIGHT pipe records: /'
