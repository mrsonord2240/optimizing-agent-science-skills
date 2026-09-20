# INPUT 4 (part E): import CPC2 + Pfam results for the REAL chrX switching genes and run the consequence steps of the Skill.
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R")
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR))
sl <- readRDS("real_after_seq.rds")
system2(file.path("F:/OpenScience/audit-envs/alternative-splicing/Scripts/python.exe"), c("../40c_domtbl_to_pfamscan.py", "annot_real/pfam_domtbl.txt", "annot_real/pfam_scanfmt.txt", "annot/Pfam-A.clans.tsv.gz"))
# Skill order: analyzeORF (Skill says MUST precede) -> CPC2 -> PFAM -> (SignalP, IUPred not available) -> analyzeAlternativeSplicing -> analyzeSwitchConsequences
sl <- suppressWarnings(analyzeORF(sl, orfMethod = "longest", genomeObject = NULL, quiet = TRUE))
cat("orf_origin after Skill's analyzeORF() on a switch list that already has GTF-annotated ORFs:\n"); print(table(sl$orfAnalysis$orf_origin))
sl <- analyzeCPC2(sl, pathToCPC2resultFile = "annot_real/cpc2_result.txt", removeNoncodinORFs = TRUE, quiet = TRUE)
sl <- analyzePFAM(sl, pathToPFAMresultFile = "annot_real/pfam_scanfmt.txt", showProgress = FALSE, quiet = TRUE)
cat("real Pfam domain rows imported:", nrow(sl$domainAnalysis), " in", length(unique(sl$domainAnalysis$isoform_id)), "isoforms\n")
sl <- analyzeAlternativeSplicing(sl, onlySwitchingGenes = TRUE, quiet = TRUE, showProgress = FALSE)
sl <- analyzeSwitchConsequences(sl, consequencesToAnalyze = c("intron_retention", "coding_potential", "ORF_seq_similarity", "NMD_status", "domains_identified"), dIFcutoff = 0.1, quiet = TRUE, showProgress = FALSE)
sc <- sl$switchConsequence; print(table(sc$featureCompared, sc$switchConsequence))
chk("Real-data consequence table has NMD / IR / domain / coding-potential rows (workflow runs end to end)", length(unique(sc$featureCompared)) >= 4 && nrow(sc) > 20, sprintf("%d rows; features: %s", nrow(sc), paste(unique(sc$featureCompared), collapse = ", ")))
# independent check of intron_retention: an isoform pair flagged IR must differ by an exon structure with a retained intron -> verify with Ensembl biotype 'retained_intron' enrichment
ir <- sc[which(sc$featureCompared == "intron_retention" & sc$isoformsDifferent), ]
tid_of <- function(x) vapply(regmatches(x, regexec('transcript_id "([^"]+)"', x)), function(m) m[2], "")
g <- read.delim("annotation.gtf", header = FALSE, stringsAsFactors = FALSE, quote = "", comment.char = ""); tl <- g[g$V3 == "transcript", ]; bt <- setNames(tl$V2, tid_of(tl$V9))
cat("IR rows:", nrow(ir), " | Ensembl biotype of the isoform with IR: "); irIso <- ifelse(grepl("gain|more|retain", ir$switchConsequence, ignore.case = TRUE) , ir$isoformUpregulated, ir$isoformDownregulated); print(table(bt[unique(c(ir$isoformUpregulated, ir$isoformDownregulated))]))
# top switch check: RPL10 (dIF -0.33 on ENST00000406022) -- what does the Skill's pipeline say about it?
top <- extractTopSwitches(sl, filterForConsequences = FALSE, n = 5, sortByQvals = TRUE); print(top[, intersect(c("gene_name", "gene_switch_q_value", "switchConsequencesGene", "Rank"), colnames(top))])
chk("extractTopSwitches returns real chrX genes with q-values", nrow(top) > 0 && all(!is.na(top$gene_switch_q_value)), sprintf("%d rows; top %s", nrow(top), top$gene_name[1]))
saveRDS(sl, "real_final.rds"); cat("DONE 36c\n")
