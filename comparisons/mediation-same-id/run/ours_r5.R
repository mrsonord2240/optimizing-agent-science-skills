# OURS request 5: same data, OUR 4-way block as written (CMAverse cmest EMint=TRUE, rb, paramfunc, bootstrap; nboot=200 instead of 1000 for time).
source('F:/OpenScience/comparisons/mediation-same-id/run/common.R'); suppressMessages(library(CMAverse))
dat <- read.csv(file.path(D, 'D_interaction.csv')); set.seed(1)
res <- try_run('cmest 4way', cmest(data = dat, model = 'rb', outcome = 'y_cont', exposure = 'genotype', mediator = 'expression',
  basec = c('age', 'sex'), EMint = TRUE, mreg = list('linear'), yreg = 'linear', astar = 0, a = 1, mval = list(0),
  estimation = 'paramfunc', inference = 'bootstrap', nboot = 200))
s <- summary(res)$summarydf; print(round(s[, c('Estimate', 'Std.error', '95% CIL', '95% CIU')], 3))
cat('TRUTH: cde 0.2, intref 0, intmed 0.2, pnie 0.3, te 0.7\n')
g <- function(n) s[n, 'Estimate']; cat('names:', rownames(s), '\n')
stopifnot(abs(g('cde') - 0.2) < 0.12, abs(g('intmed') - 0.2) < 0.12, abs(g('pnie') - 0.3) < 0.12, abs(g('te') - 0.7) < 0.15); cat('ASSERT pass: cde/intmed/pnie/te within tolerance of planted truth\n')
