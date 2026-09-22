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

## 2026-09-21

Worktree `F:\OpenScience\wt\crispr-screens-screen-qc`, branch `fix/crispr-screens-screen-qc`, from staging `431aa55`.
Audit: `F:\OpenScience\audits\bio-crispr-screens-screen-qc\eval_report_bio-crispr-screens-screen-qc_result.json` (2 P2). Env `crispr-screen-analyst` (Python 3.12, pandas 3.0.5, numpy 2.5.3, scipy 1.18.1, scikit-learn 1.9.1).

Commits: `1b20045` fix, `3ccf0a8` redundancy, `7aec95b` split, `ea262e3` scripts.

### Findings

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| `validate_counts()` does not enforce the documented sgRNA-identifier index | P2 | `examples/screen_qc.py`: raises a named `ValueError` when the index is a `RangeIndex` or an integer `0..n-1` index; SKILL.md Input Validation row now says a default index means the ID column was lost | ran: the audit's `input9_validate_counts.py` (pointed at the fixed example, base table given string IDs) passes all 6 documented-failure checks; bare RangeIndex and int `0..n-1` index rejected, `sg{i}` string IDs accepted; example runs end to end on `stage5_mixed.count.txt` | The audit's own `base_table()` used a default index, so it had to be given real IDs once the check existed |
| Example `STAGE_THRESHOLDS` is a hand copy of SKILL.md's thresholds | P2 | Comment above the dict names the sources (`stage_specific_thresholds()` in `scripts/library_representation.py` / SKILL.md "Library Representation Metrics", and the "Gini Coefficient" stage table) | read against both tables; example re-run after the final edit | Chose the comment option; the example stays standalone by design |

P2 fixed 2/2.

### Redundancy pass (SKILL.md vs usage-guide.md)

| deleted passage | new home |
| --- | --- |
| usage-guide "Prerequisites" install block and required inputs | SKILL.md "Install and Inputs"; guide now names the section |
| "What the Agent Will Do" steps 1-9 | Restate SKILL.md sections; deleted |
| "What the Agent Will Do" step 10 (hit-calling method by quality grade) | SKILL.md "Interpretation Notes" |
| Tips: plasmid >=99% detection at >25 reads/guide | Interpretation Notes |
| Tips: PR-AUC as most diagnostic metric / final gate | Interpretation Notes |
| Tips: drug screens compare vs vehicle | Interpretation Notes |
| Tips: CRISPRi/a calibrate against CRISPRi sub-essentialome | Interpretation Notes |
| Tips: cancer lines always need CN correction; MOI 0.3 non-negotiable; high Pearson / low Spearman -> RRA/drugZ | Already in SKILL.md (Copy-Number failure mode, MOI decision rule, Replicate Concordance) |
| "QC Decision Reference": Day 0 Pearson with plasmid >0.9 | Interpretation Notes |
| "QC Decision Reference": other rows | Already in SKILL.md (Stage Hierarchy, Quantitative Thresholds, depth grades, MOI table) |
| SKILL.md Version Compatibility duplicate `packageVersion('MAGeCKFlute')` bullet | Merged into the R bullet |
| SKILL.md "Low Day-0 coverage from high MOI" failure-mode mechanism/fix restating the Poisson math | Points at the MOI Verification table and decision rule |

Left as is: the Stage Hierarchy table, the stage-threshold dict/tables and the Quantitative Thresholds table overlap on numbers, but each has a different job (overview, code constants, citation column); collapsing them would drop the sources.

### Split

SKILL.md 434 -> 229 lines (412 at dispatch; +22 from moving guide-only content in). Verbatim into `references/`: `essentialome-recovery.md`, `copy-number-bias.md`, `depth-and-moi.md`, `pca-and-composite-score.md`, `failure-modes.md`. Index "Reference Files" plus a new "Detail" column on the Stage Hierarchy table point at each. Every non-blank line accounted for (differences: the table rows that gained the Detail column, and the "Failure Modes" heading, now that file's H1); all python fences `ast.parse`.

### Scripts

| old location | script |
| --- | --- |
| SKILL.md "Library Representation Metrics" code block (`library_representation`, `stage_specific_thresholds`) | `scripts/library_representation.py` |
| references/copy-number-bias.md `cn_bias_diagnostic` block | `scripts/cn_bias.py` |
| references/essentialome-recovery.md `essentialome_recovery` block | `scripts/essentialome_recovery.py` |

Ran as SKILL.md invokes them, on the audit data: library table (plasmid 70712 detected, 0.532% zero, skew 4.253) agrees with the example's zero-count output; `cn_bias.py` on the synthetic amplicon gives rho -0.066, gap -0.858, 40 amplified genes, `cn_bias_present: True` (audit: -0.066 / -0.858); `essentialome_recovery.py` on HAP1 TKOv3 canonical counts gives PR-AUC 0.9977, 646 / 797 (audit: 0.9977, 646 / 797), and shuffled LFC gives 0.4495 -> NO SIGNAL. Import-and-assert run also passes. Not moved (under about 15 lines): `gini`, `replicate_concordance`, `depth_audit`, `screen_pca`, `composite_qc_score`; `gini` also has a copy in `examples/screen_qc.py`.

### Left unfixed

None.

## Final pass, Phase 1 — 2026-09-21

Same worktree/branch, tip `ea262e3` (no new commits this phase — nothing needed fixing).
Checkpoint: `F:\OpenScience\audits\_final_pass\bio-crispr-screens-screen-qc\CHECKPOINT.md`.

Independently re-verified every claim in the 2026-09-21 pass above (library representation, CN-bias
two-rule diagnostic, essentialome PR-AUC on real HAP1 TKOv3 data plus a new shuffled-LFC negative
control, the shipped end-to-end example, and the `validate_counts()` sgRNA-index fix against 7 cases
including two not in the original audit script) and ran the five short inline blocks that stayed in
SKILL.md/references/ (`gini`, `replicate_concordance`, `depth_audit`, `screen_pca`,
`composite_qc_score`) against `stage5_mixed.count.txt` — all real, non-degenerate output. Also
confirmed `library(MAGeCKFlute)` loads via the env's `r.sh` (1.99.2001). No defect found; nothing
left unfixed.
