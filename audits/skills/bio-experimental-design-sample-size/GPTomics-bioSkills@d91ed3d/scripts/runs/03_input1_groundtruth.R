# Input 1 ground truth: PLANTED-TRUTH power curve at the SKILL.md canonical parameters.
# Generative model matches ssizeRNA's own assumptions (NB, mu=10, disp=0.2, 5% DE at FC 1.5).
# Question: what is the smallest n per group that actually delivers marginal power >= 0.80
# at BH FDR 0.05?  Compare with whatever ssizeRNA prescribes.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(edgeR); library(limma)})
set.seed(20260916)

nGenes <- 20000; pi0 <- 0.95; MU <- 10; DISP <- 0.2; FC <- 1.5
nDE <- round(nGenes*(1-pi0))
de <- 1:nDE; fcv <- rep(1, nGenes); fcv[de] <- rep(c(FC, 1/FC), length.out = nDE)

one_rep <- function(n) {
  cts <- cbind(matrix(rnbinom(nGenes*n, mu = MU,        size = 1/DISP), nGenes, n),
               matrix(rnbinom(nGenes*n, mu = MU*fcv,    size = 1/DISP), nGenes, n))
  grp <- factor(rep(c("A","B"), each = n))
  keep <- rowSums(cts) > 0
  # --- edgeR QL ---
  y <- DGEList(cts[keep,], group = grp); y <- calcNormFactors(y)
  des <- model.matrix(~grp); y <- estimateDisp(y, des)
  qlf <- glmQLFTest(glmQLFit(y, des), coef = 2)
  p_e <- rep(1, nGenes); p_e[keep] <- qlf$table$PValue
  # --- limma-voom (the engine ssizeRNA itself uses) ---
  v <- voom(DGEList(cts[keep,]), des, plot = FALSE)
  fit <- eBayes(lmFit(v, des))
  p_v <- rep(1, nGenes); p_v[keep] <- fit$p.value[,2]
  sc <- function(p) { q <- p.adjust(p, "BH"); sig <- q < 0.05
    c(power = mean(sig[de]), fdr = if (sum(sig)) sum(sig & fcv==1)/sum(sig) else 0, disc = sum(sig)) }
  c(edgeR = sc(p_e), voom = sc(p_v))
}

REPS <- 8
res <- do.call(rbind, lapply(c(3,4,5,6,8,10,12), function(n) {
  m <- colMeans(do.call(rbind, replicate(REPS, one_rep(n), simplify = FALSE)))
  cat(sprintf("n=%2d  edgeR power=%.3f FDR=%.3f (%4.0f calls) | voom power=%.3f FDR=%.3f (%4.0f calls)\n",
              n, m["edgeR.power"], m["edgeR.fdr"], m["edgeR.disc"],
                 m["voom.power"],  m["voom.fdr"],  m["voom.disc"])); flush.console()
  data.frame(n = n, t(m))
}))
write.csv(res, "runs/03_input1_groundtruth.csv", row.names = FALSE)
cat("\nSmallest n reaching marginal power >= 0.80 at BH FDR 0.05:\n")
cat("  edgeR QL   :", {i <- which(res$edgeR.power >= .80)[1]; if (is.na(i)) ">12" else res$n[i]}, "\n")
cat("  limma-voom :", {i <- which(res$voom.power  >= .80)[1]; if (is.na(i)) ">12" else res$n[i]}, "\n")
cat(sprintf("(%d reps per n, %d genes, %d truly DE, NB mu=%g disp=%g fc=%g)\n", REPS, nGenes, nDE, MU, DISP, FC))
