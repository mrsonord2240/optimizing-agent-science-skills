# bio-proteomics-differential-abundance fixes (2026-09-15)

Branch `fix/proteomics` (worktree `F:\OpenScience\external\bioSkills-wt-proteomics`). Runtime: R via `r.sh` (limma 3.62.2, DEqMS 1.24.0, proDA 1.20.0, ashr 2.2.63) and the candidate venv (pandas 3.0.5, scipy 1.18.1, statsmodels 0.15.0). SKILL.md blocks were extracted and run on the audit data (`proteinGroups.txt` 4 v 4 with batch, `three_arm_log2.csv`, `plasma_12v12.csv`).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| proDA block calls a coefficient that does not exist | P1 | `test_diff(fit, 'conditionTreatment')`, design `~condition + batch`; Common Errors row | ran: 1500 rows, 40 at adj_pval < 0.05 | |
| limma and DEqMS blocks break on real MaxQuant matrices | P1 | Valid-value filter (>= 2 per group) before `lmFit` with Approach text; `stopifnot(all(fit2$df.residual > 0))` before `spectraCounteBayes`; two Common Errors rows | ran: 1500 -> 1300 rows, `eBayes(trend, robust)` OK, 99 calls / 3 null; DEqMS with no recycling warning | |
| `treat()` silently drops trend and robust | P1 | `treat(fit2, lfc, trend = TRUE, robust = TRUE)` into `fit_treat` (SKILL.md and example); Approach and Common Errors | ran: `fit_treat$s2.prior` varies with intensity (df.prior median 153.8), 83 calls; example 37 | ashr and DEqMS keep using the eBayes `fit2` |
| Downshift and double-filter FDR claims overstated | P1 | Insight 1, downshift failure mode, double-filter Approach/Symptom and two threshold rows: sigma is the run-wide SD, imputed FC is set by the constant (wing), no FDR guarantee; >50% FDR regime-specific | method change on audit run evidence: Input 3 (downshift 0-1 false positives, 62-68 vs 104 calls, logFC vs AveExpr r = -0.96) and Input 7 (double filter 1.3-3.8% realized FDR) | recommendation against imputation and double filtering kept |
| Example "median centering" scales log values | P1 | `sweep()` subtraction of column medians plus global median | ran: `examples/limma_analysis.R` exit 0 (41 significant, 37 treat); `parse()` OK | |
| msqrob2 and MSstats promised but not provided | P2 | none | -- | adding code blocks is new content |
| Design rename hard-codes two groups | P2 | `colnames(design)[seq_len(nlevels(cond))] <- levels(cond)`; Common Errors row | ran on three-arm data: design Control, DrugA, DrugB, batchD2, batchD3; `makeContrasts` + `eBayes` OK on 1074 rows | |
| No stop condition for n=1 or clinical questions | P2 | Scope sentence; `ValueError` when no protein has >= 2 values per group (SKILL.md block and example); Common Errors row | ran: n=1 case raises the ValueError; 12 v 12 tests 826 proteins; example exit 0, `py_compile` OK | |
| Silent defaults in ashr and proDA outputs | P2 | Drop NA rows before `ash()`; comment not to report proDA `diff` for proteins unobserved in a group | ran: 1300 shrunk, 0 zero PosteriorMean | |

Also: MSstats taxonomy row now says AFT censored imputation exists only in `dataProcess(MBimpute = TRUE)`, matching the quantification fix; version line changed to the checked versions.

Left unfixed:
- P2 msqrob2 / MSstats code blocks: new content, out of scope.

---

# Pass 3 — 2026-09-15 (re-audit at 82, Limited Release, CORE floor 85)

