> **Audit record for `bio-phylo-tree-visualization`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@966f838](https://github.com/mrsonord2240/bioSkills/tree/966f838b0ba32918310bd223a34f71d78f190560/phylogenetics/tree-visualization) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-phylo-tree-visualization (re-audit of the fixed Skill)
Generated: 2026-09-15 · Re-auditor: molecular-phylogenetics-analyst round 2 · skill-auditor@1.0

Source: `mrsonord2240/bioSkills@966f838b0ba32918310bd223a34f71d78f190560:phylogenetics/tree-visualization`
Pre-fix: 78 → ⚠️ Beta Only. Evidence: `runs_v2/`. Data Analysis · Mode A · 7 regression + 2 new = **N = 9**. **All data SYNTHETIC**.

## Static: 84/100 (pre-fix 79)
Functional 10 · Reliability 10 · Performance 7 · Agent usability 13 · Human 6 · Security 11 · Maintainability 9 · Agent-specific 18. Gate 8 PASS.

## Summary
| Input | Type | Basic | Spec. | Total | Assertions | Executed |
|---|---|---|---|---|---|---|
| 1 | Canonical (regr.) | 36 | 52 | 88 | 5/5 | yes |
| 2 | Variant A (regr.) | 30 | 46 | 76 | 3/5 | yes |
| 3 | Edge (regr.) | 33 | 47 | 80 | 4/5 | yes |
| 4 | Variant B (regr.) | 36 | 52 | 88 | 5/5 | yes |
| 5 | Stress (regr.) | 30 | 46 | 76 | 3/5 | yes |
| 6 | Scope Boundary (regr.) | 36 | 51 | 87 | 5/5 | yes |
| 7 | Adversarial (regr.) | 34 | 47 | 81 | 3/5 | yes |
| 8 | NEW version block | 35 | 49 | 84 | 3/4 | yes |
| 9 | NEW ape edgelabel | 36 | 52 | 88 | 4/4 | yes |

**Execution average 83.1** · assertions 35/43 (81.4 %) · L1 34.0 · L2 49.1. Research Veto PASS.
**Final: 84 × 0.4 + 83.1 × 0.6 = 33.6 + 49.9 = 84 → ✅ Limited Release** (LR floors met; PR execution floor 85 not met).

## Key outputs
**In1** `support labels drawn: 13 ['100/100','88/92',...] | raw names left: []` · title `Node support: SH-aLRT (%) / UFBoot (%)` · reroot `7 of 13` moved.
**In2** `red segments drawn: 44 | MRCA tips: ['Aotus_nancymaae','Callithrix_jacchus',...,'Microcebus_murinus','Otolemur_garnettii'...]` (unrooted tree) ·
raw `99.5/100` strings still drawn.
**In3** `>~150 tips: switch to a circular layout ...` · height 40 · x ticks −2…10 · 49 adjacent overlaps at 10 pt.
**In4** `center = auto -> 4.95 Ma` · `center = height -> 0.00 Ma`.
**In5–7** auditor R scripts re-run and saved; defects unchanged from pre-fix.
**In8 (NEW)** prompt: "Will these ggtree layouts work on my R stack as your guide says?" → rectangular/circular/fan OK; slanted/equal_angle/daylight/align ERROR `is.waive`;
`gheatmap OK`; `geom_fruit fallback OK`; `ape plot.phylo(type='unrooted') OK`.
**In9 (NEW)** prompt: "Root the IQ-TREE tree in R on the strepsirrhines without moving the support values." →
`edgelabel = FALSE ... on a different split 5, not placed 1` · `edgelabel = TRUE ... 0, 0`.
**Examples** three exit 0; `labeled_tree.py`: `Support labels drawn: ['88/97', '72/90']`.

## Recommendations
[P1] root before colouring by MRCA (Input 2) · [P2] gheatmap line · [P2] ggtree rich-figure patterns.
