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

## 2026-09-21 P2 fix pass

Worktree `F:\OpenScience\wt\crispr-screens-batch-correction`, branch `fix/crispr-screens-batch-correction` (from staging `431aa55`).
Fixer: Claude Sonnet 5. Env: `crispr-screen-analyst` (Python venv, `combat` 0.3.3, mageck 0.5.9.5). Audit: 4 P2s.
Commits: `03d9a36` fix, `bb597c4` redundancy, `8458687` split, `f04f3c5` scripts. SKILL.md 332 lines -> 231 (split: 252, then scripts: 231).
Verification data: real HAP1 TKOv3 counts with the audit's planted two-batch design (input 1) and batch-free design (input 7), plus planted zero-residual guides.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Within-batch-constant filter over-excludes (294/71,090 guides) | P2 | Filter is now the residual sum of squares after regressing out batch (+ condition) with the same design pycombat uses, threshold 1e-8 (not `== 0`, round-off) | ran | Input-1 design: 0 guides dropped, batch centroid distance 233.8 -> 1.0 (old filter: 16.2 on the 70,796 kept guides), essential AUC preserved; the 294 guides constant in one batch are now corrected (batch mean gap 7.2 -> 0.19). Planted: constant-in-both-batches and 0,0,1,1-per-batch guides dropped, constant-in-one-batch guide corrected |
| Dropped guides only printed, not returned | P2 | `combat_correct()` returns `(corrected, uncorrected)`; prose, Common Errors and the Validation Checklist say to flag them in hit calling | ran | Uncorrected rows equal raw counts; script also writes them to a file |
| All-NaN framed as the reliable failure signature | P2 | Docstring and prose: the pre-fit filter prevents both NaN and silent constant collapse; NaN check is a backstop | ran | Also corrected a wrong claim: the input-7 NaN was caused by 340 zero-residual guides, not by absence of batch effect. Bare pycombat 100% NaN; with those 340 dropped the wrapper returns a clean matrix (no ValueError any more on that data) |
| Genome-scale `mageck mle` runtime undisclosed | P2 | Runtime paragraph (multi-hour; subset or lower `--permutation-round` for a sanity check) | docs (TOOLS.md note 7, `mageck mle --help`) | Not re-run: genome-scale is the multi-hour job the note describes |
| (found) `biological_covariate` named as a ComBat argument in SKILL.md and guide; guide said log10 for a log2 recipe | small | Now `mod` / log2 | ran (signature) | |
| (found) `batch_diagnostic` errors with fewer than 5 samples | small | `n_pc = min(5, samples, features)`; script prints PCs where batch is significant | ran | Batch was on PC2 in the input-1 design, so PC1-only reading would miss it |

### Left unfixed

None of the 4 P2s. Note on the audit's assertion "ValueError on batch-free data": it no longer raises there, because the filter now handles the cause; the ValueError stays as a backstop.

### Deleted passage -> new home (redundancy pass)

| deleted from `usage-guide.md` | now in |
|---|---|
| Prerequisites install block (its `pip install combat` comment swallowed the following package list) | SKILL.md "Version Compatibility" (install line, inputs, versions checked) |
| Tips: always supply `mod`; ComBat-then-test over-confident FDR; verify after correction; Chronos for panels; NTC >= 500; in-vivo batch sources; sequential correction double-corrects | SKILL.md ComBat failure mode, "Why this is preferred", Validation Checklist, decision tree, NTC section, Batch Sources table, "ComBat after RUV double-corrects" |
| Tips: CN correction before batch; fall back to median normalization | SKILL.md decision tree (panel row); NTC section |
| Decision Cheat Sheet rows | SKILL.md decision tree / When NOT to Correct / Thresholds; new row "Several screens sharing one library -> JACKS or Chronos" |
| What the Agent Will Do (steps 1-9) | SKILL.md decision tree, RUV, Thresholds, Validation Checklist (new last item: compare hit list with the uncorrected one) |
| Validation Checklist | SKILL.md "Validation Checklist" (+ item for `uncorrected`) |

