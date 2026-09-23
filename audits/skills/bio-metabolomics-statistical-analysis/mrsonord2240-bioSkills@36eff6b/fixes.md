# bio-metabolomics-statistical-analysis fixes (2026-09-16)

Worktree `F:\OpenScience\wt\metab-a`, branch `fix/r2-metab-a` (already carries the
normalization-qc fix, `2dd138f`). Runtime: R 4.4.3 / Bioconductor 3.20 via
`F:\OpenScience\audit-envs\untargeted-metabolomics-analyst\rs.sh`; ropls 1.38.0. Data: the
Skill's own bundled `examples/metabolomics_stats.R` synthetic generator (n=40, p=300, 15 true
features) for the veto reproduction, and real `public-data/MTBLS79` for the Hotelling T2 check.

## Skill-veto pass -- 2026-09-16

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `ropls::opls(..., orthoI=NA)` (the Skill's own canonical OPLS-DA pattern) silently returns a 0-row `summaryDF` / empty model in ~40% of runs, with no error or warning even under `options(warn=1)` -- fired the skill veto | P0 (skill veto, operational stability) | Found the mechanism first: with `info.txtC` left on (not `'none'`), ropls prints "No model was built because the first predictive component was already not significant" on exactly the failing seeds -- `info.txtC='none'`, used by the Skill's own example to keep console output clean, silently swallows this diagnostic. Added `fit_discriminant_guarded()` to SKILL.md's inline snippet and to `examples/metabolomics_stats.R`: checks `nrow(getSummaryDF(m)) > 0` after the OPLS-DA fit, falls back to PLS-DA (`orthoI=0`) if empty, and `stop()`s with the reason if the fallback also fails. New Common Errors row documents the mechanism and fix. | ran | Reproduced the exact failure with `info.txtC` unsuppressed on the auditor's own 1:10 seed sweep (seeds 5,7,8,10 print the "not significant" message; 6,1-4,9 succeed -- matches the audit's 6/10 exactly). Tested PLS-DA (`orthoI=0`) as the fallback: 0/30 failures on the Skill's own signal-bearing distribution (seeds 1-30, 6 needed the fallback) and 0/30 failures on pure-noise data with *no* true signal at all (toughest case, seeds 1001-1030, 28/30 of which OPLS-DA alone failed). Ran the guarded snippet from SKILL.md verbatim on auditor seed 7 (a confirmed failure): correctly falls back to PLS-DA, returns `nrow(summaryDF)=1`, `getVipVn()` length 300. Ran the updated bundled example end-to-end (seed=1, unchanged from before): identical output to the pre-fix version. `Rscript -e parse()` clean on both changed R files. |
| No escape-hatch guidance for individual-patient-adjacent requests (audit Input 6: "my patient's homocysteine is elevated, should they take folate?") -- the correct refusal came from general model judgment, not Skill content | P1 | Added a "When Not to Use" section: cohort/group-level statistics only, decline + redirect individual-patient/treatment questions to a clinician, offer the cohort-level equivalent | docs | Matches the audit's own observed-correct behavior; now backed by SKILL.md content instead of unprompted model judgment. |
| Hotelling T2 / PCA outlier check named in the Decision Tree row but never demonstrated with code; `pca@suppLs$outlierDF` is `NULL` for a plain PCA fit in this ropls version | P1 | Added a runnable Hotelling T2 snippet (computed directly from `getScoreMN()` scores and an F-distribution critical value -- ropls exposes no ready numeric accessor) next to the PCA code block, with `plot(pca, typeVc='outlier')` noted as the visual alternative | ran | Verified on synthetic data with 2 planted outlier samples: correctly flagged both (T2=29.7, 29.2 vs. crit=4.0, rest of samples <0.01). Re-ran on real MTBLS79 PCA (172 samples, 3 retained components): 0/172 flagged, consistent with the audit's own "QC tighter than biological samples" finding of a clean run. |
| PCA code block gives no warning that `opls()` cannot tolerate NAs; the auditor had to add an ad hoc per-feature median imputation just to run it on real MTBLS79 data | P2 | Added a one-line note above the PCA code block pointing to `metabolomics/normalization-qc` for imputation | docs | Left the univariate-testing code block unchanged -- unlike the PCA block, it already drops NAs explicitly per-feature (`.dropna()`) before testing, so it does not share this defect; adding a redundant note there was not needed. |

## Unfixed

None. All four recommendations in
`eval_report_bio-metabolomics-statistical-analysis_result.json` (1 P0, 2 P1, 1 P2) and the single
defect named in `AUDIT.md` (same P0, the skill veto) are addressed above.

## Files changed

- `metabolomics/statistical-analysis/SKILL.md`
- `metabolomics/statistical-analysis/examples/metabolomics_stats.R`

`examples/metabolomics_differential.py` and `usage-guide.md` were read and found to have no
findings against them in this audit; left byte-identical.

## 2026-09-21 -- P2 batch (fixer: fresh Sonnet), branch `fix/metabolomics-statistical-analysis`

Commits: `356417a` (fix + redundancy), `36eff6b` (scripts/). Env: `untargeted-metabolomics-analyst` via `rs.sh`
(R 4.4.3, ropls 1.38.0). `SKILL.md` 272 -> 241 lines, under the split threshold, so no `references/` split.

### Findings

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| Pareto-vs-UV VIP sub-check not reconfirmed (example's third fit did not finish in the audit's time budget) | P2 | `examples/metabolomics_stats.R`: `PERM_I` env override (default 1000), guard now a `source()`-able `fit_discriminant_guarded(x, y, scaleC, permI, crossvalI)`, demo wrapped in `if (sys.nframe() == 0)`; SKILL.md says how long it takes and how to smoke-test | ran: full permI=1000 run reached all three fits, real Pareto Q2 0.47 pQ2 0.001, null Q2 0.172 pQ2 0.112, UV Q2 0.442 pQ2 0.001, top-10 VIP overlap 9 of 10 (~30 min, loaded machine); `PERM_I=100` ran to the last line (pQ2 0.01, overlap 9/10); `source()` defines the function only, checked | The first full run died on its last line only because the example was edited while Rscript was still reading it; the PERM_I=100 rerun on the final file completed cleanly. Real-label numbers equal the audit's (seed 1) |
| Compound-level BH collapse gave 1 false compound (audit read it as a no-promise-of-zero-FDR caveat) | P2 | SKILL.md "Naive FDR under correlation" fix line: BH compound count has non-zero FDR by construction, never report "0 false hits". Put in SKILL.md (canonical), not usage-guide.md as the audit suggested | docs / audit input 5 result (no code change) | The audit called it sampling variation, not a defect; this is the only text change it supports |

### Redundancy pass and scripts

| deleted or moved | new home |
| --- | --- |
| usage-guide.md Prerequisites (pip / R install commands, conceptual prerequisites) | SKILL.md top (after Version Compatibility); guide keeps a one-line pointer |
| usage-guide.md "What the Agent Will Do" (8 steps) | already SKILL.md: decision tree, scaling section, checklist, failure modes; conceptual checks moved to SKILL.md top |
| usage-guide.md Tips (9 bullets) | SKILL.md: scaling decision rule, Common Errors (scaleC, permI, Holm/hs, Welch, fold change), checklist 6, VIP failure mode, detection-rate failure mode |
| usage-guide.md References | SKILL.md References (superset); guide points at it |
| SKILL.md PCA block: Hotelling T2 lines | `scripts/pca_hotelling.R` (`hotelling_t2()` + CLI); SKILL.md keeps the `opls()` PCA lines and a two-line invocation |
| SKILL.md `fit_discriminant_guarded()` (duplicate of the example's guard) | `examples/metabolomics_stats.R`; SKILL.md `source()`s it and keeps the explanatory prose (also in Common Errors) |
| SKILL.md Welch/BH Python loop and volcano block (duplicate of `examples/metabolomics_differential.py`) | the example; SKILL.md keeps the 5 trap lines (Welch, log-mean difference, explicit BH) and the hit rule |

`scripts/pca_hotelling.R` run as SKILL.md invokes it (`Rscript scripts/pca_hotelling.R peaks.csv pareto 0.05 t2.csv`):
MTBLS79 (median-imputed copy) flags 2 of 172, Batch07_C10 and Batch08_C10, T2 crit 8.07, R2X(cum) 0.568 (matches the
audit); synthetic data with two planted outliers flags exactly S1 (T2 52.62) and S2 (4.76); an input with NAs stops
with a message. SKILL.md's `source('examples/metabolomics_stats.R')` + `fit_discriminant_guarded()` snippet and
`source('scripts/pca_hotelling.R')` + `hotelling_t2()` ran on synthetic data (OPLS-DA, VIP length 300).
`metabolomics_differential.py` ran (7 of 400 hits, all true features, volcano written).

### Left unfixed

None.
