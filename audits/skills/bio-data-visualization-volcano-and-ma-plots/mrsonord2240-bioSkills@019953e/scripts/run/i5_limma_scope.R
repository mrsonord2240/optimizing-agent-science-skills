# Input 5 (SCOPE): the Skill claims to cover microarray / proteomics limma tables. Real data: Bioconductor ALL (Chiaretti 2004), BCR/ABL vs NEG B-cell ALL.
suppressMessages({library(limma); library(ALL); library(ggplot2); library(ggrepel); library(dplyr); library(EnhancedVolcano)})
D <- "F:/OpenScience/audits/bio-data-visualization-volcano-and-ma-plots"
data(ALL)
keep <- grepl("^B", ALL$BT) & ALL$mol.biol %in% c("BCR/ABL", "NEG")
e <- ALL[, keep]; grp <- factor(as.character(e$mol.biol), levels = c("NEG", "BCR/ABL"))
fit <- eBayes(lmFit(exprs(e), model.matrix(~ grp))); tt <- topTable(fit, coef = 2, number = Inf, sort.by = "none")
cat("ALL subset:", ncol(e), "arrays (", paste(table(grp), collapse = "/"), ") x", nrow(tt), "probes; columns:", paste(colnames(tt), collapse = ","), "; adj.P.Val<0.05:", sum(tt$adj.P.Val < .05), "\n")
fails <- 0; chk <- function(name, ok, note="") { cat(sprintf("[%s] %s %s\n", if (ok) "PASS" else "FAIL", name, note)); if (!ok) fails <<- fails + 1 }
source(file.path(D, "run/blocks/skill_block02.R"))
# (a) Skill: "Proteomics (limma/MSstats): Already moderated; plot logFC vs adj.P.Val directly" -> call the Skill's function on the topTable as-is
r <- try(volcano_plot(tt), silent = TRUE)
msg <- if (inherits(r, "try-error")) conditionMessage(attr(r, "condition")) else "no error"
cat("(a) volcano_plot(topTable) as delivered ->", substr(msg, 1, 160), "\n")
chk("Skill function runs on a limma topTable as-is (Skill: 'plot logFC vs adj.P.Val directly')", !inherits(r, "try-error"))
# (b) adapt by renaming columns (what an agent must do; Skill gives no mapping)
tt2 <- tt; colnames(tt2)[colnames(tt2) == "logFC"] <- "log2FoldChange"; colnames(tt2)[colnames(tt2) == "P.Value"] <- "pvalue"; colnames(tt2)[colnames(tt2) == "adj.P.Val"] <- "padj"; colnames(tt2)[colnames(tt2) == "AveExpr"] <- "baseMean"
p <- volcano_plot(tt2, lfc_threshold = 1, top_n = 8)
png(file.path(D, "figs/i5_limma_volcano_renamed.png"), 1300, 1100, res = 180); print(p); dev.off()
b <- ggplot_build(p)$data[[1]]; cls <- table(p$data$significance); print(cls)
own <- with(tt, sum(adj.P.Val < .05 & logFC > 1)); own_d <- with(tt, sum(adj.P.Val < .05 & logFC < -1))
chk("Up/Down counts on the plot equal an independent limma-table recompute", cls[["Up"]] == own && cls[["Down"]] == own_d, paste0("plot Up/Down ", cls[["Up"]], "/", cls[["Down"]], " vs table ", own, "/", own_d))
cat("x-axis label on the plot: '", "log2 fold change (shrunken)", "' -- limma logFC is NOT shrunk; moderation acts on the SE/t-statistic. max|logFC| =", round(max(abs(tt$logFC)), 2), "\n")
cat("labelled probes:", paste(unique(p$data$label[p$data$label != ""]), collapse = ","), "\n")
# limma logFC vs its eBayes-free ordinary LFC (difference of group means): identical -> nothing is shrunk
m <- exprs(e); ord <- rowMeans(m[, grp == "BCR/ABL"]) - rowMeans(m[, grp == "NEG"])
chk("limma logFC differs from the plain difference of group means (i.e. limma shrinks LFC, Skill claim)", max(abs(ord - tt$logFC)) > 1e-6, sprintf("max abs difference = %.2e", max(abs(ord - tt$logFC))))
# (c) EnhancedVolcano on limma columns directly, y = adj.P.Val
pe <- EnhancedVolcano(tt, lab = rownames(tt), x = "logFC", y = "adj.P.Val", pCutoff = .05, FCcutoff = 1, selectLab = rownames(tt)[order(tt$P.Value)][1:5], drawConnectors = TRUE, maxoverlapsConnectors = Inf)
png(file.path(D, "figs/i5_limma_enhancedvolcano.png"), 1400, 1100, res = 180); print(pe); dev.off()
be <- ggplot_build(pe); pts <- do.call(rbind, lapply(which(sapply(pe$layers, function(l) inherits(l$geom, "GeomPoint"))), function(i) be$data[[i]]))
chk("EnhancedVolcano draws all 12,625 probes from limma columns", nrow(pts) == nrow(tt), paste("points:", nrow(pts)))
saveRDS(list(tt = tt), file.path(D, "data/all_limma_tt.rds")); write.csv(tt, file.path(D, "data/all_limma_toptable.csv"))
cat("SUMMARY fails =", fails, "\n")
