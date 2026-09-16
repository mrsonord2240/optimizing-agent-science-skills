.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Input 4 (Variant B), continued after the default-nbins segfault.
# nbins is pinned to 4 (the largest value that survives on this build) so the
# substantive IHW-vs-BH comparison can still be made. The crash itself is
# recorded in runs/input4c_ihw_scale.log and runs/input4d_ihw_nbins.log.
suppressMessages(library(IHW))
de_table <- read.csv('F:/OpenScience/audits/bio-experimental-design-multiple-testing/data/synthetic_de_pvalues.csv')
truth <- de_table$is_truly_de == 1
bh <- p.adjust(de_table$pvalue, 'BH')

score <- function(sel, label) {
  R <- sum(sel); V <- sum(sel & !truth); S <- sum(sel & truth)
  cat(sprintf('%-30s R=%5d  true+=%5d  false+=%4d  realized FDP=%.4f  power=%.4f\n',
              label, R, S, V, ifelse(R > 0, V / R, 0), S / sum(truth)))
}

# SKILL.md formula interface, with nbins pinned
res <- ihw(pvalue ~ mean_expression, data = de_table, alpha = 0.05, nbins = 4)
cat('SKILL.md formula interface ihw(pvalue ~ mean_expression, data=, alpha=, nbins=4): OK\n')
de_table$padj_ihw <- adj_pvalues(res)

# the covariate the SHIPPED EXAMPLE uses: drawn at random, null-independent but
# carrying no information about power
set.seed(20260528)
uninformative <- rgamma(nrow(de_table), shape = 2, rate = 0.5)     # examples/ line 45
res_u <- ihw(de_table$pvalue, uninformative, alpha = 0.05, nbins = 4)

# the covariate the skill warns against: group-blind variance (Bourgon 2010)
res_v <- ihw(de_table$pvalue, de_table$overall_variance, alpha = 0.05, nbins = 4)

cat('\n-- against planted truth (18000 genes, 1500 alternatives) --\n')
score(bh < 0.05, 'BH')
score(de_table$padj_ihw < 0.05, 'IHW, mean expression (valid)')
score(adj_pvalues(res_u) < 0.05, 'IHW, examples/ random covariate')
score(adj_pvalues(res_v) < 0.05, 'IHW, group-blind variance')
cat(sprintf('\nweights by bin (mean expression): %s\n',
            paste(round(as.numeric(weights(res, levels_only = TRUE)), 3), collapse = ', ')))
cat(sprintf('weights by bin (examples/ covariate): %s\n',
            paste(round(as.numeric(weights(res_u, levels_only = TRUE)), 3), collapse = ', ')))
