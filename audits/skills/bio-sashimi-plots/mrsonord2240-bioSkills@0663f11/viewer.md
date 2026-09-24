> **Audit record for `bio-sashimi-plots`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@0663f11](https://github.com/mrsonord2240/bioSkills/tree/0663f11fbc8026f2134cdcc27c57ad80996c8447/alternative-splicing/sashimi-plots) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-sashimi-plots

## Canonical final summary

**Final:** 92/100 — ⭐ Production Ready; deployable: true.

Generated: 2026-09-23 · rendered from `report.json` by `tools/render_viewer.py`.

> This viewer is **generated from the audit report**, not written by the auditor. It restates the report's own recorded scores, notes and assertions and adds nothing to them. Where a hand-written viewer would argue from the runs, this one points at the scripts in [scripts/](scripts/) instead.

Source: `mrsonord2240/bioSkills@0663f11fbc8026f2134cdcc27c57ad80996c8447:alternative-splicing/sashimi-plots`
Final-pass metadata: `auditor_independent: false` — final pass: fixed and audited under one brief, see CHECKPOINT.md.
Category: Data Analysis · Execution mode: D · Complexity: Complex · N = 9 · Executed: None

## What the Skill claims to do

Creates RNA-seq sashimi plots with ggsashimi, rmats2sashimiplot, leafviz, Jutils, and pyGenomeTracks, selecting the route by upstream splicing result and publication or interactive goal.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 57 | **95** | 3/3 | yes | PASS |
| 2 | Adversarial | 37 | 55 | **92** | 2/2 | yes | PASS |
| 3 | Variant | 38 | 57 | **95** | 2/2 | yes | PASS |
| 4 | Regression | 38 | 57 | **95** | 2/2 | yes | PASS |
| 5 | Workflow | 37 | 56 | **93** | 2/2 | yes | PASS |
| 6 | Workflow | 38 | 56 | **94** | 3/3 | yes | PASS |
| 7 | Scope Boundary | 37 | 56 | **93** | 2/2 | yes | PASS |
| 8 | Variant | 38 | 56 | **94** | 4/4 | yes | PASS |
| 9 | Scope Boundary | 36 | 55 | **91** | 1/1 | yes | PASS |

**Execution Average: 94.0 / 100** · **Assertion Pass Rate: 21/21**

**Static: 90/100** · Static weighted 36.0 + dynamic weighted 56.4 = **92/100** → ⭐ Production Ready, deployable.

---

## Veto gates

### Skill veto — **PASS**

| Check | Result | Detail |
|---|---|---|
| stability | PASS |  |
| contract | PASS |  |
| determinism | PASS |  |
| security | PASS |  |

### Research veto — **PASS**

| Check | Result | Detail |
|---|---|---|
| scientific integrity | PASS | All reported output facts are from this run's logs or generated files. MAJIQ/VOILA is described as licence-gated rather than asserted to work. |
| practice boundaries | PASS | The Skill visualizes RNA-seq splicing evidence and does not provide diagnostic, therapeutic, or prescriptive conclusions. |
| methodological ground | PASS | The run exercised grouped BAM overlays, rMATS event plotting, leafcutter visualization preparation, result conversion, and coverage/junction tracks using real local fixture inputs. |
| code usability | PASS | Every shipped executable path was freshly exercised from a copied source tree: example functions, rmats2sashimiplot, leafviz build mode, Jutils pipeline and its four converters, and pyGenomeTracks preparation/rendering. The MAJIQ/VOILA reference is a documented licence boundary, not runnable evidence. |

## Static score

| Category | Score | Note |
|---|---|---|
| functional suitability | 11/12 | Clear tool selection across major upstream splicing formats and rendering goals; the MAJIQ/VOILA path is necessarily unverified without a licence. |
| reliability | 12/12 | The example rejects missing BAMs, unknown contigs and empty regions; shell helpers use strict mode and check non-empty outputs where silent success is known. |
| performance context | 6/8 | The comprehensive single Skill is useful but long; tool-specific references provide only partial progressive disclosure. |
| agent usability | 15/16 | Inputs, flags, version notes, expected files and failure modes are concrete; several recipes rely on installed tools or prior block state. |
| human usability | 8/8 | Decision guidance and command-oriented recipes make the intended route understandable to a working analyst. |
| security | 11/12 | No credentials or remote write actions; list-form Python subprocesses and sanitized plot names help. Shell recipes still accept user paths. |
| maintainability | 9/12 | Versions and compatibility constraints are named, but reproducible fixtures and automated tests are not shipped with the Skill. |
| agent specific | 18/20 | Strong failure semantics, explicit licence boundary, version pin and postcondition language; the multi-tool scope remains cognitively dense. |

## Input 1 — Canonical: ggsashimi grouped 3v3 planted BAM overlay

- Status: PASS COMPLETED · Basic 38/40 · Specialized 57/60 · **Total 95/100**
- Execution: PID-owned runner 1437510 -> 1437557; logs/input01.log; copied examples/plot_sashimi.py invoked under as-viz-gg34.
- Finding: Generated non-empty PDF with a source-created grouping file, palette and observed junction counts.

| Assertion | Result | Evidence |
|---|---|---|
| Grouped overlay writes a non-empty PDF | PASS | happy.pdf exists and is over 1 KB. |
| Grouping and palette are generated by copied source functions | PASS | groups.tsv and palette.txt written. |
| Independent source junction scan finds a junction | PASS | junction_counts returned data before rendering. |

## Input 2 — Adversarial: ggsashimi missing-BAM and unknown-contig guards

- Status: PASS COMPLETED · Basic 37/40 · Specialized 55/60 · **Total 92/100**
- Execution: PID-owned runner 1437745 -> 1437791; logs/input02.log; copied example called with invalid user input.
- Finding: Both invalid cases were rejected before a misleading plot could be emitted.

| Assertion | Result | Evidence |
|---|---|---|
| Missing BAM raises FileNotFoundError | PASS | ASSERT missing_bam_guard. |
| Unknown contig raises ValueError | PASS | ASSERT contig_guard. |

## Input 3 — Variant: Batch plot of significant planted rMATS SE event

- Status: PASS COMPLETED · Basic 38/40 · Specialized 57/60 · **Total 95/100**
- Execution: PID-owned runner 1440971 -> 1441022; logs/input08.log; copied batch_plot_rmats_events used a planted rMATS table.
- Finding: The significant event produced exactly one non-empty PDF.

| Assertion | Result | Evidence |
|---|---|---|
| Batch selection finds the significant event | PASS | Log reports top 1 event. |
| Batch output is non-empty | PASS | ASSERT batch_rmats_one_pdf. |

## Input 4 — Regression: rmats2sashimiplot helper on matching planted SE data

- Status: PASS COMPLETED · Basic 38/40 · Specialized 57/60 · **Total 95/100**
- Execution: PID-owned runner 1438617 -> 1438663; logs/input03_happy.log; copied rmats2sashimiplot_events.sh.
- Finding: The helper generated one figure and its postcondition counted it. A separate mismatched chrX/chrP fixture caused the helper's zero-figure check to fail as designed (logs/input03_mismatched_contig_expected_failure.log).

| Assertion | Result | Evidence |
|---|---|---|
| Matching SE input produces a PDF | PASS | OK: 1 figures. |
| Postcondition counts rendered PDFs | PASS | ASSERT rmats_pdf_count=1. |

## Input 5 — Workflow: leafviz annotation and RData build without launching a server

- Status: PASS COMPLETED · Basic 37/40 · Specialized 56/60 · **Total 93/100**
- Execution: PID-owned runner 1438809 -> 1438862; logs/input04.log; copied leafviz_run.sh with LAUNCH=0 under as-rleaf.
- Finding: Prepared an annotation and non-empty LeafViz RData from leafcutter output in the audit directory.

| Assertion | Result | Evidence |
|---|---|---|
| RData is written | PASS | leafviz.RData non-empty. |
| Annotation generation succeeds | PASS | annot_all_exons.txt.gz non-empty. |

## Input 6 — Workflow: Jutils rMATS conversion, heatmap, sashimi and Venn pipeline

- Status: PASS COMPLETED · Basic 38/40 · Specialized 56/60 · **Total 94/100**
- Execution: PID-owned runner 1438998 -> 1439050; logs/input05.log; copied jutils_pipeline.sh under as-viz-gg34.
- Finding: Converted rMATS results and wrote the expected sashimi PDF and Venn PNG.

| Assertion | Result | Evidence |
|---|---|---|
| Conversion TSV exists | PASS | rmats_JC_results.tsv non-empty. |
| Sashimi PDF exists | PASS | out/sh/sashimi.pdf non-empty. |
| Venn PNG exists | PASS | out/vn/venn_diagram.png non-empty. |

## Input 7 — Scope Boundary: pyGenomeTracks coverage, junction BEDPE and figure

- Status: PASS COMPLETED · Basic 37/40 · Specialized 56/60 · **Total 93/100**
- Execution: PID-owned runner 1439747 -> 1439798; logs/input06_happy.log; copied pgt_tracks.sh under as-core then pyGenomeTracks under as-viz-gg34.
- Finding: Produced 3 junctions, coverage tracks and a non-empty rendered figure. The first fixture omitted annotation.gtf and failed before rendering; its log is retained separately rather than counted as success.

| Assertion | Result | Evidence |
|---|---|---|
| Junction BEDPE is non-empty | PASS | OK: 3 junctions. |
| Track rendering writes a figure | PASS | ASSERT pgt_bedpe_and_render. |

## Input 8 — Variant: Jutils leafcutter, MntJULiP, MAJIQ and rMATS converters

- Status: PASS COMPLETED · Basic 38/40 · Specialized 56/60 · **Total 94/100**
- Execution: PID-owned runner 1440737 -> 1440788; logs/input07_happy.log; Jutils shipped test data used under as-viz-gg34.
- Finding: All four documented converter families wrote non-empty result TSVs.

| Assertion | Result | Evidence |
|---|---|---|
| leafcutter conversion exists | PASS | leafcutter_results.tsv. |
| MAJIQ conversion exists | PASS | majiq_results.tsv. |
| MntJULiP conversion exists | PASS | mntjulip_DSR_results_raw.tsv. |
| rMATS conversion exists | PASS | rmats_JunctionCountOnly_results.tsv. |

## Input 9 — Scope Boundary: MAJIQ/VOILA licence boundary

- Status: PASS COMPLETED · Basic 36/40 · Specialized 55/60 · **Total 91/100**
- Execution: No licence-gated MAJIQ/VOILA binary was launched. The run explicitly records this as an unsupported unauthenticated route; no external download or environment mutation was attempted.
- Finding: The documented boundary is accurate: the Skill does not present a licence-gated runtime as verified.

| Assertion | Result | Evidence |
|---|---|---|
| Unlicensed route is not represented as executed | PASS | No MAJIQ/VOILA process was started. |

## Key strengths

- Fresh PID-owned tests covered every non-licence-gated executable route from a copied source tree.
- Input guards prevent ggsashimi from silently accepting missing BAMs or unknown contigs.
- rMATS, leafcutter, Jutils and pyGenomeTracks all produced asserted output artifacts.

## Recommendations

### P2 — Provide reproducible fixtures

- Observed in inputs: —
- Problem: The Skill itself has no small test fixture bundle.
- Root cause:
- Fix: Add optional tiny fixtures and a smoke-test recipe so compatibility can be checked without audit infrastructure.

### P2 — Clarify recipe state

- Observed in inputs: —
- Problem: Some later examples presume files created by earlier blocks or a tool on PATH.
- Root cause:
- Fix: State dependencies adjacent to every runnable block.
