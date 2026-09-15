#!/bin/bash
# Input 5 (Stress, post-fix regression 2026-09-15): "(a) how many callerB records need normalization? (b) a copy for database
# matching and a copy for functional annotation. (c) annotate consequences on the right copy, explain the codon at chr1:1041.
# (d) HGVS c. vs VCF POS for the CA-repeat deletion." Windows bcftools 1.24 part (the cyvcf2 part runs in WSL: run_py.sh).
set -uo pipefail
E=/f/OpenScience/audit-envs/variant-annotation-curation-analyst
export PATH=$E/msys/mingw64/bin:$PATH
D=../../data; R=$D/ref.fa
bgzip -c $D/callerB.vcf > callerB.vcf.gz; bcftools index -f callerB.vcf.gz
bgzip -c $D/genes.gff3 > genes.gff3.gz
echo "== matching copy: post-fix pipeline (split -> atomize -> left-align), REF mismatch excluded =="
bcftools norm -m- callerB.vcf.gz | bcftools norm --atomize | bcftools norm -f $R -c x -Oz -o match.vcf.gz; bcftools index -f match.vcf.gz
bcftools query -f '%POS %REF>%ALT; ' match.vcf.gz | tr -d '\r'; echo
echo "== annotation copy: split -> left-align, no atomize =="
bcftools norm -m- callerB.vcf.gz | bcftools norm -f $R -c x -Oz -o annot.vcf.gz; bcftools index -f annot.vcf.gz
bcftools query -f '%POS %REF>%ALT; ' annot.vcf.gz | tr -d '\r'; echo
echo "== SKILL.md csq line (post-fix, verbatim; file names substituted) on the annotation copy =="
bcftools csq -p a -f $R -g genes.gff3.gz annot.vcf.gz 2>csq.err | bcftools query -i 'POS>=1026 && POS<=1500' -f '%POS %REF>%ALT\t%INFO/BCSQ\n' | tr -d '\r' | cut -c1-150; echo "exit=${PIPESTATUS[0]}"; grep -i error csq.err
echo "== same on the atomized matching copy =="
bcftools csq -p a -f $R -g genes.gff3.gz match.vcf.gz 2>/dev/null | bcftools query -i 'POS>=1026 && POS<=1500' -f '%POS %REF>%ALT\t%INFO/BCSQ\n' | tr -d '\r' | cut -c1-150
echo "== -p s on the atomized copy (Skill: 'treats unphased hets as separate haplotypes') =="
bcftools csq -p s -f $R -g genes.gff3.gz match.vcf.gz 2>/dev/null | bcftools query -i 'POS>=1026 && POS<=1500' -f '%POS %REF>%ALT\t%INFO/BCSQ\n' | tr -d '\r' | cut -c1-150
