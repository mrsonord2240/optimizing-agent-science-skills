#!/usr/bin/env bash
# Probe which envs carry an aligner usable for building a realistic paired BAM.
for e in /home/sci/micromamba/envs/*; do
  hits=$(ls "$e/bin" 2>/dev/null | grep -xE 'bwa|bowtie2|bwa-mem2|wgsim' | tr '\n' ' ')
  [ -n "$hits" ] && echo "$(basename "$e"): $hits"
done
ls /mnt/openscience/audit-envs/atac-seq/public-data/reference/bt2
