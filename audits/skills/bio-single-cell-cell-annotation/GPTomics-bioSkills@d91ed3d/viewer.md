> **Audit record for `bio-single-cell-cell-annotation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/single-cell/cell-annotation) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-cell-annotation

Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:single-cell/cell-annotation`
Category: 3 — Data Analysis | Mode: A | Complexity: Moderate → N = 5

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | yes | 37 | 56 | 93 | 3/4 PASS | ✅ |
| 2 | Variant A | yes | 35 | 55 | 90 | 3/4 PASS | ✅ |
| 3 | Edge | yes | 36 | 53 | 89 | 3/4 PASS | ✅ |
| 4 | Variant B | yes | 36 | 54 | 90 | 4/4 PASS | ✅ |
| 5 | Stress | yes | 32 | 48 | 80 | 3/4 PASS | ✅ |

**Execution Average: 88.4 / 100**
**Assertion Pass Rate: 16/20 (80 %)**
**Executed inputs: 5/5**

Data: the SYNTHETIC 8-sample PBMC set (ground-truth cell types, doublet and low-quality labels) for
inputs 1, 2, 3 and 5; the **real** public 10x PBMC 1k v3 run for input 4, because `pbmcref` is a
curated real-PBMC atlas. No derived datasets were needed, so this audit has no `data/` folder.

---

## Detailed Outputs

### Input 1 — Canonical

**Prompt:** "6,000 PBMCs from eight donors, already clustered. Give me cell-type labels I can put in a
figure, and tell me which cells I shouldn't trust."

**Response.** SKILL.md:61-77 verbatim — restore raw counts, CP10K + `log1p`, `celltypist.annotate`
with `majority_voting=True` over the existing Leiden clustering, then `conf_score < 0.5` as the
uncertainty flag. Then tested the Skill's own headline silent-failure claim by re-running the same
model on three wrong inputs. Code in `run/input1.py`.

**What ran and what it printed** (`run/input1.log`):

```
celltypist 1.7.1 | 6049 cells | 15 Leiden clusters for majority voting

CORRECT input (CP10K log1p): 8 distinct labels, 2186 cells below conf_score 0.5 (36.1%)
  Tcm/Naive helper T cells 2132 | Classical monocytes 1184 | Tem/Trm cytotoxic T 726
  B cells 706 | CD16+ NK cells 557 | Non-classical monocytes 352 | DC 250 | Mk/platelets 142

  per-cell lineage accuracy vs truth:        0.892
  majority-voted lineage accuracy vs truth:  1.000
        B   DC   Mk  Mono   NK     T
  B   706    0    0     0    0     0
  DC    0  250    0     0    0     0
  Mk    0    0  142     0    0     0
  Mono  0    0    0  1536    0     0
  NK    0    0    0     0  557     0
  T     0    0    0     0    0  2858

SILENT-FAILURE TEST:
  CP10K log1p (correct)                 accuracy 0.892  mean max-prob 0.644  ERROR: no
  raw counts, no normalization          ERROR RAISED: ValueError: Invalid expression matrix in `.X`,
                                        expect log1p normalized expression to 10000 counts per cell
  log1p of raw counts, no CP10K         accuracy 0.842  mean max-prob 0.384  ERROR: no
  median-normalized log1p (scanpy default) accuracy 0.882  mean max-prob 0.379  ERROR: no
```

**Findings.** `majority_voting` is the Skill's central recommendation for CellTypist and it earns it:
per-cell lineage accuracy 0.892 became **1.000** after voting, a perfectly diagonal 6×6 crosstab
against the injected truth. That is the strongest single tool recommendation validated anywhere in
this candidate's Skill set.

The silent-failure claim needs updating in two directions at once. celltypist 1.7.1 now **refuses**
raw counts with a hard `ValueError`, so the Skill's "no error" is wrong for the case it names. But
the two subtler wrong inputs — `log1p` without CP10K, and scanpy's default median normalization —
do pass silently, and they are the ones a careful analyst is more likely to hit. Their accuracy loss
is small (0.842 and 0.882) but mean max-probability nearly halves (0.38 against 0.64), so the
confidence score *does* signal the problem — which again contradicts the Skill's "confident but
degraded" wording. The requirement is right; the described symptom is wrong twice over.

