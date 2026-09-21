# Skill code blocks run on TCGA-LAML (real data shipped in maftools). Each block runs in tryCatch so a failure is logged, not fatal.
suppressMessages({library(maftools); library(data.table)})
source("F:/OpenScience/audits/bio-data-visualization-lollipop-protein-maps/run/helpers.R")
setwd("F:/OpenScience/audits/bio-data-visualization-lollipop-protein-maps/run/out")
maffile <- "F:/OpenScience/audit-envs/data-visualization/public-data/mutations/tcga_laml.maf.gz"
try_ <- function(label, expr) { cat("\n==== ", label, "\n"); r <- tryCatch(withCallingHandlers(expr, warning=function(w){cat("WARNING:", conditionMessage(w), "\n"); invokeRestart("muffleWarning")}), error=function(e){cat("ERROR:", conditionMessage(e), "\n"); NULL}); invisible(r) }
class_col <- c(Missense_Mutation='#D55E00', Nonsense_Mutation='#000000', Frame_Shift_Del='#0072B2', Frame_Shift_Ins='#56B4E9', Splice_Site='#CC79A7', In_Frame_Del='#009E73')

maf <- read.maf(maf = maffile, verbose = FALSE)
cat("HGVSp_Short in maf@data:", 'HGVSp_Short' %in% colnames(maf@data), " ; cols:", paste(colnames(maf@data), collapse=","), "\n")

# L1: SKILL.md block 1 AS WRITTEN (TP53, AACol HGVSp_Short) on the LAML MAF
try_("L1 as written: lollipopPlot TP53 AACol=HGVSp_Short", {
  png("L1_tp53_as_written.png", 1600, 800, res = 200)
  on.exit(dev.off())
  lollipopPlot(maf = maf, gene = 'TP53', AACol = 'HGVSp_Short', labelPos = c(175, 248, 273), labPosSize = 1.0, showMutationRate = TRUE,
               domainLabelSize = 1, printCount = TRUE, colors = class_col)
})
while (dev.cur() > 1) dev.off()

# L2: TP53 with the column that exists
try_("L2 lollipopPlot TP53 AACol=Protein_Change + skill args", {
  png("L2_tp53_protein_change.png", 1600, 800, res = 200)
  r <- lollipopPlot(maf = maf, gene = 'TP53', AACol = 'Protein_Change', labelPos = c(175, 248, 273), labPosSize = 1.0, showMutationRate = TRUE,
               domainLabelSize = 1, printCount = TRUE, colors = class_col)
  dev.off(); print(r)
})
while (dev.cur() > 1) dev.off()

# L3: block 1 with proteinID = 'P04637' (SKILL example "explicit canonical isoform")
try_("L3 example: proteinID='P04637'", {
  png("L3_proteinID_P04637.png", 1600, 800, res = 200)
  lollipopPlot(maf = maf, gene = 'TP53', AACol = 'Protein_Change', proteinID = 'P04637', printCount = TRUE); dev.off()
})
while (dev.cur() > 1) dev.off()
try_("L3b proteinID='NP_000537' (real RefSeq ID)", {
  png("L3b_proteinID_NP000537.png", 1600, 800, res = 200)
  r <- lollipopPlot(maf = maf, gene = 'TP53', AACol = 'Protein_Change', proteinID = 'NP_000537', printCount = TRUE); dev.off(); print(dim(r))
})
while (dev.cur() > 1) dev.off()
try_("L3c refSeqID='NM_001126118' (354 aa isoform)", {
  png("L3c_refseq_isoform.png", 1600, 800, res = 200)
  r <- lollipopPlot(maf = maf, gene = 'TP53', AACol = 'Protein_Change', refSeqID = 'NM_001126118', printCount = TRUE); dev.off(); print(dim(r))
})
while (dev.cur() > 1) dev.off()

# L4: DNMT3A hotspot R882 (19 x R882H, 7 x R882C in LAML): drawn geometry vs independent count from the MAF
m <- fread(maffile)
tr <- m[Hugo_Symbol == "DNMT3A" & Protein_Change != "" , .N, by = Protein_Change]
cat("\nIndependent count from raw MAF (DNMT3A):\n"); print(tr[order(-N)][1:6])
svglite("L4_dnmt3a.svg", width = 40, height = 6)
r <- lollipopPlot(maf, gene = "DNMT3A", AACol = "Protein_Change", labelPos = 882, printCount = TRUE, colors = class_col)
dev.off()
p <- svg_parse("L4_dnmt3a.svg"); cal <- svg_calib(p); pts <- svg_points(p, cal)
cat("x calibration R2:", summary(cal$fx)$r.squared, " x ticks:", paste(cal$xt$label, collapse=","), "\n")
pts <- pts[!is.na(height) & abs(height - round(height)) < 0.15 & height > 0.5]
pts[, `:=`(pos = round(pos, 1), height = round(height, 2))]
print(pts[order(-height)][1:8])
top <- pts[order(-height)][1]
cat(sprintf("DRAWN top lollipop: pos %.1f height %.2f fill %s ; truth: R882H = %d\n", top$pos, top$height, top$fill, tr[Protein_Change=="p.R882H", N]))
cat("drawn point radii unique:", paste(sort(unique(round(p$circ$r, 2))), collapse = ","), " (constant r => size does NOT encode count)\n")
# domain rectangles (protein length + domain boundaries as drawn)
rc <- p$rect[h > 1 & w > 1]; rc[, `:=`(aa_start = predict(cal$fx, newdata=data.frame(x = x)), aa_end = predict(cal$fx, newdata=data.frame(x = x + w)))]
print(rc[, .(fill, aa_start = round(aa_start,1), aa_end = round(aa_end,1))])
cat("Drawn protein length (last x tick):", tail(cal$xt$label, 1), "\n")

