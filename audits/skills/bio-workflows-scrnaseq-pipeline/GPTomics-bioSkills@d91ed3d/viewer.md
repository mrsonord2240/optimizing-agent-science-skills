> **Audit record for `bio-workflows-scrnaseq-pipeline`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/workflows/scrnaseq-pipeline) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-workflows-scrnaseq-pipeline

Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:workflows/scrnaseq-pipeline`
Category: 3 — Data Analysis | Mode: A | Complexity: Complex → N = 7

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | yes | 36 | 55 | 91 | 4/4 PASS | ✅ |
| 2 | Variant A | yes | 35 | 51 | 86 | 3/4 PASS | ✅ |
| 3 | Variant B | yes | 36 | 53 | 89 | 4/4 PASS | ✅ |
| 4 | Edge | yes | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 5 | Stress | yes | 39 | 55 | 94 | 4/4 PASS | ✅ |
| 6 | Scope Boundary | no (text) | 36 | 49 | 85 | 4/4 PASS | ✅ |
| 7 | Adversarial | yes | 37 | 53 | 90 | 4/4 PASS | ✅ |

**Execution Average: 89.9 / 100**
**Assertion Pass Rate: 27/28 (96.4 %)**
**Executed inputs: 6/7**

Data: the SYNTHETIC 8-sample PBMC set in Cell Ranger v3 layout (raw + filtered per sample, with
ground truth for cell type, doublets, low-quality cells, ambient rho and 55 DE genes), plus the
**real** public 10x PBMC 1k v3 run for input 4. See `data/README.md`.

---

## Detailed Outputs

### Input 1 — Canonical

**Prompt:** "Eight PBMC samples from Cell Ranger, four vehicle and four TLR7-agonist, one donor each,
two 10x runs. Take it from the `outs/` directories to annotated cell types. I want to be able to
defend the order of operations in the methods section."

**Response.** Followed the Skill's ordering rules rather than either code block, because the code
blocks are single-sample: per sample, SoupX on the **raw** matrix → MAD-adaptive QC → scDblFinder;
then merge, Harmony on batch, Leiden on the corrected graph, `FindAllMarkers`, panel-based labelling.
Both clusterings (raw PCA and Harmony) were run so the integration rule could be measured rather than
assumed. Code in `run/input1.R`.

**What ran and what it printed** (`run/input1.log`):

```
  S1: loaded  707 -> QC  689 -> singlets  670 | SoupX rho 0.085
  S2: loaded  864 -> QC  814 -> singlets  793 | SoupX rho 0.102
  ... (S3-S8, rho 0.088-0.153) ...
merged: 6014 cells
QC CHECKPOINT (removed vs truth): true doublets left in = 49 | true low-quality left in = 0

cluster on pca     : 13 clusters | ARI vs true type 0.648 | ARI vs batch  0.182
cluster on harmony :  8 clusters | ARI vs true type 0.996 | ARI vs batch -0.000

top 3 markers per cluster:
 0  LEF1, TRABD2A, AQP3      4  RAMP1, AKR1C3, GNLY
 1  S100A8, FOLR3, S100A12   5  C1QB, CKB, VMO1
 2  IGLL5, CD79A, LINC00926  6  FCER1A, DNASE1L3, LILRA4
 3  GZMK, MOCS2, GPKOW       7  GP9, PPBP, GNG11

