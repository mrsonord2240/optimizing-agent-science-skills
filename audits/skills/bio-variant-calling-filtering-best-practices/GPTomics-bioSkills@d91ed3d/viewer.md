> **Audit record for `bio-variant-calling-filtering-best-practices`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/variant-calling/filtering-best-practices) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-variant-calling-filtering-best-practices
Generated: 2026-09-15 · Auditor: variant-annotation-curation-analyst round-2 audit · skill-auditor@1.0

Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:variant-calling/filtering-best-practices`  
Category: Data Analysis · Mode A · Complexity: Complex → N = 7. Several task types (VQSR/VETS/NVScoreVariants/hard filters, genotype-level, somatic, Python, validation) with branching method selection; 3 files.

Environment and data: Mode A. Windows: bcftools 1.24 (MSYS2 build, plugins via BCFTOOLS_PLUGINS) and GATK 4.6.1.0 (OpenJDK 17); WSL agents distro (files passed by tar, no drive mount): bcftools 1.21, cyvcf2 0.34.0. Data SYNTHETIC (data/make_data.py, seed 20260911): 8-sample raw joint callset, 361 sites with planted truth in data/cohort_truth_classes.tsv (240 true SNPs, 25 hom-alt-only true sites, 20 true indels, 6 excess-het paralog sites, 60 artifact SNPs, 10 artifact indels), plus SYNTHETIC DeepVariant-shaped (runs/in6) and Mutect2-shaped (runs/in7) VCFs. Not executed: FilterMutectCalls itself (needs Mutect2 stats/contamination tables; flags checked with --help), VETS and NVScoreVariants (no model/GPU).

## Step 1 — Skill Veto
T1 stability PASS (instruction Skill, deterministic tools), T2 contract PASS (frontmatter name/description present), T3 determinism PASS (no stochastic steps without seeds), T4 security PASS (no eval/exec of user strings, no credentials).

## Step 2 — Static score: 84/100
| Category | Score | Note |
|---|---|---|
| Functional suitability | 10/12 | VQSR/hard-filter/genotype guidance verified: GATK VariantFiltration with the SKILL.md thresholds kept 240/240 true SNPs, 25/25 hom-alt, 20/20 true indels and 8/70 artifacts; the guarded bcftools expression reproduced the GATK SNP PASS set exactly. Three shipped snippets fail: examples/filter_variants.sh aborts at bcftools concat on any multi-chromosome input, and the somatic FMT/AF[0] and usage-guide AD[1]/(AD[0]+AD[1]) expressions are rejected by bcftools 1.21 and 1.24 (Number=A/R tags need [sample:subfield]). |
| Reliability | 9/12 | Common Errors table maps hom-alt loss, VQSR non-convergence and empty output to fixes; it misses the concat-contiguity and subfield-index errors the Skill's own code triggers. |
| Performance context | 7/8 | 261-line SKILL.md; dense tables, all load-bearing. |
| Agent usability | 14/16 | Governing principle (site vs genotype, SNP vs indel, missing=>PASS) is exactly what an agent needs; the cyvcf2 block is presented as the Python counterpart but omits QD/SOR/RankSum terms (kept 26/60 artifacts vs 4/60). |
| Human usability | 7/8 | Natural prompts in usage guide; method-selection table readable. |
| Security | 11/12 | Local files only; no credentials; no destructive commands. |
| Maintainability | 8/12 | Modular sections; the shipped example is broken for multi-contig input and no test data ships to catch it. |
| Agent specific | 18/20 | Precise trigger with hand-offs to normalization and vcf-statistics; DL-caller and somatic escape hatches explicit. |

Shipped-means-present (gate 8): SKILL.md cross-references other Skills only; usage-guide.md and examples/filter_variants.sh exist. PASS (the example exists but fails on multi-contig input, see P1).

Research scope (gate 7): Callset filtering; no individual-level interpretation. PASS.

## Summary Table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 34 | 50 | 84 | 3/4 | yes | ✅ |
| 2 | Variant A | 35 | 51 | 86 | 3/4 | yes | ✅ |
| 3 | Edge | 37 | 54 | 91 | 4/4 | yes | ✅ |
| 4 | Variant B | 36 | 53 | 89 | 4/4 | yes | ✅ |
| 5 | Stress | 34 | 50 | 84 | 3/4 | yes | ✅ |
| 6 | Scope Boundary | 36 | 52 | 88 | 4/4 | yes | ✅ |
| 7 | Adversarial | 30 | 44 | 74 | 2/4 | yes | ⚠️ |

**Execution Average: 85.1 / 100** · **Assertion Pass Rate: 23/28 (82 %)** · Layer 1 avg 34.6 · Layer 2 avg 50.6

Research Veto: scientific integrity PASS; practice boundaries PASS; methodological ground PASS; code usability PASS.  
**Final: 84 × 0.4 + 85.1 × 0.6 = 33.6 + 51.1 = 85 → ✅ Limited Release** (Production Ready floor not met (assertions): downgraded one tier)

## Detailed Outputs

### Input 1 — Canonical: GATK hard filters on an 8-sample joint callset
**Prompt:** "Apply GATK best-practice hard filters to our 8-sample joint callset, SNPs and indels separately, and tell me what was removed."

**Executed:** yes — runs/in1/run.sh on Windows (bcftools 1.24, GATK 4.6.1.0); shipped example run from an upstream byte copy (git show).

Code (`runs/in1/run.sh`):
```bash
#!/bin/bash
# Input 1 (Canonical): "Apply GATK best-practice hard filters to our 8-sample joint callset (cohort.vcf),
# SNPs and indels separately, and tell me what was removed." SYNTHETIC data (data/make_data.py).
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -t -f cohort.vcf.gz
git -C F:/OpenScience/external/GPTomics__bioSkills show HEAD:variant-calling/filtering-best-practices/examples/filter_variants.sh > filter_variants.upstream_copy.sh
echo "### bcftools $(bcftools --version | head -1)"
echo "### shipped examples/filter_variants.sh (Windows bcftools 1.24)"
bash filter_variants.upstream_copy.sh cohort.vcf.gz ex > ex.log 2>&1; echo "script exit=$?"
grep -E "Merging|not contiguous|Could not read|Failed" ex.log
ls ex_all_filtered.vcf.gz 2>&1
echo "### GATK $($GATK --version 2>/dev/null | grep -m1 'The Genome Analysis Toolkit')"
$GATK SelectVariants -V cohort.vcf.gz -select-type SNP -O raw_snps.vcf.gz --QUIET true 2>/dev/null; echo "SelectVariants SNP exit=$?"
$GATK SelectVariants -V cohort.vcf.gz -select-type INDEL -O raw_indels.vcf.gz --QUIET true 2>/dev/null; echo "SelectVariants INDEL exit=$?"
# SKILL.md commands verbatim (reference/paths substituted)
$GATK VariantFiltration -R $(cygpath -w $S/ref.fa) -V raw_snps.vcf.gz -O filtered_snps.vcf.gz --QUIET true \
    --filter-expression "QD < 2.0" --filter-name "QD2" \
    --filter-expression "FS > 60.0" --filter-name "FS60" \
    --filter-expression "MQ < 40.0" --filter-name "MQ40" \
    --filter-expression "MQRankSum < -12.5" --filter-name "MQRankSum-12.5" \
    --filter-expression "ReadPosRankSum < -8.0" --filter-name "ReadPosRankSum-8" \
    --filter-expression "SOR > 3.0" --filter-name "SOR3" 2>gatk_snps.log; echo "VariantFiltration SNP exit=$?"
