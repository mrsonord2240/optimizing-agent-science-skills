#!/bin/bash
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
for t in picard bowtie2 qualimap featureCounts fastq_screen minimap2 bwa gtfToGenePred bedtools; do
  echo -n "$t: "; (which $t 2>/dev/null || echo none)
done
echo ---picard3; ls /home/sci/micromamba/envs/af-picard3/bin | grep -i picard
micromamba run -n af-picard3 picard CollectRnaSeqMetrics --version 2>&1 | tail -3
micromamba run -n as-maxent python -c "import maxentpy, sys; print(maxentpy.__file__)"
micromamba run -n as-maxent pip list 2>/dev/null | grep -i -E "maxent|pysam|pandas"
micromamba run -n as-core fastq_screen --version
micromamba run -n as-core fastq_screen --help | head -40
