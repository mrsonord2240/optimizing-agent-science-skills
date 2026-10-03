> **Audit record for `bio-machine-learning-atlas-mapping`**
> - Audited working candidate `d4048dcc887b51c820dba4669bf05620829970e083f7512d24a2539953ad48a6`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/machine-learning/atlas-mapping), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-machine-learning-atlas-mapping

Generated: 2026-10-03  
Audit type: bounded diagnostic initial audit  
Exact candidate content SHA-256: `d4048dcc887b51c820dba4669bf05620829970e083f7512d24a2539953ad48a6`

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 34 | 45 | 79 | 3/5 | ✅ COMPLETED |
| 2 | Variant A | 33 | 45 | 78 | 3/5 | ✅ COMPLETED |
| 3 | Edge | 33 | 45 | 78 | 3/4 | ✅ COMPLETED |
| 4 | Variant B | 35 | 50 | 85 | 2/4 | ✅ COMPLETED |
| 5 | Stress | 24 | 37 | 61 | 3/5 | ⚠️ COMPLETED |

**Execution average:** 76.2 / 100  
**Assertion pass rate:** 14 / 23  
**Static score:** 79 / 100  
**Final score:** 77 / 100 — ✅ Limited Release  
**Research veto:** PASS

This score is diagnostic. It does not make the candidate ready. Findings are ordered in the ledger below; exact identity is in [`source-identity.json`](source-identity.json).

## Executed versus static-only

| Surface | Classification | Evidence |
|---|---|---|
| scripts/scarches_annotation.py | executed | scripts/canonical_scored.py runs it unmodified twice (logs/canonical_a.log, canonical_b.log) |
| scripts/ood_gating_demo.py | executed | logs/ood_gating_demo.log |
| SKILL.md snippets 1-3 (saved-model route, predict(soft=True), kNN gate) | executed | scripts/saved_model_surgery.py, logs/saved_model_surgery.log |
| Held-out-type OOD behavior (B cells, Monocytes removed) | executed | scripts/heldout_ood.py, logs/heldout_Bcells.log, heldout_Mono.log |
| Symphony, Azimuth/Seurat (R, prose only) | static-only (no code shipped, not exercised) | n/a |
| scPoli, popV, treeArches/scHPL, scGPT/Geneformer | static-only, reason heavy-optional (not tooled); the Skill does not label them not executed (AM-002) | n/a |

## Veto review

- Skill veto: PASS (stability, contract, determinism, security all PASS).
- Research veto: PASS
  - scientific_integrity: PASS — No fabricated citations or values; the cited methods and thresholds (HLCA 0.2 uncertainty, scIB 0.6/0.4 weighting, CellTypist log1p CP10k input) match the literature and the executed outputs.
  - practice_boundaries: PASS — Research-use single-cell annotation; no diagnostic or prescriptive medical conclusions in any output.
  - methodological_ground: PASS — The headline claim that the kNN-uncertainty gate makes labels trustworthy is overstated (held-out Monocytes: 97.3% confidently mislabelled as DC, finding AM-001), but the Skill itself prescribes spiked-in unseen-type validation and per-reference recalibration, so this is a P1 overclaim, not an inverted conclusion.
  - code_usability: PASS — Both scripts and the saved-model snippets ran on CPU (scvi-tools 1.5.1) without errors; scarches_annotation.py ran unmodified in about 90 s.

## Static categories

