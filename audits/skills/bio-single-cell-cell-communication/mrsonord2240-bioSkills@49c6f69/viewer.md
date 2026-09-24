> **Audit record for `bio-single-cell-cell-communication`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@49c6f69](https://github.com/mrsonord2240/bioSkills/tree/49c6f6943243f8faebc9848429c877be240d10d6/single-cell/cell-communication) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-cell-communication (Final Pass, Phase 2)

## Canonical final summary

**Final:** 94/100 — ⭐ Production Ready; deployable: true.

Generated: 2026-09-23

Exact source: mrsonord2240/bioSkills@49c6f6943243f8faebc9848429c877be240d10d6:single-cell/cell-communication

Final-pass metadata: `auditor_independent: false`; `final pass: fixed and audited under one brief, see CHECKPOINT.md`.

Worktree: F:\OpenScience\wt\single-cell-cell-communication on fix/single-cell-cell-communication.

Audit metadata: auditor_independent: false; final pass fixed and audited under one brief, see CHECKPOINT.md.

Prior audit preserved intact: F:\OpenScience\audits\_pre-fix-20260923\bio-single-cell-cell-communication.

## Outcome

94/100 — Production Ready — deployable: true — no veto.

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Executed |
|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical LIANA consensus | 38 | 57 | 95 | 4/4 | yes |
| 2 | Exact CellPhoneDB dual run | 38 | 58 | 96 | 5/5 | yes |
| 3 | Single-group edge | 37 | 57 | 94 | 3/3 | yes |
| 4 | Known-null condition stability | 38 | 57 | 95 | 5/5 | yes |
| 5 | Resource sensitivity | 37 | 57 | 94 | 4/4 | yes |
| 6 | Spatial scope boundary | 37 | 56 | 93 | 4/4 | yes, direct mode |
| 7 | Mouse resource boundary | 37 | 57 | 94 | 4/4 | yes |
| 8 | CellChat/NicheNet R branches | 33 | 50 | 83 | 4/5 | yes — parse/availability probe; dependencies absent |

Execution average: 93.0/100. Assertion rate: 33/34 (97.1%).

Static: 96/100. Final: 96 × 0.4 + 93.0 × 0.6 = 94.2, rounded to 94.

## Fresh evidence

Every fresh script and log is in run/phase2_20260923. The Python tool environment recorded liana 1.10.0, cellphonedb 5.0.1, scanpy 1.12.4, anndata 0.13.4, pandas 2.3.3, and numpy 2.5.3.

### 1. Consensus inference

The fresh real-PBMC 1k execution with 1,000 permutations wrote canonical_all_pairs.csv and canonical_robust_pairs.csv:

    TOTAL_PAIRS 31812
    ROBUST_PAIRS 1122

Both magnitude_rank and specificity_rank were asserted. The leading robust candidates included S100A9-ITGB2 and B2M-KLRD1.

### 2. Exact CellPhoneDB script

The exact current source CLI was invoked twice with 1,000 iterations, threads=1, and seed=1337:

    cpdb_run1 EXIT 0
    cpdb_run2 EXIT 0
    PVALUES_SHAPE (535, 238)
    BIT_IDENTICAL_THREADS1 True
    SIGNIFICANCE_FLAG_FLIPS 0

Both runs produced all expected result tables. This verifies the exact Windows main guard and the documented single-thread reproducibility constraint.

### 3. One-group edge

    EXPECTED_VALUE_ERROR
    Cannot compute log2FC for group 'all_cells': every cell belongs to it, leaving no cells to compare against.

The current Skill’s corrected explanation matches the actual behavior.

### 4. Condition-comparison stability

A fresh stratified random control/stimulated split was constructed within cell type on the real PBMC data. It has no biological effect by construction. The exact current condition_stability.py then ran at documented defaults: ten null permutations and 1,000 LIANA permutations.

    real gained+lost: 297 | null median: 306.0 range: 222 356
    noise-prone pairs: 196 of 297
    real count is inside the null range: not evidence of a condition effect

The saved TSV contains direction, pair identity, null frequency, and noise_prone for all 297 apparent gained/lost pairs. The workflow correctly avoids treating this known-null difference as biology.

### 5. Resource sensitivity

    consensus PAIRS 31812 SIGNIFICANT 12948
    cellphonedb PAIRS 6708 SIGNIFICANT 3035
    cellchatdb PAIRS 7609 SIGNIFICANT 3601
    SURVIVE_ALL_THREE 930

All three current source-named resources ran and yielded material outputs.

### 6–7. Boundaries

The fresh direct-mode spatial answer is saved as 06_spatial_scope_response.md. It requires deconvolution for Visium, names spatial methods, and preserves the co-expression/proxy boundary. Mouse routing was executed:

    MOUSECONSENSUS_ROWS 3989
    COLUMNS ['ligand', 'receptor']

### 8. R-only branches

Fresh designated-R parsing passed:

    PARSE_OK cellchat.md
    PARSE_OK nichenet.md
    PARSE_OK cellchat_analysis.R
    CELLCHAT_AVAILABLE FALSE
    NICHENETR_AVAILABLE FALSE

The R workflows were not executed or credited as live results. This is a stated environment-evidence limitation, not a fabricated pass.

## Gates and issues

Skill Veto: stability, contract, determinism, and security all PASS. Research Veto: scientific integrity, practice boundaries, methodological ground, and code usability all PASS.

- P0: none.
- P1: CellChat and NicheNet need live verification in a supported isolated R environment.
- P2: condition_stability.py should preflight its two-condition input contract before expensive fitting.

See eval_report_bio-single-cell-cell-communication_result.json for per-input assertions, execution flags, notes, scoring, and recommendations.
