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
