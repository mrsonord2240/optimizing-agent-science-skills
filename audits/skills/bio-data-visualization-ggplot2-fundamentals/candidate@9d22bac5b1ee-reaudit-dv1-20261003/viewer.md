> **Audit record for `bio-data-visualization-ggplot2-fundamentals`**
> - Audited working candidate `9d22bac5b1ee4b3c7a26211b5f6033f1658a8ac43fb2514e02026ee32b12c54e`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/data-visualization/ggplot2-fundamentals), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-data-visualization-ggplot2-fundamentals

Generated: 2026-10-03  
Audit type: final independent re-audit (certification run) of the fixed candidate  
Exact candidate content SHA-256: `9d22bac5b1ee4b3c7a26211b5f6033f1658a8ac43fb2514e02026ee32b12c54e`

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 37 | 55 | 92 | 4/4 | ✅ COMPLETED |
| 2 | Variant A | 37 | 54 | 91 | 5/5 | ✅ COMPLETED |
| 3 | Variant B | 36 | 53 | 89 | 5/5 | ✅ COMPLETED |
| 4 | Stress | 28 | 40 | 68 | 3/5 | ⚠️ COMPLETED |
| 5 | Canonical | 38 | 56 | 94 | 5/5 | ✅ COMPLETED |
| 6 | Edge | 32 | 46 | 78 | 4/5 | ✅ COMPLETED |

**Execution average:** 85.3 / 100  
**Assertion pass rate:** 26 / 29  
**Static score:** 84 / 100  
**Final score:** 85 / 100 — ⭐ Production Ready  
**Research veto:** PASS

Readiness decision: **not candidate-ready** (GG-004 P1 still open; assertion pass rate 26/29 = 89.7 % is under the 90 % gate). Exact identity is in [`source-identity.json`](source-identity.json).

## Prior findings (initial audit 34a174ab0263)

