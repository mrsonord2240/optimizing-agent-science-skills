#!/bin/bash
cd /mnt/openscience/audits/bio-alignment-validation/run/data/fp
FA=/mnt/openscience/audit-envs/alignment-files/public-data/human/genome.fasta
echo "ref at 1968: $(samtools faidx $FA chr22:1968-1968 | tail -1)   (hap.txt line: $(grep -m1 site0 hap.txt))"
for b in A B H; do echo "$b @1968: $(samtools mpileup -f $FA -r chr22:1968-1968 -Q 0 -B $b.bam 2>/dev/null | cut -f4,5 | cut -c1-70)"; done
