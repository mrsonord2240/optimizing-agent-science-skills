# Batch-design Input 5 (stress): unbalanced 3-batch design (batch sizes 10/6/8, case share 80%/50%/12%), 1000 proteins,
# 60 true changes, batch effects. Compare ComBat-cleaned-then-limma vs batch-in-model, 20 seeds. SYNTHETIC.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(sva); library(limma)})
batch <- factor(rep(c('B1', 'B2', 'B3'), c(10, 6, 8)))
cond <- factor(c(rep('case', 8), rep('ctrl', 2), rep('case', 3), rep('ctrl', 3), rep('case', 1), rep('ctrl', 7)), levels = c('ctrl', 'case'))
print(table(cond, batch))
res <- t(sapply(1:20, function(s) {
  set.seed(s); n <- 1000
  X <- matrix(rnorm(n * 24, 22, 0.35), n, 24); tr <- rep(0, n); tr[1:60] <- sample(c(-0.8, 0.8), 60, TRUE)
  X <- X + outer(tr, as.numeric(cond == 'case')) + t(sapply(1:n, function(i) c(B1 = 0, B2 = rnorm(1, 0, 0.5), B3 = rnorm(1, 0, 0.5))[as.character(batch)]))
  Xc <- suppressMessages(ComBat(dat = X, batch = batch, mod = model.matrix(~cond), prior.plots = FALSE))
  t1 <- topTable(eBayes(lmFit(Xc, model.matrix(~cond))), coef = 2, number = Inf, sort.by = 'none')
  t2 <- topTable(eBayes(lmFit(X, model.matrix(~cond + batch))), coef = 'condcase', number = Inf, sort.by = 'none')
  c(combat_calls = sum(t1$adj.P.Val < 0.05), combat_fp = sum(t1$adj.P.Val < 0.05 & tr == 0), combat_nullp05 = mean(t1$P.Value[tr == 0] < 0.05),
    model_calls = sum(t2$adj.P.Val < 0.05), model_fp = sum(t2$adj.P.Val < 0.05 & tr == 0), model_nullp05 = mean(t2$P.Value[tr == 0] < 0.05))
}))
print(round(colMeans(res), 3))
cat(sprintf('realized FDR (pooled over 20 seeds): ComBat-then-test %.1f%% | batch in model %.1f%%\n', 100 * sum(res[, 'combat_fp']) / sum(res[, 'combat_calls']), 100 * sum(res[, 'model_fp']) / sum(res[, 'model_calls'])))