$GATK VariantFiltration -R $(cygpath -w $S/ref.fa) -V raw_indels.vcf.gz -O filtered_indels.vcf.gz --QUIET true \
    --filter-expression "QD < 2.0" --filter-name "QD2" \
    --filter-expression "FS > 200.0" --filter-name "FS200" \
    --filter-expression "ReadPosRankSum < -20.0" --filter-name "ReadPosRankSum-20" \
    --filter-expression "SOR > 10.0" --filter-name "SOR10" 2>gatk_indels.log; echo "VariantFiltration INDEL exit=$?"
echo "SNP FILTER labels (top):"; bcftools query -f '%FILTER\n' filtered_snps.vcf.gz | tr -d '\r' | tr ';' '\n' | sort | uniq -c | sort -rn
echo "INDEL FILTER labels:"; bcftools query -f '%FILTER\n' filtered_indels.vcf.gz | tr -d '\r' | tr ';' '\n' | sort | uniq -c | sort -rn
bcftools concat -a filtered_snps.vcf.gz filtered_indels.vcf.gz 2>/dev/null | bcftools view -f PASS | bcftools query -f '%CHROM\t%POS\n' | tr -d '\r' > gatk_kept.tsv
$PY ../../data/score_truth.py gatk_kept.tsv "GATK VariantFiltration PASS:"
echo "hom-alt-only sites (RankSum missing) that PASS: $(bcftools concat -a filtered_snps.vcf.gz filtered_indels.vcf.gz 2>/dev/null | bcftools view -f PASS -i 'INFO/MQRankSum="."' -H | wc -l) of $(bcftools view -H -i '...
echo "### Fixed example (concat -a) to confirm the only defect is the concat step"
sed -e 's/bcftools concat "\${OUTPUT_PREFIX}_snps_filtered.vcf.gz"/bcftools concat -a "${OUTPUT_PREFIX}_snps_filtered.vcf.gz"/' \
    -e '/=== Merging filtered variants ===/a bcftools index -f "${OUTPUT_PREFIX}_snps_filtered.vcf.gz"; bcftools index -f "${OUTPUT_PREFIX}_indels_filtered.vcf.gz"' \
    filter_variants.upstream_copy.sh > filter_variants.concat_a.sh
diff filter_variants.upstream_copy.sh filter_variants.concat_a.sh
bash filter_variants.concat_a.sh cohort.vcf.gz fx > fx.log 2>&1; echo "fixed script exit=$?"
grep -E "Ti/Tv ratio" fx.log
bcftools query -f '%CHROM\t%POS\n' fx_all_filtered.vcf.gz | tr -d '\r' > fx_kept.tsv; $PY ../../data/score_truth.py fx_kept.tsv "example (concat -a) kept:"
```
Printed (`runs/in1/out.txt`, trimmed):
```
### bcftools bcftools 1.24
### shipped examples/filter_variants.sh (Windows bcftools 1.24)
script exit=127
=== Merging filtered variants ===
The chromosome block chr1 is not contiguous, consider running with -a.
Could not read VCF/BCF headers from -
ls: cannot access 'ex_all_filtered.vcf.gz': No such file or directory
### GATK The Genome Analysis Toolkit (GATK) v4.6.1.0
SelectVariants SNP exit=0
SelectVariants INDEL exit=0
VariantFiltration SNP exit=0
VariantFiltration INDEL exit=0
SNP FILTER labels (top):
    275 PASS
     39 QD2
     28 SOR3
     28 ReadPosRankSum-8
     23 FS60
     18 MQRankSum-12.5
     13 MQ40
INDEL FILTER labels:
     24 PASS
      6 QD2
      2 SOR10
      1 ReadPosRankSum-20
GATK VariantFiltration PASS: true_snp:240/240 true_homalt:25/25 true_indel:20/20 excess_het:6/6 artifact_snp:4/60 artifact_indel:4/10
hom-alt-only sites (RankSum missing) that PASS: 25 of 25
### Fixed example (concat -a) to confirm the only defect is the concat step
44c44,45
< bcftools concat "${OUTPUT_PREFIX}_snps_filtered.vcf.gz" "${OUTPUT_PREFIX}_indels_filtered.vcf.gz" | \
---
> bcftools index -f "${OUTPUT_PREFIX}_snps_filtered.vcf.gz"; bcftools index -f "${OUTPUT_PREFIX}_indels_filtered.vcf.gz"
> bcftools concat -a "${OUTPUT_PREFIX}_snps_filtered.vcf.gz" "${OUTPUT_PREFIX}_indels_filtered.vcf.gz" | \
fixed script exit=0
Ti/Tv ratio: 1.72 (expected ~2.0-2.1 for WGS, ~3.0-3.3 for exomes)
example (concat -a) kept: true_snp:240/240 true_homalt:25/25 true_indel:20/20 excess_het:6/6 artifact_snp:4/60 artifact_indel:4/10
```

**Output (agent answer, Mode A):** Split the callset with SelectVariants, applied the SKILL.md SNP thresholds (QD<2, FS>60, MQ<40, MQRankSum<-12.5, ReadPosRankSum<-8, SOR>3) and indel thresholds (QD<2, FS>200, ReadPosRankSum<-20, SOR>10), then merged. 56 SNP and 7 indel records were flagged (QD2 is the most common label, 39 SNPs); every hom-alt-only site passed because GATK treats missing RankSums as passing. Reported the FILTER label counts and advised checking the QD/FS histograms before tightening. Noted that the shipped helper script needs `bcftools concat -a` on indexed files to finish.

**Scores:** Basic 34/40 | Specialized 50/60 | Total 84/100 · **Assertions 3/4**
- [PASS] SNPs and indels are split and filtered with type-specific thresholds — SelectVariants by type; FS60 vs FS200, ReadPosRankSum -8 vs -20
- [PASS] Hom-alt sites with missing RankSum annotations survive — 25/25 PASS
- [PASS] Filtering removes most artifacts without losing true variants — 8/70 artifacts kept; 0 of 285 true sites lost
- [FAIL] The shipped example script runs end to end — concat without -a aborts on two-chromosome input; no output written

### Input 2 — Variant A: bcftools replica of the GATK filter plus cyvcf2 version
**Prompt:** "Reproduce the GATK SNP hard filter in bcftools so hom-alt sites don't get dropped, and give me a cyvcf2 version I can extend."

**Executed:** yes — runs/in2/run.sh (Windows bcftools 1.24) and run_py.sh in WSL (cyvcf2 0.34.0) via tar hand-over.

Code (`runs/in2/run.sh`):
```bash
#!/bin/bash
# Input 2 (Variant A): "Reproduce the GATK SNP hard filter in bcftools so hom-alt sites don't get dropped,
# and give me a cyvcf2 version for custom logic." SYNTHETIC data.
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf | bcftools view -v snps -Oz -o snps.vcf.gz; bcftools index -f snps.vcf.gz
echo "SNP records: $(bcftools view -H snps.vcf.gz | wc -l); records without MQRankSum (hom-alt-only sites): $(bcftools view -H -i 'INFO/MQRankSum="."' snps.vcf.gz | wc -l)"
# SKILL.md block, expression verbatim
bcftools filter -i '
    QUAL >= 30 && (INFO/QD >= 2.0 || INFO/QD = ".") &&
    (INFO/FS <= 60.0 || INFO/FS = ".") && (INFO/MQ >= 40.0 || INFO/MQ = ".") &&
    (INFO/MQRankSum >= -12.5 || INFO/MQRankSum = ".") &&
    (INFO/ReadPosRankSum >= -8.0 || INFO/ReadPosRankSum = ".") &&
    (INFO/SOR <= 3.0 || INFO/SOR = ".")' snps.vcf.gz -Oz -o snps_guarded.vcf.gz; echo "guarded exit=$?"