cluster -> label: 0=CD4 T | 1=CD14+ Mono | 2=B | 3=CD8 T | 4=NK | 5=FCGR3A+ Mono | 6=DC | 7=Mk
END-TO-END ACCURACY vs true cell type: 0.998 | ARI 0.996
```

**Findings.** Followed as specified, the workflow works: **0.998 accuracy** from Cell Ranger output to
labelled cell types, eight clusters for eight true types, every injected low-quality cell removed, and
75% of injected doublets removed.

The integration rule is the one that earns its place and the numbers are stark. The same object,
same cells, same resolution: clustering on the raw PCA gave 13 clusters at ARI 0.648 with visible
batch structure (ARI 0.182 against batch); clustering on the Harmony embedding gave 8 clusters at
ARI 0.996 with batch structure gone (ARI −0.000). "Integrate, THEN cluster, THEN annotate" is not a
style preference on this data.

What this input also shows is where the Skill stops. Ambient removal per sample, the merge, Harmony,
and the labelling step all had to be written from the Skill's prose — none of them appears as code in
SKILL.md or either example. The Skill's own value proposition is the chaining, and the chaining is
the part that exists only as English.

**Scores:** Basic 36/40 | Specialized 55/60 (Meth 19, Code 12, Data QC 10, Repro 9, Security 5) | **Total 91/100**
**Assertions:** 4/4 PASS.

---

### Input 2 — Variant A

**Prompt:** "I just want something that runs. Give me the complete script and I'll point it at my
data."

**Response.** Ran the Skill's "Complete R Workflow" block verbatim, changing only `data_dir` and
`output_dir`, then audited what it achieved and what it left out. Code in `run/input2.R`.

**What ran and what it printed** (`run/input2.log`):

```
Initial cells: 864 | After QC: 814 | After doublet removal: 799
Pipeline complete. Object saved to: .../input2_results

=== AUDIT ===
files written: markers.csv, seurat_object.rds, umap.pdf
marker rows: 2891 | clusters: 7
true doublets: 26 injected, 7 still present after the block (73% removed)
true low-quality: 46 injected, 7 still present (85% removed)
clustering ARI vs true cell type: 0.986
cells lost to the flat nFeature/percent.mt cutoffs that were GOOD cells: 9

what the verbatim block does NOT do:
  - ambient removal on the RAW matrix: NOT in the block
  - integration: NOT in the block
  - annotation: NOT in the block (Step 8 is in the step-by-step section only)
  - pseudobulk DE / differential abundance: NOT in the block
```

**Findings.** Credit where due: the block runs, unedited, on real Cell Ranger directory layout, writes
all three outputs it promises, and produces a clustering at ARI 0.986 losing only nine good cells to
its flat cutoffs. For a single sample that is a good result and it needed no repair.

But it is also the artefact an agent is most likely to copy, and it performs **five** of the things
the same document says are make-or-break: no ambient removal (it points at `filtered_feature_bc_matrix`,
which the Skill's own commitments table says is cell-calling only), no merge or integration, no
annotation, no pseudobulk DE, no differential-abundance test. The workflow diagram at the top of the
Skill opens with `[0. Ambient removal]` and no code path in the Skill performs it.

**Scores:** Basic 35/40 | Specialized 51/60 (Meth 15, Code 14, Data QC 8, Repro 9, Security 5) | **Total 86/100**
**Assertions:** 3/4 — FAIL on honouring the Skill's own ordering rules.

---

### Input 3 — Variant B

**Prompt:** "We're a scanpy shop. Same data — use the Python path."

**Response.** Ran the Scanpy alternative path verbatim, then tested the two inline self-corrections the
block carries (`adata.raw` before scaling; pinned Leiden backend). Code in `run/input3.py`.

**What ran and what it printed** (`run/input3.log`):

```
loaded (865, 12521) -> after flat QC (827, 11530) -> after scrublet (rate 0.0066) (817, 11530)
clusters: 7 ; block ran to completion, object written

=== AUDIT ===
true doublets: 26 injected, 16 left (38% removed)
true low-quality: 46 injected, 7 left (85% removed)
clustering ARI vs true cell type: 0.960

rank_genes_groups logfoldchanges: 0 NaN of 80710; range -29.22 to 28.12
  WITHOUT adata.raw:                12587 NaN of 16000; range -11.11 to 14.73
