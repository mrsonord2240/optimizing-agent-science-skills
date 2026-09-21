# trackViewer::lolliplot: SKILL.md block (as written) and example section 5 (as written) on synthetic TP53, then UniProt-exact domains.
suppressMessages({library(maftools); library(data.table); library(jsonlite); library(trackViewer); library(GenomicRanges)})
source("F:/OpenScience/audits/bio-data-visualization-lollipop-protein-maps/run/helpers.R")
D <- "F:/OpenScience/audits/bio-data-visualization-lollipop-protein-maps/data/"
setwd("F:/OpenScience/audits/bio-data-visualization-lollipop-protein-maps/run/out")
try_ <- function(label, expr) { cat("\n==== ", label, "\n"); tryCatch(withCallingHandlers(expr, warning=function(w){cat("WARNING:", conditionMessage(w), "\n"); invokeRestart("muffleWarning")}), error=function(e){cat("ERROR:", conditionMessage(e), "\n"); NULL}) }

# ---- T1: SKILL.md block as written ----
snps <- GRanges('chr17', IRanges(c(175, 248, 273), width = 1, names = c('R175H', 'R248Q', 'R273H')),
                color = c('#D55E00', '#D55E00', '#D55E00'), score = c(45, 38, 29))
features <- GRanges('chr17', IRanges(c(102, 323, 363), width = c(190, 30, 30), names = c('DNA-binding', 'Tetramerization', 'Regulatory')),
                    fill = c('#0072B2', '#009E73', '#CC79A7'), height = 0.04)
cat("SKILL.md domain rows as coded (start-end):\n"); print(as.data.frame(ranges(features)))
png("T1_skillmd_trackviewer.png", 2000, 900, res = 200)
try_("T1 SKILL.md lolliplot as written", lolliplot(snps, features, ylab = 'Mutation count', xaxis = TRUE, yaxis = TRUE))
dev.off()
cat("T1 heights/positions measured from the PNG pixels with 07_png_measure.py (svglite draws grid circles as polygons)\n")

# ---- T2: example block 5 as written (uses a MAF with HGVSp_Short) ----
maf <- read.maf(paste0(D, "synthetic_lollipop.maf"), verbose = FALSE)
mutation_summary <- try_("T2 example mutation_summary (data.table syntax as written)",
  maf@data[Hugo_Symbol == 'TP53', .(count = .N, class = Variant_Classification[1]),
           by = .(aa_pos = as.numeric(sub('p\\.[A-Z](\\d+).*', '\\1', HGVSp_Short)))])
cat("rows:", nrow(mutation_summary), " NA aa_pos rows:", sum(is.na(mutation_summary$aa_pos)), "\n")
print(mutation_summary[order(-count)][1:8]); print(mutation_summary[is.na(aa_pos)])
class_col <- c(Missense_Mutation = '#D55E00', Nonsense_Mutation = '#000000', Frame_Shift_Del = '#0072B2', Frame_Shift_Ins = '#56B4E9',
               Splice_Site = '#CC79A7', In_Frame_Del = '#009E73', In_Frame_Ins = '#F0E442')
snps2 <- try_("T2 GRanges(IRanges(aa_pos)) with NA present", {
  s <- GRanges('chr17', IRanges(mutation_summary$aa_pos, width = 1), color = class_col[mutation_summary$class], score = mutation_summary$count)
  names(s) <- mutation_summary$class; s })
cat("T2 GRanges built:", !is.null(snps2), "\n")
# Independent truth for what the example should produce: one lollipop per position with the position's mutation-row count
truth <- fromJSON(paste0(D, "synthetic_truth.json"), simplifyVector = FALSE)$TP53
tp <- data.table(aa_pos = as.integer(names(truth)), count = sapply(truth, function(v) v$mutations))
ms <- mutation_summary[!is.na(aa_pos)]
cmp <- merge(tp, ms[, .(aa_pos = as.integer(aa_pos), count_example = count, class_first = as.character(class))], by = "aa_pos", all = TRUE)
cat("\nExample position-level counts vs independent position counts, rows that differ:\n"); print(cmp[is.na(count) | is.na(count_example) | count != count_example])
cat("Positions carrying >1 variant class, coloured by class[1] only:\n")
mc <- maf@data[Hugo_Symbol == "TP53", .(n_classes = uniqueN(Variant_Classification)), by = .(pos = as.numeric(sub("p\\.[A-Z](\\d+).*", "\\1", HGVSp_Short)))][n_classes > 1]
print(mc)

# ---- T3: same example after dropping NA rows, UniProt-consistent domains, names = residue labels ----
uni <- fromJSON(paste0(D, "P04637_uniprot.json"), simplifyVector = FALSE)
cat("\nUniProt P04637 length:", uni$sequence$length, "\n")
ft <- Filter(function(f) f$type %in% c("Region", "DNA binding") && f$description %in% c("", "Transcription activation (acidic)", "Oligomerization", "Basic (repression of DNA-binding)") || f$type == "DNA binding", uni$features)
uf <- rbindlist(lapply(ft, function(f) data.table(type = f$type, desc = if (is.null(f$description)) "" else f$description, start = f$location$start$value, end = f$location$end$value)))
print(uf)
# Example's own coded coordinates (from the example file)
ex <- data.table(name = c("TAD", "DNA-binding", "Tetramer", "Reg"), start = c(1, 102, 323, 363), width = c(41, 190, 33, 30))
ex[, end := start + width - 1]
cat("Example domain coordinates as coded (IRanges width semantics):\n"); print(ex)
cat("Example comment claims: TAD 1-42, DNA-binding 102-292, Tetramerization 323-356, Regulatory 363-393\n")
cat("UniProt (P04637 JSON cached 2026-09-20): TAD 1-44, DNA binding 102-292, Oligomerization 325-356, Basic 368-387\n")

feat_ok <- GRanges("chr17", IRanges(c(1, 102, 325, 368), c(44, 292, 356, 387), names = c("TAD", "DNA-binding", "Oligomerization", "Basic")),
                   fill = c('#56B4E9', '#0072B2', '#009E73', '#CC79A7'), height = 0.04)
pal_full <- c(class_col, Translation_Start_Site = '#999999', Nonstop_Mutation = '#E69F00')   # palette extended (the Skill's 7-class palette lacks these two)
tp53_sum <- ms[aa_pos >= 1 & aa_pos <= 393]
snps3 <- GRanges('chr17', IRanges(tp53_sum$aa_pos, width = 1), color = pal_full[as.character(tp53_sum$class)], score = tp53_sum$count)
names(snps3) <- ifelse(tp53_sum$count >= 20, paste0("pos", tp53_sum$aa_pos), "")
png("T3_trackviewer_uniprot.png", 2400, 900, res = 200)
try_("T3 png", lolliplot(snps3, feat_ok, ylab = 'Mutation count', xaxis = TRUE, yaxis = TRUE, legend = list(labels = names(class_col), col = class_col)))
dev.off()
cat("T3 done; heights/positions measured from the PNG pixels with 07_png_measure.py\n")
