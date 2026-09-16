> **Audit record for `bio-single-cell-markers-annotation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/single-cell/markers-annotation) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-markers-annotation

Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:single-cell/markers-annotation`
Category: 3 — Data Analysis | Mode: A | Complexity: Moderate → N = 5

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | yes | 37 | 55 | 92 | 4/4 PASS | ✅ |
| 2 | Variant A | yes | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 3 | Edge | yes | 37 | 55 | 92 | 4/4 PASS | ✅ |
| 4 | Variant B | yes | 30 | 46 | 76 | 3/4 PASS | ✅ |
| 5 | Stress | yes | 39 | 57 | 96 | 4/4 PASS | ✅ |

**Execution Average: 90.0 / 100**
**Assertion Pass Rate: 19/20 (95 %)**
**Executed inputs: 5/5**

All data SYNTHETIC (8-sample PBMC set with ground-truth cell types and 55 injected DE genes in
CD14+ monocytes). No derived datasets were needed, so this audit has no `data/` folder.

---

## Detailed Outputs

### Input 1 — Canonical

**Prompt:** "I've got 12 clusters from 6,000 PBMCs. Find me the markers and tell me what each cluster
is. I want something I can defend, not a list of genes with tiny p-values."

**Response.** SKILL.md:61-71 verbatim — `rank_genes_groups(method='wilcoxon', pts=True,
corr_method='benjamini-hochberg')`, pull to a DataFrame, and apply the Skill's specificity filter
(`logfoldchanges > 1`, `pct_nz_group > 0.5`, `pct_nz_reference < 0.25`). Then module-scored each of
the Skill's eight canonical PBMC panels per cluster and assigned labels by argmax. The "Defaults that
bite" claim about `method=None` was checked first. Code in `run/input1.py`.

**What ran and what it printed** (`run/input1.log`):

```
6049 cells, 12 clusters, 8 true types
rank_genes_groups default method = None
  params recorded after a default call: {'groupby': 'leiden', 'method': 't-test', ...}
  top-20 marker overlap between the default call and explicit wilcoxon: 0.86
columns returned: group, names, scores, logfoldchanges, pvals, pvals_adj, pct_nz_group, pct_nz_reference
markers total 150252 -> specific 712 (12/12 clusters keep any)

smallest adjusted p across all clusters: 0.00e+00; genes at padj<0.05: 16189 of 150252
  top-5-by-p vs top-5-by-specificity overlap per cluster: 0.25

module score per cluster (excerpt):
leiden   CD4 T  CD8 T     B    DC    NK  CD14 Mono  FCGR3A Mono  Platelet
0        -0.54  -0.89 -0.19  1.15 -0.50       2.62         0.05     -0.13
2        -0.40  -0.37 -0.06  0.86 -0.04       0.35        -0.09      5.23
4        -0.52  -0.67 -0.24 -0.34  2.38      -0.25         0.61     -0.17
6         0.33   0.54 -0.19 -0.48  1.19      -0.29        -0.07     -0.13

accuracy of the manual labelling vs truth: 0.879
                   B  CD14 Mono  CD4 T   DC  FCGR3A Mono  Mk    NK
B cells          706          0      0    0            0   0     0
CD4 T cells        0          0   2127    0            0   0     0
CD8 T cells        0          0      7    0            0   0   724   <-- the whole error
CD14+ Monocytes    0       1184      0    0            0   0     0
Dendritic cells    0          0      0  250            0   0     0
FCGR3A+ Mono       0          0      0    0          352   0     0
Megakaryocytes     0          0      0    0            0 142     0
NK cells           0          0      0    0            0   0   557
```

**Findings.** The `method=None` claim is verified from the object itself: after a default call,
`uns['params']` records `'method': 't-test'`. The consequence is real but moderate here — 0.86 top-20
overlap with an explicit Wilcoxon run — which is exactly why it is the kind of thing a Skill should
tell an agent rather than leaving it to be noticed.

