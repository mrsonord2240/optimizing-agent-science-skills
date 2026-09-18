# Input 6 (NEW -- not in the pre-fix audit): SKILL.md's Quantitative Thresholds table and
# the IHW failure-mode section both assert that IHW's automatic nbins formula
# (floor(m/1500), capped 40) collapses to a SINGLE bin below m ~ 1500, and that at nbins==1
# IHW literally reduces to plain Benjamini-Hochberg. Test this literally on a small family
# where auto nbins should equal 1, and confirm IHW's rejections exactly match BH.
library(IHW)
set.seed(31415)
m <- 800  # < 1500 -> floor(800/1500) = 0 -> should hit the nbins==1 branch
p <- c(rbeta(80, 0.4, 6), runif(m - 80))
covariate <- runif(m)  # independent of p under null by construction

res <- tryCatch(ihw(p, covariate, alpha = 0.05), error = function(e) { cat("ERROR:", conditionMessage(e), "\n"); NULL })
if (!is.null(res)) {
  cat(sprintf("nbins used: %d\n", res@nbins))
  ihw_rej <- adj_pvalues(res) < 0.05
  bh_rej  <- p.adjust(p, method = 'BH') < 0.05
  cat(sprintf("IHW rejections: %d | BH rejections: %d | identical sets: %s\n",
              sum(ihw_rej), sum(bh_rej), all(ihw_rej == bh_rej)))
  cat(sprintf("max abs diff IHW padj vs BH padj: %.10f\n", max(abs(adj_pvalues(res) - p.adjust(p, method='BH')))))
}
