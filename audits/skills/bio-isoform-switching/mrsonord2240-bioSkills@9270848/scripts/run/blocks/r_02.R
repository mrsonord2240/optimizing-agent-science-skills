# Same import, filter and test as the workflow, on any design; returns the genes called
call_genes <- function(design) {
    sl <- importRdata(isoformCountMatrix = salmonQuant$counts, isoformRepExpression = salmonQuant$abundance,
                      designMatrix = design, isoformExonAnnoation = 'annotation.gtf', isoformNtFasta = 'transcripts.fa',
                      addAnnotatedORFs = FALSE, showProgress = FALSE, quiet = TRUE)
    sl <- preFilter(sl, geneExpressionCutoff = 1, isoformExpressionCutoff = 0, IFcutoff = 0.01,
                    removeSingleIsoformGenes = TRUE, keepIsoformInAllConditions = TRUE, quiet = TRUE)
    sl <- if (max(table(design$condition)) > 5) {
        isoformSwitchTestSatuRn(sl, reduceToSwitchingGenes = FALSE, alpha = 0.05, dIFcutoff = 0.1, diagplots = FALSE, quiet = TRUE)
    } else {
        isoformSwitchTestDEXSeq(sl, reduceToSwitchingGenes = FALSE, alpha = 0.05, dIFcutoff = 0.1, quiet = TRUE)
    }
    f <- sl$isoformFeatures
    unique(f$gene_id[!is.na(f$isoform_switch_q_value) & f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1])
}

# Shuffled labels that keep the group sizes and share only the chance overlap with the true split
lab <- design$condition; n <- length(lab); in1 <- lab == lab[1]; k <- sum(in1)
canon <- function(v) paste(v == v[1], collapse = '')          # a split and its mirror image are the same split
seen <- canon(in1); perms <- list(); set.seed(1)
for (i in 1:5000) {
    if (length(perms) >= 10) break
    p <- sample(lab); key <- canon(p == lab[1])
    if (abs(sum(p == lab[1] & in1) - k * k / n) <= 0.5 && !key %in% seen) { seen <- c(seen, key); perms[[length(perms) + 1]] <- p }
}
observed <- length(call_genes(design))
permuted <- sapply(perms, function(p) { d <- design; d$condition <- p; tryCatch(length(call_genes(d)), error = function(e) NA) })
cat('observed', observed, 'genes; label-permuted:', permuted, '\n')