# The naive translation the Skill warns against
bcftools filter -i 'QUAL >= 30 && INFO/QD >= 2.0 && INFO/FS <= 60.0 && INFO/MQ >= 40.0 && INFO/MQRankSum >= -12.5 && INFO/ReadPosRankSum >= -8.0 && INFO/SOR <= 3.0' snps.vcf.gz -Oz -o snps_naive.vcf.gz
for f in snps_guarded snps_naive; do bcftools query -f '%CHROM\t%POS\n' $f.vcf.gz | tr -d '\r' > $f.tsv; $PY ../../data/score_truth.py $f.tsv "$f:"; done
echo "== Python (cyvcf2) block: run in WSL, see run_py.sh / out_py.txt =="
```
Code (`runs/in2/py_filter.py`):
```python
# SKILL.md "Python Filtering (cyvcf2)" block, verbatim except the input path (SYNTHETIC SNP VCF).
from cyvcf2 import VCF, Writer

vcf = VCF('snps.vcf.gz')
writer = Writer('filtered.vcf', vcf)
for variant in vcf:
    qual = variant.QUAL or 0
    dp = variant.INFO.get('DP') or 1e9      # missing depth => do not fail on depth
    fs = variant.INFO.get('FS') or 0.0      # missing strand bias => pass (None -> 0)
    mq = variant.INFO.get('MQ') or 1e9      # missing MQ => pass
    if qual >= 30 and dp >= 10 and fs <= 60.0 and mq >= 40.0:
        writer.write_record(variant)
writer.close(); vcf.close()
```
Printed (`runs/in2/out.txt`, trimmed):
```
SNP records: 331; records without MQRankSum (hom-alt-only sites): 24
guarded exit=0
snps_guarded: true_snp:240/240 true_homalt:25/25 true_indel:0/20 excess_het:6/6 artifact_snp:4/60 artifact_indel:0/10
snps_naive: true_snp:239/240 true_homalt:2/25 true_indel:0/20 excess_het:6/6 artifact_snp:4/60 artifact_indel:0/10
== Python (cyvcf2) block: run in WSL, see run_py.sh / out_py.txt ==
```
Printed (`runs/in2/out_py.txt`, trimmed):
```
cyvcf2 0.34.0
py_filter exit=0
cyvcf2 block kept: true_snp:240/240 true_homalt:25/25 true_indel:0/20 excess_het:6/6 artifact_snp:26/60 artifact_indel:0/10
QD<2 artifacts kept by the Python block (it has no QD term): 12
rc=0
```

**Output (agent answer, Mode A):** Gave the SKILL.md guarded expression, explaining that each RankSum term needs `|| INFO/X="."` because RankSums are undefined at hom-alt sites; showed that dropping the guard deletes 23 of 25 hom-alt sites. For Python, gave the cyvcf2 loop but stated that it is a starting point: to match the hard filter it must add QD, SOR and the guarded RankSum checks (as written it keeps 26 of 60 artifacts).

**Scores:** Basic 35/40 | Specialized 51/60 | Total 86/100 · **Assertions 3/4**
- [PASS] Guarded bcftools expression reproduces the GATK PASS set — same 240/25/6/4 counts as VariantFiltration
- [PASS] Naive translation loses hom-alt sites, as the Skill warns — 2/25 kept
- [PASS] cyvcf2 block runs as written — exit 0 in WSL
- [FAIL] cyvcf2 block implements the same filter as the bcftools/GATK expression — no QD/SOR/RankSum terms; 26/60 artifacts vs 4/60

### Input 3 — Edge: VQSR requested for an 8-sample panel
**Prompt:** "We only have 8 jointly-called samples on a small targeted panel. Set up VQSR like the GATK best practices."

**Executed:** yes — runs/in3/run.sh (GATK 4.6.1.0) with a SYNTHETIC circular truth resource (the simulation's true sites: best case for VQSR).

Code (`runs/in3/run.sh`):
```bash
#!/bin/bash
# Input 3 (Edge): "We only have 8 jointly-called samples on a small targeted panel. Set up VQSR like the
# GATK best practices." The Skill says VQSR is non-identifiable here; we run the SKILL.md command anyway
# to observe what happens, using a SYNTHETIC truth resource (the simulation's true sites: a best case).
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -t -f cohort.vcf.gz
awk -F'\t' 'NR>1 && ($3=="true_snp"||$3=="true_homalt") {print $1"\t"$2}' $S/cohort_truth_classes.tsv > truth_pos.tsv
bcftools view -T truth_pos.tsv -v snps cohort.vcf.gz | bcftools view -G -Oz -o truth_resource.vcf.gz; bcftools index -t -f truth_resource.vcf.gz
bcftools view -G -v snps cohort.vcf.gz -i 'ID!="."' -Oz -o known_resource.vcf.gz; bcftools index -t -f known_resource.vcf.gz
echo "variants: $(bcftools view -H -v snps cohort.vcf.gz | wc -l) SNPs; resource sites: truth=$(bcftools view -H truth_resource.vcf.gz | wc -l) known=$(bcftools view -H known_resource.vcf.gz | wc -l)"
echo "== SKILL.md VariantRecalibrator (-an QD MQ MQRankSum ReadPosRankSum FS SOR, -mode SNP) =="
$GATK VariantRecalibrator -R $(cygpath -w $S/ref.fa) -V cohort.vcf.gz \
    --resource:hapmap,known=false,training=true,truth=true,prior=15.0 truth_resource.vcf.gz \
    --resource:dbsnp,known=true,training=false,truth=false,prior=2.0 known_resource.vcf.gz \
    -an QD -an MQ -an MQRankSum -an ReadPosRankSum -an FS -an SOR \
    -mode SNP -O snp.recal --tranches-file snp.tranches 2> vqsr.log; echo "VariantRecalibrator exit=$?"
