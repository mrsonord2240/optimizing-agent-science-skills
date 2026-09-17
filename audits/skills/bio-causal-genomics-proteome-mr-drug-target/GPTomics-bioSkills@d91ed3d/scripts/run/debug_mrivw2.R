suppressPackageStartupMessages({ library(TwoSampleMR); library(coloc); library(ieugwasr) })
suppressPackageStartupMessages({ library(MendelianRandomization) })
n <- 3
bx <- rnorm(n, 0.3, 0.05); bxse <- rep(0.05, n)
by <- rnorm(n, 0.15, 0.05); byse <- rep(0.05, n)
ld <- diag(n); ld[1,2] <- ld[2,1] <- 0.3
mr_obj <- mr_input(bx=bx, bxse=bxse, by=by, byse=byse, correlation=ld)
cat("Which mr_ivw is found first on search path:\n")
print(environmentName(environment(mr_ivw)))
res <- tryCatch(mr_ivw(mr_obj, model="default", correl=TRUE), error=function(e) paste("ERROR:", conditionMessage(e)))
print(res)
cat("\nFix: call MendelianRandomization::mr_ivw explicitly ->\n")
res2 <- MendelianRandomization::mr_ivw(mr_obj, model="default", correl=TRUE)
print(res2)
