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
