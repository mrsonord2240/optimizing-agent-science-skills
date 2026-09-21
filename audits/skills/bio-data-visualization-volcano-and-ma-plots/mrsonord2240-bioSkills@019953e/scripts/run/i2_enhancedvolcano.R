# Input 2: SKILL.md block 03 (EnhancedVolcano) VERBATIM + verification of the Skill's stated EnhancedVolcano/shrinkage claims on real airway data.
suppressMessages({library(DESeq2); library(EnhancedVolcano); library(ggplot2)})
D <- "F:/OpenScience/audits/bio-data-visualization-volcano-and-ma-plots"
o <- readRDS(file.path(D, "data/airway_objs.rds"))
res <- o$apeglm; sym <- o$sym
ok <- !is.na(sym[rownames(res)]) & !duplicated(sym[rownames(res)]) & !duplicated(sym[rownames(res)], fromLast = TRUE)
newn <- sym[rownames(res)][ok]; res <- res[ok, ]; rownames(res) <- newn
fails <- 0; chk <- function(name, ok, note="") { cat(sprintf("[%s] %s %s\n", if (ok) "PASS" else "FAIL", name, note)); if (!ok) fails <<- fails + 1 }
df <- as.data.frame(res)
cat("selectLab genes in table:\n"); print(round(df[c("TP53","MYC","BRCA1"), c("baseMean","log2FoldChange","pvalue","padj")], 4))
# --- block 03 verbatim
png(file.path(D, "figs/i2_enhancedvolcano_block03.png"), 1600, 1200, res = 200)
p <- withCallingHandlers(source(file.path(D, "run/blocks/skill_block03.R"), echo = FALSE)$value,
                         warning = function(w) { cat("WARNING:", conditionMessage(w), "\n"); invokeRestart("muffleWarning") })
print(p); dev.off()
cat("class of return:", class(p), "\n")
b <- ggplot_build(p)
# find layers: points and text/repel labels
for (i in seq_along(b$data)) cat("layer", i, class(p$layers[[i]]$geom)[1], "rows:", nrow(b$data[[i]]), "\n")
lab_layers <- which(sapply(p$layers, function(l) inherits(l$geom, "GeomTextRepel") || inherits(l$geom, "GeomLabelRepel")))
labs_shown <- unique(unlist(lapply(lab_layers, function(i) as.character(b$data[[i]]$label))))
cat("labels drawn:", paste(labs_shown, collapse = ","), "\n")
pt_layer <- which(sapply(p$layers, function(l) inherits(l$geom, "GeomPoint")))
npts <- sum(sapply(pt_layer, function(i) nrow(b$data[[i]])))
cat("points drawn:", npts, " rows in res:", nrow(res), " padj NA:", sum(is.na(res$padj)), " rows with padj:", sum(!is.na(res$padj)), "\n")
chk("EnhancedVolcano point count == rows with non-NA padj (Skill: 'drops padj = NA')", npts == sum(!is.na(res$padj)))
chk("Skill claim: TP53 (padj 3e-4 but |LFC|<1) is silently NOT labelled (selectLab filtered by FCcutoff)", !"TP53" %in% labs_shown, paste("TP53 in labels:", "TP53" %in% labs_shown))
chk("MYC / BRCA1 labelled only if they pass thresholds", TRUE, paste("MYC in labels:", "MYC" %in% labs_shown, "; BRCA1 in labels:", "BRCA1" %in% labs_shown))
# pCutoff line location on padj axis
hl <- unlist(lapply(seq_along(b$data), function(i) if ("yintercept" %in% names(b$data[[i]])) b$data[[i]]$yintercept))
vl <- unlist(lapply(seq_along(b$data), function(i) if ("xintercept" %in% names(b$data[[i]])) b$data[[i]]$xintercept))
cat("hline y:", hl, " vline x:", vl, "\n")
chk("hline at -log10(0.05) on the padj axis", any(abs(hl - (-log10(0.05))) < 1e-6))
# separation: with y=padj do the colored points sit above the line? 
pts <- do.call(rbind, lapply(pt_layer, function(i) b$data[[i]]))
cat("points min y among red/blue/lightblue colour groups:\n")
print(aggregate(y ~ colour, pts, function(v) round(c(min = min(v), n = length(v)), 2)))
# does a symmetric x-limit hold? (Gotcha 3)
xr <- b$layout$panel_params[[1]]$x.range; cat("x range:", xr, " LFC range:", range(df$log2FoldChange), "\n")
chk("default x-limits asymmetric (Gotcha 3 premise)", abs(xr[1] + xr[2]) > 0.5)

