# Input 6 (Scope Boundary): protein LG distance tree. Data: SYNTHETIC prot15.fa (AliSim LG+G4 alpha=0.8).
library(ape); library(phangorn)
dat  <- read.phyDat('../../data/prot15.fa', format = 'fasta', type = 'AA')
names(dat) <- trimws(names(dat))         # AliSim pads FASTA names
true <- read.tree('../../data/prot15_true.nwk')
rf <- function(t) RF.dist(unroot(t), unroot(true), normalize = FALSE)
d <- dist.ml(dat, model = 'LG')                    # Skill line
dg <- dist.ml(dat, model = 'LG', k = 4, shape = 0.8)
cat('LG distance range', format(range(d), digits = 3), '| LG+G(0.8) range', format(range(dg), digits = 3), '\n')
set.seed(20260915)
t_lg <- fastme.bal(d); t_lgg <- fastme.bal(dg)
cat('RF (max', 2 * (Ntip(true) - 3), '): LG NJ', rf(NJ(d)), '| LG FastME', rf(t_lg), '| LG+G FastME', rf(t_lgg),
    '| JC69(AA) NJ', rf(NJ(dist.ml(dat, model = 'JC69'))), '| p-dist NJ', rf(NJ(dist.hamming(dat))), '\n')
bs <- bootstrap.phyDat(dat, function(x) fastme.bal(dist.ml(x, model = 'LG')), bs = 200)
t_lg <- plotBS(t_lg, bs, type = 'none')
cat('LG FastME bootstrap:', t_lg$node.label, '\n')
write.tree(t_lg, 'lg_fastme_bs.nwk')
