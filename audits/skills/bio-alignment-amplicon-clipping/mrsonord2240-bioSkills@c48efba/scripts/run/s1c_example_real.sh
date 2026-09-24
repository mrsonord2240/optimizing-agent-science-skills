#!/bin/bash
# Input 1 cont.: shipped example on real ARTIC BAM from a COPY (default CLIP_OPTS, CLIP_OPTS=--strand, determinism THREADS 4/1/4),
# iVar help, checker timing.
set -u
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-amplicon-clipping/run
W=$R/out/i1c; rm -rf $W; mkdir -p $W; cd $W
cp -r $R/skill $W/skillcopy
SC=$AFDATA/sarscov2; EX=$W/skillcopy/examples/ampliconclip_workflow.sh
echo "== example, default CLIP_OPTS"
bash $EX $SC/sars-cov-2_v5.3.2.nanopore.bam $SC/v5.3.2.primer.bed $SC/MN908947.3.fasta $W/ex_default.bam > ex_default.out 2>&1; echo "rc=$?"; cat ex_default.out | cut -c1-200
echo "records $(samtools view -c ex_default.bam); MD $(samtools view ex_default.bam | grep -c 'MD:Z:'); index: $(ls ex_default.bam.bai)"
echo "== example, CLIP_OPTS=--strand (Skill says 3' primer stays)"
CLIP_OPTS=--strand bash $EX $SC/sars-cov-2_v5.3.2.nanopore.bam $SC/v5.3.2.primer.bed $SC/MN908947.3.fasta $W/ex_strand.bam > ex_strand.out 2>&1; echo "rc=$?"; tail -3 ex_strand.out | cut -c1-200
echo "== determinism: THREADS 4 / 1 / 4"
for t in 4 1 4b; do tt=${t%b}; THREADS=$tt bash $EX $SC/sars-cov-2_v5.3.2.nanopore.bam $SC/v5.3.2.primer.bed $SC/MN908947.3.fasta $W/det_$t.bam >/dev/null 2>&1; echo "THREADS=$tt rc=$?  record md5 $(samtools view $W/det_$t.bam | md5sum | cut -c1-12)"; done
echo "== example leaves temp files? (mktemp trap)"; ls /tmp | grep -c tmp\\. || true
echo "== iVar trim -h"; ivar trim -h 2>&1 | grep -aE '^ *-[a-z]' | head -14
echo "== checker timing on 4916 reads (193 primers)"
cp -r $R/skill/examples $W/ex2
time python $W/ex2/check_primer_residual.py $W/det_4.bam $SC/v5.3.2.primer.bed --three-prime
ls -la $W/skillcopy/examples $W/ex2 | grep -c pycache
