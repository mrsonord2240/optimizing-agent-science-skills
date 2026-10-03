> **Audit record for `bio-data-visualization-ggplot2-fundamentals`**
> - Audited working candidate `be703ae7f69598daa981d477afa71a873d0616a2f2830936b575c014a1f3f120`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/data-visualization/ggplot2-fundamentals), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-data-visualization-ggplot2-fundamentals

Generated: 2026-10-03  
Audit type: final independent re-audit (second loop) of the fixed candidate  
Exact candidate content SHA-256: `be703ae7f69598daa981d477afa71a873d0616a2f2830936b575c014a1f3f120`

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 38 | 56 | 94 | 5/5 | ✅ COMPLETED |
| 2 | Variant A | 37 | 55 | 92 | 4/4 | ✅ COMPLETED |
| 3 | Edge | 34 | 49 | 83 | 3/4 | ❌ PARTIAL |
| 4 | Variant B | 37 | 55 | 92 | 5/5 | ✅ COMPLETED |
| 5 | Stress | 37 | 55 | 92 | 4/4 | ✅ COMPLETED |

**Execution average:** 90.6 / 100  
**Assertion pass rate:** 21 / 22  
**Static score:** 87 / 100  
**Final score:** 89 / 100 — ⭐ Production Ready  
**Research veto:** PASS

Readiness decision: **candidate-ready** for this exact identity (final 89, static 87, execution average 90.6, assertions 21/22 = 95.5 %, no veto, no open P0 or P1; three P2 recommendations open: GG-010, GG-011, GG-012). Exact identity is in [`source-identity.json`](source-identity.json).

## Prior findings (initial audit 34a174ab0263; failed re-audit 9d22bac5b1ee)

| Prior finding | Verdict | Evidence |
|---|---|---|
| GG-004 (P1) long-ID volcano labels collide where the Skill promises clean | corrected (closed); residual P2 wording gap GG-011 | `create_volcano` default now 10 symbols / 3 IDs. All 16 claimed zero rows reproduce with 0 overlapping pairs and 0 labels outside the panel on ggplot2 4.0.3 and 3.5.2 (symbols standalone 183x128, 120x84, 89x70; Ensembl standalone 183x128, 150x105, 120x84; 3- and 4-panel composites at 183x120 and 183x150, both label types); the shipped multi-panel example with defaults is clean (`logs/measure_gg4.log`, `logs/measure_gg35.log`). Documented limits reproduce: Ensembl 89x70 = 1 tie pair (1.5x2.0 mm), 120x110 composite Ensembl 1 pair + 3 outside, symbols 9-11 pairs (ggrepel time-limited, run-to-run). Probe: 183x90 composite 1 pair, re-ranked Ensembl set 3 pairs (`logs/probe_gg4.log`) |
| GG-009 (P2) failure-modes.md misstates the ggrepel drop | corrected | 300 labels: 120 drawn at default with no warning, message or stdout; `verbose = TRUE` reports '180 unlabeled data points (too many overlaps)'; `max.overlaps = Inf` and `options(ggrepel.max.overlaps = Inf)` draw 300; sparse 30-label plot unaffected (`logs/refs_gg4.log`, `logs/refs_gg35.log`) |
| fraction-valued var_explained (residual) | corrected | fraction input: warning 'sums to <= 1 ... Multiply fractions by 100', label 'PC1 (0.6%)'; percent input: no warning, 'PC1 (57.6%) PC2 (26.5%)' equals prcomp(mtcars) (`logs/measure_gg4.log`) |
| GG-001 (P1) volcano threshold on wrong quantity | corrected, not regressed | y equals -log10(padj) recomputed; hline 1.3010 (2 at fdr 0.01); 541/497/17,200 classes (`logs/regress_gg4.log`) |
| GG-002 (P1) save_publication_figure not cairo_pdf/mm | corrected, not regressed | 252x198 pt and 518x340 pt; ArialMT/SymbolMT/Arial-ItalicMT embedded; default pdf() Helvetica unembedded (`logs/pdffonts_regress.log`, `logs/pdffonts.log`) |
| GG-003 (P1) theme/palette drift | corrected, not regressed | blank grid, Okabe-Ito fills/colours, composite keeps theme (`logs/regress_gg4.log`) |
| GG-005 (P2) Grammar block does not render | corrected, not regressed | grammar_183x70.png opened; ticks 3/5/10; all 5 SKILL.md blocks verbatim (`logs/blocks_gg4.log`) |
| GG-006 (P2) failure-mode claims | corrected | salmon #F8766D, size-for-lines warning, aes_string warning, 89 in page, ggrepel drop (`logs/refs_gg4.log`, `logs/blocks_gg4.log`) |
| GG-007 (P2) usage-guide tips | corrected, not regressed | `{{ }}` bare-name caveat reproduces (`logs/blocks_gg4.log`) |
| GG-008 (P2) reproducibility and input contract | corrected, not regressed | seeded jitter identical; clear errors (`logs/regress_gg4.log`) |

