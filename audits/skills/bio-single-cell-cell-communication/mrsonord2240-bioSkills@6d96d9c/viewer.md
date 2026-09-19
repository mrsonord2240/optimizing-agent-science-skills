> **Audit record for `bio-single-cell-cell-communication`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6d96d9c](https://github.com/mrsonord2240/bioSkills/tree/6d96d9c0c90124466fdecd0694b0bfd1dc177b07/single-cell/cell-communication) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-cell-communication (RE-AUDIT, fix pass follow-up)

Generated: 2026-09-19
Auditor: re-auditor (third agent — different from both the original auditor and the fixer)
Source: `mrsonord2240/bioSkills@6d96d9c0c90124466fdecd0694b0bfd1dc177b07:single-cell/cell-communication`
Worktree: `F:\OpenScience\wt\sc-cellcomm`, branch `fix/sc-cell-communication` — confirmed clean, HEAD == 6d96d9c
Prior audit: `F:\OpenScience\audits\_pre-fix-20260919\bio-single-cell-cell-communication\` (score 86, Limited Release, 2026-09-19)
Fix log (claim, not evidence): `F:\optimizing-agent-science-skills\fixes\bio-single-cell-cell-communication.md`

## How this re-audit was run

Per `AUDIT_BRIEF.md`'s "Re-auditing a fixed Skill": the 3 originally real-executed inputs (LIANA canonical,
CellPhoneDB specificity, LIANA single-group edge) were re-run as regressions, independently, in fresh
processes, reusing only the *static* real-data inputs from the pre-fix audit (`data/adata_annotated.h5ad`,
`run/counts_normalized.h5ad`, `run/meta.tsv`, `run/cpdb_db/`) — never the fixer's or original auditor's
*saved outputs*. Two brand-new inputs were added: the Resource-Sensitivity Check section (never executed by
any prior audit) and an independently-constructed Condition Comparison null-case test. The CellPhoneDB
determinism claim was checked against the full 120,375-cell result matrix, not a spot check, and cross-checked
against a threads=1 isolation run to pin down root cause.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 2 | Variant A — CellPhoneDB (regression + new determinism deep-dive) | 33 | 45 | 78 | 4/5 PASS | ✅ |
| 3 | Edge — single group (regression) | 36 | 55 | 91 | 3/3 PASS | ✅ |
| 4 | Variant B — NicheNet (carried over, unaffected by fix) | 34 | 47 | 81 | 4/4 PASS | ✅ |
| 5 | Stress — Condition Comparison (own null-case split, NEW) | 33 | 44 | 77 | 4/5 PASS | ✅ |
| 6 | Scope Boundary — spatial (carried over, unaffected) | 37 | 55 | 92 | 4/4 PASS | ✅ |
| 7 | Adversarial — mouse CellPhoneDB (carried over, unaffected) | 37 | 56 | 93 | 4/4 PASS | ✅ |
| 8 | Resource-Sensitivity Check (NEW, never tested before) | 37 | 56 | 93 | 4/4 PASS | ✅ |

**Execution Average: 87.5 / 100**
**Assertion Pass Rate: 31/33 (93.9%)**

> Note for reviewer: Input 2 and Input 5 are the ones to read closely — both reveal a real gap between what
> the fix log claims and what this re-audit's own fresh runs found. Neither rises to a P0 or veto (code runs,
> no crash, no fabrication), but both are genuine, currently-undocumented defects.

## Detailed Outputs

### Input 1 — Canonical (regression)
**Prompt:** "Run LIANA rank_aggregate and report both magnitude and specificity ranks" (SKILL.md's Consensus
Inference block, unmodified, on real annotated PBMC 1k v3 data).
**Output:** 31,812 total pairs, 1,122 robust pairs (specificity_rank<0.05 & magnitude_rank<0.05). Top hits:
`S100A9-ITGB2` (Classical monocytes -> CD16+ NK), `B2M-KLRD1` (multiple T/NK sources -> CD16+ NK, NK inhibitory
checkpoint), `S100A8-ITGB2`. Exact match to the pre-fix audit's original run, reproduced in a fresh, independent
process. This section was not touched by the fix.
**Scores:** Basic: 38/40 | Specialized: 57/60 | Total: 95/100
**Assertions:** all 4 PASS — see JSON for text/notes.

### Input 2 — Variant A: CellPhoneDB v5 specificity (regression + new determinism deep-dive)
**Prompt:** "Run CellPhoneDB with permutation p-values and proper complex handling" (SKILL.md's now-guarded,
now-seeded Specificity Test block, unmodified, twice independently).
**Output:**
- Run 1 and Run 2 both completed with **no crash** (the pre-fix P1 crash is genuinely fixed). Shapes (535, 238)
  as documented.
- Real biology confirmed in fresh output: `HLA-E_VSIR`, `HLA-F_LILRB1` (inhibitory checkpoints),
  `ICAM2/3_integrin_aLb2` (LFA-1 adhesion), `CD58_CD2`, `CD47_SIRPG`, `PPIA_BSG`.
- **Full-matrix determinism check** (`run/04_compare_cpdb_determinism.py`), comparing the entire 535×225
  pvalues matrix (120,375 cell-pair × interaction values) between the two fresh runs at the exact documented
  parameters (`debug_seed=1337, threads=4, iterations=1000`):
  ```
  FULL_PVALUE_MATRIX_BIT_IDENTICAL: False
  n_differing_cells 5150 of 120375
  max_abs_diff 0.07499999999999996
  SIGNIFICANCE_FLAGS_FLIPPED: 82   (of 120,375, at p<0.05)
  ```
  This is a real improvement over the pre-fix audit's unseeded baseline (252/120,375 flipped) but directly
  contradicts the fix log's and SKILL.md's own Permutation Rationale table's claim of full reproducibility.
- **Root-cause isolation** (`run/05a`/`05b_cpdb_threads1_run*.py`): repeating the identical seeded call at
  `threads=1` (the fixer's actual verification setting per the fix commit message, which states
  "iterations=100, threads=1") reproduces the fix log's claim exactly:
  ```
  threads=1 bit-identical: True
  n differing 0 of 120375
  ```
  **The non-determinism is specific to the `threads=4` multiprocessing path that SKILL.md's shipped code block
  actually uses.** The fixer verified determinism at a thread count the documented code does not run at.
**Scores:** Basic: 33/40 | Specialized: 45/60 | Total: 78/100
**Assertions:** 4/5 PASS — the reproducibility assertion FAILs; see JSON for full text.

### Input 3 — Edge: single-group groupby (regression)
**Prompt:** "Run CCC with only one cell-type group present."
**Output:** `ValueError: Cannot compute log2FC for group 'all_cells': every cell belongs to it, leaving no
cells to compare against...` — reproduced fresh, independently. SKILL.md's corrected sentence ("a single
group raises a `ValueError` (log2FC has no comparison group), not a silent autocrine-only result") now
matches this verbatim. The pre-fix audit's P2 finding is genuinely fixed.
**Scores:** Basic: 36/40 | Specialized: 55/60 | Total: 91/100
**Assertions:** all 3 PASS.

### Input 4 — Variant B: NicheNet (carried over, not re-executed)
**Prompt:** "Which Monocyte ligand best explains activated-vs-naive CD8 T cell DE genes?"
**Output:** Not re-executed. `git diff` of commit `6d96d9c` (`git show --stat HEAD`) confirms only
`SKILL.md` (+65/-0 mixed) and `usage-guide.md` (-39) changed, and reading the diff shows the NicheNet section's
R code and prose are byte-identical pre- and post-fix. nichenetr remains an unbuildable GitHub-only package on
this Windows box (TOOLS.md batch-7 log, RcppPlanc compile failure). Static-API-inspection conclusions from the
pre-fix audit stand, confirmed not to have regressed.
**Scores:** Basic: 34/40 | Specialized: 47/60 | Total: 81/100 (carried forward unchanged)
**Assertions:** all 4 PASS (unchanged).

### Input 5 — Stress: Condition Comparison, re-auditor's own null-case split (NEW methodology)
**Prompt:** "Compare cell communication between two conditions and show gained/lost interactions" — using the
Skill's brand-new Condition Comparison section.
**Why a null-case split, not the fixer's:** the real PBMC 1k v3 data has no genuine experimental conditions
(single sample). The fixer's own demo used an arbitrary 50/50 split with no stated rationale and no way to
tell whether the observed 409 gained / 70 lost pairs reflected real structure or pure noise. A skeptical
re-audit needs a split where the *ground truth* is known: stratifying by `cell_type` (preserving per-type
composition) and randomly assigning cells 50/50 within each type (seed `20260919`, different from the
fixer's) gives two "conditions" with, by construction, **no true biological difference**.
**Output:** Ran end-to-end with zero errors: conditionA 555 cells / 827 robust pairs, conditionB 558 cells /
864 robust pairs.
```
NULL_CASE_GAINED 154
NULL_CASE_LOST 117
NULL_CASE_SHARED 710
NULL_CASE_UNION 981
FRACTION_OF_UNION_THAT_IS_GAINED_OR_LOST: 0.276
```
Even under a true null, 27.6% of the robust-pair union is flagged gained or lost — comparable in scale to the
fixer's own (non-null, uncontrolled) 409/1,527≈27% demo. SKILL.md gives no warning that a similar fraction of
any real gained/lost call could be sampling noise from the halved per-condition cell count, and recommends no
stability check (bootstrap, repeat-split, or minimum cell count).
**Scores:** Basic: 33/40 | Specialized: 44/60 | Total: 77/100
**Assertions:** 4/5 PASS — the noise-distinguishability assertion FAILs; see JSON.

### Input 6 — Scope Boundary: Visium spatial data (carried over, not re-executed)
**Output:** `git diff` confirms the Spatial-Aware Methods table is byte-identical pre- and post-fix. Mode A
reasoning output, no code to run. Conclusions unchanged.
**Scores:** Basic: 37/40 | Specialized: 55/60 | Total: 92/100 (carried forward unchanged)
**Assertions:** all 4 PASS (unchanged).

### Input 7 — Adversarial: mouse CellPhoneDB (carried over, not re-executed)
**Output:** `git diff` confirms the Method Decision Table's mouse-DB row and the Common Errors table row are
byte-identical pre- and post-fix. Mode A reasoning output, no code to run. Conclusions unchanged.
**Scores:** Basic: 37/40 | Specialized: 56/60 | Total: 93/100 (carried forward unchanged)
**Assertions:** all 4 PASS (unchanged).

### Input 8 — Resource-Sensitivity Check (NEW — never executed by any prior audit)
**Prompt:** "Re-run the same method with the CellPhoneDB and CellChat resources and show which pairs are
stable" (SKILL.md's Resource-Sensitivity Check block, unmodified).
**Output:** This section existed in the pre-fix Skill but neither the original audit nor the fix log ever ran
it. Ran clean on first try across all three named resources:
```
consensus   n_pairs 31812  n_significant 12948
cellphonedb n_pairs  6708  n_significant  3035
cellchatdb  n_pairs  7609  n_significant  3601
SURVIVE_ALL_3_RESOURCES 930
```
Sample surviving pairs: `HLA-C_KIR2DL3` (NK inhibitory checkpoint), `CD40LG_ITGA5_ITGB1` (T-cell
costimulation), `GAS6_MERTK` (efferocytosis), `CCL4_CCR5` (chemokine), `SEMA4D_PLXNB2` (semaphorin).
All real, well-characterized immune biology; no spurious or nonsensical pairs in the surviving set.
**Scores:** Basic: 37/40 | Specialized: 56/60 | Total: 93/100
**Assertions:** all 4 PASS.

## Redundancy pass check

Verified `usage-guide.md` post-fix now holds only Overview, Quick Start, Example Prompts, and Related Skills
(51 lines, down from a longer pre-fix version). Confirmed against `SKILL.md`:
- Prerequisites (pip/R install commands) now live in SKILL.md's own `## Prerequisites` section, matching the
  fix log's claim.
- No remaining "What the Agent Will Do" / "Tips" duplication found.
- **One remaining redundancy the fix's "mandatory every fix" pass did not catch:** the 8-line "Related Skills"
  block is duplicated verbatim in both `SKILL.md` (lines ~245–254) and `usage-guide.md` (lines ~42–50). Logged
  as a P2 recommendation, not blocking.

## Veto gates

**Skill Veto:** T1 Stability PASS (zero crashes across all 6 freshly-executed inputs, including two dual-run
CellPhoneDB determinism checks and the null-case Condition Comparison). T2 Contract PASS (frontmatter intact).
T3 Determinism PASS — the CellPhoneDB threads=4 non-determinism is real but narrow (82/120,375 = 0.068% of
calls, confined to marginal near-0.05 p-values; deep/robust hits at p=0 remain stable in both runs) and IS
seed-controlled (unlike the pre-fix unseeded baseline) — this does not meet the T3 FAIL bar of "no seed
management" or "critical numerical results fluctuate randomly", but it is flagged as the top P1. T4 Security
PASS.

**Research Veto** (Category 3 — Data Analysis, applicable): all four dimensions PASS. See JSON `veto_gates`
for full detail strings, including the methodological_ground discussion of the Condition Comparison noise gap
(judged a completeness gap, not an active fallacy).

## Final Score

```
Static Score   : 87/100  × 40% = 34.8
Dynamic Score  : 87.5/100 × 60% = 52.5
FINAL SCORE    : 87 / 100
GRADE          : ⭐ Production Ready
Deployable     : true
Veto override  : false
```

Floors (Production Ready): Static ≥80 (87 ✓) · Execution ≥85 (87.5 ✓) · L1 avg ≥32 (35.6 ✓) · L2 avg ≥48
(51.9 ✓) · Assertion pass rate ≥90% (93.9% ✓). All clear.
