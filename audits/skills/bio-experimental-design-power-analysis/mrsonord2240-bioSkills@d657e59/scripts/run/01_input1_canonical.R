# Input 1 (Canonical, regression): bulk RNA-seq replicate sizing, CV=0.3, 1.5-fold, 80% power,
# closed-form vs PROPER simulation cross-check. Depth expressed via the new Depth Units conversion.
suppressPackageStartupMessages({ library(RNASeqPower); library(PROPER) })

reads_millions <- 20
depth_conservative <- 0.1 * reads_millions
cat('depth from 20M-read budget (conservative floor):', depth_conservative, '\n')

n_needed <- rnapower(depth = depth_conservative, cv = 0.3, effect = 1.5, alpha = 0.05, power = 0.80)
cat('n for 80% power at depth', depth_conservative, ':', ceiling(n_needed), 'per group\n')

n_needed_d20 <- rnapower(depth = 20, cv = 0.3, effect = 1.5, alpha = 0.05, power = 0.80)
cat('n for 80% power at depth 20 (vignette-style deep budget):', ceiling(n_needed_d20), 'per group\n')

set.seed(11111)
sim_opts <- RNAseq.SimOptions.2grp(ngenes = 20000, p.DE = 0.05, lOD = 'cheung', lBaselineExpr = 'cheung')
sims <- runSims(Nreps = c(3, 5, 8, 12), sim.opts = sim_opts, nsims = 20, DEmethod = 'edgeR')
powr <- comparePower(sims, alpha.type = 'fdr', alpha.nominal = 0.05, stratify.by = 'expr', delta = log(1.5))
print(summaryPower(powr))
