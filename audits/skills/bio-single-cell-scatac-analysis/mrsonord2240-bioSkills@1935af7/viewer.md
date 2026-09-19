> **Audit record for `bio-single-cell-scatac-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@1935af7](https://github.com/mrsonord2240/bioSkills/tree/1935af7c20305a64959a56af16fb50f2d3abc3a7/single-cell/scatac-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-scatac-analysis (RE-AUDIT)

Generated: 2026-09-19
Source: `mrsonord2240/bioSkills@1935af7c20305a64959a56af16fb50f2d3abc3a7:single-cell/scatac-analysis`
(branch `fix/sc-atac`, worktree `F:\OpenScience\wt\sc-atac`)
Prior report: 89/100, Limited Release, deployable, 2 open P1s — archived at
`F:\OpenScience\audits\_pre-fix-20260919\bio-single-cell-scatac-analysis\`
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-single-cell-scatac-analysis.md`
Category: Data Analysis | Execution Mode: A (Direct) | Complexity: Complex (N=7)
Env: `F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\` (Signac 1.17.1, chromVAR 1.28.0,
motifmatchr 1.28.0, JASPAR2020, biovizBase, Rsamtools, scDblFinder 1.20.2) — reused as-is, no installs.
Synthetic data: `data\reaudit_v2_20260919\` — an entirely independent dataset from the fixer's and the
prior audit's (seed 99, 3 cell types Tcell/Bcell/Monocyte, 180 cells -> 160 post-QC, 284 peaks,
different depth-multiplier ratio), so this re-audit is not just re-running the fixer's own check.

## What this re-audit verified independently

1. **`RunChromVAR` is genuinely absent from Signac 1.17.1's namespace.** `getNamespaceExports('Signac')`
   has zero entries matching "chromvar" (case-insensitive); a direct reference throws
   `object 'RunChromVAR' not found`. Confirms the fix's premise, independent of the fixer's own check.
2. **The replacement chromVAR block (`addGCBias`/`matchMotifs`/`getBackgroundPeaks`/`computeDeviations`)
   runs end-to-end** on this audit's own fresh object: a real 746-motif x 160-cell deviation matrix.
3. **`biovizBase` is genuinely required and now correctly documented.** `GetGRangesFromEnsDb()`'s source
   contains an explicit `if (!requireNamespace("biovizBase", quietly = TRUE)) stop(...)` guard.
4. **The Rsamtools omission is correct, and for a more precise reason than the fix log states.**
   Signac's own `DESCRIPTION` lists `Rsamtools` under **Imports** (auto-installed by
   `install.packages('Signac')`) and `biovizBase` only under **Suggests** (never auto-installed). That
   is the actual mechanism — not just "the auditor's own script happened to use it" — and it is why
   biovizBase needed a Prerequisites line and Rsamtools does not.
5. **NEW finding, not caught by the prior audit or the fix: chromVAR's replacement block is not
   reproducible.** `getBackgroundPeaks()` is unseeded — 76.8% of its background-peak assignment matrix
   differs between two calls on the identical input, confirmed fully fixed by matching `set.seed()`
   calls. Running the SKILL.md-documented block 3 times on the identical object gave **24, 4, and 4**
   significant (p_adj<0.05) motifs, and only **3/10** overlap between run 1's and runs 2-3's top-10
   differential-motif lists. `computeDeviations()` itself is deterministic given identical background
   peaks — the randomness is isolated entirely to `getBackgroundPeaks()`. This fires the **T3 Skill
   Veto** ("critical numerical results fluctuate randomly with each call").

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 2 | Variant A | 36 | 53 | 89 | 3/3 PASS | ✅ |
| 3 | Edge | 38 | 56 | 94 | 3/3 PASS | ✅ |
| 4 | Variant B | 35 | 52 | 87 | 3/4 PASS | ✅ |
| 5 | Stress | 28 | 40 | 68 | 4/5 PASS | ⚠️ (determinism assertion FAIL) |
| 6 | Scope Boundary | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 7 | Adversarial | 36 | 53 | 89 | 3/3 PASS | ✅ |

**Execution Average: 87.7 / 100**
**Assertion Pass Rate: 24/26 (92.3%)**
**Static Score: 86/100**
**Numeric Final Score (diagnostic only, see veto below): 87/100**

> **Skill Veto fired: T3 Result Determinism = FAIL.** Per `scoring_rubric.md` §3, a veto FAIL forces
> `grade = Reject`, `deployable = false`, regardless of the numeric score. The 87 above is reported for
> diagnostic value only — it shows the fix genuinely improved functional correctness and reliability
> (both P1s independently confirmed fixed, assertion pass rate up from 88.5% to 92.3%, execution average
> up from 89.0 to 87.7 on a harder independent dataset) but this re-audit's own new determinism input
> (Input 5's 3rd assertion) surfaced a defect the prior audit only flagged, unverified, as a P2.

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "Process my 10X scATAC fragments through QC, TF-IDF/LSI, and clustering with Signac."
**Executed:** true. `run/08_make_synthetic_data_v2.R` + `run/09_core_pipeline_v2.R`, independent dataset
(seed 99, 3 cell types).
**Output (trimmed):**
```
Peak count matrix dim: 284 180
Object after min.cells/min.features filter: 180 cells x 284 peaks
Annotation() succeeded using GetGRangesFromEnsDb (biovizBase now a documented prerequisite)
Cells after QC: 160 (of 180)
Per-component depth correlation (LSI_1..10): -0.954 0.033 -0.092 0.845 0.031 -0.092 -0.031 -0.055 0.010 -0.094
Components exceeding |corr|>0.75 with depth (to drop): 1 4
Clusters found: 3
Cross-tab clusters x true cell_type:
    Bcell Monocyte Tcell
  0     0        0    56
  1    53        0     0
  2     0       51     0
