suppressPackageStartupMessages({ library(MendelianRandomization) })
set.seed(1)
n <- 3
bx <- rnorm(n, 0.3, 0.05); bxse <- rep(0.05, n)
by <- rnorm(n, 0.15, 0.05); byse <- rep(0.05, n)
ld <- diag(n); ld[1,2] <- ld[2,1] <- 0.3
mr_obj <- mr_input(bx=bx, bxse=bxse, by=by, byse=byse, correlation=ld)
cat("class:", class(mr_obj), "\n")
print(showMethods("mr_ivw"))
res <- mr_ivw(mr_obj, model="default", correl=TRUE)
print(res)
