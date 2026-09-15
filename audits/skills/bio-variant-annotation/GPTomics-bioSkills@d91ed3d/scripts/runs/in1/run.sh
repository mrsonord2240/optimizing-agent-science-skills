#!/bin/bash
# Input 1 (canonical): normalize -> rsID -> gnomAD grpmax FAF -> ClinVar (+review status) -> bcftools csq -> triage table.
set -uo pipefail
DATA=../../data
for db in dbsnp_syn gnomad_syn clinvar_syn; do bgzip -c $DATA/$db.vcf > $db.vcf.gz; bcftools index -f $db.vcf.gz; done
bgzip -c $DATA/callerA.vcf > in.vcf.gz; bcftools index -f in.vcf.gz
# SKILL.md: normalize before annotation (-m-any -f)
bcftools norm -f $DATA/ref.fa -m-any in.vcf.gz -Oz -o norm.vcf.gz 2>norm.log; bcftools index -f norm.vcf.gz; cat norm.log
# SKILL.md bcftools annotate (one source per step; indexed intermediates)
bcftools annotate -a dbsnp_syn.vcf.gz -c ID norm.vcf.gz -Oz -o a1.vcf.gz && bcftools index -f a1.vcf.gz
bcftools annotate -a gnomad_syn.vcf.gz -c INFO/AF_grpmax,INFO/fafmax_faf95_max,INFO/grpmax a1.vcf.gz -Oz -o a2.vcf.gz && bcftools index -f a2.vcf.gz
bcftools annotate -a clinvar_syn.vcf.gz -c INFO/CLNSIG,INFO/CLNREVSTAT a2.vcf.gz -Oz -o a3.vcf.gz && bcftools index -f a3.vcf.gz
echo "== csq exactly as SKILL.md writes it =="
bcftools csq -f $DATA/ref.fa -g $DATA/genes.gff3 a3.vcf.gz -Oz -o csq.vcf.gz 2>&1 | tail -2; echo "exit=${PIPESTATUS[0]}"
echo "== csq with -p a (unphased hets treated as one haplotype) =="
bcftools csq -p a -f $DATA/ref.fa -g $DATA/genes.gff3 a3.vcf.gz -Oz -o csq.vcf.gz 2>/dev/null; bcftools index -f csq.vcf.gz
bcftools query -f '%CHROM:%POS\t%REF>%ALT\t%ID\t%INFO/BCSQ\t%INFO/fafmax_faf95_max\t%INFO/CLNSIG\t%INFO/CLNREVSTAT\n' csq.vcf.gz
echo "== triage: coding HIGH/MODERATE-like consequences =="
bcftools view -i 'INFO/BCSQ~"stop_gained" || INFO/BCSQ~"frameshift" || INFO/BCSQ~"missense" || INFO/BCSQ~"splice"' csq.vcf.gz | bcftools query -f '%POS\t%INFO/BCSQ\n' | cut -d'|' -f1,2,6
echo "== shipped examples/annotate_vcf.sh as written =="
cp /f/OpenScience/external/GPTomics__bioSkills/variant-calling/variant-annotation/examples/annotate_vcf.sh ./annotate_vcf.upstream_copy.sh
bash annotate_vcf.upstream_copy.sh norm.vcf.gz dbsnp_syn.vcf.gz ex_out.vcf.gz; echo "exit=$?"
GNOMAD_VCF=gnomad_syn.vcf.gz bash annotate_vcf.upstream_copy.sh norm.vcf.gz dbsnp_syn.vcf.gz ex_out2.vcf.gz; echo "exit(gnomAD branch)=$?"