grep -E "USER ERROR|Bad input" vqsr.log | head -3
echo "== retry without MQ (constant 60 at simulated true sites: synthetic-data artifact) =="
$GATK VariantRecalibrator -R $(cygpath -w $S/ref.fa) -V cohort.vcf.gz \
    --resource:hapmap,known=false,training=true,truth=true,prior=15.0 truth_resource.vcf.gz \
    --resource:dbsnp,known=true,training=false,truth=false,prior=2.0 known_resource.vcf.gz \
    -an QD -an MQRankSum -an ReadPosRankSum -an FS -an SOR \
    -mode SNP -O snp2.recal --tranches-file snp2.tranches 2> vqsr2.log; echo "VariantRecalibrator exit=$?"
grep -E "Convergence|Training with|very few|worst" vqsr2.log | head -6
grep -v '^#' snp2.tranches
$GATK ApplyVQSR -R $(cygpath -w $S/ref.fa) -V cohort.vcf.gz -mode SNP --recal-file snp2.recal --tranches-file snp2.tranches \
    --truth-sensitivity-filter-level 99.7 -O snp_vqsr.vcf.gz --QUIET true 2>/dev/null; echo "ApplyVQSR 99.7 exit=$?"
bcftools view -v snps -f PASS snp_vqsr.vcf.gz | bcftools query -f '%CHROM\t%POS\n' | tr -d '\r' > vqsr_kept.tsv
$PY ../../data/score_truth.py vqsr_kept.tsv "VQSR 99.7 PASS (circular best-case truth):"
echo "== what the Skill recommends instead: hard filters (guarded bcftools SNP expression) =="
bcftools view -v snps cohort.vcf.gz | bcftools filter -i 'QUAL >= 30 && (INFO/QD >= 2.0 || INFO/QD = ".") && (INFO/FS <= 60.0 || INFO/FS = ".") && (INFO/MQ >= 40.0 || INFO/MQ = ".") && (INFO/MQRankSum >= -12.5 || INFO...
$PY ../../data/score_truth.py hard_kept.tsv "hard filter PASS:"
```
Printed (`runs/in3/out.txt`, trimmed):
```
variants: 331 SNPs; resource sites: truth=265 known=225
== SKILL.md VariantRecalibrator (-an QD MQ MQRankSum ReadPosRankSum FS SOR, -mode SNP) ==
VariantRecalibrator exit=2
A USER ERROR has occurred: Bad input: Found annotations with zero variance. They must be excluded before proceeding.
== retry without MQ (constant 60 at simulated true sites: synthetic-data artifact) ==
Tool returned:
true
VariantRecalibrator exit=0
06:40:07.299 INFO  VariantDataManager - Training with 265 variants after standard deviation thresholding.
06:40:07.299 WARN  VariantDataManager - WARNING: Training with very few variant sites! Please check the model reporting PDF to ensure the quality of the model is reliable.
06:40:07.499 INFO  VariantRecalibratorEngine - Convergence after 31 iterations!
06:40:07.517 INFO  VariantDataManager - Selected worst 10 scoring variants --> variants with LOD <= -5.0000.
06:40:07.518 INFO  VariantRecalibratorEngine - Convergence after 3 iterations!
targetTruthSensitivity,numKnown,numNovel,knownTiTv,novelTiTv,minVQSLod,filterName,model,accessibleTruthSites,callsAtTruthSites,truthSensitivity
90.00,205,93,1.5309,1.2683,3.4348,VQSRTrancheSNP0.00to90.00,SNP,265,238,0.8981
99.00,223,99,1.5341,1.3571,-1.1940,VQSRTrancheSNP90.00to99.00,SNP,265,262,0.9887
99.90,225,102,1.5281,1.3182,-8.1859,VQSRTrancheSNP99.00to99.90,SNP,265,264,0.9962
100.00,225,106,1.5281,1.2553,-10.4436,VQSRTrancheSNP99.90to100.00,SNP,265,265,1.0000
ApplyVQSR 99.7 exit=0
VQSR 99.7 PASS (circular best-case truth): true_snp:239/240 true_homalt:25/25 true_indel:0/20 excess_het:6/6 artifact_snp:57/60 artifact_indel:0/10
== what the Skill recommends instead: hard filters (guarded bcftools SNP expression) ==
hard filter PASS: true_snp:240/240 true_homalt:25/25 true_indel:0/20 excess_het:6/6 artifact_snp:4/60 artifact_indel:0/10
```

**Output (agent answer, Mode A):** Advised against VQSR: 331 SNPs across 8 samples are far too few to fit the Gaussian mixture, and GATK may still report convergence while VQSLOD is noise. Recommended the per-type hard filters (or VETS/NVScoreVariants if validated against a truth set), and explained that a tranche is a truth-set sensitivity, not an FDR. Showed the VQSR trial on this panel keeping 57 of 60 artifacts.

**Scores:** Basic 37/40 | Specialized 54/60 | Total 91/100 · **Assertions 4/4**
- [PASS] Steers away from VQSR on a small panel — Skill table and pitfalls applied
- [PASS] Recommends hard filters, VETS or NVScoreVariants instead — hard filters kept 4/60 artifacts
- [PASS] SKILL.md VariantRecalibrator/ApplyVQSR syntax is valid in GATK 4.6.1.0 — resource tags parsed; tranches and recal files written
- [PASS] Tranche is explained as truth sensitivity, not FDR — tranche file truthSensitivity column matches

### Input 4 — Variant B: Genotype-level no-calls before cohort metrics
**Prompt:** "Null out low-confidence genotypes before I compute per-sample missingness and HWE on the cohort."

**Executed:** yes — runs/in4/run.sh (Windows bcftools 1.24, +fill-tags plugin).

Code (`runs/in4/run.sh`):
```bash
#!/bin/bash
# Input 4 (Variant B): "Null out low-confidence genotypes before I compute per-sample missingness and HWE
# on the cohort." Site filter -> genotype filter (SKILL.md verbatim) -> recompute cohort metrics. SYNTHETIC data.
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -f cohort.vcf.gz
bcftools filter -i '(TYPE="snp" && QUAL>=30 && (INFO/QD>=2.0||INFO/QD=".") && (INFO/FS<=60.0||INFO/FS=".") && (INFO/MQ>=40.0||INFO/MQ=".") && (INFO/MQRankSum>=-12.5||INFO/MQRankSum=".") && (INFO/ReadPosRankSum>=-8.0||...
echo "passing sites: $(bcftools view -H passing_sites.vcf.gz | wc -l)"
# SKILL.md genotype-level command, verbatim
bcftools filter -S . -e 'FMT/GQ<20 | FMT/DP<8' passing_sites.vcf.gz -Oz -o gt_filtered.vcf.gz; echo "genotype filter exit=$?"
bcftools index -f gt_filtered.vcf.gz
echo "sites retained by -S . (genotype-level, site kept): $(bcftools view -H gt_filtered.vcf.gz | wc -l)"
bcftools query -l cohort.vcf.gz | tr -d '\r' | tr '\n' ' '; echo
for f in passing_sites gt_filtered; do
  echo "[$f] per-sample ./. : $(bcftools query -f '[%GT\t]\n' $f.vcf.gz | tr -d '\r' | awk '{for(i=1;i<=NF;i++) if($i=="./.") m[i]++} END{for(i=1;i<=8;i++) printf m[i]+0" "}')"
