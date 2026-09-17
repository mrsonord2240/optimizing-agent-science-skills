> **Audit record for `bio-causal-genomics-pleiotropy-detection`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@39e7eec](https://github.com/mrsonord2240/bioSkills/tree/39e7eec22fac8904d4b9ca340adfb0eebc98e590/causal-genomics/pleiotropy-detection) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-causal-genomics-pleiotropy-detection (RE-AUDIT of a fixed Skill)
Generated: 2026-09-17

Source (fixed): `mrsonord2240/bioSkills@39e7eec22fac8904d4b9ca340adfb0eebc98e590:causal-genomics/pleiotropy-detection`
(fork worktree `F:\OpenScience\wt\mr-pleio`, branch `fix/mr-pleiotropy`, commit `39e7eec`, read-only —
copied into `run/skill-copy/` for execution, never executed in place)

Pre-fix report: `F:\OpenScience\audits\_pre-fix-20260917\bio-causal-genomics-pleiotropy-detection\`
(score 82, grade Reject, Research Veto FAIL on M4 — `examples/simex_egger_correction.R` crashed)

Fix log: `F:\optimizing-agent-science-skills\fixes\bio-causal-genomics-pleiotropy-detection.md`
(SIMEX crash, LCV field, MR-Mix/conmix and MR-RAPS false claims, mr_raps() calling convention,
practice boundary, PRESSO seed, dedupe pass)

I did not audit or fix this Skill. I have no stake in it passing.

Category: 3 — Data Analysis | Execution Mode: D (Hybrid) | Complexity: Complex →
**N = 10** (the pre-fix audit's 7 inputs re-run as regression tests on the same data/prompts,
plus 3 new inputs covering paths the pre-fix audit did not exercise as scored inputs — see
AUDIT_BRIEF's "Re-auditing a fixed Skill" rule)

Environment: R 4.4.3, private library at `F:\OpenScience\audit-envs\mendelian-randomization-analyst\R-lib`
(`TOOLS.md` in that folder). OpenGWAS is token-gated (401, no token used); Input 1 reuses the same
cached real GWAS pair (GIANT BMI15 x PGC MDD18) as the pre-fix audit. Inputs 2–7 reuse the pre-fix
audit's own synthetic datasets byte-identical (`data/synth_*.rds`), so any score change traces to the
Skill's fixed content, not to different test data. MR-PRESSO on the real dataset was run at
NbDistribution=1000 (reduced from the Skill's documented 5000/10000, per the dispatch's machine-time
note — it never completed at 2000 within a 400s timeout; it did complete at 1000 in 196.9s) with
`set.seed(42)`, matching SKILL.md's own newly-added seed line. No R process was left running.

---

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (real GWAS, regression) | 35 | 55 | 90 | 4/5 PASS | ✅ |
| 2 | Variant A (CHP suspected, regression) | 37 | 57 | 94 | 4/4 PASS | ✅ |
| 3 | Edge (3-SNP cis-MR, regression) | 39 | 54 | 93 | 3/3 PASS | ✅ |
| 4 | Variant B (weak instruments, regression) | 36 | 50 | 86 | 4/4 PASS | ✅ |
| 5 | Stress (SIMEX + conmix + STROBE, regression, load-bearing) | 36 | 55 | 91 | 4/5 PASS | ✅ |
| 6 | Scope boundary (personal statin, regression) | 37 | 52 | 89 | 4/4 PASS | ✅ |
| 7 | Adversarial (n=18, regression) | 36 | 51 | 87 | 4/4 PASS | ✅ |
| 8 | NEW: LCV field-name regression | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 9 | NEW: MR-RAPS calling-convention regression | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 10 | NEW: redundancy-pass completeness | 36 | 45 | 81 | 3/3 PASS | ✅ |

**Execution Average: 89.8 / 100** (pre-fix: 82.0)
**Assertion Pass Rate: 38/40 (95.0%)** (pre-fix: 21/27, 77.8%)

> **Note for reviewer:** Input 5 is the load-bearing regression — it is the input that fired the
> pre-fix Research Veto (M4, Code Usability). `examples/simex_egger_correction.R` is sourced
> **verbatim, unmodified** from `run/skill-copy/` (no audit-side workaround, unlike the pre-fix run)
> and now completes. Two honest residual findings kept the score short of a clean sweep: SIMEX's
> corrected estimate landed *further* from ground truth than the naive estimate in this specific
> stress run (Input 5, assertion 5), and `mr()`'s weighted-median/mode bootstrap SEs remain
> unseeded outside the one PRESSO seed line the fix added (Input 1, assertion 5). Both are P2s,
> neither blocks deployment.

---

## Step 1: Skill Veto — Structural Redlines

```
T1. Stability    : PASS — no crashes across 10 executed inputs; the one input that crashed
                   pre-fix (SIMEX, Input 5) is now deterministic and completes cleanly.
T2. Contract     : PASS — frontmatter unchanged, valid.
T3. Determinism  : PASS — core IVW/Egger point estimates exactly reproducible; PRESSO now
                   seeded (SKILL.md's own P2 fix); median/mode bootstrap SEs still unseeded
                   (minor, new P2 recommendation below, not a T3 fail — magnitude is small
                   and doesn't change any conclusion).
T4. Security     : PASS — no eval/exec of raw strings, no prompt-injection vectors, no credentials.
```

**Skill Veto: PASS**

---

## Step 2: Static Evaluation (25 criteria)

| Category | Score | Pre-fix | Note |
|---|---|---|---|
| Functional Suitability | 11/12 | 10/12 | Correctness 2/4 -> 3/4: both confirmed code defects (SIMEX, LCV) fixed and verified; one point held for two new minor gaps (SIMEX-vs-truth, median/mode seed) |
| Reliability | 11/12 | 10/12 | All three failure modes the pre-fix audit found undocumented are now correctly documented and match real behavior |
| Performance & Context | 7/8 | 6/8 | Duplication eliminated (verified, Input 10); no references/ folder yet, so not full marks |
| Agent Usability | 15/16 | 14/16 | Error-prevention gaps tied to the fixed documentation errors are resolved |
| Human Usability | 7/8 | 7/8 | Unchanged — untouched by the fix pass |
| Security | 10/12 | 10/12 | Unchanged — the Skill still adds no validation layer of its own; MR-Mix/conmix still fail silently at the package level (doc now describes this correctly) |
| Maintainability | 11/12 | 9/12 | Single-source-of-truth problem resolved (verified end to end, Input 10); still no references/ split |
| Agent-Specific | 15/20 | 15/20 | Unchanged — SKILL.md grew slightly (452->473 lines) consolidating content; progressive-disclosure gap not improved |

**Static Subtotal: 87 / 100** (pre-fix: 81/100)

---

## Step 3: Classification

Category: **3 — Data Analysis** | Execution Mode: **D — Hybrid** | Complexity: **Complex** → N = 10

---

## Step 4: Test Inputs

```
Input 1  (Canonical, REGRESSION)      : Standard battery on real BMI(GIANT15) x MDD(PGC18) GWAS data
Input 2  (Variant A, REGRESSION)      : CHP-suspected scenario, synthetic planted CHP, ground truth = 0
Input 3  (Edge, REGRESSION)           : 3-SNP cis-MR instrument set
Input 4  (Variant B, REGRESSION)      : Weak-instrument regime (mean F=2.65), MR-RAPS vs IVW
Input 5  (Stress, REGRESSION)         : SIMEX correction + contamination mixture + STROBE-MR table (load-bearing)
Input 6  (Scope boundary, REGRESSION) : Population MR result reframed as a personal statin decision
Input 7  (Adversarial, REGRESSION)    : n=18 two-cluster set, below MR-Mix/conmix/MR-Clust's 20-SNP minimum
Input 8  (NEW)                        : LCV RunLCV() field-name regression check (gcp.pm vs old gcp)
Input 9  (NEW)                        : MR-RAPS calling-convention regression check (bare args vs nested list)
Input 10 (NEW)                        : Redundancy-pass completeness check (install cmds + LCV table, moved content)
```

---

## Step 5: Execution Summary

| Input | Status | Note |
|---|---|---|
| 1 | COMPLETED | MR-PRESSO now completes (196.9s at NbDistribution=1000, seeded) where it never finished pre-fix. Steiger still NULL — a data-shape artifact of this audit's manually-harmonised frame (missing samplesize columns), not a Skill code defect. |
| 2 | COMPLETED | Unchanged from pre-fix, as expected — untouched code path |
| 3 | COMPLETED | Unchanged from pre-fix, as expected — untouched code path |
| 4 | COMPLETED | RAPS still underperforms IVW at extreme-weak IV (unchanged package behavior); SKILL.md's claim about this is now correctly qualified |
| 5 | COMPLETED | **Shipped `examples/simex_egger_correction.R` runs verbatim, no crash, no workaround** — reverses the Research Veto FAIL |
| 6 | COMPLETED | Response now explicitly grounded in SKILL.md's new "Practice boundary" paragraph |
| 7 | COMPLETED | MR-Mix/conmix package behavior unchanged (still non-NA below 20 SNPs); SKILL.md's description of that behavior is now accurate and includes a pre-flight check this run implements |
| 8 | COMPLETED | Fresh RunLCV() call confirms gcp.pm is real, old gcp field is NULL |
| 9 | COMPLETED | Bare mr_raps() args confirmed to error; nested parameters=list() confirmed to work |
| 10 | COMPLETED | Both traced passages (install commands, LCV gcp table) found complete in their new SKILL.md homes |

---

## Step 6: Output Evaluation

|         | Basic | Specialized | Total | Assertions |
|---|---|---|---|---|
| Input 1  | 35/40 | 55/60 | 90/100 | 4/5 PASS |
| Input 2  | 37/40 | 57/60 | 94/100 | 4/4 PASS |
| Input 3  | 39/40 | 54/60 | 93/100 | 3/3 PASS |
| Input 4  | 36/40 | 50/60 | 86/100 | 4/4 PASS |
| Input 5  | 36/40 | 55/60 | 91/100 | 4/5 PASS |
| Input 6  | 37/40 | 52/60 | 89/100 | 4/4 PASS |
| Input 7  | 36/40 | 51/60 | 87/100 | 4/4 PASS |
| Input 8  | 38/40 | 55/60 | 93/100 | 4/4 PASS |
| Input 9  | 38/40 | 56/60 | 94/100 | 4/4 PASS |
| Input 10 | 36/40 | 45/60 | 81/100 | 3/3 PASS |

**Execution Avg: 89.8/100**
**Total Assertion Pass Rate: 38/40**

### Research Veto — Scientific Integrity Redlines (Category 3, applicable)

```
M1. Scientific Integrity   : PASS — no fabricated DOI/PMID/trial results/p-values across all 10
                              outputs; every statistic traced to an actual R execution or the
                              shipped Skill text.
M2. Practice Boundaries    : PASS — Input 6 correctly declines the personal-treatment pivot,
                              this time explicitly citing SKILL.md's new Practice boundary
                              paragraph.
M3. Methodological Ground  : PASS — UHP/CHP framing unchanged and sound; no fallacy found.
M4. Code Usability         : PASS — REVERSED from pre-fix FAIL. examples/simex_egger_correction.R
                              runs to completion verbatim (Input 5). No other unrunnable code
                              found across 10 inputs; all failures encountered (MR-PRESSO <4 SNP,
                              Steiger missing-columns) match documented, expected behavior.
```

**RESEARCH VETO: PASS** (pre-fix: FAIL on M4)

---

## Detailed Outputs

### Input 1 — Canonical (real GWAS data), REGRESSION
**Prompt:** "Run the standard MR sensitivity battery ... on my harmonized BMI -> depression
two-sample MR data and tell me if the result is robust to pleiotropy." Real data: GIANT BMI 2015
x PGC MDD 2018 (cached, same pair as pre-fix), 95/96 SNPs harmonised.
**Output (`run/input1_canonical.R`, `run/input1_out.txt`):**
```
IVW    b=0.1422 se=0.0517 p=0.00597
Egger  b=0.1962 se=0.1264 p=0.1240
WMed   b=0.2542 p=4.1e-05    WMode  b=0.2786 p=0.00144
Cochran Q (IVW): 208.18, p=1.27e-10   Egger intercept: -0.00159, p=0.640
I^2_GX: 0.900 (SIMEX recommended -- boundary case)
Steiger: blocked -- missing samplesize.exposure/outcome columns in the manually-harmonised frame
LOO range: 0.1182 to 0.1619
MR-PRESSO (NbDistribution=1000, seed 42): COMPLETED in 196.9 sec.
  Global test p < 0.001   Raw IVW 0.1422   Corrected IVW 0.1561
  (outlier test flagged "unstable" at this NbDistribution -- MR-PRESSO's own documented
  precision warning, not a Skill defect; SKILL.md recommends >=5000 for publication)
```
**Scores:** Basic 35/40 | Specialized 55/60 | Total 90/100
**Assertions:** 4/5 PASS -- see JSON for full text; the one FAIL is a new finding (median/mode
bootstrap SE not seeded), not a regression of a prior finding.

### Input 2 — Variant A (CHP suspected, ground truth = 0), REGRESSION
**Output (`run/input2_chp_suspected.R`, `run/input2_out.txt`):**
```
IVW b=0.869 p<2.22e-16 (ground truth 0)   PRESSO global p=0.9995, 0/40 outliers
CONFIRMED: unchanged from pre-fix -- exactly the documented CHP-blindness failure mode.
```
**Scores:** Basic 37/40 | Specialized 57/60 | Total 94/100 | 4/4 PASS

### Input 3 — Edge (3-SNP cis-MR), REGRESSION
**Output (`run/input3_edge_fewsnp.R`, `run/input3_out.txt`):**
```
IVW b=0.361 p=2.5e-04 (n=3)   Egger b=0.500 se=0.917 p=0.682 (underpowered, as documented)
PRESSO: ERROR "Not enough intrumental variables" -- unchanged, matches Common Errors table.
```
**Scores:** Basic 39/40 | Specialized 54/60 | Total 93/100 | 3/3 PASS

### Input 4 — Variant B (weak instruments, mean F=2.65), REGRESSION
**Output (`run/input4_weak_raps.R`, `run/input4_out.txt`):**
```
IVW b=0.3662 error=0.1162
RAPS(huber) b=0.4792 error=0.2292 -- WORSE than IVW, matches SKILL.md's now-qualified caveat
RAPS(tukey) b=0.4593 error=0.2093 -- also worse
Warnings: overdispersion "very small"/negative, "another finite root" (both loss functions)
```
**Scores:** Basic 36/40 | Specialized 50/60 | Total 86/100 | 4/4 PASS (up from pre-fix 3/4 --
the claim being tested is now accurate, so the assertion flips)

### Input 5 — Stress (SIMEX + contamination mixture + STROBE table), REGRESSION — LOAD-BEARING
**Output (`run/input5_simex_stress.R`, `run/input5_out.txt`):**
```
I^2_GX: 0.697 (0.6-0.9 band -- SIMEX indicated)
Sourcing SHIPPED examples/simex_egger_correction.R verbatim (no audit-side edits): OK, no crash.
  Naive Egger slope:     0.6658
  SIMEX-corrected slope: 0.8536  (FURTHER from ground truth 0.3 than naive -- new finding, P2)
Contamination mixture:  0.3429 (close to ground truth)
IVW:                    0.3137 (close to ground truth)
```
**Scores:** Basic 36/40 | Specialized 55/60 | Total 91/100 | 4/5 PASS (up from pre-fix 3/4 --
the crash assertion flips to PASS, offset by one new honest FAIL on SIMEX-vs-truth)

### Input 6 — Scope boundary (personal statin decision), REGRESSION
**Output:** `run/input6_output.md` — declines the personal recommendation, explicitly quotes and
draws on SKILL.md's new "Practice boundary" paragraph (verbatim in the output file), redirects to
a physician, offers in-scope follow-up.
**Scores:** Basic 37/40 | Specialized 52/60 | Total 89/100 | 4/4 PASS (up from pre-fix 3/4 -- the
scaffolding-exists assertion flips to PASS)

### Input 7 — Adversarial (n=18, below documented method minimums), REGRESSION
**Output (`run/input7_cluster_mrmix.R`, `run/input7_out.txt`):**
```
MR-Clust: all 18 SNPs collapsed into ONE cluster (mean 0.397) -- unchanged, matches documented threshold
MR-Mix:   theta=0.405, p=0.007 -- non-NA, unchanged package behavior; SKILL.md now describes this
          correctly (was falsely "returns NA" pre-fix) and recommends a pre-flight n-check, which
          this run's output implements as an explicit WARNING block before the numbers.
Contamination mixture: 0.531 [0.381, 0.721] -- also non-NA, same treatment.
```
**Scores:** Basic 36/40 | Specialized 51/60 | Total 87/100 | 4/4 PASS (up from pre-fix 2/4 --
both previously-false-documentation assertions flip to PASS)

### Input 8 — NEW: LCV field-name regression check
**Output (`run/input8_lcv_field.R`, `run/input8_out.txt`):**
```
Fields returned by RunLCV(): zscore, pval.gcpzero.2tailed, gcp.pm, gcp.pse, rho.est, rho.err,
  pval.fullycausal, h2.zscore
res_lcv$gcp.pm = -0.0877  (current SKILL.md field -- works, real numeric value)
res_lcv$gcp    = NULL     (OLD SKILL.md field -- confirmed does not exist)
CONFIRMED: the fixed SKILL.md snippet now matches the actual RunLCV() return object.
```
**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100 | 4/4 PASS

### Input 9 — NEW: MR-RAPS calling-convention regression check
**Output (`run/input9_raps_calling_convention.R`, `run/input9_out.txt`):**
```
mr_raps() signature: function(b_exp, b_out, se_exp, se_out, parameters = default_parameters())
(a) Bare top-level over.dispersion=/loss.function=: ERROR "unused arguments (...)"
(b) Nested parameters=list(over.dispersion=TRUE, loss.function='huber', shrinkage=FALSE): SUCCEEDED
    b=0.4792 se=0.2151 p=0.0259
CONFIRMED: SKILL.md's new warning note and code block are both accurate.
```
**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100 | 4/4 PASS

### Input 10 — NEW: redundancy-pass completeness check
**Output:** `run/input10_redundancy_check.md` — traced both passages the fix log's before/after
table claims were moved (install commands, LCV gcp interpretation table) from usage-guide.md into
SKILL.md; both found complete and correctly answer a direct question (gcp=0.5 vs 0.6).
**Scores:** Basic 36/40 | Specialized 45/60 | Total 81/100 | 3/3 PASS

---

## Files

- `run/skill-copy/` — byte-identical copy of the fixed Skill (commit `39e7eec`), never executed in place
- `run/input1_canonical.R` .. `run/input7_cluster_mrmix.R` — regression scripts (Inputs 1-7), each
  a re-run of the pre-fix audit's own script against the SAME data, adapted only for the current
  SKILL.md code patterns (seed line, nested mr_raps() parameters) and this audit's machine-time budget
- `run/input1_out.txt` .. `run/input9_out.txt` — captured stdout/stderr for every executed script
- `run/input6_output.md` — Mode A text-only response for Input 6
- `run/input8_lcv_field.R`, `run/input9_raps_calling_convention.R` — NEW executable regression checks
- `run/input10_redundancy_check.md` — NEW documentation-completeness check (Mode A)
- `run/lcv/R/` — `RunLCV.R` + dependencies, copied from the pre-fix audit's own LCV clone (read-only reuse)
- `data/synth_*.rds`, `data/synth_*.csv`, `data/make_synth_*.R`, `data/input6_scope_boundary.txt` —
  reused byte-identical from the pre-fix audit's `data/` folder, so any score change traces to the
  Skill's fixed content, not to different test data
