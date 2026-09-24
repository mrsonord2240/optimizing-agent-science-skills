# bio-proteomics-data-import fixes (2026-09-15)

Branch `fix/proteomics` (worktree `F:\OpenScience\external\bioSkills-wt-proteomics`). Runtime: candidate venv, pyOpenMS 3.5.0, pandas 3.0.5, numpy 2.5.3. SKILL.md Python blocks were extracted and run verbatim on copies of the audit data (`proteinGroups.txt`, `report.parquet`, `synthetic_mixed.mzML`).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| DIA-NN import omits `Global.PG.Q.Value` | P1 | Added to the DIA block, DIA-NN decision-tree row, Stale-parsing fix, Quantitative Thresholds row and usage guide; `Lib.PG.Q.Value` named for 1.9.x library-based MBR | ran: matrix 887 x 8, 0 LOWCONF groups (audit: 947 / 60) | matches sibling dia-analysis filter |
| DIA missingness labelled MCAR against the Skill's own diagnostic | P1 | Description, insight 1, DIA decision-tree row, missingness Approach and MNAR failure mode now say DIA has fewer but still mostly intensity-dependent missing values and the imputer is chosen from the diagnostic; cites Hediyeh-zadeh 2023 (msImpute, MCP 22(8):100558) | ran: diagnostic DIA -0.495, DDA -0.619 | method evidence: audit Input 5 (missing DIA cells in lowest abundance quartile, KNN bias +0.47) |
| DIA block keeps PG.MaxLFQ zeros (-inf after log2) | P1 | `matrix = np.log2(matrix.replace(0, np.nan))` after the pivot; Approach states `assess_missingness` expects log2 with NaN; Common Errors row names PG.MaxLFQ | ran: 0 -inf | |
| mzML loop crashes on MS2 scans without precursor | P1 | Guard `if not precs: continue`; warn when lower+upper offset == 0; Approach text and Common Errors row | ran: loop completes over 20 spectra; scan 18 flagged "offsets not written" | |
| Silent failure modes in the MaxQuant block | P2 | Raise `ValueError` when no `LFQ intensity` columns; drop rows with no valid value (SKILL.md and `examples/load_maxquant.py`); >=2-peptide threshold row states it is not applied by the import code | ran: 1445 rows, 0 all-NaN (audit kept 55); no-LFQ table raises; example exit 0, `py_compile` OK | |
| pyOpenMS misattributed to Chambers 2012 | P2 | Taxonomy cites Rost 2014; reference added | docs: Rost HL et al. Proteomics 2014;14(1):74-77 | Chambers 2012 kept for msconvert |

Also: version line changed from "pyOpenMS 3.1+, pandas 2.2+, numpy 1.26+" to the checked versions.

Left unfixed:
- P2 "R route named but no QFeatures code": adding a QFeatures code block is new content, out of scope.

## Final pass (2026-09-24)

Exact source commit: `mrsonord2240/bioSkills@622daddbf14af58b9a83bdae2d586133ba35b2a6:proteomics/data-import`.

| finding | priority | correction | exact-source evidence |
|---|---|---|---|
| MaxQuant TMT table has no usable route | P1 | Added a `Reporter intensity corrected <channel>` import block, decision-tree row, and a no-LFQ error that names TMT rather than suggesting non-existent per-sample `Intensity` columns. Reporter correction/normalization remains routed to quantification. | Fresh synthetic TMT10 fixture: 10 corrected channels, 390 x 12 finite-or-missing log2 matrix. |
| All three bookkeeping fields absent yields `KeyError: True` | P2 | Replaced scalar `.get()` masking with a row-indexed keep mask; all fields absent now raises a named MaxQuant-table error. | Fresh flagless table raises `ValueError` naming the missing bookkeeping columns. |
| QFeatures route was named but not executable | P2 | Added `examples/load_maxquant_qfeatures.R` and a concise `make.names()` QFeatures block; clarified that proteinGroups is already protein-level. | Source surface added; no fresh clean R-process result is claimed in this pass. |
| Import cleaning had no methods-record count | P2 | Added read, post-bookkeeping, and quantified row counts to the LFQ block and example. | Archived MaxQuant regression reports 1560 read, 1500 after bookkeeping, 1445 quantified. |

## Final verification completion (2026-09-24)

- Added and ran the missing packaged `load_diann.py` and `inspect_mzml.py` examples, alongside the MaxQuant example.
- Ran the new QFeatures example on the archived label-free table in a bounded 60-second Windows R process. Its first normal process completed output but faulted during teardown; a retained process-local `cli` cleanup-guard run exited 0, wrote its receipt, and returned `1500 x 8` with no `-Inf`. The guard was audit-only and was not added to the Skill or installed globally.
- Corrected the raw-format promise too: `.mzML` now uses `MzMLFile`, `.mzXML` uses `MzXMLFile`, and a fresh generated mzXML check matches the source fixture's MS1/MS2/all-ion/window counts.
- Exact-source evidence is now six archived executions plus four fresh checks, all passing, under `F:\OpenScience\audits\bio-proteomics-data-import\final-pass-20260924\`.

Canonical report: **95/100, Production Ready, deployable**. Final-pass metadata is deliberately `auditor_independent: false`; final pass: fixed and audited under one brief, see `CHECKPOINT.md`.
