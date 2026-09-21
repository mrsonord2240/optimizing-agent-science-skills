# INPUT 4 (real chrX): SKILL block r_02 part 2 verbatim on the real chrX switch list (annotated ORFs), CPC2 + hmmscan->converter results from 40b.
# Independent references: Ensembl transcript biotype (nonsense_mediated_decay, protein_coding) from the GTF's source column.
# Also tests the Skill's warning that analyzeORF('longest') over annotated ORFs degrades the NMD call.
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R"); source("../helpers2.R")
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR))
setwd("w3"); file.copy("annot/cpc2_result.txt", "cpc2_result.txt", overwrite = TRUE); file.copy("annot/pfam_scanfmt.txt", "pfam_scanfmt.txt", overwrite = TRUE)
aSwitchList <- readRDS("sl_part1.rds")
run_block_part("r_02.R", 2)
sc <- aSwitchList$switchConsequence
cat("real consequence rows:", nrow(sc), "| types:", paste(names(table(sc$featureCompared)), table(sc$featureCompared), collapse = "; "), "\n")
chk("real chrX: analyzePFAM accepted the converter output (domain rows imported)", nrow(aSwitchList$domainAnalysis) > 0, sprintf("%d domain rows, %d isoforms", nrow(aSwitchList$domainAnalysis), length(unique(aSwitchList$domainAnalysis$isoform_id))))
# PTC flag vs Ensembl NMD biotype (independent), all isoforms with an ORF
gtf <- readLines("annotation.gtf"); fl <- strsplit(gtf, "\t", fixed = TRUE); src <- vapply(fl, `[`, "", 2); tid <- vapply(fl, function(x) sub('.*transcript_id "([^"]+)".*', "\\1", x[9]), "")
bio <- tapply(src, tid, function(x) x[1])
orf <- aSwitchList$orfAnalysis; cat("orfAnalysis columns:", paste(colnames(orf), collapse = ","), "\n")
ptccol <- grep("PTC|nmd", colnames(orf), ignore.case = TRUE, value = TRUE)[1]; cat("PTC column:", ptccol, "\n")
ev <- function(orf, label) {
  o <- orf[!is.na(orf$orf_origin), ]; o$biotype <- bio[o$isoform_id]; o <- o[!is.na(o$biotype) & o$biotype %in% c("nonsense_mediated_decay", "protein_coding"), ]
  truth <- o$biotype == "nonsense_mediated_decay"; call <- !is.na(o[[ptccol]]) & (o[[ptccol]] == TRUE | o[[ptccol]] == "TRUE")
  cat(sprintf("%s: n=%d (NMD biotype %d) | PTC flag sens %.2f (%d/%d) spec %.2f (%d/%d) | orf_origin %s\n", label, nrow(o), sum(truth), sum(call & truth) / sum(truth), sum(call & truth), sum(truth), sum(!call & !truth) / sum(!truth), sum(!call & !truth), sum(!truth), paste(names(table(o$orf_origin)), table(o$orf_origin), collapse = ",")))
  c(sens = sum(call & truth) / sum(truth), spec = sum(!call & !truth) / sum(!truth)) }
a <- ev(orf, "annotated ORFs (Skill route)")
chk("annotated-ORF PTC flag agrees with Ensembl NMD biotype: sens >= 0.9 and spec >= 0.95", a["sens"] >= 0.9 && a["spec"] >= 0.95)
al <- suppressWarnings(analyzeORF(readRDS("sl_part1.rds"), orfMethod = "longest", genomeObject = NULL, quiet = TRUE))
b <- ev(al$orfAnalysis, "after analyzeORF('longest') over annotated ORFs")
chk("Skill warning verified: analyzeORF('longest') over annotated ORFs degrades the NMD call (sens or spec drops)", b["sens"] < a["sens"] - 0.1 || b["spec"] < a["spec"] - 0.05, sprintf("sens %.2f -> %.2f, spec %.2f -> %.2f", a["sens"], b["sens"], a["spec"], b["spec"]))
# CPC2 vs biotype
cpc <- read.delim("cpc2_result.txt"); cpc$biotype <- bio[cpc$X.ID]
cat("CPC2 label by Ensembl biotype (top biotypes):\n"); print(head(sort(table(paste(cpc$biotype, cpc$label)), decreasing = TRUE), 8))
cat("DONE 40d\n")
