> **Audit record for `bio-data-visualization-lollipop-protein-maps`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@4f5e4c0](https://github.com/mrsonord2240/bioSkills/tree/4f5e4c0e54f612acdab50562e7a5cb07abb0b6bc/data-visualization/lollipop-protein-maps) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-data-visualization-lollipop-protein-maps

Generated: 2026-09-24 · rendered from `report.json` by `tools/render_viewer.py`.

> This viewer is **generated from the audit report**, not written by the auditor. It restates the report's own recorded scores, notes and assertions and adds nothing to them. Where a hand-written viewer would argue from the runs, this one points at the scripts in [scripts/](scripts/) instead.

Source: `mrsonord2240/bioSkills@4f5e4c0e54f612acdab50562e7a5cb07abb0b6bc:data-visualization/lollipop-protein-maps`
Audit type: focused final-pass re-audit at the exact follow-up commit
Category: Data Analysis · Execution mode: A · Complexity: Moderate · N = 7 · Executed: None

## What the Skill claims to do

Plot per-gene mutation distributions on protein-domain maps with maftools, trackViewer, and g3viz.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 57 | **95** | 5/5 | yes | ✅ |
| 2 | Variant A | 38 | 56 | **94** | 5/5 | yes | ✅ |
| 3 | Edge | 38 | 56 | **94** | 5/5 | yes | ✅ |
| 4 | Variant B | 37 | 56 | **93** | 5/5 | yes | ✅ |
| 5 | Stress | 38 | 57 | **95** | 5/5 | yes | ✅ |
| 6 | Variant A | 38 | 56 | **94** | 5/5 | yes | ✅ |
| 7 | Edge | 37 | 56 | **93** | 5/5 | yes | ✅ |

**Execution Average: 94.0 / 100** · **Assertion Pass Rate: 35/35**

**Static: 92/100** · Static weighted 36.8 + dynamic weighted 56.4 = **93/100** → ⭐ Production Ready, deployable.

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
| scientific integrity | PASS | No fabricated measurements or clinical claims. |
| practice boundaries | PASS | Research visualization only; no diagnosis or prescription. |
| methodological ground | PASS | Rows, samples, per-change recurrence, and formal hotspot inference are distinguished. |
| code usability | PASS | Exact example and two new input routes produced checked outputs. |

## Static score

| Category | Score | Note |
|---|---|---|
| functional suitability | 12/12 | Three clear routes cover standard, custom, and interactive maps. |
| reliability | 10/12 | Column selection, warnings, palette fallback, and isoform checks are explicit; maftools emits its own stop-extension coercion warning. |
| performance context | 7/8 | Focused route table and code avoid redundant steps. |
| agent usability | 15/16 | Inputs, routes, checks, outputs, and feature-source distinctions are clear. |
| human usability | 8/8 | Compact guide gives natural prompts. |
| security | 11/12 | No credentials, remote writes, or destructive operations. |
| maintainability | 11/12 | The runnable example labels 102--292 as a conventional supplied range and requires a chosen literature citation for publication use. |
| agent specific | 18/20 | Narrow trigger and concise escape hatches. |

## Input 1 — Canonical: Exact shipped TP53 maftools demonstration

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 57/60 · **Total 95/100**
- Execution: Disposable exact source copy.

| Assertion | Result | Evidence |
|---|---|---|
| Exact example completes maftools route. | PASS | Exited through r.sh. |
| Supported column is selected. | PASS | HGVSp_Short selected. |
| TP53 RefSeq is shown. | PASS | PDF contains NM_000546. |
| PDF parses. | PASS | 5121 bytes; pdftotext passed. |
| Row-count semantics are stated. | PASS | Skill and y-axis say mutation-row count. |

## Input 2 — Variant A: Exact shipped paired lollipopPlot2

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 56/60 · **Total 94/100**
- Execution: Deterministic Luminal and Basal route.

| Assertion | Result | Evidence |
|---|---|---|
| lollipopPlot2 completes. | PASS | Both subset and plot calls completed. |
| Cohort labels appear. | PASS | Luminal and Basal in PDF. |
| Paired PDF parses. | PASS | 5384 bytes; pdftotext passed. |
| RefSeq appears. | PASS | PDF contains NM_000546. |
| Column is not hard-coded. | PASS | AACol arguments receive change_col. |

## Input 3 — Edge: HGVSp edge cases and short-isoform guidance

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 56/60 · **Total 94/100**
- Execution: Exact demo plus independent parser input.

| Assertion | Result | Evidence |
|---|---|---|
| Uncertain start loss warns and drops. | PASS | Exact run dropped p.M1?. |
| One-letter, three-letter, and stop extension parse. | PASS | 175, 175, and 394. |
| Silent and empty strings return NA. | PASS | Independent parser assertion. |
| Short-isoform clipping is warned. | PASS | Skill requires max-position comparison. |
| NA positions do not reach GRanges. | PASS | Example filters first. |

## Input 4 — Variant B: Exact trackViewer TP53 map and references

- Status: ✅ COMPLETED · Basic 37/40 · Specialized 56/60 · **Total 93/100**
- Execution: Exact PDF plus live UniProt and Ensembl checks, followed by exact-commit source-attribution verification.

| Assertion | Result | Evidence |
|---|---|---|
| Residue and domain labels appear. | PASS | PDF contains all intended labels. |
| Palette lookup is factor-safe. | PASS | No NA colors; missense #D55E00. |
| TP53-201 identifier is correct. | PASS | Ensembl returned ENST00000269305. |
| Three direct UniProt ranges match. | PASS | 1-44, 325-356, and 368-387. |
| The 102--292 boundary is not misattributed to current UniProt JSON. | PASS | The exact commit labels it as a supplied conventional DNA-binding-core range and requires a chosen literature citation for publication use. |

## Input 5 — Stress: Exact shipped g3viz supplement

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 57/60 · **Total 95/100**
- Execution: Exact readMAF to g3Lollipop to saveWidget route.

| Assertion | Result | Evidence |
|---|---|---|
| Route uses readMAF. | PASS | No nonexistent helper. |
| saveWidget writes HTML. | PASS | 312321 bytes. |
| HTML has widget content. | PASS | g3viz or g3Lollipop text found. |
| Archive caveat is documented. | PASS | g3viz 1.2.0 stated archived. |
| HTML path is explicit. | PASS | saveWidget used. |

## Input 6 — Variant A: New Protein_Change-only MAF

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 56/60 · **Total 94/100**
- Execution: Fresh seven-row synthetic MAF.

| Assertion | Result | Evidence |
|---|---|---|
| Protein_Change is selected. | PASS | Only supported available column. |
| maftools accepts it. | PASS | Returned data.table. |
| New maftools PDF parses. | PASS | Over 1 KB. |
| p.M1? is excluded. | PASS | NA before plot. |
| Unknown class gets fallback color. | PASS | No NA colors. |

## Input 7 — Edge: New duplicate recurrence and label test

- Status: ✅ COMPLETED · Basic 37/40 · Specialized 56/60 · **Total 93/100**
- Execution: Independent recurrence summary and custom track.

| Assertion | Result | Evidence |
|---|---|---|
| Rows and samples differ. | PASS | Three rows versus one duplicate-R175H sample. |
| Deduplication key is stated. | PASS | Sample barcode plus HGVSp. |
| Residue labels remain names. | PASS | R175H label retained. |
| New trackViewer PDF parses. | PASS | Over 1 KB. |
| Unsupported tools were removed. | PASS | No pyLollipop or Bio.PDB claim. |

## Key strengths

- Exact example writes three parseable PDFs and nonempty HTML without Rplots.pdf.
- The Skill distinguishes row counts, unique-sample recurrence, and residue aggregation.
- Column, parser, palette, RefSeq, transcript, and g3viz corrections held on regression and new inputs.
- The concise guide removes stale tool claims.
