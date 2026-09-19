> **Audit record for `bio-single-cell-hashing-demultiplexing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/single-cell/hashing-demultiplexing) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-hashing-demultiplexing
Generated: 2026-09-19
Source: `GPTomics/bioSkills@d91ed3d5:single-cell/hashing-demultiplexing`
Env: `F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\` (Seurat 5.5.0, demuxmix 1.8.0, scanpy 1.12.4 with `sce.pp.hashsolo`)
All data synthetic; scripts in `run/`, data in `data/`.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (HTODemux) | 38 | 52 | 90 | 5/5 PASS | ✅ |
| 2 | Variant A (hashsolo, 2 tags) | 16 | 23 | 39 | 2/5 PASS | ❌ |
| 3 | Edge (demuxmix rescue) | 33 | 45 | 78 | 3/4 PASS | ❌ |
| 4 | Variant B (genetic vs. hashtag) | 38 | 50 | 88 | 4/4 PASS | ✅ |
| 5 | Stress (unequal pooling) | 38 | 54 | 92 | 5/5 PASS | ✅ |

**Execution Average: 77.4 / 100**
**Assertion Pass Rate: 19/23 (82.6%)**

> Status flags follow the schema rule: ✅ = COMPLETED and total ≥ 75; ⚠️ = COMPLETED but total < 75; ❌ = PARTIAL/ERROR or a content/scope assertion failed. Inputs 2 and 3 are flagged ❌ despite `status: COMPLETED` because they had failing content assertions (2's total is also < 75).

## Detailed Outputs

### Input 1 — Canonical: HTODemux, 4-sample equal pooling
**Prompt:** "I have hashed cells pooled from 4 samples with CITE-seq HTO antibody tags. Assign each cell to its sample of origin and flag cross-sample doublets."

**What ran:** `run/input1_htodemux.R`, following `examples/htodemux_seurat.R` verbatim (CLR `margin=2`, `HTODemux(positive.quantile=0.99)`) on a synthetic 1600-cell, 4-tag Seurat object (`data/hto_counts_4tag.csv`, ground truth included).

**Key output:**
```
 Doublet Negative  Singlet
     123      117     1360