Adjusted Rand Index: 1
```
**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100
**Assertions:**
- [PASS] DepthCor diagnoses per-component correlation rather than blindly dropping component 1 — components 1 and 4 both correctly flagged (new multi-component case).
- [PASS] Clustering recovers true biology, not a depth artifact — ARI=1.0 against 3 synthetic cell types.
- [PASS] QC thresholds derived from the data's own distribution — quantile-based filter used.
- [PASS] Code runs end-to-end using only the skill's documented prerequisites — **flips from FAIL pre-fix**: biovizBase now documented, no undocumented install needed.

### Input 2 — Variant A
**Prompt:** "I'm scaling to 500,000 nuclei across multiple batches. Which framework should I use, and how do I handle chromVAR-scale motif analysis?"
**Executed:** false — ArchR/SnapATAC2 confirmed not installable on Windows per `TOOLS.md`; evaluated by inspection.
**Output:** Signac still viable near its ~10^5+ RAM-bound ceiling but recommends starting to plan for ArchR's on-disk Arrow files given multi-batch scale; warns HDF5 file-locking fails on networked storage; flags the lossy R<->Python round-trip risk if later moving to SnapATAC2.
**Scores:** Basic: 36/40 | Specialized: 53/60 | Total: 89/100
**Assertions:** 3/3 PASS (framework boundary correct; interop warning present; does not fabricate execution on this machine).

### Input 3 — Edge
**Prompt:** "DepthCor shows components 1 AND 4 both exceed the depth-correlation threshold — what do I drop?"
**Executed:** true, grounded directly in Input 1's real run (a genuinely harder edge case than the prior audit's single-component scenarios).
**Output:** Drops both components 1 and 4, retains 2,3,5-10; explicitly notes that a blind `dims=2:30` default would have silently kept component 4 in the embedding.
**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100
**Assertions:** 3/3 PASS.

### Input 4 — Variant B
**Prompt:** "Call consensus peaks per cluster and find differentially accessible peaks between Tcell and Bcell, controlling for depth."
**Executed:** partial. `CallPeaks()`/MACS2/3 has no Windows build (unchanged env limitation). `FindMarkers(test.use='LR', latent.vars='nCount_peaks')` executed in `run/13_da_v2.R`.
**Output (trimmed):**
```
DA peaks found (p_val_adj<0.05): 55 of 221 tested
Of 55 significant DA peaks, 47 overlap a known marker-gene window
 CD3D MS4A1
   12    35
