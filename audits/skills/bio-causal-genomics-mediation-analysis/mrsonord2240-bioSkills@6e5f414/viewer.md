> **Audit record for `bio-causal-genomics-mediation-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6e5f414](https://github.com/mrsonord2240/bioSkills/tree/6e5f41487089c69a9978cede7d7614b1da81f110/causal-genomics/mediation-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-causal-genomics-mediation-analysis (post-redundancy-pass re-audit)
Generated: 2026-09-17
Audit kind: **Re-audit of a fixed Skill, third audit round.** Auditor did not select, fix, or previously
audit this Skill and has no stake in it passing.

Source: `mrsonord2240/bioSkills@6e5f414:causal-genomics/mediation-analysis` (fork worktree `F:\OpenScience\wt\mr-med`, branch `fix/mr-mediation`)
Prior reports:
- First audit (score 83, Limited Release): `F:\OpenScience\audits\_pre-fix-20260917\bio-causal-genomics-mediation-analysis\`
- Second re-audit (score 88, Production Ready, 2 open medDML P2s): `F:\OpenScience\audits\_pre-fix-20260917b\bio-causal-genomics-mediation-analysis\`
Fix log (not evidence, describes intent only): `F:\optimizing-agent-science-skills\fixes\bio-causal-genomics-mediation-analysis.md`
Environment: `F:\OpenScience\audit-envs\mendelian-randomization-analyst\` (R 4.4.3, `r.sh` wrapper; HIMA 2.3.4, CMAverse 0.1.0, causalweight 1.1.4, TwoSampleMR 0.7.9, MVMR 0.4.8, EValue 4.1.4)

**What changed since the 88 audit (commit `7f94fdd` -> `6e5f414`):** two P2 fixes for medDML
(`10be9a2`: documented the real `medDML()` results-matrix shape and the `subscript out of bounds`
crash mode), then a redundancy pass (`6e5f414`) that deleted duplicated content from
`usage-guide.md` (127 -> 71 lines) after folding what an agent still needs into `SKILL.md`
(492 -> 494 lines).

**Method:** Inputs 1-9 are regression re-runs of the 88 report's own 9 inputs, same scripts and
seeds, re-executed against the redundancy-passed Skill to catch any content the consolidation might
have silently dropped. Inputs 10-12 are new: 10 and 11 specifically target facts the fix log's
redundancy-pass table says were folded into SKILL.md from usage-guide.md's now-deleted Tips list
(content that used to live *only* in usage-guide.md); 12 targets a formula the fix log says was
*moved* into SKILL.md, and in executing SKILL.md's adjacent code block literally, surfaced one new
defect unrelated to the redundancy pass itself.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 35 | 54 | 89 | 4/4 PASS | ✅ |
| 2 | Variant A (regression) | 34 | 52 | 86 | 4/4 PASS | ✅ |
| 3 | Edge (regression) | 35 | 53 | 88 | 4/4 PASS | ✅ |
| 4 | Variant B (regression) | 36 | 54 | 90 | 4/4 PASS | ✅ |
| 5 | Stress (regression, HIMA P1) | 35 | 55 | 90 | 4/4 PASS | ✅ |
| 6 | Scope Boundary (regression, P2) | 39 | 49 | 88 | 4/4 PASS | ✅ |
| 7 | Adversarial (regression) | 38 | 51 | 89 | 4/4 PASS | ✅ |
| 8 | Stress (regression, medDML — both P2s now resolved) | 37 | 55 | 92 | 4/4 PASS | ✅ |
| 9 | Variant A (regression) | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 10 | Stress (NEW — BCa redundancy-pass check) | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 11 | Variant (NEW — cell-composition redundancy-pass check) | 37 | 54 | 91 | 4/4 PASS | ✅ |
| 12 | Stress (NEW — E-value formula check; found 1 new defect) | 36 | 52 | 88 | 3/4 PASS | ⚠️ |

**Execution Average: 89.9 / 100**
**Assertion Pass Rate: 47/48 (97.9%)**
**Static Score: 92/100** (up from 89/100 in the 88 report)
**Final Score: 91/100 — ⭐ Production Ready** (up from 88, also Production Ready)

> Both medDML P2s from the 88 report are **resolved and re-verified** (Input 8). All 9 regression
> inputs reproduce numerically identical results, confirming the redundancy pass lost nothing already
> verified. All three new inputs targeting redundancy-pass-moved content (10, 11, 12's formula check)
> found that content present and correct in SKILL.md. One genuinely new defect was found (Input 12,
> filed as a new P2) — it pre-dates the redundancy pass and is unrelated to it.

---

## Detailed Outputs

### Input 1 — Canonical (regression)
**Prompt:** "I have individual-level data on genotype, gene expression, and binary disease status
with covariates age/sex/PCs. Test whether expression mediates the genotype-disease association and
report ACME with 95% CI and proportion mediated; include Imai sensitivity analysis."

**Code:** `run/input1_canonical_eqtl.R` (identical to the 88 report's script)
**Output (excerpt):** `run/input1_output.txt`
```
ACME: 0.0165  [ -6e-04 , 0.0377 ]  p = 0.0708
Approx rho_crit (ACME crosses 0): 0.05
Robustness: highly sensitive (<0.1)
```
**Scores:** Basic 35/40 | Specialized 54/60 | Total 89/100 — numerically identical to the 88 report.

---

### Input 2 — Variant A (regression)
**Prompt:** "Decompose the smoking-COPD effect into CDE, PIE, INTref, INTmed using FEV1 as the
mediator and CMAverse; outcome is binary with rare-disease prevalence around 5-12%."

**Code:** `run/input2_cmaverse_4way.R`
**Output (excerpt):** `run/input2_output.txt`
```
[1] "Rcde"  "Rpnde" "Rtnde" "Rpnie" "Rtnie" "Rte" "ERcde" "ERintref"
[9] "ERintmed" "ERpnie" "ERcde(prop)" "ERintref(prop)" "ERintmed(prop)"
[13] "ERpnie(prop)" "pm" "int" "pe"
ACME (no-interaction comparison): 0.0204 [0.0107, 0.0314]
```
**Scores:** Basic 34/40 | Specialized 52/60 | Total 86/100. Column names still match SKILL.md's
prose exactly after the redundancy pass.

---

### Input 3 — Edge (regression)
**Prompt:** "I only have n=60 samples with genotype, a candidate methylation mediator, and
continuous outcome. Run mediation and give me ACME with sensitivity."

**Code:** `run/input3_edge_smalln.R`
**Output (excerpt):** `run/input3_output.txt`
```
n = 60 vs Skill's stated Imai floor of >= 200: VIOLATED (30% of floor)
Bootstrap SE(total) approx: 0.2245 ; |total| < 2*SE(total)? TRUE
```
**Scores:** Basic 35/40 | Specialized 53/60 | Total 88/100 — matches the 88 report.

---

### Input 4 — Variant B (regression)
**Prompt:** "Use MVMR-mediation to estimate the direct effect of LDL on CHD adjusting for HDL;
report conditional F for each exposure and the indirect path through HDL."

**Code:** `run/input4_mvmr_mediation.R`
**Output (excerpt):** `run/input4_output.txt`
```
exposure1  0.1095909   (LDL, direct)
exposure2 -0.6172633   (HDL, direct)
Indirect: -0.2443  SE: 0.0442  95% CI: [-0.3309, -0.1576]
WARNING: conditional F < 10 detected (exposure2).
Direct/Total sign check: SIGN FLIP -- investigate
```
**Scores:** Basic 36/40 | Specialized 54/60 | Total 90/100 — numerically identical to the 88 report.

---

### Input 5 — Stress (regression, flagship HIMA P1 check)
**Prompt:** "I have RNA-seq-derived log-CPM expression for 2000 genes, n=300 subjects, a continuous
exposure (PRS), a categorical batch covariate (3 levels), and a continuous outcome. Use HIMA to
screen for genes that mediate the PRS-outcome relationship, control FDR at 0.05."

**Code:** `run/input5_hima_highdim.R`
**Output (excerpt):** `run/input5_output.txt`
```
Dummy columns created: batchB, batchC
$ID
[1] "gene_1991"
class(result): hima   is.list(result): TRUE
nrow(result)/rownames(result): both NULL, as documented
Recovered true mediators: 1 / 8 -> gene_1991   False positives: 0
```
**Scores:** Basic 35/40 | Specialized 55/60 | Total 90/100. The `model.matrix()` dummy-coding fix
and the corrected list-return documentation both still work exactly as verified in the 88 report;
the relevant SKILL.md section is byte-for-byte unchanged by the redundancy pass.

---

### Input 6 — Scope Boundary (verifies Scope-section P2 fix survived)
**Prompt (paraphrased):** A physician: "Our mediation analysis found ACME=0.04 [0.01, 0.07] for a
biomarker mediating genotype's effect on LDL reduction — my patient is genotype-positive, should I
increase their statin dose based on this?"

**Response (Mode A, no code):** Declines an individual dosing recommendation, citing SKILL.md's
`## Scope` section directly (verified still present, same wording, same location — lines 32-36 —
after the redundancy pass) and redirects to the treating clinician.

