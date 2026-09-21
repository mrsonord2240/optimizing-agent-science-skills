# lollipopPlot2 (two cohorts, one up / one down): SKILL.md block 2 and example block 4, on synthetic subtype cohorts and on LAML.
suppressMessages({library(maftools); library(data.table); library(jsonlite)})
source("F:/OpenScience/audits/bio-data-visualization-lollipop-protein-maps/run/helpers.R")
D <- "F:/OpenScience/audits/bio-data-visualization-lollipop-protein-maps/data/"
setwd("F:/OpenScience/audits/bio-data-visualization-lollipop-protein-maps/run/out")
try_ <- function(label, expr) { cat("\n==== ", label, "\n"); tryCatch(withCallingHandlers(expr, warning=function(w){cat("WARNING:", conditionMessage(w), "\n"); invokeRestart("muffleWarning")}), error=function(e){cat("ERROR:", conditionMessage(e), "\n"); NULL}) }
class_col <- c(Missense_Mutation='#D55E00', Nonsense_Mutation='#000000', Frame_Shift_Del='#0072B2', Frame_Shift_Ins='#56B4E9', Splice_Site='#CC79A7', In_Frame_Del='#009E73', In_Frame_Ins='#F0E442')
clin <- fread(paste0(D, "synthetic_clinical.tsv"))
maf <- read.maf(paste0(D, "synthetic_lollipop.maf"), clinicalData = clin, verbose = FALSE)

# Example block 4 as written: subsetMaf(clinQuery = 'Subtype == "Luminal"')
maf_lumin <- subsetMaf(maf, clinQuery = 'Subtype == "Luminal"', verbose = FALSE)
maf_basal <- subsetMaf(maf, clinQuery = 'Subtype == "Basal"', verbose = FALSE)
cat("Luminal samples:", as.numeric(maf_lumin@summary[ID == "Samples", summary]), " Basal samples:", as.numeric(maf_basal@summary[ID == "Samples", summary]), "\n")

svglite("P2_tp53_subtype.svg", width = 40, height = 8)
r2 <- try_("lollipopPlot2 as in example (colors=class_col)", lollipopPlot2(m1 = maf_lumin, m2 = maf_basal, gene = 'TP53', m1_name = 'Luminal', m2_name = 'Basal',
              AACol1 = 'HGVSp_Short', AACol2 = 'HGVSp_Short', colors = class_col))
dev.off()
png("P2_tp53_subtype.png", 2000, 1000, res = 200)
try_("png", lollipopPlot2(m1 = maf_lumin, m2 = maf_basal, gene = 'TP53', m1_name = 'Luminal', m2_name = 'Basal', AACol1 = 'HGVSp_Short', AACol2 = 'HGVSp_Short', colors = class_col))
dev.off()
cat("class of return:", class(r2), "\n")

