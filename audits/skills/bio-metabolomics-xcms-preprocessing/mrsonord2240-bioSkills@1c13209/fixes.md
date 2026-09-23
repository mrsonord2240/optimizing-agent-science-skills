# bio-metabolomics-xcms-preprocessing fixes (2026-09-16)

Worktree `F:\OpenScience\wt\metab-b`, branch `fix/r2-metab-b` (based on `openscience-fixes` @
61e60d8). Runtime: R 4.4.3 / Bioconductor 3.20 via
`F:\OpenScience\audit-envs\untargeted-metabolomics-analyst\rs.sh`; xcms 4.4.0, MsExperiment
1.8.0, CAMERA 1.62.0. Data: real faahKO CDFs at
`F:\OpenScience\audit-envs\untargeted-metabolomics-analyst\public-data\faahKO` (KO/WT, 6 files
used per run, a subset of the audit's own 12-file cohort).

Scope per Sam's 2026-09-16 override: fix every finding in
`eval_report_bio-metabolomics-xcms-preprocessing_result.json` (`recommendations[]`) — this Skill
carries 1 P1 (the assertion-rate cap, whose root cause is a set of six small assertion-level
gaps) and 4 P2s, no P0. `AUDIT.md` names the same P1 (assertion pass rate) as this Skill's
open item and no other defect specific to this Skill.

## Findings

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `PeakGroupsParam(minFraction=0.85, ...)` — SKILL.md's own commented alternative-alignment example — fails with a cryptic low-level error ("attempt to set 'colnames' on an object with less than two dimensions") on a real small-anchor-count run | P1 | Retention-Time Alignment section: added a paragraph explaining `minFraction`/anchor-count fragility and the two failure modes to expect; changed the commented example's `minFraction` from 0.85 to 0.5 with a note to raise only after confirming enough peak groups survive; added a Common Errors row for the same failure | ran | The auditor's own diagnostic sweep (`eval_viewer_...md`, Input 2) on the real 12-file/6-WT-anchor cohort is the primary evidence: `minFraction=0.5` OK, `0.7` "Not enough peak groups", `0.85`/`1.0` the cryptic colnames error. Independently re-ran on a smaller 6-file/3-WT-anchor real faahKO subset: `minFraction=0.5` (the new documented default) → OK in both subsets tested; `0.85` was data/anchor-count sensitive (succeeded on this smaller subset's 152 peak groups, failed on the auditor's larger cohort) — this variability is exactly the fragility the new guidance describes and is why the doc now tells users to start low and confirm peak-group count before raising it, rather than asserting 0.85 always fails. |
| `featureValues()` can retain NA cells after `fillChromPeaks` (240/6888 in the audit's run) with no SKILL.md guidance on the case | P2 | Gap-Filling section: added a sentence that residual NAs are genuine non-detections, not fill failures, plus a `sum(is.na(feat))` line in the code block | ran | Reproduced independently on a 6-file real faahKO run: 267 residual NA cells in a 722×6 matrix after `fillChromPeaks(ChromPeakAreaParam())` — same phenomenon at a different sample count, confirming this is a real, reproducible xcms behavior and not an audit-specific artifact. |
| Redundancy Collapse code block shows only `library(CAMERA)`; running it against a saved `xdata` in a fresh session fails with `could not find function "sampleData"` | P2 | Added `library(xcms); library(MsExperiment)` to the top of the Redundancy Collapse code block, before `library(CAMERA)`; added a matching Common Errors row | ran | Negative control (old block, `library(CAMERA)` only, fresh session, real saved `xdata` RDS): reproduced the exact audit error, `could not find function "sampleData"`. Positive control (fixed block, same fresh session, same RDS): completed cleanly — 722 peaklist rows, 381 pseudospectra groups, 161 isotope-flagged features, real CAMERA output. |
| No `minFraction` guidance for very small cohorts (e.g. n=2/group), where the 0.5/0.85 examples don't apply | P2 | Correspondence section: added a sentence to re-derive `minFraction` as a fraction of the smaller group for very small cohorts (e.g. 1.0 for n=2/group) | docs | Not independently executable (no n=2 dataset in the audit env, same limitation the audit itself noted for this input); the guidance follows directly from `PeakDensityParam`'s documented `minFraction` semantics (fraction of samples in a group a peak must appear in) — mathematically, any value below 1.0 at n=2 admits single-replicate detections. |
| No purpose-built escape hatch against deadline/publication-pressure requests to skip gap-fill tracking or QC filtering for more "hits" | P2 | Added one sentence to "The Single Most Important Insight" naming this pressure scenario as consequence (2) (gap-filling fabrication) and pointing to the failure-mode entry | docs | Prose-only addition cross-referencing an already-verified mechanism (gap-filling fabrication, itself demonstrated via Input 1's real 0.197 filled-fraction run in the audit); no new code to execute. |
| Assertion pass rate (79.3%) caps grade at Beta Only | P1 (meta) | Direct consequence of fixing the five findings above — each was tied to a specific failing assertion (Input 1's NA-guidance, Input 2's PeakGroupsParam robustness x2, Input 3's small-cohort minFraction, Input 4's cross-session library(), Input 7's escape hatch) | n/a | Not re-scored here (a different agent re-audits); this row records that the fix targets the assertions' underlying defects, not the wording. |

## Unfixed

None. All five `recommendations[]` entries and the one `AUDIT.md` open item for this Skill are
addressed above.

## Files changed

- `metabolomics/xcms-preprocessing/SKILL.md`

## 2026-09-21: P2 fix batch (Production Ready, 92)

Worktree `F:\OpenScience\wt\metabolomics-xcms-preprocessing`, branch `fix/metabolomics-xcms-preprocessing` (from staging `main` 431aa55), commit bb934d8. Env `untargeted-metabolomics-analyst` via `rs.sh`: xcms 4.4.0, MsExperiment 1.8.0, R 4.4.3. Data: real faahKO CDFs (the audit's data; no synthetic set). Nothing installed.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `MatchedFilterParam` named in the Decision Tree with no example or parameter guidance | P2 | Peak Detection: worked `MatchedFilterParam(binSize = 0.1, fwhm = 30, snthresh = 10, steps = 2)` block plus notes (`fwhm` = measured EIC FWHM in s, `sigma = fwhm/2.3548`, `binSize` = m/z slice, `mzdiff` default `0.8 - binSize*steps`); decision-tree row points to it | ran + help | Block run verbatim on 1 KO + 1 WT faahKO: 930 peaks (470/460), columns mz/rt/into/sn present. `fwhm = 10` on sample 1: 276 peaks vs 470 at 30. `mzdiff(MatchedFilterParam())` = 0.6 = 0.8 - 0.1*2. Defaults checked against `?MatchedFilterParam`. Per-instrument-class starting values NOT given: no evidence beyond the docs' defaults and the run, so `fwhm` is tied to the measured EIC width instead. |
| AutoTuner / IPO: one unelaborated Decision Tree cell | P2 | Claim deleted (brief option 3): row now says start from Quantitative Thresholds, measure base-widths on 5-10 known EICs, iterate `peakwidth`/`snthresh`/`ppm`; AutoTuner/IPO kept only as a caution ("not covered here", McLean 2020). New EIC snippet in Peak Detection using `chromatogram()` + `plot()` supplies the "verify against EIC width" step the row depends on | ran | `IPO` and `AutoTuner` are not installed in the env (`requireNamespace` FALSE) and installs are forbidden, so no runnable block could be written. EIC snippet run on the strongest faahKO peak (mz 508.2, rt 3514 s): 77-point chromatogram, peak FWHM about 39 s; `plot()` to a null device OK. |
| `minFraction` guidance does not distinguish 2 replicates of one condition from 1 sample per condition | P2 | Correspondence: `minFraction` is per sample group; 2 replicates of one condition -> 1.0 vs 0.5 differ; 1 per condition -> every value in (0,1] identical and `minSamples = 2` returns 0 features; to require presence in both, use one group (`sampleGroups = c('all','all')`) | ran | faahKO, CentWave (ppm 25, peakwidth 20-80) + obiwarp then `PeakDensityParam(bw = 5)`: 2 KO replicates 259 (1.0) vs 2158 (0.5); 1 KO + 1 WT as two groups 1926/1926 in one run and 1877/1877 in the second (different files), `minSamples = 2` 0 features; same pair as one group 319 (1.0) vs 1877 (0.5); 2 KO + 2 WT 348 vs 3469. Assertions in scripts checked equality and inequality. Went beyond the audit's suggested clause: its "no true replicates" advice was incomplete because `minSamples` also cannot substitute. |

### Left unfixed

None.

### Redundancy pass (usage-guide.md vs SKILL.md)

| deleted passage (usage-guide.md) | new home |
|---|---|
| Prerequisites: `BiocManager::install(c('xcms', 'MsExperiment', 'Spectra', 'CAMERA'))` | SKILL.md Version Compatibility ("Install:", with checked versions) |
| Prerequisites: centroid in software with a documented algorithm, not irreversible on-instrument centroiding | SKILL.md Decision Tree, "Profile data of any kind" row |
| Prerequisites: record sample design (groups, QCs, blanks, injection order) per file | SKILL.md Peak Detection, `readMsExperiment` comment |
| Prerequisites: feature table is a parameterized result reported with its processing spec | already in SKILL.md (Version Compatibility, Insight); deleted |
| Tips: CentWave vs MatchedFilter, `peakwidth` c(20,50) default, `ppm` 2-3x scatter | already in SKILL.md (Decision Tree, failure modes, Quantitative Thresholds); deleted |
| Tips: align to pooled QC, not file #1 (outlier propagates) | SKILL.md Retention-Time Alignment approach |
| Tips: inspect RT-deviation plots and EICs, alignment can look perfect in QCs | SKILL.md Retention-Time Alignment approach (plus Insight, Decision Tree row) |
| Tips: filled values are imputations, track `is_filled`, MNAR-aware imputation | already in SKILL.md (Gap-Filling, failure mode); deleted |
| Tips: finding surviving one parameter set is a candidate, not a result | SKILL.md Version Compatibility closing paragraph |
| What the Agent Will Do (7-step restatement of the workflow) | already in SKILL.md workflow line and per-step sections; deleted |
| Overview restating the description | shortened to two sentences pointing at SKILL.md |

Both files keep a Related Skills list (guide's, per the brief, and SKILL.md's); left as is. One example prompt (low-res quadrupole run) added to the guide.

### Scripts / split

SKILL.md 236 -> 255 lines: under the 300-line threshold, no split. `scripts/`: the largest fenced block is 12 lines (Peak Detection); none is at the ~15-line threshold, so nothing moved. All 8 fenced R blocks parse (`parse()`). `examples/xcms_workflow.R` untouched; re-run as a regression check, it completes (4 files, 4667 peaks, 2931 features, filled fraction 0.496).

## 2026-09-22: Phase 1 final pass

Worktree `F:\OpenScience\wt\metabolomics-xcms-preprocessing`, branch `fix/metabolomics-xcms-preprocessing` (tip before this pass: `bb934d8`). Runtime: R 4.4.3 / Bioconductor 3.20 via `F:\OpenScience\audit-envs\untargeted-metabolomics-analyst\rs.sh`; xcms 4.4.0, MsExperiment 1.8.0, CAMERA 1.62.0. Data: real faahKO CDFs and the saved 12-file audit result. Nothing installed.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Retention-Time Alignment instructed pooled-QC alignment but the `ObiwarpParam` block did not pass QC indices; the commented `PeakGroupsParam` alternative also used undefined `pdp_anchor` | P2 | The obiwarp block now builds `qc_idx`, uses `ObiwarpParam(..., subset = qc_idx, subsetAdjust = 'average')` when >=2 QCs are present, and clearly falls back to full-cohort alignment otherwise. The peakGroups alternative now defines `pdp_anchor`. | ran + docs | Installed xcms 4.4.0 vignette documents subset-based alignment for both parameter classes. Full serial execution against real faahKO passed: 10,826 obiwarp-adjusted peaks, `PeakGroupsParam(minFraction = 0.5)` QC subset OK, then 497 features, 137 residual NAs, CAMERA 497-row peaklist, and QC filters 497 -> 79 -> 32. All 8 fenced R blocks parse. |

### Left unfixed

None. All prior recommendations and the final-pass revisit item are resolved; no install, authentication, licence, data, or decision blocker remains.