**Scores:** Basic 37/40 | Specialized 56/60 (Meth 19, Code 14, Data QC 9, Repro 9, Security 5) | **Total 93/100**
**Assertions:** 3/4 — FAIL on the stated wrong-input symptom.

---

### Input 2 — Variant A

**Prompt:** "Everything downstream is R and I don't have a Python environment. Annotate these PBMCs
against a public reference and tell me which calls to throw away."

**Response.** SKILL.md:85-101: build the SCE, fetch `celldex::HumanPrimaryCellAtlasData()`, run
`SingleR` with `de.method='classic'` and `fine.tune=TRUE`, take `pruned.labels` as the rejection set,
inspect the delta distribution. Ran `de.method='wilcox'` as the comparison the Skill's guidance
implies. Code in `run/input2.R`.

**What ran and what it printed** (`run/input2.log`):

```
SingleR 2.8.0 | celldex 1.16.0 | 3023 cells
reference: 19363 genes x 713 samples; 36 main labels
logcounts present in the SCE handed to SingleR: TRUE

de.method=classic   12.9s  lineage accuracy 0.906 | pruned to NA: 15 (0.5%) | accuracy among kept 0.908
  confusion (rows = truth, cols = SingleR):
              B   Mk Mono   NK  CMP  HSC    T
     B      358    0    0    0    0    1    0
     DC      59    0   75    0    0    0    0
     Mk       0   65    2    0    1    0    0
     Mono   110    0  686    0    0    0    0
     NK       0    0    0  170    0    0    1
     T       10    0    0   26    0    0 1458
  delta.next: median 0.0934, IQR 0.0636-0.1468; pruneScores(nmads=3) flags 0 cells

de.method=wilcox    47.8s  lineage accuracy 0.534 | pruned to NA: 44 (1.5%) | accuracy among kept 0.541
```

**Findings.** The `de.method` rule is one line in the Skill and it is worth a great deal: on a bulk
reference, `classic` gave 0.906 lineage accuracy in 12.9 s where `wilcox` gave 0.534 in 47.8 s.
An agent that ignored that line would have produced an annotation that is wrong for half the cells,
four times slower, with no error.

The rejection machinery is the weak half. `pruned.labels` removed 15 of 3,023 cells and
`pruneScores(nmads=3)` removed none, while the confusion table shows 110 monocytes and 59 dendritic
cells confidently placed in `B_cell`. Accuracy among the retained cells (0.908) is no better than
overall (0.906) — the rejection set carries no information about the errors that actually happened.
This is consistent with what delta-based pruning measures (best vs second-best score ambiguity), but
the Skill presents it as the guard against exactly the closed-world errors it does not catch. The
Skill's own marker-triangulation step would have caught the monocyte→B_cell block instantly.

**Scores:** Basic 35/40 | Specialized 55/60 (Meth 18, Code 14, Data QC 9, Repro 9, Security 5) | **Total 90/100**
**Assertions:** 3/4 — FAIL on the rejection mechanism.

---

### Input 3 — Edge

**Prompt:** "My h5ad came out of a pipeline that kept Ensembl IDs as the gene names. CellTypist gave
me labels but they look odd — how much should I trust them?"

**Response.** Ran CellTypist both ways on the same 2,000 cells and measured the model-gene overlap
before looking at any label. Code in `run/input3.py`.

**What ran and what it printed** (`run/input3.log`):

```
gene SYMBOLS (correct):
  lineage accuracy 0.899 | mean max-probability 0.644 | 32 distinct labels
  genes in the model that matched the query: 3931/6639 (59.2%)
  is that fraction reported by annotate()?  no such attribute
  [celltypist stdout: "Matching reference genes in the model" / "3931 features used for prediction"]

Ensembl IDs (the trap):
  HARD ERROR RAISED: ValueError: No features overlap with the model. Please provide gene symbols
  genes in the model that matched the query: 0/6639
```

**Findings.** The Skill's *fix* is exactly right — set `var_names` to gene symbols and everything
works (3,931 matched genes, 0.899 lineage accuracy). Its *symptom* is wrong: celltypist 1.7.1 does
not return confident nonsense, it raises. The practical consequence is small but real — an agent
told to watch for "nonsensical labels" will not recognise this error when it arrives, and the Common
Errors table is the place it would look.

