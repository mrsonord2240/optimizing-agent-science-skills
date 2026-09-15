# Input 7 - R check of the UPGMA trap and rooting alternatives. SYNTHETIC noclock8.fa.
library(ape); library(phangorn)
aln  <- read.dna('../../data/noclock8.fa', format = 'fasta')
rownames(aln) <- trimws(rownames(aln))   # AliSim pads FASTA names; read.dna keeps the padding
true <- read.tree('../../data/noclock8_true.nwk')
rf <- function(t) RF.dist(unroot(t), unroot(true), normalize = FALSE)
for (m in c('raw', 'JC69', 'K80')) {
  d <- dist.dna(aln, model = m)
  cat(sprintf('%-5s RF (max 10): UPGMA %d | NJ %d | FastME %d\n', m, rf(upgma(d)), rf(nj(d)), rf(fastme.bal(d))))
}
d <- dist.dna(aln, 'K80')
cat('UPGMA K80:', write.tree(upgma(d)), '\n')
cat('midpoint-rooted FastME K80:', write.tree(midpoint(fastme.bal(d))), '\n')
set.seed(20260915)
u <- upgma(d); bu <- boot.phylo(u, aln, function(x) upgma(dist.dna(x, 'K80')), B = 200, quiet = TRUE)
cat('UPGMA bootstrap %:', round(100 * bu / 200), ' node in true tree:', prop.clades(u, true, rooted = FALSE), '\n')
