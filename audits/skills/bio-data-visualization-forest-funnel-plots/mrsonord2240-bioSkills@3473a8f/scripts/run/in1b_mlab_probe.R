# Probe (root cause of the "paste" summary label): class of the SKILL's mlab, and two candidate fixes; plus MR forest without SNP rows
suppressMessages({library(metafor); library(MendelianRandomization)})
D <- "F:/OpenScience/audits/bio-data-visualization-forest-funnel-plots"
studies <- read.csv(file.path(D, "data/bcg_logor.csv"))
res <- rma(yi = log_or, vi = log_or_se^2, data = studies, slab = paste(author, year), method = 'REML')
m <- bquote(paste('RE Model (Q = ', .(round(res$QE, 2)), ')'))
cat("class(bquote(paste(...))) =", class(m), " | is.expression:", is.expression(m), " | is.character:", is.character(m), "\n")
png(file.path(D, "figs/in1_mlab_fixes.png"), width = 1000, height = 520, res = 100)
par(mfrow = c(1, 1))
forest(res, atransf = exp, at = log(c(0.25,0.5,1,2,4)), refline = 0, xlab = 'Odds Ratio (95% CI)', header = c('Study','OR [95% CI]'),
       mlab = as.expression(bquote(paste('RE Model (Q = ', .(round(res$QE, 2)), ', df = ', .(res$k - 1), '; ', I^2, ' = ', .(round(res$I2, 1)), '%)'))),
       addpred = TRUE)
dev.off()
cat("as.expression(bquote(...)) fix rendered -> see figs/in1_mlab_fixes.png\n")
mrin <- mr_input(bx = ldlc, bxse = ldlcse, by = chdlodds, byse = chdloddsse)
png(file.path(D, "figs/in5_mr_forest_nosnp.png"), width = 900, height = 400, res = 110)
print(mr_forest(mrin, snp_estimates = FALSE, methods = c('ivw','wmedian','mbe','egger'))); dev.off()
