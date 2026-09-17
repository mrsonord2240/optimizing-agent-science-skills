# Fix log — bio-crispr-screens-hit-calling (2026-09-16)

Commit: `e22f956` on `fix/r2-crispr-a` (worktree `F:\OpenScience\wt\crispr-a`).
Verdict context: candidate `crispr-screen-analyst` scored 78 (Limited Release), needs
85 as a core Skill. Sam's scope override (2026-09-16): fix every P0/P1/P2 named for
this Skill.

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| BAGEL2 non-determinism named in scope, unaddressed | P1 | Added Reconciliation-table row + Common-Errors row citing `-s/--seed` and cross-linking `bagel-essentiality`'s Reproducibility section; added the same tip to usage-guide.md | ran | reused the fix already established in `ead41a5` (bagel-essentiality), not re-derived; independently reproduced 26.7 max BF diff / 33 flips on real HAP1 TKOv3 reruns from the audit's own data |
| 3 conflicting MAGeCK-FDR/BAGEL-BF threshold pairs (SKILL.md inline fn 0.05/5, examples/consensus_hits.py 0.1/5, Quantitative Thresholds table 0.05/6) | P1 | Unified both code paths on the table's FDR<0.05/BF>6; added a note naming the table as the single source of truth | ran | real data: both code paths now give 844 Tier-1 hits (was 844 vs 1131, a 34% swing) |
| Spearman rho prompt ignores MAGeCK neg\|score vs BAGEL2 BF sign/scale inversion | P1 | Added "Correlating MAGeCK and BAGEL2 Scores" section to SKILL.md with a worked real-data example; usage-guide.md's rho prompt now says to sign-correct first | ran | real HAP1 TKOv3, n=18,053: rho=-0.806 naive, +0.806 sign-corrected — matches audit exactly |
| Empty-consensus guidance has only one cause (screen quality); real failure mode is merging non-comparable comparisons | P1 | Added `_check_comparable()` (hypergeometric overlap-enrichment test) to `consensus_hits()` in SKILL.md and examples/consensus_hits.py; documented the alternate cause in Failure Modes + Common Errors | ran | matched MAGeCK/BAGEL2 real data: overlap p≈0 (enriched, no warning); matched data vs an unrelated real drugZ table: overlap p=1.0 (fires warning) — reproduces the audit's Input 5/7 scenario exactly |
| `second_best_lfc()` silently exempts single-guide genes (fallback reads as a pass) | P2 | Returns `NaN` + `single_guide=True` instead of the lone guide's own LFC; updated the Rule prose and two table rows | ran | direct single-guide-gene unit test: old behavior would have "passed"; new behavior flags it |
| No `references/` split for the dense 7-method tables | P2 | Left unfixed | n/a | audit itself calls this "optionally"; no sibling Skill in this fork's `crispr-screens/` folder uses a `references/` subfolder, and restructuring a Skill that's 7 points from its floor for a cosmetic reorg risked more (broken links, larger diff) than it fixed. Revisit only if a later pass standardizes `references/` across the folder. |

All three SKILL.md Python blocks (`consensus_hits`+`_check_comparable`,
`second_best_lfc`, `custom_zscore_hit_calling`) and the rewritten
`examples/consensus_hits.py` were `py_compile`d and executed against the real
HAP1 TKOv3 data copied read-only from
`F:\OpenScience\audits\bio-crispr-screens-hit-calling\run\` (MAGeCK
`mageck_hap1.gene_summary.txt`/`mageck_hap1.sgrna_summary.txt`, BAGEL2
`bayes_factor.txt`/`bayes_factor_rep2.txt`, drugZ `drugz_drug_output.txt`) via
`F:\OpenScience\audit-envs\crispr-screen-analyst`'s Python 3.12 venv
(`Scripts/python.exe`). No new packages needed — pandas/numpy/scipy already
installed there.

Needs Sam: nothing. This Skill's own defects are now all P1/P2-addressed; whether
78→85+ actually clears the candidate's core-Skill floor depends on the re-audit,
not on anything left undone here.
