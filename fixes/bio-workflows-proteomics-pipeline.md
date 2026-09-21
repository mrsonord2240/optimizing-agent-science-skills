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


## Pass 5 (2026-09-15)

Re-audit after pass 1 scored **81** (static 79, execution 82.8), deployable at the supporting floor of 75, with
every pass-1 fix reproduced cell for cell. This pass hardens what the re-audit newly found; nothing was blocking.
Worktree `F:\OpenScience\external\bioSkills-wt-prot5b`, branch `fix/proteomics-5b`, cut from `openscience-fixes`
at `1110c24`. Commit `d61774d`. Runtime: R 4.4.3 via the candidate `r.sh` (limma 3.62.2, MSstats 4.14.2,
MSnbase 2.32.0, arrow 23.0.1.2). All five fenced blocks re-extracted byte-for-byte from the edited SKILL.md and
run with `sys.source()`; audit data copied read-only into the scratchpad; the three-condition design rebuilt with
the re-audit's own `make_3cond.py` (seed 31415).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Complete R Workflow halts at `prcomp` with `a dimension is zero` when no protein is observed in every sample | P1 | Guard `nrow(complete) >= 3`; on failure a message naming missingness as the cause with the three real options (lower `min_frac`, drop the sparsest samples, read the correlation) and an explicit "do NOT impute"; fall back to `cor(..., use = 'pairwise.complete.obs', method = 'spearman')`. QC no longer gates the statistics | ran: failure reproduced first on the rebuilt 3-condition design (893 proteins after the completeness filter, **0** complete cases, `ERROR: a dimension is zero`); with the guard the block completes and prints a correlation matrix that is cleanly dose-ordered (Ctl-Ctl 0.94-0.95, Ctl-High 0.88-0.91) | Same guard propagated to `examples/proteomics_workflow.R` |
| `makeContrasts(Treatment - Control)` hard-coded, so >2 conditions die with `object 'Treatment' not found` | P1 | Contrasts built from `levels(sample_info$condition)` against the reference (first) level, named `<level>_vs_<ref>`; `results` gains a `contrast` column; significance from `unclass(decideTests(fit2_treat, method = 'global', adjust.method = 'BH'))` so BH covers the whole contrast family; per-contrast breakdown printed; the omnibus `eBayes` + `topTable` F-test documented as the ANOVA-style alternative | ran: 3-condition design completes -- `High_vs_Ctl` 20 called with **0 false positives among 780 true nulls**, `Low_vs_Ctl` 0. Two-condition regression byte-for-byte: Input 1 still 62 called (Up 35, Down 27), 18 non-estimable, 0 false positives; Input 3 (failed sample) still 60, T4 still dropped | `unclass()` is required: `decideTests` returns an S4 `TestResults` that `as.matrix()` does not demote, and whose `[` refuses the two-column character index (`Two subscripts required`) |
| TMT CoA guard does not detect a transposed matrix, which is exactly what its comment claimed | P2 | Orientation test before `purityCorrect`: a CoA row is one reagent's isotopic envelope and sums to 100% by construction, a column does not, so `sum((rowSums - 100)^2)` must beat `sum((colSums - 100)^2)`; plus diagonal-dominance and a percent-vs-fraction check. The negatives `stopifnot` is kept but its comment no longer claims to be a transposition test | ran: on the audit's `tmt10_synthetic.mzML` the correct CoA passes at median relative error 0.0006 (uncorrected 0.0022, all three re-audit figures reproduced); the transposed CoA gives 0.0015 with **0 negatives** and now stops with `CoA looks TRANSPOSED (18.4 vs 76.5)`; wrong channel names still stop; a fraction-scaled sheet now stops too | The test is self-calibrating: it cannot fire on a near-symmetric matrix, which is exactly the case where transposition does not matter numerically |
| SKILL.md never states that median centring assumes symmetric change | P2 | Assumption documented at both places the choice is made -- the limma median sweep (step 3) and MSstats `equalizeMedians` -- with the measured consequence, the one-sided-design escape (`normalization = FALSE` on externally normalized input, or `globalStandards` with a spike-in / unchanged set) and a "check the null centre" instruction; Common Errors row added; usage-guide Tips line rewritten | ran: MSstats block on the audit's evidence subset reproduces the re-audit exactly -- 296 proteins, 44 up / 26 down, all 179 true nulls shifted **-0.1934 log2** (median -0.1951, t vs 0 **p = 2.29e-55**), 105 called at BH 5% of which **21 are true nulls, all 21 negative** | Filed by the re-auditor against the Skill, not against MSstats; three independent null controls of theirs call 0 |
| MSstats block's comparison matrix is two-condition only, with no statement of the shape for more | P2 | Comment giving the >2-condition shape: columns = every Condition level in sorted order, one row per contrast, and adjust across rows yourself | ran: `groupComparison` with a 2 x 3 contrast matrix on a three-condition relabelling of the same evidence -- levels sorted `Control HighDose MidDose`, 296 proteins per contrast, no error | |
| `usage-guide.md` sample-annotation template omits the `batch` column the design branch keys on | P2 | `batch` added to the CSV template, with a sentence saying when it is required and that `condition` may have more than two levels | docs: matches the `has_batch` branch in the block | |

