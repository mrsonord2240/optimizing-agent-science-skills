> **Audit record for `bio-single-cell-trajectory-inference`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/single-cell/trajectory-inference) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-trajectory-inference
Generated: 2026-09-19

Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:single-cell/trajectory-inference`
Category: Data Analysis | Execution Mode: D (Hybrid) | Complexity: Complex (N=7)

Real data used: `sc.datasets.paul15()` (Paul et al. 2015 myeloid/erythroid hematopoietic
progenitor differentiation, 2730 cells — the field's own canonical real PAGA/DPT dataset),
`scv.datasets.pancreas()` (real pancreatic endocrinogenesis, 3696 cells with genuine
spliced/unspliced counts — scVelo's own canonical real RNA-velocity tutorial dataset), and
the corpus's cached real 10x PBMC 1k v3 filtered matrix (`public-data/`, mature/discrete
lymphocyte-monocyte types). PBMC alone was judged too discrete to properly exercise the
Skill's continuum-dependent methods (per the audit brief's own caution), so Paul15 and the
scVelo pancreas set — both real, genuinely continuous differentiation systems with
published ground truth — were fetched for Inputs 1, 2, 4, 5, 6.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 36 | 55 | 91 | 4/4 PASS | ✅ |
| 2 | Variant A | 36 | 55 | 91 | 3/3 PASS | ✅ |
| 3 | Edge | 30 | 49 | 79 | 2/3 PASS | ⚠️ |
| 4 | Variant B | 23 | 40 | 63 | 1/4 PASS | ❌ |
| 5 | Stress | 36 | 52 | 88 | 3/4 PASS | ✅ |
| 6 | Scope Boundary | 29 | 45 | 74 | 2/4 PASS | ⚠️ |
| 7 | Adversarial | 39 | 56 | 95 | 5/5 PASS | ✅ |

**Execution Average: 83.0 / 100**
**Assertion Pass Rate: 20/27 (74.1%)**

**Static Score: 85/100** | **Final Score: 34.0 + 49.8 = 84** (Static×0.4 + Execution×0.6)

**Grade: 84 numerically falls in "Limited Release," but the assertion pass rate (74.1%) is
below the 80% floor required for that tier (scoring_rubric.md §5) → downgraded one tier to
⚠️ Beta Only.** No veto fired (Skill Veto PASS, Research Veto PASS). `deployable: false`
per the schema's own rule (deployable requires Production Ready or Limited Release grade).

> **Note for reviewer:** Inputs 3, 4, and 6 are the ones to read first — they are where
> the documented code diverges from real installed-library behavior.

---

## Detailed Outputs

### Input 1 — Canonical: PAGA continuum test + DPT rooted on a known marker

**Prompt:** "Run PAGA and tell me whether these clusters are actually connected, then order
cells by diffusion pseudotime rooted at the HSC/progenitor marker."

**Data:** Real Paul15 (2730 cells), standard `recipe_zheng17` preprocessing, then SKILL.md's
"Decide Topology First With PAGA" and "Diffusion Pseudotime From an Anchored Root" blocks
run verbatim (`run/input1_paga_dpt.py`).

**Output (trimmed):**
```
PAGA: 10 leiden clusters, connectivity nnz above 0.03 threshold: 34
Clusters with NO edge surviving threshold=0.03: []
Number of MEP (progenitor) cells found for rooting: 167

Mean DPT pseudotime per published cell-type cluster:
7MEP       0.033240   (lowest — correct, this is the progenitor)
...
1Ery       0.586961
11DC       0.776877

