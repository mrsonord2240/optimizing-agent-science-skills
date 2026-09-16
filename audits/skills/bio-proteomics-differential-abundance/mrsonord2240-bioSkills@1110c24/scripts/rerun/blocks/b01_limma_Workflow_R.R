library(limma)

cond <- factor(sample_info$condition)
# Valid-value filter BEFORE lmFit: >= 2 values in every group (study choice; 3 of 4 is common)
n_valid <- sapply(levels(cond), function(g) rowSums(!is.na(protein_matrix[, cond == g, drop = FALSE])))
protein_matrix <- protein_matrix[apply(n_valid >= 2, 1, all), ]

design <- model.matrix(~0 + condition + batch, data = sample_info)  # batch in the model, not removed first
colnames(design)[seq_len(nlevels(cond))] <- levels(cond)

fit <- lmFit(protein_matrix, design)
contrast_matrix <- makeContrasts(Treatment - Control, levels = design)
fit2 <- contrasts.fit(fit, contrast_matrix)
fit2 <- eBayes(fit2, trend = TRUE, robust = TRUE)  # trend mandatory for label-free; robust Winsorizes outliers

results <- topTable(fit2, coef = 1, number = Inf, adjust.method = 'BH')
# columns: logFC, AveExpr, t, P.Value, adj.P.Val, B  (adj.P.Val is the BH p; there is no $FDR)
