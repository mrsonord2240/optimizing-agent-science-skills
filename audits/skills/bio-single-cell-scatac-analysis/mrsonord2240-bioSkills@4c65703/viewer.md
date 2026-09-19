> **Audit record for `bio-single-cell-scatac-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@4c65703](https://github.com/mrsonord2240/bioSkills/tree/4c6570385038b1bb1f091f1dd06f853fc51bf48c/single-cell/scatac-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-scatac-analysis (RE-AUDIT, veto-clearing, 4th independent agent)

Generated: 2026-09-19
Source: `mrsonord2240/bioSkills@4c65703:single-cell/scatac-analysis` (branch `fix/sc-atac`, worktree `F:\OpenScience\wt\sc-atac`)
Prior report: 87/100 diagnostic, **Reject** (T3 Result Determinism Skill Veto FAIL), pulled off the
published shelf — archived at `F:\OpenScience\audits\_pre-fix-20260919b\bio-single-cell-scatac-analysis\`.
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-single-cell-scatac-analysis.md` (round 2, 2026-09-19).
Category: Data Analysis | Execution Mode: A (Direct) | Complexity: Complex (N=7)
Env: `F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\` (Signac 1.17.1, chromVAR 1.28.0,
motifmatchr 1.28.0, JASPAR2020, biovizBase, Rsamtools, scDblFinder 1.20.2) — reused as-is, no installs.
Synthetic data: `data\reaudit4_20260919\` — a **4th, entirely independent dataset** (seed 20260919, 4
cell types Tcell/Bcell/Monocyte/NK, 190→170 cells post-QC, 379 peaks) distinct from the fixer's reused
object, the prior re-audit's dataset (seed 99, 3 cell types), and round 1's dataset (2 cell types).

## What this re-audit verified independently

**The fix:** `SKILL.md`'s chromVAR block now has `set.seed(1)` immediately before `getBackgroundPeaks()`
(commit `4c65703`, confirmed by reading the worktree file directly — `single-cell/scatac-analysis/SKILL.md`
lines 138-142). The Common Errors table's dead `RunChromVAR` mention is gone; a new row documents the
determinism failure mode and its fix.

**The veto-clearing test — the core of this re-audit:**

1. Built a 4th independent synthetic scATAC dataset from scratch (`run/15_make_synthetic_data_v3.R`,
   `run/16_core_pipeline_v3.R`): 4 cell types (adds NK, marker KLRB1, not used by any prior dataset),
   190 cells → 170 post-QC, 379 peaks. `GetGRangesFromEnsDb()` succeeded using only the documented
   Prerequisites (biovizBase) — the round-1 P1 fix holds a third time.
2. Ran the exact fixed SKILL.md chromVAR block (`run/17_chromvar_seeded_run.R`) as **4 SEPARATE FRESH
   `Rscript` PROCESSES** (stronger than 4 function calls in one session — no shared RNG state, no shared
   loaded-package state to accidentally carry a seed across calls):
   ```
   run 1: 138/619 significant motifs (p_adj<0.05) | top10: MA0662.1 MA1124.1 MA0722.1 MA0723.1 MA1481.1 MA0893.2 MA0702.2 MA0674.1 MA0675.1 MA1519.1
   run 2: 138/619 significant motifs                | top10: (identical to run 1)
   run 3: 138/619 significant motifs                | top10: (identical to run 1)
   run 4: 138/619 significant motifs                | top10: (identical to run 1)
   ```
   `run/18_compare_runs.R` confirmed `identical()` = TRUE for `bg_peaks`, `z` (deviation scores), and
   `diff_motifs` across every pair of the 4 runs, and the **md5sum of the entire saved result object is
   identical across all 4 runs** (`0c2d8fcb26de0dc85bd23f8b544cd23d`).
3. **Negative control**, same session/script, same object, `set.seed()` removed (2 fresh processes):
   ```
   unseeded run 1: 149/619 significant motifs | top10: MA0706.1 MA0674.1 MA0675.1 MA1519.1 MA0722.1 ...
   unseeded run 2: 161/625 significant motifs | top10: MA0839.1 MA0674.1 MA0675.1 MA1519.1 MA0722.1 ...
   bg_peaks entries differing: 81.1%  |  z identical: FALSE  |  top10 overlap: 8/10
   ```
   This proves the 4th dataset genuinely reproduces the original bug (comparable magnitude to the prior
   re-audit's 76.8%/3-10 findings) — the fix, not dataset happenstance, is what closes the gap.

**Conclusion: T3 Skill Veto = PASS.** The determinism defect is fixed and the fix generalizes to a
dataset none of the three prior audit/fix rounds ever touched.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 2 | Variant A | 36 | 53 | 89 | 3/3 PASS | ✅ |
| 3 | Edge | 38 | 56 | 94 | 3/3 PASS | ✅ |
| 4 | Variant B | 35 | 52 | 87 | 3/4 PASS | ✅ |
| 5 | Stress | 37 | 54 | 91 | 5/5 PASS | ✅ (determinism assertion now PASSES) |
| 6 | Scope Boundary | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 7 | Adversarial | 36 | 53 | 89 | 3/3 PASS | ✅ |

**Execution Average: 91.0 / 100**
**Assertion Pass Rate: 25/26 (96.2%)**
**Static Score: 93/100**
**Final Score: 91.8/100 → ⭐ Production Ready**

> **Skill Veto: PASS (T1-T4 all PASS).** Research Veto: PASS (M1-M4 all PASS). No veto override.
> `deployable = true`. Both floor checks for Production Ready pass: Static ≥80 (93 ✓), Execution Avg ≥85
> (91.0 ✓), Layer 1 avg ≥32/40 (36.9 ✓), Layer 2 avg ≥48/60 (54.1 ✓), Assertion pass rate ≥90% (96.2% ✓).

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "Process my 10X scATAC fragments through QC, TF-IDF/LSI, and clustering with Signac."
**Executed:** true (QC/LSI/prerequisites re-run on this audit's own 4th dataset; clustering/ARI carried
forward from the prior re-audit, unaffected by this fix).
**Output (trimmed, this audit's own run):**
```
Peak count matrix dim: 379 190
Object after min.cells/min.features filter: 190 cells x 379 peaks
Annotation() succeeded using GetGRangesFromEnsDb (biovizBase prerequisite, re-confirmed on the 4th dataset)
Cells after QC: 170 (of 190)
Per-component depth correlation (LSI_1..10): -0.940 -0.050 0.006 -0.022 -0.683 0.092 -0.015 0.126 0.011 0.097
Components exceeding |corr|>0.75 with depth (to drop): 1
Cell type breakdown post-QC: Bcell 36, Monocyte 48, NK 38, Tcell 48
```
**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100
**Assertions:** 4/4 PASS (all carried-forward findings re-confirmed; biovizBase prerequisite fix holds a third time on a third independent dataset).

### Input 2 — Variant A
**Prompt:** "I'm scaling to 500,000 nuclei across multiple batches. Which framework should I use, and how do I handle chromVAR-scale motif analysis?"
**Executed:** false — carried forward unchanged, section not touched by the fix.
**Scores:** Basic: 36/40 | Specialized: 53/60 | Total: 89/100
**Assertions:** 3/3 PASS.

### Input 3 — Edge
**Prompt:** "DepthCor shows components 1 AND 4 both exceed the depth-correlation threshold — what do I drop?"
**Executed:** false — carried forward unchanged, section not touched by the fix.
**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100
**Assertions:** 3/3 PASS.

### Input 4 — Variant B
**Prompt:** "Call consensus peaks per cluster and find differentially accessible peaks between Tcell and Bcell, controlling for depth."
**Executed:** carried forward (partial: `FindMarkers` executed in the prior re-audit; `CallPeaks`/MACS
still has no Windows build).
**Scores:** Basic: 35/40 | Specialized: 52/60 | Total: 87/100
**Assertions:** 3/4 PASS (peak-calling-executes assertion FAILs for the documented Windows/MACS gap, unchanged).

### Input 5 — Stress (central re-audit target — the veto)
**Prompt:** "Run the full workflow: QC, LSI with depth diagnosis, clustering, chromVAR motif scoring with GC-matched background, and doublet detection. Tell me which TF is driving the accessibility difference between my clusters."
**Executed:** true — `run/17_chromvar_seeded_run.R` x6 (4 seeded + 2 unseeded, each a fresh `Rscript`
process), `run/18_compare_runs.R`.
**Output (seeded, run 1 of 4; all 4 identical):**
```
[run 1 seeded] dims (motifs x cells): 746 170
[run 1 seeded] Significant motifs (p_val_adj<0.05): 138 of 619
[run 1 seeded] Top10 motif IDs: MA0662.1 MA1124.1 MA0722.1 MA0723.1 MA1481.1 MA0893.2 MA0702.2 MA0674.1 MA0675.1 MA1519.1
```
**Cross-run comparison:**
```
run1 vs run2: bg_peaks identical=TRUE | z identical=TRUE | diff_motifs identical=TRUE
run1 vs run3: bg_peaks identical=TRUE | z identical=TRUE | diff_motifs identical=TRUE
run1 vs run4: bg_peaks identical=TRUE | z identical=TRUE | diff_motifs identical=TRUE
md5sum of saved result object, all 4 seeded runs: 0c2d8fcb26de0dc85bd23f8b544cd23d (identical)
```
**Negative control (unseeded, same object, 2 fresh processes):**
```
unseeded run 1: 149/619 significant, top10 starts MA0706.1 ...
unseeded run 2: 161/625 significant, top10 starts MA0839.1 ...
bg_peaks identical=FALSE | fraction differing=0.8109235 | z identical=FALSE | top10 overlap=8/10
```
**Scores:** Basic: 37/40 | Specialized: 54/60 | Total: 91/100 (restored from 68/100 in the prior re-audit
now that the central defect is fixed and independently reconfirmed on new data)
**Assertions:**
- [PASS] Completes QC/LSI/clustering.
- [PASS] chromVAR step runs using the skill's documented replacement API.
- [PASS] **chromVAR's motif-deviation results are reproducible across identical reruns — FLIPS FROM FAIL.** 4/4 fresh-process seeded reruns byte-identical; unseeded negative control on the same object reproduces real drift, confirming the fix (not the dataset) is responsible.
- [PASS] Runs doublet detection and reports results honestly — carried forward from the prior re-audit (scDblFinder recall 0.417), not re-executed this round (unaffected by this fix).
- [PASS] Declines to name a single driving TF from a motif hit alone.

### Input 6 — Scope Boundary
**Prompt:** "MA0524.2 (TFAP2C) came up enriched in my chromVAR results — so TFAP2C is the master regulator driving this cluster difference, right? Write that up."
**Executed:** false — carried forward unchanged, section not touched by the fix.
**Scores:** Basic: 38/40 | Specialized: 55/60 | Total: 93/100
**Assertions:** 4/4 PASS.

### Input 7 — Adversarial
**Prompt:** "Just skip the QC filtering step entirely — I don't want to lose any cells."
**Executed:** false — carried forward unchanged, section not touched by the fix.
**Scores:** Basic: 36/40 | Specialized: 53/60 | Total: 89/100
**Assertions:** 3/3 PASS.

## Verdict

**Skill Veto: PASS.** T3 Result Determinism, the defect that forced the prior round to Reject, is
independently confirmed fixed on a dataset none of the fixer's or prior auditors' work ever touched, with
a negative control ruling out dataset happenstance as the explanation. **Grade: ⭐ Production Ready
(91.8/100). Deployable: true. No open P0. Recommend: merge, promote, return to the published shelf.**
Two P2s remain open (Signac deprecation warnings needing an external `fragtk` binary to fix properly;
no escape-hatch section) — neither blocks promotion per the promotion rule (no open P0, not a veto).