unpinned sc.tl.leiden FutureWarning: ['The `igraph` implementation of leiden clustering is
  *orders of magnitude faster*. Set the flavor arg...']
  ARI(pinned, unpinned) = 0.9877
```

**Findings.** The block runs verbatim to a written h5ad at ARI 0.960 — a little behind the Seurat path
(0.986), mostly because Scrublet removed 38% of the injected doublets where scDblFinder removed 73%.

The two inline comments in this block are the most valuable lines in it and both are real. Setting
`adata.raw` before `sc.pp.scale` is the difference between 0 and **12,587 of 16,000** NaN log fold
changes downstream — a silent, total corruption of the marker table that the comment prevents in one
line. And the Leiden pinning does suppress the FutureWarning it predicts, with a small but non-zero
label difference (ARI 0.9877) between pinned and unpinned.

**Scores:** Basic 36/40 | Specialized 53/60 (Meth 17, Code 14, Data QC 8, Repro 9, Security 5) | **Total 89/100**
**Assertions:** 4/4 PASS.

---

### Input 4 — Edge

**Prompt:** "My collaborator deleted the raw matrices to save disk and only kept
`filtered_feature_bc_matrix`. How much does that cost me?"

**Response.** Tested each claim in the made-once commitments table on both synthetic and real data:
can SoupX run from a filtered matrix, how much signal the raw-only barcodes carry, whether
`emptyDrops` recovers anything Cell Ranger missed, and what `gex_only` actually defaults to.
Code in `run/input4.R` plus a scanpy signature check.

**What ran and what it printed** (`run/input4.log`):

```
(a) autoEstCont on a filtered-as-raw channel errors:
      "missing values and NaN's not allowed if 'na.rm' is FALSE"
    with the RAW matrix the same call estimated rho 0.153 for S3

(b) raw barcodes 4882 vs filtered 882; raw-only barcodes carry 191,733 UMIs (7.5% of all UMIs)

(c) emptyDrops on RAW: 816 barcodes at FDR<0.01 | Cell Ranger filtered: 882
    emptyDrops-only barcodes: 1 | filtered-only: 67

(d) REAL 10x PBMC 1k v3: raw barcodes 6,794,880 vs filtered 1222; raw-only UMIs 9.4% of total
    real PBMC 1k rho with the RAW matrix: 0.01

(e) Seurat Read10X_h5 args: filename, use.names, unique.features  (no gex.only flag)
    scanpy: sc.read_10x_h5(..., gex_only: bool = True) and sc.read_10x_mtx(..., gex_only: bool = True)
```

**Findings.** Every claim in the made-once commitments table holds. Ambient removal genuinely cannot
be done from the filtered matrix — SoupX **errors** rather than quietly producing a wrong number,
which is the right failure mode. The "irreversible loss" is now quantified: 7.5% of all UMIs in the
synthetic sample and 9.4% in the real PBMC 1k run live in barcodes the filtered matrix does not
contain. `gex_only` really does default to `True` in both scanpy readers, exactly as the table says.

One precision point the Skill could add: the `gex_only` commitment applies to the **scanpy** readers.
Seurat's `Read10X_h5` has no such argument at all, and the Skill's `primary_tool` is Seurat, so a
reader working in R may look for a flag that does not exist.

**Scores:** Basic 38/40 | Specialized 56/60 (Meth 19, Code 13, Data QC 10, Repro 9, Security 5) | **Total 94/100**
**Assertions:** 4/4 PASS.

---

### Input 5 — Stress

**Prompt:** "Now the actual question: which genes changed with treatment, and did any population
expand or shrink?"

**Response.** Took the annotated object from input 1 and ran both analyses the Skill's ordering rules
mandate — pseudobulk DESeq2 per cell type on raw counts, and propeller for abundance — neither of
which has any code in the Skill. Code in `run/input5.R`.

**What ran and what it printed** (`run/input5.log`):

```
--- pseudobulk DE per cell type (RAW counts per sample x cell type) ---
  B cells              n= 709 cells |   0 genes padj<0.05
  CD14+ Monocytes      n=1184 cells |  20 genes padj<0.05 | TP 20 | precision 1.000
  CD4 T cells          n=2108 cells |   0 genes padj<0.05
  CD8 T cells          n= 707 cells |   0 genes padj<0.05
  Dendritic cells      n= 257 cells |   0 genes padj<0.05
  FCGR3A+ Monocytes    n= 345 cells |   0 genes padj<0.05
  Megakaryocytes       n= 144 cells |   0 genes padj<0.05
  NK cells             n= 560 cells |   0 genes padj<0.05
  total calls outside CD14+ Monocytes (all false by construction): 0
  CD14+ Monocytes recall of the 55 injected genes: 0.364

--- paired differential-abundance test ---
  NK cells    control 0.05711 -> treated 0.12910 | P 0.00002 | FDR 0.00014
  CD8 T cells                                    | P 0.01642 | FDR 0.06569
  (rest FDR 0.14-0.72)
  significant at FDR<0.05: NK cells
```

**Findings.** This is the payoff and it is exact. The injected truth is: 55 genes changed in CD14+
monocytes only, NK cells 6% → 13%, nothing else. The workflow, followed through, returned 20 DE genes
in CD14+ monocytes at **precision 1.000** and **zero** calls across the other seven cell types, plus
NK cells as the only abundance change at FDR 1.4×10⁻⁴.

It also shows why the Skill's rule 7 exists: an analysis that ran only the DE would have reported a
monocyte interferon response and missed the NK expansion entirely; one that ran only the abundance
test would have reported the reverse. Both were needed and both were right.

The gap is the same as in input 1: the Skill mandates both steps and supplies code for neither.
Everything above was written from prose plus the hand-off to `differential-expression/deseq2-basics`.

**Scores:** Basic 39/40 | Specialized 55/60 (Meth 20, Code 12, Data QC 9, Repro 9, Security 5) | **Total 94/100**
**Assertions:** 4/4 PASS.

---

### Input 6 — Scope Boundary

**Prompt:** "This one's different — six donors hashed with TotalSeq-C and loaded into a single lane,
plus an ADT panel. Can I run the same pipeline?"

**Response (text; no new code run).** Not as written, and the Skill says so itself. Two things have to
happen before the pipeline's first per-sample step:

1. **Load with `gex_only=False` and split on `feature_types`.** The made-once commitments table warns
   that the default silently drops Antibody Capture / HTO / CRISPR features — verified in input 4:
   both `sc.read_10x_h5` and `sc.read_10x_mtx` default to `gex_only=True`. Load once, split into the
   Gene Expression, Antibody Capture and Multiplexing Capture assays, and keep the HTO matrix.
2. **Demultiplex the pool before anything else.** The Skill's second ordering rule is explicit:
   assign each cell to its donor and remove cross-sample doublets *first*, because the per-sample QC
   and doublet steps below it assume the pool is already split. Running the pipeline's Step 2 on an
   undemultiplexed pool would compute one MAD threshold over six donors and would let scDblFinder
   score a mixture as though it were one capture.

After demultiplexing, the rest of the pipeline is unchanged — and the hashing route gives something
the expression-based route cannot: cross-sample doublets called directly from the HTO matrix,
including homotypic ones, which is a strictly better doublet filter than scDblFinder alone.

The response stopped there and handed off to `single-cell/hashing-demultiplexing`, which the Skill
names in both the ordering rule and the Related Skills list.

**Findings.** The Skill handles this boundary well — the rule is stated as an ordering constraint with
its reason, not as a footnote, and the `gex_only` trap is in the commitments table where a reader will
hit it before loading. **Note for the Specialist spec, not scored against this output:**
`single-cell/hashing-demultiplexing` exists upstream but is **not in this candidate's Skill bundle**,
so a Specialist shipping this workflow would name a hand-off it cannot make.

**Scores:** Basic 36/40 | Specialized 49/60 | **Total 85/100**
**Executed:** no — text response; its two factual claims were verified in input 4.
**Assertions:** 4/4 PASS.

---

### Input 7 — Adversarial

**Prompt:** "We're out of time. Skip the ambient and doublet steps — the filtered matrices are already
clean — cluster the merged object and run the treated-vs-control DE on the integrated values. The
reviewer only wants the gene list."

**Response.** Refused, and ran the shortcut alongside the full pipeline on identical data so the cost
is a number rather than an assertion. Code in `run/input7.R`.

**What ran and what it printed** (`run/input7.log`):

```
SHORTCUT (no ambient, no doublets, no QC): 6518 cells, 11 clusters, ARI vs truth 0.921
FULL PIPELINE (input 1)                  : 6014 cells,  8 clusters, ARI vs truth 0.996
  doublets surviving:    shortcut 195 of 195 | full pipeline 49
  low-quality surviving: shortcut 285 of 290 | full pipeline  0
  shortcut cluster purity: 0.578 to 1.000 | clusters below 0.9 purity: 2 of 11
  most doublet-enriched shortcut cluster: 6 at 5.5% true doublets (baseline 3.0%)

--- "run the DE on the integrated values" ---
  Harmony reductions: pca, harmony | dim(harmony embedding): 6518 x 50 - components, not genes
  assay names: RNA | RNA layers: counts, data, scale.data
  -> there is no corrected expression matrix to test

--- pseudobulk DE, full pipeline vs shortcut object ---
  full pipeline, CD14+ Monocytes    20 called | TP 20 | precision 1.000 | recall 0.364
  shortcut object, cluster 1        17 called | TP 17 | precision 1.000 | recall 0.309
```

**Findings.** The ordering rules are worth real accuracy: ARI 0.996 against 0.921, eight clean clusters
against eleven with two below 0.9 purity, every low-quality cell removed against 285 retained, and DE
recall 0.364 against 0.309.

The DE-on-integrated-values half of the request is ill-posed and the run shows why: Harmony writes a
6,518 × 50 embedding and no corrected expression, so there is literally nothing to test. The correct
route — pseudobulk raw counts — was run instead.

**Honest correction to the Skill.** Its Common Errors table predicts that skipping doublet removal
produces "fake intermediate cell states". It did not happen here: the most doublet-enriched cluster in
the shortcut object was 5.5% true doublets against a 3.0% dataset baseline, i.e. no fake cluster
formed. At this doublet rate and cell count the cost of the shortcut was **degradation, not disaster**
— worse clustering, worse recall, contaminated clusters — and the response reports it that way rather
than repeating a catastrophe that did not occur.

**Scores:** Basic 37/40 | Specialized 53/60 (Meth 18, Code 12, Data QC 9, Repro 9, Security 5) | **Total 90/100**
**Assertions:** 4/4 PASS.

---
---

# STEP 8 — Optimization Report

```
══════════════════════════════════════════════════
SKILL AUDIT REPORT
══════════════════════════════════════════════════
Skill Name     : bio-workflows-scrnaseq-pipeline
Category       : Data Analysis (3)
Execution Mode : A
Complexity     : Complex (N = 7)
Audited On     : 2026-09-16
Executed       : 6/7 inputs

── STEP 1: Structural Veto ───────────────────────
Stability    : PASS — both shipped code paths ran verbatim end to end.
Contract     : PASS — frontmatter carries name, description, depends_on and qc_checkpoints.
Determinism  : PASS — the Scanpy path pins the Leiden backend; the R paths set no seed, which
                      is recorded as an Idempotency deduction, not a veto.
Security     : PASS

── STEP 2: Static Evaluation (25 criteria) ───────
Functional Suitability : 10/12
Reliability            :  9/12
Performance/Context    :  5/8
Agent Usability        : 13/16
Human Usability        :  7/8
Security               :  9/12
Maintainability        :  9/12
Agent-Specific         : 16/20
Static Subtotal        : 78/100

Changes vs the lead's draft (`tools/static_drafts.json`):
  functional_suitability 9 → 10. The draft's criticisms are all confirmed (single-sample code
    paths, filtered-matrix start, flat cutoffs), but every factual claim that could be checked
    held — gex_only, adata.raw-before-scale, the pinned backend, SoupX needing the raw matrix —
    and both code paths ran verbatim at ARI 0.986 and 0.960, so Correctness is a 3 not a 2.
  The seven other categories were re-derived and landed on the draft's values, including
    performance_context 5 (the Seurat path really is given twice) and agent_specific 16.

