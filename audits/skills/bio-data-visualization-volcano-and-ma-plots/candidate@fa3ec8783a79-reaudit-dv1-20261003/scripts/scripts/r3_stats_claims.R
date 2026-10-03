# Re-audit 3 (volcano-and-ma-plots): numeric and API claims of SKILL.md / references on the real airway dds.
# Usage: r.sh r3_stats_claims.R <outdir>
a <- commandArgs(TRUE); out <- a[1]; dir.create(out, FALSE, TRUE); setwd(out)
suppressMessages({library(DESeq2); library(ggplot2)})
ok <- TRUE
chk <- function(l, c) { ok <<- ok && isTRUE(c); cat(sprintf("[%s] %s\n", if (isTRUE(c)) "PASS" else "FAIL", l)) }
dds <- readRDS("F:/OpenScience/audit-envs/data-visualization/public-data/derived/airway_dds_condition.rds")
q <- function(expr) suppressMessages(suppressWarnings(expr))
raw <- results(dds, name = 'condition_treated_vs_control')
ape <- q(lfcShrink(dds, coef = 'condition_treated_vs_control', type = 'apeglm'))
ash <- q(lfcShrink(dds, contrast = c('condition', 'treated', 'control'), type = 'ashr'))
ashc <- q(lfcShrink(dds, coef = 'condition_treated_vs_control', type = 'ashr'))
cat("lfcShrink default type in this DESeq2:", deparse(formals(lfcShrink)$type)[1], "\n")
chk("default lfcShrink type is 'apeglm' in DESeq2 1.46.0 (SKILL.md)", identical(eval(formals(lfcShrink)$type)[1], "apeglm"))
chk("ashr accepts coef= as well as contrast= (table row)", inherits(ashc, "DESeqResults") && nrow(ashc) == nrow(dds))
r <- try(q(lfcShrink(dds, contrast = c('condition', 'treated', 'control'), type = 'apeglm')), silent = TRUE)
cat("apeglm with contrast= ->", if (inherits(r, "try-error")) substr(as.character(r), 1, 140) else "no error", "\n")
chk("apeglm with contrast= is rejected (table row 'no support for contrast=')", inherits(r, "try-error"))
# --- svalue
sv_a <- q(lfcShrink(dds, coef = 'condition_treated_vs_control', type = 'apeglm', svalue = TRUE))
sv_s <- q(lfcShrink(dds, coef = 'condition_treated_vs_control', type = 'ashr', svalue = TRUE))
cat("apeglm svalue cols:", paste(colnames(sv_a), collapse = ","), "\nashr   svalue cols:", paste(colnames(sv_s), collapse = ","), "\n")
chk("svalue=TRUE (apeglm, ashr): has svalue, no pvalue/padj", all(c("svalue") %in% colnames(sv_a), "svalue" %in% colnames(sv_s)) && !any(c("pvalue", "padj") %in% c(colnames(sv_a), colnames(sv_s))))
chk("default apeglm/ashr results have no svalue column", !"svalue" %in% colnames(ape) && !"svalue" %in% colnames(ash))
chk("SKILL.md column list 'baseMean, log2FoldChange, lfcSE, svalue' matches apeglm", identical(colnames(sv_a), c("baseMean", "log2FoldChange", "lfcSE", "svalue")))
r <- try(q(lfcShrink(dds, coef = 'condition_treated_vs_control', type = 'normal', svalue = TRUE)), silent = TRUE)
cat("normal svalue=TRUE ->", if (inherits(r, "try-error")) substr(as.character(r), 1, 140) else "no error", "\n")
chk("type='normal' with svalue=TRUE errors in 1.46.0", inherits(r, "try-error"))
# s-value vs padj counts
s005 <- sum(sv_a$svalue < 0.005, na.rm = TRUE); p05 <- sum(ape$padj < 0.05, na.rm = TRUE); both <- sum(sv_a$svalue < 0.005 & ape$padj < 0.05, na.rm = TRUE)
cat(sprintf("s<0.005: %d genes; padj<0.05: %d; shared %d  (claim 4,684 / 3,994 / 3,842)\n", s005, p05, both))
chk("s-value claim '4,684 vs 3,994 genes, 3,842 shared' (apeglm)", s005 == 4684 && p05 == 3994 && both == 3842)
# --- shrinkage claims
bm <- raw$baseMean; lo <- !is.na(bm) & bm < 5
cat(sprintf("baseMean<5 genes: %d; median |LFC| MLE %.2f, apeglm %.2f, ashr %.2f\n", sum(lo), median(abs(raw$log2FoldChange[lo]), na.rm = TRUE), median(abs(ape$log2FoldChange[lo]), na.rm = TRUE), median(abs(ash$log2FoldChange[lo]), na.rm = TRUE)))
chk("claim median |LFC| at baseMean<5: 0.77 -> 0.01 (apeglm), 0.02 (ashr)", round(median(abs(raw$log2FoldChange[lo]), na.rm = TRUE), 2) == 0.77 && round(median(abs(ape$log2FoldChange[lo]), na.rm = TRUE), 2) == 0.01 && round(median(abs(ash$log2FoldChange[lo]), na.rm = TRUE), 2) == 0.02)
inc_a <- sum(abs(ape$log2FoldChange) > abs(raw$log2FoldChange), na.rm = TRUE); inc_s <- sum(abs(ash$log2FoldChange) > abs(raw$log2FoldChange), na.rm = TRUE)
diffa <- abs(ape$log2FoldChange) - abs(raw$log2FoldChange); idx <- which(diffa > 0)
cat(sprintf("apeglm |LFC| > MLE for %d of %d genes; ashr %d; max |LFC| MLE %.2f -> apeglm %.2f; largest increase %.2f; median baseMean of raised genes %.0f\n", inc_a, nrow(dds), inc_s, max(abs(raw$log2FoldChange), na.rm = TRUE), max(abs(ape$log2FoldChange), na.rm = TRUE), max(diffa, na.rm = TRUE), median(bm[idx])))
chk("claim: apeglm exceeded MLE in 108 of 29,391; ashr 0; max 9.51 -> 10.99; largest increase 1.48; median baseMean 1444", inc_a == 108 && nrow(dds) == 29391 && inc_s == 0 && round(max(abs(raw$log2FoldChange), na.rm = TRUE), 2) == 9.51 && round(max(abs(ape$log2FoldChange), na.rm = TRUE), 2) == 10.99 && round(max(diffa, na.rm = TRUE), 2) == 1.48 && round(median(bm[idx])) == 1444)
# --- EnhancedVolcano: selectLab and NA claims, svalue
suppressMessages(library(EnhancedVolcano))
res <- ape; nm <- rownames(res)
ev <- function(sel, r = res) suppressWarnings(EnhancedVolcano(r, lab = rownames(r), x = 'log2FoldChange', y = 'padj', pCutoff = 0.05, FCcutoff = 1, selectLab = sel, drawConnectors = FALSE))
lab_texts <- function(p) { L <- lapply(ggplot_build(p)$data, function(d) if ("label" %in% names(d)) as.character(d$label) else NULL); unlist(L) }
ns_gene <- nm[which(!is.na(res$padj) & res$padj > 0.5 & abs(res$log2FoldChange) < 0.05)[1]]
na_gene <- nm[which(is.na(res$padj))[1]]
sel <- c(ns_gene, "NOT_A_GENE", na_gene); lt <- lab_texts(ev(sel)); cat("selectLab asked:", paste(sel, collapse = ", "), " | labelled:", paste(setdiff(lt, ""), collapse = ", "), "\n")
chk(sprintf("a listed gene failing pCutoff/FCcutoff (%s: padj %.2f, LFC %.3f) is still labelled", ns_gene, res[ns_gene, "padj"], res[ns_gene, "log2FoldChange"]), ns_gene %in% lt)
chk("a name absent from lab is silently ignored (no error, not drawn)", !"NOT_A_GENE" %in% lt)
# built data keeps NA rows; geom_point removes them only when the plot is drawn. Count what is actually drawn from the gtable.
drawn <- function(p) { gt <- suppressWarnings(ggplotGrob(p)); n <- 0; labs <- character()
  walk <- function(g) { if (inherits(g, "points")) n <<- n + length(g$x) else if (inherits(g, "text") && is.character(g$label)) labs <<- c(labs, g$label); if (inherits(g, "gTree")) for (ch in g$children) walk(ch) ; if (inherits(g, "gList")) for (ch in g) walk(ch) }
  for (g in gt$grobs) walk(g); list(points = n, text = labs) }
