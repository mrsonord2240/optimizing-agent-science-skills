#!/usr/bin/env bash
# Exact-commit final-pass audit for bio-variant-normalization.
# Run from WSL. Outputs are written only below this run directory.
set -euo pipefail

ROOT=/mnt/f/OpenScience
SRC="$ROOT/worktrees/bio-variant-normalization-finalpass-20260924/variant-calling/variant-normalization"
DATA="$ROOT/audits/bio-variant-normalization/data"
OUT="$ROOT/audits/bio-variant-normalization/runs/finalpass_20260924/work"
mkdir -p "$OUT"
cd "$OUT"

bcftools --version | head -1
test -f "$SRC/SKILL.md"
test -f "$SRC/usage-guide.md"
grep -Fq 'bcftools norm -m- in.vcf.gz | bcftools norm --atomize | bcftools norm -f ref.fa' "$SRC/SKILL.md"
grep -Fq 'skips unphased hets, so it must not be used to create separate haplotypes' "$SRC/SKILL.md"
grep -Fq 'mismatch: confirm the exact reference build' "$SRC/usage-guide.md"
echo 'SOURCE-CHECK PASS: primary route, phase semantics, and guide preflight present'

for name in callerA callerB; do
  bgzip -c "$DATA/$name.vcf" > "$name.vcf.gz"
  bcftools index -f "$name.vcf.gz"
done

# Archived input 1: caller comparison, REF mismatch detection, no atomization-star artifact,
# and idempotence on the no-mismatch caller.
bcftools norm -f "$DATA/ref.fa" -c w callerB.vcf.gz -Ou 2>&1 >/dev/null | \
  grep -Eq 'REF_MISMATCH|does not match'
bcftools norm -m- callerA.vcf.gz | bcftools norm --atomize | \
  bcftools norm -f "$DATA/ref.fa" -Oz -o callerA.norm.vcf.gz
bcftools norm -m- callerB.vcf.gz | bcftools norm --atomize | \
  bcftools norm -f "$DATA/ref.fa" -c x -Oz -o callerB.norm.vcf.gz
bcftools view -H -i 'ALT="*"' callerA.norm.vcf.gz | (! read)
bcftools view -H -i 'ALT="*"' callerB.norm.vcf.gz | (! read)
bcftools norm -m- callerA.norm.vcf.gz | bcftools norm --atomize | \
  bcftools norm -f "$DATA/ref.fa" -Ov | grep -v '^#' | cut -f1-5 > renorm.tsv
bcftools view -H callerA.norm.vcf.gz | cut -f1-5 > norm.tsv
diff -u norm.tsv renorm.tsv
echo 'ARCHIVED-1 PASS: mismatch surfaced; zero ALT=*; normalized output idempotent'

# Archived input 2: a right-shifted homopolymer deletion reaches the canonical ClinVar key.
bcftools norm -m- callerB.vcf.gz | bcftools norm --atomize | \
  bcftools norm -f "$DATA/ref.fa" -c x -Ou | \
  bcftools query -f '%POS %REF>%ALT\n' | grep -Fx '500 GA>G'
echo 'ARCHIVED-2 PASS: chr1:506 AA>A normalizes to 500 GA>G'

# Archived input 3: declared per-ALT data splits, whereas Number=. is intentionally retained.
bcftools norm -m-any "$DATA/edge_multiallelic_fixedhdr.vcf" -Ov > split-any.vcf
bcftools norm -m-both "$DATA/edge_multiallelic_fixedhdr.vcf" -Ov > split-both.vcf
diff -u <(grep -v '^##' split-any.vcf) <(grep -v '^##' split-both.vcf)
grep -Eq 'XAF=0\.1' split-any.vcf
grep -Eq 'XAF=0\.2' split-any.vcf
echo 'ARCHIVED-3 PASS: -m-both equals -m-any while splitting; declared ALT fields subset'

# Archived logical input 4: standardizing atomized and unatomized representations removes
# MNP representation discordance. vt is not installed in this final-pass host, so the
# archived vt output is reproduced by the documented bcftools atomization equivalent.
bcftools norm -f "$DATA/ref.fa" -c x callerB.vcf.gz -Ou | \
  bcftools norm -m- | bcftools norm --atomize | \
  bcftools norm -f "$DATA/ref.fa" -Oz -o atomized.vcf.gz
bcftools norm -f "$DATA/ref.fa" -c x callerB.vcf.gz -Ou | \
  bcftools norm -m- | bcftools norm -f "$DATA/ref.fa" -Oz -o unatomized.vcf.gz
bcftools norm -m- unatomized.vcf.gz | bcftools norm --atomize | \
  bcftools norm -f "$DATA/ref.fa" -Oz -o unatomized.standard.vcf.gz
bcftools index -f atomized.vcf.gz
bcftools index -f unatomized.standard.vcf.gz
bcftools isec -n=2 -w1 atomized.vcf.gz unatomized.standard.vcf.gz -Ov | grep -v '^#' > shared.tsv
test "$(wc -l < shared.tsv)" -eq "$(bcftools view -H atomized.vcf.gz | wc -l)"
echo 'ARCHIVED-4 PASS: atomized and re-standardized cohorts have identical site sets (vt unavailable)'

# Archived input 5: the documented csq phase modes match installed help and behavior.
bgzip -c "$DATA/genes.gff3" > genes.gff3.gz
bcftools csq -p a -f "$DATA/ref.fa" -g genes.gff3.gz unatomized.vcf.gz -Ov > csq-a.vcf
bcftools csq -p s -f "$DATA/ref.fa" -g genes.gff3.gz unatomized.vcf.gz -Ov > csq-s.vcf
grep -Eq 'BCSQ=.*11L>11F' csq-a.vcf
awk -F '\t' '$2 == 1041 { if ($8 ~ /BCSQ=/) exit 1 }' csq-s.vcf
echo 'ARCHIVED-5 PASS: -p a annotates the unphased MNP; -p s omits that merged consequence (while isolated-site output remains version-sensitive)'

# Fresh input A: a mixed SNP/indel record confirms splitting and joining semantics.
cat > fresh-mixed.vcf <<'VCF'
##fileformat=VCFv4.2
##contig=<ID=chr1,length=20>
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	S
chr1	5	.	A	C,AT,G	.	PASS	.	GT	1/2
VCF
bcftools norm -m-any fresh-mixed.vcf -Ov > fresh-any.vcf
bcftools norm -m-both fresh-mixed.vcf -Ov > fresh-both.vcf
diff -u <(grep -v '^##' fresh-any.vcf) <(grep -v '^##' fresh-both.vcf)
bcftools norm -m+both fresh-any.vcf -Ov > fresh-joined.vcf
test "$(grep -vc '^#' fresh-joined.vcf)" -eq 2
echo 'FRESH-A PASS: split forms agree; -m+both keeps SNP and indel records separate'

# Fresh input B: the usage-guide preflight returns an actionable mismatch before a pipeline
# can create and index a broken destination. The same grep used in the guide detects it.
if bcftools norm -f "$DATA/ref.fa" -c w callerB.vcf.gz -Ou 2>&1 >/dev/null | \
     grep -q 'REF_MISMATCH\|does not match'; then
  echo 'FRESH-B PASS: guide preflight detects REF mismatch before output creation'
else
  echo 'Guide preflight did not detect the known mismatch' >&2
  exit 1
fi

echo 'ALL ASSERTIONS PASS: archived=5 fresh=2'
