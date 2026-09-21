source("helpers.R")
df <- read_maf_df(file.path(Sys.getenv("DV"), "public-data/mutations/tcga_laml.maf.gz")); long <- maf_to_long(df); allsamp <- sort(unique(df$Tumor_Sample_Barcode))
cnt <- sort(tapply(long$Tumor_Sample_Barcode, long$Hugo_Symbol, function(z) length(unique(z))), decreasing=TRUE); genes <- names(cnt)[1:20]
mat <- build_mat(long, genes, allsamp)
ht <- oncoPrint(mat, alter_fun=get_alter_fun(SKILL_COL), col=SKILL_COL, remove_empty_columns=FALSE); hd <- draw(ht)
ro <- unlist(row_order(hd)); co <- unlist(column_order(hd))
B <- (mat[ro, co] != "") * 1
score <- apply(B, 2, function(v) sum(v * 2^(rev(seq_along(v)) - 1)))
cat("memo-sort: binary-pattern score (rows in drawn order) non-increasing across drawn columns:", !is.unsorted(rev(score)), "\n")
ev <- sapply(rownames(mat), function(g) sum(lengths(strsplit(mat[g,], ";")))); sc <- rowSums(mat!="")
cat("drawn row order == order by alteration EVENTS (type counts):", identical(rownames(mat)[ro], names(sort(ev, decreasing=TRUE))), "| == order by mutated SAMPLES:", identical(rownames(mat)[ro], names(sort(sc, decreasing=TRUE))), "\n")
cat("rows where samples-order and drawn order disagree:", paste(rownames(mat)[ro][rownames(mat)[ro] != names(sort(sc, decreasing=TRUE))], collapse=" "), "\n")
n1 <- sum(B[1,]); cat("top drawn row (", rownames(mat)[ro][1], "): altered samples", n1, "| all occupy the first", n1, "columns:", all(B[1, seq_len(n1)] == 1), "\n")
# second row within the non-altered block of row 1 and within the altered block: contiguity of leading altered columns
blk <- B[2, B[1,]==1]; cat("row 2 within row-1-altered block: altered samples come first:", !is.unsorted(rev(blk)), "\n")
blk0 <- B[2, B[1,]==0]; cat("row 2 within row-1-unaltered block: altered samples come first:", !is.unsorted(rev(blk0)), "\n")