## Executed versus static-only

Environment: Windows R 4.4.3 via `r.sh` (ggplot2 4.0.3) and `r-gg35.sh` (ggplot2 3.5.2), ggrepel 0.9.8, patchwork 1.3.2, ggrastr 1.0.2; fingerprint sha256 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721 over `snapshots/lane1_versions.txt` (re-hashed identical); poppler (`pdffonts`, `pdfinfo`) in WSL `dv-cli`. Inputs: staged airway DESeq2 results (19,772 genes), its HGNC-symbol derivative, `datasets::mtcars`. Tool inventory: `TOOLS-bio-data-visualization-ggplot2-fundamentals.md` sha256 5d13e5750af0ab3b172603d035311317491057206d2c3e576c2fd4f73c73c55f. Skill bytes were not edited; SKILL.md blocks ran from a copy of the Skill directory.

| Surface | Classification | Evidence |
|---|---|---|
| `create_volcano` default `top_n = NULL`, plotted values, classes, threshold (GG-001, GG-004) | executed | `scripts/rb_regress.R`, `scripts/rb_na_label.R`, `logs/regress_*.log`, `logs/nalabel_*.log` |
| Label-overlap envelope, drawn ggrepel boxes, every claimed row (GG-004) | executed | `scripts/lane1_gg_overlap_measure.R`, `scripts/lane1_gg_lib_overlap.R`, `logs/measure_gg4.log`, `logs/measure_gg35.log`; figures opened |
| Envelope probe beyond claimed rows (other heights, re-ranked label sets) | executed | `scripts/rb_envelope_probe.R`, `logs/probe_gg4.log` |
| `create_pca_plot` fraction warning and contract | executed | `logs/measure_gg4.log`, `logs/measure_gg35.log` |
| `save_publication_figure`, PDF fonts and page size (GG-002) | executed | `scripts/rb_regress.R`, `scripts/pdffonts_regress.sh`, `logs/pdffonts_regress.log` |
| Theme, Okabe-Ito, boxplot, PCA, multi-panel (GG-003, GG-008) | executed | `scripts/rb_regress.R` |
| SKILL.md R blocks (5), Grammar block (GG-005), tidy eval (GG-007) | executed | `scripts/rb_blocks.R`, `logs/blocks_gg4.log`, `logs/blocks_gg35.log` |
| `references/geoms-scales-facets.md` (23 lines) | executed | `scripts/rb_repel_refs.R`, `logs/refs_gg4.log`, `logs/refs_gg35.log` |
| `references/failure-modes.md` claims incl. GG-009, pdf() fonts, inches default | executed | `scripts/rb_repel_refs.R`, `scripts/pdffonts_rb.sh`, `logs/pdffonts.log` |
| `usage-guide.md` | static-only | prose, prompts and the install line (GG-012 raised statically) |