| Prior finding | Verdict | Evidence |
|---|---|---|
| GG-001 (P1) volcano threshold on wrong quantity | corrected | y = -log10(padj) equals independent recomputation; hline 1.3010 = FDR cutoff; smallest coloured point 1.3035, largest grey |LFC|>1 point 1.3004 (`logs/r1_gg4.log`) |
| GG-002 (P1) save_publication_figure not cairo_pdf/mm | corrected | 252 x 198 pt default, 518 x 340 pt at 183 x 120 mm; ArialMT/SymbolMT/Arial-ItalicMT embedded (`logs/pdffonts.log`) |
| GG-003 (P1) theme/palette drift from SKILL baseline | corrected | borderless theme_classic, no grid, black axes, bold strips; one Okabe-Ito vector in every helper; multi-panel keeps the theme (`logs/r1_gg4.log`) |
| GG-004 (P1) volcano label overlaps | partly corrected; still open P1 | standalone 183 mm clean; default multi-panel at 183 mm and top_n = 3 at 89 mm still overlap; symbols clean (`logs/r2_lab4.log`) |
| GG-005 (P2) Grammar block does not render as written | corrected | grammar_block.png opened: colour mapped, ticks 3/5/10, title 'Expression' |
| GG-006 (P2) failure-mode claims | partly corrected | colour (#F8766D) and per-label trigger reproduce; 'dropped with a warning' does not (see GG-009) |
| GG-007 (P2) inert/malformed usage-guide tips | corrected | tips replaced; `{{ }}` bare-name caveat reproduces (`logs/r3_snip4.log`) |
| GG-008 (P2) reproducibility and input contract | corrected | seeded jitter identical; clear errors for missing var_explained and >8 groups |

## Executed versus static-only

Environment: Windows R 4.4.3 via `r.sh` (ggplot2 4.0.3) and `r-gg35.sh` (ggplot2 3.5.2); fingerprint sha256 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721 over `snapshots/lane1_versions.txt` (re-hashed identical); poppler 26.07.0 (`pdffonts`, `pdfinfo`) in WSL `dv-cli`. Inputs: public airway DESeq2 results (19,772 genes) and `datasets::mtcars`; gene symbols from the staged `org.Hs.eg.db`.

| Surface | Classification | Evidence |
|---|---|---|
| `scripts/publication_figures.R` create_volcano (GG-001) | executed | `scripts/r1_gg.R`, `logs/r1_gg4.log`, `logs/r1_gg35.log` |
| `save_publication_figure` and PDF fonts/page size (GG-002) | executed | `scripts/r1_gg.R`, `scripts/pdffonts.sh`, `logs/pdffonts.log` |
| `theme_publication`, `okabe_ito`, multi-panel theme (GG-003) | executed | `scripts/r1_gg.R` element-level checks |
| Label collisions, create_volcano and create_multi_panel, 85-183 mm (GG-004) | executed | `scripts/r2_labels.R`, `scripts/lib_overlap.R` (box measurement from drawn ggrepel grobs), `logs/r2_lab4.log` (4.0.3, full matrix), `logs/r2_lab35.log` (3.5.2, key rows); figures opened |
| create_boxplot, create_pca_plot guards (GG-008) | executed | `scripts/r1_gg.R` |
| SKILL.md snippets (Grammar block GG-005, theme, tidy eval GG-007, ggtext, rasterise, PNG/TIFF, cairo) | executed | `scripts/r3_snippets.R`, `logs/r3_snip4.log`, `logs/r3_snip35.log`; grammar_block.png, ggtext.png opened |
| `references/geoms-scales-facets.md` (23 lines) | executed | `scripts/r6_reference.R`, `logs/r6_ref4.log`, `logs/r6_ref35.log` |
| `references/failure-modes.md` claims (GG-006) | executed | `scripts/r3_snippets.R`, `scripts/r5_repel.R`, `logs/r5_repel4.log` |
| Volcano y-axis title "purple minus" observation | executed | `scripts/r4_minus.R`, `logs/r4_minus4.log`, `out/minus_compare.png`: a `png()` device artefact (coloured sub-pixel fringes on the thin minus glyph in `png()` under both ggplot2 versions), absent in `ggsave()` output; not a Skill defect |
| `usage-guide.md` | static-only | prose, tips and prompts; its claims are covered by the executed rows above |

## Veto review

- Skill veto: PASS (stability, contract, determinism, security all PASS).
- Research veto: PASS
  - scientific_integrity: PASS — Volcano classes (541 Up, 497 Down, 17,200 NS among 18,238 padj-bearing airway genes), the plotted y values (-log10 padj) and PCA variance labels (57.6 %, 26.5 %) equal independent recomputation; no fabricated values.
  - practice_boundaries: PASS — Plotting skill; no clinical or prescriptive output.
  - methodological_ground: PASS — The volcano threshold now sits on the plotted -log10(padj) axis; no methodological fallacy remains.
  - code_usability: PASS — All six helpers, every SKILL.md block and every references/geoms-scales-facets.md line built and rendered on ggplot2 4.0.3 and 3.5.2; the remaining defect is label collision, not failure to run.

## Static categories

- functional_suitability: 10/12 — Covers the grammar, theme, programmatic aes, export and helper workflows, and the first four fixes hold; the shipped create_multi_panel with the default volcano still prints overlapping Ensembl labels (GG-004).
- reliability: 10/12 — Input guards give clear errors (missing var_explained, >8 groups, missing padj/label column) and jitter is seeded; a fraction-valued var_explained is silently labelled '0.6%' (the contract says percent). Label placement is only reliable at >= ~150 mm with Ensembl IDs.
- performance_context: 7/8 — SKILL.md routes to two references and one script; compact, with some restatement across SKILL.md, usage-guide.md and failure-modes.md.
- agent_usability: 13/16 — Idioms and guardrails are clear and the theme/palette now come from one script; the narrow-panel label rule ('top_n = 3 under ~90 mm') is wrong at both ends (GG-004).
- human_usability: 7/8 — Readable; usage-guide tips repaired. failure-modes.md says ggrepel drops labels 'with a warning' and elsewhere 'silently' (GG-009).
- security: 11/12 — No credentials, network or destructive operations; local ggsave writes only.
- maintainability: 10/12 — Single-purpose helpers on one theme and one palette; no tests; label-collision limits live in prose, not a guard.
- agent_specific: 16/20 — Precise trigger description and progressive disclosure to two references and a script; two failure-mode statements about ggrepel are inaccurate (GG-009).

## Detailed outputs

### Input 1 — Canonical: create_volcano on airway DESeq2 results (19,772 genes, 1,534 NA padj): plotted quantity, threshold line, labels at 183 mm

**Status:** COMPLETED — Plotted y equals -log10(padj) computed independently; hline 1.3010 = FDR cutoff; min coloured point 1.3035, max grey |LFC|>1 point 1.3004; 10 labels, 0 overlaps at 183 mm, no warnings, identical on 3.5.2.  
**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100

**Assertions:**

- PASS — Volcano classes equal independent classification (541 Up / 497 Down / 17,200 NS) (Exact match; NA padj filtered with no warnings.)
- PASS — The plotted y of every point equals -log10(padj) recomputed from the raw CSV (all.equal on ggplot_build layer data (GG-001).)
- PASS — The horizontal threshold lies on the colour boundary in the same quantity (hline 1.3010; smallest coloured y 1.3035; largest grey y with |LFC|>1 is 1.3004; fdr_threshold = 0.01 moves the line to 2.)
- PASS — The ten labelled genes are the ten smallest padj and are not overlapping at 183 mm (Measured label boxes: 10 drawn, 0 overlapping pairs; standalone_top10_w183.png opened.)

### Input 2 — Variant A: save_publication_figure defaults and 183 x 120 mm, fonts and page size inspected with pdffonts/pdfinfo

**Status:** COMPLETED — Default save is 252 x 198 pt (89 x 70 mm) and 1051 x 826 px; 183 x 120 mm gives 518 x 340 pt; ArialMT/SymbolMT/Arial-ItalicMT embedded; default pdf() device still leaves Helvetica/Symbol unembedded as the Skill states.  
**Scores:** Basic 37/40 | Specialized 54/60 | Total 91/100

**Assertions:**

- PASS — Default PDF page size is 89 x 70 mm (pdfinfo 252 x 198 pt (GG-002).)
- PASS — 183 x 120 mm PDF page is 518 x 340 pt (pdfinfo 518 x 340 pt on 4.0.3 and 3.5.2.)
- PASS — All fonts of the helper PDF are embedded TrueType (pdffonts: ArialMT, SymbolMT, Arial-ItalicMT, emb yes sub yes.)
- PASS — Default ggsave PDF leaves Helvetica/Symbol unembedded (Skill's stated reason for cairo_pdf) (pdffonts on default_dev.pdf: Helvetica, Helvetica-Oblique, Symbol Type 1 emb no.)
- PASS — PNG is 300 dpi at the stated mm size (1051 x 826 and 2161 x 1417 px.)

### Input 3 — Variant B: Theme/palette consistency (GG-003), boxplot and PCA helpers on synthetic groups and prcomp(mtcars)

**Status:** COMPLETED — theme_publication is borderless theme_classic with no grid and black axes; every helper and the multi-panel composite use it and the single Okabe-Ito vector; boxplot jitter is seeded; PCA labels equal prcomp; errors are clear.  
**Scores:** Basic 36/40 | Specialized 53/60 | Total 89/100

**Assertions:**

- PASS — theme_publication equals the SKILL baseline (theme_classic, no grid, no border, black axes, bold strips) (Element-level comparison against theme_classic(base_size = 10); no redefinition elsewhere.)
- PASS — Volcano, boxplot and PCA colours are drawn only from the Okabe-Ito vector in SKILL.md (Built layer colours subset of okabe_ito; okabe_ito[1:2] = #0072B2/#D55E00.)
- PASS — Multi-panel panels keep the borderless theme_publication (plot_theme of every patchwork sub-plot has blank border and grid.)
- PASS — Boxplot medians equal raw medians, jitter reproducible, PCA axis labels equal prcomp variance, guards raise clear errors (all.equal on medians; identical jitter; 'PC1 (57.6%)'; clear errors for missing var_explained and 12 groups.)
- PASS — Volcano with a missing padj column or a bad label_col fails with a message naming the column ('object padj not found' in argument !is.na(padj); 'Column `nope` not found in `.data`'.)

### Input 4 — Stress: Label collision matrix: create_volcano Ensembl IDs vs symbols, standalone and create_multi_panel, 85-183 mm, ggplot2 4.0.3 and 3.5.2

**Status:** COMPLETED — Label boxes measured from drawn ggrepel grobs and figures opened. Default top_n = 10 collides at 120 mm (1 pair), 89 mm (6) and in the shipped 3- and 4-panel composites at 183 mm (2-3 pairs); the Skill's top_n = 3 remedy still collides at 89 mm (1 pair) and at 120 x 110 mm; symbols are clean everywhere tested.  
**Scores:** Basic 28/40 | Specialized 40/60 | Total 68/100

**Assertions:**

- FAIL — The default create_multi_panel example with the default volcano renders without overlapping labels (multi3 183x120: 3 overlapping pairs; multi3 183x150 and multi4 183x150: 2 pairs each (ENSG00000152583~ENSG00000165995 and ENSG00000157214~ENSG00000189221 by 3.8 and 14-15 mm); same on 3.5.2.)
- FAIL — The Skill's rule 'top_n = 3 in panels under ~90 mm' yields clean labels at those widths (Standalone 89 x 70 mm with top_n = 3: ENSG00000152583 overlaps ENSG00000165995 by 1.5 mm; 85 mm control the same; at 120 x 110 mm in a 4-panel 1 pair and 3 labels leave the panel.)
- PASS — The Skill's multi-panel guidance (top_n = 3) is clean at 183 mm (multi3 and multi4 at 183 x 120 and 183 x 150: 0 overlapping pairs, 4.0.3 and 3.5.2.)
- PASS — Short gene symbols with top_n = 10 are clean at 89 mm and in the 183 mm composites (Symbols mapped with org.Hs.eg.db: 0 overlapping pairs in standalone 89 and 183 mm and multi3/multi4 composites; opened multi4_symbols10_183x150.png.)
- PASS — Labels are never silently dropped by the helper (max.overlaps = Inf: 10 of 10 labels drawn in every top_n = 10 cell and 3 of 3 with top_n = 3 (none dropped, though some overlap).)

### Input 5 — Canonical: SKILL.md and reference snippets run as written: Grammar block, theme, tidy eval, ggtext, rasterise, PNG/TIFF, geoms-scales-facets (23 lines), on both ggplot2 versions

**Status:** COMPLETED — Every block builds and renders without warnings except the documented ones; Grammar block now shows colour-coded jitter, log ticks 3/5/10, 'Expression' title; rasterised PDF is 63 KB versus 634 KB all-vector; results identical on 4.0.3 and 3.5.2.  
**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100

**Assertions:**

- PASS — Grammar in Layers block renders as its comments describe (Opened grammar_block.png: ctrl/trt in #0072B2/#D55E00, y ticks 3 5 10 (no 10^0.477), title 'Expression' (GG-005).)
- PASS — Tidy-eval blocks map the named columns and the {{ }} string caveat is true (.data[[ ]] and {{ }} with bare names reproduce mtcars$wt; {{ }} with strings maps a constant (GG-007 wording); aes_string deprecation warning emitted.)
- PASS — ggtext label block renders a true minus and subscripts; cairo_pdf embeds the CID TrueType font (Opened ggtext.png; pdffonts ArialMT TrueType and CID TrueType emb yes.)
- PASS — rasterise() keeps vector axes and shrinks the PDF; PNG 89 mm @300 dpi; TIFF LZW written (63 KB vs 634 KB; 1051 x 826 px; figure.tiff written.)
- PASS — All 23 reference snippet lines build and save without warning or error (r6_reference.R: 23/23 PASS on 4.0.3 and 3.5.2.)

### Input 6 — Edge: failure-modes.md claims reproduced (colour, linewidth, ggrepel default drop, default pdf device, inches trap)

**Status:** COMPLETED — Four of five claims reproduce; ggrepel 0.9.8 drops labels with no warning at all (message only when verbose = TRUE), contradicting 'dropped with a warning' and the 'warning buried in log' symptom.  
**Scores:** Basic 32/40 | Specialized 46/60 | Total 78/100

**Assertions:**

- PASS — aes(color = 'red') renders salmon #F8766D with a 'red' legend entry (Built colour #F8766D.)
- PASS — size = on geom_line warns in ggplot2 >= 3.4 ('Using `size` aesthetic for lines was deprecated in ggplot2 3.4.0.')
- PASS — Default ggrepel drops labels at default max.overlaps and Inf draws them all (300 clustered labels: 120 drawn by default, 300 with max.overlaps = Inf.)
- FAIL — The drop is accompanied by a warning in the log, as failure-modes.md states (No warning or message at draw time on ggrepel 0.9.8 (message only if verbose = TRUE); the file also says 'silently missing' in the same entry.)
- PASS — Default pdf() leaves fonts unembedded; width 89 without units gives an 89 inch page (pdffonts Helvetica emb no; pdfinfo 6408 x 5040 pt.)

## Key strengths

- GG-001, GG-002, GG-003, GG-005, GG-007 and GG-008 reproduce as fixed: the volcano y axis and threshold share one quantity, the helper PDF is a 518 x 340 pt cairo_pdf with embedded TrueType, and every helper wears one borderless theme and one Okabe-Ito vector.
- Every SKILL.md block and all 23 reference snippet lines build and render, identically on ggplot2 4.0.3 and 3.5.2.
- Input guards (missing var_explained, over 8 groups, missing padj or label column) fail with actionable messages.
- Core export claims are verified by pdffonts: cairo_pdf embeds TrueType, the default device does not, rasterise() shrinks the PDF tenfold.

## Recommendations

- **[P1] GG-004 Long-ID volcano labels still collide where the Skill promises clean** (inputs [4]): The shipped 3- and 4-panel create_multi_panel with the default volcano overprints 2-3 label pairs at 183 mm; the Skill's top_n = 3 rule 'under ~90 mm' still collides at 89 mm (1 pair) and at 120 mm, while a 91 mm slot (183 mm composite) already needs it; only gene symbols were clean in every cell. Fix: Text-only: tell the agent to pass label_col with gene symbols for any multi-panel or single-column volcano, to use Ensembl IDs only standalone at roughly 150 mm or wider, and to measure or open the figure; optionally set the helper default to legend.position = 'bottom' in panels.
- **[P2] GG-009 failure-modes.md misstates the ggrepel drop warning** (inputs [6]): The ggrepel entry says labels are dropped 'with a warning' and that the warning is 'buried in log'; ggrepel 0.9.8 emits nothing unless verbose = TRUE, so the drop is fully silent. Fix: Text-only: say the drop is silent, name verbose = TRUE as the only message, and keep 'count the labels actually drawn'.

## Ordered finding ledger

Audited identity: `9d22bac5b1ee4b3c7a26211b5f6033f1658a8ac43fb2514e02026ee32b12c54e`

| Order | ID | Priority | State | Evidence inputs | Required disposition |
|---:|---|---|---|---|---|
| 1 | GG-004 | P1 | open | [4] | Long-ID volcano labels still collide where the Skill promises clean. Text-only: tell the agent to pass label_col with gene symbols for any multi-panel or single-column volcano, to use Ensembl IDs only standalone at roughly 150 mm or wider, and to measure or open the figure; optionally set the helper default to legend.position = 'bottom' in panels. |
| 2 | GG-009 | P2 | open | [6] | failure-modes.md misstates the ggrepel drop warning. Text-only: say the drop is silent, name verbose = TRUE as the only message, and keep 'count the labels actually drawn'. |

GG-001, GG-002, GG-003, GG-005, GG-007 and GG-008 are corrected and not listed. No audit-local repair was made; no Skill bytes changed.
