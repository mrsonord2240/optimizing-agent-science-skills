# Input 4 (Variant B): scRNA-seq donors-vs-cells. Tests the SKILL.md claim that population
# DE power is set by the number of DONORS, not cells, and that cell-level tests inflate FDR.
# powsimR (the tool the SKILL.md names for this route) is NOT installed -- see 10_powsimR_check.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(edgeR); library(limma)})
set.seed(20260916)

G <- 4000; PI0 <- 0.95; FC <- 1.5
DONOR_SD <- 0.35            # donor-to-donor biological sd on the log scale
CELL_DISP <- 0.5            # within-donor cell-level NB dispersion
nDE <- round(G*(1-PI0)); de <- 1:nDE
fcv <- rep(1, G); fcv[de] <- rep(c(FC, 1/FC), length.out = nDE)
gmu <- 2 * exp(rnorm(G, 0, 0.8))   # per-cell expected counts

sim_study <- function(nDonor, nCell) {
  pb <- matrix(0, G, 2*nDonor); cellmat <- list(); lab <- c()
  for (g in 1:2) for (d in 1:nDonor) {
    dm <- gmu * (if (g == 2) fcv else 1) * exp(rnorm(G, 0, DONOR_SD))
    cells <- matrix(rnbinom(G*nCell, mu = dm, size = 1/CELL_DISP), G, nCell)
    pb[, (g-1)*nDonor + d] <- rowSums(cells)
    cellmat[[length(cellmat)+1]] <- cells; lab <- c(lab, rep(g, nCell))
  }
  grp <- factor(rep(c("A","B"), each = nDonor))
  des <- model.matrix(~grp)
  keep <- rowSums(pb) > 0
  v <- voom(calcNormFactors(DGEList(pb[keep,])), des, plot = FALSE)
  p <- rep(1, G); p[keep] <- eBayes(lmFit(v, des))$p.value[,2]
  q <- p.adjust(p, "BH"); sig <- q < 0.05
  pbres <- c(power = mean(sig[de]), fdr = if (sum(sig)) sum(sig & fcv==1)/sum(sig) else 0)
  # --- cell-level test: cells treated as independent replicates (the named failure mode) ---
  cl <- do.call(cbind, cellmat); cpm_l <- log2(t(t(cl)/pmax(colSums(cl),1))*1e4 + 1)
  tt <- rowttests(cpm_l, factor(lab))
  qc <- p.adjust(tt$p.value, "BH"); sc <- qc < 0.05
  cellres <- c(power = mean(sc[de]), fdr = if (sum(sc)) sum(sc & fcv==1)/sum(sc) else 0)
  c(pseudobulk = pbres, cellwise = cellres)
}
library(genefilter)
grid <- expand.grid(nDonor = c(3,6,10), nCell = c(50,200,800))
out <- do.call(rbind, lapply(seq_len(nrow(grid)), function(i) {
  r <- colMeans(do.call(rbind, replicate(4, sim_study(grid$nDonor[i], grid$nCell[i]), simplify = FALSE)))
  cat(sprintf("donors=%2d cells/donor=%4d | pseudobulk power=%.3f FDR=%.3f | cell-level power=%.3f FDR=%.3f\n",
              grid$nDonor[i], grid$nCell[i], r["pseudobulk.power"], r["pseudobulk.fdr"],
              r["cellwise.power"], r["cellwise.fdr"])); flush.console()
  data.frame(grid[i,], t(r))
}))
write.csv(out, "runs/06_input4_scrna.csv", row.names = FALSE)