- functional_suitability: 8/12 — Core scArches/scANVI mapping and gating are covered and executable; the OOD-gate claim is stronger than the evidence (AM-001), and Symphony, Azimuth, scPoli, popV, treeArches and foundation models are prose only with no code or install steps.
- reliability: 7/12 — No shared-gene or input-contract check in the script (it silently needs layers['counts'], obs['batch'], obs['cell_type']); failure modes are documented in references/failure-modes.md.
- performance_context: 7/8 — SKILL.md is 176 lines with failure modes routed to a reference; the method taxonomy table is dense but useful; scripts run in about 90 s on CPU.
- agent_usability: 13/16 — Strong error prevention (projection-not-oracle framing, prepare_query_anndata warning); snippets are not self-contained (ref_vae and adata_ref undefined) and predict(soft=True) return type is unstated.
- human_usability: 7/8 — Trigger text and usage-guide prompts match how users ask; script inputs are fixed filenames in the working directory with no CLI arguments.
- security: 11/12 — No credentials, network calls, or shell execution; scripts read local h5ad files only and write nothing.
- maintainability: 9/12 — Sensible split into SKILL.md, failure-modes reference and two scripts; the gate logic is duplicated across SKILL.md, scarches_annotation.py and the demo; no seed or test assertions in the real-data script.
- agent_specific: 17/20 — Precise description with scope pointers to sibling Skills and good progressive disclosure; the real-data script is unseeded and non-persisting, so re-runs differ slightly and produce no artefact.

## Detailed outputs

### Input 1 — Canonical: scArches scANVI transfer + kNN gate, PBMC 1k v3 reference to PBMC3k query (script unmodified)

**Status:** COMPLETED — Two unmodified runs (about 90 s each, CPU): accuracy 0.965 and 0.967 against PBMC3k annotation (silver reference labels), Unknown 1.8% and 1.3%; mean uncertainty 0.003 for correct vs 0.14-0.19 for wrong calls; results differ between runs (no seed) and nothing is saved.  
**Scores:** Basic 34/40 | Specialized 45/60 | Total 79/100

**Assertions:**

- PASS — Script runs unmodified end to end on a realistic reference/query pair (rc 0 twice; reference scVI+scANVI, surgery and gate completed)
- PASS — Transferred labels agree with the independent PBMC3k annotation (accuracy >= 0.9) (0.965 and 0.967; 0.98 among non-Unknown cells)
- PASS — Gate separates wrong from right calls (mean transfer_uncertainty higher for wrong calls) (0.003 vs 0.19 and 0.002 vs 0.14)
- FAIL — Repeated runs on identical inputs give identical flagged fraction and accuracy (Unknown 1.82% vs 1.29%, accuracy 0.9647 vs 0.9666; scvi.settings.seed is never set)
- FAIL — Script persists predicted labels, latent and uncertainty for the user (Only stdout counts; no file written beyond the inputs)

### Input 2 — Variant A: SKILL.md snippets 1-3 via saved-model directories (SCVI.load, prepare_query_anndata, load_query_data, SCANVI save/load, predict(soft=True), kNN gate)

**Status:** COMPLETED — Ran with 30/20/30 epochs on CPU: scVI query latent (2638, 30); scANVI surgery; predict(soft=True) is a pandas DataFrame (2638 x 8, columns are reference labels, rows sum to 1, idxmax equals predict()); 2.6% flagged Unknown, accuracy 0.964.  
**Scores:** Basic 33/40 | Specialized 45/60 | Total 78/100

**Assertions:**

- PASS — Saved-model surgery route (directory arguments) runs end to end (SCVI and SCANVI save, prepare_query_anndata('dir'), load_query_data('dir') all succeeded)
- PASS — predict(soft=True) rows are probabilities that agree with the hard labels (row sums 1.0000; idxmax(axis=1) equals predict())
- FAIL — SKILL.md states the return type of predict(soft=True) (Says only 'per-class probabilities'; it is a DataFrame, so proba.max() returns per-class maxima and proba[:, 0] raises InvalidIndexError)
- FAIL — Snippets are copy-runnable as written (ref_vae and adata_ref are undefined in the SKILL.md snippets; the audit script had to define them)
- PASS — Gated accuracy against the independent annotation is >= 0.8 (0.964 with 2.6% flagged Unknown)

### Input 3 — Edge: Held-out cell type: remove B cells from the reference, map PBMC3k, inspect the 342 query B cells

