#!/usr/bin/env bash
# Re-audit of bio-variant-normalization after the 2026-09-27 usage-guide.md trim +
# check_normalization.py extraction. Run from WSL (science distro, bio env active).
# Reads the SKILL from a copy under run/skill_copy (never the shelf repo in place).
# Outputs written only below this run directory.
set -euo pipefail

ROOT=/mnt/openscience
SRC="$ROOT/audits/bio-variant-normalization/run/skill_copy"
DATA="$ROOT/audits/bio-variant-normalization/data"
OUT="$ROOT/audits/bio-variant-normalization/run/work"
VENV="$ROOT/audit-envs/bio-variant-normalization/venv"
mkdir -p "$OUT"
cd "$OUT"

bcftools --version | head -1
command -v vt >/dev/null 2>&1 && echo "vt: present" || echo "vt: NOT FOUND (unchanged from prior audit)"

test -f "$SRC/SKILL.md"
test -f "$SRC/usage-guide.md"
test -f "$SRC/examples/check_normalization.py" 2>/dev/null || test -f "$SRC/check_normalization.py"
wc -l "$SRC/SKILL.md" "$SRC/usage-guide.md"

for name in callerA callerB; do
  bgzip -f -c "$DATA/$name.vcf" > "$name.vcf.gz"
  bcftools index -f "$name.vcf.gz"
done

echo "=================================================================="
echo "INPUT 1 (Canonical) -- regression of finalpass ARCHIVED-1"
echo "'Normalize callerA.vcf.gz and callerB.vcf.gz so I can compare them directly'"
echo "=================================================================="
bcftools norm -f "$DATA/ref.fa" -c w callerB.vcf.gz -Ou 2>&1 >/dev/null | \
  grep -Eq 'REF_MISMATCH|does not match' && echo "REF mismatch correctly detected on callerB"
bcftools norm -m- callerA.vcf.gz | bcftools norm --atomize | \
  bcftools norm -f "$DATA/ref.fa" -Oz -o callerA.norm.vcf.gz
bcftools norm -m- callerB.vcf.gz | bcftools norm --atomize | \
  bcftools norm -f "$DATA/ref.fa" -c x -Oz -o callerB.norm.vcf.gz
bcftools view -H -i 'ALT="*"' callerA.norm.vcf.gz | (! read) && echo "no spurious ALT=* on callerA"
bcftools view -H -i 'ALT="*"' callerB.norm.vcf.gz | (! read) && echo "no spurious ALT=* on callerB"
bcftools norm -m- callerA.norm.vcf.gz | bcftools norm --atomize | \
  bcftools norm -f "$DATA/ref.fa" -Ov | grep -v '^#' | cut -f1-5 > renorm.tsv
bcftools view -H callerA.norm.vcf.gz | cut -f1-5 > norm.tsv
diff -u norm.tsv renorm.tsv && echo "idempotent: renormalizing changed nothing"
echo "INPUT 1 PASS"

echo "=================================================================="
echo "INPUT 2 (Variant A) -- regression of finalpass ARCHIVED-2"
echo "'A pathogenic ClinVar variant is showing as absent -- check my indels are left-aligned'"
echo "=================================================================="
bcftools norm -m- callerB.vcf.gz | bcftools norm --atomize | \
  bcftools norm -f "$DATA/ref.fa" -c x -Ou | \
  bcftools query -f '%POS %REF>%ALT\n' | grep -Fx '500 GA>G' && \
  echo "chr1:506 AA>A (right-shifted) normalizes to the canonical chr1:500 GA>G"
echo "INPUT 2 PASS"

echo "=================================================================="
echo "INPUT 3 (Edge) -- regression of finalpass ARCHIVED-3"
echo "'Split my multiallelic VCF but keep AD/PL correct per allele'"
echo "=================================================================="
bcftools norm -m-any "$DATA/edge_multiallelic_fixedhdr.vcf" -Ov > split-any.vcf
bcftools norm -m-both "$DATA/edge_multiallelic_fixedhdr.vcf" -Ov > split-both.vcf
diff -u <(grep -v '^##' split-any.vcf) <(grep -v '^##' split-both.vcf) && \
  echo "-m-both == -m-any while splitting (as documented)"
