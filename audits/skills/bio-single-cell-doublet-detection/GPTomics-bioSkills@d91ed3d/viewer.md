> **Audit record for `bio-single-cell-doublet-detection`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/single-cell/doublet-detection) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-doublet-detection

Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:single-cell/doublet-detection`
Category: 3 — Data Analysis | Mode: A | Complexity: Moderate → N = 5

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | yes | 37 | 52 | 89 | 3/4 PASS | ✅ |
| 2 | Variant A | yes | 34 | 48 | 82 | 3/4 PASS | ✅ |
| 3 | Edge | yes | 37 | 54 | 91 | 4/4 PASS | ✅ |
| 4 | Variant B | yes | 33 | 46 | 79 | 3/4 PASS | ✅ |
| 5 | Stress | yes | 37 | 53 | 90 | 4/4 PASS | ✅ |

**Execution Average: 86.2 / 100**
**Assertion Pass Rate: 17/20 (85 %)**
**Executed inputs: 5/5**

All data SYNTHETIC (the 8-sample PBMC set with labelled doublets) except where noted.

---

## Detailed Outputs

### Input 1 — Canonical

**Prompt:** "Eight PBMC 10x lanes, 700–950 cells each, one donor per lane, four vehicle and four
treated. I want doublets called before I integrate. Use whatever you think is best, set the expected
rate properly, and tell me how much you trust the result."

**Response.** Followed SKILL.md's scDblFinder section: build a SingleCellExperiment from merged raw
counts with a `sample_id` column, `scDblFinder(sce, samples='sample_id')`, read `.class`/`.score` back.
Computed the expected rate per lane with the Skill's `0.008 × recovered/1000` rule before running, and
ran the merged (no `samples=`) call as a control. Full code in `run/input1.R` and
`run/input1b_determinism.R`.

**What ran and what it printed** (`run/input1.log`, `run/input1b.log`):

```
scDblFinder 1.20.2 | Seurat 5.5.0
merged: 6524 cells across 8 samples
rate rule (0.008 * recovered/1000) per lane:
  S1 n=707 -> expected 0.57% (4 doublets); TRUE injected rate 2.97%
  ... S2-S8 the same shape: expected 0.59-0.72%, injected 2.95-3.06% ...
PER-SAMPLE (samples=): called 215 (3.30%)  TP=149 FP=66 FN=46  recall=0.764 precision=0.693
AUC of scDblFinder.score vs truth: 0.9772
MERGED  (no samples=): called 298 (4.57%)  TP=159 FP=139 FN=36  recall=0.815 precision=0.534
cor(scDblFinder.score, log10 total counts) = 0.634
false-positive rate by true cell type: CD4 T 0.021, CD8 T 0.016, CD14+ Mono 0.004, rest 0.000

set.seed(20260916) twice: calls 215 vs 207; disagree on 54 cells (22.7% of the union of calls)
BPPARAM = SerialParam(RNGseed=20260916) twice: calls 211 vs 211; disagree on 0 cells (0.0%)
```

**Findings.** The Skill's first Common Errors row is right and now has a number behind it: dropping
`samples=` costs 16 precision points (0.693 → 0.534) on identical data. The score itself is excellent
(AUC 0.977); what limits recall is the threshold, not the model. The Governing Principle's third
claim — that doublet score rides the same axis as count-based QC — is confirmed at r = 0.634.

The finding that matters: **`set.seed()` does not control the call the Skill prescribes.** Two runs of
the same script with the same seed disagreed on 54 cells, 22.7% of the union of their doublet calls.
`samples=` dispatches through BiocParallel, which does not inherit the base R seed, and
`BPPARAM = SerialParam(RNGseed=)` fixes it completely. The Skill mentions seeds nowhere — not in
SKILL.md, not in the usage guide, not in either example. This was the closest call in the audit
(see the veto note below).

**Scores:** Basic 37/40 | Specialized 52/60 (Meth 19, Code 14, Data QC 9, Reproducibility 5, Security 5) | **Total 89/100**
**Assertions:** 3/4 — FAIL on reproducibility.

---

### Input 2 — Variant A

**Prompt:** "My pipeline is scanpy end to end, I don't want to bounce to R. Same eight lanes. Run
Scrublet properly — last time I used the default 5% rate and the reviewer asked where the number came
from."

**Response.** Followed SKILL.md:95-105: `sc.pp.scrublet` on raw counts, per sample, with
`expected_doublet_rate` from the lane's recovered cells. Ran four variants for comparison: the Skill's
rate rule, the 0.05 placeholder it warns against, the `batch_key` alternative it offers in the same
sentence, and one call on the merged object. Then, separately, the loop exactly as SKILL.md:105 prints
it. Code in `run/input2.py` and `run/input2b_view.py`.

**What ran and what it printed** (`run/input2.log`, `run/input2b_view.py` output):

```
  S1: n=707 expected_rate=0.0057 threshold=0.0294 called=5  true=21
  ... S2-S8: expected 0.0059-0.0072, called 5-8, true 22-27 ...