The specificity filter does the work the Skill claims: 150,252 marker rows to 712, with every cluster
keeping something. And its argument against p-value ranking is measurable — the top-5-by-p and
top-5-by-specificity lists overlap only 0.25 per cluster, and 16,189 gene-by-cluster tests clear
padj < 0.05 with a smallest value of exactly 0.

The labelling reached 0.879 accuracy, and the single systematic error is instructive: 724 of 731 CD8
T cells were labelled NK, because the Skill's NK panel (NKG7, GNLY, NCAM1) is shared with cytotoxic
CD8 T cells while its CD8 panel leans on sparsely-detected CD8A/CD8B. The Skill states the general
principle ("a marker is a conditional statement, not a property of a gene") but its own panel table
does not flag which pairs it cannot separate. That is the P2 below.

**Scores:** Basic 37/40 | Specialized 55/60 (Meth 19, Code 14, Data QC 9, Repro 8, Security 5) | **Total 92/100**
**Assertions:** 4/4 PASS.

---

### Input 2 — Variant A

**Prompt:** "We're a Seurat lab and our old script used `logfc.threshold = 0.25`. On v5 it returns a
completely different number of markers and I don't know which is right."

**Response.** Checked the three Seurat rows of the "Defaults that bite" table against the installed
package with `formals()`, then ran `FindAllMarkers` both at the Skill's explicit thresholds and at
the v5 defaults, then applied the specificity filter. Also exercised the cell-cycle section.
Code in `run/input2.R`.

**What ran and what it printed** (`run/input2.log`):

```
Seurat 5.5.0 | presto 1.1.0
  FindMarkers logfc.threshold default: 0.1   (Skill says 0.1 in v5, folklore 0.25)
  FindMarkers min.pct default        : 0.01  (Skill says 0.01 in v5, folklore 0.1)
  test.use default                   : "wilcox"
  presto installed (so wilcox is fast): TRUE

6048 cells, 14 clusters
FindAllMarkers (logfc 0.25 / min.pct 0.1) took 7 s   -> 15241 rows
FindAllMarkers at the v5 DEFAULTS took 8.5 s         -> 28584 rows   (1.9x)
after the Skill's specificity filter: 140 rows, 14 of 14 clusters retain markers

cell-cycle scoring:  G1 1693 | G2M 2317 | S 2038
  cc.genes.updated.2019 available with both lists: TRUE
```

**Findings.** All three Seurat claims are exactly right against Seurat 5.5.0, and the "permissive,
returns more hits" characterisation is measurable at 1.9×. This is precisely the question the
researcher asked, and the Skill answers it without the agent having to guess.

The marker shortlist that comes out of the Skill's filter is biologically coherent (cluster 2:
IGLL5/CD79A/LINC00926; cluster 8: CLIC3/GNLY/GZMB; cluster 11: GP9/CLDN5 platelets; cluster 13:
FCER1A/LILRA4 DC), which is what a marker-grade list should look like.

`CellCycleScoring` with `cc.genes.updated.2019` ran as documented and both gene lists are exposed, as
SKILL.md:125 says. One claim I could **not** verify: the Skill says scanpy uses 25 control bins and
Seurat 24. scanpy's `n_bins` default is 25 as stated, but `AddModuleScore`'s `nbin` shows as `NULL`
at the generic, so the Seurat side is unconfirmed from this environment — recorded as a P2 about the
audit's coverage rather than as a defect.

**Scores:** Basic 38/40 | Specialized 56/60 (Meth 19, Code 15, Data QC 9, Repro 8, Security 5) | **Total 94/100**
**Assertions:** 4/4 PASS.

---

### Input 3 — Edge

**Prompt:** "This is a sorted CD4 fraction — one population, 2,100 cells. `rank_genes_groups` gives me
a table of NaNs. What am I supposed to do with that?"

**Response.** Reproduced the degenerate case, then evaluated both branches the Skill's Common Errors
row offers ("subcluster the population **or** report it as a single homogeneous type"), and checked
what the subcluster split actually tracks. Code in `run/input3.py`.