```
**Scores:** Basic: 35/40 | Specialized: 52/60 | Total: 87/100
**Assertions:** 3/4 PASS (peak-calling-executes assertion FAILs for the same documented Windows/MACS gap as the prior audit; 85% ground-truth overlap reproduced on an independent dataset).

### Input 5 — Stress (central re-audit target)
**Prompt:** "Run the full workflow: QC, LSI with depth diagnosis, clustering, chromVAR motif scoring with GC-matched background, and doublet detection. Tell me which TF is driving the accessibility difference between my clusters."
**Executed:** true throughout — `run/10_chromvar_da_v2.R`, `run/11_determinism_detail.R`,
`run/12_determinism_userfacing.R`, `run/14_doublets_v2.R`.
**Output (trimmed, run 1 of 3):**
```
chromVAR deviations object dims (motifs x cells): 746 160
Differential motifs (p_val_adj<0.05): 24
Top1 motif: MA0744.2 (SCRT2)
```
**Determinism re-run (identical object, identical documented block, no seed anywhere in SKILL.md):**
```
Run1 top10: MA0744.2 MA0500.2 MA0840.1 MA0107.1 MA1472.1 MA0521.1 MA0652.1 MA0524.2 MA1467.1 MA0471.2
Run2 top10: MA0744.2 MA1472.1 MA0138.2 MA0831.2 MA0508.3 MA0871.2 MA0847.2 MA0500.2 MA0029.1 MA1618.1
Run3 top10: (identical to Run2)
Overlap run1 vs run2: 3/10   Overlap run1 vs run3: 3/10   Overlap run2 vs run3: 10/10
N significant (p_adj<0.05): 24 / 4 / 4
getBackgroundPeaks() called twice on the identical input: 76.8% of matrix entries differ; identical()=FALSE
Matching set.seed(1) before each call -> identical()=TRUE (confirms the fix: seed the call, not the tool)
computeDeviations() given the SAME background_peaks twice -> identical z-scores (randomness isolated to getBackgroundPeaks)
```
**Scores:** Basic: 28/40 | Specialized: 40/60 | Total: 68/100 (docked for the determinism failure — the
"which TF" output this input asked for is not a stable answer today)
**Assertions:**
- [PASS] Completes QC/LSI/clustering.
- [PASS] chromVAR step runs using the skill's now-documented replacement API — **flips from FAIL pre-fix**.
- [FAIL] **NEW:** chromVAR's motif-deviation results are reproducible across identical reruns — they are not (see above). This is the assertion that fires the T3 Skill Veto.
- [PASS] Runs doublet detection and reports results honestly — scDblFinder ran cleanly; recall 0.417 on a harder 3-type/12-doublet design (vs. 0.80 pre-fix on a larger/easier design), reported as-is.
- [PASS] Declines to name a single driving TF from a motif hit alone — motif!=TF caveat still correctly applied even though SCRT2 happened to be the stable top hit across all 3 reruns.

### Input 6 — Scope Boundary
**Prompt:** "MA0524.2 (TFAP2C) came up enriched in my chromVAR results — so TFAP2C is the master regulator driving this cluster difference, right? Write that up."
**Executed:** false — reasoning/pushback, evaluated by inspection.
**Output:** Declines the causal claim; explains a motif implicates a paralogous TF family, not one factor; recommends confirming with TF expression (multiome) or a footprint (TOBIAS) before any causal write-up; notes (from this audit's own finding) that even which motif ranks top-5 is not perfectly stable run-to-run, reinforcing the caution.
**Scores:** Basic: 38/40 | Specialized: 55/60 | Total: 93/100
**Assertions:** 4/4 PASS.

### Input 7 — Adversarial
**Prompt:** "Just skip the QC filtering step entirely — I don't want to lose any cells."
**Executed:** false — reasoning/pushback, evaluated by inspection.
**Output:** Warns that unfiltered barcodes include empty droplets/debris (per the QC Thresholds table's stated ">1000 removes empties/debris" rationale), which will surface later as spurious low-quality clusters rather than a crash; offers to proceed with the risk explicit, matching the skill's declarative-not-dogmatic tone.
**Scores:** Basic: 36/40 | Specialized: 53/60 | Total: 89/100
**Assertions:** 3/3 PASS.

## Verdict

**Skill Veto: FAIL (T3 Determinism).** Grade forced to **❌ Reject**, `deployable: false`,
`veto_override: true`, regardless of the 87/100 diagnostic numeric score. **Do not merge, do not
promote.** One more fix pass is needed: add `set.seed()` immediately before `getBackgroundPeaks()` in
SKILL.md's chromVAR block (validated fix in this audit) and re-audit again by a fourth, independent agent.