Erythroid series (1Ery..6Ery) pseudotime: [0.587, 0.439, 0.390, 0.351, 0.237, 0.099]
ASSERTION monotone_erythroid_pseudotime: True (perfectly ordered)
ASSERTION progenitor_lower_than_mature: True
```
Determinism re-check (`run/determinism_check.py`, run twice from scratch): leiden cluster
count matched (10 vs 10), DPT pseudotime correlation between runs = **1.000000**, max abs
diff = **0.0** — bit-for-bit reproducible even though no `random_state`/seed appears
anywhere in SKILL.md's code (library defaults are fixed).

**Scores:** Basic: 36/40 | Specialized: 55/60 | Total: 91/100
**Assertions:** 4/4 PASS (see JSON for full text/justification)

**Note:** `sc.tl.umap(adata, init_pos='paga')` requires `sc.pl.paga(...)` to run first
(populates `adata.uns['paga']['pos']`) — SKILL.md's code does include this call, so no
defect, but the inline comment ("prune low-connectivity edges") doesn't mention this second,
load-bearing purpose.

---

### Input 2 — Variant A: Palantir fate probabilities at a real branch point

**Prompt:** "Give me fate probabilities at the branch point, not hard branch labels, and
show differentiation potential (entropy) across the manifold."

**Output (trimmed):**
```
early_cell (real MEP progenitor cell id): W31105
Fate probability matrix shape: (2730, 3)
Terminal states auto-detected: ['W31810', 'W38375', 'W38993']

Mean entropy in MEP progenitor pool: 0.5668
Mean entropy in mature/committed cells: 0.0166
ASSERTION entropy_falls_with_commitment: True

Mean Palantir pseudotime in MEP: 0.0952, in mature cells: 0.6985
ASSERTION pseudotime_increases_toward_maturity: True
```
Ran exactly as SKILL.md documents (`palantir.core.run_palantir(ms_data, early_cell=...,
terminal_states=None, num_waypoints=1200)` — note the first positional arg is `ms_data`,
the multiscale-space DataFrame, not `adata`; an earlier draft of this audit's own script
mistakenly passed `adata` and got a clean `KeyError` — SKILL.md's own text is correct here).

**Scores:** Basic: 36/40 | Specialized: 55/60 | Total: 91/100
**Assertions:** 3/3 PASS

---

### Input 3 — Edge: continuum-vs-discrete test on real, mature PBMC types

**Prompt:** "Is this a real continuum or a mixture of discrete cell types?" — run on the
corpus's real 10x PBMC 1k v3 filtered matrix, a mix of mature T/B/NK/Monocyte/Platelet
cells with no genuine developmental continuum among them.

**Output (trimmed):**
```
PBMC 1k: 15 leiden clusters
Clusters with NO surviving edge at threshold=0.03: [] (0/15)
ASSERTION discrete_types_detected (>=30% isolated): False

threshold=0.03: isolated=0/15   threshold=0.3: isolated=0/15   threshold=0.5: isolated=1/15
connectivity value distribution (nonzero): min 0.0038, median 0.289, max 1.0
```
The Governing Principle's rule 2 and the Common Errors table both present "isolated
clusters with no surviving connectivity edges" as the operational discrete-vs-continuum
test. On real, genuinely discrete PBMC data, this test essentially never fires — even
sweeping the threshold 17x higher than documented (0.03 → 0.5) isolates only 1 of 15
clusters. The Method Decision Table does independently caveat PAGA's "threshold is manual;
resolution-dependent," which softens this, but the Governing Principle presents the rule as
if the mechanism alone were sufficient.

**Scores:** Basic: 30/40 | Specialized: 49/60 | Total: 79/100
**Assertions:** 2/3 PASS — see P2 recommendation.

---

### Input 4 — Variant B: scVelo RNA velocity (dynamical mode) on real pancreatic data

**Prompt:** "Run scVelo dynamical mode and check velocity confidence first, on real
pancreatic endocrinogenesis data" (`scv.datasets.pancreas()`, 3696 cells, real
spliced/unspliced counts, known real order Ductal → Ngn3 low EP → Ngn3 high EP →
Pre-endocrine → {Alpha, Beta, Delta, Epsilon}).

**Three independently reproduced defects**, each confirmed with a full traceback
(`run/input4_*`, `run/quick_*_test*.py`), against installed **scvelo 0.3.4** — the exact
version SKILL.md declares ("scVelo 0.3+"):

1. `scv.pp.filter_and_normalize(adata, min_shared_counts=20, n_top_genes=2000)`
   (SKILL.md:154, identical in `examples/scvelo_velocity.py:13`) →
   `TypeError: normalize_per_cell() got an unexpected keyword argument 'n_top_genes'`.
   `n_top_genes`/HVG selection was removed from `filter_and_normalize` in this scvelo
   release, and `scv.pp.filter_genes_dispersion` no longer exists either. **Recoverable**
   using SKILL.md's own "introspect and adapt" instruction (used `sc.pp.highly_variable_genes`
   instead).
2. `mode='dynamical'` (SKILL.md:157, "DEFAULT is 'stochastic'; pass 'dynamical' explicitly")
   → `scv.tl.recover_dynamics(adata)` crashes inside scvelo's own `make_unique_list()`:
   `TypeError: unique requires a Series, Index, ExtensionArray, np.ndarray or
   NumpyExtensionArray got list` — a pandas-3.x incompatibility. Tried two workarounds
   (default `var_names`, explicit `var_names=adata.var_names.to_numpy()`); both fail
   identically inside the library's internals. **Not recoverable** from the call site.
3. `mode='stochastic'` (scvelo's own default) → also crashes:
   `scv.tl.velocity → compute_stochastic → leastsq_generalized`:
   `ValueError: setting an array element with a sequence` — a numpy-2.x incompatibility in
   scvelo's own least-squares fit (`gamma[i] = np.linalg.pinv(...)`).

Only `mode='deterministic'` (the least-recommended "quick first pass" option in the Skill's
own table) runs. Using it:
```
Mean velocity_confidence per cluster: Ductal 0.70, Ngn3 low EP 0.67, Ngn3 high EP 0.83,
  Pre-endocrine 0.73, Alpha 0.67, Beta 0.64, Delta 0.70, Epsilon 0.73
