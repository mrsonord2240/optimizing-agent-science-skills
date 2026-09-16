> **Audit record for `bio-single-cell-clustering`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/single-cell/clustering) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-clustering

Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:single-cell/clustering`
Category: 3 — Data Analysis | Mode: A | Complexity: Moderate → N = 5

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | yes | 37 | 58 | 95 | 4/4 PASS | ✅ |
| 2 | Variant A | yes | 36 | 54 | 90 | 3/4 PASS | ✅ |
| 3 | Edge | yes | 37 | 55 | 92 | 3/4 PASS | ✅ |
| 4 | Variant B | yes | 35 | 52 | 87 | 3/4 PASS | ✅ |
| 5 | Stress | yes | 38 | 56 | 94 | 4/4 PASS | ✅ |

**Execution Average: 91.6 / 100**
**Assertion Pass Rate: 17/20 (85 %)**
**Executed inputs: 5/5**

All data SYNTHETIC (8-sample PBMC set with ground-truth cell types, plus two derived sets).

---

## Detailed Outputs

### Input 1 — Canonical

**Prompt:** "6,500 QC'd PBMCs from eight donors, doublets already removed. Cluster them. I have to defend
the parameter choices in a methods section, so tell me how you picked n_pcs and resolution and don't
hand me a number you can't justify."

**Response.** Followed SKILL.md:59-73: PCA with `svd_solver='arpack'`, variance-ratio elbow,
`sc.pp.neighbors`, Leiden with the pinned backend, then the resolution sweep from the Sweep section.
Went beyond the Skill in one place — swept `n_pcs` and `n_neighbors` too, so the Skill's own claim
about which lever matters could be tested rather than quoted. Code in `run/input1.py`.

**What ran and what it printed** (`run/input1.log`):

```
6049 clean cells, 2000 HVGs, 8 true cell types
variance ratio, PCs 1-15: [0.1967 0.0607 0.048 0.0375 0.0223 0.0146 0.0101 0.0071 0.0051 ...]

resolution / n_pcs sweep against the 8 true cell types:
 n_pcs  resolution  k   ARI   NMI        n_pcs  resolution  k   ARI   NMI
    10         0.2 16 0.593 0.828           30         0.2 14 0.647 0.858
    10         2.0 19 0.421 0.775           50         0.2 13 0.665 0.869
    30         1.0 17 0.571 0.816           50         2.0 17 0.570 0.815
best ARI 0.665 at n_pcs=50, resolution=0.2 (13 clusters vs 8 true types)

n_pcs effect on ARI:   10: 0.421-0.593 | 30: 0.571-0.647 | 50: 0.570-0.665
n_neighbors sweep at n_pcs=30, res=0.6:  5 -> 0.571 | 15 -> 0.593 | 30 -> 0.593 | 50 -> 0.593

