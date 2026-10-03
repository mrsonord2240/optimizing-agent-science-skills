Environment: Windows R 4.4.3 via `r.sh` (ggplot2 4.0.3) and `r-gg35.sh` (ggplot2 3.5.2); fingerprint sha256 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721 over `snapshots/lane1_versions.txt`; pdffonts 26.07.0 in WSL `dv-cli`. Input: public airway DESeq2 results (19,772 genes) and `datasets::mtcars`.

| Surface | Classification | Evidence |
|---|---|---|
| `scripts/publication_figures.R` (six helpers) | executed | `scripts/g1_example.R`, logs `logs/g1_example_gg4.log`, `logs/g1_example_gg35.log`; figures `out/ex4/`, `out/ex35/` opened |
| SKILL.md and reference snippets (grammar, tidy eval, ggtext, rasterise, export, theme_pub, geoms/scales/facets) | executed | `scripts/g2_snippets.R`, logs `logs/g2_snippets_gg*.log`; `out/snip4/` opened |
| PDF font embedding | executed | `scripts/pdffonts.sh`, `logs/pdffonts_*.log` |
| `usage-guide.md`, `references/failure-modes.md` claims | executed where testable (colour, ggrepel, axis-line tip); remainder static-only | g2 log |
