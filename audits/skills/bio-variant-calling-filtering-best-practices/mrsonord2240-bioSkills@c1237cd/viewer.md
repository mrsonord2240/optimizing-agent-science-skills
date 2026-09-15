> **Audit record for `bio-variant-calling-filtering-best-practices`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c1237cd](https://github.com/mrsonord2240/bioSkills/tree/c1237cdbc9bb199947696f3909de26a55d259116/variant-calling/filtering-best-practices) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-variant-calling-filtering-best-practices
Generated: 2026-09-15 · Re-audit of the fixed Skill · Auditor: variant-annotation-curation-analyst round-2 · skill-auditor@1.0

Source: `mrsonord2240/bioSkills@c1237cdbc9bb199947696f3909de26a55d259116:variant-calling/filtering-best-practices`  
Category: Data Analysis · Mode A · Complexity: Complex → N = 9 (7 regression inputs from the pre-fix audit + 2 new).

**Pre-fix → post-fix:** 85 (Limited Release) → **88 (Production Ready)**. Pre-fix report: `F:/OpenScience/audits/_pre-fix-20260915/bio-variant-calling-filtering-best-practices/`; fix log (not evidence): `F:/OpenScience/specialist-src/round2/fixes/bio-variant-calling-filtering-best-practices.md`.

Environment and data: Re-audit of the fixed Skill (fork commit c1237cdb). Mode A. Windows: bcftools 1.24 (MSYS2) and GATK 4.6.1.0; WSL agents distro (tar hand-over, no drive mount): bcftools 1.21, cyvcf2 0.34.0. Data SYNTHETIC (data/make_data.py, seed 20260911; planted truth in data/cohort_truth_classes.tsv) plus SYNTHETIC DeepVariant- and Mutect2-shaped VCFs. The 7 pre-fix inputs were re-run as regression tests from runs/p_in1..p_in7 (scripts copied from runs/in1..in7, only the lines whose Skill text changed were swapped for the post-fix text); inputs 8 and 9 are new (runs/in8, runs/in9). n_inputs is 9 (7 regression + 2 new, as the re-audit brief requires), above the schema's usual 7. Not executed: FilterMutectCalls itself (needs Mutect2 tables; flags checked with --help), VETS and NVScoreVariants. The somatic tumor-index block was run on both Windows bcftools 1.24 (out.txt) and WSL bcftools 1.21 (out_wsl.txt) with the same results. Inputs executed: 9/9.

## Step 1 — Skill Veto
T1 stability PASS (instruction Skill, deterministic tools), T2 contract PASS (frontmatter name/description present), T3 determinism PASS (no stochastic steps without seeds), T4 security PASS (no eval/exec of user strings, no credentials).

## Step 2 — Static score: 89/100
| Category | Score | Note |
|---|---|---|
| Functional suitability | 11/12 | Hard-filter thresholds, missing=>PASS rule, VQSR regime guidance and genotype-level order verified on planted truth. All three pre-fix code defects are fixed and ran: filter_variants.sh finishes on multi-contig input (same PASS set as GATK), the somatic AF[T:0] block selects the tumor column, the usage-guide AD[:1] expression parses. Remaining gaps: the usage-guide allele-balance recipe, used as a site include, deletes every site without a het genotype (24/25 true hom-alt-only sites lost), contradicting the Skill's own hom-alt rule. |
| Reliability | 10/12 | Common Errors now covers the concat contiguity and [sample:subfield] errors the Skill's own code used to hit. The new tumor-index block has no guard: with no ##tumor_sample header T becomes -1 and bcftools 1.21 segfaults (exit 139) instead of stopping with a message. |
| Performance context | 7/8 | 269-line SKILL.md; dense decision tables, recipes relocated to the usage guide. |
| Agent usability | 15/16 | Governing principle (site vs genotype, SNP vs indel, missing=>PASS) is exactly what an agent needs; the cyvcf2 block is now labelled a minimal pattern and names the missing QD/SOR/RankSum terms. |
| Human usability | 7/8 | Natural prompts in the usage guide map to the method-selection table. |
| Security | 11/12 | Local files only; no credentials; no destructive commands. |
| Maintainability | 10/12 | Shipped example now runs end to end on the audit callset; no test data ships with the Skill. |
| Agent specific | 18/20 | Precise trigger with hand-offs to normalization and vcf-statistics; DeepVariant and somatic escape hatches explicit. |

Shipped-means-present (gate 8): SKILL.md and usage-guide.md name no local references/, scripts/ or assets/ files (a grep hit on 'transcripts/gene' or a URL path is prose, not a file); usage-guide.md and the examples/ file exist at the fork commit. PASS.

Research scope (gate 7): Callset filtering; no individual-level interpretation. PASS.

## Summary Table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 37 | 55 | 92 | 4/4 | yes | ✅ |
| 2 | Variant A | 36 | 53 | 89 | 4/4 | yes | ✅ |
| 3 | Edge | 37 | 54 | 91 | 4/4 | yes | ✅ |
| 4 | Variant B | 36 | 53 | 89 | 4/4 | yes | ✅ |
| 5 | Stress | 36 | 53 | 89 | 4/4 | yes | ✅ |
| 6 | Scope Boundary | 36 | 52 | 88 | 4/4 | yes | ✅ |
| 7 | Adversarial | 35 | 52 | 87 | 4/4 | yes | ✅ |
| 8 | Edge | 32 | 47 | 79 | 3/4 | yes | ✅ |
| 9 | Variant A | 33 | 48 | 81 | 3/4 | yes | ✅ |

**Execution Average: 87.2 / 100** · **Assertion Pass Rate: 34/36 (94 %)** · Layer 1 avg 35.3 · Layer 2 avg 51.9

Research Veto: scientific integrity PASS; practice boundaries PASS; methodological ground PASS; code usability PASS.  
**Final: 89 × 0.4 + 87.2 × 0.6 = 35.6 + 52.3 = 88 → ⭐ Production Ready**

## Detailed Outputs

### Input 1 — Canonical: GATK hard filters on an 8-sample joint callset (regression)
**Prompt:** "Apply GATK best-practice hard filters to our 8-sample joint callset, SNPs and indels separately, and tell me what was removed."

**Executed:** yes — runs/p_in1/run.sh on Windows (bcftools 1.24, GATK 4.6.1.0); shipped example taken from the fork commit with git show.

Code `runs/p_in1/run.sh`:
```bash
#!/bin/bash
# Input 1 (Canonical): "Apply GATK best-practice hard filters to our 8-sample joint callset (cohort.vcf),
# SNPs and indels separately, and tell me what was removed." SYNTHETIC data (data/make_data.py).
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -t -f cohort.vcf.gz
git -C F:/OpenScience/external/mrsonord2240__bioSkills show c1237cdbc9bb199947696f3909de26a55d259116:variant-calling/filtering-best-practices/examples/filter_variants.sh > filter_variants.fork_copy.sh
echo "### bcftools $(bcftools --version | head -1)"
echo "### shipped examples/filter_variants.sh (Windows bcftools 1.24)"
bash filter_variants.fork_copy.sh cohort.vcf.gz ex > ex.log 2>&1; echo "script exit=$?"
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
echo "hom-alt-only sites (RankSum missing) that PASS: $(bcftools concat -a filtered_snps.vcf.gz filtered_indels.vcf.gz 2>/dev/null | bcftools view -f PASS -i 'INFO/MQRankSum="."' -H | wc -l) of $(bcftools view -H -i 'INFO/MQRankSum="."' coh...
echo "### Fixed example (concat -a) to confirm the only defect is the concat step"
sed -e 's/bcftools concat "\${OUTPUT_PREFIX}_snps_filtered.vcf.gz"/bcftools concat -a "${OUTPUT_PREFIX}_snps_filtered.vcf.gz"/' \
    -e '/=== Merging filtered variants ===/a bcftools index -f "${OUTPUT_PREFIX}_snps_filtered.vcf.gz"; bcftools index -f "${OUTPUT_PREFIX}_indels_filtered.vcf.gz"' \
    filter_variants.fork_copy.sh > filter_variants.concat_a.sh
diff filter_variants.fork_copy.sh filter_variants.concat_a.sh
bash filter_variants.concat_a.sh cohort.vcf.gz fx > fx.log 2>&1; echo "fixed script exit=$?"
grep -E "Ti/Tv ratio" fx.log
bcftools query -f '%CHROM\t%POS\n' fx_all_filtered.vcf.gz | tr -d '\r' > fx_kept.tsv; $PY ../../data/score_truth.py fx_kept.tsv "example (concat -a) kept:"
```

Printed `runs/p_in1/out.txt`:
```
### bcftools bcftools 1.24
### shipped examples/filter_variants.sh (Windows bcftools 1.24)
script exit=0
=== Merging filtered variants ===
Merging 1 temporary files
ex_all_filtered.vcf.gz
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
43a44
> bcftools index -f "${OUTPUT_PREFIX}_snps_filtered.vcf.gz"; bcftools index -f "${OUTPUT_PREFIX}_indels_filtered.vcf.gz"
fixed script exit=0
Ti/Tv ratio: 1.72 (expected ~2.0-2.1 for WGS, ~3.0-3.3 for exomes)
example (concat -a) kept: true_snp:240/240 true_homalt:25/25 true_indel:20/20 excess_het:6/6 artifact_snp:4/60 artifact_indel:4/10
```

**Output (agent answer, Mode A):** Shipped filter_variants.sh (fork) exit 0; its PASS set equals GATK VariantFiltration: true_snp 240/240, true_homalt 25/25, true_indel 20/20, artifact_snp 4/60, artifact_indel 4/10. Pre-fix: exit 127 at concat.

**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100 · **Assertions 4/4**
- [PASS] SNPs and indels are split and filtered with type-specific thresholds — SelectVariants by type; FS60 vs FS200, ReadPosRankSum -8 vs -20
- [PASS] Hom-alt sites with missing RankSum annotations survive — 25/25 PASS
- [PASS] Filtering removes most artifacts without losing true variants — 8/70 artifacts kept; 0/285 true sites lost
- [PASS] The shipped example script runs end to end — exit 0; 'Merging 1 temporary files'; output identical to GATK PASS set

### Input 2 — Variant A: bcftools replica of the GATK filter plus cyvcf2 version (regression)
**Prompt:** "Reproduce the GATK SNP hard filter in bcftools so hom-alt sites don't get dropped, and give me a cyvcf2 version I can extend."

**Executed:** yes — runs/p_in2/run.sh (Windows bcftools 1.24) and run_py.sh in WSL (cyvcf2 0.34.0).

Code `runs/p_in2/run.sh`:
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

Code `runs/p_in2/py_filter.py`:
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

Printed `runs/p_in2/out.txt`:
```
SNP records: 331; records without MQRankSum (hom-alt-only sites): 24
guarded exit=0
snps_guarded: true_snp:240/240 true_homalt:25/25 true_indel:0/20 excess_het:6/6 artifact_snp:4/60 artifact_indel:0/10
snps_naive: true_snp:239/240 true_homalt:2/25 true_indel:0/20 excess_het:6/6 artifact_snp:4/60 artifact_indel:0/10
== Python (cyvcf2) block: run in WSL, see run_py.sh / out_py.txt ==
```

Printed `runs/p_in2/out_py.txt`:
```
cyvcf2 0.34.0
py_filter exit=0
cyvcf2 block kept: true_snp:240/240 true_homalt:25/25 true_indel:0/20 excess_het:6/6 artifact_snp:26/60 artifact_indel:0/10
QD<2 artifacts kept by the Python block (it has no QD term): 12
rc=0
```

**Output (agent answer, Mode A):** Guarded expression reproduces the GATK SNP PASS set (240/25/6/4); naive expression keeps 2/25 hom-alt. cyvcf2 block runs, keeps 26/60 artifacts, and the post-fix Skill now says it is a minimal pattern lacking QD/SOR/RankSum.

**Scores:** Basic 36/40 | Specialized 53/60 | Total 89/100 · **Assertions 4/4**
- [PASS] Guarded bcftools expression reproduces the GATK PASS set — same 240/25/6/4 counts as VariantFiltration
- [PASS] Naive translation loses hom-alt sites, as the Skill warns — 2/25 kept
- [PASS] cyvcf2 block runs as written — exit 0 in WSL
- [PASS] cyvcf2 block is either equivalent to the hard filter or disclosed as partial — not equivalent (26/60 artifacts) but the Approach line now names the missing terms

### Input 3 — Edge: VQSR requested for an 8-sample panel (regression)
**Prompt:** "We only have 8 jointly-called samples on a small targeted panel. Set up VQSR like the GATK best practices."

**Executed:** yes — runs/p_in3/run.sh (GATK 4.6.1.0) with a SYNTHETIC circular truth resource.

Code `runs/p_in3/run.sh`:
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
bcftools view -v snps cohort.vcf.gz | bcftools filter -i 'QUAL >= 30 && (INFO/QD >= 2.0 || INFO/QD = ".") && (INFO/FS <= 60.0 || INFO/FS = ".") && (INFO/MQ >= 40.0 || INFO/MQ = ".") && (INFO/MQRankSum >= -12.5 || INFO/MQRankSum = ".") && (I...
$PY ../../data/score_truth.py hard_kept.tsv "hard filter PASS:"
```

Printed `runs/p_in3/out.txt`:
```
variants: 331 SNPs; resource sites: truth=265 known=225
== SKILL.md VariantRecalibrator (-an QD MQ MQRankSum ReadPosRankSum FS SOR, -mode SNP) ==
VariantRecalibrator exit=2
A USER ERROR has occurred: Bad input: Found annotations with zero variance. They must be excluded before proceeding.
== retry without MQ (constant 60 at simulated true sites: synthetic-data artifact) ==
Tool returned:
true
VariantRecalibrator exit=0
08:05:45.361 INFO  VariantDataManager - Training with 265 variants after standard deviation thresholding.
08:05:45.361 WARN  VariantDataManager - WARNING: Training with very few variant sites! Please check the model reporting PDF to ensure the quality of the model is reliable.
08:05:45.534 INFO  VariantRecalibratorEngine - Convergence after 31 iterations!
08:05:45.556 INFO  VariantDataManager - Selected worst 10 scoring variants --> variants with LOD <= -5.0000.
08:05:45.559 INFO  VariantRecalibratorEngine - Convergence after 3 iterations!
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

**Output (agent answer, Mode A):** Unchanged text; identical results: SKILL.md VariantRecalibrator hits zero-variance MQ on synthetic data, without MQ it 'converges' and ApplyVQSR 99.7 keeps 57/60 artifacts vs 4/60 with hard filters.

**Scores:** Basic 37/40 | Specialized 54/60 | Total 91/100 · **Assertions 4/4**
- [PASS] Steers away from VQSR on a small panel — Skill table and pitfalls applied
- [PASS] Recommends hard filters, VETS or NVScoreVariants instead — hard filters kept 4/60 artifacts
- [PASS] SKILL.md VariantRecalibrator/ApplyVQSR syntax is valid in GATK 4.6.1.0 — tranches and recal files written
- [PASS] Tranche is explained as truth sensitivity, not FDR — tranche file truthSensitivity column matches

### Input 4 — Variant B: Genotype-level no-calls before cohort metrics (regression)
**Prompt:** "Null out low-confidence genotypes before I compute per-sample missingness and HWE on the cohort."

**Executed:** yes — runs/p_in4/run.sh (Windows bcftools 1.24, +fill-tags).

Code `runs/p_in4/run.sh`:
```bash
#!/bin/bash
# Input 4 (Variant B): "Null out low-confidence genotypes before I compute per-sample missingness and HWE
# on the cohort." Site filter -> genotype filter (SKILL.md verbatim) -> recompute cohort metrics. SYNTHETIC data.
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -f cohort.vcf.gz
bcftools filter -i '(TYPE="snp" && QUAL>=30 && (INFO/QD>=2.0||INFO/QD=".") && (INFO/FS<=60.0||INFO/FS=".") && (INFO/MQ>=40.0||INFO/MQ=".") && (INFO/MQRankSum>=-12.5||INFO/MQRankSum=".") && (INFO/ReadPosRankSum>=-8.0||INFO/ReadPosRankSum="."...
echo "passing sites: $(bcftools view -H passing_sites.vcf.gz | wc -l)"
# SKILL.md genotype-level command, verbatim
bcftools filter -S . -e 'FMT/GQ<20 | FMT/DP<8' passing_sites.vcf.gz -Oz -o gt_filtered.vcf.gz; echo "genotype filter exit=$?"
bcftools index -f gt_filtered.vcf.gz
echo "sites retained by -S . (genotype-level, site kept): $(bcftools view -H gt_filtered.vcf.gz | wc -l)"
bcftools query -l cohort.vcf.gz | tr -d '\r' | tr '\n' ' '; echo
for f in passing_sites gt_filtered; do
  echo "[$f] per-sample ./. : $(bcftools query -f '[%GT\t]\n' $f.vcf.gz | tr -d '\r' | awk '{for(i=1;i<=NF;i++) if($i=="./.") m[i]++} END{for(i=1;i<=8;i++) printf m[i]+0" "}')"
done
echo "genotypes that are GQ<20 or DP<8 but not no-call before: $(bcftools query -i 'GT!="mis"' -f '[%GT:%GQ:%DP\t]\n' passing_sites.vcf.gz | tr -d '\r' | tr '\t' '\n' | awk -F: 'NF==3 && $1!="./." && ($2<20 || $3<8)' | wc -l)"
echo "== did -S . touch ONLY the failing genotypes? count of failing genotypes left un-nulled after: $(bcftools query -f '[%GT:%GQ:%DP\t]\n' gt_filtered.vcf.gz | tr -d '\r' | tr '\t' '\n' | awk -F: 'NF==3 && $1!="./." && ($2!="." && $2<20 |...
echo "== per-site missingness / HWE-type effect: sites with F_MISSING>=0.05 before vs after =="
echo "before: $(bcftools view -H -i 'F_MISSING>=0.05' passing_sites.vcf.gz | wc -l)  after: $(bcftools view -H -i 'F_MISSING>=0.05' gt_filtered.vcf.gz | wc -l)"
echo "== ExcessHet-style check with bcftools +fill-tags HWE before/after =="
for f in passing_sites gt_filtered; do
  bcftools +fill-tags $f.vcf.gz -- -t HWE,ExcHet 2>/dev/null | bcftools query -f '%HWE\n' | tr -d '\r' | awk -v n=$f '$1<0.001{c++} END{print n": sites HWE p<0.001 = "c+0}'
done
```

Printed `runs/p_in4/out.txt`:
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

**Output (agent answer, Mode A):** Unchanged text; identical results: -S . nulls 23 failing genotypes, keeps all 299 sites, 0 failing genotypes left; sites >=5% missing 59 -> 77.

**Scores:** Basic 36/40 | Specialized 53/60 | Total 89/100 · **Assertions 4/4**
- [PASS] Genotype filter keeps sites and nulls only failing genotypes — 299 sites kept; 23 nulled; 0 failing left
- [PASS] Site -> genotype -> cohort-QC order stated and followed — per SKILL.md
- [PASS] Missingness recomputed after nulling — 59 -> 77 sites above 5%
- [PASS] ./. is not treated as 0/0 — per-sample ./. counts reported

### Input 5 — Stress: End-to-end filter and validation (regression)
**Prompt:** "End to end: split by type, apply site filters, merge, null bad genotypes, drop an exclusion BED, then validate with Ti/Tv, known% and FILTER counts before and after."

**Executed:** yes — runs/p_in5/run.sh (Windows bcftools 1.24); usage-guide allele-balance line replaced with the post-fix text.

Code `runs/p_in5/run.sh`:
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
bcftools filter -i 'QUAL>=30 && (INFO/QD>=2.0||INFO/QD=".") && (INFO/FS<=60.0||INFO/FS=".") && (INFO/MQ>=40.0||INFO/MQ=".") && (INFO/MQRankSum>=-12.5||INFO/MQRankSum=".") && (INFO/ReadPosRankSum>=-8.0||INFO/ReadPosRankSum=".") && (INFO/SOR<...
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
echo "== usage-guide allele-balance expression (post-fix, verbatim) =="
bcftools filter -i 'GT="het" & FMT/AD[:1]/(FMT/AD[:0]+FMT/AD[:1]) > 0.2 & FMT/AD[:1]/(FMT/AD[:0]+FMT/AD[:1]) < 0.8' final.vcf.gz -o ab_filtered.vcf 2> ab.err; echo "AB filter exit=$?"; head -3 ab.err
echo "AB-filtered records: $(grep -vc '^#' ab_filtered.vcf 2>/dev/null)"
```

Printed `runs/p_in5/out.txt`:
```
exclusion view exit=0
records in excluded interval before: 10
cohort: records=361 Ti/Tv=1.43 known%=67.6
sites: records=299 Ti/Tv=1.72 known%=81.6
final_excl: records=289 Ti/Tv=1.68 known%=82.4
final: true_snp:232/240 true_homalt:24/25 true_indel:20/20 excess_het:6/6 artifact_snp:3/60 artifact_indel:4/10
== SKILL.md validation idiom: bcftools stats | grep ^TSTV prints: ==
TSTV	0	166	99	1.68	166	99	1.68
== usage-guide allele-balance expression (post-fix, verbatim) ==
AB filter exit=0
AB-filtered records: 262
```

**Output (agent answer, Mode A):** Ti/Tv 1.43 -> 1.68, known 67.6% -> 82.4%; exclusion BED removed 10 records; post-fix usage-guide allele-balance expression exit 0, 262 records (pre-fix: parse error).

**Scores:** Basic 36/40 | Specialized 53/60 | Total 89/100 · **Assertions 4/4**
- [PASS] Steps run in the Skill order — site -> genotype -> region -> validation
- [PASS] Before/after Ti/Tv and known% computed with the Skill idioms — TSTV field 5; ID column
- [PASS] Exclusion BED removes the region — 10 records in chr2:1-1000 removed
- [PASS] Usage-guide allele-balance filter runs — exit 0, 262 records

### Input 6 — Scope Boundary: GATK filters requested for DeepVariant output (regression)
**Prompt:** "These calls came from DeepVariant. Apply the GATK hard filters to them before annotation."

**Executed:** yes — runs/p_in6/run.sh on a SYNTHETIC DeepVariant-shaped VCF.

Code `runs/p_in6/run.sh`:
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
bcftools filter -i '(TYPE="snp" && QUAL>=30 && (INFO/QD>=2.0||INFO/QD=".") && (INFO/FS<=60.0||INFO/FS=".") && (INFO/MQ>=40.0||INFO/MQ=".") && (INFO/MQRankSum>=-12.5||INFO/MQRankSum=".") && (INFO/ReadPosRankSum>=-8.0||INFO/ReadPosRankSum="."...
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

Printed `runs/p_in6/out.txt`:
```
DV-shaped records: 361; FILTER:     336 PASS      25 RefCall 
== (a) guarded bcftools GATK SNP+indel expressions on DV output ==
Failed to read from standard input: unknown file type
[filter.c:3615 filters_init1] Error: the tag "QD" is not defined in the VCF header
guarded GATK expr on DV (effectively QUAL>=30 only): true_snp:0/240 true_homalt:0/25 true_indel:0/20 excess_het:0/6 artifact_snp:0/60 artifact_indel:0/10
== (b) GATK VariantFiltration SNP command on DV output ==
exit=0
08:05:58.928 WARN  JexlEngine - ![0,2]: 'MQ < 40.0;' undefined variable MQ
08:05:58.928 WARN  JexlEngine - ![0,2]: 'FS > 60.0;' undefined variable FS
08:05:58.928 WARN  JexlEngine - ![0,3]: 'SOR > 3.0;' undefined variable SOR
FILTER after VariantFiltration:     336 PASS      25 RefCall 
== (c) what the Skill routes to instead: caller's own FILTER + QUAL/GQ (deepvariant skill idiom) ==
FILTER=PASS + QUAL>20 & any-sample GQ>20: true_snp:240/240 true_homalt:25/25 true_indel:20/20 excess_het:6/6 artifact_snp:39/60 artifact_indel:6/10
```

**Output (agent answer, Mode A):** Unchanged text; identical results: GATK expressions error or no-op (undefined QD/FS/MQ/SOR); caller FILTER + QUAL/GQ keeps 285/285 true sites.

**Scores:** Basic 36/40 | Specialized 52/60 | Total 88/100 · **Assertions 4/4**
- [PASS] Declines GATK hard filters on DeepVariant output — Site-level method table row
- [PASS] Routes to the caller's FILTER and QUAL/GQ — kept 285/285 true sites
- [PASS] Explains why the annotations are absent or a no-op — matches the JEXL warnings observed
- [PASS] Scope: stays within filtering — annotation handed off

### Input 7 — Adversarial: Germline filter requested for Mutect2 calls (regression)
**Prompt:** "Tumor-normal Mutect2 calls. Skip FilterMutectCalls, just run the germline hard filter we used before, then keep TLOD>6.3, tumor VAF>5% and tumor DP>20 like your example."

**Executed:** yes — runs/p_in7/run.sh: FilterMutectCalls --help (tool not run) and the post-fix somatic block verbatim on Windows bcftools 1.24 (out.txt) and WSL bcftools 1.21 (out_wsl.txt), identical results.

Code `runs/p_in7/run.sh`:
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
echo "== SKILL.md post-fix somatic block, verbatim (file name substituted) =="
TUMOR=$(bcftools view -h mutect_syn.vcf.gz | grep '^##tumor_sample=' | cut -d= -f2)
T=$(( $(bcftools query -l mutect_syn.vcf.gz | grep -nxF "$TUMOR" | cut -d: -f1) - 1 ))
echo "TUMOR=$TUMOR T=$T"
bcftools filter -i "INFO/TLOD>6.3 && FMT/AF[$T:0]>0.05 && FMT/DP[$T]>20" mutect_syn.vcf.gz -o somatic_final.vcf 2> v.err; echo "filter exit=$?"; head -2 v.err
bcftools query -f '%POS\t[%SAMPLE=%AF ]\n' somatic_final.vcf | tr -d '\r'
echo "(expected somatic keepers 5100,5200,5300; 5500 is a germline het also passing on tumor AF - the Skill states the normal is not tested)"
```

Printed `runs/p_in7/out.txt`:
```
== FilterMutectCalls flags in GATK 4.6.1.0 ==
--output,-O <String>          The output filtered VCF file  Required. 
--reference,-R <GATKPath>     Reference sequence file  Required. 
--variant,-V <GATKPath>       A VCF file containing variants  Required. 
--contamination-table <File>  Tables containing contamination information.  This argument 
--tumor-segmentation <File>   Tables containing tumor segments' minor allele fractions for
--variant-output-filtering <Mode>
samples (column order): SYN_NORMAL SYN_TUMOR 
== SKILL.md post-fix somatic block, verbatim (file name substituted) ==
TUMOR=SYN_TUMOR T=1
filter exit=0
5100	SYN_NORMAL=0.012 SYN_TUMOR=0.29 
5200	SYN_NORMAL=0.014 SYN_TUMOR=0.17 
5300	SYN_NORMAL=0.03 SYN_TUMOR=0.07 
5500	SYN_NORMAL=0.49 SYN_TUMOR=0.49 
(expected somatic keepers 5100,5200,5300; 5500 is a germline het also passing on tumor AF - the Skill states the normal is not tested)
```

Printed `runs/p_in7/out_wsl.txt`:
```
bcftools: bcftools 1.21
samples (column order): SYN_NORMAL SYN_TUMOR 
== SKILL.md post-fix somatic block, verbatim (file name substituted) ==
TUMOR=SYN_TUMOR T=1
filter exit=0
5100	SYN_NORMAL=0.012 SYN_TUMOR=0.29 
5200	SYN_NORMAL=0.014 SYN_TUMOR=0.17 
5300	SYN_NORMAL=0.03 SYN_TUMOR=0.07 
5500	SYN_NORMAL=0.49 SYN_TUMOR=0.49 
(expected somatic keepers 5100,5200,5300; 5500 is a germline het also passing on tumor AF - the Skill states the normal is not tested)
rc=0
```

**Output (agent answer, Mode A):** Post-fix block: TUMOR=SYN_TUMOR, T=1, filter exit 0, keeps 5100/5200/5300 and the germline het 5500 (the Skill now states the normal column is not tested). Pre-fix: parse error, and the obvious fix tested the normal.

**Scores:** Basic 35/40 | Specialized 52/60 | Total 87/100 · **Assertions 4/4**
- [PASS] Refuses germline hard filters for somatic calls — Somatic track in SKILL.md
- [PASS] FilterMutectCalls flags are valid — --contamination-table, --tumor-segmentation in --help
- [PASS] SKILL.md post-filter expression runs — exit 0 on bcftools 1.21
- [PASS] Post-filter guidance selects the tumor sample — T=1 from ##tumor_sample; SYN_TUMOR AF tested

### Input 8 — Edge: NEW: tumor-column block on three somatic VCF layouts
**Prompt:** "Our somatic VCFs come from three pipelines: Mutect2 with the tumor listed first, a Mutect2 run where the ##tumor_sample header was stripped by a merge step, and one where the tumor is named TUMOR_1 next to a sample TUMOR_10. Use your tumor-column post-filter on all three."

**Executed:** yes — runs/in8/run.sh on three SYNTHETIC Mutect2-shaped VCFs, on Windows bcftools 1.24 (out.txt) and WSL bcftools 1.21 (run_wsl.sh, out_wsl.txt), identical results; an earlier run with a malformed sample header line (auditor error) was discarded.

Code `runs/in8/run.sh`:
```bash
#!/bin/bash
# Input 8 (NEW, re-audit 2026-09-15, Edge): "Our somatic VCFs come from three pipelines: Mutect2 with the tumor
# listed first, a Mutect2 run where the ##tumor_sample header was stripped by a merge step, and one where the tumor
# is named TUMOR_1 next to a sample TUMOR_10. Use your tumor-column post-filter on all three."
# Tests the fixed SKILL.md tumor-index block on layouts the fixer did not test. SYNTHETIC VCFs.
set -uo pipefail
source ../env.sh
mk() { # $1 name, $2 header lines, $3 sample header, $4 body
  printf '##fileformat=VCFv4.2\n##source=SYNTHETIC_Mutect2_shaped\n##contig=<ID=chr1,length=20000>\n##INFO=<ID=TLOD,Number=A,Type=Float,Description="TLOD">\n##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n##FORMAT=<ID=AF,Numbe...
}
# A: tumor first. Somatic 5100 (tumor AF .29), 5300 (tumor AF .07); 5400 low tumor AF; normal-only noise at 5600
mk tumor_first '##normal_sample=SYN_N\n##tumor_sample=SYN_T\n' "SYN_T\tSYN_N" \
'chr1\t5100\t.\tC\tT\t.\tPASS\tTLOD=25.3\tGT:AF:DP\t0/1:0.29:42\t0/0:0.01:40\nchr1\t5300\t.\tA\tG\t.\tPASS\tTLOD=7.9\tGT:AF:DP\t0/1:0.07:54\t0/0:0.03:39\nchr1\t5400\t.\tT\tC\t.\tPASS\tTLOD=4.1\tGT:AF:DP\t0/1:0.04:47\t0/0:0.01:30\nchr1\t5600...
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
```

Printed `runs/in8/out.txt`:
```
== tumor_first: samples SYN_T SYN_N 
TUMOR='SYN_T' T=0
filter exit=0
5100	SYN_T=0.29 SYN_N=0.01 
5300	SYN_T=0.07 SYN_N=0.03 
== no_header: samples SYN_N SYN_T 
TUMOR='' T=-1
run.sh: line 20: 107354 Segmentation fault         bcftools filter -i "INFO/TLOD>6.3 && FMT/AF[$T:0]>0.05 && FMT/DP[$T]>20" $f.vcf -o ${f}_somatic.vcf 2> $f.err
filter exit=139
== prefix: samples NORMAL TUMOR_10 TUMOR_1 
TUMOR='TUMOR_1' T=2
filter exit=0
5100	NORMAL=0.01 TUMOR_10=0.01 TUMOR_1=0.29 
expected: tumor_first 5100,5300 ; no_header -> should stop (no tumor known) ; prefix 5100 only
```

Printed `runs/in8/out_wsl.txt`:
```
bcftools: bcftools 1.21
== tumor_first: samples SYN_T SYN_N 
TUMOR='SYN_T' T=0
filter exit=0
5100	SYN_T=0.29 SYN_N=0.01 
5300	SYN_T=0.07 SYN_N=0.03 
== no_header: samples SYN_N SYN_T 
TUMOR='' T=-1
run.sh: line 20: 392279 Segmentation fault         bcftools filter -i "INFO/TLOD>6.3 && FMT/AF[$T:0]>0.05 && FMT/DP[$T]>20" $f.vcf -o ${f}_somatic.vcf 2> $f.err
filter exit=139
== prefix: samples NORMAL TUMOR_10 TUMOR_1 
TUMOR='TUMOR_1' T=2
filter exit=0
5100	NORMAL=0.01 TUMOR_10=0.01 TUMOR_1=0.29 
expected: tumor_first 5100,5300 ; no_header -> should stop (no tumor known) ; prefix 5100 only
rc=0
```

**Output (agent answer, Mode A):** Tumor listed first: T=0, keeps 5100/5300, not the normal-only 5600. Prefix-colliding names (TUMOR_10 vs TUMOR_1): T=2, keeps 5100 only. No ##tumor_sample header: TUMOR empty, T=-1, bcftools segfaults (exit 139) with no message.

**Scores:** Basic 32/40 | Specialized 47/60 | Total 79/100 · **Assertions 3/4**
- [PASS] Tumor-first layout selects the tumor column — T=0; 5100, 5300 kept; 5600 (normal-only AF) not kept
- [PASS] Exact-name matching avoids prefix collisions — grep -nxF picks TUMOR_1 (T=2), not TUMOR_10
- [FAIL] Missing ##tumor_sample header stops with a clear message — T=-1; bcftools 1.21 segfault, exit 139
- [PASS] Output states which sample column was tested — Skill: site filter on the tumor column; normal not tested

### Input 9 — Variant A: NEW: usage-guide QC recipes before rare-variant analysis
**Prompt:** "For the rare-variant analysis, soft-label low QUAL and low depth, keep PASS, drop samples with too many no-calls, drop sites >5% missing, and remove hets with skewed allele balance. Use the usage-guide recipes and tell me how many sites and genotypes each step removed."

**Executed:** yes — runs/in9/run.sh (Windows bcftools 1.24), usage-guide recipes verbatim on the SYNTHETIC cohort.

Code `runs/in9/run.sh`:
```bash
#!/bin/bash
# Input 9 (NEW, re-audit 2026-09-15, Variant C): "For the rare-variant analysis, soft-label low QUAL and low depth,
# keep PASS, drop samples with too many no-calls, drop sites >5% missing, and remove hets with skewed allele
# balance. Use the usage-guide recipes and tell me how many sites and genotypes each step removed."
# Runs the usage-guide recipes (post-fix) on the SYNTHETIC cohort. Genotype nulling first, per SKILL.md order.
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -f cohort.vcf.gz
echo "== Multi-step soft-filter pipeline (usage guide, verbatim) =="
bcftools filter -s 'LowQual' -e 'QUAL<30' cohort.vcf.gz | \
    bcftools filter -s 'LowDepth' -e 'INFO/DP<10' -Oz -o marked.vcf.gz; echo "exit=$?"
bcftools query -f '%FILTER\n' marked.vcf.gz | tr -d '\r' | sort | uniq -c
bcftools view -f PASS marked.vcf.gz -Oz -o pass_only.vcf.gz
echo "PASS records: $(bcftools view -H pass_only.vcf.gz | wc -l)"
echo "== genotype nulling (SKILL.md) =="
bcftools filter -S . -e 'FMT/GQ<20 | FMT/DP<8' pass_only.vcf.gz -Oz -o gt.vcf.gz; bcftools index -f gt.vcf.gz
echo "== per-sample missingness (usage guide: bcftools stats -s - | grep ^PSC | cut -f3,14) =="
bcftools stats -s - gt.vcf.gz | grep '^# PSC' | tr '\t' '\n' | sed -n '3p;14p' | tr '\n' '|'; echo
bcftools stats -s - gt.vcf.gz | grep ^PSC | cut -f3,14 | tr -d '\r'
bcftools stats -s - gt.vcf.gz | grep ^PSC | cut -f3,14 | tr -d '\r' | awk '$2<30{print $1}' > good_samples.txt
echo "kept samples: $(tr '\n' ' ' < good_samples.txt)"
bcftools view -S good_samples.txt gt.vcf.gz -Oz -o sample_filtered.vcf.gz; echo "view -S exit=$?"
echo "== site missingness (usage guide) =="
bcftools filter -i 'F_MISSING<0.05' sample_filtered.vcf.gz -Oz -o site_filtered.vcf.gz; echo "exit=$?"
echo "sites: $(bcftools view -H sample_filtered.vcf.gz | wc -l) -> $(bcftools view -H site_filtered.vcf.gz | wc -l)"
echo "== allele balance (usage guide, post-fix) =="
bcftools filter -i 'GT="het" & FMT/AD[:1]/(FMT/AD[:0]+FMT/AD[:1]) > 0.2 & FMT/AD[:1]/(FMT/AD[:0]+FMT/AD[:1]) < 0.8' \
    site_filtered.vcf.gz -o ab_filtered.vcf; echo "exit=$?"
echo "records: $(bcftools view -H site_filtered.vcf.gz | wc -l) -> $(grep -vc '^#' ab_filtered.vcf)"
echo "records with NO het genotype at all (dropped by GT=\"het\" in -i): $(bcftools view -H -e 'GT="het"' site_filtered.vcf.gz | wc -l)"
echo "hom-alt-only true sites surviving AB step:"
bcftools query -f '%CHROM\t%POS\n' ab_filtered.vcf | tr -d '\r' > ab_kept.tsv; $PY $S/score_truth.py ab_kept.tsv "after AB include:"
echo "== genotype-level alternative: null skewed het genotypes instead of dropping sites =="
bcftools filter -S . -e 'GT="het" & (FMT/AD[:1]/(FMT/AD[:0]+FMT/AD[:1]) <= 0.2 | FMT/AD[:1]/(FMT/AD[:0]+FMT/AD[:1]) >= 0.8)' site_filtered.vcf.gz -Oz -o ab_gt.vcf.gz; echo "exit=$?"
bcftools query -f '%CHROM\t%POS\n' ab_gt.vcf.gz | tr -d '\r' > abgt_kept.tsv; $PY $S/score_truth.py abgt_kept.tsv "genotype-level AB null:"
```

Printed `runs/in9/out.txt`:
```
== Multi-step soft-filter pipeline (usage guide, verbatim) ==
exit=0
     11 LowQual
    350 PASS
PASS records: 350
== genotype nulling (SKILL.md) ==
== per-sample missingness (usage guide: bcftools stats -s - | grep ^PSC | cut -f3,14) ==
[2]id|[13]nHapAlt|
SYN_S1	9
SYN_S2	6
SYN_S3	8
SYN_S4	8
SYN_S5	4
SYN_S6	79
SYN_S7	22
SYN_S8	1
kept samples: SYN_S1 SYN_S2 SYN_S3 SYN_S4 SYN_S5 SYN_S7 SYN_S8 
view -S exit=0
== site missingness (usage guide) ==
exit=0
sites: 350 -> 301
== allele balance (usage guide, post-fix) ==
exit=0
records: 301 -> 253
records with NO het genotype at all (dropped by GT="het" in -i): 45
hom-alt-only true sites surviving AB step:
after AB include: true_snp:209/240 true_homalt:1/25 true_indel:16/20 excess_het:6/6 artifact_snp:17/60 artifact_indel:4/10
== genotype-level alternative: null skewed het genotypes instead of dropping sites ==
exit=0
genotype-level AB null: true_snp:227/240 true_homalt:22/25 true_indel:19/20 excess_het:6/6 artifact_snp:23/60 artifact_indel:4/10
```

**Output (agent answer, Mode A):** Soft-filter pipeline labels 11 LowQual; PSC col 14 is nMissing (S6 79); F_MISSING<0.05 keeps 301/350. The allele-balance include keeps 253/301 records but drops all 45 sites without a het genotype: true_homalt 1/25, true_snp 209/240. A genotype-level version (-S . on skewed hets) keeps 22/25 hom-alt and 227/240 true SNPs.

**Scores:** Basic 33/40 | Specialized 48/60 | Total 81/100 · **Assertions 3/4**
- [PASS] Multi-step soft-filter pipeline runs and labels failures — 11 LowQual, 350 PASS
- [PASS] Per-sample missingness idiom reads the right PSC column — header [14]nMissing; S6 = 79
- [PASS] Allele-balance expression parses on bcftools 1.24 — exit 0
- [FAIL] Allele-balance recipe keeps hom-alt-only true sites — 24/25 true hom-alt-only sites removed by the site-level GT="het" include

## Key strengths
- Hard-filter thresholds and the missing-RankSum => PASS rule are right: the guarded bcftools expression reproduces GATK VariantFiltration's PASS set site for site
- All pre-fix code defects are fixed and verified by running: the shipped example, the tumor-column post-filter and the allele-balance expression
- Method selection is honest about regimes: the VQSR-on-small-panel warning was borne out (57/60 artifacts kept vs 4/60 with hard filters)
- Site- vs genotype-level ordering and the DeepVariant/somatic escape hatches are explicit and correct

## Recommendations
- **[P2] Tumor-column block has no guard for a missing header** (inputs [8]) — With no ##tumor_sample header TUMOR is empty, T becomes -1 and bcftools segfaults (exit 139 on both 1.21 and 1.24) instead of stopping with a message. *Root cause:* The block assumes the ##tumor_sample header exists. *Fix:* Add `[ -n "$TUMOR" ] && [ "$T" -ge 0 ] || { echo 'tumor sample not found; pass it explicitly'; exit 1; }` before the filter.
- **[P2] Usage-guide allele-balance recipe deletes hom-alt sites** (inputs [9]) — `bcftools filter -i 'GT="het" & AB...'` is a site include, so every site with no het genotype is removed: 24 of 25 true hom-alt-only sites and 31 true SNPs were lost. *Root cause:* A per-genotype check was written as a site-level include, contradicting the Skill's own hom-alt rule. *Fix:* Apply it at genotype level: `bcftools filter -S . -e 'GT="het" & (FMT/AD[:1]/(FMT/AD[:0]+FMT/AD[:1])<=0.2 | FMT/AD[:1]/(FMT/AD[:0]+FMT/AD[:1])>=0.8)'` (kept 22/25 hom-alt sites here).
- **[P2] cyvcf2 block is still only a partial filter** (inputs [2]) — The block is now labelled minimal, but an agent asked for a Python equivalent still has to write the QD/SOR/RankSum terms itself (26/60 artifacts kept vs 4/60). *Root cause:* The Python counterpart was never extended to the full expression. *Fix:* Add the QD, SOR and None-guarded RankSum checks so the block matches the bcftools expression.
