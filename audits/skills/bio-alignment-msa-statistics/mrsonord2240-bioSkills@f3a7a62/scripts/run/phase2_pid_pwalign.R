# INPUT 3 ground truth: pwalign::pid (Bioconductor) PID1-PID4 on the auditor's OWN pairs.
# Pairs: (1) all 28 pairs of the 8 UniProt globins x {global, local, overlap} with BLOSUM62 10/0.5,
#        (2) 40 random pairs of Pfam-seed sequences (fixed seed) x {global, local, overlap, global-local, local-global}
#            with BLOSUM45 open 12 / ext 1 (different scoring => gaps in different places), first sequence randomly TRUNCATED
#            to a fragment so terminal overhangs are frequent,
#        (3) DNA: all 15 pairs of 6 HBB CDS x {global, overlap, local}, match 1 / mismatch -3, gap 5/2.
# Output data/derived/pid_pairs_R.tsv: name, aligned strings, full strings, aligned ranges, PID1-4.
# Run: bash F:/OpenScience/audit-envs/alignment/r.sh b03_pid_pwalign.R   (from run/)
suppressMessages({library(Biostrings); library(pwalign)})
set.seed(20260920)
rows <- list()
add <- function(name, p, s, a) {
  pa <- as.character(alignedPattern(a)); su <- as.character(alignedSubject(a))
  v <- sapply(c("PID1","PID2","PID3","PID4"), function(t) pwalign::pid(a, type = t))
  rows[[length(rows)+1]] <<- data.frame(name=name, a=pa, b=su, PID1=v[1], PID2=v[2], PID3=v[3], PID4=v[4],
     pfull=as.character(p), sfull=as.character(s), ps=start(pattern(a)), pe=end(pattern(a)),
     ss=start(subject(a)), se=end(subject(a)), stringsAsFactors=FALSE)
}
g <- readAAStringSet("data/globins_uniprot.fasta"); names(g) <- sub("^sp[|][A-Z0-9]+[|]", "",sub(" .*", "", names(g)))
for (i in 1:7) for (j in (i+1):8) for (ty in c("global","local","overlap")) {
  a <- pairwiseAlignment(g[[i]], g[[j]], substitutionMatrix="BLOSUM62", gapOpening=10, gapExtension=0.5, type=ty)
  add(paste("globin", names(g)[i], names(g)[j], ty, sep="|"), g[[i]], g[[j]], a)
}
sd <- readAAStringSet("data/seed_ungapped.fa")
ty5 <- c("global","local","overlap","global-local","local-global")
for (k in 1:40) {
  ij <- sample(length(sd), 2); p <- sd[[ij[1]]]; s <- sd[[ij[2]]]
  L <- length(p); st <- sample(1:max(1, L %/% 3), 1); en <- sample((L - L %/% 3):L, 1); p <- subseq(p, st, en)
  ty <- ty5[(k - 1) %% 5 + 1]
  a <- pairwiseAlignment(p, s, substitutionMatrix="BLOSUM45", gapOpening=12, gapExtension=1, type=ty)
  add(paste("seed", names(sd)[ij[1]], names(sd)[ij[2]], ty, sep="|"), p, s, a)
}
d <- readDNAStringSet("data/hbb6.fa")
sm <- nucleotideSubstitutionMatrix(match=1, mismatch=-3)
for (i in 1:5) for (j in (i+1):6) for (ty in c("global","overlap","local")) {
  a <- pairwiseAlignment(d[[i]], d[[j]], substitutionMatrix=sm, gapOpening=5, gapExtension=2, type=ty)
  add(paste("hbbcds", names(d)[i], names(d)[j], ty, sep="|"), d[[i]], d[[j]], a)
}
df <- do.call(rbind, rows)
write.table(df, "data/derived/pid_pairs_R.tsv", sep="\t", quote=FALSE, row.names=FALSE)
stopifnot(nrow(df) == 84 + 40 + 45, all(is.finite(as.matrix(df[, c("PID1","PID2","PID3","PID4")]))))
cat("wrote", nrow(df), "pairs; alignment lengths", range(nchar(df$a)), "\n")
cat("pairs with a terminal gap in either aligned string:", sum(grepl("^-|-$", df$a) | grepl("^-|-$", df$b)), "\n")
cat("pairs with an unaligned flank (ps>1, ss>1, pe<len, se<len):", sum(df$ps > 1 | df$ss > 1 | df$pe < nchar(df$pfull) | df$se < nchar(df$sfull)), "\n")
cat("versions:", as.character(packageVersion("pwalign")), as.character(packageVersion("Biostrings")), "\n")