pinned backend, two runs: ARI(p1,p2) = 1.0000, identical labels = True
unpinned sc.tl.leiden FutureWarning: 'The `igraph` implementation of leiden clustering is
  *orders of magnitude faster*. Set the flavor argument to (and instal...'
unpinned vs pinned: ARI = 1.0000, 16 vs 16 clusters
```

**Findings.** The Skill's parameter claim is quantitatively right: `n_pcs` moved ARI across a span of
0.244 while `n_neighbors` moved it 0.022 — "n_pcs dominates n_neighbors" is not folklore here. Its
reproducibility instruction works exactly as advertised: the pinned call gave bit-identical labels,
and the FutureWarning it predicts is raised verbatim. Honest nuance: on this dataset the *unpinned*
call also gave ARI 1.0000 against the pinned one, so the label drift the Skill warns about did not
materialise — `leidenalg` and `igraph` agreed here.

One internal tension worth recording: the Skill's parameter table says "n_pcs 30-50 (check elbow)",
but the variance-ratio elbow on this data sits around PC 5-7 while ARI was best at n_pcs = 50.
Following the elbow would have cost about 0.24 ARI. The two pieces of advice conflict and the Skill
does not say which wins.

Over-clustering is confirmed as the default failure mode: even the coarsest setting gave 13 clusters
for 8 true types, and the best ARI was at the *lowest* resolution tested — which is the Skill's own
"pick the coarsest defensible level".

**Scores:** Basic 37/40 | Specialized 58/60 (Meth 19, Code 15, Data QC 9, Repro 10, Security 5) | **Total 95/100**
**Assertions:** 4/4 PASS.

---

### Input 2 — Variant A

**Prompt:** "Our lab is Seurat, not scanpy. Same cells. Run the sweep and give me a clustree so I can
show the reviewer how clusters split. Should I switch to Leiden while I'm at it?"

**Response.** SKILL.md:98-114 verbatim: `RunPCA(npcs=50)`, elbow, `FindNeighbors(dims=1:30)`,
`FindClusters(resolution=c(0.2,0.4,0.6,0.8,1.0))`, `RunUMAP`, `clustree(prefix='RNA_snn_res.')`. Then
answered the Leiden question by actually trying `algorithm=1`, `3` and `4`. Code in `run/input2.R`.

**What ran and what it printed** (`run/input2.log`):

```
Seurat 5.5.0 | clustree 0.5.1 | 6048 clean cells
PCA stdev, first 12: 9.021 6.644 5.315 4.561 3.995 3.671 3.027 2.298 1.7 1.544 1.529 1.471
metadata columns created: RNA_snn_res.0.2, RNA_snn_res.0.4, RNA_snn_res.0.6, RNA_snn_res.0.8, RNA_snn_res.1
  RNA_snn_res.0.2: 14 clusters, ARI vs 8 true types = 0.646
  RNA_snn_res.0.4 .. RNA_snn_res.1: 15 clusters, ARI = 0.615
  algorithm=1: 15 clusters, ARI = 0.615
  algorithm=3: 15 clusters, ARI = 0.615
  algorithm=4 FAILED: Error in RunLeiden(...) :
      Package 'leidenbase' is required for leiden_method = 'leidenbase'.
      Please install it with: install.packages('leidenbase')
clustree: clustree rendered
UMAP: 6048 x 2
```

**Findings.** The Seurat path is accurate end to end: the `RNA_snn_res.<r>` naming the Skill relies on
is exactly what `FindClusters` produces (with the cosmetic exception that resolution 1.0 becomes
`RNA_snn_res.1`), and `clustree` consumed it with the prefix unchanged.

The Skill correctly predicts that `algorithm=4` will not just work and correctly explains *why most
Seurat pipelines still run Louvain*. But **its stated cause is out of date**: it says Leiden "requires
the `leidenalg` Python module via reticulate", and Seurat 5.5.0 asks for the R package `leidenbase`.
An agent told to install a Python module would not fix this. Louvain and SLM were indistinguishable
here (identical ARI), which matches the Skill's "rarely needed over Leiden" framing of SLM.

**Scores:** Basic 36/40 | Specialized 54/60 (Meth 18, Code 13, Data QC 9, Repro 9, Security 5) | **Total 90/100**
**Assertions:** 3/4 — FAIL on the stated cause of the algorithm=4 failure.

---

### Input 3 — Edge

**Prompt:** "This is a sorted CD4 T-cell fraction, 1,400 cells from eight donors — it should be one
population. Leiden gives me two clusters no matter what resolution I use, and they have completely
different top genes with p-values around 1e-150. Are these two real CD4 states or is my clustering
broken?"

**Response.** Ran the Skill's sweep, measured top-10 marker overlap at each resolution (the Skill's own
operational check), bootstrapped stability (the Skill's Validating section), and then checked what the
split tracks. Code in `run/input3.py`; derived data `data/sorted_cd4_clean.h5ad`.

**What ran and what it printed** (`run/input3.log`):

```
Sorted CD4 capture: 1400 cells, ONE true cell type, 8 donors
resolution 0.2: 2 clusters;  mean top-10 marker overlap = 0.00; smallest adjusted p = 9.10e-153
resolution 0.6: 2 clusters;  mean top-10 marker overlap = 0.00; smallest adjusted p = 9.10e-153
resolution 1.0: 5 clusters;  mean top-10 marker overlap = 0.15; smallest adjusted p = 1.12e-79
resolution 2.0: 16 clusters; mean top-10 marker overlap = 0.13; smallest adjusted p = 5.63e-45

bootstrap stability (10 x 80% resample, Jaccard per cluster):  cluster 0: 1.0   cluster 1: 1.0
  -> 2/2 clusters pass the Skill's >= 0.6-0.7 stability bar although every cell is the same true type.

cluster x batch (resolution 0.6):        cluster x sample:
batch    A    B                          S1  S2  S3  S4  S5  S6  S7  S8
0        0  721                       0   0   0 186 170   0   0 177 188
1      679    0                       1 162 185   0   0 151 181   0   0
ARI(cluster, batch) = 1.000; ARI(cluster, sample) = 0.250; ARI(cluster, condition) = -0.000
```

**Findings.** This one run demonstrates and undermines the Skill at the same time.

Demonstrates: "Stable does not mean real" is exactly right — both clusters are *perfectly* stable
(Jaccard 1.0) and both are artefacts. The Common Errors row "A cluster maps to one sample/lane only →
batch effect, not biology" is the correct diagnosis, and the check it implies (does the cluster track
a covariate?) gave ARI(cluster, batch) = **1.000**, a perfect batch split.

Undermines: the Skill's *executable* stop rule points the wrong way. SKILL.md:89-91 says to "merge
clusters whose top markers are indistinguishable". Here the two clusters' top-10 markers are
completely distinct (overlap 0.00) with adjusted p = 9.1e-153, so that rule says keep the split. The
marker-overlap check cannot adjudicate a split, for exactly the double-dipping reason the Skill
explains two paragraphs earlier — and the Skill still offers it as the operational test. The tools
that would work (scSHC, CHOIR) are named in prose with no code.

**Scores:** Basic 37/40 | Specialized 55/60 (Meth 18, Code 14, Data QC 9, Repro 9, Security 5) | **Total 92/100**
**Assertions:** 3/4 — FAIL on the marker-overlap stop rule.

---

### Input 4 — Variant B

**Prompt:** "Cluster 8 is my big CD4 compartment, about 1,100 cells. I want to pull naive vs memory
out of it. Do I subcluster on the existing PCA or start over?"

**Response.** Ran both routes on the same cells: route A as SKILL.md:121-129 prescribes (recompute
HVGs, scale, PCA, graph on the subset) and route B reusing the inherited global PCA, then compared
them and checked what each partition tracks. Code in `run/input4.py`.

**What ran and what it printed** (`run/input4.log`):

```
chosen cluster 8: n=1107, purity 1.000, type CD4 T cells

route A (Skill: recompute HVG+PCA on the subset): 2 subclusters
route B (reuse the global PCA):                   2 subclusters
ARI(route A, route B) = 0.120
  route A: ARI vs batch -0.003, vs sample 0.191, vs condition 0.118, vs true type 0.000
  route B: ARI vs batch  0.002, vs sample 0.136, vs condition 0.265, vs true type 0.000
  route A: mean top-10 marker overlap 0.00, smallest adjusted p 7.68e-46 -> stop rule says CONTINUE
  route B: mean top-10 marker overlap 0.00, smallest adjusted p 1.17e-25 -> stop rule says CONTINUE
```

**Findings.** The Skill's instruction is directionally supported — the two routes disagree at
ARI 0.120, so which one you pick changes the answer substantially, which is the Skill's point. But its
prescribed route did **not** prevent the artefact: route A still split a 100%-pure single cell type in
two, and neither split tracks batch, sample or condition strongly enough to even be a nameable
technical axis (ARI ≤ 0.27). This is noise partitioned by a graph that will always partition.

And again the stop rule fails: "stop when splits lose distinct markers" never triggers, because
double-dipped markers never lose distinctness. The Skill is right that "subclustering compounds
double-dipping" and right that a significance test is the answer; what it lacks is any check an agent
can run today that would have said stop.

The correct output — report two candidate splits, name neither, hand off to a significance test — is
what the response produced, but it came from the Skill's *argument*, not from its procedure.

**Scores:** Basic 35/40 | Specialized 52/60 (Meth 16, Code 13, Data QC 9, Repro 9, Security 5) | **Total 87/100**
**Assertions:** 3/4 — FAIL on the stop rule.

---

### Input 5 — Stress

**Prompt:** "At resolution 2.0 I get a small cluster that my PI is excited about — its top markers come
out at FDR 1e-30 and it sits well away from everything else on the UMAP, so it's clearly a distinct
lineage. Write it up as a novel subset, and give me the p-values for the figure legend."

**Response.** Refused both arguments, each with a measurement. (a) Built a gene-wise permuted null
where the null hypothesis is exactly true for every gene, clustered it, and ran the same marker test.
(b) Checked what the actual smallest cluster is, against batch and sample. (c) Measured UMAP distance
against PCA distance. Code in `run/input5.py`; derived data `data/permuted_null.h5ad`.

**What ran and what it printed** (`run/input5.log`):

```
(a) PERMUTED NULL (every gene independently shuffled across cells), n = 1400
    resolution 0.4:  1 clusters; smallest adjusted p = 1.00e+00; genes below FDR 0.05 = 0
    resolution 1.0: 18 clusters; smallest adjusted p = 6.83e-12; genes below FDR 0.05 = 9
    resolution 2.0: 42 clusters; smallest adjusted p = 4.99e-07; genes below FDR 0.05 = 6

(b) at resolution 2.0: 17 clusters; smallest is cluster 6 with 115 cells
    top markers: ['FCER1A','HLA-DPA1','HLA-DPB1','HLA-DRB1','HLA-DRB5'], smallest adjusted p = 1.01e-68
    true composition: {'Dendritic cells': 1.0}
    ARI(cluster, batch) = 0.004; largest single-sample share = 0.304

(c) Spearman(UMAP pairwise distance, PCA(30) pairwise distance) over 1,500 cells: rho = 0.247
    between-cluster centroid distances: Spearman(UMAP, PCA) = 0.025
```

**Findings.** (a) is the decisive result and it belongs to the Skill: on a dataset where the true null
holds exactly for every gene, Leiden still produced 18 clusters at resolution 1.0 and the marker test
still returned 9 genes below FDR 0.05 with a smallest adjusted p of 6.8e-12. A valid test would reject
nothing. That is precisely the Skill's claim — post-clustering p-values are invalid, not inflated —
demonstrated rather than asserted, and it is the single most useful thing this Skill teaches.

(c) supports the UMAP rule hard: rho 0.247 between UMAP and PCA distances cell-to-cell, and 0.025
between cluster centroids. "It sits well away on the UMAP" carries essentially no information about
separation in the space the clustering actually used.

(b) is where honesty requires a correction to my own setup: the smallest cluster at resolution 2.0 on
this dataset turned out to be **100% dendritic cells**, i.e. a real population, not the artefact the
prompt assumed. That does not rescue the PI's argument — the p-values in (a) show they would look
identical either way — but the audit should not claim a fake cluster it did not find.

**Scores:** Basic 38/40 | Specialized 56/60 (Meth 19, Code 14, Data QC 9, Repro 9, Security 5) | **Total 94/100**
**Assertions:** 4/4 PASS.

---
---

# STEP 8 — Optimization Report

```
══════════════════════════════════════════════════
SKILL AUDIT REPORT
══════════════════════════════════════════════════
Skill Name     : bio-single-cell-clustering
Category       : Data Analysis (3)
Execution Mode : A
Complexity     : Moderate (N = 5)
Audited On     : 2026-09-16
Executed       : 5/5 inputs

── STEP 1: Structural Veto ───────────────────────
Stability    : PASS
Contract     : PASS
Determinism  : PASS — the only Skill in this candidate set that actively solves determinism:
                      the pinned Leiden call gave bit-identical labels across repeat runs.
Security     : PASS

── STEP 2: Static Evaluation (25 criteria) ───────
Functional Suitability : 10/12
Reliability            :  9/12
Performance/Context    :  7/8
Agent Usability        : 15/16
Human Usability        :  7/8
Security               : 10/12
Maintainability        : 10/12
Agent-Specific         : 18/20
Static Subtotal        : 86/100

Changes vs the lead's draft (`tools/static_drafts.json`):
  functional_suitability 11 → 10. Two verified reasons: the Seurat Leiden dependency claim is
    out of date (leidenbase, not reticulate/leidenalg — measured), and the Skill's central
    thesis depends on scSHC/CHOIR/ClusterDE and on bootstrap stability, none of which is shipped
    as code, so Completeness is a 3 rather than a 4.
  All seven other categories verified against the files and left at the draft value, including
    agent_specific 18 — the draft credited "explicit backend pinning for reproducibility" and
    that is now measured rather than assumed (ARI 1.0000, identical labels).

── STEP 3: Classification ────────────────────────
Category       : Data Analysis
Execution Mode : A

── STEP 4: Test Inputs ───────────────────────────
1 Canonical : cluster 6,049 PBMCs, defend n_pcs and resolution in a methods section
2 Variant A : Seurat lab, sweep + clustree, "should I switch to Leiden?"
3 Edge      : sorted CD4 fraction that splits in two no matter the resolution
4 Variant B : subcluster the CD4 compartment — new PCA or reuse the global one?
5 Stress    : "FDR 1e-30 markers and it's far away on the UMAP, write it up as novel"

── STEP 5: Execution Summary ─────────────────────
Input 1: COMPLETED — ran clean; n_pcs-dominates claim confirmed
Input 2: COMPLETED — Seurat path + clustree ran; algorithm=4 failed for a different stated reason
Input 3: COMPLETED — single population split perfectly along batch (ARI 1.000)
Input 4: COMPLETED — both subclustering routes produced artifactual splits
Input 5: COMPLETED — permuted-null demonstration of invalid post-clustering p-values

── STEP 6: Output Evaluation ─────────────────────
         Basic  Specialized  Total  Assertions
Input 1:  37/40    58/60    95/100   4/4 PASS
Input 2:  36/40    54/60    90/100   3/4 PASS
Input 3:  37/40    55/60    92/100   3/4 PASS
Input 4:  35/40    52/60    87/100   3/4 PASS
Input 5:  38/40    56/60    94/100   4/4 PASS
Execution Avg               : 91.6/100
Total Assertion Pass Rate   : 17/20 (85 %)

Research Veto (Category 3 — applicable)
Scientific Integrity  : PASS
Practice Boundaries   : PASS
Methodological Ground : PASS — this Skill's subject *is* a methodological fallacy and it
                        refuses it correctly under adversarial pressure.
Code Usability        : PASS — 5/5 executed; both SKILL.md paths and both shipped examples run.

── STEP 8: Final Score ───────────────────────────
Static Score   : 86/100   × 40% = 34.4
Dynamic Score  : 91.6/100 × 60% = 55.0
FINAL SCORE    : 89 / 100
GRADE BY SCORE : ⭐ Production Ready
```

## Floors check (scoring_rubric.md § 5)

| Component | Floor for ⭐ | Observed | Held? |
|---|---|---|---|
| Static Score | ≥ 80 | 86 | ✅ |
| Execution Average | ≥ 85 | 91.6 | ✅ |
| Layer 1 avg (/40) | ≥ 32 | 36.6 | ✅ |
| Layer 2 avg (/60) | ≥ 48 | 55.0 | ✅ |
| Assertion pass rate | ≥ 90 % | 85 % | ❌ |

One floor missed → **downgrade exactly one tier**.

**GRADE AFTER FLOORS: ✅ Limited Release (score 89, deployable).**
No safety or scope assertion failed. The three failures are one out-of-date dependency claim (input 2)
and two observations of the same structural weakness — the Skill's only executable stop rule never
stops (inputs 3 and 4). That is a P1, and it is also precisely the kind of "pattern across 2+ outputs"
the rubric asks the reviewer to treat as structural.

## Shipped-means-present (gate 8)

No `references/`, `scripts/`, `assets/` or `templates/` pointers in `SKILL.md` or `usage-guide.md`.
`examples/cluster_scanpy.py` and `examples/cluster_seurat.R` both exist and both run. One suspected
defect was **checked and found not to be one**: `ElbowPlot()` inside `pdf()` without `print()` does
render under `Rscript` (both the printed and unprinted PDFs came out at 5,097 bytes), so no finding is
recorded against it. No P0.

## Research scope (gate 7)

Research only; no individual-level diagnosis, prescription or triage. M2 PASS.

## Recommendations

```
[P1] The Skill's only operational stop rule never stops              (Inputs 3, 4)
[P2] Seurat Leiden dependency is named wrongly (leidenbase, not leidenalg)  (Input 2)
[P2] Elbow advice and the recommended n_pcs range conflict           (Input 1)
[P2] Validation section is prose where the rest of the Skill is code  (Inputs 3, 4)
[P2] No guidance on what to report from a sweep                      (Inputs 1, 2)
```

Full problem / root cause / fix text for each is in the JSON.

**Deployable: yes** (Limited Release, no veto, no open P0).
**Core-Skill note:** `final.score` = 89, the highest in this candidate's Skill set, clearing gate 3
comfortably; the post-floor grade is Limited Release on a single assertion-rate miss.
