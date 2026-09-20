# Independent ground truth for percent identity: pwalign::pid (Bioconductor; Raghava & Barton 2006 PID1..PID4).
# Run: bash F:/OpenScience/audit-envs/alignment/r.sh s03_pid_ref.R   (from the run/ dir)
suppressMessages({library(Biostrings); library(pwalign)})
s <- readAAStringSet("data/globins_uniprot.fasta")
names(s) <- sub("^sp\\|[A-Z0-9]+\\|", "", sub(" .*", "", names(s)))
cat("sequences:", paste(names(s), collapse=","), "\n")
hba <- s[["HBA_HUMAN"]]; hbb <- s[["HBB_HUMAN"]]; myg <- s[["MYG_PHYMC"]]
frag <- subseq(hbb, 30, 120)        # 91-residue fragment of HBB (domain-vs-full pathology)
jobs <- list(
  list("HBA_vs_HBB_global",    hba, hbb,  "global"),
  list("MYG_vs_HBB_global",    myg, hbb,  "global"),
  list("HBAfull_vs_HBBfrag_overlap", hba, frag, "overlap"),   # free end gaps -> terminal gaps
  list("HBBfrag_vs_HBAfull_local",   frag, hba, "local")      # local
)
rows <- list()
for (j in jobs) {
  a <- pairwiseAlignment(j[[2]], j[[3]], substitutionMatrix = "BLOSUM62", gapOpening = 10, gapExtension = 0.5, type = j[[4]])
  pa <- as.character(alignedPattern(a)); su <- as.character(alignedSubject(a))
  p <- sapply(c("PID1","PID2","PID3","PID4"), function(t) pwalign::pid(a, type = t))
  cat(sprintf("%-28s alnlen=%d  PID1=%.3f PID2=%.3f PID3=%.3f PID4=%.3f\n", j[[1]], nchar(pa), p[1], p[2], p[3], p[4]))
  rows[[length(rows)+1]] <- data.frame(name=j[[1]], a=pa, b=su, PID1=p[1], PID2=p[2], PID3=p[3], PID4=p[4],
    pfull=as.character(j[[2]]), sfull=as.character(j[[3]]), ps=start(pattern(a)), pe=end(pattern(a)), ss=start(subject(a)), se=end(subject(a)))
}
df <- do.call(rbind, rows)
write.table(df, "data/pid_pairs_R.tsv", sep = "\t", quote = FALSE, row.names = FALSE)
stopifnot(nrow(df) == 4, all(is.finite(as.matrix(df[, c("PID1","PID2","PID3","PID4")]))))
cat("wrote data/pid_pairs_R.tsv with", nrow(df), "pairs\n")
