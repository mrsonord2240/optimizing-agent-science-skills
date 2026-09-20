# Independent check of MARVEL ComputePSI(SE) on the REAL demo: recompute PSI from junction counts by hand.
suppressMessages(library(MARVEL))
m <- readRDS(system.file('extdata/data/marvel.demo.rds', package='MARVEL'))
sj <- m$SpliceJunction; rownames(sj) <- sj$coord.intron
se <- m$SpliceFeatureValidated$SE
cat('validated SE events:', nrow(se), ' cols:', paste(colnames(se), collapse=','), '\n')
m2 <- CreateMarvelObject(SpliceJunction=m$SpliceJunction, SplicePheno=m$SplicePheno, SpliceFeature=m$SpliceFeature, IntronCounts=m$IntronCounts, GeneFeature=m$GeneFeature, Exp=m$Exp)
m2 <- ComputePSI(m2, CoverageThreshold=10, UnevenCoverageMultiplier=10, EventType='SE')
psi <- m2$PSI$SE; rownames(psi) <- psi$tran_id
cells <- colnames(psi)[-(1:ncol(psi[,sapply(psi, function(x) !is.numeric(x)),drop=FALSE]))]
cells <- setdiff(colnames(sj), 'coord.intron')
nfound <- 0; maxdiff <- 0; nmatch <- 0; nnaMismatch <- 0
for (tid in rownames(psi)) {
  p <- strsplit(strsplit(tid, '@')[[1]], ':'); e <- lapply(p, function(x) as.integer(x[2:3])); chr <- p[[1]][1]
  j_inc1 <- paste(chr, e[[1]][2]+1, e[[2]][1]-1, sep=':'); j_inc2 <- paste(chr, e[[2]][2]+1, e[[3]][1]-1, sep=':'); j_skip <- paste(chr, e[[1]][2]+1, e[[3]][1]-1, sep=':')
  if (!all(c(j_inc1,j_inc2,j_skip) %in% rownames(sj))) next
  nfound <- nfound+1
  a <- unlist(sj[j_inc1, cells]); b <- unlist(sj[j_inc2, cells]); s <- unlist(sj[j_skip, cells])
  for (cell in cells) {
    mp <- psi[tid, cell]
    hand <- (a[cell]+b[cell])/2 / ((a[cell]+b[cell])/2 + s[cell])
    if (!is.na(mp) && !is.na(hand)) { nmatch <- nmatch+1; maxdiff <- max(maxdiff, abs(mp-hand)) }
    if (is.na(mp) != is.na(hand)) nnaMismatch <- nnaMismatch+1
  }
}
cat('events with all 3 junctions locatable by e1+1:s2-1 convention:', nfound, 'of', nrow(psi), '\n')
cat('cell x event PSI compared:', nmatch, ' max |MARVEL - hand| (PSI scale 0-1):', maxdiff, ' NA-pattern mismatches:', nnaMismatch, '\n')
cat('MARVEL PSI scale: range', range(unlist(psi[,cells]), na.rm=TRUE), '\n')
