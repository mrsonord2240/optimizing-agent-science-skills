# THEIRS request 3: 100 candidate mediators, binary disease outcome (dataset C). True mediators M1,M2; decoys M3 (alpha only), M4 (beta only).
# Follows THEIR "High-Dimensional Mediation (HDMA)" block as written; on failure, adapt per their Version Compatibility text (introspect and adapt).
source('F:/OpenScience/comparisons/mediation-same-id/run/common.R')
suppressMessages(library(HIMA)); cat('HIMA', as.character(packageVersion('HIMA')), '\n')
ph <- read.csv(file.path(D, 'C_pheno.csv')); M <- as.matrix(read.csv(file.path(D, 'C_mediators.csv')))
dat <- cbind(ph, M); mediator_cols <- colnames(M); covariate_cols <- c('age', 'sex')
set.seed(1)
cat('--- as written ---\n')
result <- try_run('hima as written', hima(X = dat$genotype, Y = dat$disease, M = as.matrix(dat[, mediator_cols]),
  COV.XM = as.matrix(dat[, covariate_cols]), Y.family = 'binomial', M.family = 'gaussian', penalty = 'MCP'))
asw <- !is.null(result)
if (asw) { print(class(result)); sig <- try_run('BH.FDR subset', result[result$BH.FDR < 0.05, ]); print(sig) }
cat('--- adapted: their code has Y.family/M.family + BH.FDR (HIMA 2.2 names); 2.3.4 classic engine is hima_classic(X,M,Y,COV.XM,Y.type,M.type,penalty) ---\n')
res2 <- try_run('hima_classic adapted', hima_classic(X = dat$genotype, M = as.matrix(dat[, mediator_cols]), Y = dat$disease,
  COV.XM = as.matrix(dat[, covariate_cols]), Y.type = 'binary', M.type = 'gaussian', penalty = 'MCP', verbose = FALSE))
print(class(res2)); print(res2)
ids <- if (is.data.frame(res2)) res2$Index else res2$ID  # hima_classic: mediator name is in column 'Index' (rownames are 1..k)
cat('adapted recovered:', ids, '\n'); cat('truth: M1,M2 true; M3,M4 decoys\n')
stopifnot(all(c('M1', 'M2') %in% ids)); cat('ASSERT pass: adapted run recovers M1 and M2\n')
cat('decoys flagged:', intersect(ids, c('M3', 'M4')), '\n')
