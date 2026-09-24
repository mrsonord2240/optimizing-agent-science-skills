#!/bin/bash
# Input 8 (NEW, re-audit 2026-09-15, Edge): "Our somatic VCFs come from three pipelines: Mutect2 with the tumor
# listed first, a Mutect2 run where the ##tumor_sample header was stripped by a merge step, and one where the tumor
# is named TUMOR_1 next to a sample TUMOR_10. Use your tumor-column post-filter on all three."
# Tests the fixed SKILL.md tumor-index block on layouts the fixer did not test. SYNTHETIC VCFs.
set -uo pipefail
source ../env.sh
mk() { # $1 name, $2 header lines, $3 sample header, $4 body
  printf '##fileformat=VCFv4.2\n##source=SYNTHETIC_Mutect2_shaped\n##contig=<ID=chr1,length=20000>\n##INFO=<ID=TLOD,Number=A,Type=Float,Description="TLOD">\n##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n##FORMAT=<ID=AF,Number=A,Type=Float,Description="AF">\n##FORMAT=<ID=DP,Number=1,Type=Integer,Description="DP">\n%b#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t%b\n%b' "$2" "$3" "$4" > $1.vcf
}
# A: tumor first. Somatic 5100 (tumor AF .29), 5300 (tumor AF .07); 5400 low tumor AF; normal-only noise at 5600
mk tumor_first '##normal_sample=SYN_N\n##tumor_sample=SYN_T\n' "SYN_T\tSYN_N" \
'chr1\t5100\t.\tC\tT\t.\tPASS\tTLOD=25.3\tGT:AF:DP\t0/1:0.29:42\t0/0:0.01:40\nchr1\t5300\t.\tA\tG\t.\tPASS\tTLOD=7.9\tGT:AF:DP\t0/1:0.07:54\t0/0:0.03:39\nchr1\t5400\t.\tT\tC\t.\tPASS\tTLOD=4.1\tGT:AF:DP\t0/1:0.04:47\t0/0:0.01:30\nchr1\t5600\t.\tG\tA\t.\tPASS\tTLOD=7.0\tGT:AF:DP\t0/0:0.02:45\t0/1:0.30:40\n'
# B: header line stripped
mk no_header '' "SYN_N\tSYN_T" \
'chr1\t5100\t.\tC\tT\t.\tPASS\tTLOD=25.3\tGT:AF:DP\t0/0:0.01:40\t0/1:0.29:42\nchr1\t5600\t.\tG\tA\t.\tPASS\tTLOD=7.0\tGT:AF:DP\t0/1:0.30:40\t0/0:0.02:45\n'
# C: prefix-colliding names, tumor TUMOR_1 is the third column
mk prefix '##normal_sample=NORMAL\n##tumor_sample=TUMOR_1\n' "NORMAL\tTUMOR_10\tTUMOR_1" \
'chr1\t5100\t.\tC\tT\t.\tPASS\tTLOD=25.3\tGT:AF:DP\t0/0:0.01:40\t0/0:0.01:40\t0/1:0.29:42\nchr1\t5700\t.\tG\tA\t.\tPASS\tTLOD=9.0\tGT:AF:DP\t0/0:0.01:40\t0/1:0.40:50\t0/0:0.01:44\n'
for f in tumor_first no_header prefix; do
  echo "== $f: samples $(bcftools query -l $f.vcf | tr -d '\r' | tr '\n' ' ')"
  # SKILL.md block verbatim (file name substituted)
  TUMOR=$(bcftools view -h $f.vcf | grep '^##tumor_sample=' | cut -d= -f2)
  T=$(( $(bcftools query -l $f.vcf | grep -nxF "$TUMOR" | cut -d: -f1) - 1 ))
  echo "TUMOR='$(echo -n $TUMOR | tr -d '\r')' T=$T"
  bcftools filter -i "INFO/TLOD>6.3 && FMT/AF[$T:0]>0.05 && FMT/DP[$T]>20" $f.vcf -o ${f}_somatic.vcf 2> $f.err; echo "filter exit=$?"; head -2 $f.err
  bcftools query -f '%POS\t[%SAMPLE=%AF ]\n' ${f}_somatic.vcf 2>/dev/null | tr -d '\r'
done
echo "expected: tumor_first 5100,5300 ; no_header -> should stop (no tumor known) ; prefix 5100 only"
