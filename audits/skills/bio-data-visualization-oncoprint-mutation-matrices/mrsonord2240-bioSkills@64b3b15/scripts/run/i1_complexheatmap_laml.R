source("helpers.R")
library(svglite)
DV <- Sys.getenv("DV")
df <- read_maf_df(file.path(DV, "public-data/mutations/tcga_laml.maf.gz"))
ann <- read.delim(file.path(DV, "public-data/mutations/tcga_laml_annot.tsv"), stringsAsFactors=FALSE)
cat("MAF rows", nrow(df), "samples", length(unique(df$Tumor_Sample_Barcode)), "annot rows", nrow(ann), "\n")
long <- maf_to_long(df)
allsamp <- sort(unique(df$Tumor_Sample_Barcode))
cnt <- sort(tapply(long$Tumor_Sample_Barcode, long$Hugo_Symbol, function(z) length(unique(z))), decreasing=TRUE); genes <- names(cnt)[1:20]
cat("top20 by mutated samples (non-silent, my class map):", paste0(names(cnt)[1:20],":",cnt[1:20]), "\n")
mat <- build_mat(long, genes, allsamp)
clinical <- data.frame(subtype = ann$FAB_classification[match(colnames(mat), ann$Tumor_Sample_Barcode)],
                       stage = ifelse(ann$Overall_Survival_Status[match(colnames(mat), ann$Tumor_Sample_Barcode)]==1,"Dead","Alive"),
                       tmb = as.numeric(table(factor(long$Tumor_Sample_Barcode, levels=colnames(mat)))), stringsAsFactors=FALSE)
# ---- Skill code, adapted only for data (FAB / vital status instead of Luminal/Stage) ----
col <- SKILL_COL; alter_fun <- get_alter_fun(col)
fabcol <- c(M0='#0072B2', M1='#D55E00', M2='#009E73', M3='#F0E442', M4='#CC79A7', M5='#56B4E9', M6='#999999', M7='#E69F00')
ha_clin <- HeatmapAnnotation(
    Subtype = clinical$subtype, Stage = clinical$stage,
    col = list(Subtype = fabcol, Stage = c(Alive='#FFFFCC', Dead='#BD0026')))
ht <- oncoPrint(mat, alter_fun = alter_fun, col = col, top_annotation = ha_clin, column_title = 'TCGA-LAML mutation landscape',
          row_names_gp = gpar(fontsize = 8), pct_gp = gpar(fontsize = 7), show_pct = TRUE, remove_empty_columns = FALSE, remove_empty_rows = FALSE)
svglite("out/i1.svg", width=40, height=9); hd <- draw(ht); dev.off()
png("out/i1.png", width=2400, height=900, res=100); draw(ht); dev.off()
ro <- unlist(row_order(hd)); co <- unlist(column_order(hd))
cat("drawn gene order   :", rownames(mat)[ro], "\n")
cat("input (count desc) :", genes, "\n")
cnt_drawn <- rowSums(mat!="")[ro]; cat("counts along drawn order:", cnt_drawn, "\n non-increasing:", !is.unsorted(rev(cnt_drawn)), "\n")
cat("n columns drawn:", length(co), " cohort N:", length(allsamp), "\n")
D <- decode_cells("out/i1.svg", col)
cat("decoded grid", nrow(D$cells), "x", ncol(D$cells), "\n")
exp <- mat[ro, co]; got <- D$cells
mism <- sum(norm_cell(as.vector(exp)) != norm_cell(as.vector(got))); cat("cell mismatches (drawn vs matrix in drawn order):", mism, "of", length(exp), "\n")
cat("multi-class cells: matrix", sum(grepl(";", mat)), " drawn", sum(grepl(";", got)), "\n")
print(table(unlist(strsplit(as.vector(mat), ";"))))
print(table(unlist(strsplit(as.vector(got), ";"))))
tx <- D$P$txt; pc <- tx[grepl("^[0-9]+%$", tx$label),]; pc <- pc[order(pc$y),]
cat("pct labels top->bottom  :", pc$label, "\n")
cat("expected round(n/193*100):", paste0(round(cnt_drawn/length(allsamp)*100),"%"), "\n")
# annotation mapping: FAB strip colour per column vs sample FAB
R <- D$P$rect
R <- R[!is.na(R$fill),]
strip <- R[R$fill %in% toupper(fabcol) & R$w > median(D$bg$w)+0.5 & R$w < median(D$bg$w)+3 & R$cy < min(D$bg$cy) - 1 & R$cx >= min(D$xs)-1 & R$cx <= max(D$xs)+1,]
strip <- strip[order(strip$cx),]
cat("subtype strip rects:", nrow(strip), "\n")
inv <- setNames(names(fabcol), toupper(fabcol))
colidx <- sapply(strip$cx, function(v) which.min(abs(D$xs - v)))
drawn_fab <- rep(NA_character_, length(co)); drawn_fab[colidx] <- inv[strip$fill]
exp_fab <- clinical$subtype[co]
cat("columns with NA subtype in clinical:", sum(is.na(exp_fab)), " (", colnames(mat)[co][is.na(exp_fab)], ")
")
cat("subtype strip mismatches vs expected (by sample in drawn order):", sum(drawn_fab != exp_fab, na.rm=TRUE), "of", sum(!is.na(exp_fab)), " NA-consistency:", identical(is.na(drawn_fab), is.na(exp_fab)), "
")
# TMB-like check not applicable here (Skill's block 1 has no TMB); report the default top bar exists in the drawn object? no - top_annotation was overridden.
