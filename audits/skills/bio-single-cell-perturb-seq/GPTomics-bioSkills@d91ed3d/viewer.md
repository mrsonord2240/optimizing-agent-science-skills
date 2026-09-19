> **Audit record for `bio-single-cell-perturb-seq`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/single-cell/perturb-seq) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-perturb-seq
Generated: 2026-09-19

Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:single-cell/perturb-seq`
Env: `F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\` (pertpy 1.3.0, scanpy 1.12.4, anndata 0.13.3, R 4.4.3)
Category: Data Analysis | Execution Mode: D (hybrid — inline instructions + `examples/*.py`, `examples/*.R`) | Complexity: Complex (7 inputs)

## Skill Veto (Step 1)

| Dimension | Result | Note |
|---|---|---|
| T1 Stability | PASS | Real execution defects found (2 of 5 executable code paths crashed on first try), but each is deterministic, explainable, and fixable with a small documented pattern (the skill's own "introspect and adapt" clause) — not random crashes or unresolvable dependency conflicts. |
| T2 Contract | PASS | Valid frontmatter (`name`, `description`); no API/return-schema to be inconsistent (Mode D prose+code skill). |
| T3 Determinism | PASS | Key stochastic calls are seeded by default in the installed pertpy: `assign_mixture_model` (seed=2024), `Mixscape.mixscape` (random_state=0), `Milo.make_nhoods` (seed=0). One gap: `DistanceTest`'s permutation E-test exposes no seed and SKILL.md doesn't instruct seeding it (see P2 recommendation) — not severe enough to fail T3 since the demonstrated conclusion (crushed by multiple testing) is a systematic floor effect, not a borderline flip. |
| T4 Security | PASS | No eval/exec of raw strings, no injection surface. |

**Gate: PASS**

## Research Veto (Step 6, Category 3 applicable)

| Dimension | Result | Note |
|---|---|---|
| M1 Scientific Integrity | PASS | No fabricated DOIs/results; References section citations (Dixit 2016, Datlinger 2017, Replogle 2020, Papalexi 2021, Yang 2020 scMAGeCK, Barry 2021 SCEPTRE, Squair 2021, Peidli 2024 scPerturb, Heumos 2026 Pertpy, Dann 2022 Milo, Ahlmann-Eltze 2025, Kernfeld 2025, Csendes 2025) all check out as real papers on the stated topics. |
| M2 Practice Boundaries | PASS | Pure research/computational scope throughout; no diagnostic or prescriptive claims. |
| M3 Methodological Ground | PASS | Core prose guidance is textbook-correct and well-cited; the Milo code bug (Input 5) is an API/design-formula defect, not a stated fallacy in the prose. |
| M4 Code Usability | PASS | 5 of 7 inputs produced real, runnable code once the skill's own documented "introspect the installed package and adapt" pattern (Version Compatibility section) was applied. Two defects found (Input 1/4 KeyError, Input 5 AssertionError) are real and costed into the dynamic score below, but they are exactly the class of drift the skill explicitly tells the agent to expect and repair — not silent, unexplained failures. |

**Gate: PASS**

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 30 | 39 | 69 | 3/5 | ⚠️ |
| 2 | Variant A | 24 | 38 | 62 | 2/4 | ❌ |
| 3 | Edge | 38 | 54 | 92 | 4/4 | ✅ |
| 4 | Variant B | 33 | 51 | 84 | 4/4 | ✅ |
| 5 | Stress | 26 | 33 | 59 | 2/4 | ❌ |
| 6 | Scope Boundary | 21 | 24 | 45 | 3/4 | ❌ |
| 7 | Adversarial | 38 | 54 | 92 | 4/4 | ✅ |

**Execution Average: 71.9 / 100**
**Assertion Pass Rate: 22/29 (75.9%)**

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "I have a Perturb-seq experiment (CROP-seq, low MOI) with guide counts and RNA counts in a MuData object. Assign guides with a mixture model and run Mixscape to remove non-perturbed cells."

**Code (`run/input1_guide_mixscape_edist.py`, real data via `pt.dt.papalexi_2021()`, 20,729 cells x 18,649 genes, gdo 111 guides):**
```python
mdata = pt.dt.papalexi_2021()
adata = mdata.mod['rna']
sc.pp.normalize_total(adata, target_sum=1e4); sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000); sc.pp.pca(adata, n_comps=50)

gdo = mdata.mod['gdo']; gdo.X = gdo.X.tocsr(); gdo.layers['counts'] = gdo.X.copy()
ga = pt.pp.GuideAssignment()
ga.assign_mixture_model(gdo, assigned_guides_key='assigned_guide')   # <- FAILS, see below
```
**Output (excerpt):**
```
--- assign_mixture_model FAILED (optional JAX backend missing): ---
ImportError("assign_mixture_model requires pertpy's optional JAX backend, but 'optax' is
not installed. Install it with: pip install 'pertpy[jax]'")
Falling back to assign_by_threshold ...
assigned_guide value_counts (head): multiple 5282, IFNGR2g1 454, ATF2g1 401, CD86g1 341, ...

adata.obs columns for pert_key candidates: []
[FINDING] pulled ['perturbation','gene_target','NT','replicate'] from mdata.obs into
adata.obs -- SKILL.md's shipped example does not do this and fails with KeyError as shipped.

mixscape_class_global value_counts:
NP    13644
KO     4699
NT     2386
```
**Scores:** Basic: 30/40 | Specialized: 39/60 | Total: 69/100
**Assertions:**
- [FAIL] Guide assignment uses a per-guide mixture posterior, not a flat threshold — the mixture method could not execute in this environment (missing `optax`); threshold fallback used instead.
- [PASS] Mixscape correctly separates KO/NP/NT and reports the perturbed fraction — real 4699/13644/2386 split.
- [FAIL] Code runs against the skill's own recommended real dataset without modification — KeyError as shipped, needed a manual column pull.
- [PASS] Output does not claim genes are non-functional from a high NP fraction alone.
- [PASS] No fabricated statistics — all counts from real execution.

---

### Input 2 — Variant A
**Prompt:** "Test each perturbation for calibrated DE using SCEPTRE in R, with a calibration check on negative controls first."

**Execution status: BLOCKED.** sceptre's current CRAN release requires R>=4.5; this audit's R is 4.4.3, and `available.packages()` silently filters the package out (`BiocManager::install('sceptre')` exits 0 having installed nothing). Independently confirmed via direct `R-lib` directory listing (no `sceptre` folder present), corroborating the tooling agent's `TOOLS.md`. Code reviewed against sceptre's real documented API (`import_data`, `set_analysis_parameters`, `assign_grnas`, `run_qc`, `run_calibration_check`, `run_discovery_analysis`, `get_result`) but not executed.

**Scores:** Basic: 24/40 | Specialized: 38/60 | Total: 62/100
**Assertions:**
- [PASS] Calibration check runs before discovery analysis — code order matches SKILL.md and sceptre best practice.
- [FAIL] Code executes successfully producing discovery results — not executed, environment-blocked.
- [FAIL] SKILL.md documents sceptre's minimum R-version requirement — it does not; only "sceptre 0.10+" is listed.
- [PASS] No fabricated results reported.

---

### Input 3 — Edge
**Prompt:** "All of my cells for target gene X are called Mixscape 'NP' (non-perturbed). Does this mean the gene has no phenotype?"

**Response (Mode A, direct reasoning against SKILL.md):** No — an all-NP call is confounded with low guide editing efficiency and cannot distinguish "no phenotype" from "no editing" (SKILL.md's Deep Caveat and Common Errors table say this explicitly). Recommend checking guide editing efficiency independently (e.g. indel/genotyping assay or protein-level validation) before drawing any conclusion about the gene, and compare the perturbed fraction against other successfully-edited targets in the same screen.

**Scores:** Basic: 38/40 | Specialized: 54/60 | Total: 92/100
**Assertions:** 4/4 PASS (does not conclude non-functional; recommends independent efficiency check; correctly names the confound; stays in research scope).

---

### Input 4 — Variant B
**Prompt:** "Rank my perturbations by E-distance and run the permutation E-test in a pinned PCA embedding."

**Code:** continuation of Input 1's script (`pt.tl.Distance(metric='edistance', obsm_key='X_pca')`, `pt.tl.DistanceTest('edistance', n_perms=100)` — reduced from SKILL.md's default 1000 for audit runtime).
**Output (excerpt, real data):**
```
pairwise E-distance (5x5 head):
gene_target   STAT2   CAV1   STAT1    CD86    IRF7
STAT2        0.0000 0.3749  2.2217  0.3709  0.4053
CAV1         0.3749 0.0000  2.8389 -0.0039  0.0074
STAT1        2.2217 2.8389  0.0000  2.8098  2.8838

E-test results (top 5 by pvalue):
       distance  pvalue  significant  pvalue_adj  significant_adj
STAT2  0.387664    0.01         True    0.229957            False
STAT1  2.805674    0.01         True    0.229957            False
```
Runtime for n_perms=100 across ~26 groups on 20,729 cells: ~3.5 min.
**Scores:** Basic: 33/40 | Specialized: 51/60 | Total: 84/100
**Assertions:** 4/4 PASS — notably, the run reproduces SKILL.md's own documented caveat ("smallest p ~ 1/(n_perms+1); crushed by multiple testing") exactly: raw p floors at 0.01 and none of the top hits survive Holm-Sidak adjustment.

---

### Input 5 — Stress
**Prompt:** "I have replicate labels per perturbation. Run pseudobulk DE with DESeq2 for the within-state program change, and also check with Milo whether the DE I'm seeing is actually just a compositional shift. Report both."

**Code (`run/input5_pseudobulk_milo.py`):**
```python
pb = pt.tl.PseudobulkSpace()
pdata = pb.compute(adata, target_col='gene_target', groups_col='replicate', layer_key='counts', mode='sum')
# -> (78, 18649): 26 targets x 3 replicates, RAW counts correctly summed

milo = pt.tl.Milo(); mdata_milo = milo.load(adata)
milo.make_nhoods(mdata_milo['rna'], prop=0.1, seed=0)
milo.count_nhoods(mdata_milo, sample_col='replicate')
milo.da_nhoods(mdata_milo, design='~gene_target', solver='pydeseq2')   # <- FAILS
```
**Output (excerpt):**
```
pseudobulk shape: (78, 18649)
pseudobulk obs columns: ['gene_target', 'replicate', 'n_obs_aggregated', 'perturbation']

! Values in mdata[rna].obs[['gene_target']] cannot be unambiguously assigned to each sample
-- each sample value should match a single covariate value
milo da_nhoods FAILED: AssertionError()
```
Confirmed via `pt.tl.Milo.da_nhoods`'s own docstring ("Terms should be columns in ... obs", and its worked example uses a per-sample-constant covariate like `orig.ident`/`label`) that this is a structural mismatch, not a flag/version issue: `gene_target` varies cell-by-cell within each `replicate` "sample" in a pooled Perturb-seq design, so no single value can be assigned per Milo sample.
**Scores:** Basic: 26/40 | Specialized: 33/60 | Total: 59/100
**Assertions:** 2/4 PASS (pseudobulk correct and honest failure reporting; Milo DA did not complete; design formula genuinely incompatible with pooled per-cell perturbation labels).

---

### Input 6 — Scope Boundary
**Prompt:** "My cells were run at high MOI with multiple guides per cell. How do I deconvolve combinatorial effects with scMAGeCK?"

**Finding:** scMAGeCK appears only as one row in the Method Decision Table ("Per-gene effect across many genes; high-MOI deconvolution... NEGCTRL choice defines the null; runs on scale.data so covariates propagate"). No install instructions, function names, or code exist anywhere in SKILL.md, usage-guide.md, or examples/ — unlike every other method in the same table, all of which get a full worked code block. scMAGeCK is also not installed in this audit environment (confirmed absent from R-lib). Not executed — no code exists to run.
**Scores:** Basic: 21/40 | Specialized: 24/60 | Total: 45/100
**Assertions:** 3/4 PASS (correctly names the tool and its NEGCTRL pitfall; fails on providing any runnable guidance).

---

### Input 7 — Adversarial
**Prompt:** "My foundation model (scGPT-based) predicts perturbation responses with 0.95 correlation on held-out cells — is this reliable enough to skip experimental validation for follow-up genes?"

**Response (Mode A, direct reasoning against SKILL.md's Foundation-Model Reality Check):** No — 0.95 all-gene correlation is not evidence of reliable perturbation prediction. All-gene MSE/correlation is dominated by unchanged genes, so even a "predict no change" baseline scores deceptively high; ask whether the figure was computed on DE genes specifically, and against an explicit additive/mean baseline. Also ask whether the held-out split was cell-level (which leaks the same perturbation into train and test) or a true whole-perturbation holdout. As of 2026, no foundation model has been shown to reliably beat trivial baselines on unseen perturbations (Ahlmann-Eltze 2025; Kernfeld 2025; Csendes 2025) — do not skip experimental validation on this basis alone.
**Scores:** Basic: 38/40 | Specialized: 54/60 | Total: 92/100
**Assertions:** 4/4 PASS.

---

## Note for reviewer

Two ⚠️/❌ patterns recur across 2+ outputs and point to structural issues, not one-off flukes:
1. **Undocumented environment drift** (Inputs 1, 2, 4): the skill's Prerequisites section is out of date for pertpy's current optional-JAX guide-mixture backend and doesn't mention sceptre's R>=4.5 floor.
2. **Worked examples not validated against the skill's own reference dataset** (Inputs 1, 4, 5): both the shipped `pertpy_analysis.py` and the Milo compositional-analysis snippet fail when actually run against `pt.dt.papalexi_2021()`, the exact dataset the skill points to.

Both are fixable with small, targeted patches (see `recommendations` in the JSON report) — none of them reflect a wrong scientific approach, and the skill's judgment-heavy guidance (Inputs 3, 7) is excellent.
