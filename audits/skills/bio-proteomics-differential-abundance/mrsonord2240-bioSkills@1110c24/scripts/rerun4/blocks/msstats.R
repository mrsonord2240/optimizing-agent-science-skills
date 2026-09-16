library(MSstats)

input <- MaxQtoMSstatsFormat(evidence = evidence, proteinGroups = protein_groups,
                             annotation = annotation, use_log_file = FALSE)  # annotation: Raw.file, Condition, BioReplicate, IsotopeLabelType
proc <- dataProcess(input, normalization = 'equalizeMedians', summaryMethod = 'TMP',
                    censoredInt = 'NA', MBimpute = FALSE, use_log_file = FALSE)

contrast <- matrix(c(-1, 1), nrow = 1,
                   dimnames = list('Treatment-Control', c('Control', 'Treatment')))  # order = levels(GROUP)
res <- groupComparison(contrast.matrix = contrast, data = proc, use_log_file = FALSE)$ComparisonResult
res$Protein <- as.character(res$Protein)

undetected <- res[res$issue %in% 'oneConditionMissing', ]   # infinite log2FC; report as undetected, not as a ratio
tested <- res[is.finite(res$log2FC) & !is.na(res$adj.pvalue), ]
# columns: Protein, Label, log2FC, SE, Tvalue, DF, pvalue, adj.pvalue, issue (adj.pvalue is the BH p)
