# Batch-design Input 3 (edge): study already run with all cases on day 1 and all controls on day 2; "can ComBat rescue it?"
# SYNTHETIC log2 protein matrix (1000 proteins, 8 v 8, 80 true changes, day effect 0.8 log2 on 30% of proteins).
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(sva); library(limma)})
set.seed(3); n <- 1000; s <- 16
cond <- factor(rep(c('ctrl', 'case'), each = 8), levels = c('ctrl', 'case')); day <- factor(rep(c('D1', 'D2'), each = 8))
X <- matrix(rnorm(n * s, 22, 0.3), n, s); true <- rep(0, n); true[1:80] <- sample(c(-1, 1), 80, TRUE)
X <- X + outer(true, as.numeric(cond == 'case')); bshift <- ifelse(runif(n) < 0.3, 0.8, 0); X <- X + outer(bshift, as.numeric(day == 'D2'))
cat('design:\n'); print(table(cond, day))
r <- tryCatch({ Xc <- ComBat(dat = X, batch = day, mod = model.matrix(~cond)); 'ran' }, error = function(e) paste('ComBat with condition covariate ERROR:', conditionMessage(e)))
cat(r, '\n')
Xc0 <- ComBat(dat = X, batch = day, mod = NULL)
fit <- eBayes(lmFit(Xc0, model.matrix(~cond))); tt <- topTable(fit, coef = 2, number = Inf, sort.by = 'none')
cat(sprintf('ComBat without covariate, then limma: calls %d | true hits among them %d | nulls %d\n', sum(tt$adj.P.Val < 0.05), sum(tt$adj.P.Val < 0.05 & true != 0), sum(tt$adj.P.Val < 0.05 & true == 0)))
fit2 <- eBayes(lmFit(X, model.matrix(~cond))); t2 <- topTable(fit2, coef = 2, number = Inf, sort.by = 'none')
cat(sprintf('no correction (condition = day): calls %d | true %d | nulls (pure day effect) %d\n', sum(t2$adj.P.Val < 0.05), sum(t2$adj.P.Val < 0.05 & true != 0), sum(t2$adj.P.Val < 0.05 & true == 0)))
d3 <- tryCatch({ lmFit(X, model.matrix(~cond + day)); 'fit' }, warning = function(w) paste('warning:', conditionMessage(w)), error = function(e) paste('error:', conditionMessage(e)))
cat('limma ~cond + day on the confounded design:', d3, '\n')
