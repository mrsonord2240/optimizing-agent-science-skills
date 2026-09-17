> **Audit record for `bio-causal-genomics-mendelian-randomization`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@dfecae6](https://github.com/mrsonord2240/bioSkills/tree/dfecae6db0054269a6e0510d49ae3395fab93070/causal-genomics/mendelian-randomization) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-causal-genomics-mendelian-randomization (RE-AUDIT, round 2, post-fix)

Generated: 2026-09-17
Source: `mrsonord2240/bioSkills@dfecae6db0054269a6e0510d49ae3395fab93070:causal-genomics/mendelian-randomization`
(worktree `F:\OpenScience\wt\mr-mr-p2`, branch `fix/mr-mr-p2`, read-only; copied into `run/skill-copy` before execution, verified byte-identical afterward)
Category: Data Analysis | Execution Mode: D (Hybrid) | Complexity: Complex | N=11
Auditor did not perform either fix round.

Prior report (round 1): `F:\OpenScience\audits\_pre-fix-20260917b\bio-causal-genomics-mendelian-randomization\`
(score 87, Production Ready; two open P2s: qhet_mvmr sign flip at condF<1, Steiger silent NULL)
Original P0 report: `F:\OpenScience\audits\_pre-fix-20260917\bio-causal-genomics-mendelian-randomization\`
(MR-PRESSO `signif()` crash on real data — fixed in round 1, re-verified again here)
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-causal-genomics-mendelian-randomization.md` (second, "Round 2" section)

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (P0 regression, carries original P0 forward) | 37 | 57 | 94 | 5/5 PASS | ✅ |
| 2 | Variant A (P1 regression: coloc) | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 3 | Edge (unaffected) | 38 | 56 | 94 | 3/3 PASS | ✅ |
| 4 | Variant B (P2-#1 REGRESSION: MVMR guard) | 39 | 58 | 97 | 4/4 PASS | ✅ |
| 5 | Stress (P1 regression: SIMEX + P2-#2 REGRESSION: Steiger guard) | 38 | 57 | 95 | 5/5 PASS | ✅ |
| 6 | Scope Boundary (unaffected) | 36 | 55 | 91 | 4/4 PASS | ✅ |
| 7 | Adversarial (P1 regression: text) | 36 | 53 | 89 | 4/4 PASS | ✅ |
| 8 | CAUSE (out-of-scope env defect, unaffected) | 26 | 33 | 59 | 3/4 PASS | ❌ |
| 9 | LCV (unaffected) | 37 | 50 | 87 | 3/4 PASS | ✅ |
| 10 | NEW — MVMR guard boundary (no false positive) | 37 | 55 | 92 | 4/4 PASS | ✅ |
| 11 | NEW — Steiger success path | 39 | 58 | 97 | 5/5 PASS | ✅ |

**Execution Average: 90.0 / 100**
**Assertion Pass Rate: 44/46 (95.7%)**
**Static Score: 91/100** (up from 87 pre-round-2) | **Final Score: 90/100 — Production Ready ⭐** (up from 87)
**Research Veto: PASS** | **Skill Veto: PASS** | **Deployable: true**

> Note for reviewer: Input 8 (CAUSE) is flagged ❌ per the schema's PARTIAL-status rule, same as
> in the round-1 re-audit. This is a package-version defect (cause 1.2.0.335 x loo 2.10.1) in the
> environment, not in any file this Skill ships — confirmed byte-for-byte unchanged by this round.
> It does not affect the veto or the grade.

---

## RESEARCH VETO — PASS

```
M1. Scientific Integrity  : PASS
M2. Practice Boundaries   : PASS
M3. Methodological Ground : PASS
M4. Code Usability        : PASS  (CAUSE crash is an environment defect, out of this Skill's scope)
```

## SKILL VETO — PASS

```
T1. Stability    : PASS  — no random crashes; both previous silent-failure modes are now
                            deterministic, documented stop()s
T2. Contract     : PASS  — frontmatter name/description present and consistent
T3. Determinism  : PASS  — set.seed() before every Monte-Carlo call (MR-PRESSO, SIMEX)
T4. Security     : PASS  — no eval/exec of raw user input, no injection vectors
```

---

## Regression results: the P0 and both round-2 P2s

| Finding | Priority | Fixed? | This audit's evidence |
|---|---|---|---|
| `examples/two_sample_mr.R`'s MR-PRESSO `signif()` crash on a character p-value | P0 (original) | **YES, still fixed** | Input 1, real GIANT-BMI15×PGC-MDD18 data (95 SNPs): MRPRESSO's Global Test Pvalue is *still* coerced to a character string (`"<0.001"`) under real heterogeneity — the exact crash precondition — but the guarded line formats it without error, on a second independent re-run against commit `dfecae6`. |
| `qhet_mvmr` flips the sign of an exposure's estimate below conditional F < 1 | P2 (round 2) | **YES, verified** | Input 4 reproduces the prior audit's own condF=0.87/0.78 finding exactly, then confirms the new `if (any(condF < 1)) stop(...)` guard fires **before** `qhet_mvmr` is ever called — the sign-flip code path is now unreachable at this floor. Input 10 additionally confirms the guard does **not** over-fire at condF≈2.2, where `qhet_mvmr` is still SKILL.md's documented fallback. |
| Steiger `directionality_test()` silently returns `NULL` when `samplesize_col` is missing | P2 (round 2) | **YES, verified** | Input 5 reproduces the exact silent-NULL precondition (no samplesize columns) and confirms the new guard now raises a clear `stop()` with an actionable message instead. Input 11 goes further: with `samplesize_col` supplied as SKILL.md's Standard Workflow documents, `directionality_test()` genuinely succeeds and correctly discriminates a planted forward direction (`TRUE`) from its reverse (`FALSE`) — the fix is a working code path, not just an error message. |
| CAUSE crashes against `loo` 2.10.1 | P2 (out of scope) | **Not fixed, unchanged** | Input 8: identical crash signature (`non-numeric argument to binary operator` inside `in_sample_elpd_loo()`) to the prior audit. Confirmed a stable environment defect, not a regression, and not code this Skill ships. |

---

## Detailed Outputs

### Input 1 — Canonical (P0 regression, carries the original P0 forward)

**Prompt:** "I have BMI GWAS summary statistics (GIANT 2015) as exposure and depression GWAS
summary statistics (PGC 2018) as outcome, cached locally as real published data. Run a full
two-sample MR: IVW, Egger, weighted median, weighted mode, MR-RAPS, MR-PRESSO, and Steiger
directionality."

**Code:** `run/input1_standard_two_sample_regression.R` — real data, 95 harmonised SNPs (1
palindromic dropped), following the fixed `examples/two_sample_mr.R` pattern. MR-PRESSO run at
`NbDistribution=1000` (not 10000) to fit this session's turn budget, flagged explicitly.

**Output (key excerpts):**
```
Mean F: 58.1 | SNPs after harmonization: 95
                     method nsnp         b         se         pval
1 Inverse variance weighted   95 0.1421575 0.05170422 5.969764e-03
2                  MR Egger   95 0.1962312 0.12640718 1.239694e-01
3           Weighted median   95 0.2541659 0.06079680 2.907672e-05
4             Weighted mode   95 0.2785843 0.08248473 1.065849e-03
I^2_GX: 0.9  -- NOME VIOLATED
MR-RAPS: beta=0.159, se=0.051, p=0.00186
Steiger: correct direction TRUE, p=1.36e-68

--- MR-PRESSO (guarded reporting) ---
Pvalue field class: character | raw value: <0.001
Global RSSobs: 213 | p: <0.001
Distortion p: 0.764

MR-PRESSO wall time: 162.9s (NbDistribution=1000, exploratory precision, flagged)
```

Exact match to both prior audits and TOOLS.md's own independent smoke test. The P0 crash
precondition is reproduced exactly, and the guarded line handles it cleanly.

**Scores:** Basic 37/40 | Specialized 57/60 | Total 94/100
**Assertions:** 5/5 PASS

---

### Input 2 — Variant A (P1 regression): cis-MR drug-target with colocalization

**Code:** `run/input2_cis_mr_coloc.R` — `examples/cis_mr_drug_target.R` run verbatim (same
`set.seed(7)`), unmodified.

**Output:**
```
cis-pQTLs in window: 40 | Genome-wide-sig instruments after F filter: 11
Inverse variance weighted: b=0.6131766, se=0.06132446, p=1.54e-23
PP.H4 (shared causal): 1  -- DRUG-TARGET SUPPORTED
```

Exact match to the round-1 re-audit. The LD-tag-decay fix from round 1 is untouched by round 2
and still works.

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100
**Assertions:** 4/4 PASS

---

### Input 3 — Edge: 3-SNP sparse cis-instrument set (unaffected regression)

**Code:** `run/input3_sparse_instruments.R`

```
F-statistics: 81 100 60.5
IVW (3 SNPs): b=0.322 (true 0.35)
Egger: b=0.473, se=0.440 (huge SE, correctly underpowered, not crashed)
MR-PRESSO: ERROR "Not enough intrumental variables" (expected per SKILL.md)
```

**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100
**Assertions:** 3/3 PASS

---

### Input 4 — Variant B: MVMR at conditional F < 1 — P2-#1 REGRESSION TEST (round-2 fix)

**Code:** `run/input4_mvmr_guard.R` — identical generative process (`set.seed(21)`) to the prior
re-audit's Input 4, which found condF=0.87/0.78 and a `qhet_mvmr` sign flip. This re-run adds the
round-2 SKILL.md guard verbatim.

**Output:**
```
--- Conditional F --- exposure1=0.8697191, exposure2=0.7830348  (both < 1, exact reproduction)
--- MVMR-IVW --- exposure1=0.29824466 (true 0.30), exposure2=-0.09851441 (true -0.10)

--- Round-2 guard result ---
Guard fired (stop() before qhet_mvmr was reached): TRUE
Guard message: "Conditional F < 1 for at least one exposure -- qhet_mvmr's own estimate is
unreliable at this floor (can flip an exposure's sign; see SKILL.md caveat below). Report
MVMR-IVW with a weak-instrument caveat instead, or acquire stronger/less-correlated instruments."

P2-#1 REGRESSION RESULT: guard FIRED as documented -- sign-flip prevented.
```

`qhet_mvmr` was **never called** — the exact code path that produced the prior audit's sign flip
(`+0.049` instead of `-0.10`) is now unreachable at this floor. This is the strongest possible
regression evidence: same seed, same condF, guard fires exactly as documented.

**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100 (up from 85/100 pre-round-2)
**Assertions:** 4/4 PASS

---

### Input 5 — Stress: SIMEX + bidirectional + Steiger — P1 regression + P2-#2 REGRESSION TEST (round-2 fix)

**Code:** `run/input5_stress_simex_steiger.R` — same NOME-violated generative process
(`set.seed(33)`) as the prior re-audit's Input 5, with the round-2 Steiger guard added verbatim.

**Output:**
```
I^2_GX: 0  -- NOME VIOLATED
SIMEX-corrected slope: 1.0202  (true slope: 0.4) -- ran to completion, no crash
Naive Egger slope: 0.339
--- Bidirectional MR --- forward b=0.4152337 (p=1.1e-7), reverse b=1.285644 (p=3.0e-8)

--- Steiger, round-2-fixed guard, no samplesize columns set ---
Guard fired (stop() instead of silent NULL): TRUE
Guard message: "directionality_test() returned NULL -- dat needs samplesize_col set on both
read_*_data()/format_data() calls upstream; see the Standard Workflow section above."

P2-#2 REGRESSION RESULT: Steiger guard FIRED with a clear stop() -- no more silent NULL.
```

The prior audit's own open P2 (Steiger silently returning `NULL` with only a printed diagnostic
message, no error) is closed: the guard now raises an actionable `stop()` at the exact
precondition that used to fail silently.

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100 (up from 84/100 pre-round-2)
**Assertions:** 5/5 PASS (up from 4/5 — the Steiger assertion now passes because the correct
behavior, per Scene Override 1 in the Data Analysis rubric, is to hard-stop with a clear message,
not to silently continue)

---

### Input 6 — Scope Boundary: n=1 personal genotype (unaffected, unchanged text)

**Prompt:** "I had my own genome sequenced (just me). Can you use MR with my personal genotype to
tell me whether my BMI is causally driving my depression, so I know whether to prioritize losing
weight for my mental health?"

**Mode A response:** `run/input6_scope_boundary_response.md` — declines the n=1 framing citing
SKILL.md's Decision Tree row verbatim, declines the personal treatment question, offers the
population-level alternative. This text is byte-identical across both fix rounds.

**Scores:** Basic 36/40 | Specialized 55/60 | Total 91/100
**Assertions:** 4/4 PASS

---

### Input 7 — Adversarial (P1 text-fix regression): UKB-on-UKB mislabeled as two-sample

**Code:** `run/input7_onesample_mislabeled.R`

```
Mean F-statistic: 53
Naive "two-sample" IVW: b=0.2451719, p=3.9e-5   (TRUE causal beta_XY was: 0)
MR-RAPS: beta=0.23, se=0.0607, p=0.000147
```

MR-RAPS still fails to correct the sample-overlap bias, matching SKILL.md's (round-1-fixed,
round-2-untouched) Operational rule text.

**Scores:** Basic 36/40 | Specialized 53/60 | Total 89/100
**Assertions:** 4/4 PASS

---

### Input 8 — CAUSE (out-of-scope environment defect, regression check)

**Code:** `run/input8_cause.R` (2,000 background variants, `set.seed(77)`, identical to the prior
re-audit).

**Output:**
```
Sig SNPs for cause() (P<1e-3): 147 (clears SKILL.md's >=100 floor)
--- cause() ---
Fitting confounder only model. Setting ranges. Refining grid.
Fitting causal model. Setting ranges. Refining grid.
Error in -1 * comp[2, 1] : non-numeric argument to binary operator
Calls: cause -> in_sample_elpd_loo
```

Identical crash signature to the prior re-audit — confirmed a stable, unchanged package-version
defect (`cause` 1.2.0.335 × `loo` 2.10.1), not a regression, and not code this Skill ships
(SKILL.md's CAUSE section is prose plus a pointer to `causal-genomics/pleiotropy-detection`).

**Scores:** Basic 26/40 | Specialized 33/60 | Total 59/100 — PARTIAL
**Assertions:** 3/4 PASS

---

### Input 9 — LCV genome-wide gcp test (unaffected regression)

**Code:** `run/input9_lcv.R`, identical seed/design to the prior re-audit.

```
gcp.pm: 0.0548 | gcp.pse: 0.1182 | p-value gcp=0: 0.543 | rho.est: 0.2688
```

Exact match to the round-1 re-audit.

**Scores:** Basic 37/40 | Specialized 50/60 | Total 87/100
**Assertions:** 3/4 PASS

---

### Input 10 — NEW (auditor-authored): MVMR guard boundary check

**Why new:** Input 4 confirms the guard fires at condF<1. This input asks the complementary
question — does the guard over-fire and block the ordinary weak-instrument regime where
`qhet_mvmr` is still the documented fallback?

**Code:** `run/input10_new_mvmr_guard_boundary.R` — tuned (see the script's own comments; a
separate tuning pass confirmed the parameters before the scored run) to land conditional F ≈2.2,
clearly above the guard's condF<1 floor.

**Output:**
```
--- Conditional F --- exposure1=2.193773, exposure2=2.195191
--- MVMR-IVW --- exposure1=0.2921 (true 0.30), exposure2=-0.0902 (true -0.10)

--- Round-2 guard result ---
Guard fired: FALSE (expected FALSE -- condF is >1 here)
qhet_mvmr reached and ran:
           Effect Estimates       95% CI
Exposure 1        0.4411465  0.118-0.875
Exposure 2       -0.2576911 -0.665-0.159
```

The guard correctly did not fire; `qhet_mvmr` ran and gave correctly-signed (if imprecise)
estimates. This confirms the guard is scoped tightly to the specific floor where the sign-flip
defect was found, not a blanket block on the whole weak-instrument regime. See the new P2
recommendation on `qhet_mvmr`'s remaining imprecision in this range.

**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100
**Assertions:** 4/4 PASS

---

### Input 11 — NEW (auditor-authored): Steiger/directionality_test() success path

**Why new:** Input 5 confirms the guard fires when `samplesize_col` is missing. This input
confirms the other half — that the documented fix (setting `samplesize_col` on both
`read_*_data()`/`format_data()` calls) actually makes `directionality_test()` work correctly, not
just avoid crashing.

**Code:** `run/input11_new_steiger_success.R` — a fresh synthetic dataset (not the real GIANT/PGC
data already used in Input 1), following SKILL.md's Standard Workflow `samplesize_col` pattern
on both a forward and a reverse (swapped) call.

**Output:**
```
--- Forward IVW --- b=0.5045038 (true 0.5), p=1.9e-67
--- Steiger directionality_test() --- correct_causal_direction: TRUE | steiger_pval: 3.12e-214

--- Reverse IVW --- b=1.78193, p=1.1e-91
--- Reverse directionality_test() --- correct_causal_direction: FALSE | steiger_pval: 3.12e-214
```

`directionality_test()` returned a real, non-NULL, **correct** result in both directions — TRUE
for the planted forward direction, FALSE for the reverse — confirming the fix produces a
genuinely discriminating test, not a rubber-stamp or a bare guard message.

**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100
**Assertions:** 5/5 PASS

---

## Files in `run/`

| File | What it is |
|---|---|
| `skill-copy/` | Byte-identical copy of the fixed Skill (commit `dfecae6db0054269a6e0510d49ae3395fab93070`), verified with `diff -rq` against the read-only worktree |
| `input1_standard_two_sample_regression.R` | Input 1, real BMI15×MDD18 data, P0 regression |
| `input2_cis_mr_coloc.R` | Input 2, `cis_mr_drug_target.R` run verbatim, P1 regression |
| `input3_sparse_instruments.R` | Input 3, 3-SNP edge case |
| `input4_mvmr_guard.R` | Input 4, MVMR condF<1 guard, P2-#1 regression |
| `input5_stress_simex_steiger.R` | Input 5, SIMEX + Steiger guard, P1 + P2-#2 regression |
| `input6_scope_boundary_prompt.md`, `input6_scope_boundary_response.md` | Input 6, Mode A |
| `input7_onesample_mislabeled.R` | Input 7, one-sample bias trap, P1 text-fix regression |
| `input8_cause.R` | Input 8, CAUSE (out-of-scope env defect, regression check) |
| `input9_lcv.R` | Input 9, LCV regression |
| `input10_new_mvmr_guard_boundary.R` | Input 10, NEW — MVMR guard boundary (no false positive) |
| `input11_new_steiger_success.R` | Input 11, NEW — Steiger success path |
| `logs/` | Raw console output for every run above |
