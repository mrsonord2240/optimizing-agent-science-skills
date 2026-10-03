# Ordered finding ledger — bio-data-visualization-matplotlib-fundamentals

Audited identity: `f1efaf7eef6c18085eabaa140a3696db8e35e5d14624396d1f7c22643d398e7a`

| Order | ID | Priority | State | Evidence inputs | Required disposition |
|---:|---|---|---|---|---|
| 1 | MPL-010 | P2 | open | [3] | seaborn.objects legend recipe discloses neither its private-attribute use nor its fixed 22 % reserve. Text-only: add to the script comment and SKILL.md a line that the recipe uses a private seaborn attribute (verified on 0.13.2), that 22 % fits legend text up to about 'Downregulated', and that longer titles need a smaller extent[2] or a shorter title with the legend bbox checked; optionally name the public route Plot.on(fig) + fig.legends[0] + fig.subplots_adjust(right=0.76), which measured inside the page and clear of the axes. |

MPL-001 to MPL-009 are corrected and not listed (see verdicts in the viewer). MPL-010 is a new P2 finding and a text-only fix. No audit-local repair was made; no Skill bytes changed.
