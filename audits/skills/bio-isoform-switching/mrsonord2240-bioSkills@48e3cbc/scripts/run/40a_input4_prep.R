# INPUT 4 prep: SKILL workflow block (r_01) + consequence block PART 1 (r_02: ORFs, alternative splicing, extractSequence) verbatim,
# on (S) SYNTHETIC 3 v 3 with shuffled IDs (no CDS in the GTF -> analyzeORF branch) and (R) real chrX (CDS in GTF -> annotated ORFs).
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R"); source("../helpers2.R")
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR)); set.seed(404)
shuf <- function(k) sprintf("SRR70%05d", sample(10000:99999, k))
ids3 <- c(sprintf("ctrl_%d", 1:3), sprintf("trt_%d", 1:3)); o <- sample(6); ids3 <- ids3[o]; cond3 <- rep(c("control", "treatment"), each = 3)[o]
stage_salmon("w4s", ids3, shuf(6), cond3); setwd("w4s")
run_block("r_01.R"); cat("S: ORF origins before block 2:", paste(names(table(aSwitchList$orfAnalysis$orf_origin, useNA = "ifany")), table(aSwitchList$orfAnalysis$orf_origin, useNA = "ifany")), "\n")
run_block_part("r_03.R", 1)
cat("S: ORF origins after part 1:", paste(names(table(aSwitchList$orfAnalysis$orf_origin)), table(aSwitchList$orfAnalysis$orf_origin)), "\n")
cat("S: sequences:", paste(list.files("sequences"), collapse = ", "), "\n")
chk("S: extractSequence wrote nt and AA FASTA", all(c("isoformSwitchAnalyzeR_isoform_nt.fasta", "isoformSwitchAnalyzeR_isoform_AA.fasta") %in% list.files("sequences")))
saveRDS(aSwitchList, "sl_part1.rds")
# ---- real chrX
setwd("../w3")            # staged by 30_input3_real_chrX.R (real salmon_quant, GTF with CDS, transcripts.fa, sample_metadata.tsv)
run_block("r_01.R"); cat("R: ORF origins after import:", paste(names(table(aSwitchList$orfAnalysis$orf_origin)), table(aSwitchList$orfAnalysis$orf_origin)), "\n")
run_block_part("r_03.R", 1)
cat("R: ORF origins after part 1:", paste(names(table(aSwitchList$orfAnalysis$orf_origin)), table(aSwitchList$orfAnalysis$orf_origin)), "\n")
chk("R: block kept annotated ORFs (analyzeORF branch skipped)", all(aSwitchList$orfAnalysis$orf_origin[!is.na(aSwitchList$orfAnalysis$orf_origin)] == "Annotation"))
saveRDS(aSwitchList, "sl_part1.rds")
cat("DONE 40a\n")