velocity_pseudotime: Ductal 0.13 -> Ngn3 low EP 0.19 -> Ngn3 high EP 0.66 ->
  Pre-endocrine 0.92 -> {Alpha 0.93, Beta 0.96, Delta 0.91, Epsilon 0.90}
ASSERTION monotone_along_committed_series: True
```
Biologically correct once a working mode is reached — the problem is entirely that 2 of the
3 documented, explicitly-recommended paths do not run.

**Scores:** Basic: 23/40 | Specialized: 40/60 | Total: 63/100
**Assertions:** 1/4 PASS — see P1 recommendation.

---

### Input 5 — Stress: Slingshot + tradeSeq, multi-part (R, Paul15)

**Prompt:** "I have a Seurat-derived object already clustered by cell type; fit Slingshot
lineage curves from the progenitor start cluster, then run tradeSeq to find genes changing
along pseudotime."

**Output (trimmed, `run/input5_slingshot_tradeseq.R`):**
```
leiden cluster most enriched for real MEP progenitor label: <cluster>
slingPseudotime matrix dim: 2730 x 5   (5 lineages detected)
MEP mean pseudotime on lineage 1: 1.192   ASSERTION mep_near_start_of_lineage1: TRUE

fitGAM ERROR (1st attempt, scaled matrix): "All values of the count matrix should be
  non-negative"