**Found while working (fixed inline).** The annotation was re-aligned to the surviving samples with
`sample_info[sample_info$sample %in% colnames(normalized), ]`, which filters but does **not** reorder. `lmFit`
pairs design rows with matrix columns positionally, so an annotation sorted differently from the intensity columns
silently fits the wrong design. Replaced with `match(colnames(normalized), sample_info$sample)` plus a
`stopifnot`. No change on the audit data (orders already agreed) -- Input 1 and Input 3 numbers are identical.

**Shipped example.** Same PCA guard; a note that it is a deliberate two-condition demo, pointing at the
generalized block for three or more. Re-run twice from two empty directories: exit 0 both times, S8 dropped,
1373 PCA proteins, 16 non-estimable, 79 significant, five files written, `proteomics_results.csv` byte-identical
between runs -- all unchanged from the re-audit.

All five R fences and the example `parse()` clean.

## Left unfixed (pass 5)

- **[P2] FragPipe named but not coded, MSstatsTMT multi-plex still a comment.** Unchanged from pass 1:
  MSFragger/FragPipe are licence-gated and absent from this machine, so a runnable block could not be verified
  here at all.
- **[P2] Token cost / progressive disclosure.** The file is now 479 lines (from 396). Splitting into
  `references/` is a restructure, explicitly out of scope, and this pass had to add executable guards.

## Pass 6 (2026-09-21)

Fixer for the pass-5 re-audit (87.7, Production Ready; open: 1 P1, 4 P2). Worktree
`F:\OpenScience\wt\workflows-proteomics-pipeline`, branch `fix/workflows-proteomics-pipeline`. Commits `1dd932b`
(fixes) and `29d0616` (split). Runtime: R 4.4.3 via the env `r.sh` -- limma 3.62.2, MSstats 4.14.2,
MSstatsTMT 2.14.2, arrow 23.0.1.2. Blocks re-extracted from the edited files and run on copies of the audit data
(pass5 `work1`, `workC`, `work2`, `work5`, `work7`) in a scratchpad.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `treat(lfc = log2(1.5))` silently zeroes intermediate dose levels | P1 | comment beside `treat()`: the floor is a per-contrast minimum; lower `lfc` and screen with the F-test; a zero on an intermediate level means "not detected at this n" | ran on the audit's 3-condition data: High/Low calls 20/0 at log2(1.5), 52/0 at 0.3, 78/8 at 0; F-test 75 hits at BH 5% | the auditor's suggested wording ("lower lfc") is only partly right: at n=4 the low dose is also underpowered (0 calls at lfc 0.3), so the text says so instead of promising a rescue |
| example hard-codes the two-condition contrast | P2 | `examples/proteomics_workflow.R` builds contrasts from the condition levels and calls significance from global `decideTests`, as SKILL.md does; heatmap protein list now from `results$protein` | ran from an empty dir: 2-condition identical to before (1373 PCA proteins, 16 non-estimable, 79 significant, up 48 / down 31, five files); with `sample_groups` edited to 3 levels it completes | |
| MSstatsTMT multi-plex route is a comment | P2 | wrote the runnable MaxQuant route (`MaxQtoMSstatsTMTFormat` -> `proteinSummarization` with reference-channel normalization -> `groupComparisonTMT`, moderated, level-driven contrasts, BH across rows) | ran on MSstatsTMT 2.14.2's bundled 5-plex `evidence`/`proteinGroups`/`annotation.mq`: completes, 8 proteins x 3 contrasts. Planted 2x on 3 proteins in the channels of condition `1`: they read +0.64 to +0.68 log2 against -0.31 for the 5 unspiked (difference 0.97 vs planted 1.00; the offset is the median normalization on an 8-protein set) | chose "write it": MSstatsTMT is installed. Package and API are the only source; no synthetic 2-plex was built |
| FragPipe named as an input, no code | P2 | claim deleted from the description (the only mention) | n/a | chose "delete": FragPipe/MSFragger are licence-gated and absent from this machine |
| result table has no stated schema | P2 | columns and the meaning of `significant` stated above step 7 | ran: `colnames(results)` = protein, contrast, logFC, AveExpr, t, P.Value, adj.P.Val, significant | |
| 396 -> 479 lines, no `references/` | P2 | split, see below | see below | |

