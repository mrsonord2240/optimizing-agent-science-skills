#!/bin/bash
# Re-audit 2026-09-27 -- Input 2 (Variant A): the shipped examples/annotate_vcf.sh helper.
# Regression of the 2026-09-24 final-pass fresh cases (valid, unindexed, bad GNOMAD_VCF,
# contig mismatch); re-executed fresh via WSL bcftools 1.24 against the CURRENT script
# (unchanged since the final pass -- verified by git diff against the shelf repo).
set -uo pipefail
DATA=/mnt/openscience/audits/bio-variant-annotation/data
BASE=/mnt/openscience/audits/bio-variant-annotation/run/reaudit_20260927
cd "$BASE/in2"

bgzip -c "$DATA/dbsnp_syn.vcf" > dbsnp_syn.vcf.gz; bcftools index -f dbsnp_syn.vcf.gz
bgzip -c "$DATA/gnomad_syn.vcf" > gnomad_syn.vcf.gz; bcftools index -f gnomad_syn.vcf.gz
bgzip -c "$DATA/callerA.vcf" > in.vcf.gz; bcftools index -f in.vcf.gz
bcftools norm -f "$DATA/ref.fa" -m-any in.vcf.gz -Oz -o norm.vcf.gz 2>/dev/null
bcftools index -f norm.vcf.gz

echo "== Case A: valid run, no GNOMAD_VCF =="
bash "$BASE/annotate_vcf.sh" norm.vcf.gz dbsnp_syn.vcf.gz out_a.vcf.gz
echo "exit=$?"

echo "== Case B: valid run WITH GNOMAD_VCF =="
GNOMAD_VCF=gnomad_syn.vcf.gz bash "$BASE/annotate_vcf.sh" norm.vcf.gz dbsnp_syn.vcf.gz out_b.vcf.gz
echo "exit=$?"

echo "== Case C: unindexed target VCF (copy without .csi) =="
cp norm.vcf.gz norm_noidx.vcf.gz
bash "$BASE/annotate_vcf.sh" norm_noidx.vcf.gz dbsnp_syn.vcf.gz out_c.vcf.gz
echo "exit=$?"

echo "== Case D: GNOMAD_VCF set but path does not exist =="
GNOMAD_VCF=/mnt/openscience/does_not_exist.vcf.gz bash "$BASE/annotate_vcf.sh" norm.vcf.gz dbsnp_syn.vcf.gz out_d.vcf.gz
echo "exit=$?"

echo "== Case E: chr1 vs 1 contig-name mismatch between input and gnomAD source =="
sed -e 's/^chr//' -e 's/##contig=<ID=chr/##contig=<ID=/' "$DATA/callerA.vcf" | bgzip -c > nochr.vcf.gz
bcftools index -f nochr.vcf.gz
GNOMAD_VCF=gnomad_syn.vcf.gz bash "$BASE/annotate_vcf.sh" nochr.vcf.gz dbsnp_syn.vcf.gz out_e.vcf.gz
echo "exit=$?"

echo "== Case F: missing bcftools on PATH (simulate) =="
PATH=/usr/bin:/bin bash "$BASE/annotate_vcf.sh" norm.vcf.gz dbsnp_syn.vcf.gz out_f.vcf.gz
echo "exit=$?"
