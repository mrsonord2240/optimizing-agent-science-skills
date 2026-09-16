# Input 3 (Edge): budget-fixed n, and a target that cannot be reached within maxN.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
pdf(NULL)
suppressPackageStartupMessages({library(ssizeRNA); library(edgeR); library(limma)})

cat("=== A. SKILL.md decision-tree row 'Budget already fixed at some n' -> check.power ===\n")
set.seed(20260916)
cp <- check.power(nGenes = 20000, pi0 = 0.95, m = 6, mu = 10, disp = 0.2, fc = 1.5, fdr = 0.05, sims = 50)
for (nm in names(cp)) cat(sprintf("   %-14s %s\n", nm, paste(signif(unlist(cp[[nm]]), 4), collapse = " ")))

cat("\n=== B. Independent replication of check.power's claim (edgeR QL + BH, 20 sims) ===\n")
nGenes <- 20000; pi0 <- 0.95; MU <- 10; DISP <- 0.2; FC <- 1.5
nDE <- round(nGenes*(1-pi0)); de <- 1:nDE
fcv <- rep(1, nGenes); fcv[de] <- rep(c(FC, 1/FC), length.out = nDE)
sim1 <- function(n) {
  cts <- cbind(matrix(rnbinom(nGenes*n, mu = MU,     size = 1/DISP), nGenes, n),
               matrix(rnbinom(nGenes*n, mu = MU*fcv, size = 1/DISP), nGenes, n))
  grp <- factor(rep(c("A","B"), each = n)); keep <- rowSums(cts) > 0
  des <- model.matrix(~grp)
  y <- estimateDisp(calcNormFactors(DGEList(cts[keep,], group = grp)), des)
  p <- rep(1, nGenes); p[keep] <- glmQLFTest(glmQLFit(y, des), coef = 2)$table$PValue
  q <- p.adjust(p, "BH"); sig <- q < 0.05
  c(power = mean(sig[de]), fdr = if (sum(sig)) sum(sig & fcv == 1)/sum(sig) else 0)
}
set.seed(4242)
m <- colMeans(do.call(rbind, replicate(20, sim1(6), simplify = FALSE)))
cat(sprintf("   independent sim at n=6: marginal power = %.3f, realized FDR = %.3f\n", m["power"], m["fdr"]))

cat("\n=== C. Unreachable target: disp=0.8, fc=1.2, power=0.80, maxN=30 ===\n")
for (fn in c("ssizeRNA_vary","ssizeRNA_single")) {
  set.seed(11)
  r <- tryCatch(do.call(fn, list(nGenes=20000, pi0=0.95, m=200, mu=100, disp=0.8,
                                 fc=1.2, fdr=0.05, power=0.80, maxN=30)),
                error=function(e) paste("ERROR:", conditionMessage(e)))
  if (is.list(r)) cat(sprintf("   %-16s -> ssize = %s ; power at maxN = %s\n", fn, r$ssize,
                              paste(signif(tail(r$power, 1), 3), collapse=" ")))
  else cat(sprintf("   %-16s -> %s\n", fn, r))
}
