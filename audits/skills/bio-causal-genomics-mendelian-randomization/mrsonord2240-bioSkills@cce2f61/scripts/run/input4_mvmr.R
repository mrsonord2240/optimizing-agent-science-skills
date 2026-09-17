# Input 4 (regression) -- MVMR of two correlated exposures (LDL/HDL-like) jointly on an
# outcome (CHD-like), following SKILL.md's MVMR-with-Conditional-F section. Correlated
# exposure architecture deliberately built in to push conditional F below 10 and trigger
# the qhet_mvmr fallback branch. Synthetic, planted true direct effects (0.30, -0.10).
library(MVMR)

set.seed(21)
n_snps <- 60
true_b1 <- 0.30
true_b2 <- -0.10

# shared latent factor to correlate exposure1/exposure2 instrument strength (weak conditional F)
shared <- rnorm(n_snps, 0, 0.02)
beta_x1 <- shared + rnorm(n_snps, 0.03, 0.01)
beta_x2 <- shared * 0.9 + rnorm(n_snps, 0.02, 0.01)
se_x1 <- runif(n_snps, 0.008, 0.014)
se_x2 <- runif(n_snps, 0.009, 0.015)
beta_y <- true_b1 * beta_x1 + true_b2 * beta_x2 + rnorm(n_snps, 0, 0.01)
se_y <- runif(n_snps, 0.010, 0.018)

mvmr_dat <- format_mvmr(
    BXGs = cbind(beta_x1, beta_x2), BYG = beta_y,
    seBXGs = cbind(se_x1, se_x2), seBYG = se_y,
    RSID = paste0("rs", 1:n_snps)
)

condF <- strength_mvmr(r_input = mvmr_dat, gencov = 0)
cat("--- Conditional F per exposure ---\n")
print(condF)

mv_ivw <- ivw_mvmr(r_input = mvmr_dat)
cat("\n--- MVMR-IVW ---\n")
print(mv_ivw)
cat("True direct effects: exposure1=", true_b1, " exposure2=", true_b2, "\n")

if (any(condF < 10)) {
    cat("\n--- Conditional F < 10 detected -- switching to qhet_mvmr per SKILL.md ---\n")
    pcor <- cor(cbind(beta_x1, beta_x2))
    qhet <- qhet_mvmr(r_input = mvmr_dat, pcor = pcor, CI = TRUE, iterations = 100)
    print(qhet)
}
