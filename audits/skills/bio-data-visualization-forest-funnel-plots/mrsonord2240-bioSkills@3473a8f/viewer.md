> **Audit record for `bio-data-visualization-forest-funnel-plots`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@3473a8f](https://github.com/mrsonord2240/bioSkills/tree/3473a8f48eccab6c73436a627c3e8568f3736eef/data-visualization/forest-funnel-plots) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# bio-data-visualization-forest-funnel-plots — exact-commit re-audit

**Result:** ⭐ Production Ready — **95/100**  \
**Source:** `3473a8f48eccab6c73436a627c3e8568f3736eef`  \
**Assertions:** 25/25 passed  \
**Veto gates:** PASS

## Evidence

- Structural wrapper: PASS (stability, contract, determinism, security).
- Exact-source contract: 13/13 PASS.
- R exact execution: full shipped workflow PASS with `options(warn = 2)`.
- Visual inspection: BCG forest footer is rendered and all study whiskers are visible; funnel is rendered.

## Scores

| Static | Dynamic | Final | Grade |
|---:|---:|---:|---|
| 93/100 | 96.6/100 | 95/100 | ⭐ Production Ready |

## Input assertions

| Input | Result | Assertions |
|---|---|---:|
| REML BCG forest with log-ratio axis and prediction interval | PASS | 5/5 |
| Funnel, contour funnel, Egger, and trim-and-fill safeguards | PASS | 5/5 |
| Three-study small-k meta-analysis | PASS | 5/5 |
| Cox covariate forest and treatment-by-subgroup forest | PASS | 5/5 |
| MR method comparison with outlier-safe layout | PASS | 5/5 |

## Recommendations

No open P0, P1, or P2 findings.
