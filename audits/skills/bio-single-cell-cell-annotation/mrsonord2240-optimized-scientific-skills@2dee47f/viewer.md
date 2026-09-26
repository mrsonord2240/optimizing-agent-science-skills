> **Audit record for `bio-single-cell-cell-annotation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/optimized-scientific-skills@2dee47f](https://github.com/mrsonord2240/optimized-scientific-skills/tree/2dee47f80dac6f3ba5c78b53ea9ec132a87cf5db/skills/bio-single-cell-cell-annotation) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-25 by Codex independent auditor agent, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-cell-annotation

Generated: 2026-09-25

Source: mrsonord2240/optimized-scientific-skills@2dee47f80dac6f3ba5c78b53ea9ec132a87cf5db:skills/bio-single-cell-cell-annotation

Auditor independence: true. The source checkout was treated as immutable and remained unmodified.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 39 | 58 | 97 | 5/5 | ✅ Completed |
| 2 | Variant A | 32 | 47 | 79 | 4/5 | ❌ Partial |
| 3 | Edge | 37 | 55 | 92 | 5/5 | ✅ Completed |
| 4 | Variant B | 32 | 48 | 80 | 4/5 | ❌ Partial |
| 5 | Stress | 38 | 57 | 95 | 5/5 | ✅ Completed |
| 6 | Scope Boundary | 39 | 58 | 97 | 5/5 | ✅ Completed |
| 7 | Adversarial | 38 | 57 | 95 | 5/5 | ✅ Completed |

Execution average: 90.7 / 100

Assertion pass rate: 33 / 35 (94.3%)

Cleanly executed inputs: 5 / 7. Inputs 2 and 4 produced validated scientific outputs but are not counted as executed successes because their R processes returned nonzero exit 2816.

Static score: 91 / 100

Final score: 91 / 100 — ⭐ Production Ready

Veto: none. Deployable: true.

Open recommendations: P0 0, P1 1, P2 2.

## Test inputs

1. Canonical: Run the exact shipped CellTypist CLI on the clustered synthetic PBMC fixture using a local Immune_All_Low model. Restore the counts layer to CP10K/log1p, use the seeded Leiden over-clustering, retain confidence, and write caller-selected H5AD, figure, and counts destinations.
2. Variant A: Annotate four synthetic PBMC lanes with SingleR and HumanPrimaryCellAtlasData. Confirm logcounts, compare classic and wilcox for the bulk reference, preserve pruned labels and delta evidence, and score against known lineages.
3. Edge: Repeat CellTypist annotation with correct gene symbols and with Ensembl IDs occupying var_names. Quantify matched model features and stop rather than trust labels when there is no overlap.
4. Variant B: Map real public 10x PBMC 1k v3 data onto Azimuth pbmcref, retain hierarchical labels and confidence, and validate predictions with normalized canonical-marker expression.
5. Stress: A cluster appears poorly mapped; determine whether it is novel. Screen every cluster for doublet, low-quality, batch, and confidence evidence before considering novelty, using planted artifact truth for validation.
6. Scope Boundary: Run the shipped CellTypist CLI in an air-gapped process with an isolated empty default cache, an explicit local model, and custom outputs. Then request an uncached model and prove it fails without acquisition.
7. Adversarial: Two plausible CellTypist immune models appear to disagree. Compare them on the same seeded real PBMC query, reconcile label granularity, retain confidence, and flag ambiguity without declaring either model ground truth.

## Detailed outputs

### Input 1 — Exact shipped CellTypist CLI

Status: COMPLETED, exit 0.

What ran:

- run/input1_prepare.py prepared 6,049 clean synthetic PBMC cells, 12,521 genes, 15 Leiden clusters, PCA/neighbors/UMAP seed 17, and a raw counts layer.
- The exact immutable source examples/celltypist_annotation.py ran with all five CLI path arguments and an explicit local Immune_All_Low.pkl.
- run/input1_validate.py parsed every output and checked normalization, clustering, confidence, counts, and accuracy.
- run/verify_seed_repeat.py repeated prediction twice on 1,000 cells.

Key output:

    prepared cells=6049 genes=12521 clusters=15 seed=17
    cp10k_min=10000.00 cp10k_max=10000.00
    seeded_clusters_preserved=15
    per_cell_lineage_accuracy=0.891
    majority_lineage_accuracy=1.000
    low_confidence=2186/6049
    configured_outputs=PASS
    majority_labels_identical=True
    confidence_identical=True

Scores: Basic 39/40; Specialized 58/60; Total 97/100.

Assertions:

- PASS — Counts restoration produced CP10K/log1p input.
- PASS — Seeded Leiden labels were preserved and consumed.
- PASS — Majority voting improved coarse lineage accuracy.
- PASS — Per-cell confidence and rejection membership were retained.
- PASS — Every configured output existed and parsed.

Evidence: run/input1.log, run/verify_seed_repeat.log, data/input1_annotated.h5ad, data/input1_annotation.png, data/input1_counts.csv.

### Input 2 — SingleR HPCA regression

Status: PARTIAL. The scientific work completed twice, but neither Windows R process exited cleanly.

What ran:

- run/input2.R used the same four-lane synthetic PBMC fixture as the prior audit, Seurat normalization, SingleR, and cached celldex HPCA.
- run/input2_clean_prepare.py and run/input2_clean.R independently repeated the analysis from a sparse Matrix Market input through SingleCellExperiment and logNormCounts, without Seurat.

Key output:

    original route exit=2816
    de.method=classic accuracy=0.906 pruned=15/3022 kept_accuracy=0.908
    de.method=wilcox accuracy=0.530 pruned=41/3022 kept_accuracy=0.537
    clean route exit=2816
    clean_route_accuracy=0.908 pruned=14/3023

WSL disposition:

- The science WSL image had R 4.4.1 but did not have SingleR, celldex, Seurat, or SingleCellExperiment.
- A unique isolated environment named cellann-reaudit-2dee47f was attempted and stopped when it exceeded the 1 GB install limit.
- Exact partial path: /home/sci/micromamba/envs/cellann-reaudit-2dee47f
- Recorded size: 1,965,733,894 bytes.
- WSL SingleR itself was not executed.
- The partial environment export is run/input2_wsl_partial_environment.yaml.
- The interruption and state log is run/input2_wsl_install_interrupted.log.
- Removal is safe after the audit report and export are validated: the name was unique to this audit, no create process remains, and the shared bio environment was only listed, not modified. This audit does not remove it.

Scores: Basic 32/40; Specialized 47/60; Total 79/100.

Assertions:

- PASS — SingleR received logcounts.
- PASS — classic was empirically preferable to wilcox for the bulk reference.
- PASS — Pruning and delta evidence were retained without being treated as a universal correctness check.
- PASS — A second implementation path reproduced the scientific result.
- FAIL — No complete SingleR route produced a clean process exit.

Evidence: run/input2.log, run/input2_clean.log, run/input2_wsl_probe.log, run/input2_wsl_install_interrupted.log, run/input2_wsl_partial_environment.yaml.

### Input 3 — Gene identifier boundary

Status: COMPLETED, exit 0.

Key output:

    symbols: matched=3931/6639 labels=32
    ensembl: matched=0/6639 error=No features overlap with the model
    gene identifier regression PASS

Scores: Basic 37/40; Specialized 55/60; Total 92/100.

Assertions:

- PASS — The valid symbol query annotated.
- PASS — The zero-overlap query hard-failed.
- PASS — Matched-feature counts were reported.
- PASS — The model came from an explicit local path.
- PASS — The invalid query produced no biological label.

Evidence: run/input3.py and run/input3.log.

### Input 4 — Azimuth real PBMC mapping

Status: PARTIAL. The analysis and artifact assertions completed, but the Windows R process exited 2816.

Key output:

    real_cells=1176 low_conf=257 (21.9%) mapping_score_median=0.982
    l1 labels: Mono 360, CD4 T 313, B 193, CD8 T 114, other T 88, NK 55, DC 27, other 26
    normalized_marker_validation=PASS
    process_exit=2816

Scores: Basic 32/40; Specialized 48/60; Total 80/100.

Assertions:

- PASS — Documented Azimuth metadata columns existed.
- PASS — The query was real PBMC data within the reference domain.
- PASS — Confidence was reported as a dataset distribution.
- PASS — NormalizeData preceded DotPlot marker validation.
- FAIL — The R process did not exit cleanly.

Evidence: run/input4.R, run/input4.log, data/input4_dotplot.png.

### Input 5 — QC-first novelty triage

Status: COMPLETED, exit 0.

Key output:

    all_clusters_screened=20
    artifact_clusters=4
    artifact_qc_recall=1.000
    novel_label_claimed=False

The all-cluster table retained confidently mislabeled artifacts: a 100% doublet cluster had median confidence 0.820, and 100% low-quality clusters had median confidence 0.593 and 0.973. None was excluded before QC.

Scores: Basic 38/40; Specialized 57/60; Total 95/100.

Assertions:

- PASS — Every cluster entered QC.
- PASS — All planted artifact clusters were QC-flagged.
- PASS — High annotation confidence did not suppress artifact review.
- PASS — Mitochondrial, gene-count, doublet, batch, and confidence evidence remained visible.
- PASS — No novel type was claimed.

Evidence: run/input5.py, run/input5.log, data/input5_cluster_qc.csv.

### Input 6 — Offline model resolution and custom outputs

Status: COMPLETED, exit 0.

The CellTypist cache override was set before importing CellTypist. requests, urllib, download_models, and get_all_models were patched to fail on invocation.

Key output:

    isolated_models_path=.../data/input6_empty_cache/data/models
    network_acquisition_calls=0
    missing_model_error=CellTypist model is not cached
    custom_output_destinations=PASS

Scores: Basic 39/40; Specialized 58/60; Total 97/100.

Assertions:

- PASS — An explicit local model worked with an empty default cache.
- PASS — No network or model-index helper was called.
- PASS — The uncached model failed with an actionable local error.
- PASS — Custom H5AD, PNG, and CSV paths were honored.
- PASS — No model was populated into the isolated cache.

Evidence: run/input6.py, run/input6.log, data/input6_custom.h5ad, data/input6_custom.png, data/input6_custom.csv.

### Input 7 — Competing reference granularities

Status: COMPLETED, exit 0.

Key output:

    real_pbmc_cells=800 seeded_clusters=14
    exact_label_agreement=0.019
    coarse_lineage_agreement=1.000
    cells_flagged_for_review=89
    low_model_mean_conf=0.868
    high_model_mean_conf=0.966
    either_model_treated_as_ground_truth=False

Scores: Basic 38/40; Specialized 57/60; Total 95/100.

Assertions:

- PASS — Both models used the same seeded real query.
- PASS — Label granularity was reconciled before interpreting disagreement.
- PASS — Low-confidence or coarse-disagreement cells were flagged.
- PASS — Confidence remained model-specific.
- PASS — Neither model was treated as ground truth.

Evidence: run/input7.py, run/input7.log, data/input7_model_comparison.csv.

## Required-input validation

The exact shipped CLI rejected all three malformed inputs before annotation:

    missing_counts=PASS
    missing_leiden=PASS
    missing_umap=PASS

Evidence: run/validate_required_inputs.py and run/validate_required_inputs.log.

## Veto review

Structural veto:

- Stability: PASS. Five workflows exited cleanly. The two R partials were deterministic post-output host teardown failures, not random scientific crashes; both remain explicitly non-successful in the execution count.
- Contract: PASS. Frontmatter, CLI arguments, metadata columns, and output file types were consistent.
- Determinism: PASS. Upstream seed 17 was recorded and repeated labels/confidence were identical.
- Security: PASS. No raw-code execution, credential handling, destructive command, or hidden network acquisition was observed.

Research veto:

- Scientific integrity: PASS. All numeric claims trace to saved logs.
- Practice boundaries: PASS. Research matrices were annotated; no individual diagnosis or treatment guidance was produced.
- Methodological ground: PASS. Method-specific normalization and closed-world limits were respected.
- Code usability: PASS. No code syntax error, infinite loop, or unexplained missing core dependency occurred. The two R routes are nevertheless marked partial because their process exits were nonzero.

## Static score

| Category | Score |
|---|---:|
| Functional suitability | 11 / 12 |
| Reliability | 10 / 12 |
| Performance and context | 7 / 8 |
| Agent usability | 14 / 16 |
| Human usability | 8 / 8 |
| Security | 11 / 12 |
| Maintainability | 11 / 12 |
| Agent-specific | 19 / 20 |
| Total | 91 / 100 |

## Open recommendations

### P1 — Establish a clean-exit Linux smoke for R routes

Observed in inputs 2 and 4. Provide a tested compact lockfile or container for SingleR, celldex, and Azimuth, then require process exit 0 and artifact checks. Windows outputs remain partial until an independent clean route passes.

### P2 — Align inline and CLI CellTypist model acquisition

The canonical SKILL.md code downloads a model and passes a bare name, while the shipped CLI accepts only an existing explicit or cached model. Move download to a separate optional provisioning step and use the same local-resolution contract in both places.

### P2 — Add runnable scANVI and scmap examples

The description promises those methods but provides no end-to-end examples. Add minimal workflows with explicit inputs, uncertainty outputs, and smoke fixtures.

## Artifact map

- Full JSON report: eval_report_bio-single-cell-cell-annotation_result.json
- Full execution logs: run/*.log
- Every audit or support script executed: run/*.py, run/*.R, and run/*.sh
- Generated data and plots: data/
- WSL partial environment export: run/input2_wsl_partial_environment.yaml
