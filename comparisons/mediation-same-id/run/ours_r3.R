# OURS request 3: same data. Follows OUR "High-Dimensional EWAS Mediation (HIMA2)" block as written (formula interface, parallel=TRUE, ncore=8).
source('F:/OpenScience/comparisons/mediation-same-id/run/common.R')
suppressMessages(library(HIMA)); cat('HIMA', as.character(packageVersion('HIMA')), '\n')
ph <- read.csv(file.path(D, 'C_pheno.csv')); M_matrix <- as.matrix(read.csv(file.path(D, 'C_mediators.csv')))
dat <- ph; set.seed(1)
dat <- na.omit(dat[, c('disease', 'genotype', 'age', 'sex')])
result <- try_run('hima as written', hima(disease ~ genotype + age + sex, data.pheno = dat, data.M = M_matrix, mediator.type = 'gaussian',
  penalty = 'DBlasso', scale = TRUE, sigcut = 0.05, parallel = TRUE, ncore = 8, verbose = TRUE))
if (is.null(result)) { cat('--- adapt: parallel=FALSE ---\n')
  result <- try_run('hima parallel=FALSE', hima(disease ~ genotype + age + sex, data.pheno = dat, data.M = M_matrix, mediator.type = 'gaussian',
    penalty = 'DBlasso', scale = TRUE, sigcut = 0.05, parallel = FALSE, verbose = FALSE)) }
print(class(result)); print(result)
ids <- result$ID; cat('nrow(result) is', is.null(nrow(result)), '(NULL as their text says)\n'); cat('recovered:', ids, '\n')
cat('decoys flagged:', intersect(ids, c('M3', 'M4')), '\n')
stopifnot(all(c('M1', 'M2') %in% ids)); cat('ASSERT pass: recovers M1 and M2\n')