### Split and scripts

| from | to |
|---|---|
| SKILL.md ComBat, RUV, SVA, NTC-anchored sections (verbatim, no non-blank line lost, python fences ast-parse, R fences `parse()`) | `references/combat.md`, `ruv.md`, `sva.md`, `ntc-anchored-normalization.md`; new decision-tree row for unannotated batches points to RUV/SVA |
| `references/combat.md` python block (`combat_correct`) | `scripts/combat_correct.py` (CLI + importable) |
| SKILL.md Diagnose block (`batch_diagnostic`) | `scripts/batch_diagnostic.py` (CLI + importable) |
| RUV (13 lines), SVA (10), NTC-anchored (7), MLE design matrix | stayed inline, under the 15-line bar |

## Final pass, Phase 1 — 2026-09-21

Worktree `F:\OpenScience\wt\crispr-screens-batch-correction`, branch `fix/crispr-screens-batch-correction`
(tip `f04f3c5`, unchanged). Fixer/auditor: Claude Sonnet 5. Env: `crispr-screen-analyst`.

Fix log's own "left unfixed" was already empty and `fixes/README.md`'s revisit list has no row for
this Skill, so this pass's job was to walk every runnable block in the Skill (not just what earlier
fixers touched) and confirm it executes as `SKILL.md` invokes it. Real HAP1 TKOv3 counts (planted
2-batch/2-condition design) and the prior audit's 2,500-guide RUV/SVA synthetic set. No defect found;
no commit made (nothing to change).

| block | how run | result |
|---|---|---|
| `scripts/batch_diagnostic.py` CLI | as SKILL.md invokes it, real HAP1 71,090-guide planted design | batch loads on PC2 (F=52.8, p=0.0003), not PC1; PC1 batch/cond F=0.01 |
| `scripts/combat_correct.py` CLI, with and without `--condition-col` | same data | both complete, 0 uncorrected, 0 NaN |
| `combat_correct()` import + assertions | same data | 0 guides dropped (matches "Input-1: 0 dropped" claim), batch centroid dist 233.83->0.98, CEGv2/NEGv1 AUC 0.9947->0.9966, 0 Inf |
| `combat_correct()` on a batch-free design (forced) | real HAP1 data, batch-free construction | filter drops 320 zero-residual guides, completes without raising -- confirms ValueError is now a backstop only |
| `references/ruv.md` RUVg block | audit's 2,500-guide hidden-batch set | W_1/W_2 (8x2), corrected 2,500x8, NTC median CV 0.23->0.0016; old `which()`-based `cIdx` regression-confirmed still fails S4 dispatch |
| `references/sva.md` block | same RUV dataset | 1 significant surrogate variable, 8x3 design matrix, 0 NaN |
| `references/ntc-anchored-normalization.md` function | same RUV dataset | all 8 sample NTC medians scaled to exactly `target_median` |
| `examples/batch_correct.py` | standalone, its own synthetic data | runs to completion, 15/15 true hits, 0 false positives |
| SKILL.md MAGeCK MLE design-matrix block, `--permutation-round 10` | real 1,646-gene/6,460-guide HAP1 subset, mageck 0.5.9.5 | 0/1,646 NaN betas; top treatment betas numerically identical to the prior audit's run (deterministic, as documented) |

Also checked: installed versions (`combat` 0.3.3, `mageck` 0.5.9.5, `sva` 3.54.0, `RUVSeq` 1.40.0) match
SKILL.md's "Version Compatibility" claims exactly; `--permutation-round` and `--norm-method control`
are real `mageck` flags (`--help`); `py_compile` clean on all three changed/scripted `.py` files; every
"Related Skills" cross-reference resolves to a real folder in the fork; `SKILL.md` at 231 lines, all
`references/*.md` at 16-22 lines (both under the split threshold).

### Left unfixed

Nothing found to fix. Checkpoint: `F:\OpenScience\audits\_final_pass\bio-crispr-screens-batch-correction\CHECKPOINT.md`.
