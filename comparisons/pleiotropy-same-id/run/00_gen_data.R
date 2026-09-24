# Synthetic harmonised two-sample MR summary stats with planted truth. Shared by both sides.
# Same gamma (beta.exposure), same SEs and same outcome noise across datasets A-D, so the only difference is the planted alpha.
set.seed(2026)
n <- 60
gamma <- abs(rnorm(n, 0.08, 0.03)); gamma[gamma < 0.02] <- 0.02
se_x <- 0.010; se_y <- 0.012
noise <- rnorm(n, 0, se_y)
theta <- 0.30
mk <- function(alpha, theta, label) {
  by <- theta * gamma + alpha + noise
  d <- data.frame(SNP = paste0("rs", 1:n),
    beta.exposure = gamma, se.exposure = se_x,
    beta.outcome = by, se.outcome = se_y,
    effect_allele.exposure = "A", other_allele.exposure = "G",
    effect_allele.outcome = "A", other_allele.outcome = "G",
    eaf.exposure = runif(n, .15, .85), eaf.outcome = NA_real_,
    id.exposure = "exposure", id.outcome = "outcome", exposure = "X", outcome = "Y",
    samplesize.exposure = 500000, samplesize.outcome = 500000,
    units.exposure = "SD", units.outcome = "SD",
    pval.exposure = 2*pnorm(-abs(gamma/se_x)), pval.outcome = 2*pnorm(-abs(by/se_y)),
    mr_keep = TRUE, stringsAsFactors = FALSE)
  d$eaf.outcome <- d$eaf.exposure
  write.csv(d, file.path("F:/OpenScience/comparisons/pleiotropy-same-id/run/data", paste0(label, ".csv")), row.names = FALSE)
  d
}
A <- mk(rnorm(n, 0, 0.015), theta, "A_balanced")                 # truth: theta .30, mean(alpha)=0
B <- mk(rnorm(n, 0.02, 0.008), theta, "B_directional")           # truth: theta .30, mean(alpha)=+0.02, InSIDE holds
outl <- c(7, 19, 28, 36, 47, 55)
alpha_c <- rep(0, n); alpha_c[outl] <- c(0.06, -0.05, 0.07, 0.055, -0.06, 0.065)
C <- mk(alpha_c, theta, "C_outliers")                            # truth: theta .30, 6 planted outliers
D <- mk(0.5 * gamma + rnorm(n, 0, 0.004), 0.0, "D_chp")          # truth: theta 0 (NULL); alpha = 0.5*gamma -> correlated pleiotropy, InSIDE violated
writeLines(paste0("rs", outl), "F:/OpenScience/comparisons/pleiotropy-same-id/run/data/C_true_outliers.txt")
cat("mean F:", mean((gamma/se_x)^2), "\n")
for (nm in c("A","B","C","D")) { d <- get(nm); cat(nm, "rows", nrow(d), "\n") }
