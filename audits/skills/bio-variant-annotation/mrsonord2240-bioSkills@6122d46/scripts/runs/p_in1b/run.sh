#!/bin/bash
# Second-method check (WSL bcftools 1.21) of the post-fix SKILL.md 3-line csq/annotate block: annotate -a on an unindexed target.
set -uo pipefail
export PATH=/tmp/vaca/env/bin:$PATH
bcftools --version | head -1
D=../../data
for db in dbsnp_syn gnomad_syn; do bgzip -c $D/$db.vcf > $db.vcf.gz; bcftools index -f $db.vcf.gz; done
bgzip -c $D/callerA.vcf > in.vcf.gz; bcftools index -f in.vcf.gz
bcftools norm -f $D/ref.fa -m-any in.vcf.gz -Oz -o norm.vcf.gz 2>/dev/null; bcftools index -f norm.vcf.gz
# SKILL.md block verbatim (file names substituted)
bcftools csq -p a -f $D/ref.fa -g $D/genes.gff3 norm.vcf.gz -Oz -o csq.vcf.gz 2>/dev/null; echo "csq exit=$?"
bcftools annotate -a dbsnp_syn.vcf.gz -c ID norm.vcf.gz -Oz -o rsid.vcf.gz; echo "rsid exit=$?"
bcftools annotate -a gnomad_syn.vcf.gz -c INFO/gnomAD_FAF:=INFO/fafmax_faf95_max rsid.vcf.gz -Oz -o af.vcf.gz; echo "gnomAD exit=$?"
ls af.vcf.gz 2>&1
echo "-- with bcftools index rsid.vcf.gz first --"
bcftools index -f rsid.vcf.gz
bcftools annotate -a gnomad_syn.vcf.gz -c INFO/gnomAD_FAF:=INFO/fafmax_faf95_max rsid.vcf.gz -Oz -o af.vcf.gz; echo "gnomAD exit=$?"
bcftools query -f '%POS:%INFO/gnomAD_FAF ' af.vcf.gz; echo