Branch `fix/proteomics-3` (worktree `F:\OpenScience\external\bioSkills-wt-prot3`), branched from
`fix/proteomics-2` @ `d1b8fdc`. Commit `e8d2cd4`. Evidence: the re-audit at
`F:\OpenScience\audits\bio-proteomics-differential-abundance\` (2026-09-15 14:45/14:47). Runtime: R 4.4.3
via `r.sh` (limma 3.62.2, DEqMS 1.24.0, proDA 1.20.0, ashr 2.2.63), Python 3.12 shared venv.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| No guard for paired/blocked designs: the per-condition valid-value filter does not make the contrast estimable, so limma tested rows with 0 residual df or partly NA coefficients, and the Skill's own `stopifnot(all(fit2$df.residual > 0))` in the DEqMS block fired (Input 8) | P1 | estimability filter after `lmFit` — `fit <- fit[fit$df.residual > 0 & rowSums(is.na(fit$coefficients)) == 0, ]` — plus Approach text, a Common Errors row, and the same two lines in `examples/limma_analysis.R` | ran on `data/paired_donor_log2.csv` (6 donors x Unstim/LPS): realized FDR **12.0% -> 4.8%** (63 calls, 3 null), 18 zero-df and 120 partial-NA rows dropped, and the DEqMS block then runs verbatim (stopifnot passes) at 4.8% | internal contradiction: the DEqMS `stopifnot` asserts exactly what the upstream filter was supposed to guarantee. The audit's own alternative (>=2 complete donor pairs) only reached 7.2% |
| regression check on the same change | — | — | ran on the 4 v 4 batch data: 1300 -> 1297 rows, still **99 calls / 3.0% FDR**, DEqMS 99 / 3.0%, `treat(1.2)` 83 / 0 null — identical to the audit's Input 1 numbers | also removes the rows behind the unexplained `Partial NA coefficients for 3 probe(s)` warning the auditor docked a code point for |
| Decision tree called proDA the "correct verdict for undetected in one group" (Input 3) | P2 | that row and the proDA Approach now say proDA is honest but underpowered for on/off proteins at n=3-5, and those belong in a separate undetected list | ran independently rather than reading the auditor's output file: proDA 1.20.0 `~condition + batch` on the 4 v 4 data called **0 of 11** true on/off proteins, best `adj_pval` 0.17 | a claim contradicted by what the audit actually ran |
| Python path dropped untestable proteins silently, contradicting the limma Approach's own "report proteins removed by the filter separately" (Input 4) | P2 | `differential_abundance()` returns a second frame of untestable proteins with `n_case` / `n_ctrl` (SKILL.md block and Approach, and `examples/differential_abundance.py` including its `__main__`) | ran on `data/plasma_12v12.csv`: 826 tested / 39 called / 0 false positives unchanged, **74 untestable now reported**, of which `{on_off: 8, down: 3, up: 1}` and the rest null — exactly the set the audit found dropped | internal contradiction between the two workflows |
| `usage-guide.md` contradicted the calibrated SKILL.md — downshift "manufactures systematic false positives ... collapsed within-group variance" and the double filter "inflates realized FDR above 50%" — and the SKILL.md header line still said imputation "manufactures false positives" (Input 7) | P2 | carried the calibrated wording (run-wide sigma, FC set by the imputation constant, no FDR guarantee, regime-specific inflation) into the usage guide's Missing-Value Handling and Tips, and into the SKILL.md header line | text only; wording taken from the already-verified SKILL.md Insight 1 and `treat()` Approach | a stale-text supersede, no method change |

Also: both examples re-run — `limma_analysis.R` exit 0 (400 tested / 41 significant / 37 treat, identical to
the audit's smoke test) and `parse()` clean; `differential_abundance.py` exit 0 (400 / 43 / 0 untestable) and
`py_compile` clean. All six SKILL.md blocks re-extracted after editing and run verbatim. Pure ASCII.

## Left unfixed

- **P2 — msqrob2 / MSstats feature-level blocks (Input 9).** Still new content: two new workflow sections
  rather than a correction to anything present. Note for a later pass: msqrob2 **1.14.1 is now installed**
  in `F:\OpenScience\audit-envs\mass-spec-proteomics-analyst\R-lib` (the re-audit ran with it absent), so
  such a block could now be verified by running it. The audit's alternative — deleting msqrob2/MSstats from
  the description and decision tree — would narrow real coverage, so I did not take it. **Needs Sam's call.**

---

# Pass 4 — 2026-09-15 (new executable content: the msqrob2 / MSstats gap)

Branch `fix/proteomics-4-da` (worktree `F:\OpenScience\external\bioSkills-wt-prot4b`), branched from
`fix/proteomics-3` @ `e8d2cd4`. Commit `0fe7f85`. **Deliberate exception to the fixer brief's "no new
sections, no new tools" rule** — Sam's call on 2026-09-15 that the missing executables should be written
rather than the tools deleted from the description. Runtime: R 4.4.3 / Bioconductor 3.20 via
`F:\OpenScience\audit-envs\mass-spec-proteomics-analyst\r.sh`. **MSstats 4.14.2 was already present** in
the shared R-lib (pre-existing, re-verified in the 2026-09-15 install round), so both advertised tools are
now backed by code that runs; nothing was installed or upgraded there.

Versions invoked: msqrob2 1.14.1, QFeatures 1.16.0, MsCoreUtils 1.18.0, MSstats 4.14.2, limma 3.62.2,
DEqMS 1.24.0, proDA 1.20.0, ashr 2.2.63, SummarizedExperiment 1.36.0.

## What Input 9 actually asked for

| Input 9 assertion | 2026-09-15 result | after pass 4 |
|---|---|---|
| The Skill provides runnable code for the msqrob2 or MSstats route it recommends | FAIL (taxonomy and decision-tree rows only) | two new workflow sections, four new blocks, all run verbatim |
| Proteins missing in one condition are reported as undetected, not as an infinite fold change | PASS | preserved in both new blocks (msqrob2 `adjPval = NA` list; MSstats `issue == 'oneConditionMissing'`) |
| Realized FDR of the feature-level route is at or below nominal | FAIL (21.2%; "cause not isolated, no Skill guidance to follow") | cause isolated and guarded: 0.0% |
| Scope: output stays within the statistical test | PASS | preserved — the normalization remedy is routed to proteomics/quantification, not performed |

## Root cause of Input 9's 21.2%

Not variance moderation, and not the AFT imputation the auditor suspected (the audit's own no-AFT run was
20.8%). It is an **uncorrected global offset introduced by per-run median normalization on the peptide
table**. Each run's median is taken over the peptides detected in *that* run, and the detected sets differ,
so equalizing them transfers a detection-composition difference into a uniform between-condition offset. A
protein-summary test ignores an offset that size; a feature-level test has small enough SEs to call it
significant proteome-wide.

Measured on `data/evidence.txt` (1468 precursors, 299 proteins, 4 v 4) against `data/truth_proteins.csv`:

| route | median log2FC | calls | false pos | realized FDR |
|---|---|---|---|---|
| raw peptide matrix, no normalization (reference) | +0.015 | — | — | — |
| LFQ protein matrix from the same simulation (reference) | -0.015 | — | — | — |
| MSstats `equalizeMedians`, `MBimpute = TRUE` (auditor's run, reproduced) | -0.184 | 99 | 21 | **21.2%** |
| MSstats `equalizeMedians`, `MBimpute = FALSE` (the shipped block, verbatim) | -0.184 | 101 | 21 | 20.8% |
| msqrob2, `center.median` over all peptides | -0.202 | 112 | 32 | 28.6% |
| msqrob2, `center.median` over complete-case peptides only | -0.107 | 86 | 6 | 7.0% |
| msqrob2, no normalization (shipped block b05, verbatim) | -0.005 | 80 | **0** | **0.0%** |
| msqrob2 `msqrobAggregate` peptide-level lmer (shipped block b06, verbatim) | +0.004 | 80 | **0** | **0.0%** |
| MSstats with the offset removed upstream | +0.008 | 79 | **0** | **0.0%** |

Realized FDR tracks the offset monotonically and **the true-hit count never changes** (48 up / 32 down for
every msqrob2 variant, 42–43 up / 23–25 down for every MSstats variant) — the offset adds only false
positives. That is what makes `median(log2FC) ≈ 0` a usable pre-read check rather than a fudge factor.

## Changes

| addition | audit input it answers | change | verified (ran / help / docs) |
|---|---|---|---|
| **msqrob2 Workflow (R)** section | 9 assertion 1 | `QFeatures` → `zeroIsNA` → `logTransform` → `nNonZero >= 2` filter → `aggregateFeatures(robustSummary)` → `msqrob(robust = TRUE)` → `hypothesisTest`, with the undetected list taken before aggregation and the `adjPval = NA` rows reported | ran verbatim (block b05): 286 tested, 80 calls, **0 FP, 0.0% FDR**, 8 undetected (6 of them true on/off), 12 untestable |
| **peptide-level variant** (`msqrobAggregate`, `~condition + (1 \| sample) + (1 \| feature)`) | 9 assertion 1; Insight 3 | second block, `ridge = FALSE` with the reason | ran verbatim (block b06): 282 tested, 80 calls, **0 FP**, posterior df median 151.9 vs 36.4 summarized |
| **MSstats Workflow (R)** section | 9 assertions 1, 2 | `MaxQtoMSstatsFormat` → `dataProcess(MBimpute = FALSE)` → `groupComparison`, `issue == 'oneConditionMissing'` split out as undetected | ran verbatim (block b07): 290 tested, 6 oneConditionMissing (5 true on/off) reported separately |
| **"Check the contrast is centred" subsection** + new **Per-run median normalization** failure mode | 9 assertion 3 — the FAIL the auditor could not explain | `stop()` when `abs(median(log2FC)) > 0.05`, with the mechanism and the remedy routed to proteomics/quantification | ran verbatim (block b08): **fires** on the uncentred MSstats table with `median log2FC = -0.184`, and **passes** once the offset is removed upstream (79 calls, 0 FP) |
| Insight 3 recalibrated: feature-level "keeps information … but it is not free" | the audit's Completeness note; honesty | no longer claims feature-level simply beats summarize-then-test, and states the small-SE downside | ran: on the same `robustSummary` matrix, limma `eBayes(trend, robust)` and `msqrob(robust)` returned the **identical 80 calls / 0 FP**; limma df.prior 27.4 vs msqrob2 posterior df 36.4 |
| Decision tree: new rows for "a peptide table exists", the ridge constraint and the centring check; msqrob2 row rewritten | 9; the brief's "be honest about when msqrob2 beats limma" | says to escalate to msqrob2 for peptide disagreement / unbalanced coverage, not by default | same run as above |
| `ridge = TRUE` refused on a two-group design | new | decision-tree row, threshold row and Common Errors row | ran: msqrob2 1.14.1 raises "The mean model must have more than two parameters for ridge regression", and its own message gives `~ -1 + condition` as the escape |
| Seven new Common Errors rows | traps hit while verifying | `readQFeatures` needs `colData$quantCols`; `pe[['assay']]$condition` is `NULL` because colData sits on the QFeatures object; the ridge error; `msqrobAggregate`'s "Variable sample is not found"; msqrob2's `adjPval` (no `adj.P.Val`) and its NA rows; MSstats infinite `log2FC`; MaxQuant empty flag columns read as logical `NA` so `!= '+'` drops every row | each row is an error I hit and then fixed during this pass |
| `examples/msqrob2_peptide_level.R` (new) | 9 assertion 1 | end-to-end peptide-level run; takes `evidence.txt` + annotation, or simulates a peptide table when given no arguments | ran both ways, exit 0: on the audit data 80 calls / median logFC -0.0048 / 8 undetected; on its own simulation 43 calls / 3 FP / 7.0% against the planted truth. `parse()` clean |
| `usage-guide.md` kept in step | the standing consistency finding (Input 7) | msqrob2 row rewritten to match the decision tree; two Tips added (the centring check, and that both tools hide their unusable proteins); `QFeatures` added to the install line; new example listed | text only, wording taken from the verified SKILL.md sections |
| Version Compatibility line | — | msqrob2 1.14.1, QFeatures 1.16.0, MsCoreUtils 1.18.0, MSstats 4.14.2, R 4.4.3 / Bioc 3.20 added | versions read from the R-lib with `packageVersion()` |

## Regression — passes 1–3 untouched

All **six pre-existing code blocks are byte-identical** to `fix/proteomics-3` (checked by re-extracting the
fenced blocks from both revisions and comparing), and re-running them verbatim after the edits reproduces
the pass-3 numbers exactly:

- 4 v 4 batch data (`proteinGroups.txt`): 1500 → 1297 rows, limma **99 calls / 3.0%**, `treat(log2(1.2))`
  **83 / 0%**, DEqMS **99 / 3.0%**, ashr 1297 shrunk / 0 zero PosteriorMean.
- 6-donor paired data (`paired_donor_log2.csv`): 795 tested, **63 calls / 4.8%** with pass 3's estimability
  filter, DEqMS **62 / 4.8%** — pass 3's 12.0% → 4.8% correction still holds.
- `examples/limma_analysis.R` and `examples/differential_abundance.py` both exit 0; `parse()` and
  `py_compile` clean. SKILL.md, usage-guide.md and all three examples are pure ASCII, no BOM.

Pass 3's calibrated wording (the proDA on/off row, the recalibrated imputation and double-filter claims)
was not touched.

## Left unfixed

- Nothing from the re-audit's recommendation list remains open: the P1 blocked-design guard was pass 3, and
  the four P2s (msqrob2/MSstats code, usage-guide drift, proDA oversold, Python untestable proteins) are
  now all closed.
- **Not attempted:** a head-to-head on real public data. `...\public-data\PXD070049\` (Astral HYE) has one
  replicate per condition under the submitter SDRF, which cannot support a realized-FDR or within-condition
  CV claim, so every number above comes from the audit's seeded synthetic data with planted truth. Worth a
  real spike-in benchmark in a later pass if one with replicates is fetched.
- The centring check uses a fixed `0.05` threshold, calibrated on one 4 v 4 set (the 7.0% point sits at
  -0.107, the 0.0% points at |offset| ≤ 0.005). A study that genuinely expects a global shift must override
  it deliberately, which the prose says.

---

# Pass 5 -- 2026-09-21 (re-audit at 89, Production Ready; one open P1)

Worktree `F:\OpenScience\wt\proteomics-differential-abundance`, branch `fix/proteomics-differential-abundance`, from staging `main` @ `431aa55`. Evidence: `F:\OpenScience\audits\bio-proteomics-differential-abundance\` (Input 10, Input 9, static). Runtime: R 4.4.3 via the mass-spec env `r.sh`; msqrob2 1.14.1, QFeatures 1.16.0, MsCoreUtils 1.18.0, MSstats 4.14.2, on the audit's `evidence.txt` (4 v 4, planted truth).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Centring section's mechanism refuted: a uniform -0.20 offset gives 0 FP; per-run median normalization also halves the null SE (Input 10) | P1 | Approach rewritten: normalization does two things (composition offset AND removal of within-condition loading variance); four-row table of the variants; "hundreds of proteins at once" replaced by the measured 31 FP in 111 calls; Insight 3, the decision-tree row and the failure mode reworded (no longer "the offset alone"); second check added beside the offset guard: `resid_sd()` before/after ratio against `SD_RATIO_MIN` (warning) | ran: residual SD ratio 0.757 (per-run median, all peptides), 0.735 (complete-case), 0.757 (within-condition centring, offset +0.016), 1.000 (uniform -0.20). Shipped block A: 286 tested / 80 calls / 0 FP / median -0.005. With `QFeatures::normalize(method = 'center.median')` inserted per the new text: warning `residual SD fell to 0.75`, 112 calls / 32 FP, offset stop at -0.202 | second independent measure of the same claim: MSstats SE ratio default / none = 0.585 |
| MSstats block ships the normalization the Skill blames (Input 9) | P2 | comment on the `normalization` argument pointing at the checks, `FALSE` offered with the measured consequence inline and in the Approach; MSstats route of the SD check = compare `median(tested$SE)` across the two fits | ran block verbatim: 290 tested / 101 calls / 21 FP / median -0.184 / median SE 0.119; with `normalization = FALSE`: 79 calls / 0 FP / +0.008 / SE 0.204 | I kept `'equalizeMedians'` as the shipped value (real data may need a normalization) and made the choice visible; `FALSE` requires protein-level normalization routed to proteomics/quantification |
| 0.05 threshold has no stated basis (Input 10) | P2 | named constants `OFFSET_MAX` and `SD_RATIO_MIN` at the top of the block, stated as empirical trip-wires from one 4 v 4 set, both directions of imperfection (harmless -0.20 would be stopped; within-condition centring passes the offset), and that passing does not certify the normalization; same constant in `examples/msqrob2_peptide_level.R` | ran the example: exit 0 on the audit data (80 calls, median -0.0048, 8 undetected) and on its own simulation (43 calls / 3 FP); `parse()` clean | |
| Two of three examples unreferenced (static) | P2 | `examples/limma_analysis.R` cited from the limma Approach, `examples/differential_abundance.py` from the Python Approach | text only; both examples untouched and exited 0 in the audit | |
| 398 lines, no progressive disclosure (static) | P2 | msqrob2, MSstats, centring checks, the per-run-normalization failure mode, their threshold rows and Common Errors rows moved to `references/feature_level.md`; SKILL.md keeps a "Feature-Level Workflows" pointer with the rules that hold on either route. SKILL.md 401 -> 288 lines | code blocks re-extracted and compared: the 6 protein-summary blocks are byte-identical to the previously audited revision; the two msqrob2 blocks moved byte-identical | Common Errors table stays in SKILL.md for the protein-level rows, per the audit's own split |

Decision: the msqrob2 executable question (brief section "Missing referenced executables") was closed in pass 4; nothing new written here beyond the residual-SD check, which ran.

## Redundancy removed (each fact stated once)

| deleted passage | now lives in |
|---|---|
| `usage-guide.md` "What the Agent Will Do" (9 steps) | SKILL.md Decision Tree, workflows (deleted; restates them) |
| `usage-guide.md` "Statistical Method Selection" table | SKILL.md Tool Taxonomy and Decision Tree |
| `usage-guide.md` "Missing-Value Handling" | SKILL.md Insight 1 and the imputation failure modes |
| `usage-guide.md` "Fold-Change Reporting" | SKILL.md Fold-Change Reporting; the two facts found only in the guide (raw FC with adj p and CI for tables; meta-analysis pools raw FC + SE, shrink afterwards) moved there |
| `usage-guide.md` "Tips" (13 bullets) | SKILL.md failure modes, workflows, Common Errors; "rigid near-vertical streaks are imputation artifacts" moved into the downshift failure mode's Symptom; the "matrix is log2 and normalized" tip moved into the Scope sentence |
| SKILL.md failure mode "FC + significance double filter" | SKILL.md Minimum-fold-change Approach (same mechanism and 50% regime figure) |
| SKILL.md failure mode "Per-run median normalization..." | `references/feature_level.md` (rewritten there with the corrected mechanism) |
| Downshift failure mode Mechanism (restated the constant and SD) | reduced to a pointer to Insight 1 |
| Thresholds rows: residual df, d0, downshift constants, `trend=TRUE`, DEqMS min count, 50% FDR, feature-level offset row, ridge row | Insight 2, Insight 1, Approach text; the two feature-level rows moved to the reference |
| Common Errors rows: `$FDR` NULL, topTreat no `B`, trend=FALSE, min-FC inflates, treat trend, Student's t, Holm-Sidak, batch-effect anticonservative, anchor/wing | code comments and the failure modes / Approach they restate |
| Common Errors feature-level rows (7) | `references/feature_level.md` Common Errors |

Nothing the agent acts on left the Skill. Frontmatter untouched. SKILL.md, `usage-guide.md` and the new reference are pure ASCII.

## Left unfixed

None open. Not done: a second, independent data set for the two trip-wire constants (both were read off one 4 v 4 synthetic set, and the text says so).

