# INPUT 4 part C: import external annotators (CPC2 + Pfam), run analyzeAlternativeSplicing / analyzeSwitchConsequences, compare to planted truth.
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R")
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR))
tr <- truth()
sl0 <- readRDS("in4_after_orf.rds")

cat("\n### (1) analyzePFAM with the raw hmmscan --domtblout file (the tool the Skill names)\n")
r <- tryCatch({ x <- analyzePFAM(sl0, pathToPFAMresultFile = "annot/pfam_domtbl.txt", showProgress = FALSE, quiet = TRUE); paste("returned;", nrow(x$domainAnalysis), "domain rows") },
              error = function(e) paste("ERROR:", conditionMessage(e)))
cat("raw domtblout ->", r, "\n")
chk("analyzePFAM accepts raw hmmscan --domtblout output (Skill names hmmscan only)", grepl("domain rows", r) && !grepl(" 0 domain rows", r), r)

cat("\n### (2) CPC2 -> Pfam (pfam_scan-format bridge) -> alternative splicing -> consequences\n")
sl <- analyzeCPC2(sl0, pathToCPC2resultFile = "annot/cpc2_result.txt", removeNoncodinORFs = TRUE, quiet = TRUE)
cp <- sl$isoformFeatures[, c("isoform_id", "codingPotential")]; cp <- cp[!duplicated(cp$isoform_id), ]
cat("CPC2 calls: coding", sum(cp$codingPotential), "noncoding", sum(!cp$codingPotential), "of", nrow(cp), "isoforms (random synthetic CDS)\n")
sl <- analyzePFAM(sl, pathToPFAMresultFile = "annot/pfam_scanfmt.txt", showProgress = FALSE, quiet = TRUE)
da <- sl$domainAnalysis
cat("Pfam domains imported:", nrow(da), "| by hmm_name:\n"); print(table(da$hmm_name))
skip_genes <- tr$gene_id[tr$type == "skip_switch"]
ub <- da[da$hmm_name %in% c("ubiquitin", "Ubiquitin") | grepl("^PF00240", da$hmm_acc), ]
chk("Pfam (hmmscan) finds the planted ubiquitin domain (PF00240) in A and B isoforms of skip genes, never in C", all(sub("_[ABC]$", "", ub$isoform_id) %in% skip_genes) && !any(grepl("_C$", ub$isoform_id)) && length(unique(ub$isoform_id)) >= 18,
    sprintf("%d isoforms with PF00240: %s", length(unique(ub$isoform_id)), paste(head(sort(unique(ub$isoform_id)), 6), collapse = ",")))
sl <- analyzeAlternativeSplicing(sl, onlySwitchingGenes = TRUE, quiet = TRUE, showProgress = FALSE)
as_tab <- sl$AlternativeSplicingAnalysis
ev <- colnames(as_tab)[grepl("^(ES|MEE|MES|IR|A5|A3|ATSS|ATTS)$", colnames(as_tab))]
cat("AS event columns:", paste(ev, collapse = ","), "\n"); print(colSums(as_tab[, ev, drop = FALSE]))
chk("analyzeAlternativeSplicing reports only exon skipping (ES) events (planted structures have only ES/ES-pairs)", all(colSums(as_tab[, setdiff(ev, c("ES","MEE","MES"))[setdiff(ev, c("ES","MEE","MES")) %in% colnames(as_tab)], drop = FALSE]) == 0) && sum(as_tab$ES) > 0, paste(names(colSums(as_tab[, ev, drop = FALSE])), colSums(as_tab[, ev, drop = FALSE]), collapse = " "))

