# Ordered finding ledger — bio-data-visualization-matplotlib-fundamentals

Audited identity: `146857c3b9b509e7fb41764055239b497b5793cf0b386f83542fdfd5c5302d78`

| Order | ID | Priority | State | Evidence inputs | Required disposition |
|---:|---|---|---|---|---|
| 1 | MPL-001 | P1 | open | [1, 3] | Shipped rcParams do not yield the documented 89/180 mm journal widths. Drop savefig.bbox='tight' (constrained layout already prevents clipping) from both the Standard Setup and script, or document the size change and assert page width. |
| 2 | MPL-002 | P1 | open | [2] | List palettes bind colours to data order, not to Up/Down/NS. Use palette={'NS':..., 'Down':..., 'Up':...} with hue_order in SKILL.md, matplotlib_phd.py and seaborn.objects scale. |
| 3 | MPL-003 | P2 | open | [5] | failure-modes.md contains a nonexistent method and an exaggerated claim. Use ax.set_rasterization_zorder(0), restate the size effect with a measured ratio, drop the vague mechanism. |
| 4 | MPL-004 | P2 | open | [3] | 'SVG for editable vector' leaves text as paths. Set svg.fonttype='none' (with a note that fonts must be installed) or reword the claim. |
| 5 | MPL-005 | P2 | open | [1] | Example styling departs from the Skill's own rules. Colour clusters with the Okabe-Ito list, use titlesize 7, and drop the redundant panel titles. |
| 6 | MPL-006 | P2 | open | [4] | OO-API Skill mixes pyplot state calls. Use ax.imshow and fig.colorbar(im, ax=ax) in SKILL.md, usage-guide and chart-recipes. |

No audit-local repair was made; no Skill bytes changed.
