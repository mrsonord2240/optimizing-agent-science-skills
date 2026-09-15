# Input 8 (NEW) R half: ape raw/K80 on the same gapped alignment (pairwise.deletion default FALSE vs TRUE).
library(ape); library(phangorn)
aln <- read.dna('barcode20_gapped.fa', format = 'fasta'); rownames(aln) <- trimws(rownames(aln))
true <- read.tree('../../data/barcode20_true.nwk'); rf <- function(t) RF.dist(unroot(t), unroot(true), normalize = FALSE)
p0 <- as.matrix(dist.dna(aln, 'raw')); p1 <- as.matrix(dist.dna(aln, 'raw', pairwise.deletion = TRUE))
n <- rownames(p0)
cat('ape raw', n[1], n[3], 'complete-deletion', round(p0[1, 3], 4), '| pairwise-deletion', round(p1[1, 3], 4), '\n')
cat('RF K80 NJ complete', rf(nj(dist.dna(aln, 'K80'))), '| pairwise', rf(nj(dist.dna(aln, 'K80', pairwise.deletion = TRUE))), '\n')
