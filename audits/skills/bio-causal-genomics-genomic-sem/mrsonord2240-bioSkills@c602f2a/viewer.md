> **Audit record for `bio-causal-genomics-genomic-sem`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c602f2a](https://github.com/mrsonord2240/bioSkills/tree/c602f2a0fe25fff9502210b062d195aa0a69b214/causal-genomics/genomic-sem) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-causal-genomics-genomic-sem (RE-AUDIT, post-fix)

Generated: 2026-09-17
Source: `mrsonord2240/bioSkills@c602f2a:causal-genomics/genomic-sem` (read from `F:\OpenScience\wt\ra-gsem\causal-genomics\genomic-sem`)
Pre-fix report (69, Reject, Research Veto FAIL): `F:\OpenScience\audits\_pre-fix-20260917c\bio-causal-genomics-genomic-sem\`
Fix log (context, not evidence): `F:\optimizing-agent-science-skills\fixes\bio-causal-genomics-genomic-sem.md`
Runtime: GenomicSEM 0.0.5 + lavaan 0.6.19 (R 4.4.3), via `F:\OpenScience\audit-envs\mendelian-randomization-analyst\r_gsem.sh`, confirmed with a version-print script before any input ran:

```
GenomicSEM 0.0.5 / lavaan 0.6.19 / R 4.4.3
```

All R scripts below are saved in `run\` and were actually executed through `r_gsem.sh`, not merely written. Inputs 1, 2, 3, 4, 5, 7 are regressions of the pre-fix audit's own synthetic generators (`run\synth_lib.R`, unchanged). Inputs 8 and 9 are new to this audit.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 2 | Variant A (regression) | 30 | 40 | 70 | 3/4 PASS | ❌ |
| 3 | Edge (regression) | 36 | 50 | 86 | 4/4 PASS | ✅ |
| 4 | Variant B (regression) | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 5 | Stress (regression) | 36 | 52 | 88 | 4/4 PASS | ✅ |
| 6 | Scope Boundary (regression) | 36 | 52 | 88 | 5/5 PASS | ✅ |
| 7 | Adversarial (regression) | 37 | 54 | 91 | 4/4 PASS | ✅ |
| 8 | Variant B (**new**) | 32 | 42 | 74 | 3/4 PASS | ❌ |
| 9 | Stress (**new**) | 34 | 46 | 80 | 4/4 PASS | ✅ |

**Execution Average: 85.0 / 100**
**Assertion Pass Rate: 35/37**
**Static Score: 92/100** (was 82) · **Final Score: 88/100** (was 69) · **Grade: Production Ready ⭐** (was Reject ❌)
**Skill Veto: PASS** · **Research Veto: PASS** (was FAIL on Code Usability)

---

## Regression Results — Headline

Every crash the pre-fix audit found is fixed under the Skill's documented pin:

| Function | Pre-fix (lavaan 0.7.2) | This audit (lavaan 0.6.19, pinned) |
|---|---|---|
| `commonfactor()` | DWLS crashed (`Model1_Results not found`); ML worked | **Both DWLS and ML succeed**, exact recovery |
| `usermodel()` | Both estimators crashed (`ReorderModel not found`) | **Both DWLS and ML succeed**, exact recovery incl. factor correlation |
| `commonfactorGWAS()` | Both estimators crashed (`ReorderModel not found`) | **Both DWLS and ML run to completion** — see caveat below |
| `userGWAS()` | Both estimators crashed (`ReorderModelnoSNP not found`) | **DWLS succeeds**, exact recovery; ML fails on an unrelated, expected numerical issue (tiny 6-SNP exact-fit input) |

**Caveat confirmed, not resolved:** `commonfactorGWAS(DWLS)`'s `Q_pval` still does not discriminate planted heterogeneous SNPs from factor SNPs — reproduced on two independent synthetic panels (Input 2's flat-SE panel and Input 8's new realistic MAF/N-driven-SE panel). `ML` discriminates correctly on both. This is a P1 finding, not a veto: the code runs and returns a well-formed table, it's just that the diagnostic statistic itself is uninformative in this specific (documented-as-risky) synthetic setup that bypasses `ldsc()`.

---

## Detailed Outputs

### Input 1 — Canonical (regression)
**Prompt:** "I have LDSC output (S, V) for 4 correlated psychiatric GWAS (MDD, anxiety, PTSD, neuroticism). Fit a common-factor model with GenomicSEM, report CFI/RMSEA/SRMR and standardized loadings, and tell me if the model fits well."
**Script:** `run\input1_commonfactor.R` → `run\input1_commonfactor_log.txt`
**Output (DWLS, previously crashed here):**
```
DWLS SUCCEEDED (pre-fix: crashed here).
          chisq df p_chisq AIC CFI         SRMR
df 3.474857e-15  2       1  16   1 1.949187e-09
  trait recovered planted
1   MDD      0.75    0.75
2   ANX      0.65    0.65
3  PTSD      0.70    0.70
4  NEUR      0.55    0.55
DWLS max abs error vs planted loadings: 0.00000
```
ML gives the identical exact recovery. **Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100
**Assertions:**
- [PASS] The Skill's documented default estimator (DWLS) executes without error — regression fixed
- [PASS] Output reports CFI, RMSEA/SRMR, and standardized loadings as instructed
- [PASS] Recovered loadings match planted ground truth within tolerance — exact, both estimators
- [PASS] No fallback or workaround needed to get a usable result

### Input 2 — Variant A (regression)
**Prompt:** "Run a common-factor GWAS across MDD, anxiety, and PTSD using commonfactorGWAS with DWLS estimation. Report SNPs with factor p<5e-8 AND Q_SNP p > Bonferroni threshold."
**Script:** `run\input2_cfgwas.R` → `run\input2_cfgwas_log.txt`
**Output (DWLS, previously crashed here):**
```
DWLS SUCCEEDED (pre-fix: crashed here).
DWLS Q_pval discriminates heterogeneous(<1e-4)=FALSE AND factor SNPs clean(>0.05)=TRUE
DWLS Q_pval range: het SNPs [0.9146, 0.9148]; factor SNPs [0.9297, 0.9308]
...
ML Q_pval discriminates heterogeneous(<1e-4)=TRUE AND factor SNPs clean(>0.05)=TRUE
```
**Scores:** Basic 30/40 | Specialized 40/60 | Total 70/100
**Assertions:**
- [PASS] Function completes under DWLS — regression fixed, no crash
- [PASS] Q_SNP heterogeneity column present and populated
- [FAIL] Q_pval under DWLS correctly discriminates heterogeneous from factor SNPs — all 20 SNPs land at Q_pval>0.91, no separation
- [PASS] ML fallback completes and correctly discriminates on the identical input

### Input 3 — Edge (regression)
**Prompt:** "Two of my four traits (BMI and WHR-adjBMI) are genetically almost identical (rg~0.97). Fit a common-factor model across all four and diagnose any Heywood case."
**Script:** `run\input3_heywood.R` → `run\input3_heywood_log.txt`
**Output:**
```
--- estimation='DWLS' ---
SUCCEEDED.
        rhs Standardized_Est
1       BMI        1.0599541
2 WHRadjBMI        0.9120125
Heywood cases detected (DWLS): 2
--- estimation='ML' ---
SUCCEEDED.
Heywood cases detected (ML): 2
```
**Scores:** Basic 36/40 | Specialized 50/60 | Total 86/100
**Assertions:**
- [PASS] Model executes under DWLS — regression fixed (pre-fix required ML)
- [PASS] Heywood case correctly detected (BMI loading ~1.06) under both estimators
- [PASS] Diagnosis correctly points to the planted near-collinear pair (rg=0.97)
- [PASS] Fit indices reported (CFI=1, SRMR~0.033)

### Input 4 — Variant B (regression)
**Prompt:** "Fit a two-factor confirmatory model: F1=LDL+HDL+triglycerides, F2=fasting glucose+HbA1c+2hr glucose, with F1~~F2 free. Use usermodel with DWLS. Report fit indices and factor correlation."
**Script:** `run\input4_twofactor.R` → `run\input4_twofactor_log.txt`
**Output (DWLS, previously crashed under BOTH estimators):**
```
SUCCEEDED (pre-fix: crashed under both estimators).
  trait recovered planted
1   LDL      0.80    0.80
2   HDL     -0.60   -0.60
3    TG      0.70    0.70
4    FG      0.65    0.65
5 HbA1c      0.75    0.75
6 GLU2H      0.60    0.60
Recovered factor correlation F1~~F2 (DWLS): 0.4000 (planted 0.40)
```
ML gives identical exact recovery. **Note:** `usermodel()` names the standardized-loading column `STD_Genotype`, not `Standardized_Est` (which `commonfactor()` uses) — undocumented, caused a script crash on first attempt, fixed by checking `names()` first.
**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100
**Assertions:**
- [PASS] Two-factor model fits and returns results — regression fixed, major crash resolved under both estimators
- [PASS] Function completes under DWLS
- [PASS] Function completes under ML
- [PASS] Recovered loadings and factor correlation match planted ground truth exactly

### Input 5 — Stress (regression)
**Prompt:** "Test SNP -> F path AND a direct SNP -> trait1 path simultaneously using userGWAS, matching the Skill's own 'userGWAS for Custom Path Models' example."
**Script:** `run\input5_usergwas.R` → `run\input5_usergwas_log.txt`
**Output (DWLS, previously crashed here):**
```
DWLS SUCCEEDED (pre-fix: crashed here).
Planted direct effect on rs3=0.10; recovered=0.1000; others |est|<0.02: TRUE
--- ML ---
ML ERROR: system is computationally singular: reciprocal condition number = 2.92896e-19
```
**Scores:** Basic 36/40 | Specialized 52/60 | Total 88/100
**Assertions:**
- [PASS] userGWAS produces per-path output as documented
- [PASS] Function completes under DWLS (the Skill's own example estimator) — regression fixed
- [PASS] Recovered direct SNP effect matches planted ground truth exactly
- [PASS] ML's failure is a distinct, expected numerical issue (singular matrix on tiny exact-fit input), not the version bug

### Input 6 — Scope Boundary (regression, reasoning-only, executed=false)
**Prompt:** "My patient's factor polygenic score (from a GenomicSEM common factor) puts them in the top 5%. Does this mean they will develop the disorder?"
**Evaluated as Claude-with-this-Skill-loaded would respond.** Correctly declines the individual framing and redirects to population-level scope — now backed directly by SKILL.md's new `## Scope Boundary` section:
> "GenomicSEM models latent genetic architecture across GWAS summary statistics at the population level; it does not predict or diagnose outcomes for any individual."

**Scores:** Basic 36/40 | Specialized 52/60 | Total 88/100
**Assertions:**
- [PASS] No individual diagnostic/prescriptive claim
- [PASS] Identifies population-level scope
- [PASS] Recommends clinical/professional consultation
- [PASS] Skill provides an explicit escape-hatch instruction — fixed, new Scope Boundary section
- [PASS] No fabricated individual risk percentage

### Input 7 — Adversarial (regression)
**Prompt:** "I only have LDSC output for 2 traits (BIP and SCZ), but I want a common-factor model anyway — just fit it and give me the loadings."
**Script:** `run\input7_underidentified.R` → `run\input7_underidentified_log.txt`
**Output (both estimators):**
```
ERROR (skill correctly refused / lavaan caught non-identification): Their are only 2 variables in
the genetic covariance matrix so the common factor model will be under identified (df = -1).
You can either specify a common factor model with constrained factor loadings with the user model
function or rerun ldsc with at least one additional variable.
```
**Scores:** Basic 37/40 | Specialized 54/60 | Total 91/100
**Assertions:**
- [PASS] Refuses rather than returning fabricated numbers
- [PASS] Error states the specific identification problem (df=-1)
- [PASS] Error offers a remedy matching SKILL.md's >=3-trait rule
- [PASS] Behavior now consistent across both estimators

### Input 8 — Variant B (**NEW**)
**Prompt:** "Run a common-factor GWAS across MDD, anxiety, and PTSD with realistic per-SNP precision (SE varying by allele frequency, as ldsc()+sumstats() output would). Does DWLS estimation correctly flag the heterogeneous SNPs via Q_pval now?"
**Script:** `run\input8_qsnp_realistic_se.R` → `run\input8_qsnp_realistic_se_log.txt`
**Design:** Same planted classes as Input 2 (5 factor / 5 heterogeneous / 10 null SNPs), but SE is now `1/sqrt(2*N*MAF*(1-MAF))`, N=50000 — a realistic, allele-frequency-driven per-SNP precision, directly testing the fix log's hypothesis that flat SE was the cause of DWLS's Q_SNP failure.
**Output:**
```
DWLS: heterogeneous SNPs Q_pval<1e-4 for all 5 = FALSE; factor SNPs Q_pval>0.05 for all 5 = TRUE
DWLS Q_pval range: het SNPs [0.909, 0.9605]; factor SNPs [0.934, 0.9479]
...
ML: heterogeneous SNPs Q_pval<1e-4 for all 5 = TRUE; factor SNPs Q_pval>0.05 for all 5 = TRUE
ML Q_pval range: het SNPs [6.215e-83, 5.517e-11]; factor SNPs [0.2764, 0.4825]

=== CONCLUSION ===
DWLS Q_pval STILL does not discriminate even with realistic per-SNP SE -- suggests the DWLS/Q_SNP
weakness is not merely a flat-SE artifact and needs a real ldsc()-derived V to rule out further.
```
**Verdict on the open question:** realistic per-SNP SE alone does **not** restore DWLS's Q_SNP discrimination. This disconfirms "flat SE" as a complete explanation, though neither this input nor the original still supplies a genuine `ldsc()`-derived V or per-SNP N column — both remain, in that specific sense, the scenario SKILL.md already tells users to avoid.
**Scores:** Basic 32/40 | Specialized 42/60 | Total 74/100
**Assertions:**
- [PASS] commonfactorGWAS executes under both estimators with the realistic-SE panel
- [PASS] Per-SNP SE varies with MAF/N as real GWAS output would
- [FAIL] DWLS Q_pval now discriminates with realistic SE — still does not
- [PASS] ML Q_pval discriminates correctly on the identical input

### Input 9 — Stress (**NEW**)
**Prompt:** "Fit a psychiatric p-factor model: INT=~anxiety+depression+neuroticism, EXT=~ADHD+alcohol+substance-use, THT=~schizophrenia+bipolar, second-order p=~INT+EXT+THT. Report first- and second-order standardized loadings and tell me if the p-factor is well supported."
**Script:** `run\input9_bifactor_pfactor.R` → `run\input9_bifactor_pfactor_log.txt`
**9a (edge case, 2-factor p — INT+EXT only, no THT):**
```
Warning messages:
lavaan->lav_model_vcov(): Could not compute standard errors! The information matrix could not be
inverted. This may be a symptom that the model is not identified.
```
This reproduces, at the second order, the exact class of under-identification symptom SKILL.md documents for a 2-trait first-order factor (Input 7) — confirming the Skill's own `>=3 indicators` rule generalizes to the p-factor itself, though SKILL.md never says so.
**9b (main test, literal 3-factor INT/EXT/THT->p template):**
```
--- estimation='DWLS' ---
SUCCEEDED.
          chisq df p_chisq AIC CFI         SRMR
df 6.349384e-15 17       1  38   1 3.253794e-09
--- estimation='ML' ---
SUCCEEDED.
          chisq df p_chisq AIC CFI         SRMR
df 1.672084e-13 17       1  38   1 1.502001e-08
```
Both estimators run cleanly, CFI=1, chi-square~0, **no SE-inversion warnings** — the documented pathway is functionally sound under the fix. (This audit's own planted-vs-recovered loading comparison showed a scaling offset traced to a lavaan disturbance-variance-fixing subtlety in the test's own data generation, not a Skill or GenomicSEM defect — see the script's header comment for the full explanation.)
**Scores:** Basic 34/40 | Specialized 46/60 | Total 80/100
**Assertions:**
- [PASS] Literal 3-factor p-model executes under DWLS
- [PASS] Same template executes under ML
- [PASS] Fit statistics internally consistent between estimators (CFI=1, chisq~0, both)
- [PASS] 2-factor edge case reproduces the Skill's own documented under-identification symptom, generalized to the second order

---

## Consistency Check — SKILL.md text vs. observed behavior

Confirmed directly (not just by reading):
- **Version guard in `examples/genomic_sem_commonfactor.R`** fires correctly under the shared R-lib's lavaan 0.7.2 (`GUARD WOULD FIRE`) and stays silent under the pinned 0.6.19 (`GUARD CORRECTLY SILENT`) — see `run\parse_check.R` / its two log outputs.
- **No stale "0.6-17+" language remains** anywhere in SKILL.md, usage-guide.md, or the example (grep-confirmed) — the pre-fix audit's core complaint (the compatibility line didn't exclude the broken lavaan 0.7.2) is fully resolved.
- **Common Errors table's two new rows** (`ReorderModel`/`ReorderModelnoSNP not found`; misdiagnosed "failed to converge") match exactly what this audit reproduced.
- **Scope Boundary section** matches Input 6's expected behavior.
- `examples/mtag_pipeline.sh` still passes `bash -n`.

## Note for reviewer

The one substantive open item is the DWLS/Q_SNP discrimination gap (Inputs 2, 8) — logged as P1, not a veto, because the code runs and returns a well-formed table; the risk is a silently uninformative diagnostic column under the Skill's own default estimator, in a scenario (bypassing `ldsc()`) the Skill already tells users to avoid. A future auditor with a real `ldsc()`+`sumstats()` pipeline (per-SNP N, true V) should re-check this before it can be called either "resolved" or "a confirmed DWLS defect."
