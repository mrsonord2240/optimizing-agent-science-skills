# bio-data-visualization-ggplot2-fundamentals fix pass - 2026-10-03

The helper drew the volcano FDR line on a raw-p axis, saved PDFs with the default `pdf()` device (fonts unembedded, against the Skill's own rule), and used a theme and palettes that disagreed with the SKILL baseline. It now plots `-log10(padj)`, saves with `cairo_pdf` in mm, and uses one Okabe-Ito palette and the baseline theme. Volcano labels overlapped in the shipped multi-panel example; `create_volcano` now labels 10 genes for short symbols and 3 for long IDs, and the Skill states the measured zero-overlap envelope with width and height and tells the agent to open the figure. Version drift (`geom_point(rasterize=)`, `trans=`) was removed, jitter is seeded, a fraction-valued `var_explained` warns, and the silent ggrepel label drop is described correctly. Later text-only passes completed the install line and reduced the frontmatter description to its trigger.

- Final candidate audit: `audits/skills/bio-data-visualization-ggplot2-fundamentals/candidate@9d1247b0d8cd-delta-desc-20261003`
- Result: **90/100, Production Ready**; open P2 GG-010 (`create_volcano` errors when a top-ranked label is NA).
- Candidate identity: `9d1247b0d8cd48c336a6e7ca866603cc3499b667e759af8f866583d076f0507b`.

The provider binding record is the canonical proof that the committed shelf bytes match this independently audited candidate.
