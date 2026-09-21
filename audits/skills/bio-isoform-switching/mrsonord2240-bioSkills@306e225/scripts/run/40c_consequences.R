# INPUT 4 consequences: SKILL block r_02 PART 2 verbatim (analyzeCPC2, analyzePFAM, analyzeSwitchConsequences) on the switch lists from 40a,
# with the CPC2 + hmmscan->converter outputs from 40b. Truth: GENE001-010 poison exon P (NMD, isoform B up), GENE011-020 skip E3 with ubiquitin (isoform C up, domain loss).
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R"); source("../helpers2.R")
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR))
setwd("w4s"); file.copy("annot/cpc2_result.txt", "cpc2_result.txt", overwrite = TRUE); file.copy("annot/pfam_scanfmt.txt", "pfam_scanfmt.txt", overwrite = TRUE)
aSwitchList <- readRDS("sl_part1.rds")
run_block_part("r_02.R", 2)
sc <- aSwitchList$switchConsequence
cat("consequence rows:", nrow(sc), "| types:", paste(names(table(sc$featureCompared)), table(sc$featureCompared), collapse = "; "), "\n")
poison <- sprintf("GENE%03d", 1:10); skip <- sprintf("GENE%03d", 11:20)
gene_of <- function(x) sub("_[ABC]$", "", x)
nmd <- sc[which(sc$featureCompared == "NMD_status" & sc$switchConsequence == "NMD sensitive"), ]
nmd_ok <- sapply(poison, function(g) any(gene_of(nmd$isoformUpregulated) == g & grepl("_B$", nmd$isoformUpregulated)))
cat(sprintf("NMD: %d poison genes with B (poison) up + 'NMD sensitive' | NMD calls outside poison genes: %d\n", sum(nmd_ok), sum(!gene_of(nmd$isoformUpregulated) %in% poison)))
chk("NMD_status flags the poison isoform B as NMD-sensitive and up in 10/10 poison genes (removeNoncodinORFs = FALSE)", sum(nmd_ok) == 10)
dom <- sc[sc$featureCompared == "domains_identified" & !is.na(sc$switchConsequence), ]
cat("domain rows by consequence:", paste(names(table(dom$switchConsequence)), table(dom$switchConsequence), collapse = "; "), "\n")
dl <- dom[grepl("loss", dom$switchConsequence, ignore.case = TRUE), ]
dl_ok <- sapply(skip, function(g) any(gene_of(dl$isoformDownregulated) == g & grepl("_A$", dl$isoformDownregulated) & grepl("_C$", dl$isoformUpregulated)))
cat(sprintf("Domain loss: %d/10 skip genes (A down, C up) | domain calls outside skip genes: %d\n", sum(dl_ok), sum(!gene_of(dom$isoformUpregulated) %in% skip)))
chk("domains_identified: 'Domain loss' A->C in 10/10 skip genes and quiet elsewhere", sum(dl_ok) == 10 && sum(!gene_of(dom$isoformUpregulated) %in% skip) == 0)
da <- aSwitchList$domainAnalysis; cat("domainAnalysis columns:", paste(colnames(da), collapse = ","), "| rows", nrow(da), "\n")
uu <- da[da$hmm_acc %in% grep("PF00240", da$hmm_acc, value = TRUE), ]
chk("PF00240 never in an isoform C (skip isoform lacks the domain)", !any(grepl("_C$", uu$isoform_id)) && length(unique(gene_of(uu$isoform_id))) == 10, sprintf("%d PF00240 rows in %d genes", nrow(uu), length(unique(gene_of(uu$isoform_id)))))
ir <- sc[which(sc$featureCompared == "intron_retention" & !is.na(sc$switchConsequence)), ]; cat("intron_retention calls:", nrow(ir), "(none planted)\n")
chk("no intron-retention calls on a set with no IR", nrow(ir) == 0)
# independent coordinate check of the converter: hmmscan ali coords vs ISAR domainAnalysis coords for one row
dl_ <- grep("^#", readLines("annot/pfam_domtbl.txt"), invert = TRUE, value = TRUE); dt <- data.frame(V2 = vapply(strsplit(dl_, "[ ]+"), `[`, "", 2)); dt <- dt[grepl("PF00240", dt$V2), , drop = FALSE]; cat("hmmscan PF00240 rows:", nrow(dt), " ISAR PF00240 rows:", nrow(uu), "\n")
chk("converter: number of PF00240 rows conserved through analyzePFAM", nrow(dt) == nrow(uu))
# variant: removeNoncodinORFs = TRUE (Skill says it drops PTC isoforms from the NMD call: 8/10)
al <- aSwitchList; al$switchConsequence <- NULL
al2 <- readRDS("sl_part1.rds"); al2 <- analyzeCPC2(al2, pathToCPC2resultFile = "cpc2_result.txt", removeNoncodinORFs = TRUE)
al2 <- analyzeSwitchConsequences(al2, consequencesToAnalyze = c("intron_retention", "ORF_seq_similarity", "NMD_status", "coding_potential"), dIFcutoff = 0.1)
s2 <- al2$switchConsequence; n2 <- s2[which(s2$featureCompared == "NMD_status" & s2$switchConsequence == "NMD sensitive"), ]
ok2 <- sapply(poison, function(g) any(gene_of(n2$isoformUpregulated) == g & grepl("_B$", n2$isoformUpregulated)))
cat(sprintf("removeNoncodinORFs = TRUE: NMD-sensitive B up in %d/10 poison genes\n", sum(ok2)))
cpc <- read.delim("cpc2_result.txt"); cat("CPC2 label of poison B isoforms:", paste(cpc$label[match(paste0(poison, "_B"), cpc$X.ID)], collapse = ","), "\n")
chk("Skill's claim: TRUE drops PTC isoforms from the NMD call (fewer than 10/10)", sum(ok2) < 10, sprintf("%d/10", sum(ok2)))
# missing-annotator errors quoted in the Skill
r <- try(analyzeSwitchConsequences(readRDS("sl_part1.rds"), consequencesToAnalyze = c("NMD_status", "signal_peptide_identified"), dIFcutoff = 0.1, quiet = TRUE), silent = TRUE)
cat("signal_peptide_identified without SignalP ->", if (inherits(r, "try-error")) trimws(gsub("\n", " ", conditionMessage(attr(r, "condition")))) else "NO ERROR", "\n")
chk("missing SignalP annotation is an ERROR with the Skill-quoted text", inherits(r, "try-error") && grepl("signal peptides, the result of the SignalP analysis must be", conditionMessage(attr(r, "condition"))))
r <- try(analyzeCPC2(readRDS("sl_part1.rds"), pathToCPC2resultFile = "cpc2_result.txt"), silent = TRUE); cat("analyzeCPC2 without removeNoncodinORFs ->", if (inherits(r, "try-error")) trimws(gsub("\n", " ", conditionMessage(attr(r, "condition")))) else "NO ERROR", "\n")
# raw domtblout is rejected (the Skill's stated reason for the converter)
r <- try(analyzePFAM(readRDS("sl_part1.rds"), pathToPFAMresultFile = "annot/pfam_domtbl.txt", quiet = TRUE), silent = TRUE); cat("raw --domtblout ->", if (inherits(r, "try-error")) trimws(gsub("\n", " ", conditionMessage(attr(r, "condition")))) else "ACCEPTED", "\n")
chk("raw hmmscan --domtblout is rejected by analyzePFAM (as the Skill states)", inherits(r, "try-error"))
# no-CDS GTF: extractSequence before ORFs must fail with the Skill-quoted message (fresh import via r_01 in a separate dir)
setwd(".."); set.seed(9); ids <- c(sprintf("ctrl_%d", 1:3), sprintf("trt_%d", 1:3)); stage_salmon("w4n", ids, sprintf("SRR71%05d", 1:6), rep(c("control", "treatment"), each = 3)); setwd("w4n")
run_block("r_01.R"); dir.create("sequences", showWarnings = FALSE)
r <- try(extractSequence(aSwitchList, onlySwitchingGenes = TRUE, pathToOutput = "sequences/", writeToFile = TRUE), silent = TRUE)
cat("extractSequence before ORFs (no-CDS GTF) ->", if (inherits(r, "try-error")) trimws(gsub("\n", " ", conditionMessage(attr(r, "condition")))) else "NO ERROR", "\n")
chk("extractSequence before ORFs fails with the quoted 'addORFfromGTF()' message", inherits(r, "try-error") && grepl("addORFfromGTF", conditionMessage(attr(r, "condition"))))
cat("DONE 40c synthetic\n")
