# Fresh final-pass fixture builder. Inputs are existing public-derived, real moving-pictures ASVs
# and a real region-matched SILVA slice; outputs are created only under this audit's dated folder.
.libPaths(c("F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/R-lib", .libPaths()))
out <- "F:/OpenScience/audits/bio-microbiome-taxonomy-assignment/data/2026-09-23-final-pass"
dir.create(out, recursive = TRUE, showWarnings = FALSE)
asv_fasta <- "F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/reaudit-tax/rep-seqs.fasta"
ref_tsv <- "F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/reaudit-tax/regionmatched_decipher_tax.tsv"

lines <- readLines(asv_fasta)
ids <- character(); seqs <- character(); current_id <- NULL; current <- character()
for (line in lines) {
  if (startsWith(line, ">")) {
    if (!is.null(current_id)) { ids <- c(ids, current_id); seqs <- c(seqs, paste0(current, collapse = "")) }
    current_id <- substring(line, 2); current <- character()
  } else current <- c(current, line)
}
ids <- c(ids, current_id); seqs <- c(seqs, paste0(current, collapse = ""))
seqtab <- matrix(1L, nrow = 1, ncol = length(seqs), dimnames = list("fresh_final_pass_sample", seqs))
saveRDS(seqtab, file.path(out, "moving_pictures_770_seqtab.rds"))
writeLines(c(rbind(paste0(">", ids), seqs)), file.path(out, "moving_pictures_770_asvs.fasta"))

tab <- read.delim(ref_tsv, header = FALSE, sep = "\t", quote = "", stringsAsFactors = FALSE, nrows = 3000)
stopifnot(ncol(tab) >= 3, nrow(tab) == 3000)
writeLines(c(rbind(paste0(">", tab[[1]]), tab[[3]])), file.path(out, "small_region_reference.fasta"))
writeLines(tab[[2]], file.path(out, "small_region_reference_taxonomy.txt"))
cat(sprintf("ASVs=%d; small real SILVA region reference=%d; unique taxonomy strings=%d\n", length(seqs), nrow(tab), length(unique(tab[[2]]))))
