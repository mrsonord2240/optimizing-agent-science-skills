# SKILL Bambu block (verbatim text, only bam_files/ncore edited) on REAL ONT direct RNA (SG-NEx A549, bambu extdata), Windows R via r-bambu.sh
wd <- "F:/OpenScience/audits/bio-long-read-splicing/run/out/bambu_real"; dir.create(wd, showWarnings = FALSE, recursive = TRUE); setwd(wd)
P <- "F:/OpenScience/audit-envs/alternative-splicing/public-data/longread/bambu_extdata/"
file.copy(paste0(P, c("SGNex_A549_directRNA_replicate5_run1_chr9_1_1000000.bam", "SGNex_A549_directRNA_replicate5_run1_chr9_1_1000000.bam.bai",
  "Homo_sapiens.GRCh38.dna_sm.primary_assembly_chr9_1_1000000.fa", "Homo_sapiens.GRCh38.91_chr9_1_1000000.gtf")), wd, overwrite = TRUE)
file.rename("SGNex_A549_directRNA_replicate5_run1_chr9_1_1000000.bam", "sample1.bam"); file.rename("SGNex_A549_directRNA_replicate5_run1_chr9_1_1000000.bam.bai", "sample1.bam.bai")
file.rename("Homo_sapiens.GRCh38.dna_sm.primary_assembly_chr9_1_1000000.fa", "reference.fa"); file.rename("Homo_sapiens.GRCh38.91_chr9_1_1000000.gtf", "gencode.v45.annotation.gtf")
blk <- readLines("F:/OpenScience/audits/bio-long-read-splicing/run/out/blocks/bambu-for-annotation-aware-discovery-qua_1.R")
blk <- sub("c('sample1.bam', 'sample2.bam', 'sample3.bam')", "c('sample1.bam')", blk, fixed = TRUE); blk <- sub("ncore = 8", "ncore = 1", blk, fixed = TRUE)
writeLines(blk, "bambu_block_real.R"); cat(blk, sep = "\n")
source("bambu_block_real.R")
cat("\n== content checks\n")
ct <- read.table("bambu_output/counts_transcript.txt", header = TRUE, sep = "\t")
cat("transcripts:", nrow(ct), " total count:", sum(ct[[3]]), " transcripts with count>0:", sum(ct[[3]] > 0), " novel (Bambu*):", sum(grepl("^Bambu", ct$TXNAME)), "\n")
print(head(ct[order(-ct[[3]]), ], 4))