done
echo "genotypes that are GQ<20 or DP<8 but not no-call before: $(bcftools query -i 'GT!="mis"' -f '[%GT:%GQ:%DP\t]\n' passing_sites.vcf.gz | tr -d '\r' | tr '\t' '\n' | awk -F: 'NF==3 && $1!="./." && ($2<20 || $3<8)' ...
echo "== did -S . touch ONLY the failing genotypes? count of failing genotypes left un-nulled after: $(bcftools query -f '[%GT:%GQ:%DP\t]\n' gt_filtered.vcf.gz | tr -d '\r' | tr '\t' '\n' | awk -F: 'NF==3 && $1!="./."...
echo "== per-site missingness / HWE-type effect: sites with F_MISSING>=0.05 before vs after =="
echo "before: $(bcftools view -H -i 'F_MISSING>=0.05' passing_sites.vcf.gz | wc -l)  after: $(bcftools view -H -i 'F_MISSING>=0.05' gt_filtered.vcf.gz | wc -l)"
echo "== ExcessHet-style check with bcftools +fill-tags HWE before/after =="
for f in passing_sites gt_filtered; do
  bcftools +fill-tags $f.vcf.gz -- -t HWE,ExcHet 2>/dev/null | bcftools query -f '%HWE\n' | tr -d '\r' | awk -v n=$f '$1<0.001{c++} END{print n": sites HWE p<0.001 = "c+0}'
done
```
Printed (`runs/in4/out.txt`, trimmed):
```
passing sites: 299
genotype filter exit=0
sites retained by -S . (genotype-level, site kept): 299
SYN_S1 SYN_S2 SYN_S3 SYN_S4 SYN_S5 SYN_S6 SYN_S7 SYN_S8 
[passing_sites] per-sample ./. : 0 0 0 0 0 59 0 0 
[gt_filtered] per-sample ./. : 2 1 3 3 0 59 13 1 
genotypes that are GQ<20 or DP<8 but not no-call before: 23
== did -S . touch ONLY the failing genotypes? count of failing genotypes left un-nulled after: 0
== per-site missingness / HWE-type effect: sites with F_MISSING>=0.05 before vs after ==
before: 59  after: 77
== ExcessHet-style check with bcftools +fill-tags HWE before/after ==
passing_sites: sites HWE p<0.001 = 0
gt_filtered: sites HWE p<0.001 = 0
```

**Output (agent answer, Mode A):** Ordered the work site filter -> genotype filter -> cohort QC. Used `bcftools filter -S . -e 'FMT/GQ<20 | FMT/DP<8'`, which nulls 23 genotypes and keeps every site, then recomputed missingness (77 sites now above 5 % missing) and HWE on the cleaned matrix, reminding that only ./. counts as missing.

**Scores:** Basic 36/40 | Specialized 53/60 | Total 89/100 · **Assertions 4/4**
- [PASS] Genotype filter keeps sites and nulls only failing genotypes — 299 sites kept; 23 nulled; 0 failing left
- [PASS] Site -> genotype -> cohort-QC order stated and followed — per SKILL.md
- [PASS] Missingness recomputed after nulling — 59 -> 77 sites above 5 %
- [PASS] ./. is not treated as 0/0 — per-sample ./. counts reported

### Input 5 — Stress: End-to-end filter and validation
**Prompt:** "End to end: split by type, apply site filters, merge, null bad genotypes, drop an exclusion BED, then validate with Ti/Tv, known% and FILTER counts before and after."

**Executed:** yes — runs/in5/run.sh (Windows bcftools 1.24).

Code (`runs/in5/run.sh`):
```bash
#!/bin/bash
# Input 5 (Stress): "End to end: split by type, apply site filters, merge, null bad genotypes, drop an exclusion
# BED, then validate with Ti/Tv, known%, and FILTER counts before/after." SYNTHETIC data (a 35-kb toy genome,
# so expected WGS/WES Ti/Tv ranges do not apply; the simulation used Ti:Tv 2:1 for true sites, 1:2 for artifacts).
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -f cohort.vcf.gz
bcftools view -v snps cohort.vcf.gz -Oz -o s.vcf.gz; bcftools view -v indels cohort.vcf.gz -Oz -o i.vcf.gz
bcftools filter -i 'QUAL>=30 && (INFO/QD>=2.0||INFO/QD=".") && (INFO/FS<=60.0||INFO/FS=".") && (INFO/MQ>=40.0||INFO/MQ=".") && (INFO/MQRankSum>=-12.5||INFO/MQRankSum=".") && (INFO/ReadPosRankSum>=-8.0||INFO/ReadPosRan...
bcftools filter -i 'QUAL>=30 && (INFO/QD>=2.0||INFO/QD=".") && (INFO/FS<=200.0||INFO/FS=".") && (INFO/ReadPosRankSum>=-20.0||INFO/ReadPosRankSum=".") && (INFO/SOR<=10.0||INFO/SOR=".")' i.vcf.gz -Oz -o if.vcf.gz
for f in sf if; do bcftools index -f $f.vcf.gz; done
bcftools concat -a sf.vcf.gz if.vcf.gz -Oz -o sites.vcf.gz 2>/dev/null; bcftools index -f sites.vcf.gz
bcftools filter -S . -e 'FMT/GQ<20 | FMT/DP<8' sites.vcf.gz -Oz -o final.vcf.gz; bcftools index -f final.vcf.gz
printf 'chr2\t0\t1000\n' > exclude.bed
bcftools view -T ^exclude.bed final.vcf.gz -Oz -o final_excl.vcf.gz; echo "exclusion view exit=$?"
echo "records in excluded interval before: $(bcftools view -H -r chr2:1-1000 final.vcf.gz | wc -l)"
for f in cohort sites final_excl; do
  tstv=$(bcftools stats $f.vcf.gz | grep '^TSTV' | cut -f5 | tr -d '\r')
  known=$(bcftools view -H $f.vcf.gz | awk '{n++; if($3!=".") k++} END{printf "%.1f", 100*k/n}')
  echo "$f: records=$(bcftools view -H $f.vcf.gz | wc -l) Ti/Tv=$tstv known%=$known"
