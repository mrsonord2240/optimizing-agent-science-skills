# bio-proteomics-proteomics-qc fixes (2026-09-15)

Candidate `mass-spec-proteomics-analyst`. Worktree `F:\OpenScience\external\bioSkills-wt-proteomics-b`, branch `fix/proteomics-b`, commit `f3ad60f`. Runtime: candidate venv (pandas, scikit-learn, scipy); R 4.4 with MSstatsTMT 2.14.2 via `r.sh`; audit data `audits/bio-proteomics-proteomics-qc/data` (copied to scratchpad).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `raw_sample_qc` counts MaxQuant zeros as quantified | P1 | `replace(0, np.nan)` inside; zeros-are-missing sentence (MaxQuant, DIA-NN PG.MaxLFQ) | ran on `proteinGroups_failed.txt`: T4 1031 IDs, 31.3% missing (was 1500, 0%) | |
| Un-normalised column never named; no ID threshold | P1 | MaxQuant `Intensity`, DIA-NN `Precursor.Quantity`, raw TMT reporters named; `raw_sample_qc(raw, sample_groups)` adds fold-vs-group total and IDs, flag at <=0.5x total or <0.8x IDs; prose applies the rule to total signal, not boxplot median; failure mode updated | ran: failed file flags T4 on `Intensity` (0.41x total, 0.81x IDs), not on `LFQ intensity`; clean file flags nothing | DIA-NN column names from audit Input 2 run |
| `pca_batch_check` crashes / centres failed sample | P1 | Sample-index check with explicit error, complete cases instead of row-median fill, `n_components=min(5, n-1)`; Common Errors row | ran: RangeIndex raises clear ValueError; n=4 runs (3 PCs); T4 centroid distance 36.0 vs <=15.4 for others | |
| MSstatsTMT QC plot post-normalisation by default | P1 | Decision-tree row: `proteinSummarization(..., global_norm = FALSE, reference_norm = FALSE)`, PSM-level input; new `tmt_channel_balance()`; Common Errors row | ran: MSstatsTMT 2.14.2 with both FALSE, channel medians 23.96-24.52 (A) / 24.93-25.39 (B); balance code: 0 flags on audit plexes, flags a channel scaled 0.3x | Args from `args(proteinSummarization)` |
| PTXQC ">1%" contaminant flag misattributed | P2 | Lab-baseline + group-difference wording; `contaminant_fraction()`; example print aligned | ran: 4.19-6.52% on audit table | Attribution per audit's PTXQC 1.1.5 help check |
| Dead `abundance_bins`; "~14x" | P2 | `missingness_profile` returns present fraction per abundance bin; compression worded as ln2 x mean log2 (15-20x typical) in two places | ran: profile 0.34 -> 0.98 rising; 17.6x at mean log2 25.7 (ln2 x mean = 17.8) | |
| Batch guidance inconsistent; no stop conditions | P2 | Batch in design for the test, `removeBatchEffect`/ComBat for plots only; one stop-conditions sentence | text only | |
| Example median-fill PCA | -- | Complete cases, matching the Skill | ran: py_compile, exit 0, ctrl_3 still flagged | |

Unfixed: QC-report / exclusion-decision template and DIA/Level-1/2 code (new content, out of scope). DIA-NN "High precision" claim remains unverified (no DIA-NN here).

## Pass 2 (2026-09-15)

No change; left byte-identical. The re-audit (86, Production Ready) reports no P1 and no demonstrated defect in what runs -- every open item is a P2 asking for new content (commands, code for a prose-only step, a report template) or a wording softening, which the brief puts out of scope.

Also **not tested: the DIA-NN "High precision mode halves median CV" claim**, so the sentence is unchanged. It is not cheap here: the earlier library-free run under `audit-envs/.../public-work/diann_libfree` died during spectral prediction and left `diann_out` empty, so there is no library and no `.quant` file to reuse -- testing it means two full library-free DIA-NN runs over a 7.75M-precursor predicted library for three Astral runs. And PXD070049 has one replicate per condition (its own README says there is no CV or replicate-precision check), so a within-condition median CV cannot be computed from this data at all. Needs either a replicated dataset or a budgeted DIA-NN run.

## Pass 5 — 2026-09-15 (re-audit at 85, Limited Release; assertion floor 90% missed at 87.2%)

