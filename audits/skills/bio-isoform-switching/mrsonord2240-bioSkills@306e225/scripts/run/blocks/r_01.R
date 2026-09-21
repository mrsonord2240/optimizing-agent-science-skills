library(IsoformSwitchAnalyzeR)

salmonQuant <- importIsoformExpression(
    parentDir = 'salmon_quant/',              # one sub-directory per sample, each holding quant.sf
    calculateCountsFromAbundance = FALSE,     # raw NumReads as counts; see "Count route"
    addIsofomIdAsColumn = TRUE                # (sic) the package's own spelling
)

# Join the design to the quantification BY SAMPLE NAME. importIsoformExpression sorts samples
# alphabetically, so a hand-typed condition vector silently mislabels samples (audit: on SRR-style IDs
# it recovered 0/20 planted switches with no warning; joined by name, 20/20).
meta <- read.delim('sample_metadata.tsv')     # columns: sample_id (= quant sub-directory name), condition, [batch]
ids <- setdiff(colnames(salmonQuant$counts), 'isoform_id')
stopifnot(setequal(ids, meta$sample_id), !anyDuplicated(meta$sample_id))
design <- data.frame(sampleID = ids, condition = meta$condition[match(ids, meta$sample_id)])
# design$batch <- meta$batch[match(ids, meta$sample_id)]   # extra columns = covariates, see below
print(table(design$condition))

aSwitchList <- importRdata(
    isoformCountMatrix = salmonQuant$counts,
    isoformRepExpression = salmonQuant$abundance,
    designMatrix = design,
    isoformExonAnnoation = 'annotation.gtf',   # (sic); a GTF with CDS lines also supplies annotated ORFs
    isoformNtFasta = 'transcripts.fa',
    addAnnotatedORFs = TRUE,
    showProgress = FALSE
)

aSwitchList <- preFilter(
    aSwitchList,
    geneExpressionCutoff = 1,
    isoformExpressionCutoff = 0,
    IFcutoff = 0.01,
    removeSingleIsoformGenes = TRUE,
    keepIsoformInAllConditions = TRUE
)

# DEXSeq for <=5 replicates per condition, satuRn above (see Tool Selection).
# reduceToSwitchingGenes = FALSE: with TRUE (the function default) a run with no switches stops with an error
aSwitchList <- if (max(table(design$condition)) > 5) {
    isoformSwitchTestSatuRn(aSwitchList, reduceToSwitchingGenes = FALSE, alpha = 0.05, dIFcutoff = 0.1, diagplots = FALSE)
} else {
    isoformSwitchTestDEXSeq(aSwitchList, reduceToSwitchingGenes = FALSE, alpha = 0.05, dIFcutoff = 0.1)
}
f <- aSwitchList$isoformFeatures
sum(f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1, na.rm = TRUE)   # 0 -> see "Count route"
