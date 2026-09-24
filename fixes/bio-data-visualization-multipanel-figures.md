# Fix log: bio-data-visualization-multipanel-figures

## 2026-09-24 — backlog correction

Skill `data-visualization/multipanel-figures`, branch
`fix/data-visualization-multipanel-figures`, commit
`3749f31f1c2d406f5e948bb389eaea7379c6e71a` from staging `9807004e`.
Validated with R 4.4.3, ggplot2 4.0.3, patchwork 1.3.2, cowplot 1.2.0,
gridExtra 2.3, Python 3.12, and matplotlib 3.11.2.

| finding | priority | change | verification |
| --- | --- | --- | --- |
| `plot_annotation(theme=...)` did not style patchwork tags | P1 | Apply the 8 pt bold tag theme with patchwork's `& theme(...)` operator and position tags relative to their panels. | Exact source-contract check passes; committed R example renders with the corrected route. |
| Axis collection did nothing for the nested 2x2 recipe | P1 | Use a flat `wrap_plots(..., ncol=2)` composition and qualify collection to identical compatible coordinate scales. | Focused R verification renders `flat_collect.pdf`; source contains the flat collection contract. |
| Python changed the requested dimensions and emitted Type 3 fonts | P1 | Set `pdf.fonttype=42`, use an explicit 183 x 140 mm canvas, enable constrained layout, keep tags inside axes, and omit tight bounding boxes. | Both exact PNGs are 2161 x 1653 px at 300 dpi; PDF evidence reports 518.74 x 396.85 pt, embedded CID TrueType fonts, and no Type 3. |
| Shipped R and Python examples violated their own export rules | P1 | Rewrote both examples around the same page constants, explicit layout engines, fixed-point tags, and a single honest shared legend. | Both examples execute and create nonempty named PDF/PNG outputs; report assertions are 25/25. |
| Failure-mode explanations were false or ineffective | P1 | Corrected cowplot alignment, patchwork compatibility, ggsave units, constrained-layout defaults, tag placement, and legend-equivalence guidance from observed behavior. | Static exact-source verifier passes and the corrected runtime routes execute. |
| Label sizes and journal widths conflicted | P2 | Centralized the Nature 183 mm width, 140 mm example height, 8 pt panel tags, 7 pt body/title text, and 6 pt tick text. | R and Python source constants and measured products agree. |
| Promised gridExtra and matplotlib layout coverage was absent | P2 | Added runnable gridExtra layout-matrix, GridSpec, subfigure, subplot-mosaic, figure-level legend, and fixed-point tag patterns. | gridExtra, mosaic, and subfigure verification products are nonempty and satisfy structural assertions. |
| Version notes were incomplete | P2 | Require patchwork >= 1.3 for ggplot2 4.x and state that guide removal/collection is safe only for equivalent mappings. | Version and misleading-guide guards pass in `verify_source.py`. |

## Findings left unfixed

None. The shared Windows R cleanup issue can return after all requested outputs
are complete; the re-audit records that process-level condition explicitly and
independently checks the finished files.