The Skill's instruction to "check the matched-gene fraction reported by annotate" is half true in
1.7.1: the count is printed to stdout but is not an attribute of the returned object, so an agent can
read it in a log but cannot gate on it programmatically. Worth noting because 59.2% overlap on a
perfectly ordinary query is lower than most users would guess.

**Scores:** Basic 36/40 | Specialized 53/60 (Meth 17, Code 13, Data QC 9, Repro 9, Security 5) | **Total 89/100**
**Assertions:** 3/4 — FAIL on the stated symptom.

---

### Input 4 — Variant B

**Prompt:** "This is a standard 10x PBMC run and there's a Seurat reference atlas for exactly that.
Use it, give me the finest labels it supports, and flag anything that mapped badly."

**Response.** SKILL.md:109-116 verbatim on the **real** 10x PBMC 1k v3 dataset:
`RunAzimuth(seurat_obj, reference='pbmcref')`, take `predicted.celltype.l2`, gate at score < 0.7,
then triangulate with the canonical marker DotPlot from SKILL.md:155-158. Code in `run/input4.R`.

**What ran and what it printed** (`run/input4.log`):

```
Azimuth 0.5.1 | Seurat 5.5.0 | REAL 10x PBMC 1k v3: 1176 cells
RunAzimuth took 41 s
metadata columns added: predicted.celltype.l1/.l2/.l3 (+ .score each), mapping.score
SKILL.md:114-115 column names resolve: TRUE

predicted.celltype.l1: Mono 360 | CD4 T 313 | B 193 | CD8 T 114 | other T 88 | NK 55 | DC 27 | other 26
predicted.celltype.l2 (top): CD14 Mono 328 | CD4 TCM 230 | B naive 127 | MAIT 66 | CD4 Naive 63 ...

low-confidence cells at the Skill's 0.7 gate: 257/1176 (21.9%)
mapping.score: median 0.982, 5% quantile 0.860; cells below 0.5: 0
prediction.score.l2 vs mapping.score correlation: 0.384

mean normalized expression by predicted.celltype.l1:
          B CD4 T CD8 T   DC Mono   NK
CD3D   0.02  1.68  1.82 0.03 0.02 0.04
MS4A1  2.28  0.02  0.04 0.02 0.01 0.02
CD14   0.01  0.01  0.00 0.12 1.70 0.00
FCER1A 0.00  0.01  0.00 1.56 0.10 0.00
NKG7   0.03  0.02  1.33 0.24 0.11 4.01
```

**Findings.** Clean pass on real data. Every metadata column the Skill hard-codes exists; the marker
triangulation shows the expected on/off pattern on all seven canonical genes; and the Skill's
"calibrate, do not port" instruction is vindicated concretely — its own suggested 0.7 gate flags
21.9% of cells while `mapping.score` flags none, and the two scores correlate at only 0.384. They are
measuring different things (how confident the label is, versus how well the cell sits in the
reference manifold), and an analyst who used either alone would reach a different conclusion about
data quality.

One small defect: the validation snippet's `DotPlot` runs on the object `RunAzimuth` returns, whose
RNA `data` layer is empty, and Seurat silently falls back with "data layer is not found and counts
layer is used" — so the plot is built from raw counts. The snippet needs `NormalizeData` above it.

**Scores:** Basic 36/40 | Specialized 54/60 (Meth 18, Code 13, Data QC 9, Repro 9, Security 5) | **Total 90/100**
**Assertions:** 4/4 PASS.

---

### Input 5 — Stress

**Prompt:** "At resolution 1.5 I get a handful of clusters where nothing in the reference fits well.
One of them might be a transitional state nobody's described in PBMC. Work out which of them are real
before I get excited."

**Response.** Ran the Skill's four-way triage (SKILL.md:135-144) verbatim on a version of the dataset
that still contains its injected doublets and low-quality cells, then scored the triage against those
labels. Code in `run/input5.py`.

**What ran and what it printed** (`run/input5.log`, abridged to the rows that matter):

