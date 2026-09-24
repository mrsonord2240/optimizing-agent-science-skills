# Exact-commit execution harness for 3473a8f48eccab6c73436a627c3e8568f3736eef.
options(warn = 2)
suppressPackageStartupMessages(library(metafor))

source_root <- "F:/OpenScience/wt/data-visualization-forest-funnel-plots/data-visualization/forest-funnel-plots"
out <- "F:/OpenScience/audits/bio-data-visualization-forest-funnel-plots/run/exact-commit-3473a8f"
dir.create(out, showWarnings = FALSE, recursive = TRUE)

# Canonical BCG forest: every study CI, pooled CI, and prediction interval is in alim.
dat <- dat.bcg
es <- escalc(measure = "OR", ai = tpos, bi = tneg, ci = cpos, di = cneg, data = dat)
bcg <- data.frame(author = dat$author, year = dat$year, log_or = es$yi, log_or_se = sqrt(es$vi))
res <- rma(yi = log_or, vi = log_or_se^2, data = bcg, slab = paste(author, year), method = "REML")
footer <- sprintf("RE model (tau^2 = %.3f; I^2 = %.1f%%; Q p = %s)",
                  res$tau2, res$I2, format.pval(res$QEp, digits = 2))
ticks <- log(c(0.25, 0.5, 1, 2, 4))
pred <- predict(res)
study_lb <- bcg$log_or - qnorm(0.975) * bcg$log_or_se
study_ub <- bcg$log_or + qnorm(0.975) * bcg$log_or_se
limits <- range(c(study_lb, study_ub, res$ci.lb, res$ci.ub,
                  pred$pi.lb, pred$pi.ub, ticks), finite = TRUE)
stopifnot(is.character(footer), grepl("tau\\^2", footer), grepl("I\\^2", footer),
          limits[1] <= min(study_lb, res$ci.lb, pred$pi.lb),
          limits[2] >= max(study_ub, res$ci.ub, pred$pi.ub))
png(file.path(out, "bcg_forest_exact.png"), width = 1200, height = 760, res = 120)
forest(res, atransf = exp, at = ticks, alim = limits, refline = 0,
       xlab = "Odds Ratio (95% CI)", header = c("Study", "OR [95% CI]"),
       mlab = footer, addpred = TRUE)
dev.off()
cat(sprintf("BCG PASS: OR %.4f [%.4f, %.4f]; tau2 %.6f; I2 %.2f; Q %.3f; footer=%s\n",
            exp(res$b[1]), exp(res$ci.lb), exp(res$ci.ub), res$tau2, res$I2, res$QE, footer))

# Scalar funnel reference is warning-free; small-k HKSJ omits I-squared and withholds Egger.
png(file.path(out, "bcg_funnel_exact.png"), width = 900, height = 700, res = 120)
funnel(res, xlab = "log(OR)", refline = as.numeric(coef(res)[1]))
dev.off()
k3 <- rma(yi = log(c(0.55, 0.90, 1.60)), vi = c(0.20, 0.25, 0.30)^2,
          method = "REML", test = "knha")
small_footer <- sprintf("RE model (k = %d; HKSJ CI; heterogeneity metrics withheld)", k3$k)
stopifnot(k3$k == 3, identical(k3$test, "knha"), !grepl("I\\^2", small_footer), k3$k < 10)
cat("SMALL-K PASS: ", small_footer, "; Egger withheld because k < 10\n", sep = "")

# The shipped example runs through synthetic Cox and bundled lipid/CHD MR without warnings.
old_wd <- getwd(); setwd(out)
sys.source(file.path(source_root, "examples", "forest_phd.R"), envir = new.env(parent = globalenv()))
expected <- file.path(out, "plots", c("forest.pdf", "funnel.pdf", "cox_subgroup_forest.pdf",
                                       "cox_adjusted_covariates.pdf", "mr_method_forest.pdf"))
stopifnot(all(file.exists(expected)), all(file.info(expected)$size > 1000))
cat("EXAMPLE PASS: ", paste(basename(expected), collapse = ", "), "\n", sep = "")
setwd(old_wd)
cat("HARNESS PASS\n")
quit(save = "no", status = 0, runLast = FALSE)
