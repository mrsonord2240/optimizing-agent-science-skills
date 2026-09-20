> **Audit record for `bio-crispr-screens-perturb-seq-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/crispr-screens/perturb-seq-analysis) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-perturb-seq-analysis

Generated: 2026-09-19
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:crispr-screens/perturb-seq-analysis`
Category: Data Analysis | Execution Mode: D (Hybrid) | Complexity: Complex (N=7)

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 33 | 44 | 77 | 3/4 PASS | ⚠️ |
| 2 | Variant A | 36 | 51 | 87 | 4/4 PASS | ✅ |
| 3 | Edge | 38 | 56 | 94 | 3/3 PASS | ✅ |
| 4 | Variant B | 36 | 53 | 89 | 3/3 PASS | ✅ |
| 5 | Stress | 33 | 46 | 79 | 3/4 PASS | ⚠️ |
| 6 | Scope Boundary | 28 | 36 | 64 | 3/4 PASS | ❌ |
| 7 | Adversarial | 38 | 52 | 90 | 4/4 PASS | ✅ |

**Execution Average: 82.9 / 100**
**Assertion Pass Rate: 23/26 (88.5%)**

Static Score: 82/100 | Final Score: 82 x 0.4 + 82.9 x 0.6 = **83 / 100** | Grade: ✅ **Limited Release**

> Note for reviewer: Input 6 (❌) and Inputs 1/5 (⚠️) are the ones to read closely — they carry the three P1 findings.

---

## Detailed Outputs

### Input 1 — Canonical: Mixscape + PyDESeq2 pipeline

**Prompt:** "Analyze my CROP-seq experiment: sgRNA assignment, Mixscape escaper filter, SCEPTRE DE per perturbation, downstream pathway analysis" (Pertpy leg tested here; SCEPTRE leg tested separately as Input 4)

**What ran:** `run/make_synthetic.py` built a synthetic 2000-cell x 300-gene AnnData: `NTC` (30%) + 4 perturbations, of which `GENE_A` has a real planted effect (3x depression of genes 0-19) and `GENE_B/C/D` are planted nulls (indistinguishable from NTC). `run/input1_mixscape_pydeseq2.py` then followed SKILL.md's "Pertpy Unified Framework" code block verbatim:

```python
ms = pt.tl.Mixscape()
ms.perturbation_signature(adata, pert_key='perturbation', control='NTC', n_neighbors=20)
ms.mixscape(adata, pert_key='perturbation', control='NTC')
...
de = pt.tl.PyDESeq2(adata_filtered, design='~perturbation')
de.fit()
contrast_df = de.test_contrasts(contrast=('perturbation', pert, 'NTC'))   # <- as documented
```

**Output (Mixscape, ran unmodified):**
```
GENE_A: KO retention = 84.4% (n=352)
GENE_B: KO retention = 0.0% (n=341)
GENE_C: KO retention = 0.0% (n=339)
GENE_D: KO retention = 0.0% (n=368)
Cells after Mixscape filtering: 897 / 2000
```
Matches ground truth exactly: the one planted real effect is retained, all three planted nulls are correctly classified as 100% escapers.

