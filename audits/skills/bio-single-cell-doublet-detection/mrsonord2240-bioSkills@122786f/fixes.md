# bio-single-cell-doublet-detection fix pass

## Source

- Repository worktree: `F:\OpenScience\worktrees\bio-single-cell-doublet-detection-fixpass`
- Branch: `fix/bio-single-cell-doublet-detection-audit-20260924`
- Exact commit: `122786f78fef5de2a71fb2e8ec10388ad0f66d7c`
- Changed files: `single-cell/doublet-detection/SKILL.md`, `examples/doubletfinder.R`, and `usage-guide.md`
- Base: staging `openscience-fixes` at `9d31109159d4d490ec375d4ae88c9b77570f3840`

## Fixes

- Replaced Scrublet's view-based per-sample shorthand with copied subsets, explicit parent assignment, capture metadata validation, and an unscored-cell guard.
- Added deterministic scDblFinder worker seeding via `BiocParallel::SerialParam(RNGseed=...)` and documented why `set.seed()` alone is insufficient.
- Removed the invalid logical `reuse.pANN = FALSE` from the shipped DoubletFinder example and documented the actual `cannot xtfrm data frames` recovery.
- Attached ambient-RNA and dataset-wide-background qualification to the lineage co-expression heuristic.
- Added mandatory reporting fields for per-capture rate, method/seed/threshold, call count/percentage, and homotypic limitation.

## Exact-commit re-audit

- Final score: **94 / 100 — Production Ready**
- Assertions: **20 / 20 PASS**
- Focused executable validation: **15 / 15 PASS**
- Remaining P0/P1/P2 findings: none.

The focused run verifies the exact Git SHA, parses the changed Python fences, and executes the corrected Scrublet pooled-sample fence against two capture lanes from the audit fixture. It proves parent-column write-back, complete scoring, independent lane processing, and failure on missing capture metadata. scDblFinder and DoubletFinder fixes are source-checked against retained prior R execution evidence; the host has no `Rscript`, so no new R end-to-end run is claimed.

## Artifacts

- Canonical report: `F:\OpenScience\audits\bio-single-cell-doublet-detection\eval_report_bio-single-cell-doublet-detection_result.json`
- Canonical viewer: `F:\OpenScience\audits\bio-single-cell-doublet-detection\eval_viewer_bio-single-cell-doublet-detection.md`
- Focused test: `F:\OpenScience\audits\bio-single-cell-doublet-detection\run\exact-commit-122786f\reaudit_focused.py`
- Focused log: `F:\OpenScience\audits\bio-single-cell-doublet-detection\run\exact-commit-122786f\reaudit_focused.log`
- Report builder: `F:\OpenScience\audits\bio-single-cell-doublet-detection\run\exact-commit-122786f\build_reaudit_report.py`