Cross-sample doublet rate: 0.077
Global class agreement with ground truth: 1600 / 1600 = 1.000
Singlet sample-ID agreement (both-singlet subset): 1360 / 1360 = 1.000
```
(Sample-ID comparison required normalizing Seurat's automatic `_`→`-` feature-name sanitization — a general Seurat quirk, not a Skill defect, once accounted for the match is exact.)

**Scores:** Basic: 38/40 | Specialized: 52/60 | Total: 90/100
**Assertions:**
- [PASS] Output classifies every cell into Singlet/Doublet/Negative — all 1600 cells accounted for
- [PASS] Output reports the cross-sample doublet rate — 0.077 printed
- [PASS] Sample assignment matches ground truth — 1600/1600 global, 1360/1360 sample-ID
- [PASS] Code follows the Skill's documented CLR margin=2 / positive.quantile=0.99 pattern exactly
- [PASS] Output does not exceed stated skill scope

---

### Input 2 — Variant A: hashsolo, exactly 2 hashtags ❌ (P0 finding)
**Prompt:** "I have 2 hashtags in my scanpy AnnData object with raw HTO counts in adata.obs. Use hashsolo in scanpy to assign samples when I only have two hashtags." (this exact prompt is one of usage-guide.md's own Example Prompts)

**What ran:** `run/input2_hashsolo.py`, following `examples/hashsolo_scanpy.py` verbatim, on a synthetic 900-cell, 2-tag AnnData (equal pooling, moderate background).

**Key output (first run, default parameters):**
```
=== hashsolo Classification ===
Classification
Negative    900
Cross-sample doublet rate: 0.000
Global class agreement with ground truth: 49 / 900 = 0.054
```
Every single cell — including true singlets and doublets — was called `Negative`. No exception was raised; the only symptom was a set of unrelated numpy `RuntimeWarning: Mean of empty slice` messages that do not name the actual cause.

**Root-cause investigation:** `sce.pp.hashsolo`'s signature shows `number_of_noise_barcodes: int | None = None`, documented as defaulting to `len(cell_hashing_columns) - 2`. With exactly 2 columns that default is **0**, degenerating the noise-distribution fit. Re-running the identical data with `number_of_noise_barcodes=1` set explicitly:
```
Classification
HTO_A       406
HTO_B       374
Doublet      71
Negative     49
agreement 1.0
```
— 100% accuracy. This confirms the root cause precisely. Verified deterministic (identical MD5 hash of the Classification column across 2 repeated runs).

**Scores:** Basic: 16/40 | Specialized: 23/60 | Total: 39/100
**Assertions:**
- [FAIL] Output correctly assigns singlet samples for the majority of true singlets — 0% recovered
- [FAIL] Output surfaces an actionable error/warning when classification degenerates to 100% Negative — only an unrelated numpy warning appears
- [PASS] Code follows the Skill's documented hashsolo call pattern without syntax errors
- [FAIL] Skill documents that hashsolo's number_of_noise_barcodes degenerates with exactly 2 hashtags — not mentioned anywhere, despite this being one of usage-guide.md's own example prompts
- [PASS] Output does not fabricate claims / stays in scope

**This is the audit's single most important finding** — see Recommendation P0 in the JSON report.

---

### Input 3 — Edge: demuxmix rescue of a weak-staining Negative pile
**Prompt:** "My HTODemux call gives a huge Negative pile from weak antibody staining. Which method should I use to rescue it, and how do I run it?"

**What ran:** `run/input3_demuxmix.R` — a baseline HTODemux-style quantile call and a `demuxmix()` call side by side, on a synthetic 800-cell, 3-tag dataset with heavy overdispersed ambient background (`data/hto_counts_weak.csv`).

**Key output:**
```
Baseline HTODemux agreement with truth: 0.951   (Negative fraction 0.406)
demuxmix agreement with truth:          0.961   (Negative fraction 0.405)
True negative fraction:                 0.432
```
demuxmix modestly outperformed the quantile baseline, matching the Skill's claim that it is "robust to bad staining."

**Secondary finding (not scored against the Skill, reported for completeness):** on an earlier, more Poisson-like (underdispersed) synthetic background, the identical `demuxmix()` call threw an **uncaught R error**: `Error in ... glm.nb : missing value where TRUE/FALSE needed`. demuxmix's own warning, printed just before the crash, correctly diagnosed the cause ("Underdispersion observed... Consider running demuxmix with a manual initial droplet assignment using the clusterInit parameter") — but the Skill never mentions this failure mode or the `clusterInit` remedy. See Recommendation P1.

**Scores:** Basic: 33/40 | Specialized: 45/60 | Total: 78/100
**Assertions:**
- [PASS] Output identifies demuxmix as the recommended rescue tool
- [PASS] demuxmix accuracy improves or matches baseline — 0.961 vs 0.951
- [PASS] Output reports resulting Negative fraction — 0.405 vs 0.432 true
- [FAIL] Skill warns about demuxmix's glm.nb hard-crash mode and documents clusterInit — not mentioned

---

### Input 4 — Variant B: choosing genetic vs. hashtag demultiplexing
**Prompt:** "I didn't hash my cells before pooling, but I pooled cells from several different donors. Should I use genetic demultiplexing instead? And once I've called cross-sample doublets, do I still need to run anything else for doublets?"

**What ran:** No code — Mode A direct consultation. Full response text is in `run/input4_modality_choice.md`.

**Summary of output:** Correctly states this Skill does not apply (no hashing library present); recommends genetic demultiplexing (`demuxlet`/`freemuxlet`/`souporcell`/`vireo`) and hands off to `single-cell/batch-integration`; states the same-donor limitation of genetic demux; explains that neither modality catches within-sample (homotypic) doublets and that expression-based detection (`single-cell/doublet-detection`) is still required, using the Skill's own 1/k calibration heuristic.

**Scores:** Basic: 38/40 | Specialized: 50/60 | Total: 88/100
**Assertions:**
- [PASS] Identifies genetic demultiplexing as appropriate given no hashing library
- [PASS] States the same-donor limitation of genetic demux
- [PASS] States within-sample doublets need separate expression-based detection
- [PASS] Does not exceed stated skill scope (hands off rather than inventing a procedure)

---

### Input 5 — Stress: 4-sample unequal pooling with a 5% minority tag
**Prompt:** "I pooled 4 samples with CellPlex CMOs but not in equal numbers — one sample is a rare 5% minority. Normalize the HTOs, run HTODemux, sanity-check the doublet rate against what I'd expect from loading, tell me if the minority sample's tag looks like it failed, and subset to confident singlets. I know hashing won't catch same-sample doublets — what do I still need to run after this?"

**What ran:** `run/input5_stress_unequal.R` on a synthetic 1200-cell, 4-tag dataset with a deliberately rare 5%-pooled tag (`data/hto_counts_unequal.csv`).

**Key output:**
```
 Doublet    HTO-C    HTO-A Negative    HTO-B    HTO-D
     128      240      353      111      330       38

Observed cross-sample doublet rate: 0.107  (vs. 1/k=0.250 within-sample-expected framing)
Global class agreement with ground truth: 0.988
Singlet sample-ID agreement: 1.000
```
The rare tag (HTO-D, 38/961 = 4.0% of singlets, close to the true ~5% pooling fraction net of doublet removal) was correctly distinguished from a failed-antibody signal (which the Skill's Tips describe as near-zero, <1%).

**Scores:** Basic: 38/40 | Specialized: 54/60 | Total: 92/100
**Assertions:**
- [PASS] Classifies all cells and reports per-sample counts including the minority tag
- [PASS] Reconciles observed doublet rate against the k-sample expected fraction
- [PASS] Distinguishes a genuine rare-sample minority tag from a failed antibody
- [PASS] Notes expression-based doublet detection is still required afterward
- [PASS] Sample assignment accuracy verified against ground truth

---

## Reviewer Note

Check ❌ rows first. Input 2 is the load-bearing finding of this audit: it is not a rare adversarial edge case but **one of the Skill's own advertised example prompts**, and it fails completely and silently. Inputs 1, 4, and 5 show the Skill's core reasoning and the HTODemux path are solid and accurate. Input 3 shows demuxmix genuinely helps as claimed, with one undocumented crash mode found along the way.
