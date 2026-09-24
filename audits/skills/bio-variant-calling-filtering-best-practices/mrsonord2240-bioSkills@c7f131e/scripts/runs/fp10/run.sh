#!/bin/bash
# Fresh final-pass input 10: exact-current somatic missing-header guard.
set -u
source ../env.sh
SKILL=/f/OpenScience/worktrees/bio-variant-calling-filtering-best-practices-finalpass/variant-calling/filtering-best-practices/SKILL.md
grep -Fq "tumor sample not found; pass it explicitly" "$SKILL"
cat > no_tumor_header.vcf <<'EOF'
##fileformat=VCFv4.2
##contig=<ID=chr1,length=1000>
##INFO=<ID=TLOD,Number=A,Type=Float,Description="TLOD">
##FORMAT=<ID=AF,Number=A,Type=Float,Description="AF">
##FORMAT=<ID=DP,Number=1,Type=Integer,Description="DP">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	NORMAL	TUMOR
chr1	10	.	A	C	.	PASS	TLOD=20	AF:DP	0.01:30	0.30:30
EOF
set +e
(
  TUMOR=$(bcftools view -h no_tumor_header.vcf | grep '^##tumor_sample=' | cut -d= -f2)
  T=$(( $(bcftools query -l no_tumor_header.vcf | grep -nxF "$TUMOR" | cut -d: -f1) - 1 ))
  [ -n "$TUMOR" ] && [ "$T" -ge 0 ] || { echo 'tumor sample not found; pass it explicitly'; exit 1; }
  bcftools filter -i "INFO/TLOD>6.3 && FMT/AF[$T:0]>0.05 && FMT/DP[$T]>20" no_tumor_header.vcf -o impossible.vcf
)
rc=$?
set -e
test "$rc" -eq 1
test ! -e impossible.vcf
echo "PASS: exact-current guard rejected stripped tumor header before bcftools filtering (exit=$rc)."
