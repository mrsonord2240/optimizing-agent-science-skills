source("helpers.R")
library(svglite)
DV <- Sys.getenv("DV")
mf <- file.path(DV, "public-data/mutations/tcga_laml.maf.gz")
ann <- read.delim(file.path(DV, "public-data/mutations/tcga_laml_annot.tsv"), stringsAsFactors=FALSE)
df <- read_maf_df(mf); long <- maf_to_long(df); allsamp <- sort(unique(df$Tumor_Sample_Barcode))
top <- names(sort(tapply(long$Tumor_Sample_Barcode, long$Hugo_Symbol, function(z) length(unique(z))), decreasing=TRUE))[1:8]
col <- SKILL_COL; alter_fun <- get_alter_fun(col)
msg <- function(e) if (inherits(e,"try-error")) paste("ERROR:", trimws(conditionMessage(attr(e,"condition")))) else "ok"

cat("== 7a: sample IDs differ between MAF (long TCGA barcode) and clinical (short) ==\n")
mat <- build_mat(long, top, allsamp)
mat_long <- mat; colnames(mat_long) <- paste0(colnames(mat), "-03A-01D-0756-08")
sub <- ann$FAB_classification[match(colnames(mat_long), ann$Tumor_Sample_Barcode)]      # the natural match() on the barcode
cat("annotation values matched by ID:", sum(!is.na(sub)), "of", length(sub), "(all NA = silent mismatch)\n")
w <- NULL
r <- try(withCallingHandlers({
  ha <- HeatmapAnnotation(Subtype = sub, col = list(Subtype = c(M0='#0072B2', M1='#D55E00', M2='#009E73', M3='#F0E442', M4='#CC79A7', M5='#56B4E9', M6='#999999', M7='#E69F00')))
  png("out/i7a.png", width=1400, height=450, res=100); draw(oncoPrint(mat_long, alter_fun=alter_fun, col=col, top_annotation=ha, remove_empty_columns=FALSE)); dev.off() },
  warning=function(x) { w <<- c(w, conditionMessage(x)); invokeRestart("muffleWarning") }), silent=TRUE)
cat("oncoPrint with all-NA annotation:", msg(r), "| warnings:", if (is.null(w)) "none" else paste(unique(w), collapse=" || "), "\n")
# maftools with clinical IDs that do not match the MAF
ann_bad <- ann; ann_bad$Tumor_Sample_Barcode <- paste0(ann_bad$Tumor_Sample_Barcode, "-03A")
w2 <- NULL
m <- try(withCallingHandlers(read.maf(mf, clinicalData=ann_bad, verbose=FALSE), warning=function(x){ w2 <<- c(w2, conditionMessage(x)); invokeRestart("muffleWarning")}), silent=TRUE)
cat("read.maf with non-matching clinical IDs:", msg(m), "| warnings:", if (is.null(w2)) "none" else paste(w2, collapse=" || "), "\n")
if (!inherits(m,"try-error")) { cd <- getClinicalData(m); cat("  clinical rows kept:", nrow(cd), " FAB non-NA:", sum(!is.na(cd$FAB_classification)), "\n") }

cat("== 7b: alteration string that is not in col/alter_fun (e.g. an unmapped Variant_Classification) ==\n")
mat2 <- mat; mat2[1, 1:5] <- "Silent"
cat("oncoPrint with unmapped 'Silent' cells:", msg(try(draw(oncoPrint(mat2, alter_fun=alter_fun, col=col)), silent=TRUE)), "\n")
mat3 <- mat; mat3[1, 1:5] <- "missense"     # case mismatch
cat("oncoPrint with 'missense' (case mismatch):", msg(try(draw(oncoPrint(mat3, alter_fun=alter_fun, col=col)), silent=TRUE)), "\n")
# How many LAML rows would a naive 6-class map silently drop?
tab <- table(df$Variant_Classification, useNA="ifany"); mapped <- names(tab) %in% names(CLS)
cat("LAML rows by Variant_Classification not covered by any Skill alteration class (must be decided by the agent):\n"); print(tab[!mapped])

cat("== 7c: request 'drop samples with no mutation so frequencies look bigger' ==\n")
for (rc in c(FALSE, TRUE)) { f <- paste0("out/i7c_", rc, ".svg"); svglite(f, width=30, height=6)
  ht <- oncoPrint(mat, alter_fun=alter_fun, col=col, remove_empty_columns=rc); hd <- draw(ht); dev.off()
  t <- parse_svg(f)$txt; pc <- t[grepl("%$", t$label),]; pc <- pc[order(pc$y),]
  cat("remove_empty_columns =", rc, ": columns", length(unlist(column_order(hd))), "| pct:", paste(pc$label, collapse=" "), "\n") }
cat("altered-only denominator would give:", paste0(round(rowSums(mat[,colSums(mat!="")>0]!="")/sum(colSums(mat!="")>0)*100), "%"), "(top-8 genes; rows in input order)\n")
