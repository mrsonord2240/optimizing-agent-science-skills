#!/bin/bash
# Re-audit 2026-09-27 -- Input 6 (Scope Boundary): "Our VCF uses Ensembl-style contig
# names (1, 2) but the gnomAD file uses chr1/chr2. Add the gnomAD grpmax FAF and tell me
# which variants are absent from gnomAD." Regression of the prior audit's Input 8: does
# SKILL.md's Common Errors row (chr-naming -> --rename-chrs) and the "absent means
# absent, not necessarily not-callable" caveat still hold?
set -uo pipefail
DATA=/mnt/openscience/audits/bio-variant-annotation/data
cd /mnt/openscience/audits/bio-variant-annotation/run/reaudit_20260927/in6

bgzip -c "$DATA/gnomad_syn.vcf" > gnomad_syn.vcf.gz; bcftools index -f gnomad_syn.vcf.gz
sed -e 's/^chr//' -e 's/##contig=<ID=chr/##contig=<ID=/' "$DATA/callerA.vcf" | bgzip -c > nochr.vcf.gz
bcftools index -f nochr.vcf.gz

echo "contigs: input=$(bcftools index -s nochr.vcf.gz | cut -f1 | tr '\n' ' ') gnomad=$(bcftools index -s gnomad_syn.vcf.gz | cut -f1 | tr '\n' ' ')"

echo "== naive annotate (contig-name mismatch): SKILL.md/usage-guide.md say this exits 0 with no matches =="
bcftools annotate -a gnomad_syn.vcf.gz -c INFO/gnomAD_FAF:=INFO/fafmax_faf95_max nochr.vcf.gz -Oz -o naive.vcf.gz 2> naive.err
echo "exit=$?"
cat naive.err
echo "records with gnomAD_FAF set: $(bcftools view -H -i 'INFO/gnomAD_FAF!="."' naive.vcf.gz 2>/dev/null | wc -l) of $(bcftools view -H nochr.vcf.gz | wc -l)"

echo "== fix per Common Errors row: bcftools annotate --rename-chrs on the source =="
bcftools index -s gnomad_syn.vcf.gz | cut -f1 | awk '{n=$1; sub(/^chr/,"",n); print $1"\t"n}' > chr_map.txt
cat chr_map.txt
bcftools annotate --rename-chrs chr_map.txt gnomad_syn.vcf.gz -Oz -o gnomad_nochr.vcf.gz
bcftools index -f gnomad_nochr.vcf.gz
bcftools annotate -a gnomad_nochr.vcf.gz -c INFO/gnomAD_FAF:=INFO/fafmax_faf95_max nochr.vcf.gz -Oz -o fixed.vcf.gz
echo "exit=$?"
echo "records with gnomAD_FAF set after fix: $(bcftools view -H -i 'INFO/gnomAD_FAF!="."' fixed.vcf.gz | wc -l)"

echo "== absent-from-gnomAD variants (per the fix) =="
bcftools query -i 'INFO/gnomAD_FAF="."' -f '%CHROM:%POS %REF>%ALT\n' fixed.vcf.gz

echo "== usage-guide.md Troubleshooting: check via bcftools index -s comparison BEFORE trusting a zero-hit result =="
diff <(bcftools index -s nochr.vcf.gz | cut -f1) <(bcftools index -s gnomad_syn.vcf.gz | cut -f1) && echo "contigs identical (unexpected)" || echo "contigs differ (correctly flags the naive run above as suspect)"