**What ran and what it printed** (`run/input3.log`):

```
2127 CD4 T cells, one group only

(a) rank_genes_groups with a single group:
  ran without error. rows 12521; NaN logfoldchanges 12521; NaN pvals 0; smallest padj 1.0
  warnings: ['RuntimeWarning: invalid value encountered in divide', ...]

(b) subcluster, then rank:
  subclustering gives 2 groups
  markers 25042 -> "specific" 0; smallest padj 7.33e-231
  clusters x batch:
  leiden     A     B
  0       1020     0
  1          0  1107
```

**Findings.** The Common Errors row is exact, including the detail that matters most: scanpy raises
**no exception**. All 12,521 log fold changes come back NaN with only `RuntimeWarning`s, so a
pipeline that does not check will carry a table of NaNs forward.

The better result is what happened on the second branch. Subclustering split the population perfectly
along the two sequencing batches (1020/0, 0/1107) with adjusted p-values down to 7×10⁻²³¹ — and the
Skill's own specificity filter returned **zero** markers for that split. The effect-size-plus-fraction
filter caught a batch artifact that the p-values endorsed unreservedly. That is the Skill's central
argument working as designed.

The correct branch here is the Skill's other one — report it as a single homogeneous type — which is
what the response did, and which matches the truth labels exactly.

**Scores:** Basic 37/40 | Specialized 55/60 (Meth 19, Code 14, Data QC 9, Repro 8, Security 5) | **Total 92/100**
**Assertions:** 4/4 PASS.

---

### Input 4 — Variant B

**Prompt:** "Now I want the treated-vs-control genes inside my CD14 monocytes. Aggregate it for me so
I can hand the matrix to DESeq2."

**Response.** Ran the Skill's Python pseudobulk snippet verbatim on the object its own upstream steps
produce, then ran the corrected form, compared the two matrices, and put both through pyDESeq2 against
ground truth. Code in `run/input4.py`.

**What ran and what it printed** (`run/input4.log`):

```
object state after the Skill's own upstream steps: X is log-normalized, layers = ['counts']
1184 CD14 Mono cells across 8 samples

SKILL.md snippet, verbatim  (sc.get.aggregate(ct, by='sample', func='sum')):
  shape (8, 12521); all values integral? False
  min 0.0000 max 988.9412; row sums [247516, 311364, 305074, 308235] ...

with layer="counts" (what the Skill's own rule requires):
  shape (8, 12521); all values integral? True
  min 0.0 max 17064.0; row sums [341552, 430950, 441700, 433762] ...
  correlation between the two matrices (flattened): 0.7289

  pyDESeq2 on log-normalized sums (the snippet as written):
    16 genes padj<0.05 | TP 16 | precision 1.000 | recall 0.291
  pyDESeq2 on raw count sums (layer="counts"):
    19 genes padj<0.05 | TP 19 | precision 1.000 | recall 0.345
```

**Findings.** **The Skill contradicts itself inside one document.** Its "Defaults that bite" table
says, in so many words, "Pseudobulk input — folklore: normalized/log values — actual: aggregate RAW
counts (summed), never normalized". Four sections later its Python snippet calls
`sc.get.aggregate(cell_type, by='sample', func='sum')` with no `layer=`, which on the object produced
by the Skill's own earlier steps sums the **log-normalized** values in `.X`.

The result is a non-integer matrix that R's `DESeqDataSetFromMatrix` would reject outright ("counts
matrix should be integers"), correlates only 0.729 with the correct one, and in Python silently loses
power — 16 calls instead of 19, recall 0.291 instead of 0.345. Precision stayed at 1.000, so this is
a sensitivity loss rather than a false-positive problem, but it is the kind of defect that survives
copy-paste indefinitely.

The R snippet on the very next line (`AggregateExpression(..., layer = 'counts')`) is correct, which
makes the Python omission look like an oversight rather than a misunderstanding.

