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
