#!/bin/bash
# SKILL.md Strand Balance: RSeQC infer_experiment.py -r genes.bed12 -i rna.bam (needs a BED12 gene model). One synthetic BED12 gene over the chr22 slice.
PD=/mnt/openscience/audit-envs/alignment-files/public-data; W=/mnt/openscience/audits/bio-alignment-validation/run/out/work_ie; rm -rf $W; mkdir -p $W; cd $W
printf 'chr22\t0\t40001\tGENE1\t0\t+\t0\t40001\t0\t1\t40001,\t0,\n' > genes.bed
infer_experiment.py -r genes.bed -i $PD/human/test.rna.paired_end.sorted.bam 2>&1 | grep -v '^$' | head -8
echo "rc=${PIPESTATUS[0]}"
cd ..; rm -rf $W
