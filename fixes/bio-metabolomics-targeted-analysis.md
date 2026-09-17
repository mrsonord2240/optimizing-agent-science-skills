# bio-metabolomics-targeted-analysis fixes (2026-09-17)

Worktree `F:\OpenScience\wt\mb-targ`, branch `fix/mb-targ` (from fork main `d9971f6`). Runtime:
R 4.4.3 via `F:\OpenScience\audit-envs\untargeted-metabolomics-analyst\rs.sh` (base R + ggplot2,
no extra packages needed). Audit score 90, Production Ready.

## Findings

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| SKILL.md requires both intra-day and inter-day precision acceptance but gives no formula for inter-day; a naive pooled SD across days can pass a level that is actually failing | P1 | New `### Precision: Intra-Day and Inter-Day (Nested ANOVA, Not Pooled SD)` subsection under "Calibration and Weighting": intra-day CV per day, plus a one-way-ANOVA variance-components formula for inter-day (MSwithin + max(0,(MSbetween-MSwithin)/n)), with a runnable R block on synthetic LLOQ data (2 days x 3 reps, planted rep-3 outlier both days) | ran (`rs.sh`): intra-day 21.7%/20.6% (FAIL 20% LLOQ tol), naive pooled SD 18.9% (WRONG, PASSes), nested-ANOVA inter-day 21.1% (correctly FAILs) — reproduces the audit's own Input-5 numbers from first principles and shows the correct formula catches what pooled SD misses | Quantitative Thresholds table's precision row now points to this subsection |
| No output-format template for the final deliverable | P2 | New `## Report Format` section: one-row-per-sample-x-analyte table (sample/analyte/unit/conc/lloq/reportable/id_confirmed/notes), rule to state a reason (`below_LLOQ`, `ion_ratio_fail`, `carryover_flagged`) instead of a blank/zero | n/a (documentation addition, mirrors existing section style) | |
| Trigger description is jargon-dense (MRM/SRM/%RE vocabulary) | P2 | Left unchanged | n/a | Not wrong — it accurately scopes the skill and explicitly disambiguates against 3 sibling skills (xcms-preprocessing, statistical-analysis, isotope-tracing). Dispatch and FIX_BRIEF both say change `description` only if it's actually wrong; jargon density is a discoverability nit, not a defect, so left as-is per brief. |

## Redundancy pass (usage-guide.md -> SKILL.md)

Deleted usage-guide.md's `Tips` (6 bullets) and `What the Agent Will Do` (6 steps) sections —
every point in both restated SKILL.md content verbatim or near-verbatim. Replaced with one
pointer sentence to SKILL.md. Deleted-passage -> new-home, verified by grep:

| deleted passage (usage-guide.md) | already lives at (SKILL.md) |
|---|---|
| "Judge a calibration by back-calculated %RE ... never by R-squared alone" | "Calibration and Weighting" — R-squared paragraph (line 71) |
| "One SIL-IS per analyte is the gold standard ..." | "Decision Tree" — IS rule of thumb paragraph (line 60) |
| "Prefer 13C/15N internal standards over deuterium ..." | same paragraph (line 60) |
| "Low CV is not evidence of a correct number ..." | "Per-Method Failure Modes" > One IS shared across chemically diverse analytes > Fix (line 190) |
| "Pre-analytics is upstream of every assay safeguard ..." | "Per-Method Failure Modes" > Pre-analytical degradation (line 204) |
| "A single transition has no defense against isobaric interference ..." | "Ion-Ratio Confirmation" closing paragraph (line 122) |
| "What the Agent Will Do" steps 1-5 (panel/IS strategy, calibration, LLOQ, IS normalization, ion-ratio) | paraphrase each subsection's own "Goal:" line (Decision Tree, Calibration, LOD/LLOQ, IS Normalization, Ion-Ratio) |
| "What the Agent Will Do" step 6 (validation metrics + "export concentrations with quality flags") | new `## Report Format` section (this pass) + existing Quantitative Thresholds table (matrix factor/carryover/recovery already listed) |

usage-guide.md kept: Overview, Prerequisites (install commands — unique, not in SKILL.md), Quick
Start, Example Prompts, Related Skills. SKILL.md 211 -> 269 lines; usage-guide.md 74 -> 60 lines.

## Unfixed

None. All P1 and both P2s addressed.
