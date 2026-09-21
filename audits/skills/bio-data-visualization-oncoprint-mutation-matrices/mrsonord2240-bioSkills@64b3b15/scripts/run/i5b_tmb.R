source("helpers.R")
P <- parse_svg("out/i5_B_aligned.svg"); R <- P$rect; R <- R[!is.na(R$fill),]
D <- decode_cells("out/i5_B_aligned.svg", SKILL_COL)
b <- R[R$fill=="#56B4E9" & R$cy < min(D$bg$cy)-1,]
cat("rects #56B4E9 above body:", nrow(b), " widths:", paste(head(sort(unique(round(b$w,2))),5), collapse=","), "\n")
Tr <- readRDS("data/synth_cohort_truth.rds"); clin <- Tr$clin; tmb <- setNames(clin$tmb, clin$Tumor_Sample_Barcode)
obj <- readRDS("out/i5_objects.rds"); matS <- obj$matS
hd_order <- NULL
# ordering of columns: rebuild via oncoPrint again (same call) and read column_order
library(ComplexHeatmap); library(circlize)
clinB <- obj$clinical; rownames(clinB) <- clin$Tumor_Sample_Barcode; clinB <- clinB[colnames(matS),]
ht <- oncoPrint(matS, alter_fun=get_alter_fun(SKILL_COL), col=SKILL_COL, remove_empty_columns=FALSE); hd <- draw(ht)
co <- unlist(column_order(hd))
bar <- b[abs(b$w - median(b$w)) < 0.5,]; bi <- sapply(bar$cx, function(v) which.min(abs(D$xs - v)))
h <- rep(0, length(co)); h[bi] <- bar$h
exp <- log10(tmb[colnames(matS)[co]] + 1)
cat("bars matched:", length(bi), "cor(height, log10(TMB+1)) =", round(cor(h, exp), 4), " cor(height, linear TMB) =", round(cor(h, tmb[colnames(matS)[co]]), 4), "\n")
cat("tallest/median bar:", round(max(h)/median(h[h>0]),2), " vs log10 expectation:", round(max(exp)/median(exp),2), " linear:", round(max(tmb)/median(tmb),1), "\n")
