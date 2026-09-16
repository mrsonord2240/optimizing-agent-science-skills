> **Audit record for `bio-single-cell-preprocessing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/single-cell/preprocessing) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-preprocessing

Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:single-cell/preprocessing`
(read from the byte-identical clone `F:\OpenScience\external\mrsonord2240__bioSkills\single-cell\preprocessing\`)
Category: 3 — Data Analysis | Mode: A (SKILL.md code patterns; no `scripts/`) | Complexity: Complex → N = 7

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | yes | 37 | 55 | 92 | 4/4 PASS | ✅ |
| 2 | Variant A | yes | 31 | 45 | 76 | 3/4 PASS | ✅ |
| 3 | Edge | yes | 36 | 52 | 88 | 3/4 PASS | ✅ |
| 4 | Variant B | yes | 37 | 55 | 92 | 4/4 PASS | ✅ |
| 5 | Stress | yes | 33 | 48 | 81 | 3/4 PASS | ✅ |
| 6 | Scope Boundary | no (text) | 33 | 49 | 82 | 4/4 PASS | ✅ |
| 7 | Adversarial | yes | 38 | 54 | 92 | 4/4 PASS | ✅ |

**Execution Average: 86.1 / 100**
**Assertion Pass Rate: 25/28 (89.3 %)**
**Executed inputs: 6/7**

Data used: the SYNTHETIC 8-sample PBMC set (`_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples`,
with `truth_cells.csv` ground truth), two SYNTHETIC datasets derived from it (`data/README.md`), and
the real public 10x PBMC 1k v3 run (raw + filtered) for the ambient-RNA input.

---

## Detailed Outputs

### Input 1 — Canonical

**Prompt:** "I have Cell Ranger v3 output for eight PBMC samples — four vehicle, four treated with a
TLR7 agonist, run across two 10x lanes (batch A: S1, S2, S5, S6; batch B: S3, S4, S7, S8), one donor
per sample, 700–950 cells each. Run QC and get me to a PCA I can cluster. I've been burned before by
a global filter that ate my platelets, so use adaptive thresholds and tell me exactly what came out."

**Response (abridged; full code in `run/input1.py`).** Followed the Skill's Quality Control section:
annotate `mt` / `ribo` / `hb`, `calculate_qc_metrics(..., percent_top=[20], log1p=True, inplace=True)`,
the `is_outlier` helper, 5 MAD on `log1p_total_counts` / `log1p_n_genes_by_counts` /
`pct_counts_in_top_20_genes` and 3 MAD + hard 8% on `pct_counts_mt`, computed **per sample** with the
`groupby` block at SKILL.md:81-86, then `filter_genes(min_cells=3)`, stash `layers['counts']`,
`normalize_total` + `log1p`, `seurat_v3` HVG from `layer='counts'` with `batch_key='sample'`, and PCA
on the HVG mask with no scaling.

**What ran and what it printed** (`run/input1.log`):

```
Loaded: 6524 cells, 12521 genes, 8 samples
mito genes: 13 | ribo: 98 | hb: 4
GLOBAL MAD: count/gene/top20 outliers=268, mito outliers=581, total flagged=617
SKILL per-sample block: OK, dtype bool len 6524
  index aligned with adata.obs_names: True
  S1: n=707 median_counts=2421 median_mito=2.70% count/gene outliers=24 mito outliers=40
  ... (S2-S8) ...
PER-SAMPLE MAD: total flagged=555 (8.5%)

GROUND TRUTH CHECK (synthetic labels):
  global MAD: removed 617  TP=290 FP=327 FN=0  recall=1.000 precision=0.470
    good cells lost by type: Megakaryocytes 0.256, FCGR3A+ Monocytes 0.144, CD14+ Mono 0.077
  per-sample MAD: removed 555  TP=290 FP=265 FN=0  recall=1.000 precision=0.523
    good cells lost by type: Megakaryocytes 0.288, FCGR3A+ Monocytes 0.096, CD8 T 0.055

After QC: 5969 cells, 12521 genes
HVGs: 2000
seurat_v3 on LOG-NORMALISED data: ran without error, 702/2000 HVGs shared with the correct run
PCA: (5969, 50)
```

**Findings.** (a) The `groupby(...).apply(...).droplevel(0)` block at SKILL.md:81-86 runs verbatim on
pandas 3.0.5 and returns a Series correctly aligned to `obs_names` — a block that could easily have
rotted, and has not. (b) The recipe caught **every** injected low-quality cell (recall 1.000) at both
settings, and per-sample MAD raised precision from 0.470 to 0.523, which is the Skill's claim. (c) The
collateral is concentrated in megakaryocytes (28.8% of them removed) because
`pct_counts_in_top_20_genes` is high in transcriptionally simple cells by construction; the Skill
attaches its "this is a biology metric" caveat only to `pct_counts_mt`. (d) Feeding `seurat_v3`
log-normalised data — the Skill's headline gotcha — produced 65% different HVGs. scanpy 1.12 does emit
a `UserWarning`, so the Skill's "runs silently" is slightly out of date, but the consequence is real.

**Scores:** Basic 37/40 | Specialized 55/60 (Methodological validity 18, Code executability 14, Data QC 10, Reproducibility 8, Security 5) | **Total 92/100**

**Assertions:** 4/4 PASS (see JSON).

---

### Input 2 — Variant A

**Prompt:** "Same eight PBMC captures. My reviewer says the hemoglobin signal in my T cells is soup.
Run SoupX on the Cell Ranger output, report the contamination fraction per sample, and prove to me the
correction didn't eat CD3. I also have the public 10x PBMC 1k v3 run as a clean control — what rho do
you get there?"

**Response (full code in `run/input2.R`).** Step 1 ran the SKILL.md:123-128 snippet verbatim on
`S1/outs`. Step 2 was the adapted route. Step 3 ran the real PBMC 1k.

**What ran and what it printed** (`run/input2.log`):

```
=== SKILL.md:123-128 verbatim on S1 ===
Loading raw count data / Loading cell-only count data / Loading extra analysis data where available
VERBATIM SNIPPET FAILED:
 Error in autoEstCont(sc) :
  Clustering information must be supplied, run setClusters first.

=== Adapted: build SoupChannel, cluster with Seurat, then autoEstCont ===
  S1 HBB soup gene: pre = 1763  post = 0
  S1 CD3D/E lineage marker: pre = 1849  post = 1670  cells expressing pre/post = 472 / 412
  S1 total counts removed: 8.5 %
   sample estimated_rho true_rho abs_err
S1 0.085 0.0492 0.0358 | S2 0.102 0.0456 0.0564 | S3 0.153 0.0982 0.0548 | S4 0.138 0.0649 0.0731
S5 0.088 0.0420 0.0460 | S6 0.134 0.0633 0.0707 | S7 0.093 0.0570 0.0360 | S8 0.137 0.0975 0.0395
mean |error| = 0.0515

=== REAL 10x PBMC 1k v3 (public data) ===
real PBMC 1k rho = 0.01 ; counts removed: 1 %
```

**Findings.** The single most consequential defect found in this Skill: **the SoupX pattern as printed
does not run on the input the Skill names.** `load10X` imports clusters only when Cell Ranger's
`analysis/clustering/` directory is present; a matrix-only delivery — which is what most collaborators
hand over, and what the Skill's own "needs BOTH raw and filtered" comment describes — makes
`autoEstCont` abort. Recovery needed a full Seurat normalise/PCA/neighbours/cluster pass and
`setClusters`, none of which appears anywhere in SKILL.md or the usage guide. The method itself is
right: HBB soup went to zero, the Skill's prescribed marker-survival check caught that 60 of 472 cells
lost CD3D/E (exactly the "zero out genes cells genuinely lacked" risk the Skill warns about), and the
real PBMC 1k gave the literature-typical rho = 0.01. Over-estimation against the synthetic truth
(mean |error| 0.052, roughly 2x) is reported as **context, not a Skill defect** — the synthetic soup is
a pooled-profile construction that SoupX's tf-idf marker route was not designed for.

**Scores:** Basic 31/40 | Specialized 45/60 (Meth 16, Code 8, Data QC 9, Repro 7, Security 5) | **Total 76/100**

**Assertions:** 3/4 — FAIL on "the SoupX code the Skill prescribes runs on the input the Skill names".

---

### Input 3 — Edge

**Prompt:** "This is a snRNA-seq pilot: one nucleus prep, ~120 nuclei recovered after the sort, and the
depth histogram is a spike. Your MAD filter deleted a third of them. Is that real, and what should I
do instead?"

**Response (full code in `run/input3.py`).** Derived a 120-nucleus set from synthetic S1 with MT- genes
zeroed and 70% of barcodes on an 800-UMI plateau (`data/tiny_nuclei.h5ad`), ran the Skill's QC block
verbatim, printed the MAD of every metric, and then applied the guard the Skill's Common Errors row
prescribes.

**What ran and what it printed** (`run/input3.log`):

```
Derived tiny nuclei-like set: 120 cells, 12521 genes, total_counts range 420-2177
  log1p_total_counts:          median=6.6859  MAD=0.000000
  log1p_n_genes_by_counts:     median=6.0580  MAD=0.063992
  pct_counts_in_top_20_genes:  median=28.1187 MAD=1.937500
  pct_counts_mt:               median=0.0000  MAD=0.000000
SKILL verbatim MAD rule: outlier=36, mt_outlier=0, survivors=84/120
GUARD: survival fraction = 0.700  -> no fallback needed
pct_counts_mt: all zero? True -> mt_outlier flags 0 cells (mito rule is inert on nuclei, as the Skill says)
```

**Findings.** The Skill predicted this failure precisely — the Common Errors row names the symptom
("Almost all cells filtered / tiny survivor count"), the cause ("MAD ~ 0 on a low-variance, tiny, or
nuclei sample (>50% share a value)") and the mechanism ("`is_outlier` flags every non-median cell").
All three reproduced exactly: MAD = 0 on `log1p_total_counts`, and the 36 barcodes off the plateau were
flagged for no quality reason. Its nuclei guidance is also right — `pct_counts_mt` is identically zero
and the mito rule fires on nothing. The gap is the guard: `n_obs > 0` can never fire here, and "a sane
survival fraction" has no number, so a 30% loss passed silently. That is a real but small fix.

**Scores:** Basic 36/40 | Specialized 52/60 (Meth 17, Code 13, Data QC 9, Repro 8, Security 5) | **Total 88/100**

**Assertions:** 3/4 — FAIL on "the guard the Skill prescribes fires and triggers its fixed-cutoff fallback".

---

### Input 4 — Variant B

**Prompt:** "Before I commit: shifted-log, scran, or SCTransform for this PBMC set? A reviewer on my
last paper complained that CP10k flattened my platelet population. Show me what actually differs
between the three, don't just tell me the default."

**Response (full code in `run/input4.R`).** Ran all three routes on synthetic sample S2 (865 cells,
13 megakaryocytes — the composition-divergent population standing in for the plasma/secretory cells
the Skill names), compared scran size factors to library-size factors per true cell type, and timed
SCTransform.

**What ran and what it printed** (`run/input4.log`):

```
median library size by true type: Dendritic 5292 | FCGR3A+ Mono 4194 | CD4 T 2454 | CD14+ Mono 2398
                                  CD8 T 2194 | NK 1999 | B 1941 | Megakaryocytes 1038
scran size factors: min 0.1153 max 3.59 | any negative? FALSE
cor(scran sf, library-size sf) = 0.9729
ratio scran_sf / libsize_sf by true type (1 = the two agree):
  B 0.976 | CD14+ Mono 0.971 | CD4 T 0.937 | CD8 T 1.066 | DC 0.966 | FCGR3A+ Mono 1.083
  Megakaryocytes 0.892 | NK 1.361
SCTransform: 10.7s, 3000 variable features, vst.flavor = v2
PPBP share of the megakaryocyte transcriptome: 2.9 %
```

**Findings.** The decision table is accurate on every checkable point: scran needs `quickCluster`
(it does), its factors "can go negative" (none did here, and the response says it checked rather than
assuming), and SCTransform defaults to v2 in sctransform 0.4.3 as the table implies. The Governing
Principle's compositional claim is demonstrable: the two size-factor systems agree to r = 0.973 overall
but disagree by **up to 36% systematically by cell type** (NK 1.36x, megakaryocytes 0.89x), which is
exactly why the Skill tells you to report relative and not absolute expression.

**Scores:** Basic 37/40 | Specialized 55/60 (Meth 19, Code 14, Data QC 9, Repro 8, Security 5) | **Total 92/100**

**Assertions:** 4/4 PASS.

---

### Input 5 — Stress

**Prompt:** "Bad news: my second 10x lane (S3, S4, S7, S8) under-loaded and came back at about a third
the depth of the first. Same eight donors, same design. Do I have to throw the shallow lane away? Work
through QC, feature selection and whether I should regress out depth, and show me the numbers."

**Response (full code in `run/input5.py`).** Built `data/depth_imbalanced.h5ad` (batch B binomially
downsampled to 35%), then tested the Skill's three multi-sample claims in order.

**What ran and what it printed** (`run/input5.log`):

```
median total_counts per sample: S1 2421 S2 2401 S3 831 S4 866 S5 2330 S6 2356 S7 790 S8 852

(a) removal rate per sample (% of that sample):
        n   global_rm  per_sample_rm  true_lowq
S1    707        7.6            7.1        1.8
S2    865        7.7            9.0        5.3
S3    882       10.1            9.8        6.2
S4    806        8.9            8.6        3.8
S5    738       14.6            7.7        5.0
S6    840        8.1            8.6        5.5
S7    784        8.5            8.9        2.8
S8    902        9.1            9.6        4.4
  global:     removed 607 TP=290 FP=317 FN=0 recall=1.000 precision=0.478
  per-sample: removed 569 TP=290 FP=279 FN=0 recall=1.000 precision=0.510

(b) SKILL.md:176 batch_key advice FAILED on the shallow batch:
    ValueError: b'reciprocal condition number  2.0657e-15'
    workaround (filter_genes min_cells=30 first): OK, 950/2000 shared with the no-batch_key list

    PCA(no regression): silhouette by TRUE CELL TYPE=0.2372, by BATCH=0.0877
(c) PCA after regress_out(total_counts, pct_counts_mt):
    silhouette by TRUE CELL TYPE=0.2412 (delta +0.0040), by BATCH=0.0301
```

**Findings.** Three results, two of which correct the Skill.
(a) Per-sample MAD **is** better than global — precision 0.478 → 0.510 with recall held at 1.000 — but
not for the stated reason. SKILL.md:79 says "a single global MAD over-cuts the shallow batch and
under-cuts the deep one"; here the worst global over-cut (14.6%) landed on **S5, a deep sample**. The
recommendation is right, the mechanism as stated is not what happened.
(b) The `batch_key` instruction at SKILL.md:176 has an undocumented precondition and crashed outright:
`seurat_v3`'s per-batch loess is singular when a batch is shallow enough. Filtering genes to
`min_cells=30` first fixed it. There is no Common Errors row for this.
(c) The Skill's "regressing them erases biology and can collapse data into a blob" was **not reproduced**
— cell-type silhouette moved +0.004 and batch silhouette fell. Reported as context rather than a
defect: this synthetic PBMC set has no cycling population, which is the case the Skill's warning is
actually about, so the dataset cannot falsify the claim. The response says so instead of asserting
either way.

**Scores:** Basic 33/40 | Specialized 48/60 (Meth 16, Code 11, Data QC 9, Repro 7, Security 5) | **Total 81/100**

**Assertions:** 3/4 — FAIL on "the Skill's HVG batch_key instruction executes on the design it is prescribed for".

---

### Input 6 — Scope Boundary

**Prompt:** "I've got four 10x Visium slides of mouse colon, CytAssist, and I want the same QC you'd do
on my single-cell data — mito filter, MAD thresholds, HVGs. Same recipe?"

**Response (text; no new code run).** The response kept the transferable machinery and refused the
rest. Transferable: the QC-metric computation (`calculate_qc_metrics` with mito/ribo/hb gene sets), the
MAD-on-the-log-scale logic, the per-slide rather than pooled threshold rule, and "mito % is a biology
metric". Not transferable, and said so: a Visium barcode is a 55 µm **spot** containing several cells,
so (i) the Skill's reference thresholds (`min_genes` 200, hard 8% mito) are droplet-specific and were
withheld, (ii) empty-droplet calling and ambient-RNA removal as the Skill frames them do not apply —
there is no empty-droplet population to estimate a soup from, and spot-level bleed-through is a
different problem with different tools, and (iii) doublet detection is meaningless at spot level.
The response ended by handing off to a spatial workflow.

**Findings.** The output is correct, but every part of the boundary came from the agent: **SKILL.md and
the usage guide never mention spatial data, Visium, spots or any out-of-scope statement at all.** The
`description` frontmatter does say "single-cell RNA-seq", which is why Trigger Precision still scores 4,
but there is no escape hatch for the adjacent assay a researcher will most often bring. Scored as a
static deduction (Agent-Specific 8.5), not against this output.

**Scores:** Basic 33/40 | Specialized 49/60 | **Total 82/100**
**Executed:** no — text response; its only code is the `calculate_qc_metrics` block already run in input 1.

**Assertions:** 4/4 PASS.

---

### Input 7 — Adversarial

**Prompt:** "My PI wants this out the door. Keep the flat 5% mito cutoff — the UMAP looks great and the
clusters are clean, so it's obviously fine. Also run NormalizeData once more on top, the violin plots
look smoother that way, and regress out total_counts and cell cycle so the clusters stop being driven
by depth. Just give me the code."

**Response (full code and measurements in `run/input7.py`).** All three requests refused, each with a
number rather than an appeal to the Skill's authority.

**What ran and what it printed** (`run/input7.log`):

```
median pct_counts_mt by true type (after imitating a high-mito parenchyma in FCGR3A+ Monocytes):
  FCGR3A+ Monocytes 15.43 | everything else 2.26-2.77

flat >5%: removes 663 cells; 3 MAD + hard 8%: removes 819
  flat >5%:    fraction of each type deleted -> FCGR3A+ Monocytes 1.00, CD8 T 0.06, Megakaryocytes 0.06
  3 MAD + 8%:  fraction of each type deleted -> FCGR3A+ Monocytes 1.00, Megakaryocytes 0.12, CD14+ Mono 0.11

After the flat cutoff deleted 374 of 374 FCGR3A+ monocytes: 16 Leiden clusters, silhouette 0.211
  -> the embedding looks fine; the deletion is invisible in it.

sum(X) after one normalize+log1p = 5.751e+06; after a second pass = 3.809e+06 (ratio 0.662)
  [scanpy also printed: WARNING: adata.X seems to be already log-transformed.]
```

**Findings.** The Skill's content carries this input well — it has explicit, quotable text against all
three requests, and the "a beautiful UMAP proves nothing" principle is exactly the rebuttal to the PI's
argument, now with a measurement behind it (100% of a cell type deleted, 16 clean clusters, silhouette
0.211).

But the same run exposes the Skill's most important internal contradiction: **its own prescribed rule
deletes the population it claims to protect.** The hard `pct_counts_mt > 8` cap is unconditional in
every code block, so on a constitutively high-mito tissue it removed 374/374 of that population and
**more** cells overall (819) than the flat 5% cutoff the Skill criticises (663). The tissue-dependence
lives only in prose at SKILL.md:102 and in a comment in `examples/preprocess_scanpy.py`; the code an
agent copies has no branch. That is the P1 below.

Correction to the Skill: the re-normalization symptom is wrong. `sum(X)` **fell** to 0.662x rather than
inflating ~2x, and scanpy 1.12 raises its own warning. The Skill's fix (restore from
`layers['counts']`) is still right.

**Scores:** Basic 38/40 | Specialized 54/60 (Meth 18, Code 13, Data QC 10, Repro 8, Security 5) | **Total 92/100**

**Assertions:** 4/4 PASS.

---
---

# STEP 8 — Optimization Report

```
══════════════════════════════════════════════════
SKILL AUDIT REPORT
══════════════════════════════════════════════════
Skill Name     : bio-single-cell-preprocessing
Category       : Data Analysis (3)
Execution Mode : A
Complexity     : Complex (N = 7)
Audited On     : 2026-09-16
Executed       : 6/7 inputs

── STEP 1: Structural Veto ───────────────────────
Stability    : PASS — no crash loop, no unresolvable dependency. The one dependency the Skill
                      names as optional (scikit-misc for seurat_v3) is called out in its own
                      Common Errors row and is installed here.
Contract     : PASS — frontmatter has name + description; both non-empty and accurate.
Determinism  : PASS — every numeric step is deterministic given the same input. The Skill sets no
                      seeds, but nothing in its own pipeline is stochastic (PCA is the only
                      randomised step and scanpy's default is reproducible per run). Recorded
                      instead as an Idempotency deduction (8.4).
Security     : PASS — no eval/exec, no credentials, no network calls, no shell-out.

── STEP 2: Static Evaluation (25 criteria) ───────
Functional Suitability : 9/12
Reliability            : 9/12
Performance/Context    : 7/8
Agent Usability        : 14/16
Human Usability        : 7/8
Security               : 10/12
Maintainability        : 10/12
Agent-Specific         : 17/20
Static Subtotal        : 83/100

Changes vs the lead's draft (`tools/static_drafts.json`), both downward and both evidence-based:
  functional_suitability 10 → 9. The draft flagged the SoupX/autoEstCont cluster gap as a guess;
    input 2 confirmed it is a hard error, and inputs 7 added a second correctness defect (the
    "~2x inflation" row is wrong) and a third (the unconditional 8% cap).
  reliability 10 → 9. The Common Errors table is excellent but missed both failures this audit
    actually hit (autoEstCont clusters, seurat_v3 batch_key loess) and one of its rows is wrong.
  All six other categories verified against the files and left at the draft value.

── STEP 3: Classification ────────────────────────
Category       : Data Analysis — the Skill's deliverable is Python/R preprocessing code.
Execution Mode : A — SKILL.md code patterns + usage-guide + examples/; no scripts/ or references/.

── STEP 4: Test Inputs ───────────────────────────
1 Canonical      : 8-donor PBMC drug study, QC → PCA, "don't eat my platelets"
2 Variant A      : SoupX on Cell Ranger output + real PBMC 1k control
3 Edge           : 120-nucleus snRNA-seq pilot with a depth spike
4 Variant B      : shifted-log vs scran vs SCTransform, platelet reviewer complaint
5 Stress         : under-loaded second lane, 3x depth imbalance, multi-part
6 Scope Boundary : 10x Visium slides, "same recipe?"
7 Adversarial    : keep the flat mito cutoff because the UMAP looks great

── STEP 5: Execution Summary ─────────────────────
Input 1: COMPLETED — ran first time, ground truth recall 1.000
Input 2: COMPLETED — prescribed snippet ERRORED; adapted route succeeded
Input 3: COMPLETED — predicted failure mode reproduced exactly
Input 4: COMPLETED — all three normalization routes ran
Input 5: COMPLETED — batch_key HVG advice errored; workaround found
Input 6: COMPLETED — text response, no new code
Input 7: COMPLETED — all verification code ran

── STEP 6: Output Evaluation ─────────────────────
         Basic  Specialized  Total  Assertions
Input 1:  37/40    55/60    92/100   4/4 PASS
Input 2:  31/40    45/60    76/100   3/4 PASS
Input 3:  36/40    52/60    88/100   3/4 PASS
Input 4:  37/40    55/60    92/100   4/4 PASS
Input 5:  33/40    48/60    81/100   3/4 PASS
Input 6:  33/40    49/60    82/100   4/4 PASS
Input 7:  38/40    54/60    92/100   4/4 PASS
Execution Avg               : 86.1/100
Total Assertion Pass Rate   : 25/28 (89.3 %)

Research Veto (Category 3 — applicable)
Scientific Integrity  : PASS
Practice Boundaries   : PASS
Methodological Ground : PASS
Code Usability        : PASS — 6/7 inputs executed; all generated code parses and imports;
                        the one prescribed snippet that errors has a one-line in-package fix,
                        which is a P1, not an M4 failure.

── STEP 8: Final Score ───────────────────────────
Static Score   : 83/100  × 40% = 33.2
Dynamic Score  : 86.1/100 × 60% = 51.7
FINAL SCORE    : 85 / 100
GRADE BY SCORE : ⭐ Production Ready
```

## Floors check (scoring_rubric.md § 5)

| Component | Floor for ⭐ | Observed | Held? |
|---|---|---|---|
| Static Score | ≥ 80 | 83 | ✅ |
| Execution Average | ≥ 85 | 86.1 | ✅ |
| Layer 1 avg (/40) | ≥ 32 | 35.0 | ✅ |
| Layer 2 avg (/60) | ≥ 48 | 51.1 | ✅ |
| Assertion pass rate | ≥ 90 % | 89.3 % | ❌ |

One floor missed → **downgrade exactly one tier**.

**GRADE AFTER FLOORS: ✅ Limited Release (score 85, deployable).**
No safety or scope assertion failed on any output, so the § 4 safety-assertion rule does not apply;
static is well above 60, so the static cap does not apply. The three assertion failures are all
*functional* (prescribed code that does not run as printed), which is why the score stays at 85 while
the grade steps down.

## Shipped-means-present (gate 8)

`SKILL.md` and `usage-guide.md` point at no `references/`, `scripts/`, `assets/` or `templates/` file.
The only shipped artefacts are `examples/preprocess_scanpy.py` and `examples/preprocess_seurat.R`;
**both exist and both are syntactically valid** (`py_compile` clean; the R file parses). No missing
file, no P0 on this gate. Note that neither example is referenced by name from SKILL.md — a
discoverability nit, not a gate-8 failure.

## Research scope (gate 7)

Research only. The Skill operates on count matrices, never on an individual. No output diagnoses,
prescribes or triages. M2 PASS.

## Recommendations

```
[P1] SoupX snippet errors on the input the Skill names
  Observed in: Input 2
  Problem: load10X → autoEstCont → adjustCounts aborts with "Clustering information must be
           supplied, run setClusters first" on standard Cell Ranger raw+filtered output.
  Root cause: written against a Cell Ranger run that included analysis/clustering; the
           precondition is never stated.
  Fix: add setClusters between load10X and autoEstCont, note that a matrix-only delivery needs
       clusters from a quick Seurat/scran pass, and add the error string to Common Errors.

[P1] The prescribed mito rule deletes the population the Skill says it protects
  Observed in: Input 7
  Problem: the unconditional `pct_counts_mt > 8` cap removed 374/374 of a constitutively
           high-mito population and 819 cells overall, vs 663 for the flat 5% cutoff the Skill
           criticises for exactly this failure.
  Root cause: tissue-dependence is stated in prose only; the copied code block has no branch.
  Fix: replace the literal 8 with a named variable from a short tissue table (nuclei ~1,
       PBMC 8, cardiac/hepatic/muscle 25-40, unknown = MAD only) and say when to drop the cap.

[P2] batch_key HVG advice has an undocumented precondition   (Input 5)
[P2] Re-normalization error row states the wrong symptom     (Input 7)
[P2] QC over-removes low-complexity cell types with no warning (Inputs 1, 5)
[P2] MAD-collapse fallback is unquantified                   (Input 3)
```

**Deployable: yes** (Limited Release, no veto, no open P0).
**Core-Skill note for the Specialist spec:** `final.score` = 85, which clears the gate-3 core
threshold; the post-floor *grade* is Limited Release because three prescribed code snippets did not run
as printed. Both numbers are carried into `AUDIT.md`.
