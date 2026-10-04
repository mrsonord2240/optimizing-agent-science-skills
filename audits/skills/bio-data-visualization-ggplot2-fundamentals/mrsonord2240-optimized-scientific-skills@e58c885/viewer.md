> - Provider binding: exact committed bytes at [mrsonord2240/optimized-scientific-skills@e58c885](https://github.com/mrsonord2240/optimized-scientific-skills/tree/e58c8855faaf8dcba2341453d73b62bcade3e78c/skills/bio-data-visualization-ggplot2-fundamentals) match audited candidate `9d1247b0d8cd48c336a6e7ca866603cc3499b667e759af8f866583d076f0507b` byte for byte. The scientific report was neither re-executed nor rewritten.

> **Audit record for `bio-data-visualization-ggplot2-fundamentals`**
> - Audited working candidate `9d1247b0d8cd48c336a6e7ca866603cc3499b667e759af8f866583d076f0507b`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/data-visualization/ggplot2-fundamentals), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-data-visualization-ggplot2-fundamentals

Generated: 2026-10-03  
Audit type: delta re-audit (frontmatter `description` trimmed to its "Use when ..." clause)  
Exact candidate content SHA-256: `9d1247b0d8cd48c336a6e7ca866603cc3499b667e759af8f866583d076f0507b` (files=5, bytes=23077)  
Certified baseline (carried forward): `228c088cf299564fd21d2b9d79a3963e5c0b4a500158bcb4732a1b277e6160e6` (files=5, bytes=23322), record `candidate@228c088cf299-delta-dv1-20261003`

## Delta qualification

- `skill_preflight --offline` on the candidate: PASS, identity 9d1247b0d8cd48c336a6e7ca866603cc3499b667e759af8f866583d076f0507b, files=5, bytes=23077 (re-checked at the end of the run).
- Reverting `edits.json` (fix-description-20261003) on a scratch copy (`scripts/desc_qualify.py`, `scripts/logs/qualify.log`) reproduces the certified identity 228c088cf299564fd21d2b9d79a3963e5c0b4a500158bcb4732a1b277e6160e6 exactly.
- File sets are identical; exactly one file differs (`SKILL.md`), and exactly one line (line 3, `description:`) differs (`scripts/diff_SKILL.md.txt`). No script, reference or usage-guide byte changed.
- The new frontmatter parses with a YAML loader as a single string beginning "Use when" (log above); `name` equals the directory name.
- Delta mode qualifies: prose/frontmatter only, under the contract's limits.

## New description

> Use when producing static publication-quality figures in R with ggplot2 for papers, presentations, or reports.

Verdict: Sufficient and accurate. It names the tool (ggplot2), the language (R) and the intent (static publication figures for papers, presentations or reports), which separates it from the matplotlib Skill (Python) and from the shelf's specialised plot Skills (volcano, forest, oncoprint, network, sequence logo, annotation, dimensionality reduction, palettes), none of which is a generic ggplot2 fundamentals Skill. Dropped detail (cairo_pdf, tidy evaluation, theme_classic) is body content.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 38 | 56 | 94 | 5/5 | ✅ COMPLETED |
| 2 | Variant A | 37 | 55 | 92 | 4/4 | ✅ COMPLETED |
| 3 | Edge | 34 | 49 | 83 | 3/4 | ❌ PARTIAL |
| 4 | Variant B | 37 | 55 | 92 | 5/5 | ✅ COMPLETED |
| 5 | Stress | 37 | 55 | 92 | 4/4 | ✅ COMPLETED |

**Execution average:** 90.6 / 100  
**Assertion pass rate:** 21 / 22 (95.5 %)  
**Static score:** 90 / 100  
**Final score:** 90 / 100 — ⭐ Production Ready  
**Research veto:** PASS

Readiness decision: **candidate-ready** for this exact identity (final 90, static 90, execution average 90.6, assertions 21/22, no veto, no open P0 or P1; open P2: GG-010). Scores are the certifying record's, carried forward; the static score did not move.

## Finding verdicts

| Finding | Verdict | Evidence |
|---|---|---|
| GG-010 (P2) | open, untouched | no code or body change in this delta; certifying evidence stands |
| Description trim | no new finding | accurate to the Skill body, parses as one YAML string, sufficient trigger (see verdict above) |
| Other certified findings and passes | carried forward unchanged | every non-frontmatter byte is identical to the certified bytes, so the certifying record's execution evidence (record `candidate@228c088cf299-delta-dv1-20261003` and its scripts) applies unchanged |

## Executed versus carried

| Surface | Classification | Evidence |
|---|---|---|
| Changed line (frontmatter `description`) | executed | YAML parse and revert/diff qualification, `scripts/logs/qualify.log` |
| All scripts and workflows | carried (hash-identical to the certified bytes) | record `candidate@228c088cf299-delta-dv1-20261003`; no behaviour changed, no rerun required by the delta contract |

## Veto review

- Skill veto: PASS (stability, contract, determinism, security all PASS); carried, no executable byte changed.
- Research veto: PASS
  - scientific_integrity: PASS — Volcano classes (541 Up, 497 Down, 17,200 NS among 18,238 padj-bearing airway genes), plotted y values (-log10 padj) and PCA axis labels (57.6 %, 26.5 %) equal independent recomputation; no fabricated values; the label-overlap envelope is stated as measured and reproduces.
  - practice_boundaries: PASS — Plotting skill; no clinical or prescriptive output.
  - methodological_ground: PASS — The volcano threshold sits on the plotted -log10(padj) axis; the fraction-valued var_explained input now warns instead of silently mislabelling.
  - code_usability: PASS — All five SKILL.md R blocks, all six helpers and every references/geoms-scales-facets.md line run on ggplot2 4.0.3 and 3.5.2; the one defect found is a hard error when a label is NA (GG-010), not a failure to run.

## Static categories

- functional_suitability: 12/12 — Covers grammar, theme, programmatic aes, export and helper workflows; the volcano default (10 symbols / 3 IDs) works and the stated zero-overlap envelope now names width and height, the dataset and 'label boxes only', each re-measured (GG-011 closed).
- reliability: 10/12 — Guards give clear errors (missing var_explained, >8 groups, missing padj or bad label_col) and the fraction var_explained warns. A NA label among the smallest padj (unmapped symbol) now stops create_volcano with 'missing value where TRUE/FALSE needed' (GG-010); crowded panels depend on ggrepel's time-limited layout.
- performance_context: 7/8 — SKILL.md routes to two references and one script; compact, with some restatement across SKILL.md, usage-guide.md and failure-modes.md.
- agent_usability: 15/16 — Idioms, guardrails and the label-collision rule are clear and say 'open the figure'; the envelope now states the composite height, the single measured dataset and that threshold lines and points can still cross labels.
- human_usability: 8/8 — Readable; failure-modes.md states the ggrepel drop is silent; the usage-guide install line now names every package the shipped script loads (GG-012 closed).
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
