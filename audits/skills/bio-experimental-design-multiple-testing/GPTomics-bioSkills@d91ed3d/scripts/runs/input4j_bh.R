.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
d <- read.csv('F:/OpenScience/audits/bio-experimental-design-multiple-testing/data/synthetic_de_pvalues.csv')
truth <- d$is_truly_de == 1; sel <- p.adjust(d$pvalue,'BH') < 0.05
cat(sprintf('BH                      R=%5d true+=%5d false+=%4d realized FDP=%.4f power=%.4f\n',
    sum(sel), sum(sel&truth), sum(sel&!truth), sum(sel&!truth)/sum(sel), sum(sel&truth)/sum(truth)))
