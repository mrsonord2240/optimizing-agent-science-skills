library(QFeatures)
library(msqrob2)

# peptide_wide: one row per precursor; columns 'feature', 'protein', then one intensity column per run
runs <- sample_info$run
col_data <- data.frame(quantCols = runs, condition = factor(sample_info$condition),
                       sample = factor(runs), row.names = runs)  # quantCols column is required by readQFeatures
pe <- readQFeatures(assayData = peptide_wide, quantCols = runs, colData = col_data, name = 'peptideRaw')
pe <- zeroIsNA(pe, 'peptideRaw')
pe <- logTransform(pe, base = 2, i = 'peptideRaw', name = 'peptideLog')
rowData(pe[['peptideLog']])$nNonZero <- rowSums(!is.na(assay(pe[['peptideLog']])))
pe <- filterFeatures(pe, ~ nNonZero >= 2, keep = TRUE)  # keep=TRUE: the variable exists only on peptideLog

# undetected list, taken BEFORE aggregation: msqrob2 reports these as adjPval = NA, not as a list
cond <- colData(pe)$condition  # colData lives on the QFeatures object; pe[['peptideLog']]$condition is NULL
obs <- sapply(levels(cond), function(g)
  tapply(rowSums(!is.na(assay(pe[['peptideLog']])[, cond == g, drop = FALSE])),
         rowData(pe[['peptideLog']])$protein, sum))
undetected <- rownames(obs)[apply(obs, 1, min) == 0]  # report as "undetected in group X", never as a fold change

pe <- aggregateFeatures(pe, i = 'peptideLog', fcol = 'protein', name = 'protein',
                        fun = MsCoreUtils::robustSummary, na.rm = TRUE)
pe <- msqrob(pe, i = 'protein', formula = ~condition, robust = TRUE)
L <- makeContrast('conditionTreatment = 0', parameterNames = 'conditionTreatment')
pe <- hypothesisTest(pe, i = 'protein', contrast = L)

res <- rowData(pe[['protein']])$conditionTreatment  # columns: logFC, se, df, t, pval, adjPval (no adj.P.Val)
res$protein <- rownames(pe[['protein']])
untestable <- res$protein[is.na(res$adjPval)]       # report these; they are not "not significant"
res <- res[!is.na(res$adjPval), ]