**Redundancy removed (`usage-guide.md`).** Every passage below is deleted from the guide; its content lives where stated.

| deleted from usage-guide.md | now |
|---|---|
| Prerequisites install block | SKILL.md "Inputs and Install" (limited to packages the Skill uses; `ashr` and `iq` were never referenced by SKILL.md and are dropped) |
| Pipeline Stages 1-7 (import, transform, completeness, missing values, QC, differential, output) | already in the SKILL.md workflow blocks, Governing principle and Pipeline Overview; nothing unique |
| Input Requirements: MaxQuant files, sample-annotation template and the `batch` / multi-level `condition` paragraph | SKILL.md "Inputs and Install" |
| Tips: missing values, normalization symmetry, more than two conditions, completeness, contaminants | already in SKILL.md (step 3/4 comments, Common Errors) |
| Tip "minimum 3 biological replicates per condition" (only here) | SKILL.md QC Checkpoints, new `Design` row |

The guide keeps: overview, quick start, example prompts (one new, for two-plex TMT), the example's output-file table (labelled as the example's), typical results.

**Split.** `SKILL.md` 543 -> 367 lines. Moved verbatim: `references/msstats.md` (MSstats), `references/tmt-isobaric.md`
(both TMT blocks and the multi-plex route), `references/silac.md`, `references/dia-nn.md`; index in SKILL.md
"Reference Files" replacing the `## Workflow Variants` heading (the only line not carried over), plus one
pointer line under the workflow Approach. Checked: a multiset comparison of non-blank lines old vs new found only that heading missing;
all 5 moved fences and the main block `parse()`; SILAC (453 tested, 49 at BH 5%), DIA-NN (887 x 8, 0 `-Inf`),
MSstats (296 proteins) and the main block (62 significant, 35 up / 27 down) re-ran unchanged from the extracted
files. Five comments saying "above" now name the file they point at. Common Errors, the decision-relevant
scope, thresholds and install stay in SKILL.md, which is why it is still over 300 lines (the main workflow block alone is 206).

## Left unfixed (pass 6)

- **SKILL.md still 367 lines, above the 300-line target.** What is left is what every request needs (206-line main
  workflow block, Governing principle, Common Errors, install); the brief keeps those in SKILL.md, and splitting the
  main block or its comments would break the runnable path.
- **No two-plex TMT run on data with a known effect beyond the bundled 8-protein set.** MSstatsTMT ships only that
  real dilution set; building a synthetic multi-plex MaxQuant evidence table with planted truth would be new test
  data, not a correction. The planted-2x check on the bundled set recovered the effect.
- **FragPipe route not written** (deleted instead): FragPipe/MSFragger are licence-gated and not installed, so no runnable block could be verified.