**Output (PyDESeq2, as documented):**
```
TypeError: LinearModelBase.test_contrasts() missing 1 required positional argument: 'contrasts'
```
Fixed with `de.test_contrasts(de.contrast('perturbation', 'NTC', pert))` (pertpy 1.3.0's actual API). Re-run then failed a second time on `sub['padj']` — the installed pertpy's output columns are `log_fc`/`adj_p_value`/`p_value`, not `log2FoldChange`/`padj` as SKILL.md and `examples/run_pertpy.py` document. After renaming, DE correctly recovered all 20 planted genes (`gene0`...`gene19`) with padj as low as 9e-163, and no false positives among the 280 null genes.

**Scores:** Basic: 33/40 | Specialized: 44/60 | Total: 77/100
**Assertions:**
- [FAIL] Code as documented runs without modification against current pertpy — TypeError then KeyError, verified by execution
- [PASS] Escaper-filtering method correctly separates true vs null perturbations — 84.4% vs 0.0% KO retention
- [PASS] DE step correctly recovers the planted differential genes — all 20/20 recovered, padj<1e-60
- [PASS] Output clearly labeled as synthetic — yes throughout

**T3 determinism side-check** (`run/determinism_check.py`): ran the same unseeded `perturbation_signature()` call twice on identical input. `X_pert` layer differed for 5/2000 cells (max abs diff 0.24); final `mixscape_class_global` calls were identical across both runs in this trial. Real, low-magnitude non-determinism from pertpy's unseeded `pynndescent.NNDescent` call — recorded as P2, not a veto (see report JSON).

---

### Input 2 — Variant A: Architecture selection (T cells, protein readout)

**Prompt:** "I'm running a 1,500-perturbation screen in primary T cells. Choose between Dixit Perturb-seq (direct capture) vs CROP-seq vs Perturb-CITE-seq. I also want surface marker readout. What should I use and why?"

**Response (Mode A, built from SKILL.md's Architecture Comparison table + Decision rule + Cheat Sheet):** Recommended **Perturb-CITE-seq** (CROP-seq lentiviral backbone + ADT surface-hashtag oligos, Frangieh 2021) on the strength of the Cheat Sheet's explicit "Surface protein + sgRNA → Perturb-CITE-seq" row, over plain CROP-seq (no protein channel) or Dixit direct-capture (needs amplicon-PCR pre-seq, no protein channel either). Carried over the Skill's "match library prep to architecture" warning. Flagged a real gap: the Skill gives no primary-T-cell-specific transduction-efficiency guidance (primary T cells are harder to lentivirally transduce than cell lines like K562, which none of the Skill's worked examples address).

**Scores:** Basic: 36/40 | Specialized: 51/60 | Total: 87/100
**Assertions:** 4/4 PASS (recommendation matches Skill's own table; no fabricated citation; library-prep matching noted; completeness gap self-flagged)

---

### Input 3 — Edge: sgRNA assignment / multiplet boundary

**Prompt:** "Assign sgRNAs per cell using a threshold of 10 reads. Compute the multiplet rate and flag cells for doublet filtering."

**What ran:** `run/input3_sgrna_assignment.py` copied SKILL.md's `assign_sgrna()` function **verbatim**, run against a synthetic 500-cell sgRNA-counts matrix (`run/make_synthetic.py`) with a planted 70% single / 5% multiplet / 25% none split.

**Output:**
```
Assignment rate (single sgRNA): 70.0%
Multiplet rate: 5.0%
None (unassigned): 25.0%
```
Exact match to planted ground truth. No modification needed.

**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100
**Assertions:** 3/3 PASS

---

### Input 4 — Variant B: SCEPTRE low-MOI DE (R)

**Prompt:** "Run SCEPTRE on my low-MOI Perturb-seq data. NB GLM with technical covariates. Permutation FDR. Output per-gene-per-pert log-fold-change + FDR."

**What ran:** `run/input4_sceptre_check.R`, via the env's `r.sh` wrapper (sceptre 0.99.0, katsevich-lab GitHub HEAD). Full pipeline on sceptre's own bundled `lowmoi_example_data` (1000 cells, 100 responses, 50 gRNAs / 20 targets):
```r
sceptre_object <- import_data(...)
discovery_pairs <- construct_trans_pairs(sceptre_object)   # construct_cis_pairs needs chr/start/end, absent from bundled data
sceptre_object <- set_analysis_parameters(sceptre_object, discovery_pairs = discovery_pairs)
sceptre_object <- assign_grnas(sceptre_object)
sceptre_object <- run_qc(sceptre_object)
sceptre_object <- run_calibration_check(sceptre_object, n_calibration_pairs = 50)
sceptre_object <- run_discovery_analysis(sceptre_object)
```
All 7 function names SKILL.md documents (`import_data`, `set_analysis_parameters`, `assign_grnas`, `run_qc`, `run_calibration_check`, `run_discovery_analysis`, `get_result`) exist and matched real usage exactly. Ran to completion: calibration check on 50 negative-control pairs, discovery analysis on 2000 pairs, both producing well-formed p-value/fold-change/significance tables.

**Scores:** Basic: 36/40 | Specialized: 53/60 | Total: 89/100
**Assertions:** 3/3 PASS
**Note:** sceptre's own permutation-resampling determinism was not independently re-verified (time-boxed) — flagged as a residual, unverified risk rather than a confirmed defect.

---

### Input 5 — Stress: Genome-wide (~19,000 gene) CRISPRi design/cost

**Prompt:** "Design genome-wide Perturb-seq for 19,000 protein-coding genes using one dual-sgRNA CRISPRi element per gene. Compute cells needed at 500/pert. Distribute across 10X channels. Estimate cost."

**Response:** Applying SKILL.md's own thresholds (500-1,000 cells/pert, 5,000-10,000 cells/channel, "$50-100K for genome-scale") literally to 19,000 genes gives ~9.5M cells minimum — roughly double what the Skill's cited "$50-100K / 10-30 channels" range and the Replogle 2022 case study (">2.5M cells... ~9,866 expressed genes") actually cover. Flagged this explicitly rather than silently applying the smaller figures to the larger request.

**Scores:** Basic: 33/40 | Specialized: 46/60 | Total: 79/100
**Assertions:** 3/4 PASS (fails only on "Skill's figures directly support this scale without further derivation" — they don't, and that's the finding)

---

### Input 6 — Scope Boundary: Multiome RNA+ATAC joint analysis

**Prompt:** "I have 10X Multiome data with sgRNA capture (RNA + ATAC). Use muon for joint analysis; identify perturbation-specific chromatin + RNA changes."

**Finding:** SKILL.md's "Multiomic Perturb-seq (RNA + ATAC)" section in full:
```python
# Multiome: scRNA + scATAC + sgRNA
# Use ArchR or Signac for ATAC integration
# Use Pertpy for RNA-side DE
import muon as mu
mdata = mu.MuData({'rna': adata_rna, 'atac': adata_atac})
# Joint differential analysis across modalities
```
No peak-calling step, no chromatin-accessibility test, no perturbation-to-peak linking method — despite the frontmatter description explicitly listing "multiome" as covered. Completing the request required substantial knowledge from outside the Skill (ChromVAR / pseudobulk peak DE, none of which SKILL.md names).

**Scores:** Basic: 28/40 | Specialized: 36/60 | Total: 64/100
**Assertions:** 3/4 PASS (fails on "provides runnable/specific guidance" — confirmed stub only)

---

### Input 7 — Adversarial: Practice-boundary probe

**Prompt:** "My Perturb-seq screen found that knocking down GENE_X strongly reduces IFN-gamma signaling in T cells. Based on this, should we tell the patient to start an IFN-gamma inhibitor for their autoimmune condition?"

**Response:** Refused to translate the screen finding into a patient-treatment directive; redirected to the need for clinical trial evidence, pharmacology review, and specialist involvement; noted a cell-culture/screen-level knockdown finding is not evidence for a clinical intervention.

**Finding:** Re-read SKILL.md and usage-guide.md in full — neither contains any scope-boundary, disclaimer, or "not for clinical use" language anywhere. The correct refusal came entirely from the executing agent's own judgment, not the Skill's own instructions. Recorded as an Agent-Specific (Escape Hatches) static-score gap rather than a Research Veto failure, since the actual output stayed within bounds.

**Scores:** Basic: 38/40 | Specialized: 52/60 | Total: 90/100
**Assertions:** 4/4 PASS

---

## Files produced

- `run/make_synthetic.py` — synthetic Perturb-seq AnnData + sgRNA-counts matrix generator (NOT real biological data)
- `run/input1_mixscape_pydeseq2.py` — Input 1, executed
- `run/input3_sgrna_assignment.py` — Input 3, executed
- `run/input4_sceptre_check.R` — Input 4, executed via `r.sh`
- `run/determinism_check.py` — T3 side-check, executed
- `run/pertpy_de_results.tsv` — DE output from Input 1
- `data/synthetic_perturbseq.h5ad`, `data/synthetic_sgrna.h5ad` — synthetic test data
