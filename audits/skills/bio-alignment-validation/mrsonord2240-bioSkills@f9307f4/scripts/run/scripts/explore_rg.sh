#!/bin/bash
cd /mnt/openscience/audits/bio-alignment-validation/run/data/fp
for b in A B A_rg1; do echo "$b: $(samtools view -H $b.bam | grep '^@RG')"; done
