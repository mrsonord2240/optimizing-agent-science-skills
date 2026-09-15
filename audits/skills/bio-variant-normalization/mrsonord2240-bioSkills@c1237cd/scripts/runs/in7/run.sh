#!/bin/bash
# Input 7 (NEW, re-audit 2026-09-15, Edge): "Our joint caller writes a SNP and an insertion at the same position. Should I split
# with -m-both or -m-any, and when I rejoin for delivery will -m+both put the SNP and indel back in one record? Also keep a
# trace of the original MNP when I atomize." Tests the post-fix Split Options table and --old-rec-tag. Windows bcftools 1.24.
set -uo pipefail
E=/f/OpenScience/audit-envs/variant-annotation-curation-analyst
export PATH=$E/msys/mingw64/bin:$PATH
D=../../data
printf '##fileformat=VCFv4.2\n##source=SYNTHETIC_same_position_snp_indel (audit 2026-09-15)\n##contig=<ID=chr1,length=20000>\n##INFO=<ID=AC,Number=A,Type=Integer,Description="AC">\n##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tS1\tS2\nchr1\t2000\t.\tA\tC,AT,G\t50\tPASS\tAC=1,1,1\tGT\t1/2\t0/3\nchr1\t3000\t.\tG\tT\t50\tPASS\tAC=1\tGT\t0/1\t0/0\nchr1\t3000\t.\tG\tGA\t50\tPASS\tAC=1\tGT\t0/0\t0/1\nchr1\t3000\t.\tG\tC\t50\tPASS\tAC=1\tGT\t0/0\t0/1\n' > mixed.vcf
for m in -m-any -m-both -m-snps -m-indels; do
  echo "split $m: $(bcftools norm $m mixed.vcf 2>/dev/null | bcftools query -f '%POS %REF>%ALT [%GT ]; ' | tr -d '\r')"
done
for m in -m+any -m+both -m+snps -m+indels; do
  echo "join  $m: $(bcftools norm $m mixed.vcf 2>/dev/null | bcftools query -f '%POS %REF>%ALT [%GT ]; ' | tr -d '\r')"
done
echo "== --atomize --old-rec-tag ORIGINAL on callerB's MNP =="
bgzip -c $D/callerB.vcf > B.vcf.gz; bcftools index -f B.vcf.gz
bcftools norm --atomize --old-rec-tag ORIGINAL B.vcf.gz 2>/dev/null | bcftools query -i 'INFO/ORIGINAL!="."' -f '%POS %REF>%ALT ORIGINAL=%INFO/ORIGINAL\n' | tr -d '\r'