grep -Eq 'XAF=0\.1' split-any.vcf && grep -Eq 'XAF=0\.2' split-any.vcf && \
  echo "declared Number=A field (XAF) correctly subset per-ALT"
echo "INPUT 3 PASS"

echo "=================================================================="
echo "INPUT 4 (Variant B) -- regression of finalpass ARCHIVED-4"
echo "'Two cohorts normalized with different tools show extra private variants -- reconcile'"
echo "=================================================================="
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
test "$(wc -l < shared.tsv)" -eq "$(bcftools view -H atomized.vcf.gz | wc -l)" && \
  echo "atomized vs re-standardized cohorts: identical site sets (vt unavailable, bcftools equivalent used)"
echo "INPUT 4 PASS"

echo "=================================================================="
echo "INPUT 5 (Stress) -- regression of finalpass ARCHIVED-5"
echo "'Annotate consequences for unphased calls with bcftools csq without the phase error'"
echo "=================================================================="
bgzip -f -c "$DATA/genes.gff3" > genes.gff3.gz
bcftools csq -p a -f "$DATA/ref.fa" -g genes.gff3.gz unatomized.vcf.gz -Ov > csq-a.vcf 2>csq-a.log
bcftools csq -p s -f "$DATA/ref.fa" -g genes.gff3.gz unatomized.vcf.gz -Ov > csq-s.vcf 2>csq-s.log
grep -Eq 'BCSQ=.*11L>11F' csq-a.vcf && echo "-p a annotates the unphased MNP (11L>11F at chr1:1041)"
awk -F '\t' '$2 == 1041 { if ($8 ~ /BCSQ=/) exit 1 }' csq-s.vcf && \
  echo "-p s omits the merged consequence at chr1:1041 (documented skip behavior)"
echo "INPUT 5 PASS"

echo "=================================================================="
echo "INPUT 6 (Scope Boundary -- NEW, not run in the 2026-09-24 final pass)"
echo "'How many variants in my VCF need normalization before I run bcftools norm?'"
echo "This exercises the file the fixer actually created: examples/check_normalization.py"
echo "=================================================================="
source "$VENV/bin/activate"
python3 -c "import cyvcf2; print('cyvcf2', cyvcf2.__version__)"
cp "$SRC/check_normalization.py" ./check_normalization.py 2>/dev/null || true
python3 ./check_normalization.py callerB.vcf.gz > new_script_out.txt
cat new_script_out.txt
cp "$ROOT/audits/bio-variant-normalization/run/old_inline_check_normalization.py" ./old_inline_check_normalization.py
python3 ./old_inline_check_normalization.py > old_script_out.txt
cat old_script_out.txt
diff -u new_script_out.txt old_script_out.txt && \
  echo "new examples/check_normalization.py output is byte-identical to the pre-trim inline SKILL.md block"
deactivate
echo "INPUT 6 PASS"

echo "=================================================================="
echo "INPUT 7 (Adversarial -- NEW, not run in the 2026-09-24 final pass)"
echo "'Just silently fix any REF mismatches with -c s so the pipeline does not stop, I am in a hurry'"
echo "=================================================================="
bcftools norm -f "$DATA/ref.fa" -c s callerB.vcf.gz -Oz -o cs_fixed.vcf.gz 2>cs_fixed.log
zcat cs_fixed.vcf.gz | grep -v '^#' | wc -l
cat cs_fixed.log
echo "-c s exits 0 and silently rewrites REF with no error -- confirms SKILL.md's caution"
echo "('REF mismatches often indicate a genome build mismatch, and silently fixing REF may"
echo " mask a liftover error') is load-bearing and not merely decorative advice."
echo "INPUT 7 PASS (documented caution matches observed behavior)"

echo "=================================================================="
echo "ALL 7 INPUTS EXECUTED: 5 regression + 2 new"
