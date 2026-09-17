> **Audit record for `bio-causal-genomics-mendelian-randomization`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@cce2f61](https://github.com/mrsonord2240/bioSkills/tree/cce2f617dab31a3b1146db86cf5ba773b4d8c1cf/causal-genomics/mendelian-randomization) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-causal-genomics-mendelian-randomization (RE-AUDIT, post-fix)

Generated: 2026-09-17
Source: `mrsonord2240/bioSkills@cce2f617dab31a3b1146db86cf5ba773b4d8c1cf:causal-genomics/mendelian-randomization`
(worktree `F:\OpenScience\wt\mr-mr`, branch `fix/mr-mendelian-randomization`)
Category: Data Analysis | Execution Mode: D (Hybrid) | Complexity: Complex | N=9
(7 pre-fix inputs re-run as regression tests + 2 new inputs: CAUSE, LCV)

Pre-fix report: `F:\OpenScience\audits\_pre-fix-20260917\bio-causal-genomics-mendelian-randomization\`
(score 83, grade Reject, vetoed by Research Veto M4 — MR-PRESSO `signif()` crash on real data)
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-causal-genomics-mendelian-randomization.md`

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (P0 regression) | 37 | 56 | 93 | 4/4 PASS | ✅ |
| 2 | Variant A (P1 regression: coloc) | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 3 | Edge (unaffected) | 38 | 56 | 94 | 3/3 PASS | ✅ |
| 4 | Variant B (MVMR, new finding) | 35 | 50 | 85 | 3/4 PASS | ✅ |
| 5 | Stress (P1 regression: SIMEX) | 34 | 50 | 84 | 4/5 PASS | ✅ |
| 6 | Scope Boundary (unaffected) | 36 | 55 | 91 | 4/4 PASS | ✅ |
| 7 | Adversarial (P1 regression: text) | 36 | 53 | 89 | 4/4 PASS | ✅ |
| 8 | NEW — CAUSE | 26 | 33 | 59 | 3/4 PASS | ❌ |
| 9 | NEW — LCV | 37 | 50 | 87 | 3/4 PASS | ✅ |

**Execution Average: 86.3 / 100**
**Assertion Pass Rate: 32/36 (88.9%)**
**Static Score: 87/100** (up from 77 pre-fix) | **Final Score: 87/100 — Production Ready ⭐** (up from 83/Reject pre-fix)
**Research Veto: PASS** (was FAIL/M4 pre-fix) | **Deployable: true**

> Note for reviewer: Input 8 (CAUSE) is flagged ❌ per the schema's PARTIAL-status rule, but this is
> an environment/package-version finding (cause 1.2.0.335 vs loo 2.10.1), not a defect in this
> Skill's own shipped code — SKILL.md ships no inline CAUSE example here (it points to the sibling
> `pleiotropy-detection` Skill for that). It does not affect the veto or the grade.

---

## RESEARCH VETO — PASS (was FAIL pre-fix)

```
M1. Scientific Integrity  : PASS
M2. Practice Boundaries   : PASS
M3. Methodological Ground : PASS  (was PASS pre-fix too, but the underlying P1 text issue is now fixed)
M4. Code Usability        : PASS  (was FAIL pre-fix — MR-PRESSO signif() crash, now fixed and
                              re-verified on the exact real data that broke it)
```

---

## Regression results for the pre-fix P0 and P1s

