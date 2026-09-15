#!/bin/bash
# Input 2 (Variant A): "Before association testing, screen the 8-sample cohort for sample swaps / duplicates /
# unexpected relatedness." SYNTHETIC: SYN_S8 is a re-sequenced duplicate of SYN_S3 (truth).
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -t -f cohort.vcf.gz
echo "== Version note check: does gtcheck still accept -G? =="
bcftools gtcheck -G 1 cohort.vcf.gz > /dev/null 2> G.err; echo "gtcheck -G 1 exit=$?"; head -2 G.err
bcftools gtcheck 2>&1 | grep -E "^\s+-(E|e|g|u|G)[ ,]" | head -8
echo "== SKILL.md: bcftools gtcheck input.vcf.gz (all-pairs, no -g) =="
bcftools gtcheck cohort.vcf.gz > gtcheck.txt 2> gtcheck.err; echo "exit=$?"
grep -m1 "^# DC" gtcheck.txt
grep "^DC" gtcheck.txt | sort -t$'\t' -k4,4g | head -6
echo "(lowest discordance pairs above; SKILL says smaller = more similar)"
echo "== vcftools --relatedness2 and somalier: WSL, see out_wsl.txt =="
