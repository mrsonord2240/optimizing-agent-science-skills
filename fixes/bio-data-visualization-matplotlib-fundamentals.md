# bio-data-visualization-matplotlib-fundamentals fix pass - 2026-10-03

`savefig.bbox='tight'` produced 92 mm pages for 89 mm figures, and a list palette bound colours by data order, so Up and Down swapped colours on real data. Tight bounding boxes were removed (pages now measure exactly their stated sizes) and the palette is a dict with `hue_order`. `boxplot(labels=)`, which raises on matplotlib 3.11, became `tick_labels=`; a non-existent `fig.set_rasterization_zorder` became the Axes method; SVG text is kept as text; the Tick frequency recipe and the `tight_layout` failure-mode entry now state only behaviour that runs. The seaborn.objects example keeps its legend inside the exact page, and the Skill discloses that this uses a private seaborn attribute and a fixed page reserve. A later text-only pass reduced the frontmatter description to its trigger.

- Final candidate audit: `audits/skills/bio-data-visualization-matplotlib-fundamentals/candidate@f5acfdfb5250-delta-desc-20261003`
- Result: **90/100, Production Ready**; open P2 MPL-011 (the public legend route omits three margin settings).
- Candidate identity: `f5acfdfb52509e5422c25f3dec2481ef4f182e5c0730398f2bd5bcd2d7fb2a90`.

The provider binding record is the canonical proof that the committed shelf bytes match this independently audited candidate.
