# Cross-reference — pathway and enrichment (2026-09-17)

Slice: 4 published Skills from `tumor-immune-microenvironment-analyst` — `gokegg-analysis`, `gsva-analysis-and-visualization`, `ssgsea-immune-infiltration-analysis`, `immune-pathway-analysis` — against bioSkills `pathway-analysis/*` and adjacent folders (`metabolomics/pathway-mapping`, `single-cell`, `immunoinformatics`, `systems-biology`). No dedicated bioSkill exists for immune-cell deconvolution or per-sample immune scoring (checked `immunoinformatics/` — epitope/MHC/neoantigen only; `single-cell/` — no bulk ssGSEA/GSVA immune tool; `systems-biology/` — metabolic modeling only). The nearest bioSkills counterpart for all three GSVA/ssGSEA-based published Skills is therefore `bio-pathway-gsea`'s "Per-Sample Scores" section, not a purpose-built immune-infiltration Skill.

## Summary table

| Published Skill | bioSkills counterpart(s) | Statistic each runs | Verdict | Bundle recommendation |
|---|---|---|---|---|
| `gokegg-analysis` | `bio-pathway-go-enrichment` + `bio-pathway-kegg-pathways` | All three: hypergeometric ORA (`phyper` one-sided, clusterProfiler `enrichGO`/`enrichKEGG` engine) on a gene list | **duplicate** | Bundle the bioSkills pair — audited Production Ready (90, 97), and they get the background-universe requirement right, which `gokegg-analysis` gets wrong |
| `gsva-analysis-and-visualization` | `bio-pathway-gsea` (Per-Sample Scores section) | Published: GSVA (kernel, `gsva`) or ssGSEA (rank, `ssgsea`) per-sample score, then `limma` moderated-t diff test on the score matrix. bioSkill: same two per-sample methods, described but not run (GSVA "not installed in the reference environment") | **partial** | Bundle the published Skill for the working pipeline (tested, tables + `.rda` + heatmap); cite `bio-pathway-gsea` for the correctness caveats (contrast-test alternative via CAMERA/ROAST) it alone documents |
| `immune-pathway-analysis` | `bio-pathway-gsea` (same section) **and** its own sibling `gsva-analysis-and-visualization` | GSVA/ssGSEA + `limma` diff, scored against a caller-supplied local **immune Reactome** gene-set table instead of MSigDB | **partial** vs `bio-pathway-gsea`; near-**duplicate** vs its sibling | Bundle only if a Specialist specifically needs a pre-packaged immune-Reactome table; otherwise `gsva-analysis-and-visualization` already covers the identical GSVA/limma/heatmap mechanics with an arbitrary MSigDB collection, making a second copy redundant |
| `ssgsea-immune-infiltration-analysis` | `bio-pathway-gsea` (same section) | ssGSEA (default) or GSVA per-sample score against a local immune **cell-type** gene-set table, plus case/control comparison and an inter-cell-type Spearman correlation matrix — no `limma` step | **partial** | Bundle for its immune-cell correlation/composition tooling (`immune_cell_correlation_matrix.csv`, composition/boxplot/scatter plots) that neither `bio-pathway-gsea` nor the other two published Skills provide |

## Evidence per pair

### `gokegg-analysis` vs `bio-pathway-go-enrichment` + `bio-pathway-kegg-pathways` — duplicate

`gokegg-analysis` runs GO and KEGG enrichment on one gene list and renders a combined dot chart:

> "GO and KEGG enrichment on a gene list derived from bulk RNA-seq or microarray studies" ... `--pvalue_cutoff 0.05 --qvalue_cutoff 0.2 --pAdjustMethod BH` ... outputs `GO_df.csv`, `KEGG_df.csv` with `Description`/`p.adjust` columns.

Its parameter table has no `universe`/background argument anywhere. `bio-pathway-go-enrichment` states this is exactly the defect that invalidates ORA:

> "Omitting `universe=` defaults N to ALL annotated genes (~18k for human BP); if the assay only measured ~12k genes, terms for tissue-restricted and lowly-expressed genes go spuriously significant... Omitting `universe=` is a bug, not a default."

`bio-pathway-kegg-pathways` makes the matching KEGG-side claim:

> "Whole-database universe in ORA... omitting `universe`... inflated significance for pathways enriched in measured/expressed genes (the tissue-specificity artifact)."

Both sides run the identical statistical test — one-sided hypergeometric ORA via clusterProfiler `enrichGO`/`enrichKEGG` — on the same input shape (gene list → enrichment table → dot chart). A user picks one, not both. The bioSkills pair also documents `simplify()` redundancy reduction, `FoldEnrichment` vs `GeneRatio`, and the `ont='MF'` default trap — none of which appear in `gokegg-analysis`'s SKILL.md. Audit evidence: `bio-pathway-go-enrichment` scored **90, Production Ready**; `bio-pathway-gsea` (which documents the same clusterProfiler ecosystem conventions) scored **97, Production Ready**. `gokegg-analysis` has no audit report — its quality claim rests on inspection only, and inspection finds the missing-universe gap.

**Bundle:** the bioSkills pair. Correctness (universe handling) beats convenience (one combined script) for a Specialist that will be trusted with real background-selection decisions.

### `gsva-analysis-and-visualization` vs `bio-pathway-gsea` — partial

`gsva-analysis-and-visualization` is a full CLI pipeline: expression matrix + group file → MSigDB gene sets (`--category`/`--subcategory`) → `GSVA::gsva()` or ssGSEA scores → `limma` case-vs-control diff → heatmap, with bundled test data and a documented baseline run.

