> **Audit record for `bio-data-visualization-ggplot2-fundamentals`**
> - Audited working candidate `34a174ab026364c4b2884a4465ee5bd6b13eb0d80609c9f0ce729ac0746f159a`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/data-visualization/ggplot2-fundamentals), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-data-visualization-ggplot2-fundamentals

Generated: 2026-10-03  
Audit type: bounded diagnostic initial audit  
Exact candidate content SHA-256: `34a174ab026364c4b2884a4465ee5bd6b13eb0d80609c9f0ce729ac0746f159a`

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 31 | 42 | 73 | 2/4 | ⚠️ COMPLETED |
| 2 | Variant A | 33 | 43 | 76 | 2/4 | ✅ COMPLETED |
| 3 | Edge | 28 | 38 | 66 | 3/4 | ⚠️ COMPLETED |
| 4 | Variant B | 31 | 42 | 73 | 3/4 | ⚠️ COMPLETED |
| 5 | Stress | 30 | 41 | 71 | 2/4 | ⚠️ COMPLETED |

**Execution average:** 71.8 / 100  
**Assertion pass rate:** 12 / 20  
**Static score:** 76 / 100  
**Final score:** 74 / 100 — ⚠️ Beta Only  
**Research veto:** PASS

This score is diagnostic. It does not make the candidate ready. Findings are ordered in the ledger below; exact identity is in [`source-identity.json`](source-identity.json).

## Executed versus static-only

Environment: Windows R 4.4.3 via `r.sh` (ggplot2 4.0.3) and `r-gg35.sh` (ggplot2 3.5.2); fingerprint sha256 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721 over `snapshots/lane1_versions.txt`; pdffonts 26.07.0 in WSL `dv-cli`. Input: public airway DESeq2 results (19,772 genes) and `datasets::mtcars`.

| Surface | Classification | Evidence |
|---|---|---|
| `scripts/publication_figures.R` (six helpers) | executed | `scripts/g1_example.R`, logs `logs/g1_example_gg4.log`, `logs/g1_example_gg35.log`; figures `out/ex4/`, `out/ex35/` opened |
| SKILL.md and reference snippets (grammar, tidy eval, ggtext, rasterise, export, theme_pub, geoms/scales/facets) | executed | `scripts/g2_snippets.R`, logs `logs/g2_snippets_gg*.log`; `out/snip4/` opened |
| PDF font embedding | executed | `scripts/pdffonts.sh`, `logs/pdffonts_*.log` |
| `usage-guide.md`, `references/failure-modes.md` claims | executed where testable (colour, ggrepel, axis-line tip); remainder static-only | g2 log |

## Veto review

- Skill veto: PASS (stability, contract, determinism, security all PASS).
- Research veto: PASS
  - scientific_integrity: PASS — No fabricated values. Volcano class counts (541 Up, 497 Down, 18,734 NS of 19,772 airway genes) and PCA variance labels (57.6 %, 26.5 %) equal independent recomputation.
  - practice_boundaries: PASS — Plotting skill; no clinical or prescriptive output.
  - methodological_ground: PASS — No principled fallacy. The volcano threshold line is drawn on the wrong quantity (GG-001), filed as a defect, not a conclusion-inverting method error.
  - code_usability: PASS — All six helpers and every SKILL.md block ran on ggplot2 4.0.3 and 3.5.2; defects are wrong behaviour in shipped code (GG-001..GG-004), filed P1.

## Static categories

- functional_suitability: 9/12 — Complete core ggplot2 coverage with a runnable helper script; the shipped helpers contradict the Skill's own rules (GG-001..GG-003) and one block does not render as described (GG-005).
- reliability: 8/12 — Helpers run on raw and NA-containing airway results without warnings; create_pca_plot fails cryptically without an undocumented var_explained column and Set1 breaks above 9 groups (GG-008).
- performance_context: 6/8 — SKILL.md is compact and routes to two references; the script is small. Some restatement across SKILL, usage-guide and failure-modes.
- agent_usability: 12/16 — Clear idioms and guardrails, but the helper script's styling differs from the stated baseline so an agent gets two inconsistent house styles (GG-003).
- human_usability: 6/8 — Readable; usage-guide tips include an inert axis-line tip and a nonexistent 'panel.grid.off' term (GG-007).
- security: 11/12 — No credentials, network or destructive operations; plain local ggsave writes.
- maintainability: 9/12 — Single-purpose helpers; no tests, no seed handling in the jitter (GG-008).
- agent_specific: 15/20 — Trigger description precise, progressive disclosure to two references and a script; failure-modes.md carries claims that do not reproduce (GG-006).

## Detailed outputs

### Input 1 — Canonical: create_volcano on real airway DESeq2 results (19,772 genes, 1,534 NA padj)

**Status:** COMPLETED — Runs without warnings; class counts and top-10 labels correct; the dashed horizontal line is not the colour boundary and labels collide (GG-001, GG-004).  
**Scores:** Basic 31/40 | Specialized 42/60 | Total 73/100

**Assertions:**

