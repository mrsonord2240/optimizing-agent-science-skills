# Input 2 (Variant A): fixed Skill R blocks VERBATIM (path only) on SYNTHETIC deep12.fa (GTR+G4 alpha 0.4).
library(ape)
aln <- read.dna('../../data/deep12.fa', format = 'fasta')
rownames(aln) <- trimws(rownames(aln))              # auditor: AliSim pads names
alpha <- 0.5                                        # gamma shape (alpha < 1 = strong ASRV); estimate it, do not assume
method <- function(x) fastme.bal(dist.dna(x, model = 'TN93', gamma = alpha), nni = TRUE, spr = TRUE)
tree <- method(aln)                                 # define the method ONCE so the bootstrap reuses it exactly
set.seed(42)
t0 <- Sys.time()
boot <- boot.phylo(tree, aln, method, B = 500)   # the SAME method (model + gamma + algorithm) that built the tree
cat('\nbootstrap time', format(Sys.time() - t0), '\n')
# ---- auditor checks ----
library(phangorn)
true <- read.tree('../../data/deep12_true.nwk'); rf <- function(a) RF.dist(unroot(a), unroot(true), normalize = FALSE)
cat('RF TN93+G0.5 FastME:', rf(tree), '(max 18) | Bio-style raw NJ:', rf(nj(dist.dna(aln, 'raw'))), '\n')
cat('bootstrap %:', round(100 * boot / 500), '\n')
cat('node in true tree:', prop.clades(unroot(tree), unroot(true), rooted = FALSE), '\n')
set.seed(42); b2 <- boot.phylo(tree, aln, method, B = 500, quiet = TRUE); cat('seeded rerun identical:', identical(boot, b2), '\n')
