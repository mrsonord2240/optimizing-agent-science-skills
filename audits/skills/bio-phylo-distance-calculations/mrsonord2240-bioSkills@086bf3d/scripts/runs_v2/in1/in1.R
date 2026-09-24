# Input 1 (Canonical), R half: K80 NJ + bootstrap with the fixed Skill's "define the method once" pattern, plus the
# write.csv hand-off the Skill's Python block expects. SYNTHETIC barcode20.fa (AliSim, known tree).
library(ape); library(phangorn)
aln <- read.dna('../../data/barcode20.fa', format = 'fasta'); rownames(aln) <- trimws(rownames(aln))
true <- read.tree('../../data/barcode20_true.nwk')
rf <- function(a) RF.dist(unroot(a), unroot(true), normalize = FALSE)
method <- function(x) nj(dist.dna(x, model = 'K80'))          # Skill pattern (K80 + NJ here, as the user asked)
tree <- method(aln)
set.seed(42)
boot <- boot.phylo(tree, aln, method, B = 500, quiet = TRUE)
tree$node.label <- round(100 * boot / 500)
write.csv(as.matrix(dist.dna(aln, model = 'K80')), 'k80.csv')  # Skill's R -> Python hand-off line
cat('RF K2P-NJ vs true:', rf(tree), '(max', 2 * (Ntip(true) - 3), ') | K2P-FastME', rf(fastme.bal(dist.dna(aln, 'K80'))), '\n')
ok <- prop.clades(unroot(tree), unroot(true), rooted = FALSE)
cat('bootstrap %:', tree$node.label, '\n'); cat('support on wrong splits:', tree$node.label[ok == 0 | is.na(ok)], '\n')
set.seed(42); b2 <- boot.phylo(tree, aln, method, B = 500, quiet = TRUE); cat('seeded rerun identical:', identical(boot, b2), '\n')
