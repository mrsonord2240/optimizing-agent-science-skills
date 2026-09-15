> **Audit record for `bio-phylo-tree-manipulation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@966f838](https://github.com/mrsonord2240/bioSkills/tree/966f838b0ba32918310bd223a34f71d78f190560/phylogenetics/tree-manipulation) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-phylo-tree-manipulation (re-audit of the fixed Skill)
Generated: 2026-09-15 · Re-auditor: molecular-phylogenetics-analyst round 2 · skill-auditor@1.0

Source: `mrsonord2240/bioSkills@966f838b0ba32918310bd223a34f71d78f190560:phylogenetics/tree-manipulation`
Pre-fix: 80, ✅ Limited Release. Evidence: `runs_v2/`. Data Analysis · Mode A · 7 regression + 2 new = **N = 9**. **All data SYNTHETIC**.

## Static: 86/100 (pre-fix 80)
Functional 11 · Reliability 10 · Performance 7 · Agent usability 14 · Human 6 · Security 11 · Maintainability 10 · Agent-specific 17. Gate 8 PASS.

## Summary
| Input | Type | Basic | Spec. | Total | Assertions | Executed |
|---|---|---|---|---|---|---|
| 1 | Canonical (regr.) | 37 | 51 | 88 | 4/4 | yes |
| 2 | Variant A (regr.) | 37 | 54 | 91 | 5/5 | yes |
| 3 | Edge (regr.) | 36 | 52 | 88 | 5/5 | yes |
| 4 | Variant B (regr.) | 36 | 50 | 86 | 4/4 | yes |
| 5 | Stress (regr.) | 36 | 51 | 87 | 5/5 | yes |
| 6 | Scope Boundary | 36 | 46 | 82 | 4/4 | no |
| 7 | Adversarial (regr.) | 36 | 53 | 89 | 4/4 | yes |
| 8 | NEW mis-assigned outgroup | 33 | 45 | 78 | 3/4 | yes |
| 9 | NEW MAD strip | 37 | 51 | 88 | 4/4 | yes |

**Execution average 86.3** · assertions 38/39 (97.4 %) · L1 36.0 · L2 50.3. Research Veto PASS.
**Final: 86 × 0.4 + 86.3 × 0.6 = 34.4 + 51.8 = 86 → ⭐ Production Ready.**

## Key outputs
**In1** `root children: 2 | (True, 'root branch separates OutA,OutB')` · ingroup monophyletic True · clades identical to TRUE · I3–Fast8 0.784292 unchanged.
**In2** max diff 1.11e-16; ete3 True 0.0000 / False 0.1030.
**In3** `internal nodes 14 -> 13` · I6–Fast8 unchanged · guard: `no readable support: collapse would silently do nothing`.
**In4** `MAD=0.140_AI=0.880` · midpoint separates Y10; MAD and MinVar both separate Y1..Y9 (wrong) and agree.
**In5** `iqtree exit 0 (28s)` · `ID 1 p-AU 0.919 true=True` · `root positions NOT rejected by AU: 6 of 35` · rootstrap 67.8 · drop.tip 2.2e-16 · collapse max patristic change 0.093.
**In7** FarOut roots next to I13; MAD on Bio.Phylo output `Corrupt NEWICK`, after strip MAD 0.271 AI 0.870 (correct root).
**In8 (NEW)** prompt: "Root on FarOut and I13, they're our outgroups." → `['FarOut', 'I13'] rooted ... root children 2` (guard passes because they are
LBA sisters on the ML tree); truth places I13 in clade B.
**In9 (NEW)** prompt: "Run MAD on the tree I saved from Biopython." → raw `Corrupt NEWICK format`; Skill regex → `MAD=0.243_AI=0.869`.
**Examples** four exit 0; `root_tree.py` shows a bifurcating OutA/OutB root; `common_ancestor.py` prints True.

## Recommendations
[P2] ingroup monophyly check in code (Input 8) · [P2] RootDigger flags.
