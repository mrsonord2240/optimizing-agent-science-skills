#!/usr/bin/env bash
set -euo pipefail

export PATH=/home/sci/micromamba/envs/bio/bin:$PATH
PY=/home/sci/micromamba/envs/as-mmsplice/bin/python
RUN=/mnt/f/OpenScience/audits/bio-vcf-basics/runs/finalpass_20260924
DATA=/mnt/f/OpenScience/audits/bio-vcf-basics/data
SRC=/mnt/f/OpenScience/worktrees/bio-vcf-basics-finalpass/variant-calling/vcf-basics
cd "$RUN"

bcftools --version | head -1
$PY -c 'import cyvcf2; print(cyvcf2.__version__)'

echo '== archived input 1 =='
bgzip -c "$DATA/callerA.vcf" > callerA.vcf.gz
bcftools index -f -t callerA.vcf.gz
bcftools query -l callerA.vcf.gz
bcftools query -H -f '%CHROM\t%POS\t%REF\t%ALT\t%QUAL[\t%GT\t%GQ\t%AD]\n' callerA.vcf.gz | head -2
bcftools view -v snps -H callerA.vcf.gz | wc -l
bcftools view -v indels -H callerA.vcf.gz | wc -l
bcftools view -H callerA.vcf.gz | wc -l
$PY "$SRC/examples/view_vcf.py" callerA.vcf.gz 2 | head -5

echo '== archived input 2 =='
$PY /mnt/f/OpenScience/audits/bio-vcf-basics/runs/in2/ab.py

echo '== archived input 3 =='
$PY /mnt/f/OpenScience/audits/bio-vcf-basics/runs/in3/miss.py

echo '== archived input 4 =='
bcftools query -f '%CHROM\t%POS\t%INFO/END\t%REF\t%ALT\t%QUAL[\t%GT\t%DP\t%GQ]\n' "$DATA/sample.g.vcf"
bcftools view -H -i 'N_ALT>1' "$DATA/sample.g.vcf" | wc -l

echo '== archived input 5 =='
LOCAL=$(mktemp -d /tmp/bio-vcf-basics-finalpass.XXXXXX)
cp "$DATA/cohort.vcf" "$LOCAL/cohort.vcf"
cd "$LOCAL"
bcftools view -Ob -o cohort.bcf cohort.vcf
bcftools index cohort.bcf
bgzip -c cohort.vcf > cohort.vcf.gz
bcftools index -t cohort.vcf.gz
bcftools view -H cohort.bcf chr2:1-3000 | wc -l
gzip -c cohort.vcf > plain_gzip.vcf.gz
set +e
bcftools index -f plain_gzip.vcf.gz 2>&1 | tail -2
set -e
$PY /mnt/f/OpenScience/audits/bio-vcf-basics/runs/in5/write_q30.py

echo '== fresh inputs =='
cd "$RUN"
$PY "$RUN/fresh_cases.py" "$SRC/examples/view_vcf.py"