**Status:** COMPLETED — 87.4% of held-out B cells gated Unknown (kNN uncertainty mean 0.38); 12.6% still labelled T/DC/Monocytes. A softmax >= 0.5 filter would have passed 83.6% of them. The distance gate flagged 0%.  
**Scores:** Basic 33/40 | Specialized 45/60 | Total 78/100

**Assertions:**

- PASS — Script runs unmodified on a reference lacking one cell type (rc 0; reference had 7 labels)
- PASS — At least 80% of held-out-type cells are gated to Unknown (87.4% (299 of 342))
- FAIL — At least 95% of held-out-type cells are not confidently assigned an in-reference label (43 cells (12.6%) keep a T cell, DC or Monocytes label)
- PASS — The softmax max would have been the wrong gate (passes most held-out cells) (83.6% of held-out B cells have softmax max >= 0.5 (mean 0.71))

### Input 4 — Variant B: Synthetic OOD demo scripts/ood_gating_demo.py (novel far cluster, distance gate vs kNN probability)

**Status:** COMPLETED — Deterministic (seeded): 100% of novel cells pass a 0.5 'softmax' filter, 100% flagged by the distance gate, 0% of known cells wrongly flagged. The 'softmax' here is kNN predict_proba, and the extreme separation does not transfer: on the real held-out types the same distance idea flagged 0%.  
**Scores:** Basic 35/40 | Specialized 50/60 | Total 85/100

**Assertions:**

- PASS — Demo runs without error and is reproducible (seed 0; identical output on rerun, no warnings)
- PASS — Distance gate flags the novel cluster and spares known cells (novel flagged 100%, known flagged 0%)
- FAIL — Probability filter demonstrated is the classifier softmax claimed in the docstring (It is KNeighborsClassifier.predict_proba, a different quantity from scANVI soft output)
- FAIL — Demo conclusion transfers to the real-data pair (Real held-out Monocytes: distance gate flagged 0 of 630)

### Input 5 — Stress: Held-out cell type: remove Monocytes from the reference, map PBMC3k, inspect the 630 query monocytes

**Status:** COMPLETED — Silent failure: only 2.7% gated Unknown; 95.4% (601) confidently labelled DC (mean softmax max 0.89, mean kNN uncertainty 0.013); distance gate flagged 0. In-distribution cells over-flagged only 1.2%. Caveat: silver 1,222-cell reference with only 28 DC.  
**Scores:** Basic 24/40 | Specialized 37/60 | Total 61/100

**Assertions:**

- PASS — Script runs unmodified on a reference lacking Monocytes (rc 0)
- FAIL — At least 80% of held-out-type cells are gated to Unknown (2.7% (17 of 630))
- FAIL — A distance-based gate calibrated on the reference flags a majority of held-out cells (0 of 630 above the 99th-percentile 15-NN threshold)
- PASS — In-distribution query cells are not over-flagged (1.2% Unknown among other cells)
- PASS — Skill documentation tells the user to validate OOD detection on spiked-in unseen types (failure-modes.md 'Good integration metrics, wrong labels' fix names it, but no shipped script does)

## Key strengths

- Clear projection-not-annotation framing with a method taxonomy, decision tree and failure-modes reference that match how the tools actually behave
- Real-data template runs unmodified on CPU in about 90 s and its gate separates wrong from right calls (0.003 vs 0.14-0.19 uncertainty)
- Saved-model surgery route (directory arguments) and the documented weight_decay=0.0 pattern execute correctly on scvi-tools 1.5.1
- Version, threshold and citation statements (HLCA 0.2, scIB 0.6/0.4, log1p CP10k) are accurate

## Recommendations

