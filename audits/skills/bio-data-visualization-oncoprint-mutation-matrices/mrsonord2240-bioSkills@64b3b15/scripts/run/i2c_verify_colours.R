source("helpers.R")
DV <- Sys.getenv("DV")
df <- read_maf_df(file.path(DV, "public-data/mutations/tcga_laml.maf.gz"))
vc <- maftools:::get_vcColors(); vc <- setNames(substr(toupper(vc),1,7), names(vc))
nonsil <- df[!df$Variant_Classification %in% c("Silent","Intron","RNA","IGR","3'UTR","5'UTR","3'Flank","5'Flank"),]
P <- parse_svg("out/i2.svg"); R <- P$rect; R <- R[!is.na(R$fill),]
tx <- P$txt; g_all <- unique(df$Hugo_Symbol)
gl <- tx[tx$label %in% g_all,]; gl <- gl[order(gl$y),]
# body rect rows: cells whose cy is within +-6px of a gene label baseline-ish (label y is baseline; cell centre is ~ y-4). use nearest-row assignment on rects of narrow width
bodyw <- as.numeric(names(sort(table(round(R$w,2)), decreasing=TRUE))[1]); cat("modal rect width", bodyw, "\n")
cells <- R[abs(R$w-bodyw)<0.05 & R$x < 1010 & R$y > 15 & R$y < 700,]
# svg is 14x8in = 1008x576 px; rows are ~ 20; map each rect to a gene row by nearest label
cells$row <- sapply(cells$cy, function(v) which.min(abs((gl$y-3) - v)))
cells$gene <- gl$label[cells$row]
ok <- 0; bad <- 0; report <- list()
for (g in gl$label) {
  d <- nonsil[nonsil$Hugo_Symbol==g,]
  per <- split(d$Variant_Classification, d$Tumor_Sample_Barcode)
  exp_cols <- sapply(per, function(z) if (length(z)>1) vc["Multi_Hit"] else vc[z])
  exp_tab <- table(exp_cols)
  got <- cells[cells$gene==g & !(cells$fill %in% c("#ECF0F1","#FFFFFF","#E5E5E5")),]
  # tiles narrower in height may be split; count distinct cx per fill
  got_tab <- table(tapply(got$cx, got$fill, function(z) length(unique(round(z,1)))))
  gt <- sapply(split(round(got$cx,1), got$fill), function(z) length(unique(z)))
  e <- as.integer(exp_tab); names(e) <- names(exp_tab)
  same <- all(sort(names(e))==sort(names(gt))) && all(e[names(gt)]==gt[names(gt)])
  if (same) ok <- ok+1 else { bad <- bad+1; cat("MISMATCH", g, "expected", paste(names(e), e, collapse=" "), "| drawn", paste(names(gt), gt, collapse=" "), "\n") }
}
cat("gene rows whose drawn colour counts equal the independent per-class/multi-hit counts:", ok, "of", ok+bad, "\n")
mh <- sum(sapply(gl$label, function(g) { d <- nonsil[nonsil$Hugo_Symbol==g,]; sum(table(d$Tumor_Sample_Barcode)>1) }))
cat("independent multi-hit (gene,sample) pairs in top20:", mh, "\n")
