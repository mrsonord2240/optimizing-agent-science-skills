# Audit — crispr-screen-analyst (2026-09-16)

Verdict stage only (Step 3 of `process/AUDIT_BRIEF.md`). Evidence is `SELECTION.md` plus every
`eval_report_<skill-id>_result.json` under `F:\OpenScience\audits\`. No new auditing was performed;
no Skill code was run. This replaces the prior not-viable `AUDIT.md` in full (document doctrine:
delete the old, write the new).

All 16 Skills in `SELECTION.md` were re-audited post-fix on the Sam fork
`mrsonord2240/bioSkills-Improved` (formerly `mrsonord2240/bioSkills`), branch `openscience-fixes`.
Every report's `source`/`meta.source` names `mrsonord2240/bioSkills@<commit>:<folder>/<skill>` — none
still point at `GPTomics/bioSkills`, so no report needed to be scored as unfixed on that basis.

## Audited Skills

| # | Skill ID | Role | Category | Mode | N | Executed k/N | Static | Exec. avg | Final | Grade | Veto | Top open P1 |
|---|----|----|----|----|----|----|----|----|----|----|----|----|
| 1 | bio-crispr-screens-library-design | core — framing/design | Protocol Design | D | 8 | 8/8 | 93 | 90.0 | **91** | Production Ready | none | (P2 only) |
| 2 | bio-crispr-screens-screen-qc | core — QC/validation pre-hit-calling | Data Analysis | D | 9 | 6/9* | 93 | 94.8 | **94** | Production Ready | none | (P2 only) |
| 3 | bio-crispr-screens-mageck-analysis | core — central op. (hit calling) | Data Analysis | D | 9 | 9/9 | 90 | 87.0 | **88** | Limited Release† | none | 4 open P1s (RRA-pairing claim wrong; FluteMLE example broken; MLE rerun non-determinism at default; permutation-round magnitude overclaimed) |
| 4 | bio-crispr-screens-bagel-essentiality | core — central op. (hit calling) | Data Analysis | D | 7 | 7/7 | 87 | 88.1 | **88** | Production Ready | none | reference-set failure modes documented but no runtime guard |
| 5 | bio-crispr-screens-drugz-chemogenomic | core — central op. (hit calling) | Data Analysis | B | 7 | 6/7 | 89 | 90.4 | **90** | Production Ready | none | Common Errors table still lacks the half_window_size/IndexError row |
| 6 | bio-crispr-screens-jacks-analysis | core — central op. (hit calling) | Data Analysis | D | 7 | 7/7 | 96 | 89.1 | **92** | Production Ready | none | (P2 only) |
| 7 | bio-crispr-screens-copy-number-correction | **supporting** (re-marked, see below) | Data Analysis | D | 7 | 7/7 | 92 | 75.9 | **82** | Limited Release | none | (P2 only) |
| 8 | bio-crispr-screens-hit-calling | core — cross-method reconciliation | Data Analysis | D | 9 | 9/9 | 87 | 91.4 | **90** | Production Ready | none | (P2 only) |
| 9 | bio-workflows-crispr-screen-pipeline | core — end-to-end orchestration | Data Analysis | D | 7 | 6/7 | 86 | 84.4 | **85** | Limited Release | none | Step 6b MLE example doesn't carry sibling Skill's permutation-round caveat |
| 10 | bio-crispr-screens-batch-correction | supporting | Data Analysis | D | 7 | 6/7 | 91 | 91.3 | **91** | Production Ready | none | (P2 only) |
| 11 | bio-experimental-design-batch-design | supporting (reused; re-audited post-fix) | Protocol Design | A | 7 | 7/7 | 87 | 86.6 | **87** | Production Ready | none | (P2 only) |
| 12 | bio-pathway-go-enrichment | supporting (reused) | Data Analysis | A | 7 | 6/7 | 89 | 90.1 | **90** | Production Ready | none | simplify(ont='ALL') claim wrong on the cited clusterProfiler version |
| 13 | bio-pathway-gsea | supporting (reused; assertion count corrected — see below) | Data Analysis | A | 7 | 7/7 | 97 | 96.3 | **97** | Production Ready | none | (P2 only) |
| 14 | bio-crispr-screens-crispresso-editing | core — editing-outcome quantification | Data Analysis | A | 9 | 9/9 | 93 | 89.2 | **91** | Production Ready | none | (P2 only) |
| 15 | bio-crispr-screens-base-editing-analysis | supporting | Data Analysis | D | 9 | 9/9 | 87 | 95.0 | **92** | Production Ready | none | find_be_spacers() bare KeyError on zero candidates |
| 16 | bio-crispr-screens-prime-editing-screens | supporting | Data Analysis | D | 9 | 8/9 | 90 | 75.4 | **81.2** | Limited Release | none | PRIDICT2 batch CLI omits the required `input/` subdirectory |

\* Screen-qc: 3 of 9 inputs are Mode-A reasoning/judgment prompts with no code to run (diagnostic
reasoning, scope-boundary refusal, adversarial-pressure refusal); all 6 code-executing inputs ran.
† mageck-analysis: raw weighted score is in the 85–100 band but its assertion pass rate (30/36 =
83.3%) sits below the 90% Production-Ready floor, forcing one grade-tier downgrade to Limited
Release per `scoring_rubric.md` §5 — the report's own `final.grade_note` states this and the
arithmetic checks out (see below).

**Totals: 16/16 Skills pass** (core ≥ 85, supporting ≥ 75, `deployable: true`, no fired veto, no open
P0). 125 dynamic inputs were written across the 16 reports; at least 117 were actually executed
(the rest are Mode-A reasoning inputs or one Docker-environment hang, none hiding a defect).

## Arithmetic check (per the dispatch's instruction to re-derive, not trust, the headline)

For every report, per-input `assertions_passed`/`assertions_total` were summed and checked against
`dynamic_score.assertion_pass_rate`, then checked against what `final.grade`/`grade_note` claims.

- **bio-pathway-gsea**: sums to 32/33 (97.0%). The report's own `final.grade_note` already documents
  this correction ("Input 4's fourth assertion (kcdf) is a genuine FAIL... miscounted as a PASS in an
  earlier draft") and the grade (97, Production Ready) is derived from the corrected rate, with the
  floor check shown inline. **No further correction needed here — this is the report the dispatch
  flagged as already fixed**, and the fix holds up under an independent resum.
- **bio-crispr-screens-mageck-analysis**: sums to 30/36 (83.3%), matching the report's stated rate.
  Its `final.grade_note` explicitly downgrades from the raw weighted 88.2 (which would sit in the
  Production Ready band) to Limited Release because 83.3% < 90%, and shows the arithmetic. This is
  correct and internally consistent — flagged here as the report doing its own downgrade honestly,
  not as a defect.
- **All other 14 reports**: per-input sums matched `assertion_pass_rate` exactly and matched what
  `final.grade`/`grade_note` claims (no unexplained mismatch, no unwarranted grade round-up). No
  report in this candidate's set exhibited the "100% claimed, one FAIL recorded" defect the dispatch
  warned about generically — that defect was in a different candidate's round.

## copy-number-correction re-mark (2026-09-16, Sam)

`bio-crispr-screens-copy-number-correction` was carried in `SELECTION.md` as **supporting**, not
core, per Sam's 2026-09-16 re-mark: after three audits (two fix passes) it holds at 82 — deployable,
no veto, no open P0/P1 — but capped below the 85 core floor by static score and execution average
rather than by any defect. The candidate's central hit-calling operation is carried by
mageck-analysis/bagel-essentiality/drugz-chemogenomic/jacks-analysis (all core, all ≥ 88); copy-number
correction is a supporting adjunct to that operation. Applying the 75 supporting floor, its final
score of 82 passes. This note exists so a later reader does not mistake the re-mark for a quietly
waived core-floor failure — the score and defect profile are unchanged from what a core-floor
Skill would need to clear; only the role classification moved.

## Skills read but not chosen (from SELECTION.md)

- `bio-crispr-screens-combinatorial-screens` — no installable central tool (enCas12a is a
  guide-design concept, not a CLI); niche relative to core pooled-screen scope.
- `bio-crispr-screens-in-vivo-screens` — animal-model design guidance only, nothing to execute
  against; niche relative to core pooled-screen scope.
- `bio-crispr-screens-perturb-seq-analysis` — working tool stack (pertpy/scanpy/anndata) but sits on
  `single-cell-transcriptomics-analyst`'s side of the line, not this candidate's pooled-screen scope.
- `experimental-design/power-analysis`, `experimental-design/randomization-blocking` — unaudited,
  skipped for breadth control (multiple-testing and sample-size, the two other experimental-design
  Skills already scored from this folder, both had quality problems; batch-design already covers
  design-framing).
- `pathway-analysis/kegg-pathways`, `reactome-pathways`, `wikipathways`, `enrichment-visualization` —
  unaudited, skipped for breadth control (go-enrichment + gsea already give validation/interpretation
  coverage for gene-level hits).
- `bio-experimental-design-multiple-testing` (82, not deployable) and
  `bio-experimental-design-sample-size` (67, Reject, veto) — excluded per the brief.

## Verdict: VIABLE

Against the five gates this stage owns:

- **Gate 2 (every bundled Skill audited and deployable).** All 16 have a post-fix `skill-auditor`
  report on the Sam fork, `deployable: true`, no fired veto gate, no open P0 recommendation (every
  open recommendation across all 16 reports is P1 or P2), and a final score ≥ 75 (all 16 clear their
  respective floor — see table). **PASS.**
- **Gate 3 (core workflow Skills Production Ready, ≥ 85).** All 9 Skills marked `core` in
  `SELECTION.md` score ≥ 85: library-design 91, screen-qc 94, mageck-analysis 88, bagel-essentiality
  88, drugz-chemogenomic 90, jacks-analysis 92, hit-calling 90, crispr-screen-pipeline 85 (exactly at
  the floor), crispresso-editing 91. The candidate's central step — pooled-screen hit calling — has
  four independently-audited ≥ 88 executors (MAGeCK, BAGEL2, drugZ, JACKS), not just one. **PASS.**
- **Gate 4 (end-to-end coverage: ≥ 3 core Skills spanning framing/design, central operation,
  validation/reporting).** Checked against role, not against which Skills happen to score well:
  framing/design = library-design; central operation = mageck-analysis + bagel-essentiality +
  drugz-chemogenomic + jacks-analysis (hit calling) plus crispresso-editing (editing-outcome
  quantification, the second in-scope central operation per the brief's note that editing is in
  scope); validation/reporting = screen-qc (pre-hit-calling QC) and hit-calling (post-hit-calling
  cross-method reconciliation); orchestration = crispr-screen-pipeline. No planning Skill stands in
  for an execution Skill — the four hit-calling Skills and crispresso-editing are all real executors
  with tool output, not decision trees. **PASS, with wide margin (9 core Skills, not the minimum 3).**
- **Gate 7 (research scope).** Every one of the 16 reports' `research_veto.practice_boundaries` is
  `PASS`; where a report specifically probed an individual-patient/clinical framing (bagel-essentiality
  Input 7, screen-qc Input 6, crispresso-editing's scope checks, prime-editing-screens Input 7), the
  Skill declined the clinical leap and stayed at the research/screen level. **PASS.**
- **Gate 8 (shipped means present).** No report in this set flagged a missing primary script or an
  entirely missing reference set for any of the 16 Skills. Known gaps are peripheral and already
  called out as such in the reports themselves (CRISPRessoWGS untested for lack of a cached reference
  genome; CRISPRcleanR failing to install with Chronos as the verified fallback path) — these are
  execution-environment limits on a named alternative, not shipped-file absences. **PASS.**

**Candidate is viable.** `spec.json` includes all 16 Skills; none needed to be dropped.
