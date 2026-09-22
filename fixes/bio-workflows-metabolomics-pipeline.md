# Fix log: bio-workflows-metabolomics-pipeline (2026-09-16)

Worktree `F:\OpenScience\wt\metab-a`, branch `fix/r2-metab-a`, commit `8eced48`.

| Finding | Priority | Change | Verified | Notes |
| --- | --- | --- | --- | --- |
| Stage2->Stage4 hand-off crashes on real multi-batch data: imputation is a comment, not code | P1 | Inserted a real imputation step between `pqn_normalisation` and `opls()`. Investigation went deeper than "add `impute.QRILC`": `QCRSC` silently wipes a whole batch to all-NA when it has fewer QCs than `minQC` (5 of MTBLS79's 8 batches had 4), and `impute.QRILC`'s per-sample quantile model then errors `0 (non-NA) cases` on a 100%-NA column. Fixed by dropping wholly-NA samples (report + drop, don't fabricate) before the log2/2^x QRILC round-trip already established in `normalization-qc`'s fix. | Ran (real data) | Verified end to end on the audit's real MTBLS79 data: 90/172 samples dropped, 82 survive (<=18% per-sample NA), QRILC imputes cleanly (min 11.77, no negatives), Stage 4 `opls()` (via `statistical-analysis`'s `fit_discriminant_guarded`) fits successfully, `pR2Y = pQ2 = 0.001`. |
| Stage1->Stage2 orientation comment contradicts its own code | P1 | Removed the erroneous `fm <- t(feat)`; `featureValues()` is already features x samples. Added `stopifnot` dimension check against `featureDefinitions()` row count and sample count. | Ran (real data) | Verified against the audit's real xcms `featureValues()` output (574 real faahKO features x 12 samples) -- matches the auditor's own Attempt B. |
| Two of three governing commitments (mode-lock, MSI-confidence gate) have no enforcing code anywhere | P1 | Added a Stage 3 snippet threading a `mode` column through the feature table (with a mixed-mode split branch), and a Stage 5 snippet filtering `identified_compounds` to MSI Level 1-2 rows before `Setup.MapData` (`stopifnot` on empty output). Stage 5's ORA call also brought in line with `pathway-mapping`'s fixed pattern (`current.msg` predeclaration, `Setup.KEGGReferenceMetabolome`, Local-Only-ORA fallback note) rather than the old no-op `SetMetabolomeFilter(TRUE)`. | Parsed; illustrative (defers to component Skill for live execution, matching the orchestrator's existing style for Stages 1/3/5) | Consistent with `metabolite-annotation`'s `assign_level()` output convention (`1`, `'2a'`, `'2b'`, `3`, `4`, `5`). |
| The bundled example never exercises the seams it claims to unify | P2 | Added `examples/pipeline_handoff_check.R`: a second bundled example chaining REAL `pmp` (`filter_peaks_by_fraction`/`QCRSC`/`filter_peaks_by_rsd`/`pqn_normalisation`) and REAL `ropls` (guarded fit) calls across a small synthetic multi-batch table shaped like the real failure (one batch with 3 QCs, below `minQC=5`). | Ran | Drops 13 of 29 wiped samples, imputes cleanly, fits OPLS-DA (`pR2Y = pQ2 = 0.014`). The existing `examples/metabolomics_workflow.R` re-ran unmodified and still passes (20/20 true hits recovered). |

## Left unfixed

- The P2 fix's suggestion to chain a *real* xcms Stage 1 (not a synthetic stand-in) into the new
  example was not attempted -- that needs real mzML files and instrument-specific parameters,
  which is `xcms-preprocessing`'s own bundled-example scope, not this orchestrator's. The new
  example starts from a `featureValues()`-shaped synthetic table instead, matching the existing
  `metabolomics_workflow.R`'s convention.

## Verification

- R 4.4.3, pmp 1.18.0, ropls 1.38.0, imputeLCMD 2.1, via the candidate's `rs.sh`.
- All 5 R code blocks in `SKILL.md` parse-checked (`Rscript -e "parse(...)"`); both
  `examples/*.R` files run clean end to end (see table above).
- Real audit data used: `F:\OpenScience\audit-envs\untargeted-metabolomics-analyst\public-data\MTBLS79\`
  (2433 features x 172 samples, 8 batches) and
  `F:\OpenScience\audits\bio-metabolomics-xcms-preprocessing\run\feature_table_input1.csv`
  (574 real faahKO features x 12 samples), both read-only.

# Fix log: bio-workflows-metabolomics-pipeline (2026-09-21)

Worktree `F:\OpenScience\wt\workflows-metabolomics-pipeline`, branch `fix/workflows-metabolomics-pipeline` (from staging `431aa55`). Commits: `59d2c3e` (fix + redundancy), `20b676d` (split), `ac3fdd2` (scripts/). Env `untargeted-metabolomics-analyst` (R 4.4.3, xcms 4.4.0, MsExperiment 1.8.0, pmp 1.18.0, imputeLCMD 2.1, ropls 1.38.0, MetaboAnalystR 4.3.0). SKILL.md 311 -> 349 lines after fixes and moved-in content, then 278 after the split, 253 after scripts/.

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| MS-DIAL alternate entry point has no glue code | P2 | Added a block (now `scripts/msdial_import.R`, run from `references/msdial-front-end.md`) turning an `AlignResult-*.mdalign` export into `feat`, `defs`, `sample_class`, `injection_order`, `batch_id`. Not-detected 0 -> NA (756 zeros in the real export), Blank/Standard injections excluded, RT minutes -> seconds. | Ran: real MSDIALCUI 5.5.260820 export (16437 x 2); synthetic 3-batch export with QC/Blank/Standard columns chained into Stage 2 verbatim, 20 wiped samples dropped, NA-free imputed matrix | Real export has no QCs, so the QC path is only exercised on the synthetic export |
| `impute.QRILC` unseeded | P2 | `set.seed(123)` before the call, now in `scripts/stage2_qc_impute.R` | Ran: Stage 2 twice on real MTBLS79 (90/172 dropped, 82 kept), imputed matrices identical | |
| No bundled example runs real xcms into Stage 2 | P2 | none | n/a | see Left unfixed |
| (found while running) `library(xcms)` alone does not attach MsExperiment, so `readMsExperiment()`/`sampleData()` fail in Stage 1 | not in audit | `scripts/stage1_xcms_extract.R` also calls `library(MsExperiment)` | Ran: 6 real faahKO CDFs (2 labelled QC), 2605 features x 6 samples; before the change the same call died with `could not find function "readMsExperiment"` | |
| (found while running) Stage 5 `reference_metabolome.txt` format unstated | not in audit | comment: one KEGG compound ID per line, names fail | Ran: names in the file gave "Over half of your uploaded IDs cannot be matched"; KEGG IDs passed mapping; consistent with pathway-mapping's own comment | |

## Left unfixed

- **Third bundled example chaining real xcms output through all 5 stages (P2).** It is new content, and no dataset on this machine can carry it: the only real raw files are faahKO (no pooled QCs, no batches, so Stage 2's drift, RSD and QCRSC steps have nothing to run on) and MTBLS79 ships as a processed matrix, not raw. Stage 1 (real xcms) and Stage 2 (real MTBLS79) are each run end to end in the scripts/ verification above.
- **Stage 5 MetaboAnalystR ORA block not run to completion.** With KEGG-ID input it maps, then `CalculateOraScore` fails with "Failed to connect to the API Server" (needs xialab.ca; the block's own comment says the call can be rejected). It stays inline in `references/stage5-pathway-mapping.md`, not moved to scripts/, because a script that cannot be run here would violate the run-it rule.
- **Stage 4 block not moved to scripts/.** It calls `fit_discriminant_guarded()`, defined only in metabolomics/statistical-analysis, so it is not standalone. It was checked as part of the Stage 2 run above (function copied from the audit's own script).

## Redundancy pass

| deleted passage | new home |
| --- | --- |
| usage-guide `Prerequisites` install line (`BiocManager::install(...)`) | SKILL.md "Install:" line under Version Compatibility |
| usage-guide conceptual prerequisites (QCs 1 per 5-10 samples, metadata columns, randomized groups) | SKILL.md "Required Inputs" |
| usage-guide `Required Inputs` and `Sample Metadata Format` (CSV) | SKILL.md "Required Inputs" (CSV kept) |
| usage-guide `What the Agent Will Do` (5 stages) | SKILL.md Stage 1-5 sections and Pipeline Flow (restated, nothing unique) |
| usage-guide `Tips` (6 bullets) | SKILL.md commitments 2-3, QC Checkpoints, Stage 5 and Alternative Front End (all restated; nothing unique) |
| SKILL.md Stage 2 trailing sentences on half-min replacement and feeding `normalized` to Stage 4 | Common Errors rows "Significance explodes after imputation" and "opls() ERROR missing value ..."; Stage 2 sentence "`imputed` (not `normalized`) is what Stage 4 receives" kept |

Verified by grep on each phrase in the new SKILL.md.

## Split (SKILL.md 349 -> 278 lines)

Stage 1, Stage 5 and the MS-DIAL front end moved verbatim to `references/stage1-xcms-extraction.md`, `references/stage5-pathway-mapping.md`, `references/msdial-front-end.md`; index in SKILL.md "Reference Files" plus pointers in the Stage 1 and 5 table rows. Multiset comparison of non-blank lines: none lost (only the two edited table rows and stubs differ); all r fences parse.

## Moved to scripts/ (SKILL.md 278 -> 253 lines)

| old location | script |
| --- | --- |
| references/stage1-xcms-extraction.md, xcms block | `scripts/stage1_xcms_extract.R` |
| SKILL.md Stage 2 block | `scripts/stage2_qc_impute.R` |
| references/msdial-front-end.md, import block | `scripts/msdial_import.R` |

`examples/pipeline_handoff_check.R` runs the same pmp/ropls calls on a self-generated synthetic table and was left untouched. The Stage 2 script is the reusable form on the user's own objects, so I judged it not a duplicate of the example. Each script was run exactly as SKILL.md invokes it (`source('scripts/...')` from the Skill directory).