- **[P1] AM-001 OOD gate misses a held-out type; claim overstated** (inputs [3, 4, 5]): With Monocytes removed from the reference, the shipped weighted-kNN gate flagged 2.7% of the 630 query monocytes and 95.4% were confidently labelled DC; a reference-calibrated distance gate flagged 0%. With B cells removed it gated 87.4%. SKILL.md calls the gate the step that makes labels trustworthy, and the demo's synthetic far cluster hides this. Fix: Scope the claim (the gate is a heuristic that catches between-type cells, not guaranteed novelty detection), add a short held-out-type spike-in check script and recommend running it per reference, and relabel the demo's 'softmax' as kNN probability. Changes runnable bytes (new or edited script) plus text.
- **[P2] AM-002 Prose-only and heavy methods not labelled not executed** (inputs []): Symphony, Azimuth, scPoli, popV, treeArches/scHPL and scGPT/Geneformer appear in the taxonomy and decision tree with performance and OOD claims but no code, install line or statement that they were not run. Fix: Add one line under Version Compatibility naming these methods as described from the literature and not executed or bundled. Text only.
- **[P2] AM-003 predict(soft=True) type not stated (DataFrame)** (inputs [2]): In scvi-tools 1.5.1 predict(soft=True) returns a pandas DataFrame (2638 x 8, columns are labels). SKILL.md only says 'per-class probabilities'; proba.max() then returns per-class maxima and proba[:, 0] raises. Fix: State that it is a DataFrame indexed by cell with label columns and show proba.max(axis=1) / idxmax(axis=1). Text only.
- **[P2] AM-004 Snippets and script input contract incomplete** (inputs [1, 2]): SKILL.md snippets use ref_vae and adata_ref without defining them, and scarches_annotation.py requires layers['counts'], obs['batch'] and obs['cell_type'] (and shared genes) without saying so. Fix: Define ref_vae/adata_ref in the snippets (or point to the script) and document the required h5ad fields in the script docstring and SKILL.md. Text only (docstring/comment edits, no behavior change).
- **[P2] AM-005 Script unseeded and persists nothing** (inputs [1]): Two unmodified runs on identical inputs gave 1.82% vs 1.29% Unknown and accuracy 0.9647 vs 0.9666; the script writes no predictions, latent or uncertainty to disk. Fix: Set scvi.settings.seed and write the annotated query h5ad (predicted_label, transfer_uncertainty, latent). Changes runnable bytes.

## Ordered finding ledger

Audited identity: `d4048dcc887b51c820dba4669bf05620829970e083f7512d24a2539953ad48a6`

| Order | ID | Priority | State | Evidence inputs | Required disposition |
|---:|---|---|---|---|---|
| 1 | AM-001 | P1 | open | [3, 4, 5] | OOD gate misses a held-out type; claim overstated. Scope the claim (the gate is a heuristic that catches between-type cells, not guaranteed novelty detection), add a short held-out-type spike-in check script and recommend running it per reference, and relabel the demo's 'softmax' as kNN probability. Changes runnable bytes (new or edited script) plus text. |
| 2 | AM-002 | P2 | open | [] | Prose-only and heavy methods not labelled not executed. Add one line under Version Compatibility naming these methods as described from the literature and not executed or bundled. Text only. |
| 3 | AM-003 | P2 | open | [2] | predict(soft=True) type not stated (DataFrame). State that it is a DataFrame indexed by cell with label columns and show proba.max(axis=1) / idxmax(axis=1). Text only. |
| 4 | AM-004 | P2 | open | [1, 2] | Snippets and script input contract incomplete. Define ref_vae/adata_ref in the snippets (or point to the script) and document the required h5ad fields in the script docstring and SKILL.md. Text only (docstring/comment edits, no behavior change). |
| 5 | AM-005 | P2 | open | [1] | Script unseeded and persists nothing. Set scvi.settings.seed and write the annotated query h5ad (predicted_label, transfer_uncertainty, latent). Changes runnable bytes. |

No audit-local repair was made; no Skill bytes changed.

## Score-floor note

The Production Ready/Limited Release per-layer floors in `scoring_rubric.md` section 5 are not all met (assertion pass rate 14/23, below 80 percent); the grade shown follows the score table that `audits:check` enforces. This is a diagnostic initial audit; no readiness is claimed.
