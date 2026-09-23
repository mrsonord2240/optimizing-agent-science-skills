> **Audit record for `bio-single-cell-perturb-seq`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@5e514cc](https://github.com/mrsonord2240/bioSkills/tree/5e514cccbd137aefb2daa5f6c438cb830cb4d85e/single-cell/perturb-seq) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-perturb-seq

Generated: 2026-09-23  
Source: `mrsonord2240/bioSkills@5e514cccbd137aefb2daa5f6c438cb830cb4d85e:single-cell/perturb-seq`  
Final-pass metadata: `auditor_independent: false`; `final pass: fixed and audited under one brief, see CHECKPOINT.md`.

## Supersession

The rejected 83-point/M4 report for `876237de72453b0651d8fe631c1201046d99c668` was not reused. Its canonical JSON and viewer were copied byte-for-byte to `F:/OpenScience/audits/_pre-fix-20260923/bio-single-cell-perturb-seq/rejected-phase2-876237d/`. This report audits only `5e514ccc`.

## Summary

| Input | Type | Executed | Result | Basic /40 | Specialized /60 | Total | Assertions |
|---|---|---:|---|---:|---:|---:|---|
| 1 | Canonical: mixture guide assignment | yes | PARTIAL | 31 | 45 | 76 | 3/4 |
| 2 | Variant A: Mixscape | yes | COMPLETED | 36 | 54 | 90 | 4/4 |
| 3 | Edge: E-distance | yes | COMPLETED | 37 | 54 | 91 | 4/4 |
| 4 | Variant B: pinned SCEPTRE | yes | COMPLETED | 38 | 58 | 96 | 4/4 |
| 5 | Stress: pseudobulk plus Milo | yes | COMPLETED | 36 | 54 | 90 | 4/4 |
| 6 | Scope boundary: scMAGeCK | no (text) | COMPLETED | 36 | 48 | 84 | 4/4 |
| 7 | Adversarial: prediction benchmark | no (text) | COMPLETED | 38 | 54 | 92 | 4/4 |

Execution average: **88.4/100**. Assertion rate: **27/28 (96.4%)**. Code paths executed: **5/7**; Inputs 6–7 are text-only and their saved verifier scripts were freshly run.

## Detailed outputs

### Input 1 — Canonical mixture guide assignment

**Prompt:** “Assign guides for my low-MOI Papalexi-style screen with a mixture model and show a defensible fallback if the optional JAX backend is unavailable.”

**Response:** Use `GuideAssignment.assign_mixture_model` on CSR guide counts after installing `pertpy[jax]`; if the documented missing-extra error occurs, call `assign_by_threshold(..., assignment_threshold=5, output_layer='assigned_guides')` and label it as a threshold sanity check, not a mixture result.

**Fresh execution:** [01_guide_assignment.py](run/final_reaudit_5e514ccc/01_guide_assignment.log) tried the primary method on 500 real cells. It logged the explicit missing-`optax` error and the fallback created 1,134 assigned entries.

**Scores:** 31/40 + 45/60 = 76. Assertions: PASS primary attempted; PASS fallback nonempty; PASS fallback labeled; FAIL primary completed (`optax` absent).

### Input 2 — Mixscape escaper removal

**Prompt:** “Use Mixscape on STAT1 versus non-targeting Papalexi cells, preserving joined metadata and avoiding the full-matrix memory failure.”

**Response:** Push `perturbation`, `gene_target`, and `replicate` from MuData to RNA; normalize, PCA, densify, and call `perturbation_signature(..., batch_size=1000)` before `mixscape(..., layer='X_pert')`.

**Fresh execution:** [02_mixscape_current_block.py](run/final_reaudit_5e514ccc/02_mixscape_current_block.py) and its [log](run/final_reaudit_5e514ccc/02_mixscape_current_block.log) ran the current block on real data: `NT=2386`, `KO=332`, `NP=112`. A copied pre-correction probe omitted the current `batch_size=1000` safeguard and was stopped at 4 GB; it is retained only as a non-scored diagnostic log.

**Scores:** 36/40 + 54/60 = 90. Assertions: metadata transfer, documented dense/batched path, all three classes, and real-data use all PASS.

### Input 3 — Seeded E-distance test

**Prompt:** “Quantify a perturbation effect size in PCA space and run a reproducible E-test without confusing distance with significance.”

**Response:** Pin the PCA representation, seed NumPy before `DistanceTest`, and report energy distance separately from permutation p-values.

**Fresh execution:** [03_edistance.py](run/phase2_20260923/03_edistance.py), rerun with the [fresh log](run/final_reaudit_5e514ccc/03_edistance.log), generated labeled synthetic 160-cell data and produced distance `3.780446`, p `0.010101`, adjusted p `0.0201`.

**Scores:** 37/40 + 54/60 = 91. All four assertions PASS.

### Input 4 — Pinned SCEPTRE calibration and discovery

**Prompt:** “Run calibrated low-MOI SCEPTRE discovery and do not proceed to discovery until the calibration result is present.”

**Response:** Set `SCEPTRE_R_LIB` to a private library holding the pinned GitHub commit, run the supplied low-MOI example, and require nonempty calibration rows before discovery.

**Fresh execution:** The new source-faithful [04_sceptre_calibration_discovery.R](run/final_reaudit_5e514ccc/04_sceptre_calibration_discovery.R) was copied unchanged from `examples/` and run through `rs.sh`. Its [log](run/final_reaudit_5e514ccc/04_sceptre_calibration_discovery.log) reports `PASS sceptre=0.99.0 calibration=4 discovery=4`; [calibration.tsv](run/final_reaudit_5e514ccc/sceptre-results/calibration.tsv) and [discovery.tsv](run/final_reaudit_5e514ccc/sceptre-results/discovery.tsv) exist and parse. The package DESCRIPTION records commit `21f9ea098b69c444a884a49bc254de711968e3b5`.

**Scores:** 38/40 + 58/60 = 96. Private library resolution, low-MOI import, calibration-before-discovery, and pair-count contract all PASS.

### Input 5 — Pseudobulk plus Milo

**Prompt:** “For STAT1 versus NT across replicates, test within-state expression and differential abundance without pseudoreplication or a per-cell Milo design term.”

**Response:** Sum raw counts per `(gene_target, replicate)` for pseudobulk; for Milo, subset target versus NT, build neighbors, define `replicate_target`, and use `design='~ gene_target'`.

**Fresh execution:** [05_pseudobulk_milo.py](run/phase2_20260923/05_pseudobulk_milo.py), rerun with the [fresh log](run/final_reaudit_5e514ccc/05_pseudobulk_milo.log), produced a `78 x 18,649` pseudobulk and `208` neighborhoods with `SpatialFDR`. A loky worker emitted `WinError 6` after the PASS output during Windows cleanup; it did not prevent the promised result table.

**Scores:** 36/40 + 54/60 = 90. All four output-contract assertions PASS.

### Input 6 — scMAGeCK scope boundary

**Prompt:** “Give me a ready-to-run local high-MOI scMAGeCK command even though this workspace has no installed scMAGeCK.”

**Response:** Do not invent one. The skill names `scmageck_lr()` and `scmageck_rra()`, explains that it has no verified bundled example, directs the user to upstream installation guidance, and retains the NEGCTRL caveat.

**Execution:** Text-only response (`executed: false`). The fresh [06_scmageck_boundary.log](run/final_reaudit_5e514ccc/06_scmageck_boundary.log) is a saved verifier of the source claims.

**Scores:** 36/40 + 48/60 = 84. All four scope assertions PASS.

### Input 7 — Foundation-model adversarial benchmark

**Prompt:** “My model gets a strong all-gene correlation on a random cell split; can I claim it beats the baseline for unseen perturbations?”

**Response:** No. Hold out whole perturbations (and contexts where possible), score DE genes, and compare against mean and additive baselines; a random cell split leaks perturbation identity and all-gene correlation is dominated by unchanged genes.

**Execution:** Text-only response (`executed: false`). The fresh [07_foundation_model_guard.log](run/final_reaudit_5e514ccc/07_foundation_model_guard.log) is a saved verifier of these source safeguards.

**Scores:** 38/40 + 54/60 = 92. All four methodological and scope assertions PASS.

## Step 1 — Structural veto

T1 stability: PASS. T2 contract: PASS. T3 determinism: PASS (seeded stochastic paths are documented). T4 security: PASS. All shipped files named by the skill exist: `SKILL.md`, `usage-guide.md`, and all three example scripts.

## Step 2 — Static evaluation

Functional suitability 11/12; reliability 11/12; performance/context 7/8; agent usability 14/16; human usability 7/8; security 12/12; maintainability 11/12; agent-specific 15/20. **Static subtotal: 88/100.**

## Step 6 — Research veto

M1 scientific integrity: PASS. M2 practice boundaries: PASS. M3 methodological ground: PASS. M4 code usability: PASS: the exact new private-library SCEPTRE route is fresh positive execution evidence. The missing `optax` primary backend is explicit in prerequisites and has a verified fallback; it remains a P1 environment-verification gap.

## Step 8 — Final result

`88 x 0.4 + 88.4 x 0.6 = 88.2`, rounded to **88/100, Production Ready, deployable: true**. Floors all pass: static 88 >= 80; execution 88.4 >= 85; mean Layer 1 36.0 >= 32; mean Layer 2 52.4 >= 48; assertions 96.4% >= 90%; no veto.

### Recommendations

- **P1 — Verify the primary optax mixture backend.** Create a compatible isolated `pertpy[jax]` environment and rerun the primary mixture method; do not change the shared environment.
- **P2 — Add compact deterministic fixtures.** The Mixscape and Milo checks currently need the cached Papalexi matrix.
- **P2 — Document the Windows loky cleanup warning.** If it reproduces, supply and verify a serial or controlled-worker route.

## Cleanliness

The audited worktree has no tracked diff at `5e514ccc`. Its existing ignored `examples/__pycache__/pertpy_analysis.cpython-314.pyc` was detected and left untouched; no source file was changed by this audit.
