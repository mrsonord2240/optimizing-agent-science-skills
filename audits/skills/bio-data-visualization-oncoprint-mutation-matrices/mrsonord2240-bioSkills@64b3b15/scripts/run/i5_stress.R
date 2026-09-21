source("helpers.R")
library(svglite)
source("gen_synth_cohort.R")
Tr <- readRDS("data/synth_cohort_truth.rds"); G <- Tr$G; clin <- Tr$clin
col <- SKILL_COL; alter_fun <- get_alter_fun(col)
df <- read_maf_df("data/synth_cohort.maf")
genes <- colnames(G)
top <- names(sort(colSums(G), decreasing=TRUE))[1:12]
long <- maf_to_long(df); allsamp <- clin$Tumor_Sample_Barcode
mat <- build_mat(long, top, allsamp)
# independent truth: from the planted logical matrix G
cat("mat (from MAF) altered/not equals planted G on top-12 genes:", all((mat!="") == t(G[allsamp, top])), "
")
cat("multi-class cells in mat:", sum(grepl(";", mat)), "\n")

# --- variant A: clinical exactly as in the Skill: a data.frame with subtype/stage/tmb, row order = MAF order, NOT the column order of mat ---
clinical <- data.frame(subtype=clin$subtype, stage=clin$stage, tmb=clin$tmb)
cat("mat columns == clinical order (Skill never says they must be aligned):", identical(colnames(mat), clin$Tumor_Sample_Barcode), "\n")
subcol <- c(Luminal='#0072B2', Basal='#D55E00', HER2='#009E73'); stcol <- c(I='#FFFFCC', II='#FED976', III='#FD8D3C', IV='#BD0026')
run_example <- function(mat, clinical, tag, split=NULL) {
  ha_top <- HeatmapAnnotation(
      TMB     = anno_barplot(log10(clinical$tmb + 1), gp = gpar(fill = '#56B4E9', col = NA),
                              axis_param = list(at = log10(c(1, 10, 100, 1000) + 1), labels = c('1', '10', '100', '1000'))),
      Subtype = clinical$subtype, Stage = clinical$stage,
      col = list(Subtype = subcol, Stage = stcol), annotation_name_gp = gpar(fontsize = 8), show_legend = TRUE)
  ht <- oncoPrint(mat, alter_fun = alter_fun, col = col, top_annotation = ha_top, column_title = 'synthetic cohort (N=600)',
                  row_names_gp = gpar(fontsize = 8), pct_gp = gpar(fontsize = 7), show_pct = TRUE, remove_empty_columns = FALSE, remove_empty_rows = FALSE,
                  column_split = split, heatmap_legend_param = list(title = 'Alteration', at = names(col), labels = names(col)))
  f <- paste0("out/i5_", tag, ".svg"); svglite(f, width=30, height=8); hd <- draw(ht, heatmap_legend_side='right', annotation_legend_side='right'); dev.off()
  png(paste0("out/i5_", tag, ".png"), width=2400, height=800, res=100); draw(ht); dev.off()
  list(hd=hd, f=f)
}
check <- function(res, mat, truth_sub, tag, truth_tmb) {
  hd <- res$hd; ro <- unlist(row_order(hd)); co <- unlist(column_order(hd))
  D <- decode_cells(res$f, col)
  cm <- sum(norm_cell(as.vector(mat[ro, co])) != norm_cell(as.vector(D$cells)))
  cat("[", tag, "] cols", length(co), "cell mismatches vs matrix:", cm, "of", length(ro)*length(co), "\n")
  # subtype strip -> column (by x)
  R <- D$P$rect; R <- R[!is.na(R$fill),]; bw <- median(D$bg$w)
  strip <- R[R$fill %in% toupper(subcol) & R$w > bw+0.3 & R$w < bw+3 & R$cy < min(D$bg$cy)-1 & R$cx >= min(D$xs)-1 & R$cx <= max(D$xs)+1,]
  inv <- setNames(names(subcol), toupper(subcol)); ci <- sapply(strip$cx, function(v) which.min(abs(D$xs - v)))
  drawn <- rep(NA_character_, length(co)); drawn[ci] <- inv[strip$fill]
  cat("[", tag, "] annotation strip vs TRUE subtype of the sample drawn in that column: mismatches", sum(drawn != truth_sub[colnames(mat)[co]], na.rm=TRUE), "of", length(co), "\n")
  # TMB bar heights (fill #56B4E9, above body)
  bars <- R[R$fill=="#56B4E9" & R$cy < min(D$bg$cy)-1 & R$cx >= min(D$xs)-1 & R$cx <= max(D$xs)+1 & R$w > bw+0.3 & R$w < bw+3,]
  bars <- bars[order(bars$cx),]
  if (nrow(bars) > 0) {
    bi <- sapply(bars$cx, function(v) which.min(abs(D$xs - v))); hgt <- rep(0, length(co)); hgt[bi] <- bars$h
    exp_h <- log10(truth_tmb[colnames(mat)[co]] + 1)
    cat("[", tag, "] TMB bars found:", nrow(bars), " cor(bar height, log10(true TMB+1)) =", round(cor(hgt, exp_h), 4),
        " | tallest bar / median bar =", round(max(hgt)/median(hgt[hgt>0]), 2), "(linear TMB would give", round(max(truth_tmb)/median(truth_tmb),1), ")\n")
  } else cat("[", tag, "] no TMB bars found\n")
  invisible(D)
}
true_sub <- setNames(clin$subtype, clin$Tumor_Sample_Barcode); true_tmb <- setNames(clin$tmb, clin$Tumor_Sample_Barcode)
cat("== A: clinical NOT aligned to mat columns ==\n")
# make mat columns come in a different order than clinical (e.g. sorted ids), the natural result of a pivot
matS <- mat[, sort(colnames(mat))]
resA <- run_example(matS, clinical, "A_unaligned")
check(resA, matS, true_sub, "A unaligned", true_tmb)
cat("== B: clinical aligned (clinical[colnames(mat),]) ==\n")
clinB <- clinical; rownames(clinB) <- clin$Tumor_Sample_Barcode; clinB <- clinB[colnames(matS),]
resB <- run_example(matS, clinB, "B_aligned")
check(resB, matS, true_sub, "B aligned", true_tmb)
cat("== C: column_split by subtype (aligned) ==\n")
resC <- run_example(matS, clinB, "C_split", split=clinB$subtype)
hdC <- resC$hd; coC <- column_order(hdC)
cat("[C] split panels:", paste(names(coC), sapply(coC, length), collapse=" | "), "\n")
cat("[C] every column in each panel has that panel's TRUE subtype:", all(sapply(names(coC), function(n) all(true_sub[colnames(matS)[coC[[n]]]]==n))), "\n")
check(resC, matS, true_sub, "C split", true_tmb)
# per-panel pct: the split panels' pct labels are still cohort-wide?
DC <- decode_cells(resC$f, col); pc <- DC$P$txt[grepl("%$", DC$P$txt$label),]; pc <- pc[order(pc$y),]
cat("[C] pct labels:", head(pc$label, 12), "\n")
exp_pct <- paste0(round(rowSums(matS!="")/600*100), "%"); ro <- unlist(row_order(hdC)); cat("[C] expected cohort pct in drawn order:", exp_pct[ro], "\n")
# hypermutators
cat("hypermutator TMBs:", sort(true_tmb, decreasing=TRUE)[1:4], " median:", median(true_tmb), "\n")

# --- Skill step 6: read.maf(maf='cohort.maf', clinicalData = clinical) where clinical is the Skill's data.frame (no Tumor_Sample_Barcode column) ---
file.copy("data/synth_cohort.maf", "cohort.maf", overwrite=TRUE)
e <- try(read.maf(maf = 'cohort.maf', clinicalData = clinical, verbose=FALSE), silent=TRUE)
cat("read.maf(clinicalData = Skill-shaped clinical):", if (inherits(e,"try-error")) paste("ERROR:", trimws(conditionMessage(attr(e,"condition")))) else "ok", "\n")
e2 <- try(read.maf(maf='cohort.maf', clinicalData=data.frame(Tumor_Sample_Barcode=clin$Tumor_Sample_Barcode, subtype=clin$subtype, stage=clin$stage, tmb=clin$tmb), verbose=FALSE), silent=TRUE)
cat("read.maf with Tumor_Sample_Barcode added:", if (inherits(e2,"try-error")) "ERROR" else "ok", "\n")
saveRDS(list(mat=mat, matS=matS, clinical=clinical), "out/i5_objects.rds")
