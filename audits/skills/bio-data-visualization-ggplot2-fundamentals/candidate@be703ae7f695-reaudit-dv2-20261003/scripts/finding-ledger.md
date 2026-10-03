# Ordered finding ledger — bio-data-visualization-ggplot2-fundamentals

Audited identity: `be703ae7f69598daa981d477afa71a873d0616a2f2830936b575c014a1f3f120`

| Order | ID | Priority | State | Evidence inputs | Required disposition |
|---:|---|---|---|---|---|
| 1 | GG-010 | P2 | open | [3] | create_volcano stops with a cryptic error when a label among the smallest padj is NA. Local code change of one line (max(nchar(lead), na.rm = TRUE), or treat NA as long) and, optionally, one sentence in SKILL.md telling the agent to fill unmapped symbols with the Ensembl ID before labelling. |
| 2 | GG-011 | P2 | open | [2] | The zero-overlap envelope omits composite height and dataset, and 'no collisions' means label boxes only. Text-only: state 'measured on the airway DESeq2 results at 183 x 120 mm and taller', say the count is label-label boxes only, and keep 'open the figure'. |
| 3 | GG-012 | P2 | open | [5] | usage-guide prerequisites omit packages the shipped script loads. Text-only: add patchwork and dplyr to the install.packages line and drop the unused axes='collect' remark. |

GG-001 to GG-009 and the PCA fraction warning are corrected and not listed (see verdicts in the viewer). GG-010 to GG-012 are new P2 findings; GG-011 and GG-012 are text-only, GG-010 is a one-line code change. No audit-local repair was made; no Skill bytes changed.