Reused (not rerun): none. Known noise: ggrepel layout in the 120x110 symbol composites varies between runs (9-11 pairs); the Skill does not claim those rows.

## Veto review

- Skill veto: PASS (stability, contract, determinism, security all PASS).
- Research veto: PASS
  - scientific_integrity: PASS — Volcano classes (541 Up, 497 Down, 17,200 NS among 18,238 padj-bearing airway genes), plotted y values (-log10 padj) and PCA axis labels (57.6 %, 26.5 %) equal independent recomputation; no fabricated values; the label-overlap envelope is stated as measured and reproduces.
  - practice_boundaries: PASS — Plotting skill; no clinical or prescriptive output.
  - methodological_ground: PASS — The volcano threshold sits on the plotted -log10(padj) axis; the fraction-valued var_explained input now warns instead of silently mislabelling.
  - code_usability: PASS — All five SKILL.md R blocks, all six helpers and every references/geoms-scales-facets.md line run on ggplot2 4.0.3 and 3.5.2; the one defect found is a hard error when a label is NA (GG-010), not a failure to run.

## Static categories

- functional_suitability: 11/12 — Covers grammar, theme, programmatic aes, export and helper workflows; the volcano default (10 symbols / 3 IDs) works and every stated zero-overlap row reproduces. The envelope is stated by width only and was measured on one dataset (GG-011).
- reliability: 10/12 — Guards give clear errors (missing var_explained, >8 groups, missing padj or bad label_col) and the fraction var_explained warns. A NA label among the smallest padj (unmapped symbol) now stops create_volcano with 'missing value where TRUE/FALSE needed' (GG-010); crowded panels depend on ggrepel's time-limited layout.
- performance_context: 7/8 — SKILL.md routes to two references and one script; compact, with some restatement across SKILL.md, usage-guide.md and failure-modes.md.
- agent_usability: 14/16 — Idioms, guardrails and the label-collision rule are clear and say 'open the figure'; the envelope omits the composite height and the 'no collisions' wording does not mention threshold lines crossing labels (GG-011).
- human_usability: 7/8 — Readable; failure-modes.md now states the ggrepel drop is silent and names verbose = TRUE. usage-guide prerequisites omit patchwork and dplyr that the shipped script loads (GG-012).
- security: 11/12 — No credentials, network or destructive operations; local ggsave writes only.
- maintainability: 10/12 — Single-purpose helpers on one theme and one palette; no tests; the label-collision limits live in prose, not a guard.
- agent_specific: 17/20 — Precise trigger description, progressive disclosure to two references and a script, guardrails with trigger/mechanism/symptom/fix; first-loop and second-loop corrections all hold.

## Detailed outputs

### Input 1 — Canonical: create_volcano default on airway DESeq2 results (19,772 genes, 1,534 NA padj) plus the create_pca_plot contract, ggplot2 4.0.3 and 3.5.2

**Status:** COMPLETED — Plotted y equals -log10(padj) recomputed from the CSV; hline 1.3010 = FDR cutoff (2 at fdr 0.01); default labels 3 (Ensembl) and 10 (symbols) are the smallest padj; fraction var_explained warns, percent is silent and equals prcomp; identical on 3.5.2.  
**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100

**Assertions:**

