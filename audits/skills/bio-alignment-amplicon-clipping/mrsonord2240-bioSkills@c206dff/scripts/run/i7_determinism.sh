#!/bin/bash
# T3 determinism: run the shipped example twice (THREADS=4 and THREADS=1) on the real ARTIC BAM and compare record bodies.
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-amplicon-clipping/run; W=$R/out/i7; rm -rf $W; mkdir -p $W; cd $W
SC=$AFDATA/sarscov2; cp -r $R/skill $W/skillcopy
for t in 4 1 4; do THREADS=$t bash $W/skillcopy/examples/ampliconclip_workflow.sh $SC/sars-cov-2_v5.3.2.nanopore.bam $SC/v5.3.2.primer.bed $SC/MN908947.3.fasta $W/run_$t_$RANDOM.bam >/dev/null 2>&1; echo "run THREADS=$t exit $?"; done
for f in $W/run_*.bam; do echo "$(samtools view $f | md5sum | cut -c1-12) records=$(samtools view -c $f) $(basename $f)"; done
echo "-- real-data example run: MD present on $(samtools view $(ls $W/run_*.bam | head -1) | grep -c 'MD:Z') reads; index exists: $(ls $W/run_*.bam.bai | wc -l)"
