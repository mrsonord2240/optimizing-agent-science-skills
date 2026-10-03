# Ordered finding ledger — bio-data-visualization-ggplot2-fundamentals

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
