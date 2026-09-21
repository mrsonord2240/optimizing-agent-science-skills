# maftools lollipopPlot on the SYNTHETIC TP53/KRAS cohort (planted hotspots + edge-case HGVSp strings).
# Ground truth = data/synthetic_truth.json (independent regex + counts made in 01_make_synthetic.py).
suppressMessages({library(maftools); library(data.table); library(jsonlite)})
source("F:/OpenScience/audits/bio-data-visualization-lollipop-protein-maps/run/helpers.R")
D <- "F:/OpenScience/audits/bio-data-visualization-lollipop-protein-maps/data/"
setwd("F:/OpenScience/audits/bio-data-visualization-lollipop-protein-maps/run/out")
truth <- fromJSON(paste0(D, "synthetic_truth.json"), simplifyVector = FALSE)
clin <- fread(paste0(D, "synthetic_clinical.tsv"))
maf <- read.maf(maf = paste0(D, "synthetic_lollipop.maf"), clinicalData = clin, verbose = FALSE)
cat("rows in maf@data:", nrow(maf@data), " (file has 300 rows; Silent/Intron are dropped by read.maf default vc_nonSyn)\n")
cat("TP53 rows kept:", nrow(maf@data[Hugo_Symbol == "TP53"]), "\n")

class_col <- c(Missense_Mutation='#D55E00', Nonsense_Mutation='#000000', Frame_Shift_Del='#0072B2', Frame_Shift_Ins='#56B4E9',
               Splice_Site='#CC79A7', In_Frame_Del='#009E73', In_Frame_Ins='#F0E442')

svglite("S1_tp53_maftools.svg", width = 40, height = 6)
r <- lollipopPlot(maf = maf, gene = 'TP53', AACol = 'HGVSp_Short', labelPos = c(175, 248, 273), labPosSize = 1.0, showMutationRate = TRUE,
                  domainLabelSize = 1, printCount = TRUE, colors = class_col)
dev.off()
cat("\nmaftools returned table (by pos + change):\n"); print(r[order(-count)], nrows = 60)
png("S1_tp53_maftools.png", 2000, 700, res = 200)
lollipopPlot(maf = maf, gene = 'TP53', AACol = 'HGVSp_Short', labelPos = c(175, 248, 273), labPosSize = 1.0, printCount = TRUE, colors = class_col)
dev.off()

p <- svg_parse("S1_tp53_maftools.svg"); cal <- svg_calib(p); pts <- svg_points(p, cal)
pts <- pts[!is.na(height) & abs(height - round(height)) < 0.2 & height > 0.5]
pts[, `:=`(pos = round(pos, 1), height = round(height))]
cat("\nDRAWN circles (pos, height, fill):\n"); print(pts[order(-height)][1:14, .(pos, height, r, fill)])

# --- assertion 1: every truth (position, change) appears as a drawn circle at that position with height == count of mutations with that change
tt <- rbindlist(lapply(names(truth$TP53), function(pp) { v <- truth$TP53[[pp]]
  rbindlist(lapply(names(v$changes), function(ch) data.table(pos = as.integer(pp), change = ch, n = v$changes[[ch]], klass = names(v$classes)[1]))) }))
tt[, short := sub("^p\\.", "", change)]
cat("\nTruth top by change:\n"); print(tt[order(-n)][1:8])
res <- merge(tt, r[, .(pos, conv, count, Variant_Classification)], by.x = c("pos", "short"), by.y = c("pos", "conv"), all = TRUE)
cat("\nMerge truth vs maftools table (rows where they disagree):\n")
print(res[is.na(n) | is.na(count) | n != count])
# drawn geometry check on the biggest three
for (pp in c(175, 248, 273)) {
  dr <- pts[abs(pos - pp) < 0.6][order(-height)]
  cat(sprintf("pos %d: drawn heights %s | truth by-change %s | truth mutations %d | truth samples %d\n", pp,
              paste(dr$height, collapse = "+"), paste(names(truth$TP53[[as.character(pp)]]$changes), unlist(truth$TP53[[as.character(pp)]]$changes), sep = "=", collapse = ","),
              truth$TP53[[as.character(pp)]]$mutations, truth$TP53[[as.character(pp)]]$samples))
}
# colour check: each drawn circle at a truth position should carry class_col of its class
chk <- merge(pts[, .(pos = round(pos), height, fill)], tt[, .(pos, n, klass)], by.x = c("pos", "height"), by.y = c("pos", "n"))
chk[, expect := toupper(class_col[klass])]
cat("\nColour check: ", sum(chk$fill == chk$expect), "/", nrow(chk), " circles carry the class colour; mismatches:\n"); print(chk[fill != expect])
cat("Classes in data with no entry in the Skill's palette:", paste(setdiff(unique(maf@data$Variant_Classification), names(class_col)), collapse = ","), "\n")
# domains + protein length as drawn
rc <- p$rect[!grepl("^<", fill) & h > 1 & w > 1 & fill != "#FFFFFF"]
rc[, `:=`(aa_start = round(predict(cal$fx, newdata = data.frame(x = x)), 1), aa_end = round(predict(cal$fx, newdata = data.frame(x = x + w)), 1))]
cat("\nDomain rectangles as drawn (aa):\n"); print(rc[, .(fill, aa_start, aa_end)])
cat("Drawn protein length (last x-axis tick):", tail(cal$xt$label, 1), "\n")
cat("Domain labels drawn:", paste(p$txt[grepl("P53|TAD|tetramer", label), label], collapse = " | "), "\n")
cat("Numeric labels drawn (printCount / labelPos):", paste(p$txt[grepl("^[0-9]+$", label) & anchor != "end" & abs(y - max(y[anchor == "middle"])) > 1, label], collapse = ","), "\n")
