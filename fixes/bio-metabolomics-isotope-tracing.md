# Fix log: bio-metabolomics-isotope-tracing (2026-09-17)

Worktree `F:\OpenScience\wt\mb-iso`, branch `fix/mb-iso`, base `main` @ `978ae4a`.
Commits: `5f30723` (fix), `bb99daf` (refactor).

## Findings

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| Steady-state check compares only the last timepoint pair, letting a still-decelerating series pass as plateau | P1 | `SKILL.md` steady-state snippet now checks the last 3 consecutive deltas all `<0.02`, not just the final pair; added a caution paragraph and updated the Quantitative Thresholds row | ran (`Scripts/python.exe`): audit's Input 3 series (fe 0.00/0.10/0.20/0.28/0.34/0.35, deltas 0.08/0.06/0.01) now returns `reached_plateau=False`; adjusted doc example (deltas 0.015/0.013/0.012) returns `True` | matches audit's suggested fix ("require the delta shrinking/below threshold across last 2-3 intervals") |
| Common Errors table's "half-defined resolution" text is more specific than the real error | P1 | Quoted the real generic isocor text verbatim in the Common Errors table row | ran: `MetaboliteCorrectorFactory('C6H12O6', tracer='13C', mz_of_resolution=400)` on isocor 2.2.4 raises exactly `ValueError: MetaboliteCorrectorFactory was unable to select a correction strategy. Please check your inputs.` | same env/version the audit used |
| AccuCor snippet doesn't document its default file-write side effect; auditor's first run wrote into the installed package's own `extdata/` | P1 | Added `output_base` to the SKILL.md R snippet plus a comment explaining the default-write behavior and to never point it at a package directory | ran (`rs.sh` in scratchpad, accucor 0.3.1.9000): confirmed `output_base` writes `<output_base>_corrected.xlsx`; did not re-run the unsafe no-`output_base` path (already demonstrated by the audit; re-running it risks the shared package folder again) | did not touch `R-lib/accucor/extdata/` |
| No inline recovery guidance in the code snippets | P2 (cheap) | Added a one-line try/except pointer comment to the isocor correction snippet | n/a (comment only) | accucor snippet's comment block already grew large with the P1 fix above; try/except guidance for it is covered by the existing Common Errors table reference in prose |

## Redundancy pass (commit `bb99daf`)

| deleted passage | old location | new home |
|---|---|---|
| "Never plot or model raw isotopologue areas..." | usage-guide.md Tips | SKILL.md "Natural-Abundance + Tracer-Purity Correction" (already states "never plot raw (uncorrected) areas") |
| "Fractional enrichment is concentration-independent..." | usage-guide.md Tips | SKILL.md "The Single Most Important Insight" |
| "A rising intermediate pool can mean LESS downstream flux..." | usage-guide.md Tips | SKILL.md "The Single Most Important Insight" + "Pool-size-vs-labeling confound" failure mode |
| "Quench fast and cold..." | usage-guide.md Tips | SKILL.md "Quench/extraction continuing turnover" failure mode |
| "Mass spectra resolve isotopologues..., not isotopomers..." | usage-guide.md Tips | SKILL.md Core Concepts table (Isotopologue / Isotopomer rows) |
| `## Related Skills` bullet list | SKILL.md (end) | kept only in usage-guide.md (the brief's named home); routing already lives in SKILL.md's Decision Tree table and frontmatter `description`, so no agent-needed content left the Skill |
| `pip install isocor numpy` / `install.packages('accucor')` | usage-guide.md Prerequisites | SKILL.md "Version Compatibility" (the brief names install notes as SKILL.md's home); usage-guide.md now points to that section by name |

## Unfixed

None. All P1s and the one cheap P2 were fixed; the second P2 (recovery guidance in the accucor snippet) is effectively covered — see table.

## Needs Sam

Nothing.
