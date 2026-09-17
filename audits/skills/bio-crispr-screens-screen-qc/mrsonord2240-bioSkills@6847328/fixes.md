# bio-crispr-screens-screen-qc fixes (2026-09-16)

Worktree `F:\OpenScience\wt\crispr-c`, branch `fix/r2-crispr-c`. Fixer: Claude Opus 5 (orchestrating
session). Runtime: the candidate venv (pandas 2.x, scipy, seaborn, matplotlib Agg). Verification
scripts and data: `F:\OpenScience\wt\_fixdata\qc\` — the audit's own CN test set
(`synthetic_gene_lfc_for_cn.txt` + `synthetic_copy_number.txt`, 40-gene focal amplicon) and a
5-sample count table built from the real HAP1 TKOv3 screen (`hap1_tkov3_canonical.txt`).

## Round-2 audit pass — 2026-09-16

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| CN-bias Spearman threshold misses a real focal amplicon | P1 | `cn_bias_diagnostic()` now also returns the amplified-vs-diploid mean-LFC gap with a one-sided Mann-Whitney test and a `cn_bias_present` flag that fires on either rule; the Interpretation section states both rules and points at the per-amplicon re-run | ran | On the audit's own data: rho -0.066 (rule 1 passes) but gap -0.858, p < 1e-18 -> `cn_bias_present: True`. Negative control with shuffled CN labels: gap +0.049, p 0.73 -> `False`. Same two rules as `copy-number-correction`'s `detect_cn_bias()`, fixed on the sibling branch, and the sections now cite each other |
| Shipped `examples/screen_qc.py` uses stage-blind thresholds and correlates non-replicate pairs | P1 | Rewrote it around a `stage_map` and a `condition_map`: stage-specific zero-count and Gini bands matching `stage_specific_thresholds()`, and Pearson/Spearman only within a condition | ran | On the real 5-sample table: plasmid 0.56% zeros WARN at its 0.5% limit while endpoint 1.66% PASSes at 5%; Gini 0.288 FAILs as a plasmid but the same value WARNs as day-0; only `Day0_r1 vs Day0_r2` (0.996) and `Endpoint_r1 vs Endpoint_r2` (0.776) are reported as replicate pairs. The old flat bands scored every sample against 0.2/0.3 and correlated plasmid against endpoint |
| No escape hatch for research-vs-clinical scope creep | P1 | New "When NOT to Use This Skill" section: research cell-line data only, an amplification surviving correction is not a patient biomarker, route the clinical part elsewhere | docs | Placed before the thresholds so it is read with them |
| Weak fault tolerance and error reporting | P1 | New "Input Validation" table (required columns, dtypes, all-zero sample, negative counts, duplicate sgRNA IDs and what to report for each) and a `validate_counts()` in the shipped example that raises a named error; `gini_index()` in the example gained the `np.nan` guard SKILL.md's `gini()` already had | ran | An all-zero sample is now reported and excluded rather than raising `IndexError` inside `gini_index` |
| CN-bias rho threshold inconsistent between SKILL.md (0.10) and usage-guide.md (0.05) | P2 | Both tables now label them: 0.10 pre-correction fail, 0.05 post-correction target, plus the new amplified-vs-diploid gap row | docs | |

All 5 `recommendations[]` entries (4 P1, 1 P2) fixed. Nothing left unfixed. `py_compile` clean on
`examples/screen_qc.py`, and it runs end to end (writes `screen_qc.png`).
