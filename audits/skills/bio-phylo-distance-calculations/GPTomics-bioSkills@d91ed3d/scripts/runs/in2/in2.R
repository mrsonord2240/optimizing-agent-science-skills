# Input 2 (Variant A). Data: SYNTHETIC deep12.fa (AliSim GTR+G4 alpha=0.4, known tree).
library(ape); library(phangorn)
set.seed(20260915)
aln  <- read.dna('../../data/deep12.fa', format = 'fasta')
rownames(aln) <- trimws(rownames(aln))   # AliSim pads FASTA names; read.dna keeps the padding
true <- read.tree('../../data/deep12_true.nwk')
rf <- function(a) RF.dist(unroot(a), unroot(true), normalize = FALSE)

# ---- Skill code, verbatim ----
d <- dist.dna(aln, model = 'TN93', gamma = 0.5)   # model-corrected; gamma applies ASRV (alpha < 1 = strong)
tree <- fastme.bal(d, nni = TRUE, spr = TRUE)     # balanced minimum evolution: the modern best distance tree
t0 <- Sys.time()
boot <- boot.phylo(tree, aln, function(x) fastme.bal(dist.dna(x, model = 'TN93')), B = 500, quiet = TRUE)
cat('Skill bootstrap (B=500) time:', format(Sys.time() - t0), '\n')
# ---- auditor comparison: same bootstrap with the SAME gamma correction as the point estimate ----
boot_g <- boot.phylo(tree, aln, function(x) fastme.bal(dist.dna(x, model = 'TN93', gamma = 0.5)), B = 500, quiet = TRUE)

res <- data.frame(
  method = c('raw NJ', 'JC69 NJ', 'K80 NJ', 'TN93 NJ', 'TN93+G0.5 NJ', 'TN93+G0.5 BIONJ', 'TN93+G0.5 FastME (Skill)',
             'TN93 FastME', 'raw UPGMA'),
  RF = c(rf(nj(dist.dna(aln, 'raw'))), rf(nj(dist.dna(aln, 'JC69'))), rf(nj(dist.dna(aln, 'K80'))),
         rf(nj(dist.dna(aln, 'TN93'))), rf(nj(d)), rf(bionj(d)), rf(tree),
         rf(fastme.bal(dist.dna(aln, 'TN93'))), rf(upgma(dist.dna(aln, 'raw')))))
cat('max RF =', 2 * (Ntip(true) - 3), '\n'); print(res)
ok <- prop.clades(unroot(tree), unroot(true), rooted = FALSE)
cat('FastME node in true tree:', ok, '\n')
cat('bootstrap as written (no gamma):', round(100 * boot / 500), '\n')
cat('bootstrap with gamma = 0.5     :', round(100 * boot_g / 500), '\n')

# where would alpha come from? quick ML estimate on the FastME topology (phangorn)
dat <- phyDat(aln)
fit <- optim.pml(pml(tree, dat, k = 4), model = 'GTR', optGamma = TRUE, optEdge = TRUE, rearrangement = 'none',
                 control = pml.control(trace = 0))
cat('ML-estimated gamma shape on FastME tree:', round(fit$shape, 3), ' (simulated alpha = 0.4)\n')
d_est <- dist.dna(aln, model = 'TN93', gamma = fit$shape)
cat('RF FastME with estimated alpha:', rf(fastme.bal(d_est)), '\n')
cat('tree length TN93+G0.5 FastME:', round(sum(tree$edge.length), 3), '  true:', sum(true$edge.length), '\n')
cat('tree length TN93 (no gamma) FastME:', round(sum(fastme.bal(dist.dna(aln, 'TN93'))$edge.length), 3), '\n')
tree$node.label <- round(100 * boot_g / 500)
write.tree(tree, 'tn93g_fastme.nwk')
