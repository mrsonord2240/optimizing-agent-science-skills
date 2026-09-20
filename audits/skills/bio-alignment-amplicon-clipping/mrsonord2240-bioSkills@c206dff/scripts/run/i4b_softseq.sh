#!/bin/bash
# Soft-clip reversibility: SEQ length preserved and the original span recoverable from CIGAR (SYNTHETIC PE data).
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-amplicon-clipping/run; W=$R/out/i4
echo "orig mean SEQ len: $(samtools view $R/data/synth_pe.bam | awk '{s+=length($10)}END{print s/NR}')"
echo "soft mean SEQ len: $(samtools view $W/soft.final.bam | awk '{s+=length($10)}END{print s/NR}')"
echo "soft reads with S in CIGAR: $(samtools view $W/soft.final.bam | awk '$6~/S/' | wc -l) of $(samtools view -c $W/soft.final.bam)"
# same SEQ per read name/flag as the original?
samtools view $R/data/synth_pe.bam | awk '{print $1"\t"$2"\t"$10}' | sort > $W/o.seq
samtools view $W/soft.final.bam | awk '{print $1"\t"$2"\t"$10}' | sort > $W/s.seq
echo "reads with byte-identical SEQ vs original: $(comm -12 $W/o.seq $W/s.seq | wc -l) of $(wc -l < $W/o.seq)"
