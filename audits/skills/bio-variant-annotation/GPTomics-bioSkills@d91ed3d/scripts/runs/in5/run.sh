#!/bin/bash
# Input 5 (stress): SKILL.md "Complete annotation pipeline". No VEP cache is available offline here, so the
# cache flags (--cache --offline --dir_cache --assembly) are replaced by a custom --gff/--fasta transcript source (--offline dropped: with --gff it still demands a cache dir);
# every other flag is kept as written.
set -u
export PATH=/tmp/vaca/vep/bin:/tmp/vaca/env/bin:$PATH
vep --help 2>&1 | grep -m1 "ensembl-vep"
R=../../data/ref.fa; OUT=cohortA
(grep '^#' ../../data/genes.gff3; grep -v '^#' ../../data/genes.gff3 | sort -k1,1 -k4,4n) | bgzip -c > genes.gff3.gz; tabix -f -p gff genes.gff3.gz
bgzip -c ../../data/callerA.vcf > in.vcf.gz
bcftools norm -f "$R" -m-any in.vcf.gz -Oz -o ${OUT}_norm.vcf.gz 2>/dev/null; bcftools index ${OUT}_norm.vcf.gz
echo "== 1. as written minus cache flags (keeps --everything --mane_select --pick --pick_order) =="
vep -i ${OUT}_norm.vcf.gz -o ${OUT}_vep.vcf --vcf --gff genes.gff3.gz --fasta $R \
    --everything --mane_select --pick --pick_order mane_select,canonical,biotype,rank --fork 4 --force_overwrite 2>&1 | grep -iE "error|warn|exception" | head -5; echo "exit=${PIPESTATUS[0]}"
echo "== 2. without --everything (cache-only sources) =="
vep -i ${OUT}_norm.vcf.gz -o ${OUT}_vep.vcf --vcf --gff genes.gff3.gz --fasta $R \
    --hgvs --symbol --mane_select --pick --pick_order mane_select,canonical,biotype,rank --fork 4 --force_overwrite 2>&1 | grep -iE "error|exception" | head -5; echo "exit=${PIPESTATUS[0]}"
grep -m1 '^##INFO=<ID=CSQ' ${OUT}_vep.vcf | sed 's/.*Format: //' | cut -c1-200
bcftools query -f '%POS %REF>%ALT\t%INFO/CSQ\n' ${OUT}_vep.vcf | cut -d'|' -f1-4,11-12 | head -12
echo "== 3. last two pipeline steps as written =="
bgzip -f ${OUT}_vep.vcf && bcftools index ${OUT}_vep.vcf.gz
bcftools view -i 'INFO/CSQ~"HIGH" || INFO/CSQ~"MODERATE"' ${OUT}_vep.vcf.gz -Oz -o ${OUT}_review.vcf.gz; echo "exit=$?"
bcftools view -H ${OUT}_review.vcf.gz | cut -f2,4,5
echo "== default pick_order of this VEP build =="
grep -o "pick_order[^;]*" /tmp/vaca/vep/share/ensembl-vep*/modules/Bio/EnsEMBL/VEP/Config.pm 2>/dev/null | head -2 || true
grep -rn "mane_select mane_plus_clinical canonical" /tmp/vaca/vep/share/ 2>/dev/null | head -2
