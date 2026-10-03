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