- PASS — Volcano classes equal independent classification (541 Up / 497 Down / 17,200 NS) and NA padj rows are filtered without warnings (identical(): helper classes equal ifelse recomputation; 18,238 of 19,772 rows kept; no warnings on build.)
- PASS — The plotted y of every point equals -log10(padj) recomputed from the raw CSV and the horizontal threshold sits on the colour boundary (GG-001) (all.equal on layer data; hline 1.3010; smallest coloured y >= line, largest grey |LFC|>1 y <= line; fdr_threshold = 0.01 moves it to 2.)
- PASS — Default labels are the 3 (Ensembl) or 10 (symbol) smallest padj, and top_n overrides them (Ensembl 3 = three smallest padj; symbols SPARCL1 CACNB2 DUSP1 SAMHD1 MAOA GPX3 STEAP2 NEXN MT2A ADAMTS1; top_n = 5 draws 5.)
- PASS — A fraction-valued var_explained warns and a percent one is silent with labels equal to prcomp variance (fraction: warning 'sums to <= 1 ... Multiply fractions by 100', label 'PC1 (0.6%)'; percent: no warning, 'PC1 (57.6%) PC2 (26.5%)' equals prcomp(mtcars); same on 3.5.2.)
- PASS — Rendered volcano is readable at 89 x 70 mm (standalone_sym_default_89x70.png opened: ten gene symbols, leader lines, no label-label collision.)

### Input 2 — Variant A: Label-overlap envelope: drawn ggrepel label boxes for every row the Skill claims, standalone and create_multi_panel, 3- and 4-panel, on ggplot2 4.0.3 and 3.5.2

**Status:** COMPLETED — Every claimed zero-overlap row reproduces with 0 pairs and 0 labels outside the panel on both versions; the shipped multi-panel example with defaults is clean at 183 x 120 and 183 x 150 mm; documented limits (Ensembl 89 x 70: 1 tie pair; 120 x 110 composite: 1 pair + 3 labels outside for Ensembl, 9-11 pairs for symbols) reproduce as stated; figures opened.  
**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100

**Assertions:**

- PASS — Symbols (10 labels) standalone at 183 x 128, 120 x 84 and 89 x 70 mm have no overlapping label boxes (0 pairs, 0 outside, ggplot2 4.0.3 and 3.5.2; also 89 x 55 and 89 x 89 mm in the probe.)
- PASS — Ensembl IDs (3 labels) standalone at 183, 150 and 120 mm wide have no overlapping label boxes (183 x 128, 150 x 105, 120 x 84: 0 pairs on both versions.)
- PASS — The shipped create_multi_panel example (3- and 4-panel) with the default volcano is clean at 183 mm for symbols and Ensembl IDs (183 x 120 and 183 x 150, 3- and 4-panel, both label types: 0 pairs, 0 outside; multi3_ens_default_183x120 and multi4_sym_default_183x150 opened.)
- PASS — The documented limits reproduce as the Skill states them (120 mm composite collides; Ensembl at 89 mm is not claimed) (Ensembl 89 x 70: 1 tie pair (1.5 x 2.0 mm); 120 x 110 composite: Ensembl 1 pair + 3 outside, symbols 9 (3-panel) and 9-11 (4-panel, ggrepel time-limited run-to-run variance); multi3_sym_default_120x110 opened: labels illegible.)

### Input 3 — Edge: create_volcano default top_n = NULL heuristic and input guards: 8/9-character boundary, NA or empty labels, bad columns, no significant genes

**Status:** PARTIAL — The 8-character boundary is exact (8 chars -> 10 labels, 9 -> 3) and bad columns, no-significant and 4-row inputs behave; an NA label among the smallest padj (an unmapped gene symbol) stops the helper with 'missing value where TRUE/FALSE needed' on both versions, where the explicit top_n = 10 path drew 9 labels.  
**Scores:** Basic 34/40 | Specialized 49/60 | Total 83/100

**Assertions:**

- PASS — Labels of 8 characters or fewer give 10 labels and 9 characters give 3 (G%07d labels -> 10; G%08d -> 3; ggplot2 4.0.3 and 3.5.2.)
- FAIL — A NA label among the smallest padj (unmapped symbol, label_col = 'symbol') does not crash the helper (max(nchar(lead)) is NA, so `if` errors: 'missing value where TRUE/FALSE needed'; top_n = 10 builds with 9 labels; empty-string symbol builds.)
- PASS — Missing padj column, bad label_col, missing var_explained and more than 8 PCA groups raise errors that name the cause ('object padj not found' (named in the message); 'Column `nope` not found'; "pca_df needs a 'var_explained' column"; 'Okabe-Ito has 8 colours; got 12 groups. Collapse groups or facet.')
- PASS — A 4-row input, a factor label column and an input with no significant genes build without error (4 rows -> 1 label; factor labels -> 3; padj = 0.9 everywhere builds with no labels.)

