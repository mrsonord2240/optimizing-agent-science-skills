> **Audit record for `bio-vcf-statistics`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/optimized-scientific-skills@2dee47f](https://github.com/mrsonord2240/optimized-scientific-skills/tree/2dee47f80dac6f3ba5c78b53ea9ec132a87cf5db/skills/bio-vcf-statistics) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-25 by Codex independent auditor agent, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-vcf-statistics

Generated: 2026-09-25

Source: `mrsonord2240/optimized-scientific-skills@2dee47f80dac6f3ba5c78b53ea9ec132a87cf5db:skills/bio-vcf-statistics`

Auditor independence: `true`

Category: Data Analysis · Mode D · Complexity: Complex · N=7

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 38 | 56 | 94 | 4/4 | ✅ |
| 2 | Variant A | 39 | 56 | 95 | 4/4 | ✅ |
| 3 | Variant B | 35 | 53 | 88 | 3/4 | ✅ |
| 4 | Edge | 32 | 46 | 78 | 3/4 | ✅ |
| 5 | Stress | 38 | 56 | 94 | 4/4 | ✅ |
| 6 | Scope Boundary | 37 | 54 | 91 | 4/4 | ✅ |
| 7 | Adversarial | 37 | 55 | 92 | 4/4 | ✅ |

**Execution Average: 90.3 / 100**
**Layer 1 Average: 36.6 / 40**
**Layer 2 Average: 53.7 / 60**
**Assertion Pass Rate: 26/28 (92.9%)**

The complete saved harness is `run/run_all.sh`; its final log is `outputs/reaudit_attempt4.log`. It used bcftools 1.24 from the documented alignment-files environment, VCFtools 0.1.17 from the existing `atac-jvm` environment after a read-only path search, and system WSL Python with cyvcf2 0.31.4. No environment was installed into or changed.

## Detailed Outputs

### Input 1 — Canonical: prior synthetic cohort statistics regression

**Prompt:** Generate comprehensive cohort and per-sample VCF statistics for the retained eight-sample synthetic callset, including Ti/Tv and the distinction between strict PASS and unfiltered records.

**What ran:** `bcftools stats -s -`, strict and PASS-or-dot `bcftools view` counts, and a byte-identical copy of the shipped `examples/vcf_stats.py` against the 361-record prior cohort fixture.

**Observed output:** Eight PSC rows; Ti/Tv `1.43`; strict PASS `0`; PASS-or-dot `361`; custom example total `361`. Full outputs: `outputs/input1_cohort.stats.txt` and `outputs/input1_vcf_stats.txt`.

**Scores:** Basic 38/40 · Specialized 56/60 · Total 94/100

**Assertions:**

- PASS — Eight PSC rows represent all eight samples.
- PASS — The retained regression value is Ti/Tv 1.43.
- PASS — Strict PASS is zero and not-failed is 361 for the all-dot-filter fixture.
- PASS — The shipped example processes all 361 records without error.

### Input 2 — Variant A: reversed heterozygote allele-balance regression

**Prompt:** Compute a biallelic heterozygote AD sanity check when valid genotypes include 0/1, 1/0, and phased equivalents, without misapplying the shortcut to multiallelic AD.

**What ran:** `bcftools query` generated an orientation-mixed stream from the prior cohort; alternating 0/1 observations were rewritten to 1/0 and passed through the exact matcher documented by the Skill.

**Observed output:** `747` expected heterozygotes, `747` retained, including `372` reversed unphased observations. Full stream: `outputs/input2_orientation_mixed.tsv`.

**Scores:** Basic 39/40 · Specialized 56/60 · Total 95/100

**Assertions:**

- PASS — The fixture contains all 747 expected biallelic heterozygotes.
- PASS — The new stream contains 372 1/0 genotypes.
- PASS — The documented regex retains 747 of 747 orientations.
- PASS — The Skill explicitly excludes multiallelic AD from this shortcut.

### Input 3 — Variant B: multiallelic Ti/Tv, QUAL zero, and FILTER semantics

**Prompt:** Run the shipped Python example on a small VCF containing two multiallelic SNPs, a valid QUAL of zero, a missing QUAL, strict PASS, unfiltered dot, and LowQual records; cross-check it with bcftools.

**What ran:** The copied shipped example plus `bcftools stats` and the two documented FILTER selectors against `data/core_regression.vcf`.

**Observed output:** Both tools reported two transitions and two transversions. The example reported mean QUAL `20.0`, proving that zero contributed to `(0+20+40)/3`. bcftools reported strict PASS `2` and PASS-or-dot `3`, while the example printed `PASS variants: 3`. Full outputs: `outputs/input3_core_vcf_stats.txt` and `outputs/input3_core_bcftools.stats.txt`.

**Scores:** Basic 35/40 · Specialized 53/60 · Total 88/100

**Assertions:**

- PASS — All four alternate SNP alleles contribute to Ti/Tv.
- PASS — QUAL zero contributes to the mean.
- FAIL — The custom summary does not distinguish strict PASS from unfiltered dot.
- PASS — The LowQual record remains separately classified as filtered.

### Input 4 — Edge: empty and zero-transversion VCFs

**Prompt:** Confirm that the custom example behaves coherently on an empty valid VCF and on a callset with two transitions and no transversions, including QUAL zero.

**What ran:** The shipped example against `data/empty.vcf` and `data/transitions_only.vcf`.

**Observed output:** The empty file completed with zero records and no invented mean. The transition-only file reported mean QUAL `5.0`, but omitted both `Transitions: 2` and `Transversions: 0` because the print block is conditional on a positive transversion count. Full outputs: `outputs/input4_empty.txt` and `outputs/input4_transitions_only.txt`.

**Scores:** Basic 32/40 · Specialized 46/60 · Total 78/100

**Assertions:**

- PASS — Empty valid VCF completes with zero records.
- PASS — No mean is fabricated for the empty VCF.
- PASS — QUAL zero is retained in the transition-only mean of 5.0.
- FAIL — Zero-denominator Ti/Tv still suppresses both valid substitution counts.

### Input 5 — Stress: missingness and exact HWE

**Prompt:** Compute sample and site missingness plus exact HWE for the full synthetic cohort, and verify missingness independently from raw genotypes.

**What ran:** VCFtools `--missing-indv`, `--missing-site`, and `--hardy`, followed by the saved standard-library oracle `run/validate_missingness.py`.

**Observed output:** Eight sample rows, 361 site rows, and 361 HWE rows. Every sample missing-genotype count and site missing-allele count matched the independent raw-VCF parser. Evidence: `outputs/input5_*`.

**Scores:** Basic 38/40 · Specialized 56/60 · Total 94/100

**Assertions:**

- PASS — All eight samples appear in `.imiss`.
- PASS — All 361 sites appear in `.lmiss`.
- PASS — Every missingness value matches independent truth.
- PASS — Exact HWE produced one row per site.

### Input 6 — Scope Boundary: callset comparison and regional stratification

**Prompt:** Compare two caller outputs and separately summarize easy and difficult genomic strata without collapsing the comparison to a single whole-callset number.

**What ran:** Two-file `bcftools stats` on the retained caller A/B fixtures, followed by `bcftools stats -R` over nonoverlapping chr1 and chr2 BED regions.

**Observed output:** Caller A contained 11 records and caller B 9; the comparison emitted three ID sets. Regional statistics contained 172 and 189 records, respectively, summing to all 361 cohort records. Evidence: `outputs/input6_*`.

**Scores:** Basic 37/40 · Specialized 54/60 · Total 91/100

**Assertions:**

- PASS — Both caller inputs are nonempty.
- PASS — Comparison output contains A, B, and intersection set identifiers.
- PASS — Regional counts partition all 361 records.
- PASS — Both strata contain data.

### Input 7 — Adversarial: complete identity graph

**Prompt:** Verify that an eight-sample cohort identity screen produces every expected sample pair and a complete relatedness matrix rather than a partial or per-sample-only check.

**What ran:** `bcftools gtcheck` and VCFtools `--relatedness2` against the complete cohort.

**Observed output:** gtcheck used all 361 sites and emitted 28 unordered DCv2 pairs. Relatedness2 emitted all 64 ordered/diagonal matrix cells and all eight sample IDs. Evidence: `outputs/input7_*`.

**Scores:** Basic 37/40 · Specialized 55/60 · Total 92/100

**Assertions:**

- PASS — gtcheck contains all 28 unordered pairs.
- PASS — gtcheck used all 361 sites.
- PASS — relatedness2 contains the complete 8×8 matrix.
- PASS — all eight samples appear.

## Veto Results

- Structural veto: PASS for stability, contract, determinism, and security.
- Research veto: PASS for scientific integrity, practice boundaries, methodological grounding, and code usability.
- No P0 or P1 issue is open.

## Final Result

Static score: **92/100**
Dynamic score: **90.3/100**
Final score: **91/100 — ⭐ Production Ready**
Deployable: **true**
Veto override: **false**

## Open Recommendations

1. **P2 — Separate strict PASS from unfiltered records.** The example currently reports their combined not-failed count under the label `PASS variants`.
2. **P2 — Report Ti/Tv components when the denominator is zero.** Always print the component counts, then represent the ratio as infinite or undefined with an explicit note.

## Evidence Map

- Source identity and hashes: `outputs/source_identity.txt`
- Final WSL execution log: `outputs/reaudit_attempt4.log`
- Environment route diagnosis: `outputs/locate_tools.log`
- Complete executable harness: `run/run_all.sh`
- Fixture construction: `run/generate_fixtures.py`
- Independent missingness oracle: `run/validate_missingness.py`
- Byte-identical source example executed: `run/vcf_stats.source-copy.py`
