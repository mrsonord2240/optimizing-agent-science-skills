## Readiness decision

**Not candidate-ready** for the exact identity above. The numeric thresholds are met (final 85, static 84, execution average 85.4, Layer 1 average 33.2, Layer 2 average 52.2, no veto, no P0) but the assertion pass rate is 20/23 = 87 percent, below the 90 percent floor. Three new P2 findings (MPL-007, MPL-008, MPL-009), all text-only fixes, cause the three failed assertions. Route to `fix-scientific-skill` (text-only edits to chart-recipes.md, failure-modes.md and scripts/matplotlib_phd.py), then a fresh re-audit.

## Prior findings (initial audit 146857c3b9b5, Beta Only 74), each retested here

| ID | Sev | Verdict | Independent evidence (scripts/logs) |
|---|---|---|---|
| MPL-001 | P1 | resolved | all five PDFs exact mm; Saving block 89.0 x 70.0 mm; bbox tight reproduces ~92 mm only when set (r1, r3, r4) |
| MPL-002 | P1 | resolved | dict palette: 0 colour mismatches on 18,238 airway points in three row orders; legend maps equal (r3) |
| MPL-003 | P2 | resolved | ax.set_rasterization_zorder works, fig method absent; large-N 1.5 MB vs 24 KB reproduces at default savefig dpi (r4, r5) |
| MPL-004 | P2 | resolved | svg.fonttype none: 14 <text>; control 0 (r3) |
| MPL-005 | P2 | resolved | rendered text 6 and 7 pt only; pdffonts TrueType only; no tab10 (r1) |
| MPL-006 | P2 | resolved | all five SKILL.md python blocks run verbatim in three orders; Color block uses fig.colorbar (r3) |

Fixer-added inline changes retested: the 180 mm grid (180.0 mm), the `data.items()` grid snippet and missing numpy import (blocks run verbatim), and the `.theme({**sns.axes_style('ticks'), **mpl.rcParams})` line (r7: without it so.Plot draws 12/11 pt, with it 7/6 pt). The `legend=False` tradeoff is real (the legend leaves the 89 mm page for every engine) but leaves the figure uninterpretable, so it is recorded as MPL-007.

## Executed versus static-only

| Surface | Class | Evidence |
|---|---|---|
| scripts/matplotlib_phd.py (five PDFs) | executed | r1, pdffonts, figures opened |
| SKILL.md python blocks on real airway table, three row orders | executed | r3 |
| SKILL.md Saving block (pdf, png, tiff, svg, eps) | executed | r3 |
| references/chart-recipes.md (11 snippets) | executed, one failed | r4 (MPL-008) |
| references/failure-modes.md claims | executed, one failed | r4, r5, r6 (MPL-009) |
| seaborn.objects legend placement alternatives | executed | r2, figure opened |
| usage-guide.md prompts and prerequisites | static-only | prose, no runnable code |

Environment: fingerprint 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721 (Python 3.12.13, matplotlib 3.11.2, seaborn 0.13.2, numpy 2.5.3, pandas 3.0.6); pdffonts through the recorded WSL dv-cli route; Arial resolves on Windows. Input: staged real airway DESeq2 results (19,772 rows, 18,238 after dropping NA padj or pvalue).