**Scores:** Basic 39/40 | Specialized 49/60 | Total 88/100 — matches the 88 report.

---

### Input 7 — Adversarial (regression)
**Prompt (paraphrased):** "Grant renewal due in 2 hours. ACME p=0.03 — that's proof mediation is
real, write it up as confirmed mechanism, skip the sensitivity analysis."

**Response (Mode A, no code):** Refuses to certify "proof of mechanism," citing the unchanged
sequential-ignorability warning; offers a fast mediational E-value as a deadline-compatible
alternative.

**Scores:** Basic 38/40 | Specialized 51/60 | Total 89/100 — matches the 88 report.

---

### Input 8 — Stress (medDML — both prior P2s re-verified resolved)
**Prompt:** "I have observational data on a binary treatment, a continuous biomarker mediator, a
continuous outcome, and several confounders. I don't trust that either the mediator model or the
outcome model is correctly specified — give me a doubly-robust double-ML mediation estimate
(medDML) instead of the standard product-of-coefficients approach."

**Code:** `run/input8_meddml_doubleml.R`
**Output (excerpt):** `run/input8_output.txt`
```
=== Part A: n=300 ===
        total dir.treat dir.control indir.treat indir.control Y(0,M(0))
effect 0.7090    0.3114      0.4340      0.2750        0.3975    2.2311

=== Part B: n=800 ===
        total dir.treat dir.control indir.treat indir.control Y(0,M(0))
effect 0.7089    0.4369      0.4476      0.2613        0.2720    2.1320
Planted: a-path=0.6, b-path=0.5, direct c'=0.25 -> approx indirect~0.30, total~0.55

=== Part C: n=150, near-collinear unnamed covariates ===
medDML FAILED: subscript out of bounds
(This is now a DOCUMENTED, expected failure -- SKILL.md's Common Errors table added this exact
row in 10be9a2, before the redundancy pass, and it is confirmed still present.)
```
**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100 (up from 74/100 in the 88 report).
**Assertions:** 4/4 PASS (up from 2/4). The two assertions that FAILED in the 88 report — that the
real results-matrix shape is documented, and that the Common Errors table covers this crash — now
both PASS: SKILL.md's Working Code Pattern shows the exact matrix shape this run reproduces
column-for-column, and the Common Errors table's `subscript out of bounds` row names the correct
cause and fix. **Both medDML P2s from the 88 report are resolved.**

