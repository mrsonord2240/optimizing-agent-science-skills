.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressMessages(library(IHW))
d <- read.csv('F:/OpenScience/audits/bio-experimental-design-multiple-testing/data/synthetic_de_pvalues.csv')
truth <- d$is_truly_de == 1
which_cov <- commandArgs(TRUE)[1]
cov <- switch(which_cov,
  "mean"   = d$mean_expression,
  "random" = { set.seed(20260528); rgamma(nrow(d), shape = 2, rate = 0.5) },  # examples/ line 45
  "var"    = d$overall_variance)
r <- ihw(d$pvalue, cov, alpha = 0.05, nbins = 4)
sel <- adj_pvalues(r) < 0.05
R <- sum(sel); V <- sum(sel & !truth); S <- sum(sel & truth)
cat(sprintf('IHW covariate=%-7s R=%5d true+=%5d false+=%4d realized FDP=%.4f power=%.4f weights=%s\n',
    which_cov, R, S, V, ifelse(R>0, V/R, 0), S/sum(truth),
    paste(round(as.numeric(weights(r, levels_only = TRUE)), 3), collapse='/')))