done
bcftools query -f '%CHROM\t%POS\n' final_excl.vcf.gz | tr -d '\r' > kept.tsv; $PY ../../data/score_truth.py kept.tsv "final:"
echo "== SKILL.md validation idiom: bcftools stats | grep ^TSTV prints: =="; bcftools stats final_excl.vcf.gz | grep '^TSTV'
echo "== usage-guide allele-balance expression (verbatim) =="
bcftools filter -i 'GT="het" && (AD[1]/(AD[0]+AD[1]) > 0.2 && AD[1]/(AD[0]+AD[1]) < 0.8)' final.vcf.gz -o ab_filtered.vcf 2> ab.err; echo "AB filter exit=$?"; head -3 ab.err
echo "AB-filtered records: $(grep -vc '^#' ab_filtered.vcf 2>/dev/null)"
echo "== the corrected per-sample form (FMT/AD[:1]) =="
bcftools filter -i 'GT="het" & FMT/AD[:1]/(FMT/AD[:0]+FMT/AD[:1]) > 0.2 & FMT/AD[:1]/(FMT/AD[:0]+FMT/AD[:1]) < 0.8' final.vcf.gz 2>&1 | grep -vc '^#'
```
Printed (`runs/in5/out.txt`, trimmed):
```
exclusion view exit=0
records in excluded interval before: 10
cohort: records=361 Ti/Tv=1.43 known%=67.6
sites: records=299 Ti/Tv=1.72 known%=81.6
final_excl: records=289 Ti/Tv=1.68 known%=82.4
final: true_snp:232/240 true_homalt:24/25 true_indel:20/20 excess_het:6/6 artifact_snp:3/60 artifact_indel:4/10
== SKILL.md validation idiom: bcftools stats | grep ^TSTV prints: ==
TSTV	0	166	99	1.68	166	99	1.68
== usage-guide allele-balance expression (verbatim) ==
AB filter exit=127
The FORMAT tag AD can have multiple subfields, run as AD[sample:subfield]
AB-filtered records: 0
== the corrected per-sample form (FMT/AD[:1]) ==
262
```

**Output (agent answer, Mode A):** Ran the split/filter/merge (with `concat -a`), genotype nulling and `view -T ^exclude.bed`, then compared before/after: Ti/Tv 1.43 -> 1.68 and known fraction 67.6 % -> 82.4 %, both moving in the direction the Skill describes for removing false positives. Noted that the WGS/WES Ti/Tv ranges do not apply to this small synthetic target, and replaced the usage-guide allele-balance expression with the per-sample `FMT/AD[:1]` form after bcftools rejected it.

**Scores:** Basic 34/40 | Specialized 50/60 | Total 84/100 · **Assertions 3/4**
- [PASS] Steps run in the Skill order — site -> genotype -> region -> validation
- [PASS] Before/after Ti/Tv and known% computed with the Skill idioms — bcftools stats TSTV field 5; ID column
- [PASS] Exclusion BED removes the region — 10 records in chr2:1-1000 removed
- [FAIL] Usage-guide allele-balance filter runs — bcftools: run as AD[sample:subfield]

### Input 6 — Scope Boundary: GATK filters requested for DeepVariant output
**Prompt:** "These calls came from DeepVariant. Apply the GATK hard filters to them before annotation."

**Executed:** yes — runs/in6/run.sh on a SYNTHETIC DeepVariant-shaped VCF (annotations stripped, FILTER=RefCall on low QUAL).

Code (`runs/in6/run.sh`):
```bash
#!/bin/bash
# Input 6 (Scope boundary): "These calls came from DeepVariant. Apply the GATK hard filters to them before
# annotation." The Skill says DL-native caller output must NOT get GATK hard filters. We build a SYNTHETIC
# DeepVariant-shaped VCF (no QD/FS/MQ/SOR/RankSum annotations; FILTER=RefCall on low-QUAL records) and show
# what the GATK expressions actually do to it.
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -f cohort.vcf.gz
bcftools annotate -x INFO/QD,INFO/FS,INFO/MQ,INFO/SOR,INFO/MQRankSum,INFO/ReadPosRankSum,INFO/ExcessHet cohort.vcf.gz \
  | sed 's/^##source=SYNTHETIC_cohort_GATKlike_raw_joint_callset/##source=SYNTHETIC_DeepVariant_shaped\n##FILTER=<ID=RefCall,Description="Genotyping model thinks this site is reference.">/' \
  | awk 'BEGIN{OFS="\t"} /^#/{print;next} {if($6<40) $7="RefCall"; else $7="PASS"; print}' \
  | bgzip -c > dv.vcf.gz; bcftools index -t -f dv.vcf.gz
echo "DV-shaped records: $(bcftools view -H dv.vcf.gz | wc -l); FILTER: $(bcftools query -f '%FILTER\n' dv.vcf.gz | tr -d '\r' | sort | uniq -c | tr '\n' ' ')"
echo "== (a) guarded bcftools GATK SNP+indel expressions on DV output =="
bcftools filter -i '(TYPE="snp" && QUAL>=30 && (INFO/QD>=2.0||INFO/QD=".") && (INFO/FS<=60.0||INFO/FS=".") && (INFO/MQ>=40.0||INFO/MQ=".") && (INFO/MQRankSum>=-12.5||INFO/MQRankSum=".") && (INFO/ReadPosRankSum>=-8.0||...
head -2 a.err; $PY ../../data/score_truth.py a_kept.tsv "guarded GATK expr on DV (effectively QUAL>=30 only):"
echo "== (b) GATK VariantFiltration SNP command on DV output =="
$GATK VariantFiltration -R $(cygpath -w $S/ref.fa) -V dv.vcf.gz -O dv_gatk.vcf.gz \
    --filter-expression "QD < 2.0" --filter-name "QD2" --filter-expression "FS > 60.0" --filter-name "FS60" \
    --filter-expression "MQ < 40.0" --filter-name "MQ40" --filter-expression "SOR > 3.0" --filter-name "SOR3" 2> b.log; echo "exit=$?"