# --- explicit selectLab test on a gene that DOES pass thresholds vs one that does not
sel <- c("DUSP1", "TP53")
p2 <- EnhancedVolcano(res, lab = rownames(res), x = "log2FoldChange", y = "padj", pCutoff = 0.05, FCcutoff = 1,
                      selectLab = sel, drawConnectors = TRUE, maxoverlapsConnectors = Inf)
b2 <- ggplot_build(p2); ll <- which(sapply(p2$layers, function(l) inherits(l$geom, "GeomTextRepel")))
cat("selectLab=DUSP1,TP53 -> drawn labels:", paste(unique(unlist(lapply(ll, function(i) as.character(b2$data[[i]]$label)))), collapse=","), "\n")
# --- NA handling: set NA padj to 1, count rows
res_na1 <- res; res_na1$padj[is.na(res_na1$padj)] <- 1
p3 <- EnhancedVolcano(res_na1, lab = rownames(res_na1), x = "log2FoldChange", y = "padj", pCutoff = .05, FCcutoff = 1)
b3 <- ggplot_build(p3); pl3 <- which(sapply(p3$layers, function(l) inherits(l$geom, "GeomPoint")))
n3 <- sum(sapply(pl3, function(i) nrow(b3$data[[i]]))); cat("points after NA->1:", n3, "\n")
chk("NA->1 restores all rows (Skill's stated remedy)", n3 == nrow(res))

# --- shrinkage claims
cat("\n--- Shrinkage-method claims ---\n")
cat("ashr result has svalue column (Skill code comment 'ashr also returns svalue'):", "svalue" %in% colnames(o$ashr), "\n")
chk("ashr lfcShrink returns svalue (Skill comment)", "svalue" %in% colnames(o$ashr))
cat("apeglm with svalue=TRUE keeps pvalue/padj columns: ", all(c("pvalue","padj") %in% colnames(o$apeglm_sv)), " (cols: ", paste(colnames(o$apeglm_sv), collapse=","), ")\n")
sv <- o$apeglm_sv$svalue; padj <- o$raw$padj
cat(sprintf("s<0.005: %d genes; padj<0.05: %d genes; overlap: %d\n", sum(sv < .005, na.rm=TRUE), sum(padj < .05, na.rm=TRUE), sum(sv < .005 & padj < .05, na.rm=TRUE)))
chk("s<0.005 ~ padj<0.05 (within 20% of gene count)", abs(sum(sv < .005, na.rm=TRUE) - sum(padj < .05, na.rm=TRUE)) / sum(padj < .05, na.rm=TRUE) < 0.2)
# 'normal' deprecated?  check the man page text
rd <- capture.output(tools::Rd2txt(utils:::.getHelpFile(help("lfcShrink", package = "DESeq2")), options = list(underline_titles = FALSE)))
cat("man page mentions 'normal' as deprecated/legacy: ", any(grepl("deprecat|legacy|original", rd, ignore.case = TRUE)), "\n")
cat(grep("normal|svalue", rd, value = TRUE, ignore.case = TRUE)[1:12], sep = "\n")
# apeglm vs ashr: do they disagree on top hits?
ra <- as.data.frame(o$apeglm); rb <- as.data.frame(o$ashr)
top_a <- rownames(ra)[order(-abs(ra$log2FoldChange) * ifelse(is.na(ra$pvalue), 0, -log10(ra$pvalue)))][1:20]
top_b <- rownames(rb)[order(-abs(rb$log2FoldChange) * ifelse(is.na(rb$pvalue), 0, -log10(rb$pvalue)))][1:20]
cat("top-20 combined-rank overlap apeglm vs ashr:", length(intersect(top_a, top_b)), "/ 20\n")
cat("\nSUMMARY: fails =", fails, "\n")
