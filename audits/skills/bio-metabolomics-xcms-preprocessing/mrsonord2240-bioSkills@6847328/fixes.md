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