grep -m3 -iE "warn.*(QD|attribute|JEXL)|undefined" b.log
echo "FILTER after VariantFiltration: $(bcftools query -f '%FILTER\n' dv_gatk.vcf.gz | tr -d '\r' | sort | uniq -c | tr '\n' ' ')"
echo "== (c) what the Skill routes to instead: caller's own FILTER + QUAL/GQ (deepvariant skill idiom) =="
bcftools view -f PASS dv.vcf.gz | bcftools view -i 'QUAL>20 && FMT/GQ>20' | bcftools query -f '%CHROM\t%POS\n' | tr -d '\r' > c_kept.tsv
$PY ../../data/score_truth.py c_kept.tsv "FILTER=PASS + QUAL>20 & any-sample GQ>20:"
```
Printed (`runs/in6/out.txt`, trimmed):
```
DV-shaped records: 361; FILTER:     336 PASS      25 RefCall 
== (a) guarded bcftools GATK SNP+indel expressions on DV output ==
Failed to read from standard input: unknown file type
[filter.c:3615 filters_init1] Error: the tag "QD" is not defined in the VCF header
guarded GATK expr on DV (effectively QUAL>=30 only): true_snp:0/240 true_homalt:0/25 true_indel:0/20 excess_het:0/6 artifact_snp:0/60 artifact_indel:0/10
== (b) GATK VariantFiltration SNP command on DV output ==
exit=0
06:43:47.734 WARN  JexlEngine - ![0,2]: 'MQ < 40.0;' undefined variable MQ
06:43:47.734 WARN  JexlEngine - ![0,2]: 'FS > 60.0;' undefined variable FS
06:43:47.734 WARN  JexlEngine - ![0,3]: 'SOR > 3.0;' undefined variable SOR
FILTER after VariantFiltration:     336 PASS      25 RefCall 
== (c) what the Skill routes to instead: caller's own FILTER + QUAL/GQ (deepvariant skill idiom) ==
FILTER=PASS + QUAL>20 & any-sample GQ>20: true_snp:240/240 true_homalt:25/25 true_indel:20/20 excess_het:6/6 artifact_snp:39/60 artifact_indel:6/10
```

**Output (agent answer, Mode A):** Declined to run GATK hard filters: DeepVariant output has no QD/FS/MQ/SOR/RankSum annotations and its FILTER column is already the CNN decision, so the GATK expressions either do nothing or error. Recommended keeping FILTER=PASS and thresholding QUAL/GQ, and handed normalization and annotation to their Skills.

**Scores:** Basic 36/40 | Specialized 52/60 | Total 88/100 · **Assertions 4/4**
- [PASS] Declines GATK hard filters on DeepVariant output — Site-level method table row
- [PASS] Routes to the caller's FILTER and QUAL/GQ — kept 285/285 true sites
- [PASS] Explains why the annotations are absent or a no-op — matches the JEXL warnings observed
- [PASS] Stays within filtering scope — annotation handed off

### Input 7 — Adversarial: Germline filter requested for Mutect2 calls
**Prompt:** "Tumor-normal Mutect2 calls. Skip FilterMutectCalls, just run the germline hard filter we used before, then keep TLOD>6.3, tumor VAF>5% and tumor DP>20 like your example."

**Executed:** yes — runs/in7/run.sh: GATK FilterMutectCalls --help (tool not run: needs Mutect2 stats/contamination tables) and bcftools 1.24 on a SYNTHETIC Mutect2-shaped VCF (normal column first).

Code (`runs/in7/run.sh`):
```bash
#!/bin/bash
# Input 7 (Adversarial / ambiguous): "Tumor-normal Mutect2 calls. Skip FilterMutectCalls, just run the germline
# hard filter we used before, then keep TLOD>6.3, tumor VAF>5%, tumor DP>20 like your example."
# Checks: (1) the Skill refuses the germline filter for somatic data; (2) the FilterMutectCalls flags exist
# in GATK 4.6.1.0; (3) the SKILL.md bcftools post-filter 'FMT/AF[0]' selects the FIRST sample column,
# which is the NORMAL when the VCF lists the normal first. SYNTHETIC Mutect2-shaped VCF.
set -uo pipefail
source ../env.sh
S=../../data
echo "== FilterMutectCalls flags in GATK 4.6.1.0 =="
$GATK FilterMutectCalls --help 2>&1 | grep -E -- "--contamination-table|--tumor-segmentation|--variant|--reference|--output" | sed 's/^ *//' | cut -c1-90
cat > mutect_syn.vcf <<'EOF'
##fileformat=VCFv4.2
##source=SYNTHETIC_Mutect2_shaped
##contig=<ID=chr1,length=20000>
##INFO=<ID=TLOD,Number=A,Type=Float,Description="Log 10 likelihood ratio score of variant existing versus not existing">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=AD,Number=R,Type=Integer,Description="Allelic depths">
##FORMAT=<ID=AF,Number=A,Type=Float,Description="Allele fractions of alternate alleles in the tumor">
##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Approximate read depth">
##normal_sample=SYN_NORMAL
##tumor_sample=SYN_TUMOR
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	SYN_NORMAL	SYN_TUMOR
chr1	5100	.	C	T	.	PASS	TLOD=25.3	GT:AD:AF:DP	0/0:40,0:0.012:40	0/1:30,12:0.29:42
chr1	5200	.	G	A	.	PASS	TLOD=18.1	GT:AD:AF:DP	0/0:35,0:0.014:35	0/1:40,8:0.17:48
chr1	5300	.	A	G	.	PASS	TLOD=7.9	GT:AD:AF:DP	0/0:38,1:0.03:39	0/1:50,4:0.07:54
chr1	5400	.	T	C	.	PASS	TLOD=4.1	GT:AD:AF:DP	0/0:30,0:0.016:30	0/1:45,2:0.04:47
chr1	5500	.	G	T	.	PASS	TLOD=60.2	GT:AD:AF:DP	0/1:20,19:0.49:39	0/1:21,20:0.49:41
EOF
bgzip -c mutect_syn.vcf > mutect_syn.vcf.gz; bcftools index -f mutect_syn.vcf.gz
echo "samples (column order): $(bcftools query -l mutect_syn.vcf.gz | tr -d '\r' | tr '\n' ' ')"
echo "== SKILL.md post-filter verbatim: INFO/TLOD>6.3 && FMT/AF[0]>0.05 && FMT/DP[0]>20 =="
bcftools filter -i 'INFO/TLOD>6.3 && FMT/AF[0]>0.05 && FMT/DP[0]>20' mutect_syn.vcf.gz 2> v.err | bcftools query -f '%POS\t[%SAMPLE=%AF ]\n' | tr -d '\r'; head -2 v.err
echo "(expected somatic keepers 5100,5200,5300; 5500 is a germline het present in the normal)"
echo "== minimal syntax fix, AF[0:0] (sample 0 = first column = NORMAL here) =="
bcftools filter -i 'INFO/TLOD>6.3 && FMT/AF[0:0]>0.05 && FMT/DP[0]>20' mutect_syn.vcf.gz | bcftools query -f '%POS\t[%SAMPLE=%AF ]\n' | tr -d '\r'
echo "== sample-explicit fix, AF[1:0] (tumor column) =="
bcftools filter -i 'INFO/TLOD>6.3 && FMT/AF[1:0]>0.05 && FMT/DP[1]>20' mutect_syn.vcf.gz | bcftools query -f '%POS\t[%SAMPLE=%AF ]\n' | tr -d '\r'
```
Printed (`runs/in7/out.txt`, trimmed):
```
== FilterMutectCalls flags in GATK 4.6.1.0 ==
--output,-O <String>          The output filtered VCF file  Required. 
--reference,-R <GATKPath>     Reference sequence file  Required. 
--variant,-V <GATKPath>       A VCF file containing variants  Required. 
--contamination-table <File>  Tables containing contamination information.  This argument 
--tumor-segmentation <File>   Tables containing tumor segments' minor allele fractions for
--variant-output-filtering <Mode>
samples (column order): SYN_NORMAL SYN_TUMOR 
== SKILL.md post-filter verbatim: INFO/TLOD>6.3 && FMT/AF[0]>0.05 && FMT/DP[0]>20 ==
Failed to read from standard input: unknown file type
The FORMAT tag AF can have multiple subfields, run as AF[sample:subfield]
(expected somatic keepers 5100,5200,5300; 5500 is a germline het present in the normal)
== minimal syntax fix, AF[0:0] (sample 0 = first column = NORMAL here) ==
5500	SYN_NORMAL=0.49 SYN_TUMOR=0.49 
== sample-explicit fix, AF[1:0] (tumor column) ==
5100	SYN_NORMAL=0.012 SYN_TUMOR=0.29 
5200	SYN_NORMAL=0.014 SYN_TUMOR=0.17 
5300	SYN_NORMAL=0.03 SYN_TUMOR=0.07 
5500	SYN_NORMAL=0.49 SYN_TUMOR=0.49 
```

**Output (agent answer, Mode A):** Refused to apply germline VQSR/hard filters to somatic calls and gave the FilterMutectCalls command with contamination and segmentation tables. For the post-filter, first got a bcftools error from the Skill's `FMT/AF[0]`, then wrote the tumor-explicit form `FMT/AF[1:0]>0.05 && FMT/DP[1]>20` after reading the sample order from `bcftools query -l` and the ##tumor_sample header, warning that the obvious `AF[0:0]` fix would test the normal.

**Scores:** Basic 30/40 | Specialized 44/60 | Total 74/100 · **Assertions 2/4**
- [PASS] Refuses germline hard filters for somatic calls — Somatic track in SKILL.md
- [PASS] FilterMutectCalls flags are valid — --contamination-table, --tumor-segmentation in --help
- [FAIL] SKILL.md post-filter expression runs — Number=A AF needs [sample:subfield]
- [FAIL] Post-filter guidance selects the tumor sample — index 0 is the normal when it is listed first

## Key strengths
- Hard-filter thresholds and the missing-RankSum => PASS rule are right: the guarded bcftools expression reproduced GATK VariantFiltration's PASS set site for site
- Method selection is honest about regimes: the VQSR-on-small-panel warning was borne out (57/60 artifacts kept vs 4/60 with hard filters)
- Site- vs genotype-level ordering, SNP/indel separation and the DeepVariant/somatic escape hatches are explicit and correct
- GATK commands are valid for 4.6.1.0 as written

## Recommendations
- **[P1] Shipped filter_variants.sh fails on multi-contig input** (inputs [1]) — bcftools concat without -a aborts ("chromosome block chr1 is not contiguous") whenever the SNP and indel files span more than one chromosome, so the script never writes its merged output. *Root cause:* concat is applied to two position-interleaved, unindexed files. *Fix:* Index both filtered files and use `bcftools concat -a`; verified that the script then produces the same PASS set as GATK.
- **[P1] Somatic post-filter uses invalid, wrong-sample indexing** (inputs [7]) — `FMT/AF[0]>0.05` is rejected for Number=A AF, and the obvious fix AF[0:0] filters the first sample column, which is the normal in tumor-normal VCFs listing the normal first. *Root cause:* Sample and subfield indexing were not tested on a two-sample Mutect2 VCF. *Fix:* Use `FMT/AF[T:0]` with T taken from `bcftools query -l` or the ##tumor_sample header (or `bcftools view -s TUMOR` first) and state which column is tested.
- **[P2] Usage-guide allele-balance expression does not parse** (inputs [5]) — `AD[1]/(AD[0]+AD[1])` is rejected by bcftools 1.21 and 1.24. *Root cause:* Number=R FORMAT tag indexed without sample:subfield. *Fix:* Write `GT="het" & FMT/AD[:1]/(FMT/AD[:0]+FMT/AD[:1])>0.2 & FMT/AD[:1]/(FMT/AD[:0]+FMT/AD[:1])<0.8`.
- **[P2] cyvcf2 block is not equivalent to the hard filter** (inputs [2]) — The Python block checks only QUAL/DP/FS/MQ and kept 26/60 artifacts where the bcftools/GATK filter kept 4. *Root cause:* Presented as the Python counterpart but omits QD, SOR and RankSum terms. *Fix:* Add QD, SOR and None-guarded RankSum checks, or label the block a minimal example.
- **[P2] Common Errors table misses the Skill's own failure modes** (inputs [1, 5, 7]) — The concat-contiguity and "multiple subfields" errors hit by the Skill's code are not in the table. *Root cause:* Table written from generic experience rather than running the recipes. *Fix:* Add rows for both errors with the fixes above.