- PASS — Volcano colour classes equal an independent classification (541 Up / 497 Down / 18,734 NS) (Exact match on raw results including NA padj.)
- PASS — The ten labelled genes are the ten smallest padj (setequal with order(padj)[1:10].)
- FAIL — The horizontal dashed line marks the boundary that colours the points (Line at -log10(0.05)=1.301 on raw p; smallest coloured point is 1.956; 4,692 grey points (232 with |LFC|>1) sit above the line.)
- FAIL — Rendered labels are legible and non-overlapping at the shipped max.overlaps = 20 (Opened volcano_raw.png: ENSG00000120129 overlaps ENSG00000101347.)

### Input 2 — Variant A: create_boxplot and create_pca_plot on synthetic groups and prcomp(mtcars)

**Status:** COMPLETED — Medians, jitter point count and PCA variance labels are right; palettes depart from the Skill's baseline and jitter is unseeded (GG-003, GG-008).  
**Scores:** Basic 33/40 | Specialized 43/60 | Total 76/100

**Assertions:**

- PASS — Boxplot medians equal the raw per-group medians and 60 jitter points are drawn (all.equal on ggplot_build data.)
- PASS — PCA axis labels carry the prcomp variance (PC1 57.6 %, PC2 26.5 %) (String equality with independent recomputation.)
- FAIL — Helper palettes follow the Skill's CVD-safe Okabe-Ito baseline (Brewer Set2 and Set1 (red/green) and an NPG pair; none of the Okabe-Ito pair appears.)
- FAIL — create_pca_plot works for 12 groups and reports a clear error for a missing variance column (Set1 warns 'n too large' and returns fewer colours; missing var_explained gives 'non-numeric argument to mathematical function'.)

### Input 3 — Edge: save_publication_figure and SKILL.md export blocks, fonts inspected with pdffonts

**Status:** COMPLETED — PNG is 2100 x 1500 at 7 x 5 in; the helper PDF is not cairo_pdf and embeds nothing, contradicting the Skill; the documented snippets embed TrueType.  
**Scores:** Basic 28/40 | Specialized 38/60 | Total 66/100

**Assertions:**

- PASS — The SKILL.md cairo_pdf snippet embeds TrueType fonts (pdffonts: ArialMT TrueType, emb yes.)
- PASS — Default ggsave PDF leaves fonts unembedded (rule verified) (pdffonts: Helvetica Type 1, emb no.)
- FAIL — save_publication_figure follows the Skill's cairo_pdf and mm doctrine (pub_fig.pdf: Helvetica and Symbol Type 1, emb no; width in inches.)
- PASS — 89 mm x 300 dpi PNG is 1051 x 827 px (1051 x 826 (rounding), TIFF LZW written.)

### Input 4 — Variant B: Run SKILL.md blocks: Grammar in Layers, tidy eval, ggtext, rasterise, theme_pub, reference geoms

**Status:** COMPLETED — All blocks build; the Grammar block renders with inert colour, fractional 10^n ticks and a title that duplicates the transform (GG-005).  
**Scores:** Basic 31/40 | Specialized 42/60 | Total 73/100

**Assertions:**

- PASS — Tidy-eval blocks map PC1 and PC2 with .data[[ ]] and {{ }} (Layer data equals input columns.)
- PASS — ggtext label block renders a true minus sign with subscripts (Opened ggtext.png; codepoint 8722 (U+2212).)
- PASS — rasterise() keeps vector axes and shrinks a 50,000-point PDF (105,761 B versus 1,845,026 B all-vector.)
- FAIL — Grammar in Layers block renders as its comments describe (Opened grammar_block.png: scale_color_manual has no colour mapping; ticks read 10^0.477 and 10^1.48; y title 'Expression (log10)' beside 10^n ticks.)

### Input 5 — Stress: create_multi_panel 3- and 4-panel figures with real volcano, on ggplot2 4.0.3 and 3.5.2

**Status:** COMPLETED — Layouts and tags correct on both versions; the volcano labels collapse into an unreadable stack and the theme border is lost under the patchwork `&` operator.  
**Scores:** Basic 30/40 | Specialized 41/60 | Total 71/100

**Assertions:**

- PASS — 3- and 4-panel figures carry tags A-C and A-D and build on both ggplot2 versions (Opened multi3.png, multi4.png (4.0.3) and multi3.png (3.5.2).)
- FAIL — Panels keep the theme_publication border used in the standalone plots (Multi-panel panels have no border; standalone p3 has one.)
- FAIL — Volcano labels remain legible in the multi-panel figure (ENSG labels overprint each other in panel A.)
- PASS — Results agree between ggplot2 4.0.3 and 3.5.2 (Identical counts, labels, and failures on both.)

## Key strengths

- Helpers computed volcano classes, labels and PCA variance exactly on 19,772 real airway genes.
- Documented export idioms were verified: cairo_pdf embeds TrueType, default pdf() does not, rasterise() shrinks a 50,000-point PDF 17-fold.
- Skill runs identically on ggplot2 3.5.2 and 4.0.3 and states the 4.x S7 caveat.

## Recommendations