cat("\n### (3) analyzeSwitchConsequences with the Skill's full consequence list while SignalP/IUPred2A were never imported\n")
full <- c('intron_retention','coding_potential','ORF_seq_similarity','NMD_status','domains_identified','IDR_identified','IDR_type','signal_peptide_identified')
r3 <- tryCatch({ x <- analyzeSwitchConsequences(sl, consequencesToAnalyze = full, dIFcutoff = 0.1, quiet = TRUE, showProgress = FALSE); x }, error = function(e) paste("ERROR:", conditionMessage(e)), warning = function(w) paste("WARNING:", conditionMessage(w)))
if (is.character(r3)) { cat("Skill full list ->", r3, "\n"); chk("Skill full 8-consequence call runs without SignalP/IUPred imports (Skill: 'silently drops')", FALSE, r3) } else { chk("Skill full 8-consequence call runs without SignalP/IUPred imports", TRUE); cat("types returned:", paste(unique(r3$switchConsequence$featureCompared), collapse = ", "), "\n") }
sl <- analyzeSwitchConsequences(sl, consequencesToAnalyze = c('intron_retention','coding_potential','ORF_seq_similarity','NMD_status','domains_identified'), dIFcutoff = 0.1, quiet = TRUE, showProgress = FALSE)
sc <- sl$switchConsequence
cat("consequence table columns:", paste(colnames(sc), collapse = ", "), "\n"); print(table(sc$featureCompared, sc$switchConsequence))
saveRDS(sl, "in4_final.rds")

# planted-truth checks
nmd <- sc[sc$featureCompared == "NMD status" | sc$featureCompared == "NMD_status", ]
cat("featureCompared levels:", paste(unique(sc$featureCompared), collapse = " | "), "\n")
pg <- tr$gene_id[tr$type == "poison_switch"]
nmd_rows <- sc[which(grepl("NMD", sc$featureCompared) & sc$isoformsDifferent), ]
poison_hit <- sapply(pg, function(g) any(nmd_rows$isoformUpregulated == paste0(g, "_B")))
chk("NMD consequence: poison isoform B flagged as the UP-regulated NMD-sensitive isoform in all 10 planted poison genes", all(poison_hit), sprintf("%d/10; consequence labels: %s", sum(poison_hit), paste(unique(nmd_rows$switchConsequence), collapse = " / ")))
chk("NMD consequence is quiet outside planted poison genes", all(sub("_[ABC]$", "", nmd_rows$isoformUpregulated) %in% pg) && all(sub("_[ABC]$", "", nmd_rows$isoformDownregulated) %in% pg), sprintf("%d NMD rows, %d genes", nrow(nmd_rows), length(unique(sub("_[ABC]$", "", nmd_rows$isoformUpregulated)))))
dom_rows <- sc[which(grepl("omain", sc$featureCompared) & sc$isoformsDifferent), ]
skip_hit <- sapply(skip_genes, function(g) any(dom_rows$isoformUpregulated == paste0(g, "_C") & dom_rows$isoformDownregulated == paste0(g, "_A")))
chk("Domain consequence: C (skip E3) up / A down flagged in all 10 planted skip genes with 'Domain loss'", all(skip_hit) && all(grepl("loss", dom_rows$switchConsequence[dom_rows$isoformUpregulated %in% paste0(skip_genes, "_C") & dom_rows$isoformDownregulated %in% paste0(skip_genes, "_A")])),
    sprintf("%d/10; labels: %s", sum(skip_hit), paste(unique(dom_rows$switchConsequence), collapse = " / ")))
chk("Domain consequence is quiet outside planted skip genes", all(sub("_[ABC]$", "", dom_rows$isoformUpregulated) %in% skip_genes), sprintf("%d domain rows", nrow(dom_rows)))