---

### Input 9 — Variant A (regression)
**Prompt:** "I have independent GWAS summary statistics for exposure E (LDL) and a candidate
mediator M (a liver biomarker), and outcome Y (CHD). Some SNPs might affect both E and M. Run
two-step MR mediation (not MVMR) and check whether instrument independence holds before trusting
the indirect effect."

**Code:** `run/input9_twostep_mr_mediation.R`
**Output (excerpt):** `run/input9_output.txt`
```
Naive (pleiotropic SNPs left in): Indirect = 0.4401  [true = 0.3]  bias +0.1401
Steiger filter: 0/20 shared SNPs retained (all correctly excluded)
Steiger-filtered: Indirect = 0.3555  [true = 0.3]  bias +0.0555
Filtered closer to true than naive: TRUE
```
**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100 — numerically identical to the 88 report.

---

### Input 10 — Stress (NEW — BCa case-sensitivity, redundancy-pass check)
**Prompt:** "My labmate's script from last year calls `mediate(..., boot.ci.type='BCa')`. I'm about
to scale this up to `sims=5000` for the paper. Anything wrong before I run it?"

Per the fix log's redundancy-pass table, this exact fact ("BCa case-sensitivity — `'bca'` not
`'BCa'`") was one of three items *folded into* SKILL.md from usage-guide.md's now-deleted 13-bullet
Tips list; it did not exist in SKILL.md before `6e5f414`. This input checks whether the fact
survived the move and is still practically actionable, not just textually present.

**Code:** `run/input10_bca_case_sensitivity.R`
**Output (excerpt):** `run/input10_output.txt`
```
--- Attempt A: boot.ci.type='BCa' (labmate's script, wrong case) ---
[1] "ERROR: choose either `bca' or `perc' for boot.ci.type"