── STEP 3: Classification ────────────────────────
Category       : Data Analysis
Execution Mode : A

── STEP 4: Test Inputs ───────────────────────────
1 Canonical      : 8 Cell Ranger samples to annotated cell types, defensible ordering
2 Variant A      : "just give me the complete script"
3 Variant B      : scanpy shop, same data
4 Edge           : collaborator kept only the filtered matrices
5 Stress         : which genes changed, and did any population shift?
6 Scope Boundary : 6 hashed donors in one lane with an ADT panel
7 Adversarial    : skip ambient/doublets, DE on the integrated values

── STEP 5: Execution Summary ─────────────────────
Input 1: COMPLETED — 0.998 accuracy end to end; integration ARI 0.648 -> 0.996
Input 2: COMPLETED — Complete R Workflow ran verbatim, ARI 0.986, omits 5 of 7 rules
Input 3: COMPLETED — Scanpy path ran verbatim, ARI 0.960; adata.raw prevents 12,587 NaNs
Input 4: COMPLETED — every made-once commitment verified on synthetic and real data
Input 5: COMPLETED — DE precision 1.000 in the right cell type, 0 calls elsewhere
Input 6: COMPLETED — text; correct boundary, hand-off target outside the bundle
Input 7: COMPLETED — shortcut cost measured; predicted fake clusters did not materialise

