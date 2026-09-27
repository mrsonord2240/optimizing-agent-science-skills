#!/bin/bash
# Re-audit 2026-09-27 -- Input 1 (Canonical): SKILL.md's own annotate/csq pipeline
# norm -> rsID -> gnomAD FAF (new tag) -> ClinVar -> csq -p a -> triage.
# Regression of the 2026-09 audit's Input 1; re-executed fresh against the current
# (post usage-guide-fix) SKILL.md text via WSL bcftools 1.24.
set -uo pipefail
DATA=/mnt/openscience/audits/bio-variant-annotation/data
cd /mnt/openscience/audits/bio-variant-annotation/run/reaudit_20260927/in1

for db in dbsnp_syn gnomad_syn clinvar_syn; do
  bgzip -c "$DATA/$db.vcf" > "$db.vcf.gz"; bcftools index -f "$db.vcf.gz"
done
bgzip -c "$DATA/callerA.vcf" > in.vcf.gz; bcftools index -f in.vcf.gz

echo "== SKILL.md: bcftools norm -f reference.fa -m-any input.vcf.gz =="
bcftools norm -f "$DATA/ref.fa" -m-any in.vcf.gz -Oz -o norm.vcf.gz 2>norm.log
echo "exit=$?"; cat norm.log
bcftools index -f norm.vcf.gz

echo "== SKILL.md: bcftools annotate -a dbsnp.vcf.gz -c ID =="
bcftools annotate -a dbsnp_syn.vcf.gz -c ID norm.vcf.gz -Oz -o a1.vcf.gz; echo "exit=$?"
bcftools index -f a1.vcf.gz

echo "== SKILL.md: bcftools annotate -a gnomad.vcf.gz -c INFO/gnomAD_FAF:=INFO/fafmax_faf95_max (new tag) =="
bcftools annotate -a gnomad_syn.vcf.gz -c INFO/gnomAD_FAF:=INFO/fafmax_faf95_max,INFO/AF_grpmax a1.vcf.gz -Oz -o a2.vcf.gz; echo "exit=$?"
bcftools index -f a2.vcf.gz

echo "== SKILL.md: bcftools annotate -a clinvar.vcf.gz -c INFO/CLNSIG,INFO/CLNDN =="
bcftools annotate -a clinvar_syn.vcf.gz -c INFO/CLNSIG,INFO/CLNREVSTAT a2.vcf.gz -Oz -o a3.vcf.gz; echo "exit=$?"
bcftools index -f a3.vcf.gz

echo "== SKILL.md: bcftools csq -p a -f reference.fa -g genes.gff3 (unphased short-read default) =="
bcftools csq -p a -f "$DATA/ref.fa" -g "$DATA/genes.gff3" a3.vcf.gz -Oz -o csq.vcf.gz 2>csq.log; echo "exit=$?"
cat csq.log
bcftools index -f csq.vcf.gz

echo "== record count and rsID/FAF/CLNSIG hit rates =="
TOTAL=$(bcftools view -H csq.vcf.gz | wc -l)
WITH_ID=$(bcftools view -H csq.vcf.gz | awk -F'\t' '$3!="."' | wc -l)
WITH_FAF=$(bcftools view -H -i 'INFO/gnomAD_FAF!="."' csq.vcf.gz | wc -l)
WITH_CLN=$(bcftools view -H -i 'INFO/CLNSIG!="."' csq.vcf.gz | wc -l)
echo "total=$TOTAL with_rsid=$WITH_ID with_gnomAD_FAF=$WITH_FAF with_ClinVar=$WITH_CLN"

echo "== triage table (BCSQ contains stop_gained/frameshift/missense/splice) =="
bcftools query -f '%CHROM:%POS\t%REF>%ALT\t%ID\t%INFO/BCSQ\t%INFO/gnomAD_FAF\t%INFO/CLNSIG\n' \
  -i 'INFO/BCSQ~"stop_gained" || INFO/BCSQ~"frameshift" || INFO/BCSQ~"missense" || INFO/BCSQ~"splice"' csq.vcf.gz

echo "== does INFO/gnomAD_FAF preserve '.' for gnomAD-absent variants (no cohort-AF leakage)? =="
bcftools query -i 'INFO/gnomAD_FAF="."' -f '%POS %REF>%ALT gnomAD_FAF=%INFO/gnomAD_FAF\n' csq.vcf.gz