cat("\n### (3b) same NMD test WITHOUT the CPC2 filter (CPC2 never imported)\n")
sl_nc <- analyzePFAM(sl0, pathToPFAMresultFile = "annot/pfam_scanfmt.txt", showProgress = FALSE, quiet = TRUE)
sl_nc <- analyzeAlternativeSplicing(sl_nc, onlySwitchingGenes = TRUE, quiet = TRUE, showProgress = FALSE)
sl_nc <- analyzeSwitchConsequences(sl_nc, consequencesToAnalyze = c('intron_retention','ORF_seq_similarity','NMD_status','domains_identified'), dIFcutoff = 0.1, quiet = TRUE, showProgress = FALSE)
sc2 <- sl_nc$switchConsequence; nmd2 <- sc2[which(grepl("NMD", sc2$featureCompared) & sc2$isoformsDifferent), ]
ph2 <- sapply(pg, function(g) any(nmd2$isoformUpregulated == paste0(g, "_B") & nmd2$switchConsequence == "NMD sensitive"))
chk("No-CPC2 run: poison isoform B flagged NMD-sensitive & UP in all 10 planted poison genes", all(ph2), sprintf("%d/10", sum(ph2)))
chk("No-CPC2 run: NMD rows only in planted poison genes", all(sub("_[ABC]$", "", c(nmd2$isoformUpregulated, nmd2$isoformDownregulated)) %in% pg), sprintf("%d rows in %d genes", nrow(nmd2), length(unique(nmd2$gene_id))))
missing_g <- setdiff(pg, unique(sub("_[ABC]$", "", nmd_rows$isoformUpregulated[nmd_rows$switchConsequence == "NMD sensitive"])))
cat("poison genes lacking an NMD call WITH the CPC2 filter:", paste(missing_g, collapse = ","), "\n")
cpc_b <- sl$isoformFeatures[!duplicated(sl$isoformFeatures$isoform_id) & sl$isoformFeatures$isoform_id %in% paste0(missing_g, "_B"), c("isoform_id", "codingPotential")]; print(cpc_b)

cat("\n### (4) summaries and plots from the Skill's Visualization section\n")
tp <- extractTopSwitches(sl, filterForConsequences = TRUE, n = 25, sortByQvals = TRUE)
cat("extractTopSwitches(filterForConsequences=TRUE):", nrow(tp), "rows\n"); print(head(tp[, intersect(c("gene_name", "gene_switch_q_value", "switchConsequencesGene", "Rank"), colnames(tp))], 4))
ok_set <- tr$gene_id[!tr$type %in% c("null", "dge_only")]
chk("extractTopSwitches(filterForConsequences=TRUE) lists only genes with a planted proportion change (no null / DGE-only genes) and all 20 planted switches", all(tp$gene_name %in% ok_set) && all(c(pg, skip_genes) %in% tp$gene_name), sprintf("%d rows; non-planted: %s; missing planted: %s", nrow(tp), paste(setdiff(tp$gene_name, ok_set), collapse=","), paste(setdiff(c(pg, skip_genes), tp$gene_name), collapse=",")))
ecs <- extractConsequenceSummary(sl, consequencesToAnalyze = 'all', plotGenes = FALSE, returnResult = TRUE, plot = FALSE); print(head(ecs))
ece <- extractConsequenceEnrichment(sl, consequencesToAnalyze = 'all', plot = FALSE, returnResult = TRUE); print(head(ece[, 1:min(8, ncol(ece))]))
ess <- extractSplicingSummary(sl, asFractionTotal = FALSE, plot = FALSE, returnResult = TRUE); print(head(ess))
eSw <- extractSwitchSummary(sl, filterForConsequences = TRUE); print(eSw)
chk("extractConsequenceSummary returns non-empty table", is.data.frame(ecs) && nrow(ecs) > 0, sprintf("%d rows", nrow(ecs)))
pdf("switchplot_GENE001.pdf", width = 10, height = 8)
gp <- try(switchPlot(sl, gene = 'GENE001', condition1 = 'control', condition2 = 'treatment', localTheme = ggplot2::theme_bw(base_size = 12)), silent = TRUE); dev.off()
chk("switchPlot(GENE001) writes a non-empty PDF", !inherits(gp, "try-error") && file.exists("switchplot_GENE001.pdf") && file.size("switchplot_GENE001.pdf") > 5000, sprintf("%d bytes%s", file.size("switchplot_GENE001.pdf"), if (inherits(gp, "try-error")) paste(" ERR", conditionMessage(attr(gp, "condition"))) else ""))
cat("DONE 40d\n")