Branch `fix/proteomics-5` (worktree `F:\OpenScience\external\bioSkills-wt-prot5`), branched from
`openscience-fixes` @ `1110c24`. Commit `95a8460`. Evidence: the batch-C re-audit at
`F:\OpenScience\audits\bio-proteomics-proteomics-qc\` (19:10), which ran each script more than once
and on real single-replicate DIA data. Runtime: Python 3.12 shared venv (pandas 3.0.5, numpy 2.5.3,
scikit-learn 1.9.1), R 4.4.3 via `r.sh` (PTXQC 1.1.5, rmarkdown 2.31), Pandoc 3.11, DIA-NN 2.6.1
output. All six SKILL.md python blocks were extracted programmatically and `exec`'d — nothing retyped.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `pca_batch_check` is not reproducible: `PCA(n_components=n_pc)` has no `random_state`, and sklearn's `'auto'` solver is randomized on a wide matrix | P1 | `PCA(n_components=n_pc, svd_solver='full', random_state=0)` in SKILL.md and in `examples/qc_analysis.py`; a Version Compatibility sentence ("seed anything stochastic and re-run it once"); a Common Errors row | ran, twice over: on the audit's 20 x 600 TMT matrix the OLD line gave **6 distinct** PC3~plex p-values over 6 identical fits (0.987768, 0.988524, 0.989106, 0.989532, 0.989552, 0.991638); the fixed line gives **1** (0.988923). Six calls of the fixed `pca_batch_check` produce one identical printed block and one identical `explained_variance_ratio_`. The example prints byte-identical output on two runs | `'full'` is exact, not just seeded; at QC sizes (tens of samples) it is free |
| Three checks degrade silently at n = 1 per group: `replicate_correlation` -> 0 rows, `median_cv_linear` -> NaN, loading rule inert (`fold_total_vs_group` identically 1.0) | P1 | `replicate_correlation` and `median_cv_linear` raise `ValueError` with the group sizes when no group has >=2 samples (and warn per-group otherwise); `raw_sample_qc` detects single-sample groups, warns, adds a `baseline` column and falls back to the all-sample median; a decision-tree row and a prose paragraph state the design requirement | ran on real PXD070049 DIA-NN 2.6.1 output (3 Astral runs, one per condition, 1619 precursor rows after global-q filtering): both functions raise with `{'A': 1, 'B': 1, 'C': 1}`; `raw_sample_qc` prints the warning and reports the ALL baseline with folds 0.901 / 1.127 / 1.000 and IDs 1.000 / 1.004 / 0.994 — the same numbers the auditor got by hand-building that baseline | |
| `pca_batch_check` raised `TypeError: At least two samples are required; got 1` from a correctly-indexed `sample_info` when a batch level has one sample | P1 (part of the above) | Guard before `f_oneway`: prints `NOT TESTABLE` with the level sizes and "this is not evidence of no batch effect" | ran on the same 3-run DIA matrix: `PC1 ~ batch: NOT TESTABLE, level sizes [1, 1, 1]`, PC2 likewise, function returns coords + `[0.6903 0.3097]` instead of raising | |
| Pandoc claim (dispatch item): the earlier premise that Pandoc blocked `createReport()` was wrong | P1/P2 | Decision-tree row and taxonomy row now say `createReport()` writes PDF + mzQC + heatmap + YAML with no extra dependency and HTML **only** when Pandoc is reachable; a Common Errors row explains the message is not fatal and how to point at Pandoc | ran twice on the same MaxQuant `txt/` folder: clean session -> `rmarkdown::pandoc_available()` FALSE, `Sys.which("pandoc")` empty, PTXQC prints "The 'Pandoc' converter is not installed on your system", call **completes**, writes `report_v1.1.5_*.pdf` 60.6 kB + `.mzQC` + `.yaml` + `_heatmap.txt`, **no HTML**. With `RSTUDIO_PANDOC=.../tools/pandoc/pandoc-3.11` -> `pandoc_available()` TRUE, same PDF plus a **1400 kB HTML** | Pandoc 3.11 is installed but NOT on PATH, so a clean session still prints the message. The Skill documents that rather than the old claim or the old workaround |
| Common Errors misattributes `At least two samples are required; got 1` to a RangeIndex alone | P2 | Row now names both causes and points at the `NOT TESTABLE` output | ran: RangeIndex still raises the Skill's own explicit `ValueError`; the correctly-indexed single-sample case now prints `NOT TESTABLE` | |
| No warning that a batch fully confounded with condition cannot be corrected at all | P2 | One sentence in the PCA prose: non-identifiable, do not correct and do not test | audit run (Input 8): mean \|log2FC\| on 104 true DA proteins 1.546 -> 0.000 after batch removal on a fully confounded design | not re-simulated; figure from the audit |

Regression on the audit's synthetic data with the edited blocks: T4 flagged on `Intensity` and not on
`LFQ intensity` in `proteinGroups_failed.txt`, nothing flagged in the clean file; replicate r
0.956–0.966 over 12 pairs; median CV 24.3% / 23.6%; `PC1 ~ batch: p=0.0000`. All match the re-audit.
`examples/qc_analysis.py` `py_compile` clean, exit 0, `ctrl_3` still flagged. Files pure ASCII, CRLF
preserved.

## Left unfixed (pass 5)

- **P2 — Levels 1–2 and DIA matrix construction remain prose only.** Still new content: the Skill names
  the metrics and their thresholds but never claims to supply code for them, and adding RT/iRT-fit and
  FWHM extraction would be a new section rather than a correction.
- **P2 — sample-swap detection has no code.** Same reading. The decision-tree row tells the agent what
  to do ("check if it correlates better with a DIFFERENT group") and the audit found the swap by doing
  exactly that; the centred cross-group correlation would be a new function.
- **PTXQC's fixed-score behaviour** (a healthy 1,300-peptide dataset scoring ~0.08 on
  `Peptide Count (>15000)`, a 0.375x-loaded run scoring 1.0 on `Peptide Intensity (>23.0)`) is a real
  observation from Input 2, but that input scored 91/100 with 5/5 assertions PASS and the audit called
  it a demonstration **supporting** the Skill's control-chart thesis. Not a defect; deliberately not
  written in.

## Pass 6 -- 2026-09-21 (re-audit at 88.1, Production Ready; one open P1)

Branch `fix/proteomics-proteomics-qc` (worktree `F:\OpenScience\wt\proteomics-proteomics-qc`), commit `546864d`, from staging `main`. Runtime: shared venv Python 3.12, pandas 3.0.5, numpy 2.5.3, scikit-learn 1.9.1. All seven SKILL.md python blocks extracted and `exec`'d (11 functions); audit data copied read-only from `audits/.../data` and the real PXD070049 DIA-NN 2.6.1 report.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Degenerate-design caveats are `print()` only; partial-singleton designs return NaN / omitted rows with no machine-readable signal | P1 | `replicate_correlation` emits a row per singleton group (`r` NaN, `status = not_measurable_n1`) and a `status` column; `median_cv_linear` gets `status`; `pca_batch_check` returns a third value `tests` (`pc, p, status` = tested / not_testable); `raw_sample_qc` adds `loading_rule` (within_group / fallback_all_samples). Prose and the Common Errors row say to filter `status == 'measured'` | ran: 8-sample MaxQuant set -> all `measured`; 2/1/1 design -> Treatment row `not_measurable_n1`, CV NaN + status; batch levels [1,1,1] and [3,1] -> `not_testable` rows | `pca_batch_check` now returns 3 values (was 2); the example does not call it |
| Sample-swap check named in the decision tree, no code | P2 | New `cross_group_correlation` (centred r, top-300 variable proteins, own vs every other group, `possible_swap`); decision-tree row points at it | ran on the audit's C2/T3 swap: C2 (own -0.510, best Treatment 0.141) and T3 (own -0.508, best Control 0.132) flagged, nothing on the unswapped data; singleton own group -> `not_measurable_n1` | |
| Levels-1 RT/iRT fit and FWHM advertised, no code | P2 | New section "Level-1 Run Metrics From a DIA-NN Report" with `diann_level1` (RT vs Predicted.RT R^2 < 0.99, FWHM > 1.25x across-run median, `Quantity.Quality` reported only) | ran on the real 3-run report: R^2 0.9994-0.9998, FWHM 0.0475-0.0501, none flagged; FWHM x1.6 on one run flags it; Gaussian noise on one run's Predicted.RT gives R^2 0.28 and flags it | thresholds are the Skill's own Thresholds-table rows; 3 runs is a weak baseline (stated) |
| Example states no expected output | P2 | "Expected output" block in `examples/qc_analysis.py` docstring | ran twice: byte-identical stdout, matches the block; `py_compile` clean | |
| Redundancy (brief rule) | -- | see below | text | |

Deleted passages and where the content lives:
- usage-guide "What the Agent Will Do" (8 steps) -> restates SKILL.md sections in order; deleted.
- usage-guide Tips (10 bullets) -> each is in SKILL.md (raw first: intro + Default; control chart: insight 2; co-readouts: Level table + Decision tree; log2 / linear CV / MNAR / one run per condition / seeding / Pandoc: their sections + Common Errors). "Document and justify every exclusion, sensitivity check" existed only in the guide -> moved into the PCA/stop-conditions paragraph of SKILL.md.
- usage-guide Overview (metric list) -> shortened to two sentences pointing at SKILL.md; "NOT Bioconductor" comment on PTXQC -> in Common Errors.
- SKILL.md CV prose (ln2 x mean figure) -> kept only in the "CV computed on log-transformed data" failure mode; the PCA-seeding code comment shortened, explanation stays in Common Errors.

Left unfixed: QC report / exclusion-decision template (P2) -- new content, not a correction; the audit itself rates it as structure to add. DIA-NN "High precision" claim still untested (see Pass 2).

### 2026-09-21 addendum: QC report template written (requested by Sam)

The P2 "QC report / exclusion-decision template" left unfixed above is done: `references/qc-report-template.md` (dataset, checks run, exclusion log, with/without sensitivity, design limits, result), pointed to from the loading-rule paragraph, the TMT balance section and the PCA/batch paragraph. Thresholds are not restated in the template; it cites the function columns and the Quantitative Thresholds table. The example row (ctrl_3, 0.30x, 287 of 400 quantified) was checked against a run of `examples/qc_analysis.py`.