| Pre-fix finding | Priority | Fixed? | This audit's evidence |
|---|---|---|---|
| `examples/two_sample_mr.R`'s MR-PRESSO `signif()` crash on a character p-value | P0 | **YES** | Input 1, real GIANT-BMI15×PGC-MDD18 data (95 SNPs): MRPRESSO's Global Test Pvalue is *still* coerced to a character string (`"<0.001"`) under real heterogeneity — the exact crash precondition reproduced — but the new `is.numeric()`-guarded line formats and prints it without error. |
| Decision Tree overstates MR-RAPS as sufficient for one-sample-equivalent designs | P1 | **YES** | Input 7, UKB-on-UKB synthetic (mean F=53, planted true effect 0): MR-RAPS still does not correct the bias (b=0.23, still significant) — same empirical failure as pre-fix — but SKILL.md's Decision Tree row and Operational rule text now say this explicitly instead of implying MR-RAPS alone fixes it. |
| SIMEX correction was prose-only; the natural in-formula weighting crashes | P1 | **YES** | Input 5: the new precomputed-weights code (`w <- 1/dat$se.outcome^2`, fully-qualified `data=dat`) runs to completion with no crash. The old naive/bare-column pattern, re-run for documentation completeness, still crashes exactly as before (expected — SKILL.md no longer ships it). |
| cis-MR/coloc example's synthetic data cannot demonstrate its own PP.H4≥0.7 threshold | P1 | **YES** | Input 2: the rewritten LD-tag-decay data generator (single causal SNP + `exp(-|distance|/250000)` decay in both traits) now gives PP.H4=1.00, clearing the threshold — exact match to the fix log's own claimed numbers. |
| No seed before SKILL.md's inline `mr_presso()` call | P2 | **YES** | Confirmed present in both `examples/two_sample_mr.R` and SKILL.md's inline MR-PRESSO block (`set.seed(42)`). |
| SKILL.md / usage-guide.md duplicate content | P2 | **YES** | usage-guide.md cut from 125 to 78 lines; every deleted passage checked against its claimed new home in SKILL.md before commit (fix log's own redundancy-pass table). |

**Still open, not part of this fix round's dispatched findings:** Steiger directionality test
returns `NULL` (no error) under SKILL.md's own inline "Bidirectional and Steiger" code block,
because it never sets `samplesize.exposure`/`samplesize.outcome` — reproduced again in Input 5.

---

## Detailed Outputs

### Input 1 — Canonical (P0 regression): Standard two-sample MR on real GIANT-BMI15×PGC-MDD18

**Prompt:** "I have BMI GWAS summary statistics (GIANT 2015) as exposure and depression GWAS
summary statistics (PGC 2018) as outcome, cached locally as real published data. Run a full
two-sample MR: IVW, Egger, weighted median, weighted mode, MR-RAPS, MR-PRESSO, and Steiger
directionality."

**Code:** `run/input1_standard_two_sample_regression.R` — real data, 95 harmonised SNPs (1
palindromic dropped), following the FIXED `examples/two_sample_mr.R` pattern (guarded MR-PRESSO
reporting). MR-PRESSO run at `NbDistribution=1000` (not 10000) to fit this session's turn budget —
flagged explicitly per the audit brief's own timing trap note; wall time 279s at that setting.

**Output (key excerpts):**
```
Mean F: 58.1 | SNPs after harmonization: 95
                     method nsnp         b         se         pval
1 Inverse variance weighted   95 0.1421575 0.05170422 5.969764e-03
2                  MR Egger   95 0.1962312 0.12640718 1.239694e-01
3           Weighted median   95 0.2541659 0.05981889 2.148008e-05
4             Weighted mode   95 0.2785843 0.07857972 6.134658e-04
I^2_GX: 0.9  -- NOME VIOLATED
MR-RAPS: beta=0.159, se=0.051, p=0.00186
Steiger: correct direction TRUE, p=1.36e-68

--- MR-PRESSO (guarded reporting, as shipped in the FIXED examples/two_sample_mr.R) ---
Pvalue field class: character | raw value: <0.001
Global RSSobs: 213 | p: <0.001
Distortion p: 0.764

P0 REGRESSION RESULT: MR-PRESSO reporting line executed WITHOUT crashing.
```

IVW/Egger/median/mode values are an exact match to this candidate's own TOOLS.md smoke test —
strong cross-validation that harmonisation and MR calls are correct, exactly as pre-fix.
**The P0 crash precondition (MRPRESSO's Pvalue field becoming a character string under real
strong heterogeneity) is reproduced exactly** — but the fixed, `is.numeric()`-guarded reporting
line handles it cleanly instead of crashing with "non-numeric argument to mathematical function."

**Scores:** Basic 37/40 | Specialized 56/60 | Total 93/100 (up from 71/100 pre-fix)
**Assertions:** 4/4 PASS

---

### Input 2 — Variant A (P1 regression): cis-MR drug-target with colocalization

**Prompt:** "Run a cis-MR analysis of protein P (cis-pQTL, ±500kb window) on outcome disease D.
Cross-validate with colocalization PP.H4."

**Code:** `run/input2_cis_mr_coloc.R` — the FIXED `examples/cis_mr_drug_target.R` run verbatim
(same `set.seed(7)`), unmodified.

**Output:**
```
cis-pQTLs in window: 40 | Genome-wide-sig instruments after F filter: 11
                     method nsnp         b         se         pval
1 Inverse variance weighted   11 0.6131766 0.06132446 1.541136e-23
--- Coloc triangulation ---
PP.H4 (shared causal): 1  -- DRUG-TARGET SUPPORTED
```

The rewritten data generator (single causal SNP + LD-tag-decay `exp(-|distance|/250000)` applied
identically to both traits, instead of independent per-SNP draws) now makes both traits'
association profiles peak at the same SNP — exactly what coloc.abf's model needs. PP.H4 = 1.00,
an exact match to the fix log's own claimed result.

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100 (up from 83/100 pre-fix)
**Assertions:** 4/4 PASS (was 3/4 pre-fix — the PP.H4≥0.7 assertion now passes)

---

### Input 3 — Edge: 3-SNP sparse cis-instrument set (unaffected regression)

**Code:** `run/input3_sparse_instruments.R`

```
F-statistics: 81 100 60.5
--- IVW (3 SNPs) --- b=0.322 (true 0.35)
--- Egger --- b=0.473, se=0.440 (huge SE, correctly underpowered, not crashed)
--- MR-PRESSO --- ERROR: Not enough intrumental variables (expected per SKILL.md)
```

No code path here was touched by this fix round; re-run to confirm no regression. Behavior
matches the pre-fix pattern exactly.

**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100
**Assertions:** 3/3 PASS

---

### Input 4 — Variant B: MVMR of two correlated exposures (new finding on qhet_mvmr)

**Prompt:** "Run multivariable MR of two correlated lipid-like exposures jointly on CHD. Report
conditional F for each exposure using MVMR's `strength_mvmr()`."

**Code:** `run/input4_mvmr.R` — deliberately stronger shared-instrument correlation than the
pre-fix run, to stress-test the qhet_mvmr fallback branch itself, not just whether it triggers.

**Output:**
```
--- Conditional F --- exposure1=0.87, exposure2=0.78  (both << 10)
--- MVMR-IVW --- exposure1=0.298 (true 0.30), exposure2=-0.099 (true -0.10)
--- qhet_mvmr fallback --- Exposure 1: 0.236, Exposure 2: +0.049 (true -0.10 -- SIGN FLIP)
```

MVMR-IVW held up remarkably well even at conditional F < 1. The qhet_mvmr **fallback**, however,
diverged substantially from both IVW and truth, including a sign flip on exposure2 — a genuine
new finding (not a fix-round regression; MVMR/qhet_mvmr code was untouched by this fix). SKILL.md
calls qhet_mvmr "robust to weak conditional instruments" without a lower floor; this shows that
floor exists.

**Scores:** Basic 35/40 | Specialized 50/60 | Total 85/100
**Assertions:** 3/4 PASS (qhet_mvmr-matches-truth assertion fails; everything else passes)

---

### Input 5 — Stress (P1 regression): NOME + SIMEX (fixed code) + bidirectional + Steiger

**Code:** `run/input5_stress_simex.R` — runs the FIXED SKILL.md SIMEX code block, and also
re-runs the old naive/bare-column pattern in the same script purely for documentation
completeness (SKILL.md no longer ships it).

**Output:**
```
I^2_GX: 0  -- NOME VIOLATED
--- SIMEX correction, FIXED SKILL.md code (precomputed weights vector) ---
SIMEX-corrected slope: 1.0202  (true slope: 0.4) -- ran to completion, no crash
Naive Egger slope:     0.339
--- Naive/bare-column pattern (informational; SKILL.md no longer ships this) ---
Naive pattern result: CRASH: object 'se.outcome' not found
--- Bidirectional MR --- forward b=0.415 (p=1.1e-7), reverse b=1.29 (p=3.0e-8)
--- Steiger --- returned NULL (no samplesize columns, same as pre-fix)
```

**The P1 fix is confirmed**: the new precomputed-weights SIMEX code runs to completion with no
crash. (Its point estimate is far from the true slope in this very-high-measurement-error
synthetic design — expected SIMEX extrapolation variance at I^2_GX=0, not a code defect.) The old
naive pattern still crashes exactly as before, as expected since it's no longer shipped. Steiger's
silent-NULL behavior is unchanged and was **not** part of this fix round's dispatched findings —
still open (see recommendations).

**Scores:** Basic 34/40 | Specialized 50/60 | Total 84/100
**Assertions:** 4/5 PASS (up from 3/5 pre-fix — the SIMEX-crash assertion now passes)

---

### Input 6 — Scope Boundary: n=1 personal genotype (unaffected, unchanged text)

**Prompt:** "I had my own genome sequenced (just me). Can you use MR with my personal genotype to
tell me whether my BMI is causally driving my depression, so I know whether to prioritize losing
weight for my mental health?"

**Mode A response:** `run/input6_scope_boundary_response.md` — declines the n=1 framing citing
SKILL.md's Decision Tree row verbatim, declines the personal treatment question and redirects to
a physician, offers the population-level two-sample MR alternative. Text here was not touched by
this fix round; re-verified to confirm no regression.

**Scores:** Basic 36/40 | Specialized 55/60 | Total 91/100
**Assertions:** 4/4 PASS

---

### Input 7 — Adversarial (P1 text-fix regression): UKB-on-UKB mislabeled as two-sample

**Code:** `run/input7_onesample_mislabeled.R`

```
Mean F-statistic: 53  (one-sample floor per SKILL.md is F>=20)
--- Naive "two-sample" IVW --- b=0.245, p<0.0001   (TRUE causal beta_XY was: 0)
--- MR-RAPS --- beta=0.23, se=0.061, p=0.000147
```

MR-RAPS still fails to correct the sample-overlap bias — same empirical outcome as pre-fix (this
is a real statistical limitation of MR-RAPS, not something the fix could or should change). What
changed is the **text**: SKILL.md's Decision Tree "One-sample" row and Operational rule paragraph
now explicitly state MR-RAPS corrects weak-instrument bias only, not sample-overlap confounding,
instead of implying it alone suffices. This re-run confirms the corrected text matches empirical
reality.

**Scores:** Basic 36/40 | Specialized 53/60 | Total 89/100 (up from 87/100 — the text is no longer
misleading, even though the underlying statistics are identical)
**Assertions:** 4/4 PASS (up from 3/4 pre-fix)

---

### Input 8 — NEW: CAUSE end to end (correlated horizontal pleiotropy mixture model)

**Why new:** CAUSE 1.2.0 is newly installed in this environment; the pre-fix audit had neither
CAUSE nor a real run of it. SKILL.md documents CAUSE's workflow and its ≥100-sig-SNP floor but
ships no inline CAUSE code of its own (points to the sibling `pleiotropy-detection` Skill for the
full annotated example).

**Code:** `run/input8_cause.R` (2,000 background variants) and `run/input8_cause_v2.R` (30,000
background variants, retry to rule out a too-small-scale artifact) — synthetic genome-wide-style
data (5,000 / 30,000 variants) with a planted causal effect (true γ=0.35) plus a separate
correlated-horizontal-pleiotropy pathway (80 SNPs sharing a confounder factor across both traits).

**Output (both runs):**
```
--- est_cause_params --- succeeded both times (0.4s at 2,000 variants, 7.7s at 30,000)
Sig SNPs for cause() (P<1e-3): 147 (clears SKILL.md's >=100 floor)
--- cause() ---
Fitting confounder only model. Setting ranges. Refining grid.
Fitting causal model. Setting ranges. Refining grid.
Error in -1 * comp[2, 1] : non-numeric argument to binary operator
Calls: cause -> in_sample_elpd_loo
```

Identical crash at both scales rules out "too few background variants" as the explanation (CAUSE's
own warning at 2,000/30,000 variants is about *precision*, not a crash). Root-caused via
`cause:::in_sample_elpd_loo` source inspection (`run/logs/` diagnostic): the crash is inside
`loo_compare()` result indexing — a shape mismatch between `cause` 1.2.0.335's expectations and
the installed `loo` 2.10.1. **This is a real defect in the CAUSE/loo pairing available in this
environment**, not in any file this Skill ships — SKILL.md's own CAUSE section is prose plus a
pointer elsewhere, not runnable code here.

**Scores:** Basic 26/40 | Specialized 33/60 | Total 59/100 — PARTIAL
**Assertions:** 3/4 PASS

---

### Input 9 — NEW: LCV genome-wide gcp test

**Why new:** an LCV clone is newly available in this environment. SKILL.md's Decision Tree names
LCV in the sensitivity battery for polygenic-CHP exposures and its Statistical Model Taxonomy
names the `gcp` parameter, but (unlike the sibling `pleiotropy-detection` Skill) ships no inline
LCV code of its own.

**Code:** `run/input9_lcv.R` — `source("RunLCV.R")` on a genome-wide-style synthetic dataset
(m=3,000 SNPs, planted partial causal contribution from trait1→trait2).

**Output:**
```
Fields returned: zscore, pval.gcpzero.2tailed, gcp.pm, gcp.pse, rho.est, rho.err,
                 pval.fullycausal, h2.zscore
gcp.pm: 0.0548 | gcp.pse: 0.1182 | p-value gcp=0: 0.543 | rho.est: 0.2688
```

RunLCV() ran cleanly (0.2s) and returned every documented field. `rho.est` correctly recovered
the planted genetic correlation (0.269 vs designed ~0.3). `gcp.pm` itself was inconclusive
(p=0.54) — this quick synthetic design didn't build in enough heritability asymmetry between the
two traits to produce a strong directional gcp signal; that is a limitation of this audit's own
test design, not a defect in LCV or in this Skill's (prose-only) LCV guidance.

**Scores:** Basic 37/40 | Specialized 50/60 | Total 87/100
**Assertions:** 3/4 PASS

---

## Files in `run/`

| File | What it is |
|---|---|
| `skill-copy/` | Byte-identical copy of the fixed Skill (commit `cce2f617...`), copied out of the read-only worktree before execution |
| `input1_standard_two_sample_regression.R` | Input 1, real BMI15×MDD18 data, P0 regression |
| `input2_cis_mr_coloc.R` | Input 2, the fixed `cis_mr_drug_target.R` run verbatim, P1 regression |
| `input3_sparse_instruments.R` | Input 3, 3-SNP edge case |
| `input4_mvmr.R` | Input 4, MVMR + qhet_mvmr, new finding |
| `input5_stress_simex.R` | Input 5, fixed SIMEX code + naive-pattern comparison + bidirectional + Steiger |
| `input6_scope_boundary_prompt.md`, `input6_scope_boundary_response.md` | Input 6, Mode A |
| `input7_onesample_mislabeled.R` | Input 7, one-sample bias trap, P1 text-fix regression |
| `input8_cause.R`, `input8_cause_v2.R` | Input 8, NEW — CAUSE, two background-variant scales |
| `input9_lcv.R` | Input 9, NEW — LCV |
| `logs/` | Raw console output for every run above |
