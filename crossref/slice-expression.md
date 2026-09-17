# Cross-reference — expression, differential and clustering (2026-09-17)

Slice: 8 published Skills, all from `tumor-immune-microenvironment-analyst` — `batch-effect-correction`, `gene-protein-expression-matrix-normalization`, `deg-screening-analysis`, `consensus-clustering-analysis`, `hierarchical-clustering-plot`, `sample-group-sankey-plot`, `cibersort-immune-infiltration-analysis`, `estimate-immune-score-analysis`.

## Summary table

| Published Skill | bioSkills counterpart(s) | Verdict | Which to bundle | Reason |
|---|---|---|---|---|
| `batch-effect-correction` | `bio-differential-expression-batch-correction` | partial | both, different roles | Published ships a runnable ComBat + `normalizeBetweenArrays` CLI with QC plots and tests. bioSkill has no shipped code but covers 6 methods (design-matrix inclusion, ComBat/ComBat-seq, SVA, RUVg/s/r) and the Nygaard 2016 "never test on a batch-corrected matrix" cardinal sin that the published skill does not warn about. |
| `gene-protein-expression-matrix-normalization` | `bio-expression-matrix-normalization` | partial | both, different pipeline stage | Published rescales an *already-quantified* numeric matrix (RNA or protein) with log2/z-score/min-max for visualization — and explicitly excludes count-model normalization. bioSkill owns exactly that excluded territory (TMM/RLE/VST/rlog/scran from raw counts). Neither substitutes for the other; a Specialist doing bulk RNA-seq end-to-end needs both stages. |
| `deg-screening-analysis` | `bio-differential-expression-deseq2-basics`, `bio-differential-expression-edger-basics`, `bio-data-visualization-volcano-and-ma-plots`, `bio-data-visualization-heatmaps-clustering` | partial | published for a quick limma pipeline; bioSkills for count-model DE and rigorous plotting | Published explicitly excludes DESeq2/edgeR ("NOT for count-model workflows"), so it doesn't compete with those two bioSkills on method — it fills a real gap (bioSkills has no dedicated limma-basics skill). But its volcano/heatmap outputs are unshrunken-LFC, unlabeled, default-linkage — thinner than the dedicated visualization bioSkills. |
| `consensus-clustering-analysis` | none found | distinct / no counterpart | published (only option) | No bioSkill implements ConsensusClusterPlus-style resampling or PAC-based K selection for bulk sample subtyping. Nearest candidates (`bio-single-cell-clustering`, `bio-temporal-genomics-temporal-clustering`) solve different problems (cell clustering, gene-trajectory shape clustering). |
| `hierarchical-clustering-plot` | `bio-data-visualization-heatmaps-clustering` | partial | published for a standalone dendrogram; bioSkill for rigor / annotated heatmaps | Published is a simple, runnable `dist()`+`hclust()` CLI producing a dendrogram PDF and distance matrix — no heatmap coloring. bioSkill covers the same clustering core but as part of a full heatmap (color mapping, optimal leaf ordering, annotation tracks) and explicitly documents the `ward.D` vs `ward.D2` trap that published's own `-m ward.D` argument option would silently walk an agent into. |
| `sample-group-sankey-plot` | `bio-data-visualization-flow-and-transition-plots` | duplicate | published | Same job, same tool: both build a `ggalluvial`-based alluvial/Sankey plot from a categorical sample-annotation table (`to_lodes_form` + `geom_alluvium`/`geom_stratum`). Published has a runnable CLI, tests, and readability advisories; bioSkill has no shipped code for this case (it's a reference doc covering Sankey, alluvial, and CONSORT diagrams generally). |
| `cibersort-immune-infiltration-analysis` | `bio-methylation-cell-type-deconvolution`, `bio-spatial-transcriptomics-spatial-deconvolution` | distinct | published (only option for bulk RNA-seq) | Both bioSkill candidates solve a deconvolution problem but for the wrong assay — DNA methylation arrays and spatial-transcriptomics spots, not bulk RNA-seq mixtures. Neither ships LM22 or a CIBERSORT-style nu-SVR. This is a real gap in bioSkills: bulk-RNA-seq immune deconvolution (CIBERSORT/EPIC/quanTIseq) has no dedicated skill. |
| `estimate-immune-score-analysis` | `bio-pathway-gsea` | partial | published (only option for an actual ESTIMATE score) | Both ultimately run ssGSEA-family scoring, and `bio-pathway-gsea` names ssGSEA/GSVA as the "per-sample pathway activity" method — the same computational core ESTIMATE uses. But `bio-pathway-gsea` is scoped to GO/KEGG/Reactome/MSigDB gene sets and never mentions the ESTIMATE package, its fixed 141-gene stromal/immune signatures, or the tumor-purity formula. It cannot produce a StromalScore/ImmuneScore/TumorPurity table as-is. |

No audit report exists for any of the bioSkills counterparts above except `bio-differential-expression-deseq2-basics` (final.score 92, grade "Production Ready") and `bio-pathway-gsea` (final.score 97, grade "Production Ready"). The rest of the bioSkills cited here (`bio-differential-expression-batch-correction`, `bio-expression-matrix-normalization`, `bio-differential-expression-edger-basics`, `bio-data-visualization-volcano-and-ma-plots`, `bio-data-visualization-heatmaps-clustering`, `bio-data-visualization-flow-and-transition-plots`, `bio-methylation-cell-type-deconvolution`, `bio-spatial-transcriptomics-spatial-deconvolution`) have no `F:\OpenScience\audits\<skill-id>\eval_report_*.json` — quality is not assessed here, only content compared. Published (non-bio) Skills have no audit reports of any kind.

---

## partial: `batch-effect-correction` vs `bio-differential-expression-batch-correction`

**Published (`batch-effect-correction/SKILL.md`):**
> "Run `sva::ComBat()` to remove batch-driven variation" ... "Apply `limma::normalizeBetweenArrays()` after ComBat" ... Output: `corrected_expression_matrix.csv`.

The Agent Response Contract tells the caller to report "QC assessment: describe whether before/after PCA plots show reduced batch clustering" and hand back `corrected_expression_matrix.csv` as a first-class artifact. Nothing in the SKILL.md warns against feeding that corrected matrix into a subsequent DE test.

**bioSkill (`bio-differential-expression-batch-correction/SKILL.md`):**
> "**'Remove the batch effect before DE'** -> Almost always WRONG. Include batch as a covariate in the design formula (`~ batch + condition`)... Subtraction is for visualization only." ... "Nygaard, Rødland, Hovig 2016 ... never run ComBat (or ComBat-seq, or `removeBatchEffect`, or SVA-subtract-then-test) and then run DE on the corrected matrix."

**Verdict rationale:** Same core method (ComBat, `sva` package) and same intermediate artifact (a batch-corrected matrix), but different purpose framing and different depth. The published skill is an execution tool that produces exactly the artifact the bioSkill warns is dangerous to reuse for testing. Bundle the published skill for actually running the correction (it's the only one of the two with a CLI, test data, and PDFs); bundle the bioSkill's knowledge (or add its warning) so an agent doesn't wire `corrected_expression_matrix.csv` into a downstream DEG test.

## partial: `gene-protein-expression-matrix-normalization` vs `bio-expression-matrix-normalization`

**Published:**
> "NOT for count-model normalization such as TPM/DESeq2 size factors, batch correction, or single-cell preprocessing." Methods: `log2`, `zscore`, `minmax` on "gene or protein expression matrices."

**bioSkill:**
> "Normalizes and transforms RNA-seq count matrices for DE, visualization, clustering, and ML. Covers between-sample (TMM, TMMwsp, RLE/median-of-ratios, upper quartile), within-sample (TPM, FPKM/RPKM), variance-stabilizing (VST, rlog, log-CPM)..."

**Verdict rationale:** The published skill's scope statement is almost a mirror-negative of the bioSkill's scope statement — each explicitly excludes what the other does. They are sequential pipeline stages, not competitors: bioSkill turns raw counts into a normalized matrix; published skill rescales any already-normalized (or protein-quantified) matrix for plotting/clustering. Bundle both for a complete bulk-RNA pipeline; there's no routing ambiguity because their "NOT for" clauses are self-policing.

## partial: `deg-screening-analysis` vs DESeq2/edgeR/visualization bioSkills

**Published:**
> "...limma-based two-group comparison... NOT for single-cell RNA-seq, multi-group contrasts, count-model workflows such as DESeq2/edgeR, or non-expression omics data." Current implementation supports `--diff_method limma` only; ships `plot/volcano_plot.pdf` and `plot/heatmap.pdf`.

**bioSkill (`bio-differential-expression-deseq2-basics`, score 92/Production Ready):**
> "Fit a negative-binomial GLM per gene with shared dispersion shrinkage, test the coefficient of interest (Wald) or the joint effect..." — raw-count input only.

**bioSkill (`bio-data-visualization-volcano-and-ma-plots`):**
> "Raw log2 fold change from DESeq2 / edgeR is the maximum-likelihood estimate and inflates wildly at low counts... Plot the shrunken LFC." — the published skill's volcano plots the unshrunk `logFC` column directly (`Diffanalysis.csv` columns are `name, logFC, P.value, P.adj`), with no shrinkage step (there is none in a limma two-group moderated-t workflow, so this critique is method-appropriate but the labeling/repel/threshold rigor the bioSkill teaches is absent).

**bioSkill (`bio-data-visualization-heatmaps-clustering`):**
> "Always specify `ward.D2` explicitly... `hclust(dist(x), method='ward.D')` is NOT Ward's criterion." Published's `plot/heatmap.pdf` step doesn't document its clustering method at all in SKILL.md.

**Verdict rationale:** No method collision with DESeq2/edgeR (published explicitly excludes count models — this is good self-policing, not a gap). The real overlap is superficial: "DEG table + volcano + heatmap" is also producible via `de-results` + `volcano-and-ma-plots` + `heatmaps-clustering`, but those are for count-model DE, not limma-on-a-matrix. Bundle the published skill for the specific case its scope names (pre-normalized bulk matrix, two-group, limma); it is the only integrated, runnable option for that exact input shape. Bundle the DESeq2/edgeR bioSkills instead when raw counts are available — a materially better statistical model for RNA-seq.

## partial: `hierarchical-clustering-plot` vs `bio-data-visualization-heatmaps-clustering`

**Published:**
> `--linkage_method` accepts `complete, single, average, mcquitty, median, centroid, ward.D, ward.D2`, default `complete`. "The clustering tree is built with base R `hclust()`."

**bioSkill:**
> "R `stats::hclust` exposes two methods both labeled 'Ward': `ward.D` and `ward.D2`. They produce *different* dendrograms on the same data. Only `ward.D2` ... implements Ward's actual minimum-variance criterion (Murtagh & Legendre 2014)... Always specify `ward.D2` explicitly unless reproducing a paper that used the unlabeled `ward`."

**Verdict rationale:** Identical computational core (`dist()` + `hclust()` on a sample-by-feature matrix) and identical failure surface (the `ward.D`/`ward.D2` naming trap), but published is a narrower, runnable, dendrogram-only CLI with CSV/PDF outputs and a test suite, while the bioSkill is a much deeper reference covering the same clustering step as one part of a full annotated heatmap (color mapping, optimal leaf ordering, `draw()` gotcha). Bundle the published skill when only a sample dendrogram is needed (it is simpler and runnable); a Specialist author choosing `ward.D` as a "safe default" for the published skill's CLI should first read the bioSkill's trap warning.

## duplicate: `sample-group-sankey-plot` vs `bio-data-visualization-flow-and-transition-plots`

**Published:**
> "Builds a reproducible Sankey/alluvial visualization from a tabular sample annotation file..." Uses `ggalluvial::to_lodes_form()`, `geom_flow()`/`geom_stratum()` (i.e., `geom_alluvium`-family rendering) with `--columns`, readability advisories at >5 stages or >8 values/stage.

**bioSkill:**
> "ggalluvial -- Modern R Default for Alluvial... Reshape to 'lodes' (long) format... use `geom_alluvium` for ribbons and `geom_stratum` for column boxes." Quantitative threshold table: "Max categories per column for legibility: 5-7," "Max axes for alluvial: 4-5."

**Verdict rationale:** Same tool (`ggalluvial`), same data shape (sample × categorical-stage table), same transform (`to_lodes_form`), and even matching readability thresholds (bioSkill's "5-7 categories / 4-5 axes" vs published's "fewer than 8 unique values... fewer than 5 stages"). A user or agent would pick one, not both. Bundle the published skill: it has a runnable CLI, bundled test data, and enforces the same thresholds the bioSkill only documents. Interesting note: despite being named "sankey," the published skill's implementation is technically alluvial (entity-traceable, multi-axis) — which the bioSkill's own "Sankey used when alluvial is appropriate" failure mode says is the *correct* choice for this use case, not the mistake.

## partial: `estimate-immune-score-analysis` vs `bio-pathway-gsea`

**Published:**
> "compute ESTIMATE-derived immune and stromal scores from a bulk expression matrix... `estimate::filterCommonGenes()`... `estimate::estimateScore()`." Outputs `StromalScore`, `ImmuneScore`, `ESTIMATEScore`, `TumorPurity`.

**bioSkill (score 97/Production Ready):**
> "...scores per-sample pathway activity with ssGSEA and GSVA... ssGSEA | Barbie 2009 *Nature* 462:108 | per-sample rank-based enrichment score." Scoped to "GO, KEGG, Reactome, or MSigDB gene sets" via `clusterProfiler`/`GSVA`; never mentions the `estimate` R package, its fixed gene signatures, or a purity formula.

**Verdict rationale:** ESTIMATE (Yoshihara 2013) computes StromalScore/ImmuneScore by running ssGSEA over two fixed 141-gene signatures and derives TumorPurity from a published formula — mechanically a specific application of the same ssGSEA machinery `bio-pathway-gsea` documents generically. But `bio-pathway-gsea` has no path to reproduce ESTIMATE's specific signatures or purity conversion; it would need to be extended, not just invoked. Bundle the published skill as the only route to an actual ESTIMATE score table; the shared-method overlap with `bio-pathway-gsea` is evidence of conceptual proximity, not a substitutable duplicate.

---

## No bioSkills counterpart found

- **`consensus-clustering-analysis`** — searched by folder (`clustering`), by method name (`consensus`, `PAC`, `ConsensusClusterPlus`, `NMF`), and by task (bulk sample subtype discovery). No bioSkill implements consensus-resampling cluster-stability analysis or PAC-based K selection for bulk expression matrices. The two nearest candidates by keyword (`bio-single-cell-clustering`, `bio-temporal-genomics-temporal-clustering`) solve different problems — single-cell graph clustering and time-course gene-shape clustering, respectively — and were read in full to confirm neither covers bulk sample-subtype consensus clustering.