PER-SAMPLE loop, rate from recovered cells:  called 47 (0.72%) recall=0.236 precision=0.979  AUC 0.8687
PER-SAMPLE with the 0.05 placeholder:        called 59 (0.90%) recall=0.277 precision=0.915
batch_key route:                             called 47 (0.72%) recall=0.236 precision=0.979
                                             agrees with the explicit loop on 6524/6524 cells
MERGED single call:                          called 89 (1.36%) recall=0.426 precision=0.933
no random_state, two runs on S1 agree on 707/707 cells

[the SKILL.md:105 loop, verbatim]
warnings raised: ['ImplicitModificationWarning: Trying to modify attribute `.obs` of view,
                  initializing view as actual.', ... x2]
'doublet_score' in parent .obs after the verbatim loop: False
'predicted_doublet' in parent .obs: False
```

**Findings.** **The per-sample loop the Skill prints is a no-op.** `sc.pp.scrublet(adata[adata.obs.sample == s], ...)`
scores a view; the results are discarded, scanpy raises a warning rather than an error, and the parent
object ends with no doublet columns at all. An agent that follows SKILL.md:105 literally proceeds with
an unscored dataset it believes is scored. The `batch_key` alternative offered in the very same
sentence is correct and agreed with an explicit loop on every one of 6,524 cells.

The Skill's ranking is also confirmed: Scrublet AUC 0.869 sits between DoubletFinder (0.685) and
scDblFinder (0.977). Honest nuance in the other direction: on this dataset the merged Scrublet call had
*higher* recall (0.426) than the per-sample loop, because the pooled histogram puts the threshold in a
better place — so the Skill's "run per sample" rule cost recall here even though it is correct in
principle (a doublet is a physical event in one droplet). That trade-off is not discussed anywhere.

Low absolute recall (0.236) is **dataset context, not a Skill defect**: the synthetic set injects ~3%
doublets per 800-cell lane, roughly four times what the 0.8%/1000 rule predicts.

**Scores:** Basic 34/40 | Specialized 48/60 (Meth 17, Code 9, Data QC 9, Repro 8, Security 5) | **Total 82/100**
**Assertions:** 3/4 — FAIL on the view loop.

---

### Input 3 — Edge

**Prompt:** "This one's a FACS-sorted CD4 population — I sorted on CD4+CD3+ before loading, so it's
essentially one cell type, about 900 cells. scDblFinder finds almost nothing. Is my sample clean or is
the method blind here?"

**Response.** Built the sorted population (`data/sorted_cd4.h5ad`), ran Scrublet with the rate rule,
inspected the simulated-score distribution rather than trusting the automatic threshold, applied the
Skill's prescribed manual-threshold fix, and scored both against the 25 real doublets present.
Code in `run/input3.py`.

**What ran and what it printed** (`run/input3.log`):

```
Sorted CD4 set: 900 cells, true doublets in it: 25
Skill rate rule -> expected_doublet_rate = 0.0072
auto threshold = 0.0447; called 5 doublets
simulated-doublet scores: n=1800 min=0.0029 med=0.0174 max=0.0754
observed scores:          n=900  min=0.0022 med=0.0117 max=0.0505
  auto threshold:                       called 5  TP=0 FP=5  FN=25 recall=0.000 precision=0.000
  manual threshold from the rate rule:  called 20 TP=0 FP=20 FN=25 recall=0.000 precision=0.000
homotypic check: of the 25 true doublets, 18 score above the median observed score - i.e. most
  CD4-CD4 homotypic doublets are not separable, as the Skill states.
```

**Findings.** This is the Skill's hardest claim tested in its worst case, and it holds completely: on a
sorted single-population capture containing 25 genuine doublets, **no expression-based threshold
recovered a single one**. The correct answer to the researcher's question is the Skill's own — "the
method is blind here, do not report the sample as clean, use hashing" — and the Skill supplies it in
three separate places (Governing Principle, the heterotypic/homotypic table, and the "Reported 0%
doublets" Common Errors row).

One correction: my crude modality check found three local maxima in the simulated-score histogram
rather than the clean unimodal shape the Skill's Common Errors row 2 describes. The failure was real
but the diagnostic the Skill names ("the histogram is unimodal") would not have flagged it. The Skill's
prescribed fix — set the threshold manually — also did not help, because the problem is not the
threshold.

**Scores:** Basic 37/40 | Specialized 54/60 (Meth 19, Code 13, Data QC 9, Repro 8, Security 5) | **Total 91/100**
**Assertions:** 4/4 PASS.

---

### Input 4 — Variant B

**Prompt:** "We have a three-year-old Seurat pipeline with DoubletFinder in it and a reviewer who knows
that paper. I'd rather not rewrite it. Can you make DoubletFinder work on Seurat 5 and tell me whether
it's actually worse than what you'd pick?"

**Response.** Ran the Skill's DoubletFinder block and `examples/doubletfinder.R` on one lane (S2, 864
cells after `min.cells`/`min.features`): checked what the installed package exports, swept `pK`,
applied `modelHomotypic`, ran the classifier, and compared pANN AUC with input 1's scDblFinder score on
the same cells. Code in `run/input4.R`.

**What ran and what it printed** (`run/input4.log`):

```
DoubletFinder 2.0.6 | Seurat 5.5.0
exported: doubletFinder, find.pK, modelHomotypic, paramSweep, pbmc_small, summarizeSweep
paramSweep present: TRUE | paramSweep_v3 present: FALSE
doubletFinder present: TRUE | doubletFinder_v3 present: FALSE
Loaded 864 cells
paramSweep + find.pK took 13.6 s; optimal pK = 0.18
rate = 0.00691 | nExp before homotypic adjustment = 6 | modelHomotypic = 0.195 | nExp = 5
TRUE doublets in this lane: 26

EXAMPLE SCRIPT CALL (reuse.pANN = FALSE) FAILED:
   Error in xtfrm.data.frame(x) : cannot xtfrm data frames
  -> reuse.pANN = FALSE is not NULL, so doubletFinder takes its reuse branch:
     pANN.old <- seu@meta.data[, FALSE] is a zero-column data.frame, then order() on it.

metadata column added: DF.classifications_0.25_0.18_5
DoubletFinder: called 5  TP=2 FP=3 FN=24 recall=0.077 precision=0.400
AUC of pANN vs truth: 0.6847
same pANN, nExp from the TRUE rate (21): called 21 recall=0.154 precision=0.190
```

**Findings.** Two things, one good and one bad.

Bad: **`examples/doubletfinder.R` cannot run.** Line 36 passes `reuse.pANN = FALSE`. Because `FALSE`
is not `NULL`, DoubletFinder takes its reuse branch, builds `pANN.old` from `seu@meta.data[, FALSE]`
— a zero-column data.frame — and dies in `order()`. The `SKILL.md:123` snippet, which omits the
argument entirely, runs fine, so the Skill body and its own example disagree. The Common Errors row for
DoubletFinder failures prescribes "use current function names", which does not help: the names were
already current, as the same run confirms.

Good: the Skill's characterisation of DoubletFinder is vindicated by measurement. pANN AUC 0.685 on the
same lane where scDblFinder scored 0.977, and even when `nExp` is handed the true doublet count the
precision only reaches 0.190. The Skill's instruction not to cite Xi and Li 2021 against current
scDblFinder is supported rather than merely asserted. `modelHomotypic` worked as documented (0.195
homotypic fraction, nExp 6 → 5) and `*_v3` really is gone.

**Scores:** Basic 33/40 | Specialized 46/60 (Meth 17, Code 8, Data QC 9, Repro 7, Security 5) | **Total 79/100**
**Assertions:** 3/4 — FAIL on the shipped example.

---

### Input 5 — Stress

**Prompt:** "New experiment: eight donors hashed with TotalSeq-B and loaded into a *single* lane,
~6,500 cells recovered. Two questions. What expected doublet rate do I set — per donor or for the
lane? And there's a 330-cell cluster that's CD3D+ and LYZ+ that my PI wants to write up as a
monocyte-primed T-cell intermediate. Is it real?"

**Response.** Computed the rate both ways the Skill contrasts, then clustered the pooled lane and built
a per-cluster table of true-doublet fraction against lineage co-expression, comparing each against the
dataset-wide baseline before answering. Code in `run/input5.py`.

**What ran and what it printed** (`run/input5.log`):

```
(a) per demultiplexed sample (~816 cells): 0.65%   <- the Skill says this UNDERESTIMATES
    from total lane loading (6524 cells):  5.22%   <- the Skill says use this
    physical doublets actually injected:   2.99%

(b) 20 Leiden clusters
          n  pct_true_doublet  CD3D+   LYZ+  MS4A1+  CD3D+LYZ+
leiden 6  331             13.0   26.3  100.0    11.2       26.3
leiden 5  124              7.3   37.9  100.0    18.5       37.9
leiden 9   87              5.7   11.5  100.0     5.7       11.5
leiden 12 390              4.6    9.5   71.0    83.3        7.2
  cluster 6: n=331, 13.0% true injected doublets, 26.3% CD3D+LYZ+
  true cell-type composition: {'CD14+ Monocytes': 315, 'CD4 T': 6, 'NK': 5, 'CD8 T': 3}
  dataset-wide baseline: 3.0% doublets, 36.0% CD3D+LYZ+ cells
```

**Findings.** (a) The multiplexed-lane rule is correct and materially so: 5.22% from total lane loading
against a true 2.99%, versus 0.65% from the demultiplexed subset. The Skill's direction is right and
the magnitude of the error it prevents (8x) is larger than the residual error it leaves (1.7x).

(b) The claim is refused, correctly — cluster 6 is 4.3x enriched for genuine doublets over the
dataset baseline. But **the heuristic the Skill actually prescribes would have pointed elsewhere.**
The Governing Principle says to treat a small cluster co-expressing two lineage programs (CD3+LYZ) as
doublet-suspect; cluster 6 is *below* the dataset-wide CD3D+LYZ+ rate (26.3% vs 36.0%), because ambient
RNA puts a little of everything in every barcode. The Skill knows this — "Heavy ambient RNA can mimic
co-expression and nudge scores" — but that sentence is 100 lines away in Deeper Cautions, not attached
to the heuristic it invalidates. On a dataset with the ambient contamination the Skill itself tells you
to expect, the bare heuristic is unusable and the doublet score is what works.

**Scores:** Basic 37/40 | Specialized 53/60 (Meth 18, Code 13, Data QC 9, Repro 8, Security 5) | **Total 90/100**
**Assertions:** 4/4 PASS.

---
---

# STEP 8 — Optimization Report

```
══════════════════════════════════════════════════
SKILL AUDIT REPORT
══════════════════════════════════════════════════
Skill Name     : bio-single-cell-doublet-detection
Category       : Data Analysis (3)
Execution Mode : A
Complexity     : Moderate (N = 5)
Audited On     : 2026-09-16
Executed       : 5/5 inputs

── STEP 1: Structural Veto ───────────────────────
Stability    : PASS
Contract     : PASS — frontmatter name + description present and accurate.
Determinism  : PASS — see the note below; this was the closest call in the audit.
Security     : PASS — no eval/exec, no credentials, no network calls.

  Determinism note. T3's triggers include "lack of seed management mechanism, making experiments
  irreproducible". The Skill has none, and its headline call moved 22.7% of its doublet calls
  between two identically seeded runs. It is recorded as PASS rather than FAIL because the
  underlying score is stable (AUC 0.977, and the class labels agree on 99.2% of cells) — the
  movement is confined to cells at the threshold, so the results are not "uncontrollable", they
  are imprecisely reproducible. The deduction is taken at Agent-Specific 8.4 (Idempotency 1/4)
  and as a P1. A reader who disagrees with that line would fail T3 and reject the Skill; the
  evidence for either reading is in run/input1b.log.

── STEP 2: Static Evaluation (25 criteria) ───────
Functional Suitability : 11/12
Reliability            :  9/12
Performance/Context    :  7/8
Agent Usability        : 15/16
Human Usability        :  7/8
Security               : 10/12
Maintainability        :  9/12
Agent-Specific         : 16/20
Static Subtotal        : 84/100

Changes vs the lead's draft (`tools/static_drafts.json`):
  reliability     10 → 9. Both failures this audit found were silent or misdiagnosed, which is
                  what Category 3 Override 1 says to score on. The view loop raises no error at
                  all; the DoubletFinder Common Errors row prescribes a fix for the wrong cause.
  maintainability 10 → 9. One of two shipped example scripts aborts on its own call, so half the
                  shipped verification surface does not execute (Testability 3 → 2).
  agent_specific  17 → 16. The draft flagged "no seed guidance for scDblFinder's random doublet
                  simulation" as a suspicion; it is now measured at 22.7% call movement, which is
                  an Idempotency 1, not a 3.
  functional_suitability kept at the draft's 11. The draft's specific worry (the per-sample loop
                  shown on a view) is confirmed, but so is almost every factual claim in the
                  Skill, so Completeness 4 / Correctness 3 / Appropriateness 4 stands.
  The four other categories were verified against the files and left unchanged.

── STEP 3: Classification ────────────────────────
Category       : Data Analysis
Execution Mode : A

── STEP 4: Test Inputs ───────────────────────────
1 Canonical : 8 PBMC lanes, call doublets before integration
2 Variant A : scanpy-only pipeline, Scrublet, "where did 5% come from?"
3 Edge      : FACS-sorted CD4 population — clean, or is the method blind?
4 Variant B : legacy DoubletFinder on Seurat 5, and is it actually worse?
5 Stress    : 8 hashed donors in one lane + a CD3D+LYZ+ cluster the PI wants to publish

── STEP 5: Execution Summary ─────────────────────
Input 1: COMPLETED — ran; determinism defect discovered
Input 2: COMPLETED — ran; prescribed loop found to be a silent no-op
Input 3: COMPLETED — ran; Skill's homotypic claim validated (0/25)
Input 4: COMPLETED — ran; shipped example aborts, SKILL.md snippet works
Input 5: COMPLETED — ran; rate rule validated, marker heuristic found misleading

── STEP 6: Output Evaluation ─────────────────────
         Basic  Specialized  Total  Assertions
Input 1:  37/40    52/60    89/100   3/4 PASS
Input 2:  34/40    48/60    82/100   3/4 PASS
Input 3:  37/40    54/60    91/100   4/4 PASS
Input 4:  33/40    46/60    79/100   3/4 PASS
Input 5:  37/40    53/60    90/100   4/4 PASS
Execution Avg               : 86.2/100
Total Assertion Pass Rate   : 17/20 (85 %)

Research Veto (Category 3 — applicable)
Scientific Integrity  : PASS
Practice Boundaries   : PASS
Methodological Ground : PASS
Code Usability        : PASS — 5/5 executed; the two broken snippets each have a one-token fix
                        and the primary scDblFinder path runs clean.

── STEP 8: Final Score ───────────────────────────
Static Score   : 84/100   × 40% = 33.6
Dynamic Score  : 86.2/100 × 60% = 51.7
FINAL SCORE    : 85 / 100
GRADE BY SCORE : ⭐ Production Ready
```

## Floors check (scoring_rubric.md § 5)

| Component | Floor for ⭐ | Observed | Held? |
|---|---|---|---|
| Static Score | ≥ 80 | 84 | ✅ |
| Execution Average | ≥ 85 | 86.2 | ✅ |
| Layer 1 avg (/40) | ≥ 32 | 35.6 | ✅ |
| Layer 2 avg (/60) | ≥ 48 | 50.6 | ✅ |
| Assertion pass rate | ≥ 90 % | 85 % | ❌ |

One floor missed → **downgrade exactly one tier**.

**GRADE AFTER FLOORS: ✅ Limited Release (score 85, deployable).**
No safety or scope assertion failed on any output. All three assertion failures are functional:
prescribed code that does not run as printed (inputs 2, 4) or is not reproducible (input 1).

## Shipped-means-present (gate 8)

`SKILL.md` and `usage-guide.md` contain **no** `references/`, `scripts/`, `assets/` or `templates/`
pointers, so nothing is promised and missing. Both shipped example scripts exist and parse
(`py_compile` clean; R `parse()` clean). `examples/doubletfinder.R` parses but **aborts at runtime** —
that is a correctness defect (P1 above), not a gate-8 failure. No P0.

## Research scope (gate 7)

Research only; no individual-level diagnosis, prescription or triage. M2 PASS.

## Recommendations

```
[P1] The Python per-sample loop silently discards its own results          (Input 2)
[P1] The prescribed scDblFinder call is not reproducible; no seed guidance (Input 1)
[P1] Shipped DoubletFinder example aborts on its own call                  (Input 4)
[P2] The lineage co-expression heuristic needs an ambient caveat in place  (Input 5)
[P2] No guidance on what to report                                      (Inputs 1, 2, 3)
```

Full problem / root cause / fix text for each is in the JSON.

**Deployable: yes** (Limited Release, no veto, no open P0).
**Core-Skill note:** `final.score` = 85, clearing the gate-3 core threshold; post-floor grade is
Limited Release. Both numbers carried into `AUDIT.md`. The three P1s are all one-line fixes and are
the strongest fix-pass candidates found in this candidate's Skill set.
