# bio-workflows-proteomics-pipeline fixes (2026-09-15)

Pass 1 on this Skill — no fixer had been assigned to it before. Audit: 67, **Beta Only, deployable: false**
(supporting floor 75); static 67, exec 469/7 = 67.0, assertions 17/30 = 56.7%, safety/scope assertion FAILs
on Inputs 3, 5 and 6. Evidence: `F:\OpenScience\audits\bio-workflows-proteomics-pipeline\`.

Branch `fix/proteomics-4-quant` (worktree `F:\OpenScience\external\bioSkills-wt-prot4c`), branched from
`fix/proteomics-3` @ `e8d2cd4`. Commit `962785f`. Runtime: R 4.4.3 via the candidate `r.sh` — MSstats 4.14.2,
MSnbase 2.32.0, limma 3.62.2, arrow 23.0.1.2, dplyr 1.2.1, tidyr 1.3.2, ggplot2 4.0.3, pheatmap 1.0.13.
**MSstats is installed in the shared R-lib**, so the MSstats block was verified by running it, not from docs.
All five fenced blocks were re-extracted byte-for-byte after editing and run with `sys.source()` on copies of
the audit's synthetic data in a scratchpad; the example was run from an empty directory.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| MSstats block silently truncates MaxQuant tables (Input 5) | P1 | `read.table(..., quote = '', comment.char = '')` on both tables plus a `readLines` row-count `stopifnot`; the same on `read.delim` in block 1 and in the example; Common Errors row | ran: 10369/10369 evidence rows, 1560/1560 proteinGroups rows, **296 proteins summarized** (the audit's truncated read: 2954 rows, 62 proteins); `groupComparison` 296 rows | the fix already made in `proteomics/quantification` had not been propagated here |
| DIA-NN block feeds `-Inf` into limma (Input 2) | P1 | pivoted table materialized as a matrix with rownames, `m[m == 0] <- NA` before `log2`, `stopifnot(!any(is.infinite(.)))`; Common Errors row | ran: 887 x 8, **0 `-Inf` cells** (audit: 61), then `eBayes(trend, robust)` completes — 68 at BH<0.05, 0 true nulls called, 68 of 78 true changers recovered. The audit's run stopped with "missing value where TRUE/FALSE needed" | |
| SILAC block crashes and reports unadjusted p-values (Input 7) | P1 | non-finite cells to NA, rownames from `Majority.protein.IDs`, filter to >= 2 finite ratios, `t.test` loop replaced by an intercept-only `lmFit`/`eBayes(trend, robust)` with `topTable(adjust.method = 'BH')`; Common Errors row | ran on a MaxQuant-format SILAC `proteinGroups.txt` rebuilt to the auditor's construction (500 proteins, 50 true +/-1.5, 30 rows with < 2 ratios): block **completes** (audit: `ERROR: not enough 'x' observations`), 470 tested, 48/48 recoverable changers found, **1** false positive at BH<0.05 vs **18** true nulls that raw p<0.05 would have called | |
| TMT CoA route misplaces bleed; template misdescribed (Input 4) | P1 | `makeImpuritiesMatrix(filename=)` ruled out for TMT10/TMTpro (it reads a CoA by Da OFFSET and places each column k POSITIONS away — correct only for non-interleaved reagents); block now reads a channel-named CoA matrix, reorders to `reporterNames(TMT10)` and passes it to `purityCorrect` with a negative-value guard; "near-identity template" claim removed; Common Errors row | ran, two independent checks: (a) the old route puts 126's bleed in **127N** while the truth is **127C**; (b) median \|relative error\| vs `tmt10_truth.csv` on the synthetic TMT10 mzML — uncorrected 0.0022, **old CoA route 0.0018, new channel-named route 0.0006**. Template diagonal read from `makeImpuritiesMatrix(10)`: 0.928-0.965, not near-identity | matches the auditor's own numbers for the uncorrected and old routes |
| Failed-load check cannot see a failed load (Input 3) | P1 | raw-distribution step now reads the raw `Intensity.` columns instead of the MaxLFQ-renormalized `LFQ.intensity.` ones, prints a `load_shift_log2` column, and flags on two axes as outliers (>= 1 log2 load drop OR ID count > 3 MADs below the median) in place of the 50%-of-median ID cut; same fix in the example; Common Errors row | ran: on `proteinGroups_failed.txt` **T4 is flagged and dropped** (the audit's rule flagged nothing, "(none)"); on the clean `proteinGroups.txt` **no sample is flagged** and the result is unchanged | the 3x-low load surfaces as only -0.81 log2 because the run loses its dimmest proteins entirely — the ID-count rule is what catches it, which is why both axes are needed; recorded in the block comment |
| Executable path contradicts the Skill's own rules (Input 1); unseeded imputation (T3 determinism P2) | P2 | unseeded downshift imputation removed from the executed path entirely — limma fits each protein on its observed values, PCA on complete cases, batch a covariate when the annotation has one, non-estimable contrasts reported instead of turning every `sum()` into NA; downshift text is now a DO-NOT with the differential-abundance pointer and proDA is the documented upgrade; Approach paragraph aligned | ran: 1323 tested, `design columns: Control Treatment factor.batch.B2 | batch in design: TRUE`, **62 significant, 0 true nulls called** (audit: 52 called, unseeded, `batch in design: FALSE`). The block now contains **no RNG call at all**, so determinism is exact rather than seed-dependent | audit's T3 check had found 52/52/53 calls across three seeds |
| No clinical stop condition; example not self-contained (Input 6) | P2 | one research-only Scope sentence; `examples/proteomics_workflow.R` simulates a synthetic 8-sample `proteinGroups.txt` when none is present, and all component fixes are propagated into it | ran from an empty directory: **exit 0**, S8 dropped as a failed load, 79 significant with **0 false positives** among 1400 true nulls, all five output files written. As shipped the example previously died on `cannot open file` | |
| `!= '+'` contaminant/reverse filter silently NAs the whole table | (found while fixing) | `!(x %in% '+')` with an all-NA `stopifnot` guard, in SKILL.md and the example | ran: hit it for real on the self-contained example's simulated table, where no row is flagged, so `read.delim` types those columns logical, `NA != '+'` is NA and subsetting by NA returned 1500 all-NA rows while `nrow()` still printed 1500 | the quantification pass-3 log noted this R behaviour but recorded "the Skill has no such filter" — this Skill does |

Also: Version Compatibility line changed from open-ended minima (`MSnbase 2.28+` ...) to the versions actually
checked; `usage-guide.md` line 43 ("LFQ intensity, not raw Intensity") amended so it no longer contradicts the
failed-load fix. Frontmatter `name` untouched. All five blocks `parse()` clean. Files are CRLF, UTF-8, ASCII
except one pre-existing em dash in the governing-principle prose.

## Left unfixed

- **FragPipe named but not coded** (static 1.1 Completeness). New content, out of scope for a correction pass —
  and MSFragger/FragPipe are licence-gated and absent from this machine, so it could not be verified anyway.
- **MSstatsTMT multi-plex route is still a comment block**, not executable code. Turning it into a runnable
  block is new content; the existing comment is correct as far as it goes.
- **Token cost / progressive disclosure** (3/5 each): the Skill is now 393 lines with no `references/`.
  Splitting it is a restructure, not a correction.

## Noted, not acted on

- With the truncation fixed, `dataProcess`/`groupComparison` on the full synthetic evidence table calls
  **21 of 208 true nulls** at adj.p < 0.05 (~10%, above the nominal 5%). That is MSstats' own behaviour on this
  one-feature-per-peptide synthetic set, not a defect in the Skill's code, and the audit did not raise it. The
  truncated read the audit scored had hidden it (61 calls, 0 nulls, on 62 proteins).