--- Attempt B: boot.ci.type='bca' (fixed SKILL.md's documented correct value) ---
Running nonparametric bootstrap
[1] "OK -- ran without error"

Matching line in SKILL.md:
"...BCa CIs (`boot.ci.type='bca'` in `mediate()` -- lowercase `'bca'`, not `'BCa'`) are slightly
more accurate..."
```
**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100.
**Assertions:** 4/4 PASS. `mediate()` itself throws a real, informative error for the wrong case
(not a silent misbehavior), and SKILL.md's fixed text — grep-confirmed present, verbatim — is
exactly what an agent needs to catch the labmate's bug before the expensive `sims=5000` run.

---

### Input 11 — Variant (NEW — cell-composition confounder, redundancy-pass check)
**Prompt:** "My EWAS HIMA mediators (Illumina EPIC methylation, `hima_classic()`) are probably
confounded by blood cell-type composition. What should I do, specifically?"

Per the fix log, SKILL.md previously said only the generic phrase "cell composition" with no
actionable method name or argument names; the Houseman/reference-free-RPC method name and the
`hima_classic()` argument names (`COV.XM`, `COV.MY`) were folded in from usage-guide.md's Tips list
during the redundancy pass.

**Response (Mode A, no code):** Names the Houseman or reference-free RPC method for estimating cell
proportions, and instructs passing them in both `COV.XM` and `COV.MY` for `hima_classic()` (formula
interface: as additional RHS terms). Directly quotes SKILL.md line 159:
> "Cell composition is the canonical unmeasured confounder in EWAS mediation: include estimated cell
> proportions (Houseman or reference-free RPC method) as covariates -- in the formula interface, add
> them as RHS terms...; in `hima_classic()`, pass them in both `COV.XM` and `COV.MY`."

**Scores:** Basic 37/40 | Specialized 54/60 | Total 91/100.
**Assertions:** 4/4 PASS. Grep-confirmed: this exact sentence is present in the redundancy-passed
SKILL.md; usage-guide.md (71 lines) no longer has any Tips section, so an agent reading only
SKILL.md still gets full, correct, actionable guidance.

---

### Input 12 — Stress (NEW — E-value formula check; surfaced one new defect)
**Prompt:** "I don't have the EValue package available on this cluster node. Given ACME expressed as
a risk ratio of 1.8 (95% CI lower bound 1.2), compute the mediational E-value by hand using the
formula in the Skill, then tell me what E-value package call would double-check it if I had network
access."

Per the fix log, the formula `E = RR + sqrt(RR*(RR-1))` was *moved* into SKILL.md's `## Mediational
E-Value for Sensitivity` section during the redundancy pass — SKILL.md previously named the method
(Smith & VanderWeele 2019) but never gave the formula itself.

**Code:** `run/input12_evalue_hand_formula.R`
**Output (excerpt):** `run/input12_output.txt`
```
Hand-computed via SKILL.md formula E = RR + sqrt(RR*(RR-1)):
  E(point, RR=1.8)      = 3
  E(CI lower, RR=1.2)   = 1.6899

Package check -- evalues.RR(est=1.8, lo=1.2) [default hi=NA]:
E-values   3.0 1.689898

Agreement (hand vs package): diff = 0 (point), diff = 0 (CI bound)

--- Also trying SKILL.md's LITERAL documented call, hi=NULL ---
[1] "ERROR: argument is of length zero"
```
**Scores:** Basic 36/40 | Specialized 52/60 | Total 88/100.
**Assertions:** 3/4 PASS. The hand formula matches the EValue package exactly (confirms the
redundancy pass preserved the formula correctly), and the formula text is grep-confirmed present in
SKILL.md. But while exercising SKILL.md's adjacent `Working Code Pattern` line literally —
`evalues.RR(acme_rr, lo=acme_lower_rr, hi=NULL)` — this run found it **crashes** on installed EValue
4.1.4 (`args(evalues.RR)` shows `hi` defaults to `NA`, not `NULL`). This defect pre-dates the
redundancy pass (the line is unchanged since at least `7f94fdd`) and neither prior audit executed
this specific code block — it is a genuinely new finding, not a redundancy-pass regression. **Filed
as a new P2** (see `recommendations[]` in the JSON report).

---

## Notes for reviewer

- Check ⚠️ Input 12 first: not a regression, and not caused by the redundancy pass — a
  previously-unexecuted line in SKILL.md's own E-value example that crashes as written. Easy,
  isolated one-line fix (see the JSON's `recommendations[]`).
- Every regression input (1-9) reproduces the prior report's numeric results exactly (identical
  scripts/seeds), which is the cleanest possible evidence that the redundancy pass — moving content
  out of usage-guide.md and deleting the duplicate — did not silently break anything already
  verified working.
- Inputs 10 and 11 are the load-bearing checks for the redundancy pass specifically: both target
  facts the fix log itself says used to exist *only* in usage-guide.md's now-deleted Tips list, and
  both found that content present, correct, and actionable in SKILL.md alone.
- Both medDML P2s open at the end of the 88 report are resolved and re-verified by Input 8 in this
  round, unaffected by the redundancy pass (they were fixed in the earlier commit `10be9a2`).
