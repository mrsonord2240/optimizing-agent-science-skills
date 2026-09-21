source("helpers.R")
library(svglite)
source("gen_synth_edge.R")
Tr <- readRDS("data/synth_edge_truth.rds"); T <- Tr$T; samples <- Tr$samples
genes <- c("TP53","KRAS","PIK3CA","MYC","RB1","EMPTYG")
col <- SKILL_COL; alter_fun <- get_alter_fun(col)
# ---- agent-side matrix build from the MAF (+ planted CNV calls for MYC) ----
df <- read_maf_df("data/synth_edge.maf"); long <- maf_to_long(df)
cnv <- data.frame(Hugo_Symbol="MYC", Tumor_Sample_Barcode=c("S01","S04"), cls="Amp")
long <- rbind(long, cnv)
mat <- build_mat(long, genes, samples)
# ---- independent expectation straight from the planted truth ----
expm <- matrix("", length(genes), length(samples), dimnames=list(genes, samples))
for (g in genes) for (s in samples) { z <- sort(unique(T$cls[T$gene==g & T$sample==s])); expm[g,s] <- paste(z, collapse=";") }
cat("matrix from MAF+CNV equals planted truth:", identical(norm_cell(as.vector(mat)), norm_cell(as.vector(expm))), "\n")
cat("multi-class planted cells:", sum(grepl(";", expm)), " (S01 TP53 Missense;Truncating, S04 MYC Amp;Missense expected)\n")
cat("S02 TP53 (two Missense hits) cell:", expm["TP53","S02"], "| via MAF:", mat["TP53","S02"], "\n")
draw_check <- function(remove_cols, tag) {
  ht <- oncoPrint(mat, alter_fun=alter_fun, col=col, remove_empty_columns=remove_cols, remove_empty_rows=FALSE, show_pct=TRUE,
                  pct_gp=gpar(fontsize=7), row_names_gp=gpar(fontsize=8))
  f <- paste0("out/i3_", tag, ".svg"); svglite(f, width=12, height=4); hd <- draw(ht); dev.off()
  png(paste0("out/i3_", tag, ".png"), width=1300, height=400, res=100); draw(ht); dev.off()
  ro <- unlist(row_order(hd)); co <- unlist(column_order(hd))
  D <- decode_cells(f, col)
  cat("[", tag, "] columns drawn:", length(co), "rows drawn:", length(ro), "\n")
  cat("[", tag, "] drawn gene order:", rownames(mat)[ro], "\n")
  keepcols <- if (remove_cols) which(colSums(expm!="")>0) else seq_along(samples)   # oncoPrint drops empty columns, then orders the survivors
  exp <- expm[ro, keepcols[co], drop=FALSE]
  cat("[", tag, "] cell mismatches vs planted truth:", sum(norm_cell(as.vector(exp)) != norm_cell(as.vector(D$cells))), "of", length(exp), "\n")
  pc <- D$P$txt[grepl("%$", D$P$txt$label),]; pc <- pc[order(pc$y),]
  cat("[", tag, "] pct labels (top->bottom):", pc$label, "\n")
  exp_pct_all <- round(rowSums(expm!="")/30*100)[ro]
  keep <- colSums(expm!="")>0
  exp_pct_kept <- round(rowSums(expm[,keep]!="")/sum(keep)*100)[ro]
  cat("[", tag, "] expected pct /30 (cohort):", paste0(exp_pct_all,"%"), "\n[", tag, "] expected pct /", sum(keep), "(altered only):", paste0(exp_pct_kept,"%"), "\n")
  invisible(hd)
}
draw_check(FALSE, "keepempty")
draw_check(TRUE,  "dropempty")
# ---- degenerate inputs ----
cat("\n-- one sample --\n")
m1 <- mat[, "S01", drop=FALSE]
r1 <- try({ svglite("out/i3_one.svg", width=4, height=4); ht1 <- oncoPrint(m1, alter_fun=alter_fun, col=col, remove_empty_rows=FALSE); hd1 <- draw(ht1); dev.off()
  png("out/i3_one.png", width=500, height=450, res=100); draw(ht1); dev.off(); D1 <- decode_cells("out/i3_one.svg", col); print(D1$cells); unlist(row_order(hd1)) }, silent=TRUE)
