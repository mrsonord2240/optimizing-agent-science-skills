# Shared synthetic data for the pair comparison (both sides get the SAME files).
# A: planted mediation (no confounding). B: sequential ignorability violated by latent U (true ACME = 0).
# C: high-dimensional mediators, 2 true (M1,M2), 2 decoys (M3 alpha only, M4 beta only).
out <- 'F:/OpenScience/comparisons/mediation-same-id/data'
set.seed(20260921)
n <- 1500
mk_cov <- function(n) data.frame(genotype = rbinom(n, 2, 0.3), age = rnorm(n, 55, 10),
                                 sex = rbinom(n, 1, 0.5), pc1 = rnorm(n), pc2 = rnorm(n))
# ---- A ----
A <- mk_cov(n)
A$expression <- 0.5*A$genotype + 0.01*A$age - 0.1*A$sex + 0.2*A$pc1 + rnorm(n, 0, 0.8)
A$y_cont <- 0.2*A$genotype + 0.6*A$expression + 0.01*A$age + 0.1*A$sex + rnorm(n)
lat <- 0.2*A$genotype + 0.6*(A$expression - 0.85) + 0.01*(A$age-55) + 0.1*A$sex   # probit latent
A$disease <- as.integer(lat + rnorm(n) > 0)
write.csv(A, file.path(out, 'A_planted.csv'), row.names = FALSE)
# truth on the probability scale by Monte Carlo from the TRUE parameters (avg over observed covariates)
set.seed(1); R <- 200
d <- replicate(R, {
  eps <- rnorm(n, 0, 0.8)
  base <- 0.01*A$age - 0.1*A$sex + 0.2*A$pc1 + eps
  m1 <- 0.5*1 + base; m0 <- 0.5*0 + base
  cov <- 0.01*(A$age-55) + 0.1*A$sex
  p <- function(g, m) pnorm(0.2*g + 0.6*(m - 0.85) + cov)
  c(acme0 = mean(p(0, m1) - p(0, m0)), acme1 = mean(p(1, m1) - p(1, m0)),
    ade0 = mean(p(1, m0) - p(0, m0)), tot = mean(p(1, m1) - p(0, m0)))
})
truthA <- rowMeans(d)
# ---- B ----
set.seed(777)
B <- mk_cov(n); U <- rnorm(n); lam <- 0.5
B$expression <- 0.5*B$genotype + 0.01*B$age - 0.1*B$sex + 0.2*B$pc1 + lam*U + rnorm(n, 0, 0.8)
B$y_cont <- 0.2*B$genotype + 0.0*B$expression + 0.01*B$age + 0.1*B$sex + lam*U + rnorm(n)  # M does NOT cause Y
write.csv(B, file.path(out, 'B_confounded.csv'), row.names = FALSE)
# ---- C ----
set.seed(4242); nc <- 800; p <- 100
C <- mk_cov(nc)[, c('genotype','age','sex')]
alpha <- rep(0, p); alpha[c(1,2,3)] <- 0.7
beta <- rep(0, p); beta[c(1,2,4)] <- 1.0
M <- sapply(1:p, function(j) alpha[j]*C$genotype + rnorm(nc)); colnames(M) <- paste0('M', 1:p)
C$y_cont <- as.numeric(0.3*C$genotype + M %*% beta + 0.01*C$age + rnorm(nc))
C$disease <- rbinom(nc, 1, plogis(-1.5 + 0.3*C$genotype + as.numeric(M %*% beta)*0.8))
write.csv(C, file.path(out, 'C_pheno.csv'), row.names = FALSE)
write.csv(M, file.path(out, 'C_mediators.csv'), row.names = FALSE)
truth <- list(
  A = list(acme_cont = 0.3, ade_cont = 0.2, total_cont = 0.5, prop_med_cont = 0.6, prob_scale = as.list(truthA)),
  B = list(acme = 0, ade = 0.2, total = 0.2, planted_rho = (lam^2)/sqrt((lam^2+0.64)*(lam^2+1))),
  C = list(true_mediators = c('M1','M2'), decoys = c('M3','M4'), prevalence = mean(C$disease)))
saveRDS(truth, file.path(out, 'truth.rds'))
print(truth)
