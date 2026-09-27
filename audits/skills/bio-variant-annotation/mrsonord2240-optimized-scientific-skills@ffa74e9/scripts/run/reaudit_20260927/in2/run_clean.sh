#!/bin/bash
# Re-audit 2026-09-27 -- Input 2 (Variant A), rerun with each case in its own
# process/file to avoid stdout/stderr buffering interleaving in the combined log.
set -uo pipefail
DATA=/mnt/openscience/audits/bio-variant-annotation/data
BASE=/mnt/openscience/audits/bio-variant-annotation/run/reaudit_20260927
cd "$BASE/in2"

echo "=== Case A: valid run, no GNOMAD_VCF ===" > caseA.txt
bash "$BASE/annotate_vcf.sh" norm.vcf.gz dbsnp_syn.vcf.gz out_a.vcf.gz >> caseA.txt 2>&1
echo "exit=$?" >> caseA.txt

echo "=== Case B: valid run WITH GNOMAD_VCF ===" > caseB.txt
GNOMAD_VCF=gnomad_syn.vcf.gz bash "$BASE/annotate_vcf.sh" norm.vcf.gz dbsnp_syn.vcf.gz out_b.vcf.gz >> caseB.txt 2>&1
echo "exit=$?" >> caseB.txt

echo "=== Case C: unindexed target VCF ===" > caseC.txt
bash "$BASE/annotate_vcf.sh" norm_noidx.vcf.gz dbsnp_syn.vcf.gz out_c.vcf.gz >> caseC.txt 2>&1
echo "exit=$?" >> caseC.txt

echo "=== Case D: GNOMAD_VCF set but path does not exist ===" > caseD.txt
GNOMAD_VCF=/mnt/openscience/does_not_exist.vcf.gz bash "$BASE/annotate_vcf.sh" norm.vcf.gz dbsnp_syn.vcf.gz out_d.vcf.gz >> caseD.txt 2>&1
echo "exit=$?" >> caseD.txt

echo "=== Case E: chr1 vs 1 contig mismatch ===" > caseE.txt
GNOMAD_VCF=gnomad_syn.vcf.gz bash "$BASE/annotate_vcf.sh" nochr.vcf.gz dbsnp_syn.vcf.gz out_e.vcf.gz >> caseE.txt 2>&1
echo "exit=$?" >> caseE.txt

echo "=== Case F: PATH restricted to /usr/bin:/bin (system bcftools 1.22 present, not truly 'missing') ===" > caseF.txt
PATH=/usr/bin:/bin bash "$BASE/annotate_vcf.sh" norm.vcf.gz dbsnp_syn.vcf.gz out_f.vcf.gz >> caseF.txt 2>&1
echo "exit=$?" >> caseF.txt
