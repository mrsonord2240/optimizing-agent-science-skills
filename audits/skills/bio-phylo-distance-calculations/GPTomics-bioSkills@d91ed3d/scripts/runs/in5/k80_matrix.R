# Input 5 (Stress) - R half: K80 matrix for Python + FastME reference. Data: SYNTHETIC big150.fa.
library(ape); library(phangorn)
aln <- read.dna('../../data/big150.fa', format = 'fasta')
rownames(aln) <- trimws(rownames(aln))   # AliSim pads FASTA names; read.dna keeps the padding
true <- read.tree('../../data/big150_true.nwk')
t0 <- Sys.time(); d <- dist.dna(aln, model = 'K80'); t_d <- Sys.time() - t0
write.csv(as.matrix(d), 'k80_big150.csv')
t0 <- Sys.time(); ft <- fastme.bal(d, nni = TRUE, spr = TRUE); t_f <- Sys.time() - t0
t0 <- Sys.time(); nt <- nj(d); t_n <- Sys.time() - t0
rf <- function(t) RF.dist(unroot(t), unroot(true), normalize = FALSE)
cat('dist.dna K80 time', format(t_d), '| FastME time', format(t_f), '| NJ time', format(t_n), '\n')
cat('RF (max', 2 * (Ntip(true) - 3), '): K80 FastME', rf(ft), ' K80 NJ', rf(nt), ' K80 BIONJ', rf(bionj(d)),
    ' raw NJ', rf(nj(dist.dna(aln, 'raw'))), '\n')
cat('negative NJ branch lengths:', sum(nt$edge.length < 0), '\n')
