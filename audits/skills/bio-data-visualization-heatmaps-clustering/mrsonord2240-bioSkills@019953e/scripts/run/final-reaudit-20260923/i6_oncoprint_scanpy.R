# INPUT 6 (scope boundary): OncoPrint request. Skill only says "ComplexHeatmap::oncoPrint() is the R implementation" and defers to another skill.
# REAL TCGA-LAML MAF (maftools extdata, 193 samples). Build gene x sample alteration matrix, oncoPrint, verify against MAF counts.
suppressPackageStartupMessages({library(ComplexHeatmap);library(circlize)})
maf <- read.delim(gzfile("F:/OpenScience/audit-envs/data-visualization/public-data/mutations/tcga_laml.maf.gz"), stringsAsFactors = FALSE)
cat("MAF rows:", nrow(maf), " samples:", length(unique(maf$Tumor_Sample_Barcode)), "\n")
freq <- sort(table(unique(maf[, c("Hugo_Symbol","Tumor_Sample_Barcode")])$Hugo_Symbol), decreasing = TRUE)
genes <- names(freq)[1:12]; print(freq[1:12])
smp <- unique(maf$Tumor_Sample_Barcode)
cls <- ifelse(maf$Variant_Classification %in% c("Missense_Mutation"), "MISSENSE",
      ifelse(maf$Variant_Classification %in% c("Nonsense_Mutation","Frame_Shift_Del","Frame_Shift_Ins","Splice_Site","Translation_Start_Site"), "TRUNC", "INFRAME"))
m <- matrix("", length(genes), length(smp), dimnames = list(genes, smp))
sub <- maf[maf$Hugo_Symbol %in% genes, ]; sub$cls <- cls[maf$Hugo_Symbol %in% genes]
for (i in seq_len(nrow(sub))) { g <- sub$Hugo_Symbol[i]; s <- sub$Tumor_Sample_Barcode[i]; m[g, s] <- paste0(m[g, s], sub$cls[i], ";") }
col <- c(MISSENSE = "#009E73", TRUNC = "#D55E00", INFRAME = "#56B4E9")
alter_fun <- list(background = function(x, y, w, h) grid.rect(x, y, w-unit(0.5,"pt"), h-unit(0.5,"pt"), gp = gpar(fill = "#EEEEEE", col = NA)),
  MISSENSE = function(x, y, w, h) grid.rect(x, y, w-unit(0.5,"pt"), h*0.9, gp = gpar(fill = col["MISSENSE"], col = NA)),
  TRUNC    = function(x, y, w, h) grid.rect(x, y, w-unit(0.5,"pt"), h*0.5, gp = gpar(fill = col["TRUNC"], col = NA)),
  INFRAME  = function(x, y, w, h) grid.rect(x, y, w-unit(0.5,"pt"), h*0.3, gp = gpar(fill = col["INFRAME"], col = NA)))
op <- oncoPrint(m, alter_fun = alter_fun, col = col, remove_empty_columns = TRUE, show_column_names = FALSE, column_title = "TCGA-LAML (real), top 12 genes")
png("i6_oncoprint.png", 1000, 600, res = 100); od <- draw(op); dev.off()
ro <- row_order(od); co <- column_order(od)
cat("row order genes:", rownames(m)[ro], "\n")
cat("row order == descending mutation frequency:", identical(rownames(m)[ro], names(freq)[1:12]) , "\n")
n_alt <- rowSums(m != ""); cat("altered-sample counts per gene (matrix):", n_alt[rownames(m)[ro]], "\n")
cat("matches MAF unique-sample counts:", all(n_alt[names(freq)[1:12]] == as.integer(freq[1:12])), "\n")
# oncoPrint sort order: samples with the top gene mutated come first
mm <- od@ht_list[[1]]@matrix; cn <- colnames(mm)[co]          # drawn column order (matrix after remove_empty_columns)
first <- cn[1:10]; cat("first 10 drawn columns all have", rownames(m)[ro][1], "altered:", all(m[rownames(m)[ro][1], first] != ""), "
")
ntype <- rowSums(sapply(names(col), function(k) rowSums(matrix(grepl(k, m), nrow(m)))>0) ) # sample-level per type not used
cnt_types <- sapply(rownames(m), function(g) sum(sapply(names(col), function(k) sum(grepl(k, m[g, ])))))
cat("sample x type counts:", cnt_types[rownames(m)[ro]], "-> row order == descending sample x type count:", identical(as.character(rownames(m)[ro]), names(sort(cnt_types, decreasing = TRUE))), "
")
cat("drawn columns:", length(cn), " all-altered-samples kept (remove_empty_columns):", all(colSums(m[, cn] != "") > 0), "
")
# claim: 'column_order preserved explicitly': test column_order=argument
op2 <- oncoPrint(m, alter_fun = alter_fun, col = col, column_order = seq_len(ncol(m)), remove_empty_columns = FALSE, show_column_names = FALSE)
pdf(NULL); od2 <- draw(op2); dev.off(); cat("column_order arg honoured:", identical(as.integer(column_order(od2)), seq_len(ncol(m))), "\n")