- **[P1] GG-001 Volcano threshold line is drawn on the wrong quantity** (inputs [1]): create_volcano plots -log10(raw pvalue) but draws the horizontal line at -log10(fdr_threshold) while colouring by padj; 4,692 grey points (232 with |LFC|>1) lie above the line and coloured points start at 1.956. The y label renders '− Log10 P − value' with stray spacing. Fix: Remove the hline or place it at the smallest -log10(p) among padj < fdr genes; label with expression(-log[10](italic(p))).
- **[P1] GG-002 save_publication_figure violates the Skill's cairo_pdf and mm rule** (inputs [3]): The helper saves with the default pdf() device in inches; pdffonts shows Helvetica and Symbol Type 1 unembedded. Fix: Pass device = cairo_pdf and units = 'mm' (journal widths 89/183) in the PDF save.
- **[P1] GG-003 Example theme, palettes and multi-panel theme disagree with the SKILL baseline** (inputs [2, 5]): theme_publication is theme_bw with a panel border and an NPG pair; boxplot uses Brewer Set2 and PCA Set1 (red/green, 9-colour cap), while SKILL.md prescribes theme_classic and Okabe-Ito. create_multi_panel's `& theme_publication()` removes the border. Fix: Rebase helpers on the SKILL theme_pub and Okabe-Ito palette; apply the theme to panels with `& theme(...)` or before composition; drop or document the border.
- **[P1] GG-004 Volcano labels overlap at max.overlaps = 20** (inputs [1, 5]): Rendered labels collide in the standalone volcano and form an illegible stack in multi-panel figures; the Skill's guardrail says max.overlaps = Inf. Fix: Use max.overlaps = Inf with a seed, min.segment.length, nudges or gene symbols; open the rendered label panel.
- **[P2] GG-005 Grammar in Layers block does not render as written** (inputs [4]): scale_color_manual is inert (no colour mapping), label_log() on free log y gives 10^0.477 / 10^1.48 ticks, and the y title 'Expression (log10)' duplicates the transform. Fix: Map colour = condition, use breaks_log() or plain labels, retitle 'Expression'.
- **[P2] GG-006 Failure-mode claims that do not reproduce** (inputs [4]): aes(color='red') renders #F8766D salmon, not blue; ggrepel's 'N > 10 labels' trigger is wrong (60 labels draw alike at default and Inf; the cap is per-label overlap count) and the Skill states the default 'silently drops labels'. Fix: Correct the colour statement and describe the real overlap-count trigger; tell the agent to count drawn labels.
- **[P2] GG-007 Usage-guide tips are inert or malformed** (inputs [4]): 'Remove top/right axis lines ... theme(axis.line = element_line())' does nothing (theme_classic has no top/right lines); 'panel.grid.off' is not a ggplot2 term; panel.grid = element_blank() is redundant on theme_classic; {{ x }} with a string silently maps a constant. Fix: Delete or correct the tips; warn that {{ }} needs bare names.
- **[P2] GG-008 Helper reproducibility and input contract** (inputs [2]): create_boxplot jitter is unseeded (differs between builds); create_pca_plot needs an undocumented var_explained column and fails with a cryptic error; Set1 warns above 9 groups. Fix: Use position_jitter(seed=); document or check pca_df$var_explained; choose a palette that scales.

## Ordered finding ledger

Audited identity: `34a174ab026364c4b2884a4465ee5bd6b13eb0d80609c9f0ce729ac0746f159a`

| Order | ID | Priority | State | Evidence inputs | Required disposition |
|---:|---|---|---|---|---|
| 1 | GG-001 | P1 | open | [1] | Volcano threshold line is drawn on the wrong quantity. Remove the hline or place it at the smallest -log10(p) among padj < fdr genes; label with expression(-log[10](italic(p))). |
| 2 | GG-002 | P1 | open | [3] | save_publication_figure violates the Skill's cairo_pdf and mm rule. Pass device = cairo_pdf and units = 'mm' (journal widths 89/183) in the PDF save. |
| 3 | GG-003 | P1 | open | [2, 5] | Example theme, palettes and multi-panel theme disagree with the SKILL baseline. Rebase helpers on the SKILL theme_pub and Okabe-Ito palette; apply the theme to panels with `& theme(...)` or before composition; drop or document the border. |
| 4 | GG-004 | P1 | open | [1, 5] | Volcano labels overlap at max.overlaps = 20. Use max.overlaps = Inf with a seed, min.segment.length, nudges or gene symbols; open the rendered label panel. |
| 5 | GG-005 | P2 | open | [4] | Grammar in Layers block does not render as written. Map colour = condition, use breaks_log() or plain labels, retitle 'Expression'. |
| 6 | GG-006 | P2 | open | [4] | Failure-mode claims that do not reproduce. Correct the colour statement and describe the real overlap-count trigger; tell the agent to count drawn labels. |
| 7 | GG-007 | P2 | open | [4] | Usage-guide tips are inert or malformed. Delete or correct the tips; warn that {{ }} needs bare names. |
| 8 | GG-008 | P2 | open | [2] | Helper reproducibility and input contract. Use position_jitter(seed=); document or check pca_df$var_explained; choose a palette that scales. |

No audit-local repair was made; no Skill bytes changed.
