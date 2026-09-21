# Input 6: the Skill's "Variant + Outlier Integration" block on SYNTHETIC SpliceAI-style hits + real FRASER output from the synthetic cohort.
suppressPackageStartupMessages({library(FRASER); library(dplyr)})
a <- commandArgs(TRUE); wd <- a[1]; out <- a[2]
fds <- loadFraserDataSet(dir = wd, name = "fitted_q10")
res <- results(fds, psiType = "jaccard", padjCutoff = 0.05, deltaPsiCutoff = 0.1)
write.table(as.data.frame(res), file.path(out, "fraser_results.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
cat("fraser_results.tsv columns:", paste(colnames(as.data.frame(res)), collapse = ","), "\n")
print(as.data.frame(res)[as.data.frame(res)$sampleID == "PATIENT_001", c("seqnames","start","end","sampleID","padjust","deltaPsi")])
# SYNTHETIC SpliceAI-derived table: NOTE the Skill never says how to produce `delta_max` from SpliceAI's VCF INFO (DS_AG|DS_AL|DS_DG|DS_DL); we take max() ourselves.
variants <- data.frame(chrom = c("chr21","chr21","chr21"), pos = c(90190, 130000, 250233), delta_max = c(0.85, 0.90, 0.4), stringsAsFactors = FALSE)
write.table(variants, file.path(out, "spliceai_hits.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
# ---- verbatim from SKILL.md ----
variants <- read.table(file.path(out, "spliceai_hits.tsv"), header=TRUE, sep='\t')
fraser_hits <- read.table(file.path(out, "fraser_results.tsv"), header=TRUE, sep='\t')
confirmed <- variants %>%
    filter(delta_max >= 0.2) %>%
    inner_join(
        fraser_hits %>% filter(sampleID == 'PATIENT_001', padjust < 0.05),
        by = c('chrom' = 'seqnames'),
        relationship = 'many-to-many'
    ) %>%
    filter(abs(pos - start) < 1000 | abs(pos - end) < 1000)
# ---------------------------------
print(confirmed[, c("chrom","pos","delta_max","start","end","padjust","deltaPsi")])
cat("confirmed rows:", nrow(confirmed), " distinct variants:", length(unique(confirmed$pos)), " (expected: only pos 90190 near the S05 skipping junction 90194-92840; 130000 is a decoy)\n")
# Chromosome-naming mismatch (Skill's Common Errors row): VCF-style '21' vs FRASER 'chr21'
v2 <- variants; v2$chrom <- sub("^chr", "", v2$chrom)
c2 <- v2 %>% filter(delta_max >= 0.2) %>% inner_join(fraser_hits %>% filter(sampleID == 'PATIENT_001', padjust < 0.05), by = c('chrom' = 'seqnames'), relationship = 'many-to-many')
cat("with '21' vs 'chr21': join returns", nrow(c2), "rows (silent empty, no warning)\n")
# Long-junction blind spot: variant deep inside the 2.6 kb skipped region (midpoint) is NOT within 1 kb of an end
v3 <- data.frame(chrom = "chr21", pos = 91500, delta_max = 0.9)
c3 <- v3 %>% inner_join(fraser_hits %>% filter(sampleID == 'PATIENT_001', padjust < 0.05), by = c('chrom' = 'seqnames'), relationship = 'many-to-many') %>% filter(abs(pos - start) < 1000 | abs(pos - end) < 1000)
cat("variant at 91500 (inside the 90194-92840 junction span, 1.3 kb from both ends): matches", nrow(c3), "\n")