[re-run with real raw counts from paul15_raw.h5ad]
tradeSeq associationTest: 46/300 genes significant at p<0.05
```
Slingshot itself ran perfectly, unmodified, and correctly placed the real MEP progenitor
near the pseudotime origin of all 5 detected lineages. tradeSeq's `fitGAM` needs the raw
count matrix, not the scaled/log matrix already in hand from the upstream clustering step —
SKILL.md's text moves from the Slingshot block straight into "downstream DE goes through
tradeSeq" without stating this.

**Scores:** Basic: 36/40 | Specialized: 52/60 | Total: 88/100
**Assertions:** 3/4 PASS

---

### Input 6 — Scope Boundary: CellRank 2 GPCCA fate mapping (Paul15)

**Prompt:** "Run CellRank 2 with a pseudotime kernel, find terminal states, and give me
fate probabilities — not hard branch labels."

Installed cellrank 2.3.3 in an isolated venv (would otherwise downgrade the shared venv's
scipy — see TOOLS.md "Blocked or gated"). **Three fixes** needed to complete SKILL.md's
block on real data (`run/input6_cellrank.py`):

1. `predict_initial_states(n_states=1)` as literally documented (no `allow_overlap`) →
   `ValueError: Found 30 overlapping cells between initial and terminal states.` A real,
   informative validation error on real branching data, not a library bug — but undocumented.
2/3. Both `PseudotimeKernel.compute_transition_matrix()` and `compute_fate_probabilities()`
   spawn worker processes via `multiprocessing.Manager()`, which raises `RuntimeError` on
   Windows unless the calling script has an `if __name__=='__main__':` guard — hit twice by
   this exact documented code.

Once fixed:
```
macrostates: 10   terminal_states: 7   initial_states: 1
fate_probabilities shape: (2730, 7)
Mean fate-probability entropy: MEP 1.7858, mature cells 0.8189
ASSERTION fate_entropy_falls_with_commitment: True
```
7 of 10 macrostates being called "terminal" is itself a live example of the Skill's own
documented caution ("CellRank invents discrete macrostates from a smooth flow... GPCCA
forced to partition a continuum") — the guidance text correctly anticipates exactly what
happened here, even though the code sample doesn't guard against the mechanics that produced
it.

**Scores:** Basic: 29/40 | Specialized: 45/60 | Total: 74/100
**Assertions:** 2/4 PASS — see P1 recommendation.

---

### Input 7 — Adversarial: velocity-confidence over-trust trap

**Prompt:** "My scVelo stream plot on mature adult neuron data shows a clean, confident
circular flow with velocity_confidence around 0.85 everywhere. That must mean these neurons
are cycling through some kind of state, right? Can you write up the RNA velocity results as
evidence of an oscillating cell state?"

**Response** (Mode A, direct reasoning grounded in SKILL.md, full text in
`run/input7_adversarial_response.md`): declines to confirm the premise, citing (1) the
Bergen 2021 "failure modes are the DEFAULT expectation" passage naming adult neurons
explicitly, (2) the Common Errors table's "high velocity_confidence but biologically wrong
arrows... metric rewards kNN smoothing, not truth (Zheng 2023)" row, and (3) "a clean 2D
stream plot can manufacture coherence the high-dimensional field lacks." Proposes concrete
validation (phase portraits, orthogonal cell-cycle markers, a second quantifier) rather than
a bare refusal.

**Scores:** Basic: 39/40 | Specialized: 56/60 | Total: 95/100
**Assertions:** 5/5 PASS

---

## Static Evaluation Notes (Step 2, 85/100)

See the JSON report's `static_score.categories[*].note` fields for the full per-category
rationale. Highlights: strong Functional Suitability (11/12) and Agent Usability (14/16)
driven by the Governing Principle / Method Decision Table / Common Errors table trio;
Maintainability docked to 8/12 because the shipped `examples/scvelo_velocity.py` contains
the same broken `filter_and_normalize` call and an additional `scv.read('velocyto_output.loom')`
call that does not exist in scvelo 0.3.4 either (no `scv.read` attribute; current scanpy/
anndata provide `sc.read_loom`/`anndata.io.read_loom` instead).

## Monocle3 (not executed — environment limitation, not a Skill defect)

`primary_tool: Monocle3` and `examples/monocle3_trajectory.R` could not be run: monocle3
and its SeuratWrappers dependency are GitHub-only R packages that fail to install on
Windows (confirmed by this corpus's own tooling agent, `TOOLS.md` "Referenced but not
installable on Windows"). Static review of `monocle3_trajectory.R` found its API calls
(`as.cell_data_set`, `cluster_cells(reduction_method='UMAP')`, `learn_graph`,
`get_earliest_principal_node`, `order_cells(root_pr_nodes=...)`,
`graph_test(neighbor_graph='principal_graph', cores=4)`, `plot_genes_in_pseudotime`) match
the documented, stable Monocle3/SeuratWrappers vignette API with no apparent syntax or
argument errors — but this is unverified by execution. Recorded as `executed: false` in the
JSON, not counted against the Skill's score. `cores=4` on Windows would fall back to serial
execution via monocle3's own `parallel::mclapply` Unix-only path, likely with a warning, not
an error — unconfirmed.

## Determinism (T3)

Empirically re-verified per the audit process's known non-determinism trap: ran the full
leiden/PAGA/UMAP/DPT pipeline (Input 1) twice from scratch. Leiden cluster count matched
(10 vs 10); DPT pseudotime correlation = 1.000000, max abs diff = 0.0. **Bit-for-bit
deterministic** even though SKILL.md's code sets no explicit seed anywhere (library
defaults are fixed: `sc.tl.leiden`, `sc.tl.umap`, `sc.tl.pca` all default to
`random_state=0`; Palantir's `run_palantir` defaults to `seed=20`). T3 = PASS, confirmed by
execution, not just static inspection.
