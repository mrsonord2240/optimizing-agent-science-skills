suppressPackageStartupMessages({ library(coloc); library(MendelianRandomization); library(TwoSampleMR) })
n <- 3
bx <- rnorm(n, 0.3, 0.05); bxse <- rep(0.05, n)
by <- rnorm(n, 0.15, 0.05); byse <- rep(0.05, n)
ld <- diag(n); ld[1,2] <- ld[2,1] <- 0.3
mr_obj <- mr_input(bx=bx, bxse=bxse, by=by, byse=byse, correlation=ld)
cat("mr_ivw resolves from package:", environmentName(environment(mr_ivw)), "\n")
res <- tryCatch(mr_ivw(mr_obj, model="default", correl=TRUE), error=function(e) paste("ERROR:", conditionMessage(e)))
print(res)
