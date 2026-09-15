> **Audit record for `bio-phylo-tree-io`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@966f838](https://github.com/mrsonord2240/bioSkills/tree/966f838b0ba32918310bd223a34f71d78f190560/phylogenetics/tree-io) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-phylo-tree-io (re-audit of the fixed Skill)
Generated: 2026-09-15 · Re-auditor: molecular-phylogenetics-analyst round 2 · skill-auditor@1.0

Source: `mrsonord2240/bioSkills@966f838b0ba32918310bd223a34f71d78f190560:phylogenetics/tree-io`
Pre-fix: 84 → ⚠️ Beta Only (assertion floor 76.5 %). Evidence: `runs_v2/`. Data Analysis · Mode A · 7 regression + 2 new = **N = 9**. **All data SYNTHETIC**.

## Static: 86/100 (pre-fix 79)
Functional 11 · Reliability 10 · Performance 7 · Agent usability 14 · Human 6 · Security 11 · Maintainability 9 · Agent-specific 18. Gate 8 PASS.

## Summary
| Input | Type | Basic | Spec. | Total | Assertions | Executed |
|---|---|---|---|---|---|---|
| 1 | Canonical (regr.) | 37 | 54 | 91 | 5/5 | yes |
| 2 | Variant A (regr.) | 37 | 55 | 92 | 5/5 | yes |
| 3 | Edge (regr.) | 36 | 50 | 86 | 5/5 | yes |
| 4 | Variant B (regr.) | 36 | 52 | 88 | 5/5 | yes |
| 5 | Stress (regr.) | 34 | 50 | 84 | 4/5 | yes |
| 6 | Scope Boundary (regr.) | 37 | 55 | 92 | 4/4 | yes |
| 7 | Adversarial (regr.) | 37 | 53 | 90 | 5/5 | yes |
| 8 | NEW strict readers | 35 | 51 | 86 | 4/4 | yes |
| 9 | NEW encoding | 36 | 52 | 88 | 4/4 | yes |

**Execution average 88.6** · assertions 41/42 (97.6 %). Research Veto PASS.
**Final: 86 × 0.4 + 88.6 × 0.6 = 34.4 + 53.2 = 88 → ⭐ Production Ready.**

## Key outputs
**In1** `typed rows: [('ROOT', 1.0, [38.1, 48.9]), ...] n = 5` · `posterior mismatches: []` · topology.nwk starts `((((Homo_sapiens` (no [&R]) ·
`Phylo.convert Newick contains escaped '[\[&': 11` · `DendroPy posteriors readable after Phylo.convert: 0` · treeio round trip TRUE/TRUE.
**In2** `split 7 labels; joint-rule pass 6` (Bos_taurus,Sus_scrofa 94/93 weak).
**In3** sanitized join 7/7; ete3 `KeyError`/`NewickError`; ape `NA`.
**In4** `AssertionError Two string taxonomies?`; 302 post-burn-in trees; clade prob 1.0 ×7.
**In5** phyloXML→phyloxml 10 confidences/7 taxonomy/colour; nexus/newick 0 and rooted False; cdao OK; NeXML tips `d10, d6, d7`.
**In6/7** as pre-fix.
**In8 (NEW)** prompt: "Our R pipeline uses ape — will it read the plain Newick you made?" → `topology.nwk -> tips 6`; `phylo_convert.nwk -> tips 6, node.label` empty; `[&R]` prefix tolerated.
**In9 (NEW)** prompt: "My tip names have accents; read and rewrite the tree on Windows." → `preferred encoding cp1252`; path reads `CercopithÃ¨que_ascagne`;
`UTF-8 handle round trip correct: True`; path-written file `can't decode byte 0xe8`.
**Examples** `convert_formats.py`: `DendroPy-readable posteriors: before=2, after=0`; others exit 0.

## Recommendations
[P2] remove "truncates or chokes" sentence · [P2] note Bio.Phylo NeXML writer losses.
