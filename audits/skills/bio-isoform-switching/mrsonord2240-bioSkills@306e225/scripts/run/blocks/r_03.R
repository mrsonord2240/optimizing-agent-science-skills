library(tximport); library(DRIMSeq); library(DEXSeq); library(stageR)

# meta: data.frame(sample_id, condition); files: named vector of quant.sf paths (names = sample_id)
# tx2gene: data.frame(tx = transcript ID, gene = gene ID)
txi <- tximport(files, type = 'salmon', txOut = TRUE, countsFromAbundance = 'no')
cts <- txi$counts
txdf <- data.frame(gene_id = tx2gene$gene[match(rownames(cts), tx2gene$tx)], feature_id = rownames(cts), cts, check.names = FALSE)
txdf <- txdf[!is.na(txdf$gene_id), ]

samples <- data.frame(sample_id = colnames(cts), condition = factor(meta$condition[match(colnames(cts), meta$sample_id)]))
stopifnot(!anyNA(samples$condition))

n <- nrow(samples); n_small <- min(table(samples$condition))
d <- dmDSdata(counts = txdf, samples = samples)
d <- dmFilter(d, min_samps_gene_expr = n, min_gene_expr = 10,
              min_samps_feature_expr = n_small, min_feature_expr = 10,
              min_samps_feature_prop = n_small, min_feature_prop = 0.1)

# Qualify with DRIMSeq:: -- once DEXSeq is attached, Biobase::samples masks DRIMSeq::samples() ("unable to find an
# inherited method for function 'samples' for signature 'object = "dmDSdata"'"); counts() is also exported by
# DEXSeq, DESeq2 and BiocGenerics, so qualify it too.
cnt <- DRIMSeq::counts(d)
dxd <- DEXSeqDataSet(
    countData = round(as.matrix(cnt[, samples$sample_id])),
    sampleData = DRIMSeq::samples(d),
    design = ~ sample + exon + condition:exon,
    featureID = cnt$feature_id,
    groupID = cnt$gene_id
)
dxd <- estimateSizeFactors(dxd)
dxd <- estimateDispersions(dxd, quiet = TRUE)
dxd <- testForDEU(dxd, reducedModel = ~ sample + exon)
dxr <- DEXSeqResults(dxd, independentFiltering = FALSE)
qval <- perGeneQValue(dxr)

pConfirmation <- matrix(dxr$pvalue, ncol = 1, dimnames = list(dxr$featureID, NULL))
pConfirmation[is.na(pConfirmation)] <- 1
tx2gene_d <- data.frame(transcript = dxr$featureID, gene = dxr$groupID)

stageRObj <- stageRTx(pScreen = qval, pConfirmation = pConfirmation, pScreenAdjusted = TRUE, tx2gene = tx2gene_d)
stageRObj <- stageWiseAdjustment(stageRObj, method = 'dtu', alpha = 0.05)

results <- getAdjustedPValues(stageRObj, order = FALSE, onlySignificantGenes = FALSE)   # geneID, txID, gene, transcript