```
6524 cells INCLUDING 195 injected doublets and 290 low-quality cells; 20 clusters

SKILL triage block ran. clusters with median conf_score < 0.5: ['2','6','8','10','13','16']

leiden  pct_mt  n_genes  scrublet  batch_purity  median_conf     n  TRUE_doublet  TRUE_lowq
10       2.57      962     0.010         0.268        0.245   384        0.034      0.003
8        2.84      937     0.005         0.315        0.273   365        0.027      0.000
16       3.57     1559     0.000         0.276        0.278   152        0.039      0.072
13       2.14      933     0.000         0.267        0.315  1113        0.009      0.000
6        2.69     1682     0.000         0.298        0.369   124        0.073      0.000
2        2.41      901     0.002         0.272        0.437  1042        0.012      0.000
11      21.07      432     0.000         0.181        0.593   160        0.006      1.000
7       18.09      786     0.222         0.222        0.724    81        0.284      0.728
1        2.52     1451     0.444         0.222        0.884     9        1.000      0.000
15      22.15      395     0.034         0.241        0.973    29        0.000      1.000

dataset baseline: 3.0% doublets, 4.4% low-quality
  clusters 2, 6, 8, 10, 13, 16: triage flags ['none -> novel candidate'] in every case
```

**Findings.** This is the most consequential result in the audit, and it is a self-contradiction
inside the Skill.

The screening step — *median `conf_score` < 0.5 marks a cluster suspect* — selected six clusters,
**all of which are ordinary**: true doublet fractions 0.9–7.3% against a 3.0% baseline, low-quality
0–7.2% against 4.4%. They score low because `Immune_All_Low` has many fine T-cell subtypes competing
for the same cells, not because anything is wrong with them.

Meanwhile the four clusters that *are* artifacts all scored **above** the gate: cluster 1 (100% true
doublets) at median confidence 0.884, cluster 15 (100% low-quality, 22% mito) at 0.973, cluster 11
(100% low-quality, 21% mito) at 0.593, and cluster 7 (28% doublets, 73% low-quality, 18% mito) at
0.724. Sensitivity 0/4, precision 0/6.

The reason is written in the Skill's own Governing Principle: a state the reference does not contain
"gets the nearest wrong label — often with high apparent confidence". Dying cells and doublets are
exactly such states, so they are labelled confidently. Screening on low confidence therefore selects
against the thing it is looking for.

The second half of the triage is fine. The QC columns the same code block computes separate the
artifacts perfectly — 21–22% mito against a 2.5% baseline, scrublet rates 0.44 and 0.22 against
~0.02 — so the fix is to make those the screen and demote confidence to a secondary signal.

The response itself reached the right answer (no novel population claimed, six low-confidence
clusters attributed to fine-granularity T ambiguity, artifact clusters identified from QC), but it
got there by reading the whole table rather than by following the Skill's screening rule.

**Scores:** Basic 32/40 | Specialized 48/60 (Meth 14, Code 12, Data QC 9, Repro 8, Security 5) | **Total 80/100**
**Assertions:** 3/4 — FAIL on the screening step.

---
---

# STEP 8 — Optimization Report

