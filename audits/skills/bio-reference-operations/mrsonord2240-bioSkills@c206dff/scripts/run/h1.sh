#!/bin/bash
# help pages of the tools the Skill references (flag verification)
samtools --version | head -2
for c in faidx dict consensus reheader; do echo "=========== samtools $c"; samtools $c --help 2>&1 | head -90; done
echo "=========== seq_cache_populate"
which seq_cache_populate.pl
ls /home/sci/micromamba/envs/alignment-files/bin | grep -i -E 'seq_cache|cache'
ls /home/sci/micromamba/envs/alignment-files/share 2>/dev/null | grep -i -E 'samtools|htslib'