**Scores:** Basic 30/40 | Specialized 46/60 (Meth 15, Code 9, Data QC 9, Repro 8, Security 5) | **Total 76/100**
**Assertions:** 3/4 — FAIL on the raw-counts requirement.

---

### Input 5 — Stress

**Prompt:** "Forget the aggregation — just run the marker test with `groupby='condition'` on all my
CD14 monocytes. I have 1,184 cells, that's plenty of power, and I need the gene list today."

**Response.** Refused and measured the cost, including on a deliberately null contrast where every
call is a false positive by construction. Code in `run/input5.py`.

**What ran and what it printed** (`run/input5.log`):

```
1184 CD14 Mono cells, 8 donors; ground truth: 55 genes changed in this cell type

(a) cell-level Wilcoxon, REAL contrast:
    37 called | TP 24 | precision 0.649 | recall 0.436 | smallest padj 7.41e-147

(b) cell-level Wilcoxon, NULL contrast (condition, batch and sex each balanced 2+2):
    13 genes at padj<0.05 & |logFC|>0.5 (ALL FALSE by construction); smallest padj 2.02e-13

(c) pseudobulk, NULL contrast:  0 genes at padj<0.05; smallest padj 1
    pseudobulk, REAL contrast: 19 called | TP 19 | precision 1.000 | recall 0.345
```

**Findings.** The Skill's Governing Principle carries this input completely, and the numbers make its
case better than the citation does. On a contrast where nothing is different, the cell-level test
returned 13 "significant" genes with a smallest adjusted p of 2×10⁻¹³ — values nobody would question
in a figure legend — while the pseudobulk route returned zero with a smallest padj of exactly 1.

On the real contrast, the cell-level test's apparently higher recall (0.436 vs 0.345) is bought
entirely with false positives: precision 0.649 against 1.000. The extra 13 genes are not extra
sensitivity.

The Skill's own explanation of why this error is so common — "the tool not stopping the user" — is
literally what happened: `rank_genes_groups` ran the condition contrast without complaint and returned
a tidy table with p-values down to 7×10⁻¹⁴⁷.

**Scores:** Basic 39/40 | Specialized 57/60 (Meth 20, Code 14, Data QC 9, Repro 9, Security 5) | **Total 96/100**
**Assertions:** 4/4 PASS.

---
---

# STEP 8 — Optimization Report