cat("one-sample result:", if (inherits(r1,"try-error")) paste("ERROR:", conditionMessage(attr(r1,"condition"))) else "ok", "\n")
cat("\n-- all-empty matrix (no alterations) --\n")
m0 <- mat; m0[] <- ""
r0 <- try({ png("out/i3_allempty.png", width=600, height=300); draw(oncoPrint(m0, alter_fun=alter_fun, col=col)); dev.off() }, silent=TRUE)
cat("all-empty result:", if (inherits(r0,"try-error")) paste("ERROR:", conditionMessage(attr(r0,"condition"))) else "ok", "\n")
cat("\n-- empty-gene row only, remove_empty_rows=TRUE --\n")
rr <- try({ png("out/i3_droprows.png", width=1300, height=400, res=100); ht <- oncoPrint(mat, alter_fun=alter_fun, col=col, remove_empty_rows=TRUE); hd <- draw(ht); dev.off(); rownames(mat)[unlist(row_order(hd))] }, silent=TRUE)
cat("remove_empty_rows=TRUE rows kept:", if (inherits(rr,"try-error")) paste("ERROR:", conditionMessage(attr(rr,"condition"))) else paste(rr, collapse=" "), "\n")

# ---- maftools on the same MAF: denominators when 3 cohort samples are absent from the MAF ----
cat("\n== maftools ==\n")
clin <- read.delim("data/synth_edge_clin.tsv", stringsAsFactors=FALSE)
maf <- read.maf("data/synth_edge.maf", clinicalData=clin, verbose=FALSE)
cat("maftools sample count:", maf@summary$summary[maf@summary$ID=="Samples"], "(cohort truth 30; 27 in MAF; clinicalData has 30)\n")
cat("maftools clinical rows:", nrow(getClinicalData(maf)), "\n")
svglite("out/i3_maftools.svg", width=10, height=5)
rm <- try(oncoplot(maf, genes=c("TP53","KRAS","PIK3CA","MYC","RB1"), removeNonMutated=FALSE, clinicalFeatures="Subtype"), silent=TRUE)
dev.off()
cat("oncoplot(removeNonMutated=FALSE):", if (inherits(rm,"try-error")) paste("ERROR:", conditionMessage(attr(rm,"condition"))) else "ok", "\n")
png("out/i3_maftools.png", width=1000, height=500, res=100); oncoplot(maf, genes=c("TP53","KRAS","PIK3CA","RB1"), removeNonMutated=FALSE, clinicalFeatures="Subtype"); dev.off()
P <- parse_svg("out/i3_maftools.svg"); tx <- P$txt
cat("title / labels:", paste(tx$label[grepl("Altered|%$", tx$label)], collapse=" | "), "\n")
snv_ct <- sapply(c("TP53","KRAS","PIK3CA","RB1"), function(g) length(unique(T$sample[T$gene==g & T$cls!="Amp"])))
cat("independent SNV sample counts:", paste(names(snv_ct), snv_ct, collapse=" "), " -> pct/30:", paste0(round(snv_ct/30*100),"%"), " pct/27:", paste0(round(snv_ct/27*100),"%"), "\n")
e <- try(oncoplot(maf, genes=c("TP53","EMPTYG")), silent=TRUE)
cat("oncoplot with an absent gene:", if (inherits(e,"try-error")) paste("ERROR:", conditionMessage(attr(e,"condition"))) else "ok (see warnings)", "\n")
# maftools pct with removeNonMutated = TRUE vs FALSE (does the denominator move?)
for (rmv in c(TRUE, FALSE)) { f <- paste0("out/i3_mt_", rmv, ".svg"); svglite(f, width=10, height=5)
  oncoplot(maf, genes=c("TP53","KRAS","PIK3CA","RB1"), removeNonMutated=rmv); dev.off()
  t2 <- parse_svg(f)$txt; cat("maftools removeNonMutated=", rmv, ":", paste(t2$label[grepl("Altered|%$", t2$label)], collapse=" | "), "
") }
# maftools somatic multi-hit handling
gs <- getGeneSummary(maf); print(as.data.frame(gs)[1:5, c("Hugo_Symbol","MutatedSamples","total")])
