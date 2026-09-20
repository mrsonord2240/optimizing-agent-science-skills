# Reads the files the SKILL's Bambu block wrote (writeBambuOutput -> bambu_output/) and compares transcript counts with the planted truth (ctrl1..3 = sample1..3)
setwd("F:/OpenScience/audits/bio-long-read-splicing/run/out/bambu")
cat("files in bambu_output:", paste(list.files("bambu_output"), collapse = ", "), "\n")
ct <- read.table("bambu_output/counts_transcript.txt", header = TRUE, sep = "\t", check.names = FALSE)
cat("counts_transcript columns:", paste(colnames(ct), collapse = ", "), " rows:", nrow(ct), "\n")
tr <- read.table("F:/OpenScience/audits/bio-long-read-splicing/run/data/plant/hifi/truth_counts.tsv", header = TRUE, sep = "\t")
ids <- ct[[1]]
for (k in 1:3) {
  s <- c("ctrl1", "ctrl2", "ctrl3")[k]
  tt <- tr[tr$sample == s, ]; truth <- setNames(tt$n_reads, tt$transcript)
  col <- ct[[2 + k]]  # 1=TXNAME 2=GENEID then samples
  got <- setNames(col, ids)
  common <- intersect(names(truth), names(got))
  cat(sprintf("%s: %d of %d truth tx present in Bambu output; Pearson r = %.4f; Bambu total %.0f vs truth total %d (truth includes 2 novel tx not in annotation)\n",
      s, length(common), length(truth), cor(truth[common], got[common]), sum(col), sum(truth)))
}
novel <- ids[grepl("^Bambu", ids)]
cat("novel (BambuTx) transcripts reported:", length(novel), "\n")
g <- read.table("bambu_output/extended_annotations.gtf", sep = "\t", quote = "", comment.char = "")
cat("extended_annotations.gtf rows:", nrow(g), " ; novel transcript rows:", sum(g[[3]] == "transcript" & grepl("BambuTx", g[[9]])), "\n")
