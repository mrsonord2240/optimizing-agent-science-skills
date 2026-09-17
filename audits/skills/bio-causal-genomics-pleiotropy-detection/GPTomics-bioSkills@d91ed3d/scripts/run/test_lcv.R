setwd('F:/OpenScience/audits/bio-causal-genomics-pleiotropy-detection/run/lcv/R')
set.seed(1)
m <- 2000
ell <- runif(m, 1, 50)
rho_true <- 0.3
z1 <- rnorm(m, 0, sqrt(ell)) 
z2 <- rho_true * z1 + rnorm(m, 0, sqrt(ell))
source('RunLCV.R')
res_lcv <- RunLCV(ell, z1, z2, no.blocks = 20)
cat('Fields returned by RunLCV:\n')
print(names(res_lcv))
cat('\nSKILL.md says: res_lcv$gcp  ->', is.null(res_lcv$gcp), '(TRUE means NULL -- field does not exist)\n')
cat('Actual field is res_lcv$gcp.pm =', res_lcv$gcp.pm, '\n')
cat('res_lcv$pval.gcpzero.2tailed =', res_lcv$pval.gcpzero.2tailed, ' (this one IS correct in SKILL.md)\n')