### Input 4 — Variant B: save_publication_figure, PDF fonts and page size, PNG pixels, theme/Okabe-Ito consistency, boxplot and PCA helpers (first-loop corrections GG-002/003/008)

**Status:** COMPLETED — Default save is 252 x 198 pt (89 x 70 mm) and 1051 x 826 px; 183 x 120 mm gives 518 x 340 pt and 2161 x 1417 px; ArialMT, SymbolMT and Arial-ItalicMT embedded; default pdf() leaves Helvetica unembedded; theme and palette consistent across helpers and the composite; jitter seeded.  
**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100

**Assertions:**

- PASS — save_publication_figure writes cairo_pdf pages of the requested mm size (pdfinfo 252 x 198 pt default and 518 x 340 pt at 183 x 120 mm, 4.0.3 and 3.5.2.)
- PASS — Helper PDFs embed TrueType fonts while the default pdf() device does not (the Skill's stated reason for cairo_pdf) (pdffonts: ArialMT/SymbolMT/Arial-ItalicMT TrueType emb yes; default pdf() and ggsave() without device: Helvetica Type 1 emb no; width = 89 without units gives a 6408 x 5040 pt page.)
- PASS — PNG output is 300 dpi at the stated mm size (1051 x 826 px and 2161 x 1417 px.)
- PASS — theme_publication has a blank grid, every helper and the composite use it, and boxplot/PCA fills are Okabe-Ito (fills #0072B2 #D55E00 #009E73; PCA colours the same set; every patchwork sub-plot keeps the blank grid.)
- PASS — Boxplot jitter is reproducible and medians equal raw medians (identical jitter x on two calls; middle equals tapply median for A, B, C.)

### Input 5 — Stress: SKILL.md R blocks and reference snippets run as written, failure-mode claims (including GG-009 silent ggrepel drop) reproduce, on both ggplot2 versions

**Status:** COMPLETED — All five SKILL.md R blocks run verbatim from a Skill copy with no warnings; the Grammar block renders colour-coded jitter with plain log ticks 3/5/10 and the 'Expression' title; 23 geoms-scales-facets lines build; ggrepel default drops 180 of 300 labels with no message, Inf draws 300, verbose = TRUE reports it.  
**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100

**Assertions:**

- PASS — Every R block in SKILL.md runs verbatim and the Grammar block renders as described (GG-005) (5 of 5 blocks, no warnings; grammar_183x70.png opened: colour mapped, ticks 3/5/10, y title 'Expression'; ggtext block renders subscripts.)
- PASS — Every code line in references/geoms-scales-facets.md builds (23 of 23 on both versions, including scale_color_scico after library(scico).)
- PASS — failure-modes.md states the ggrepel drop correctly: silent, verbose = TRUE only, Inf or the option fixes it (GG-009) (300 labels at default: 120 drawn, no warning, message or stdout; verbose = TRUE emits 'ggrepel: 180 unlabeled data points (too many overlaps)'; max.overlaps = Inf and options(ggrepel.max.overlaps = Inf) draw 300; a sparse 30-label plot is unaffected.)
- PASS — The other failure-mode claims reproduce (salmon #F8766D for aes(color = 'red'), size-for-lines warning, aes_string deprecation, inches default) (#F8766D; 'Using `size` aesthetic for lines was deprecated in ggplot2 3.4.0'; '`aes_string()` was deprecated in ggplot2 3.0.0'; 89 in = 6408 pt page.)

## Key strengths

- Every label-overlap row the Skill claims reproduces under drawn-box measurement on ggplot2 4.0.3 and 3.5.2, and the shipped multi-panel example with defaults is clean.
- The helper default adapts the label count to label length (10 symbols / 3 IDs) and the Skill states where it still collides and tells the agent to open the figure.
- First-loop fixes hold: volcano threshold on the plotted -log10(padj), cairo_pdf and mm saving with embedded TrueType, one theme and one Okabe-Ito palette, seeded jitter, clear input errors.
- Failure-modes.md is now accurate about the silent ggrepel drop and every Grammar and reference snippet runs as written.

## Recommendations

- **[P2] GG-010 create_volcano stops with a cryptic error when a label among the smallest padj is NA** (inputs [3]): With the new default top_n = NULL the helper evaluates max(nchar(lead)); a NA label (an unmapped gene symbol, the usual result of an org.Hs.eg.db lookup) makes the result NA and `if` fails with 'missing value where TRUE/FALSE needed' on ggplot2 4.0.3 and 3.5.2; with an explicit top_n the same data builds. Fix: Local code change of one line (max(nchar(lead), na.rm = TRUE), or treat NA as long) and, optionally, one sentence in SKILL.md telling the agent to fill unmapped symbols with the Ensembl ID before labelling.
- **[P2] GG-011 The zero-overlap envelope omits composite height and dataset, and 'no collisions' means label boxes only** (inputs [2]): The Resources line says composites collide-free 'at 183 mm', but the claim was measured at 183 x 120 and 183 x 150 mm on the airway data; a 183 x 90 mm composite with the default airway symbols has 1 overlapping pair (STEAP2~MAOA) and a re-ranked Ensembl set (3 extreme-LFC IDs) has 3 pairs at 183 x 120 mm. Threshold lines and points also cross labels in the clean rows (183 x 120 Ensembl composite), which a reader may take as collisions. Fix: Text-only: state 'measured on the airway DESeq2 results at 183 x 120 mm and taller', say the count is label-label boxes only, and keep 'open the figure'.
- **[P2] GG-012 usage-guide prerequisites omit packages the shipped script loads** (inputs [5]): usage-guide.md installs ggplot2, scales, ggrepel, ggtext, viridis, scico and ggrastr, but scripts/publication_figures.R calls library(patchwork) and library(dplyr); on a fresh R the documented source() step fails. SKILL.md's version line also keeps a stray "axes='collect'" note for a feature the Skill does not use. Fix: Text-only: add patchwork and dplyr to the install.packages line and drop the unused axes='collect' remark.

## Ordered finding ledger

Audited identity: `be703ae7f69598daa981d477afa71a873d0616a2f2830936b575c014a1f3f120`

| Order | ID | Priority | State | Evidence inputs | Required disposition |
|---:|---|---|---|---|---|
| 1 | GG-010 | P2 | open | [3] | create_volcano stops with a cryptic error when a label among the smallest padj is NA. Local code change of one line (max(nchar(lead), na.rm = TRUE), or treat NA as long) and, optionally, one sentence in SKILL.md telling the agent to fill unmapped symbols with the Ensembl ID before labelling. |
| 2 | GG-011 | P2 | open | [2] | The zero-overlap envelope omits composite height and dataset, and 'no collisions' means label boxes only. Text-only: state 'measured on the airway DESeq2 results at 183 x 120 mm and taller', say the count is label-label boxes only, and keep 'open the figure'. |
| 3 | GG-012 | P2 | open | [5] | usage-guide prerequisites omit packages the shipped script loads. Text-only: add patchwork and dplyr to the install.packages line and drop the unused axes='collect' remark. |

GG-001 to GG-009 and the PCA fraction warning are corrected and not listed (see verdicts in the viewer). GG-010 to GG-012 are new P2 findings; GG-011 and GG-012 are text-only, GG-010 is a one-line code change. No audit-local repair was made; no Skill bytes changed.
