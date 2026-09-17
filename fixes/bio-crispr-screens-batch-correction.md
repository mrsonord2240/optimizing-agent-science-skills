# bio-crispr-screens-batch-correction fixes (2026-09-16)

Worktree `F:\OpenScience\wt\crispr-c`, branch `fix/r2-crispr-c`. Fixer: Claude Opus 5 (orchestrating
session). Runtimes: the candidate venv (`combat` 3.0.5 / pycombat, pandas 2.x) and the candidate R
library via `audit-envs\crispr-screen-analyst\r.sh` (RUVSeq, sva). Verification scripts and data:
`F:\OpenScience\wt\_fixdata\bc\` (`verify_bc.py`, `verify_ruv.R`, `verify_sva.R`), run against real
HAP1 TKOv3 counts and the audit's own hidden-batch RUV dataset.

## Round-2 audit pass — 2026-09-16

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `combat_correct()` crashes on its own "Critical" covariate usage: `mod` passed as a one-hot array and `data` as a raw ndarray | P1 | Passes a DataFrame and `mod=list(condition_vector)`; docstring states pycombat one-hot-encodes `mod` itself | ran | Block extracted from SKILL.md and run on a planted two-batch HAP1 design (0.5x depth + 150-read offset): completes, PC1 batch F 0.9 -> 0.0, CEGv2 mean LFC -3.83 vs non-CEG -1.07 (essential dropout preserved) |
| The block used `pd` without importing pandas | P1 (same block) | `import pandas as pd` added | ran | Would have raised `NameError` on the covariate path even after the `mod` fix |
| Forcing ComBat on a batch-free design silently returns 100% NaN | P1 | `combat_correct()` raises `ValueError` when the returned matrix contains NaN, and a new paragraph says to diagnose before correcting | ran | Negative control (batch 2 = a copy of batch 1) now raises instead of returning a dead matrix |
| (Found while fixing) **A handful of features that are constant within one batch turn the entire ComBat output into NaN** — not just their own rows | P1-class, not in `recommendations[]` | `combat_correct()` drops within-batch-constant features from the fit, says how many, and returns them uncorrected | ran | Measured: **6 zero-within-batch guides out of 2,000 produced an all-NaN 2,000 x 6 matrix**; dropping them leaves 0 NaNs. On the full 71,090-guide screen, 310 such guides. This is the same divide-by-zero as the audited no-batch case, but it fires on ordinary data with zero-count guides |
| RUV example's `cIdx` is integer positions; `RUVg`'s `SeqExpressionSet` method requires character rownames | P1 | Uses `rownames(counts_df)[rownames(counts_df) %in% ntc_sgrna_names]` with a `stopifnot`, and a comment explaining the dispatch difference from the matrix method | ran | Old form reproduced: `unable to find an inherited method for function 'RUVg' for signature 'x = "SeqExpressionSet", cIdx = "integer", k = "numeric"`. Fixed form runs on the audit's 2,500-guide hidden-batch set with 500 NTCs: 2,500 x 8 corrected matrix, no NAs |
| (Found while fixing) RUV section returns only `normCounts()`, with no mention of the W factors | incomplete guidance | Documents both: `pData(ruv_corrected)` gives W_1..W_k for a downstream design matrix, `normCounts()` is the adjusted matrix for PCA/visual checks | ran | This matters because RUV's intended use in a screen is W as MAGeCK MLE covariates |
| No explicit out-of-CRISPR-screen scope boundary | P2 | New "Related but out of scope" section: the methods generalise, the NTC rules, CEGv2 PR-AUC checks and MAGeCK/Chronos integration do not | docs | |
| MAGeCK MLE permutation p-values not flagged as stochastic | P2 | `--permutation-round 10` added to the design-matrix example plus a Reproducibility paragraph: betas deterministic, permutation p-values not seeded | docs (`mageck mle --help`) | Consistent with `mageck-analysis`, which is quantifying this on the same branch family |
| Validation checklist had no NaN/Inf check | P1 (same root cause) | Checklist now starts with "corrected matrix has no NaN/Inf values" | ran | The checklist's other items would only be reached after already trusting a dead matrix |

The SVA block needed no change: run verbatim against the audit's data it returns 1 significant
surrogate variable and an 8 x 3 design matrix with no NAs.

All 5 `recommendations[]` entries (3 P1, 2 P2) fixed, plus two defects found while fixing. Nothing
left unfixed.