```
══════════════════════════════════════════════════
SKILL AUDIT REPORT
══════════════════════════════════════════════════
Skill Name     : bio-single-cell-cell-annotation
Category       : Data Analysis (3)
Execution Mode : A
Complexity     : Moderate (N = 5)
Audited On     : 2026-09-16
Executed       : 5/5 inputs

── STEP 1: Structural Veto ───────────────────────
Stability    : PASS
Contract     : PASS
Determinism  : PASS — CellTypist, SingleR and Azimuth are all deterministic; the only
                      stochastic dependency is the over-clustering majority_voting needs,
                      which the Skill does not create or seed (Idempotency 3).
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
  functional_suitability 11 → 10 (Correctness 3 → 2). Three prescribed things produce the
    wrong result on current tool versions: two "wrong input symptom" cells and, more
    seriously, the triage screening step, which had 0/4 sensitivity on labelled artifacts.
  reliability 10 → 9. The draft credited the normalization table as preventing silent
    failures. Its requirement column does; its symptom column — what an agent watches for —
    is wrong for the primary tool in two of four rows.
  The six other categories were verified against the files and left at the draft value.

── STEP 3: Classification ────────────────────────
Category       : Data Analysis
Execution Mode : A

── STEP 4: Test Inputs ───────────────────────────
1 Canonical : label 6,000 clustered PBMCs and say which calls not to trust
2 Variant A : R-only lab, public reference, which calls to throw away
3 Edge      : query whose gene names are Ensembl IDs
4 Variant B : real 10x PBMC run with a matching curated atlas
5 Stress    : "one of these low-confidence clusters might be a new transitional state"

── STEP 5: Execution Summary ─────────────────────
Input 1: COMPLETED — majority_voting reached 1.000 lineage accuracy
Input 2: COMPLETED — de.method guidance verified (0.906 vs 0.534)
Input 3: COMPLETED — hard ValueError, not the silent failure the Skill describes
Input 4: COMPLETED — Azimuth ran on real data; all hard-coded columns resolve
Input 5: COMPLETED — triage screen 0/4 sensitivity, 0/6 precision

── STEP 6: Output Evaluation ─────────────────────
         Basic  Specialized  Total  Assertions
Input 1:  37/40    56/60    93/100   3/4 PASS
Input 2:  35/40    55/60    90/100   3/4 PASS
Input 3:  36/40    53/60    89/100   3/4 PASS
Input 4:  36/40    54/60    90/100   4/4 PASS
Input 5:  32/40    48/60    80/100   3/4 PASS
Execution Avg               : 88.4/100
Total Assertion Pass Rate   : 16/20 (80 %)

Research Veto (Category 3 — applicable)
Scientific Integrity  : PASS
Practice Boundaries   : PASS
Methodological Ground : PASS
Code Usability        : PASS — 5/5 executed; every prescribed block runs as printed. The
                        defects are in what the code concludes, not whether it runs.

── STEP 8: Final Score ───────────────────────────
Static Score   : 86/100   × 40% = 34.4
Dynamic Score  : 88.4/100 × 60% = 53.0
FINAL SCORE    : 87 / 100
GRADE BY SCORE : ⭐ Production Ready
```

## Floors check (scoring_rubric.md § 5)

| Component | Floor for ⭐ | Observed | Held? |
|---|---|---|---|
| Static Score | ≥ 80 | 86 | ✅ |
| Execution Average | ≥ 85 | 88.4 | ✅ |
| Layer 1 avg (/40) | ≥ 32 | 35.2 | ✅ |
| Layer 2 avg (/60) | ≥ 48 | 53.2 | ✅ |
| Assertion pass rate | ≥ 90 % | 80 % | ❌ |

One floor missed → **downgrade exactly one tier**.

**GRADE AFTER FLOORS: ✅ Limited Release (score 87, deployable).**
The § 4 safety-assertion rule does **not** fire: all four scope/safety assertions (inputs 1, 2, 4, 5)
passed, and no output made a claim outside the Skill's remit. The four failures are content
assertions — two stale symptom descriptions and two rejection/screening mechanisms that do not catch
what they are advertised to catch.

## Shipped-means-present (gate 8)

No `references/`, `scripts/`, `assets/` or `templates/` pointers in `SKILL.md` or `usage-guide.md`;
`examples/` is present for both ecosystems. Nothing promised is missing. No P0.

## Research scope (gate 7)

Research only. Labels are attached to barcodes in donor-pooled matrices; no individual is diagnosed,
prescribed for or triaged. M2 PASS.

## Recommendations

```
[P1] The triage screens on the one signal artifacts do not trip            (Input 5)
[P2] Two "wrong input" symptoms are stale for current tool versions     (Inputs 1, 3)
[P2] SingleR's rejection set is presented as a safety net it is not        (Input 2)
[P2] The marker-validation snippet assumes a normalized object it is not given (Input 4)
[P2] majority_voting's over-clustering is neither created nor seeded     (Inputs 1, 5)
```

Full problem / root cause / fix text for each is in the JSON.

**Deployable: yes** (Limited Release, no veto, no open P0).
**Core-Skill note:** `final.score` = 87, clearing gate 3. The P1 is a two-line change to the triage
block and is the highest-value fix identified for this Skill.