`bio-pathway-gsea` covers the identical two methods in five lines of example code:

> "GSVA >= 1.50 uses a PARAMETER-OBJECT API... `gsva_scores <- gsva(gsvaParam(expr_matrix, gene_sets))`... GSVA is not installed in the reference environment - verify the installed signature with `?gsva` before running."

That last clause matters: the bioSkill's own GSVA/ssGSEA code was never executed in its audit environment (`bio-pathway-gsea`'s audit meta lists `GSVA 2.0.7` as installed for the *re-audit*, but the skill text itself still carries the "not installed" caveat and offers no diff-test or heatmap step). It correctly flags that GSVA/ssGSEA produce "a per-sample feature matrix, not a contrast test" and recommends `limma::camera`/`roast`/`fry` for the actual differential question — a real methodological note the published Skill's naive "GSVA-then-limma-on-scores" approach doesn't engage with (running limma directly on GSVA scores treats them as if they had expression-level noise properties, which is a known point of debate the bioSkill implicitly warns about but the published Skill does not surface to the user).

**Bundle:** `gsva-analysis-and-visualization` for the tested, working pipeline (tables, `.rda`, heatmap, CLI, error codes). `bio-pathway-gsea` remains the reference for *when GSVA/ssGSEA is the wrong tool* (i.e., when a real contrast test with a p-value is wanted) — a Specialist bundling the published Skill should still carry `bio-pathway-gsea`'s decision tree as documentation, not as a competing executable.

### `immune-pathway-analysis` vs `bio-pathway-gsea` and vs its sibling `gsva-analysis-and-visualization` — partial / near-duplicate

`immune-pathway-analysis` is structurally the same pipeline as `gsva-analysis-and-visualization` — same modes (`analyze`/`visualize`/`full`), same `--method gsva|ssgsea`, same `--kcdf`/`--min_sz`/`--max_sz`/`--tau`/`--fdr_threshold` GSVA arguments, same `limma` diff step, same heatmap output shape (`table/*_diff.csv`, `data/*.rds`/`.rda`, `plot/*_heatmap.pdf`). The only functional difference is the gene-set source:

> "`--geneset_file` ... required for `analyze` or `full` — Local immune gene-set table in long format" (immune-pathway-analysis) vs `--category`/`--subcategory` MSigDB selection (gsva-analysis-and-visualization).

Against `bio-pathway-gsea`, the relationship is the same **partial** as above — same per-sample statistic, no executable diff/heatmap pipeline on the bioSkill side. Against its own sibling `gsva-analysis-and-visualization`, this is closer to duplicate: MSigDB already includes immune-relevant collections (Hallmark, C7 ImmuneSigDB, Reactome via C2), so `gsva-analysis-and-visualization --category C7` or `--subcategory REACTOME` with an immune filter reproduces most of what `immune-pathway-analysis` does with its bespoke local table, minus the convenience of a pre-curated immune Reactome file.

**Bundle:** ship `gsva-analysis-and-visualization` as the general-purpose GSVA/ssGSEA Skill; only add `immune-pathway-analysis` if the Specialist needs a pre-packaged, ready-to-run immune Reactome gene-set table shipped with the Skill (neither `bio-pathway-gsea` nor `gsva-analysis-and-visualization` ships one). Shipping both `immune-pathway-analysis` and `gsva-analysis-and-visualization` in the same Specialist without that distinction being made explicit creates ambiguous routing — an agent asked for "immune pathway GSVA" has two structurally identical tools to choose between.

### `ssgsea-immune-infiltration-analysis` vs `bio-pathway-gsea` — partial

This Skill scores immune-cell-type gene sets per sample (ssGSEA default, GSVA optional) and adds machinery none of the other three have: a case/control `ssgsea_group_compare.csv` summary (not `limma`-based — no mention of `limma` anywhere in its SKILL.md, unlike the other two), an inter-cell-type Spearman correlation matrix with p-values, and four plot types (composition, group boxplot, correlation heatmap, gene-vs-cell scatter).

> "Estimate relative immune infiltration from a bulk RNA-seq expression matrix... NOT for... Absolute immune cell proportion estimation or deconvolution."

That last disclaimer is methodologically important and correctly self-aware: this is a per-sample *enrichment score* over immune gene sets (ssGSEA), not a deconvolution algorithm (CIBERSORT/xCell/EPIC/MCP-counter, none of which exist in bioSkills either). `bio-pathway-gsea` covers the same underlying ssGSEA statistic but, as above, only as an unexercised code fragment with no group-comparison, correlation, or immune-composition tooling.

**Bundle:** `ssgsea-immune-infiltration-analysis` for the immune-cell-specific downstream analysis (correlation matrix, composition plots) that has no bioSkill equivalent at all.

## Do the four assigned Skills overlap each other?

Yes, substantially. `gsva-analysis-and-visualization`, `immune-pathway-analysis`, and `ssgsea-immune-infiltration-analysis` are three thin wrappers around the same `GSVA::gsva()` call (identical `--method`, `--kcdf`, `--min_sz`/`--max_sz`, `--tau`, `--mx_diff` arguments across all three), differing only in which gene-set table is plugged in (MSigDB collection / local immune-Reactome table / local immune-cell-type table) and in the downstream stats (`limma` diff for the first two, group-compare + correlation matrix for the third). An agent with all three loaded has no principled way to route "run GSVA on my immune samples" to one over another without inspecting gene-set-file conventions first. `gokegg-analysis` is the outlier — ORA, not the GSVA/ssGSEA family — and does not overlap the other three, only the two bioSkills ORA Skills named above.
