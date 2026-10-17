# Context-aware Skill candidates

Router-shaped recuts kept here while the shape is under test. They are not on the
optimized shelf and are not released. The shelf is where they are meant to end up
once the shape is proven (Sam, 2026-10-04).

A `ca-` prefix means "context aware": `SKILL.md` is a short route table, each
`routes/<task>.md` leads with its command, and `scripts/` holds one entry point per
route. The rules are in `.claude/skills/normalize-scientific-skill/SKILL.md`.

| Skill | Recut of | State |
|---|---|---|
| `ca-bio-workflows-crispr-screen-pipeline` | `bio-workflows-crispr-screen-pipeline` | Through the full relay; candidate-ready in `audits/skills/bio-workflows-crispr-screen-pipeline/candidate@e609525649bd-reaudit-delta-001` (final 89). Only the frontmatter `name` differs from the audited bytes. |
| `ca-bio-differential-expression-deseq2-basics` | `bio-differential-expression-deseq2-basics` | Not audited. Eval: pseudobulk task 5 of 5 with a cheap model (old layout 2 of 5); routing check 7 of 7 routes. Eleven older reference files only lightly cleaned. |
| `ca-bio-proteomics-differential-abundance` | `bio-proteomics-differential-abundance` | Not audited. Eval: 5 of 5 (old layout 2 of 5). DEqMS, proDA, msqrob2 and MSstats scripts and `shrink=ashr` never executed. No routing cases. |
| `ca-bio-machine-learning-model-validation` | `bio-machine-learning-model-validation` | Not audited. Eval: 3 of 5 (old layout 2 of 5); routing check 9 of 9 routes. Known defects: the decision-curve route needs a predictions file nothing produces; one route overstates that leave-one-out cannot give an AUC. |
| `ca-bio-duplicate-handling` | `bio-duplicate-handling` | Normalized only, not audited. Executed: all five scripts (samtools, pysam, umi_tools, fgbio on staged BAMs). Unexecuted: `umi_tools_dedup.sh scrna` success path, alternative-marker commands. |
| `ca-bio-variant-calling-filtering-best-practices` | `bio-variant-calling-filtering-best-practices` | Normalized only, not audited. All scripts unexecuted (`hard_filter.sh`, `genotype_filter.sh`, `somatic_filter.sh`, `cyvcf2_filter.py`, `filter_stats.sh`); VQSR commands shown only. |
| `ca-bio-single-cell-clustering` | `bio-single-cell-clustering` | Normalized only, not audited. All scripts unexecuted (`cluster_scanpy.py`, `cluster_seurat.R`, `validate_partition.py`, `subcluster.py`). |
| `ca-bio-single-cell-preprocessing` | `bio-single-cell-preprocessing` | Normalized only, not audited. All scripts unexecuted (`preprocess_scanpy.py`, `preprocess_seurat.R`, `soupx.R`). |
| `ca-bio-single-cell-data-io` | `bio-single-cell-data-io` | Normalized only, not audited. All scripts unexecuted (`load_10x.py`, `load_10x.R`, `h5ad_inventory.py`). |
| `ca-bio-proteomics-proteomics-qc` | `bio-proteomics-proteomics-qc` | Normalized only, not audited. Executed once earlier: `raw_qc.py`, `matrix_metrics.py`, `pca_batch.py`, `tmt_balance.py`, `diann_level1.py` (synthetic MaxQuant/TMT, real DIA-NN report). Unexecuted: `ptxqc_report.R`. |
| `ca-bio-analytical-validation` | `bio-analytical-validation` | Normalized only, not audited. Executed: `ge_and_poisson.py`, `lod95_probit.py`, `panel_integrated_lod.py` (contrived dilution series; ETAM-seq-derived series). |
| `ca-bio-machine-learning-omics-classifiers` | `bio-machine-learning-omics-classifiers` | Normalized only, not audited. Executed once: `logistic_regression.py --signature` on Golub (dense path crashed, fixed, not rerun). Unexecuted: `rf_xgboost_classifier.py`, `batch_checks.py`, `calibration_check.py`; SMOTE path untestable (no imblearn). |
| `ca-bio-variant-annotation` | `bio-variant-annotation` | Normalized only, not audited. All scripts unexecuted (`annotate_vep.sh`, `annotate_vcf.sh`, `parse_csq.py`). |
| `ca-bio-machine-learning-prediction-explanation` | `bio-machine-learning-prediction-explanation` | Normalized only, not audited. All scripts unexecuted (`shap_tree.py`, `lime_local.py`); lime in no WSL environment. |

`shelf-pointer-edits.patch` holds two one-line edits to shelf Skills
(`bio-workflows-scrnaseq-pipeline`, `bio-single-cell-markers-annotation`) that point
at the DESeq2 recut's pseudobulk route. Apply them only when that recut reaches the
shelf.