```
══════════════════════════════════════════════════
SKILL AUDIT REPORT
══════════════════════════════════════════════════
Skill Name     : bio-single-cell-markers-annotation
Category       : Data Analysis (3)
Execution Mode : A
Complexity     : Moderate (N = 5)
Audited On     : 2026-09-16
Executed       : 5/5 inputs

── STEP 1: Structural Veto ───────────────────────
Stability    : PASS
Contract     : PASS
Determinism  : PASS — every method here is deterministic given the upstream clustering.
Security     : PASS

── STEP 2: Static Evaluation (25 criteria) ───────
Functional Suitability : 10/12
Reliability            :  9/12
Performance/Context    :  7/8
Agent Usability        : 13/16
Human Usability        :  7/8
Security               : 10/12
Maintainability        : 10/12
Agent-Specific         : 18/20
Static Subtotal        : 84/100

Changes vs the lead's draft (`tools/static_drafts.json`):
  agent_usability 14 → 13. The draft flagged the aggregate snippet as contradicting the Skill's
    own "RAW counts" rule "if confirmed". It is confirmed by measurement (input 4), which makes
    it a same-document semantic contradiction rather than a formatting nit, so Consistency is a
    2 rather than a 3.
  functional_suitability kept at the draft's 10, reliability at 9, agent_specific at 18 - all
    re-derived from the files and the runs and landing on the same values. The draft's note that
    "cell-cycle gene lists are not supplied for scanpy" is correct and the Skill says so itself,
    so it is not counted twice.

── STEP 3: Classification ────────────────────────
Category       : Data Analysis
Execution Mode : A

── STEP 4: Test Inputs ───────────────────────────
1 Canonical : 12 clusters, markers and labels I can defend
2 Variant A : Seurat v5 changed my marker counts, which threshold is right?
3 Edge      : sorted CD4 fraction, rank_genes_groups returns NaNs
4 Variant B : aggregate CD14 monocytes to pseudobulk for DESeq2
5 Stress    : "1,184 cells is plenty of power, just run the condition contrast"

── STEP 5: EXECUTION SUMMARY ─────────────────────
Input 1: COMPLETED — method=None → t-test confirmed; labelling 0.879
Input 2: COMPLETED — all three Seurat v5 default claims exactly right
Input 3: COMPLETED — 12,521 NaN logFCs, no exception; specificity filter rejected the batch split
Input 4: COMPLETED — the Skill's own snippet sums normalized values
Input 5: COMPLETED — 13 false positives on a null contrast vs 0 for pseudobulk

── STEP 6: Output Evaluation ─────────────────────
         Basic  Specialized  Total  Assertions
Input 1:  37/40    55/60    92/100   4/4 PASS
Input 2:  38/40    56/60    94/100   4/4 PASS
Input 3:  37/40    55/60    92/100   4/4 PASS
Input 4:  30/40    46/60    76/100   3/4 PASS
Input 5:  39/40    57/60    96/100   4/4 PASS
Execution Avg               : 90.0/100
Total Assertion Pass Rate   : 19/20 (95 %)

Research Veto (Category 3 — applicable)
Scientific Integrity  : PASS
Practice Boundaries   : PASS
Methodological Ground : PASS
Code Usability        : PASS — 5/5 executed; every block runs. The pseudobulk snippet produces
                        the wrong kind of matrix, which is a correctness P1, not unrunnable code.

── STEP 8: Final Score ───────────────────────────
Static Score   : 84/100   × 40% = 33.6
Dynamic Score  : 90.0/100 × 60% = 54.0
FINAL SCORE    : 88 / 100
GRADE BY SCORE : ⭐ Production Ready
```

## Floors check (scoring_rubric.md § 5)

| Component | Floor for ⭐ | Observed | Held? |
|---|---|---|---|
| Static Score | ≥ 80 | 84 | ✅ |
| Execution Average | ≥ 85 | 90.0 | ✅ |
| Layer 1 avg (/40) | ≥ 32 | 36.2 | ✅ |
| Layer 2 avg (/60) | ≥ 48 | 53.8 | ✅ |
| Assertion pass rate | ≥ 90 % | 95.0 % | ✅ |

**All five floors held.**

**GRADE AFTER FLOORS: ⭐ Production Ready (score 88, deployable).**

## Shipped-means-present (gate 8)

No `references/`, `scripts/`, `assets/` or `templates/` pointers in `SKILL.md` or `usage-guide.md`.
`examples/find_markers_scanpy.py` compiles and `examples/find_markers_seurat.R` parses. No P0.

## Research scope (gate 7)

Research only; markers and labels attached to clusters of barcodes, no individual diagnosed,
prescribed for or triaged. M2 PASS.

## Recommendations

```
[P1] The Python pseudobulk snippet sums normalized values, against the Skill's own rule (Input 4)
[P2] No Common Errors row for a non-integer pseudobulk matrix                      (Input 4)
[P2] Canonical NK and CD8 panels overlap and the table does not say so             (Input 1)
[P2] The 24-versus-25 control-bin claim could not be verified               (Inputs 1, 2)
[P2] No guidance on what to report                                          (Inputs 1, 2)
```

Full problem / root cause / fix text for each is in the JSON.

**Deployable: yes** (Production Ready, no veto, no open P0).
**Supporting-Skill note:** `final.score` = 88 with all floors held. The single P1 is a one-argument
fix (`layer='counts'`) and it sits on the hand-off path to `bio-differential-expression-deseq2-basics`,
so it is the highest-value fix in this Skill and matters to the Specialist's central workflow.