dr <- drawn(ev(c("TP53"))); cat("EnhancedVolcano points actually drawn:", dr$points, " non-NA padj:", sum(!is.na(res$padj)), " all rows:", nrow(res), "
")
chk("EnhancedVolcano draws only the non-NA-padj rows (claim 'drops padj = NA')", dr$points == sum(!is.na(res$padj)))
dr2 <- drawn(ev(sel)); cat("drawn text with selectLab = [NS gene, absent, NA-padj gene]:", paste(setdiff(dr2$text, c("", "Down", "NS", "Up")), collapse = ", "), "
")
chk("a listed gene whose padj is NA is not drawn as a label", !na_gene %in% dr2$text)
# default colours
p_def <- ev(c("TP53")); cols <- table(toupper(ggplot_build(p_def)$data[[1]]$colour)); print(cols)
nsig <- sum(res$padj < .05 & abs(res$log2FoldChange) > 1, na.rm = TRUE)
cat("default `col`: shared-colour points (padj<.05 and |LFC|>1):", nsig, "
")
chk("default EnhancedVolcano gives one colour to both Up and Down (claim)", any(cols == nsig))
# exact value for the 0.77 claim
cat(sprintf("exact median |LFC| baseMean<5: MLE %.4f, apeglm %.4f, ashr %.4f; n=%d
", median(abs(raw$log2FoldChange[lo]), na.rm = TRUE), median(abs(ape$log2FoldChange[lo]), na.rm = TRUE), median(abs(ash$log2FoldChange[lo]), na.rm = TRUE), sum(lo)))
cat("RESULT", if (ok) "PASS" else "FAIL", "\n")
