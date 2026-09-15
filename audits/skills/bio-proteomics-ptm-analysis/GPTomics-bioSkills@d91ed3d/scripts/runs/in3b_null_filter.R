# Input 3 addendum: what the Skill's regulated-filter line does when result$ADJUSTED.Model is NULL (PTM-only run)
adjusted <- NULL
res <- tryCatch(adjusted[!is.na(adjusted$adj.pvalue) & adjusted$adj.pvalue < 0.05 & abs(adjusted$log2FC) > 1, ],
                error = function(e) paste('ERROR:', conditionMessage(e)))
print(res)