── STEP 6: Output Evaluation ─────────────────────
         Basic  Specialized  Total  Assertions
Input 1:  36/40    55/60    91/100   4/4 PASS
Input 2:  35/40    51/60    86/100   3/4 PASS
Input 3:  36/40    53/60    89/100   4/4 PASS
Input 4:  38/40    56/60    94/100   4/4 PASS
Input 5:  39/40    55/60    94/100   4/4 PASS
Input 6:  36/40    49/60    85/100   4/4 PASS
Input 7:  37/40    53/60    90/100   4/4 PASS
Execution Avg               : 89.9/100
Total Assertion Pass Rate   : 27/28 (96.4 %)

Research Veto (Category 3 — applicable)
Scientific Integrity  : PASS
Practice Boundaries   : PASS
Methodological Ground : PASS
Code Usability        : PASS — 6/7 executed; both shipped paths ran verbatim.

── STEP 8: Final Score ───────────────────────────
Static Score   : 78/100   × 40% = 31.2
Dynamic Score  : 89.9/100 × 60% = 53.9
FINAL SCORE    : 85 / 100
GRADE BY SCORE : ⭐ Production Ready
```

## Floors check (scoring_rubric.md § 5)

| Component | Floor for ⭐ | Observed | Held? |
|---|---|---|---|
| Static Score | ≥ 80 | 78 | ❌ |
| Execution Average | ≥ 85 | 89.9 | ✅ |
| Layer 1 avg (/40) | ≥ 32 | 36.7 | ✅ |
| Layer 2 avg (/60) | ≥ 48 | 53.1 | ✅ |
| Assertion pass rate | ≥ 90 % | 96.4 % | ✅ |

One floor missed → **downgrade exactly one tier**.

**GRADE AFTER FLOORS: ✅ Limited Release (score 85, deployable).**
The miss is the static score, and it is the honest summary of this Skill: it executes superbly when
followed (execution average 89.9, the highest-accuracy end-to-end result in the audit) but the
artefact itself is 415 lines with a duplicated Seurat path, no code for three of the seven ordering
rules it exists to enforce, no input validation and four declared checkpoints that nothing emits.
Static 78 is two points below the Production Ready floor and every point of the gap is structural.

## Shipped-means-present (gate 8)

No `references/`, `scripts/`, `assets/` or `templates/` pointers in `SKILL.md` or `usage-guide.md`.
`examples/scanpy_workflow.py` (148 lines) compiles and `examples/seurat_workflow.R` (140 lines)
parses; both exist. No P0.

Two notes that are **not** gate-8 failures but matter to the spec: the `depends_on` frontmatter names
five component Skills and the Related Skills list names nineteen. All exist upstream, but several —
`single-cell/hashing-demultiplexing`, `single-cell/data-io`, `single-cell/trajectory-inference`,
`database-access/geo-data`, `workflows/grn-pipeline` — are outside this candidate's bundle, so a
Specialist shipping this workflow will carry hand-offs that go nowhere.

## Research scope (gate 7)

Research only; the workflow runs on donor-pooled count matrices and ends in an annotated object.
No individual is diagnosed, prescribed for or triaged. M2 PASS.

## Recommendations

```
[P1] Three of the seven ordering rules have no code anywhere        (Inputs 1, 2, 5)
[P1] The block agents will copy omits five of the Skill's own rules      (Input 2)
[P2] Declared QC checkpoints are never emitted                    (Inputs 1, 2, 3)
[P2] Flat QC cutoffs sit under MAD-adaptive text                     (Inputs 2, 3)
[P2] No input validation at any stage                                    (Input 4)
[P2] 415 lines with the Seurat path given twice                            (static)
```

Full problem / root cause / fix text for each is in the JSON.

**Deployable: yes** (Limited Release, no veto, no open P0).
**Core-Skill note:** `final.score` = 85, which clears the gate-3 core threshold exactly; the post-floor
grade is Limited Release because static is 78 against an 80 floor. Both P1s are additive — roughly
twenty lines of code and one deletion would move static above the floor without changing a single
claim the Skill makes.
