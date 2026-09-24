#!/bin/bash
# Input 7 (Scope boundary / adversarial, NEW): shipped residual checker on planted residuals + wrong-scheme BED on real ARTIC data.
set -u
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-amplicon-clipping/run; D=$R/data; W=$R/out/i7; rm -rf $W; mkdir -p $W; cd $W
cp -r $R/skill $W/skillcopy; CK=$W/skillcopy/examples/check_primer_residual.py; EX=$W/skillcopy/examples/ampliconclip_workflow.sh
SC=$AFDATA/sarscov2; ART=$SC/sars-cov-2_v5.3.2.nanopore.bam; V5=$SC/v5.3.2.primer.bed; V3=$SC/v3.0.0.primer.bed
echo "=== (A) planted-residual unit cases (SYNTHETIC)"
python $R/s7_checker_tests.py $CK
echo "=== (B) checker on the UNCLIPPED real ARTIC BAM (must flag)"
python $CK $ART $V5 --three-prime; echo "rc=$?"
echo "=== (C) planted residual in a real clipped BAM"
samtools ampliconclip --both-ends --strand -b $V5 $ART -o cl.bam 2>/dev/null; samtools sort -o cl_s.bam cl.bam; samtools index cl_s.bam
python $CK cl_s.bam $V5 --three-prime; echo "clean clipped rc=$?"
python $R/s7_plant.py
python $CK planted.bam $V5 --three-prime; echo "planted rc=$? (expect 1 with exactly 1 residual 5')"
echo "=== (D) wrong primer-scheme BED (v3.0.0) on real v5.3.2 nanopore reads, through the shipped example"
bash $EX $ART $V3 $SC/MN908947.3.fasta $W/wrong_scheme.bam > ws.out 2>&1; echo "example rc=$?"; grep -aE 'TOTAL READS|TOTAL CLIPPED|NOT CLIPPED|primer|ERROR' ws.out | cut -c1-170
echo "-- control, right v5.3.2 BED"
bash $EX $ART $V5 $SC/MN908947.3.fasta $W/right_scheme.bam > rs.out 2>&1; echo "example rc=$?"; grep -aE 'TOTAL CLIPPED|NOT CLIPPED|primer|ERROR' rs.out | cut -c1-170
echo "-- wrong-scheme output judged against the RIGHT (v5.3.2) BED"
python $CK $W/wrong_scheme.bam $V5 --three-prime; echo "rc=$?"
echo "=== (E) checker throughput: 20x concatenated clipped ARTIC BAM"
for i in $(seq 20); do echo $W/cl_s.bam; done > bams.txt
samtools cat -b bams.txt -o big.bam 2>/dev/null; echo "reads: $(samtools view -c big.bam)"
( time python $CK big.bam $V5 --three-prime ) 2>&1 | grep -E 'mapped|real'
rm -f big.bam