# independent counts per cohort straight from the files
m <- fread(paste0(D, "synthetic_lollipop.maf")); m <- merge(m, clin, by = "Tumor_Sample_Barcode")
for (sb in c("Luminal", "Basal")) {
  x <- m[Hugo_Symbol == "TP53" & Subtype == sb & HGVSp_Short %in% c("p.R175H", "p.R248Q", "p.R273H", "p.R248W")]
  cat(sb, "independent counts:", paste(x[, .N, by = HGVSp_Short][order(HGVSp_Short)][, paste0(HGVSp_Short, "=", N)], collapse = ", "), "\n")
}
# drawn geometry: read (position, height) of every circle from the SVG. Two panels, each with a linear y axis labelled only at 1 and max.
p <- svg_parse("P2_tp53_subtype.svg")
ye <- p$txt[anchor == "end" & grepl("^[0-9]+$", label)][order(y)]
cat("y-axis labels:", paste(ye$label, "@", round(ye$y, 1), collapse = "; "), "
")
# x axis: bar spans aa 0..393; use the drawn bar rect (grey) edges
bar <- p$rect[grepl("#95A5A6", fill)]
x0 <- bar$x[1]; x1 <- bar$x[1] + bar$w[1]
cat("grey backbone drawn from x =", x0, "to", x1, "(=> aa 0..393)
")
fx <- function(x) (x - x0) / (x1 - x0) * 393
up <- ye[1:2]; lo <- ye[3:4]   # upper: max then 1 ; lower: 1 then max
hu <- function(cy) { y1 <- up$y[2] - 3.56; ym <- up$y[1] - 3.56; 1 + (y1 - cy) / (y1 - ym) * (as.numeric(up$label[1]) - 1) }
hl <- function(cy) { y1 <- lo$y[1] - 3.56; ym <- lo$y[2] - 3.56; 1 + (cy - y1) / (ym - y1) * (as.numeric(lo$label[2]) - 1) }
cc <- p$circ[cy < lo$y[2] + 5]           # drop the legend markers below the lower panel
cat("circle radii:", paste(sort(unique(round(p$circ$r, 2))), collapse = ","), "
")
mid <- (up$y[2] + lo$y[1]) / 2 - 3.56
cc[, `:=`(pos = fx(cx), panel = ifelse(cy < mid, "up", "down"))]
cc[, height := ifelse(panel == "up", hu(cy), hl(cy))]
cc[, `:=`(pos = round(pos), height = round(height))]
big <- cc[height >= 5][order(panel, -height)]
print(big[, .(panel, pos, height, fill)])
cat("Drawn vs independent counts (pos 175/248/273 by cohort):
")
for (pp in c(175, 248, 273)) for (pn in c("up", "down"))
  cat(sprintf("  %s pos %d heights: %s
", ifelse(pn == "up", "Luminal", "Basal"), pp, paste(cc[panel == pn & abs(pos - pp) <= 1, height], collapse = "+")))
# LAML: the two blocks the Skill asks for with a real cohort split by FAB
laml <- read.maf("F:/OpenScience/audit-envs/data-visualization/public-data/mutations/tcga_laml.maf.gz",
                 clinicalData = "F:/OpenScience/audit-envs/data-visualization/public-data/mutations/tcga_laml_annot.tsv", verbose = FALSE)
print(head(getClinicalData(laml), 3))
fab <- getClinicalData(laml)
lo <- subsetMaf(laml, clinQuery = "FAB_classification %in% c('M0','M1','M2')", verbose = FALSE)
hi <- subsetMaf(laml, clinQuery = "FAB_classification %in% c('M4','M5')", verbose = FALSE)
png("P2_laml_dnmt3a.png", 2000, 1000, res = 200)
try_("LAML lollipopPlot2 DNMT3A M0-M2 vs M4-M5 (AACol1 = HGVSp_Short as written)", lollipopPlot2(m1 = lo, m2 = hi, gene = 'DNMT3A', m1_name = 'M0-M2', m2_name = 'M4-M5', AACol1 = 'HGVSp_Short', AACol2 = 'HGVSp_Short'))
dev.off()
png("P2_laml_dnmt3a_ok.png", 2000, 1000, res = 200)
try_("LAML lollipopPlot2 DNMT3A with Protein_Change", lollipopPlot2(m1 = lo, m2 = hi, gene = 'DNMT3A', m1_name = 'M0-M2', m2_name = 'M4-M5', AACol1 = 'Protein_Change', AACol2 = 'Protein_Change'))
dev.off()
mm <- fread("F:/OpenScience/audit-envs/data-visualization/public-data/mutations/tcga_laml.maf.gz")
an <- fread("F:/OpenScience/audit-envs/data-visualization/public-data/mutations/tcga_laml_annot.tsv")
mm <- merge(mm, an[, .(Tumor_Sample_Barcode, FAB_classification)], by = "Tumor_Sample_Barcode")
cat("independent R882H by FAB group: M0-M2 =", mm[Hugo_Symbol=="DNMT3A" & Protein_Change=="p.R882H" & FAB_classification %in% c("M0","M1","M2"), .N],
    " M4-M5 =", mm[Hugo_Symbol=="DNMT3A" & Protein_Change=="p.R882H" & FAB_classification %in% c("M4","M5"), .N], "\n")
