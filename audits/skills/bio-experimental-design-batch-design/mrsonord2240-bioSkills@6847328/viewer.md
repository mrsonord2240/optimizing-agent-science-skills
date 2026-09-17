> **Audit record for `bio-experimental-design-batch-design`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6847328](https://github.com/mrsonord2240/bioSkills/tree/684732876d2781df75d90ba35c3e9949ff4f28b2/experimental-design/batch-design) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-experimental-design-batch-design (re-audit after fix)
Generated: 2026-09-16 · Re-auditor for `bio-experimental-design-batch-design` (bundled by round-2
candidates `crispr-screen-analyst` and `untargeted-metabolomics-analyst`, supporting Skill, floor 75)
· skill-auditor@1.0

Source: `mrsonord2240/bioSkills@684732876d2781df75d90ba35c3e9949ff4f28b2:experimental-design/batch-design`
(fix commit `e543a0a`, HEAD `6847328`). Files read: `SKILL.md` (post-fix), `usage-guide.md`,
`examples/batch_design.R`.

Pre-fix report: `F:/OpenScience/audits/_pre-fix-20260916/bio-experimental-design-batch-design/`
(score 82, Limited Release; P1: SVA block fails on matrices with missing values; P2s: no
verification step after optimization, no bridge/reference-channel layout).

Environment: `F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/rs.sh` — R 4.4.3,
designit 0.5.0, sva 3.54.0, limma 3.62.2 (per that candidate's `TOOLS.md`). Four R code blocks
extracted byte-for-byte from the post-fix SKILL.md into `runs/blocks/` (`b02_assign.R`,
`b02_verify.R` — the new verification section, `b03_bridge.R` — the new bridge/reference-channel
section, `b04_sva.R` — the fixed SVA block). All designs and matrices SYNTHETIC; Inputs 4 and 7
reuse the same real synthetic MaxQuant `proteinGroups.txt` from the pre-fix audit.

Role: **supporting** (framing/design). Category **Protocol Design** · Mode A · Complexity
**Moderate** → 5 pre-fix inputs re-run as regression + **2 new inputs** targeting the fix's own
claims (per the re-audit brief) → **N = 7**.

## Step 1 — Skill Veto
| Dimension | Result | Evidence |
|---|---|---|
| T1 Stability | PASS | All 7 inputs ran to completion; every `stopifnot` halt observed was an intended design-gate firing, not a crash. |
| T2 Contract | PASS | Frontmatter complete and unchanged. |
| T3 Determinism | PASS | SKILL.md's own shown code blocks still don't call `set.seed()` (unchanged from pre-fix, non-blocking); test scripts seed explicitly. |
| T4 Security | PASS | No eval/exec, network or credentials. |

## Step 2 — Static score: 87/100 (pre-fix: 81/100)
| Category | Score | Note |
|---|---|---|
| Functional suitability | 11/12 | New bridge-channel code closes the completeness gap; still no OSAT code. |
| Reliability | 9/12 | NA guard and verification gate confirmed working; docked because the bridge block didn't inherit the soft imbalance warning (see Input 2). |
| Performance/context | 7/8 | ~250 lines; bridge-layout optimization took 144 s (unchanged cost profile). |
| Agent usability | 15/16 | Pre-fix gap ("no instruction to verify after optimization") is fixed and confirmed to work. |
| Human usability | 7/8 | Unaffected. |
| Security | 11/12 | Unaffected. |
| Maintainability | 10/12 | New sections are self-contained and independently testable. |
| Agent-specific | 17/20 | Unaffected; trigger wording still genomics-first. |

**Gate 8: PASS** — every file `SKILL.md`/`usage-guide.md` points at exists; `examples/batch_design.R` runs end to end (exit 0, per the fix log, re-confirmed by code reading this session).

## Summary Table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 53 | 91 | 5/5 | yes | ✅ |
| 2 | Variant A | 29 | 43 | 72 | 2/4 | yes | ❌ |
| 3 | Edge | 37 | 55 | 92 | 4/4 | yes | ✅ |
| 4 | Variant B | 36 | 53 | 89 | 4/4 | yes | ✅ |
| 5 | Stress | 37 | 55 | 92 | 4/4 | yes | ✅ |
| 6 | Adversarial (NEW) | 38 | 50 | 88 | 4/4 | yes | ✅ |
| 7 | Scope Boundary (NEW) | 35 | 47 | 82 | 3/3 | yes | ✅ |

**Execution Average: 606/7 = 86.6** · **Assertions 26/28 (92.9%)** · L1 avg 35.7 · L2 avg 50.9

## Detailed Outputs

### Input 1 — Canonical (regression)
**Prompt:** "We're running 24 plasma samples (12 cases, 12 controls, half male) on the LC-MS in 3 batches of 8. How should I assign samples to batches so batch doesn't wreck the comparison?"
**Code:** `runs/in1_designit.R` sourcing `runs/blocks/b02_assign.R` then `runs/blocks/b02_verify.R` (both verbatim).
```
[b02_assign] OK | designit 0.5.0
condition x batch:  ctrl 4 4 4 | treat 4 4 4
empty positions: 0
[b02_verify] OK
```
**Scores:** Basic 38 · Specialized 53 · **91**. Assertions 5/5.

### Input 2 — Variant A (regression, now against real bridge-channel code)
**Prompt:** "60 plasma samples (30 case / 30 control, 3 collection sites) across 4 TMTpro 16plex runs. We want a pooled reference in the last channel of every plex. Give me the plex/channel layout."
**Code:** `runs/in2_bridge_channel.R` sourcing `runs/blocks/b03_bridge.R` **verbatim** (pre-fix required agent adaptation; post-fix does not).
```
Achieved score: 6 at iteration 78 | elapsed s: 144
condition x plex:  case 8 8 8 6 | ctrl 7 7 7 9
site x plex:       A 4 5 6 5 | B 5 5 5 5 | C 6 5 4 5
positions per plex used: 15,15,15,15
```
**Finding:** channel 16 correctly stays empty in every plex and the hard `stopifnot(all(tab>0))` passed (no empty cell) — but the split (8/8/8/6 vs 7/7/7/9, spread 3) is the same class of avoidable imbalance the original P2 finding flagged, and **no warning fired**, because the bridge block only copies the primary block's hard confounding check, not its soft `imbalance()` warning.
**Scores:** Basic 29 · Specialized 43 · **72**. Assertions 2/4.

### Input 3 — Edge (regression, code untouched by the fix)
**Prompt:** "Our study is already run: all 8 cases were digested and injected on day 1, all 8 controls on day 2. Can we fix it with ComBat and still publish the comparison?"
**Code:** `runs/in3_confounded_rescue.R`.
```
ComBat with condition covariate ERROR: The covariate is confounded with batch!
ComBat without covariate, then limma: calls 0 | true hits among them 0 | nulls 0
no correction (condition = day): calls 346 | true 67 | nulls (pure day effect) 279
limma ~cond + day: Coefficients not estimable: dayD2
```
**Scores:** Basic 37 · Specialized 55 · **92**. Assertions 4/4. Numbers match the pre-fix report exactly.

### Input 4 — Variant B (regression, direct P1-fix test)
**Prompt:** "Our MaxQuant LFQ matrix clusters oddly on PCA and we don't have processing dates. Can you check for hidden batches with SVA?"
**Code:** `runs/in4_sva_na.R` sourcing `runs/blocks/b04_sva.R` verbatim.
```
as imported: 1500 proteins x 8 samples, NA 2120 (18%)
2120/12000 cells (18%) are missing/non-finite; sva() requires a complete matrix.
Restricting to 738/1500 features with no missing values (Option A).
Number of significant surrogate variables is: 1
rows used after filtering: 738 / 1500
n_sv: 1 | cor(SV1, day B2): 1
independent check: complete.cases(M) = 738/1500 features (49.2%)
```
**Finding:** the pre-fix crash ("infinite or missing values in x") is gone; the block explains itself and proceeds, and the independent recount confirms the reported feature count. This is the P1 fix, confirmed by execution.
**Scores:** Basic 36 · Specialized 53 · **89**. Assertions 4/4.

### Input 5 — Stress (regression, code untouched by the fix)
**Prompt:** "Our 24 samples ended up unbalanced across three batches (8/2, 3/3, 1/7 case/control). The core ran ComBat and sent us the cleaned matrix for limma. Is that OK?"
**Code:** `runs/in5_unbalanced_combat.R` (20 seeds).
```
realized FDR (pooled over 20 seeds): ComBat-then-test 33.1% | batch in model 4.6%
```
**Scores:** Basic 37 · Specialized 55 · **92**. Assertions 4/4. Numbers match the pre-fix report exactly.

### Input 6 — Adversarial (NEW: does the verification step really gate, or just print?)
**Prompt (implicit; this is a direct test of the fix, not a user prompt):** "My core just handed back this plate map — sanity-check it before we run it," where the handed-back layout is deliberately confounded.
**Code:** `runs/in6_verify_catches_confound.R` (three tests of the verification code from Inputs 1 and 2).
```
Test A (batch B3 has 0 controls):        stopifnot HALTED: condition is confounded with batch...
Test B (genuinely balanced layout):      NO ERROR — verification passed (expected)
Test C (bridge plex 1 entirely 'case'):  stopifnot HALTED: all(tab3 > 0) is not TRUE
```
**Finding:** the verification step is a real gate — it halts on every confounded layout tested (including the bridge-channel variant) and does not false-positive on a balanced one.
**Scores:** Basic 38 · Specialized 50 · **88**. Assertions 4/4.
*Note: the first draft of this script had two bugs in the auditor's own harness (a stale variable in Test B, a miscounted vector in Test C) — fixed and re-run; see `runs/in6_verify_catches_confound.R` header comment.*

### Input 7 — Scope Boundary (NEW: fact-check the fixer's stated bias claim)
**Prompt (implicit; direct test of the fix's own caveat):** is restricting to complete-observation features in the SVA block really biased toward abundant, well-detected proteins, as the fix's comment claims — or is that just an assumed rationale?
**Code:** `runs/in7_sva_bias_check.R` on `data/proteinGroups.txt`.
```
complete features: 738 | incomplete (dropped) features: 762
dropped features with 0/8 detections: 55/762
mean log2 LFQ intensity: complete 25.24 vs dropped 23.46 (delta 1.78)
median detected-samples-per-feature (of 8): complete 8.0 vs dropped 6.0
Wilcoxon rank-sum: W=400251, p=3.74e-69
% of complete features above the whole-matrix median abundance: 69.0%
```
**Finding:** the stated bias is real, in the stated direction, with a large effect size and overwhelming significance — the fixer's caveat is not just plausible, it is empirically confirmed on this Skill's own synthetic data.
**Scores:** Basic 35 · Specialized 47 · **82**. Assertions 3/3.
*Note: first draft's aggregate `mean()` propagated `NaN` from 55 fully-undetected (0/8) dropped features; fixed with `na.rm=TRUE` and an explicit undetected-feature count, then re-run.*

## Research Veto (Category 2)
| Dimension | Result | Detail |
|---|---|---|
| M1 | PASS | No fabrication; all numbers from real runs this session. |
| M2 | PASS | No individual-level content. |
| M3 | PASS | Core methodological claims reproduced, including the new verification-gate and bias claims. |
| M4 | PASS | All 7 inputs ran to completion; no syntax errors, missing dependencies, or infinite loops (two bugs found and fixed were in this auditor's own test scripts, not the Skill). |

## Final arithmetic
Static 87 × 0.4 = **34.8** · Execution 86.6 × 0.6 = **52.0** · Final = **86.8 → 87** → **⭐ Production Ready**.

Floors (Production Ready): static ≥80 (87 ✓) · exec ≥85 (86.6 ✓) · L1 ≥32 (35.7 ✓) · L2 ≥48 (50.9 ✓) ·
assertions ≥90% (92.9% ✓). All floors clear. **Deployable: true** (supporting bar 75; clears with
large margin).

## Recommendations
- **[P2] Bridge-channel block doesn't inherit the soft imbalance warning** (Input 2) — real, execution-confirmed, residual gap; not severe enough to block deployment (design stays valid/estimable, just not optimally balanced) but should be fixed for parity with the primary block.
- **[P2] Balance-verification code shown only for the primary condition, not other covariates** (Input 1)
- **[P2] No OSAT code despite OSAT being named as a designit alternative**

## What changed vs the pre-fix audit
| Finding | Pre-fix | This re-audit |
|---|---|---|
| P1: SVA fails on matrices with missing values | Open | **Closed** — confirmed fixed and correctly characterized (Inputs 4, 7) |
| P2: No verification step after optimization | Open | **Closed** for the primary path — confirmed to be a real gate (Inputs 1, 6) |
| P2: No bridge/reference-channel layout | Open | **Mostly closed** — real code now exists and runs, but doesn't fully inherit the primary block's soft imbalance check (Input 2) |
