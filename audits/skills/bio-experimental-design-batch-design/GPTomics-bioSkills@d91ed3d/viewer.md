> **Audit record for `bio-experimental-design-batch-design`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/experimental-design/batch-design) (MIT).
> - Read from [mrsonord2240/bioSkills@575ab94](https://github.com/mrsonord2240/bioSkills/tree/575ab946989a7029d235eb0ab711e47b08edbcb0/experimental-design/batch-design), a fork in which this Skill's files are unchanged from upstream; the audited content is upstream's.
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-experimental-design-batch-design
Generated: 2026-09-15 · Auditor for round-2 candidate `mass-spec-proteomics-analyst` (supporting Skill) · skill-auditor@1.0

Source: `mrsonord2240/bioSkills@575ab946989a7029d235eb0ab711e47b08edbcb0:experimental-design/batch-design` (no fix applied; identical
to upstream d91ed3d). Files read: `SKILL.md` (189 lines), `usage-guide.md`, `examples/batch_design.R`.
Role: **supporting** (framing/design). Category **Protocol Design** · Mode A · Complexity **Moderate** (assignment, confounding
diagnosis, hidden-batch detection, correction choice; one example) → **N = 5**.
Environment: R 4.4.3, designit 0.5.1 (CRAN), sva 3.54.0, OSAT 1.54.0, limma 3.62.2 (installed into the candidate R-lib for this audit).
Three R blocks extracted byte-for-byte to `runs/blocks/`. **All designs and matrices SYNTHETIC**; Input 4 uses the shared synthetic MaxQuant table.

## Step 1 — Skill Veto
| Dimension | Result | Evidence |
|---|---|---|
| T1 Stability | PASS | All inputs ran; SVA stop on NA is an input requirement (1/5). |
| T2 Contract | PASS | Frontmatter complete. |
| T3 Determinism | PASS | Optimization is stochastic; the example seeds it; block b02 does not (P2 note in static score). |
| T4 Security | PASS | No eval/exec, network or credentials. |

## Step 2 — Static score: 81/100
| # | Criterion | Score | Note |
|---|---|---|---|
| 1.1 | Completeness | 3 | No OSAT code, no bridge-channel code. |
| 1.2 | Correctness | 4 | All tested claims reproduced. |
| 1.3 | Appropriateness | 3 | Sequencing-framed; LC-MS/TMT only in taxonomy. |
| 2.1 | Fault tolerance | 2 | No NA guard, no balance check. |
| 2.2 | Error reporting | 2 | Common Errors conceptual. |
| 2.3 | Recoverability | 3 | Re-run with corrected inputs. |
| 3.1 | Token cost | 4 | 189 lines. |
| 3.2 | Execution efficiency | 3 | Default optimization 154 s on 64 positions. |
| 4.1 | Learnability | 3 | API-drift caveats. |
| 4.2 | Consistency | 4 | Consistent. |
| 4.3 | Feedback design | 2 | No verify-the-layout step. |
| 4.4 | Error prevention | 4 | Confounding, unbalanced ComBat, SV subtraction, collider. |
| 5.1 | Discoverability | 4 | Natural trigger phrasing. |
| 5.2 | Forgiveness | 3 | (Cat-2 override) strict inputs acceptable. |
| 6.1 | Credential safety | 4 | None. |
| 6.2 | Input validation | 3 | Relies on designit/sva checks. |
| 6.3 | Data safety | 4 | Metadata guidance only. |
| 7.1 | Modularity | 3 | Sections by task. |
| 7.2 | Modifiability | 3 | Independent blocks. |
| 7.3 | Testability | 3 | Runnable example. |
| 8.1 | Trigger precision | 3 | Genomics wording under-triggers for proteomics. |
| 8.2 | Progressive disclosure | 3 | Routes out. |
| 8.3 | Composability | 4 | Routes to batch-correction, randomization-blocking. |
| 8.4 | Idempotency | 3 | Unseeded optimization in block. |
| 8.5 | Escape hatches | 4 | Redesign stop condition. |

Functional 10 · Reliability 7 · Performance 7 · Agent usability 13 · Human 7 · Security 11 · Maintainability 9 · Agent-specific 17 = **81**.

**Gate 8: PASS** — no `references/`/`scripts/` pointers; `examples/batch_design.R` exists.
**Example smoke test** (`runs/smoke.out`): exit 0; confounded table 12/0 vs 0/12, balanced 4/4/4; SVA found 1 SV; PC1-vs-batch correlation 0.48 → 0.01 after ComBat (for plots only).

## Summary Table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 36 | 50 | 86 | 5/5 | yes | ✅ |
| 2 | Variant A | 33 | 44 | 77 | 2/4 | yes | ✅ |
| 3 | Edge | 37 | 55 | 92 | 4/4 | yes | ✅ |
| 4 | Variant B | 30 | 39 | 69 | 2/4 | yes | ⚠️ |
| 5 | Stress | 37 | 55 | 92 | 4/4 | yes | ✅ |

**Execution Average: 416/5 = 83.2** · **Assertions 17/21 (81.0%)** · L1 avg 34.6 · L2 avg 48.6

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "We're running 24 plasma samples (12 cases, 12 controls, half male) on the LC-MS in 3 batches of 8. How should I assign samples to batches so batch doesn't wreck the comparison?"
**Code:** `runs/in1_designit.R` (block b02 verbatim).
```
[designit block verbatim] OK | designit 0.5.1
condition x batch:  ctrl 4 4 4 | treat 4 4 4
sex x batch:        F 4 4 4 | M 4 4 4
empty positions: 0
```
**Scores:** Basic 36 · Specialized 50 (design 18; evidence 12; method combination 8; validation 8; publication 4) · **86**. Assertions 5/5.

### Input 2 — Variant A
**Prompt:** "60 plasma samples (30 case / 30 control, 3 collection sites) across 4 TMTpro 16plex runs. We want a pooled reference in the last channel of every plex. Give me the plex/channel layout."
**Code:** `runs/in2_tmt_plex.R` — agent adapts b02 with `BatchContainer$new(dimensions = list(plex = 4, channel = 16), exclude = channel 16)`.
```
Achieved score: 6 at iteration 78 | elapsed s: 154
condition x plex:  case 7 7 7 9 | ctrl 8 8 8 6
site x plex:       A 4 5 6 5 | B 5 5 5 5 | C 6 5 4 5
reference channel 16 occupied by a sample: FALSE | positions per plex used: 15,15,15,15
```
**Scores:** Basic 33 · Specialized 44 (design 15; evidence 12; method 7; validation 6; publication 4) · **77**. Assertions 2/4.

### Input 3 — Edge
**Prompt:** "Our study is already run: all 8 cases were digested and injected on day 1, all 8 controls on day 2. Can we fix it with ComBat and still publish the comparison?"
**Code:** `runs/in3_confounded_rescue.R`.
```
ComBat with condition covariate ERROR: The covariate is confounded with batch! Remove the covariate and rerun ComBat
ComBat without covariate, then limma: calls 0 | true hits among them 0 | nulls 0
no correction (condition = day): calls 346 | true 67 | nulls (pure day effect) 279
limma ~cond + day on the confounded design: Partial NA coefficients for 1000 probe(s) (dayD2 not estimable)
```
**Response:** no correction can separate day from condition; re-run a balanced subset or a new balanced batch; any existing comparison is labelled confounded.
**Scores:** Basic 37 · Specialized 55 · **92**. Assertions 4/4.

### Input 4 — Variant B
**Prompt:** "Our MaxQuant LFQ matrix clusters oddly on PCA and we don't have processing dates. Can you check for hidden batches with SVA?"
**Code:** `runs/in4_sva_proteomics.R` (block b03 verbatim).
```
--- as imported (NA present): 1500 x 8, NA 2120
[SVA block verbatim] ERROR: infinite or missing values in 'x'
--- complete cases: 738 x 8, NA 0
[SVA block verbatim] OK | n_sv: 1 | cor(SV1, day B2): 1
```
**Scores:** Basic 30 · Specialized 39 (design 13; evidence 11; method 6; validation 5; publication 4) · **69**. Assertions 2/4.

### Input 5 — Stress
**Prompt:** "Our 24 samples ended up unbalanced across three batches (8/2, 3/3, 1/7 case/control). The core ran ComBat and sent us the cleaned matrix for limma. Is that OK, or should we do something else?"
**Code:** `runs/in5_unbalanced_combat.R` (20 seeds).
```
  combat_calls 89.15 | combat_fp 29.55 | combat_nullp05 0.140
  model_calls  59.05 | model_fp  2.70  | model_nullp05  0.048
realized FDR (pooled over 20 seeds): ComBat-then-test 33.1% | batch in model 4.6%
```
**Scores:** Basic 37 · Specialized 55 · **92**. Assertions 4/4.

## Research Veto (Category 2)
| Dimension | Result | Detail |
|---|---|---|
| M1 | PASS | No fabrication; references real. |
| M2 | PASS | No individual-level content. |
| M3 | PASS | Core methodological claims reproduced. |
| M4 | PASS | designit and sva blocks ran; NA requirement filed P1. |

## Final arithmetic
Static 81 × 0.4 = **32.4** · Execution 83.2 × 0.6 = **49.9** · Final 82.3 → **82** → **✅ Limited Release**.
Floors (LR): static 81 ✓ · exec 83.2 ✓ · L1 34.6 ✓ · L2 48.6 ✓ · assertions 81.0% ✓. **Deployable: true** (supporting bar 75).

## Recommendations
- **[P1] SVA block fails on matrices with missing values** (Input 4)
- **[P2] No verification step after optimization** (Input 2)
- **[P2] Bridge/reference channel layout not shown** (Input 2)
