> **Audit record for `bio-single-cell-doublet-detection`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@122786f](https://github.com/mrsonord2240/bioSkills/tree/122786f78fef5de2a71fb2e8ec10388ad0f66d7c/single-cell/doublet-detection) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-doublet-detection

## Exact-commit re-audit

| Source commit | Re-audited | Scope | Result |
|---|---|---|---|
| `122786f78fef5de2a71fb2e8ec10388ad0f66d7c` | 2026-09-24 | All prior P1/P2 findings | 15/15 focused assertions PASS |

The five-input audit fixture evidence is retained. This re-audit executes the corrected Scrublet pooled-sample fence directly from the exact committed `SKILL.md`, while verifying the seed, example, ambient-caveat, and reporting repairs from source. The host has no `Rscript`, so a new scDblFinder/DoubletFinder end-to-end run is not claimed.

## Scores

| Dimension | Score |
|---|---:|
| Static quality | 96 / 100 |
| Dynamic execution | 92.6 / 100 |
| Assertions | 20 / 20 PASS |
| Final | **94 / 100 — Production Ready** |

## Re-audit evidence

`run/exact-commit-122786f/reaudit_focused.py` verifies the checked-out SHA before loading the source and passes all 15 assertions:

- Scrublet’s copied-subset loop writes both output columns back to the parent for two capture lanes, with no missing scores.
- Missing capture metadata causes an actionable `ValueError`, rather than an unscored continuation.
- The recommended scDblFinder path has `SerialParam(RNGseed=...)` and documents why `set.seed()` is insufficient.
- The DoubletFinder example omits the invalid logical `reuse.pANN`; its known error now has the correct recovery action.
- Ambient-aware co-expression caution and required report fields are in the main decision path.

The log is at `run/exact-commit-122786f/reaudit_focused.log`.

## Finding disposition

| Prior finding | Priority | Disposition |
|---|---|---|
| Scrublet per-sample loop discarded results from a view | P1 | Fixed and executed |
| scDblFinder call was not reproducible | P1 | Fixed; source-checked against retained R determinism evidence |
| Shipped DoubletFinder example aborted | P1 | Fixed; source-checked against retained R execution evidence |
| Co-expression heuristic lacked nearby ambient caveat | P2 | Fixed and source-checked |
| No reporting guidance | P2 | Fixed and source-checked |

**Remaining P0/P1/P2 findings: none.**
