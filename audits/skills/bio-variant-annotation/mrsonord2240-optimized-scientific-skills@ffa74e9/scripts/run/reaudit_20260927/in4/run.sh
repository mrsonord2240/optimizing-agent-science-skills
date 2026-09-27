#!/bin/bash
# Re-audit 2026-09-27 -- Input 4 (Edge): usage-guide.md "Rare Variant Analysis" recipe.
# Regression of the prior audit's Input 3: does INFO/gnomAD_FAF:=INFO/fafmax_faf95_max
# (new tag) correctly distinguish "rare/absent in gnomAD" from a cohort's own INFO/AF,
# and does the SKILL.md-consistent form avoid clobbering the cohort AF (the P1 fix from
# the 2026-09-15 backlog pass)?
set -uo pipefail
DATA=/mnt/openscience/audits/bio-variant-annotation/data
cd /mnt/openscience/audits/bio-variant-annotation/run/reaudit_20260927/in4

bgzip -c "$DATA/gnomad_syn.vcf" > gnomad_syn.vcf.gz; bcftools index -f gnomad_syn.vcf.gz
bgzip -c "$DATA/callerA.vcf" > in.vcf.gz; bcftools index -f in.vcf.gz
bcftools norm -f "$DATA/ref.fa" -m-any in.vcf.gz 2>/dev/null | bcftools +fill-tags -Oz -o cohort.vcf.gz -- -t AF
bcftools index -f cohort.vcf.gz

echo "== cohort's own INFO/AF before any gnomAD annotation =="
bcftools query -f '%POS %REF>%ALT cohortAF=%INFO/AF\n' cohort.vcf.gz

echo "== usage-guide.md recipe as currently written: gnomAD_FAF new tag, keep FAF<1% or absent =="
bcftools annotate -a gnomad_syn.vcf.gz -c INFO/gnomAD_FAF:=INFO/fafmax_faf95_max cohort.vcf.gz -Oz -o with_gnomad.vcf.gz
echo "exit=$?"
bcftools index -f with_gnomad.vcf.gz
bcftools query -f '%POS %REF>%ALT cohortAF=%INFO/AF gnomAD_FAF=%INFO/gnomAD_FAF\n' with_gnomad.vcf.gz

echo "== filter: keep FAF<0.01 or absent, THEN csq (usage-guide.md's literal -p a form) =="
bcftools filter -i 'INFO/gnomAD_FAF<0.01 || INFO/gnomAD_FAF="."' with_gnomad.vcf.gz -Ou | \
  bcftools csq -p a -f "$DATA/ref.fa" -g "$DATA/genes.gff3" -Oz -o rare_consequences.vcf.gz 2>csq.log
echo "pipe exit=${PIPESTATUS[*]}"
bcftools index -f rare_consequences.vcf.gz
echo "kept records:"
bcftools query -f '%POS %REF>%ALT cohortAF=%INFO/AF gnomAD_FAF=%INFO/gnomAD_FAF\n' rare_consequences.vcf.gz

echo "== regression check: does the cohort AF survive unclobbered (P1 fix from 2026-09-15)? =="
bcftools query -f '%POS cohortAF=%INFO/AF\n' rare_consequences.vcf.gz | grep -c 'cohortAF=0.5' || true

echo "== negative control: the OLD dangerous form (-c INFO/AF, clobbers cohort AF) for contrast, not used by usage-guide.md anymore =="
bcftools annotate -a gnomad_syn.vcf.gz -c INFO/AF cohort.vcf.gz -Oz -o old_form.vcf.gz 2>/dev/null
bcftools query -f '%POS cohortAF_after_old_form=%INFO/AF\n' old_form.vcf.gz
