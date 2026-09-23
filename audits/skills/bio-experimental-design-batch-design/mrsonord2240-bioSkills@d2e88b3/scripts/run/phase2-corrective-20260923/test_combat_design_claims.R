# Synthetic regression checks for the Skill's confounding and unbalanced-correction claims.
suppressPackageStartupMessages({ library(sva); library(limma) })
set.seed(20260923)

# Perfect confounding: ComBat must reject a biological covariate aliased with batch.
n_gene <- 300L; n <- 12L
condition <- factor(rep(c("ctrl", "case"), each = 6))
batch <- factor(rep(c("B1", "B2"), each = 6))
mat <- matrix(rnorm(n_gene * n, 8, 0.3), nrow = n_gene)
mat[1:30, condition == "case"] <- mat[1:30, condition == "case"] + 1
model <- model.matrix(~ condition)
confound_error <- tryCatch({ ComBat(dat = mat, batch = batch, mod = model); NULL }, error = function(e) conditionMessage(e))
stopifnot(!is.null(confound_error), grepl("confound", confound_error, ignore.case = TRUE))

# Partial imbalance: batch is estimable when included, and the fit has no non-estimable coefficients.
condition2 <- factor(c(rep("ctrl", 8), rep("case", 4), rep("ctrl", 2), rep("case", 10)))
batch2 <- factor(rep(c("B1", "B2", "B3"), each = 8))
mat2 <- matrix(rnorm(n_gene * 24, 8, 0.3), nrow = n_gene)
mat2[, batch2 == "B2"] <- mat2[, batch2 == "B2"] + 0.5
design2 <- model.matrix(~ condition2 + batch2)
fit <- lmFit(mat2, design2)
stopifnot(!any(is.na(fit$coefficients)))
cat("PASS: ComBat rejected perfect confounding; condition+batch model was estimable for partial imbalance.\n")
