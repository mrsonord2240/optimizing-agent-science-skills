# Extras: example section-5 code as written (clean MAF) rendered to PNG; isoform shorter than a mutation; missing gene / no-domain gene / unmutated labelPos;
# and the SKILL's TP53 canonical-isoform claim checked against Ensembl (public read-only REST, if reachable).
suppressMessages({library(maftools); library(data.table); library(trackViewer); library(GenomicRanges); library(jsonlite)})
source("F:/OpenScience/audits/bio-data-visualization-lollipop-protein-maps/run/helpers.R")
setwd("F:/OpenScience/audits/bio-data-visualization-lollipop-protein-maps/run/out")
try_ <- function(label, expr) { cat("\n==== ", label, "\n"); tryCatch(withCallingHandlers(expr, warning=function(w){cat("WARNING:", conditionMessage(w), "\n"); invokeRestart("muffleWarning")}), error=function(e){cat("ERROR:", conditionMessage(e), "\n"); NULL}) }
class_col <- c(Missense_Mutation='#D55E00', Nonsense_Mutation='#000000', Frame_Shift_Del='#0072B2', Frame_Shift_Ins='#56B4E9', Splice_Site='#CC79A7', In_Frame_Del='#009E73', In_Frame_Ins='#F0E442')
maf <- read.maf("F:/OpenScience/audits/bio-data-visualization-lollipop-protein-maps/run/out/ex/clean.maf", verbose = FALSE)

# example section 5 verbatim (clean MAF): names(snps) <- class, then lolliplot with the example's domains and legend
mutation_summary <- maf@data[Hugo_Symbol == 'TP53', .(count = .N, class = Variant_Classification[1]), by = .(aa_pos = as.numeric(sub('p\\.[A-Z](\\d+).*', '\\1', HGVSp_Short)))]
snps <- GRanges('chr17', IRanges(mutation_summary$aa_pos, width = 1), color = class_col[mutation_summary$class], score = mutation_summary$count)
names(snps) <- mutation_summary$class
features <- GRanges('chr17', IRanges(c(1, 102, 323, 363), width = c(41, 190, 33, 30), names = c('TAD', 'DNA-binding', 'Tetramer', 'Reg')),
                    fill = c('#56B4E9', '#0072B2', '#009E73', '#CC79A7'), height = 0.04)
png("E1_example_sec5_trackviewer.png", 2400, 900, res = 200)
try_("E1 example section 5 lolliplot verbatim", lolliplot(snps, features, ylab = 'Mutation count', xaxis = TRUE, yaxis = TRUE, legend = list(labels = names(class_col), col = class_col)))
dev.off()

# I1: isoform shorter than the mutation positions (NM_001126115 = 261 aa; TP53 mutations at 273, 286, 342, 381 lie beyond it)
svglite("I1_short_isoform.svg", width = 30, height = 6)
r <- try_("I1 refSeqID='NM_001126115' (261 aa) with mutations beyond aa 261", lollipopPlot(maf, gene = "TP53", AACol = "HGVSp_Short", refSeqID = "NM_001126115", colors = class_col))
dev.off()
p <- svg_parse("I1_short_isoform.svg"); cal <- svg_calib(p); pts <- svg_points(p, cal)
cat("drawn axis ticks:", paste(cal$xt$label, collapse = ","), "\n")
cat("circles drawn beyond aa 261:", sum(pts$pos > 262, na.rm = TRUE), " of ", sum(!is.na(pts$pos) & pts$r > 3), "; mutations in table beyond 261:", if (!is.null(r)) sum(r$pos > 261) else NA, "\n")
png("I1_short_isoform.png", 2000, 700, res = 200); invisible(try_("png", lollipopPlot(maf, gene = "TP53", AACol = "HGVSp_Short", refSeqID = "NM_001126115", colors = class_col))); dev.off()

# I2: labelPos at a residue with no mutation; gene absent from cohort; gene with no domain table entry
png("I2_label_unmutated.png", 1600, 700, res = 200)
try_("I2 labelPos=c(175, 999) where 999 is beyond the protein", lollipopPlot(maf, gene = "TP53", AACol = "HGVSp_Short", labelPos = c(175, 999)))
dev.off()
try_("I3 gene not in cohort", lollipopPlot(maf, gene = "NOTAGENE", AACol = "HGVSp_Short"))
try_("I4 gene with no mutations in this cohort (BRCA1)", lollipopPlot(maf, gene = "BRCA1", AACol = "HGVSp_Short"))
try_("I5 no AACol given (auto-detect)", { r <- lollipopPlot(maf, gene = "TP53"); cat("auto-detected rows:", nrow(r), "\n") })
try_("I6 colors vector missing a class present in data (drop Missense_Mutation)", {
  png("I6_partial_colors.png", 1600, 700, res = 200); lollipopPlot(maf, gene = "TP53", AACol = "HGVSp_Short", colors = class_col[-1]); dev.off() })

# Ensembl check of the Skill's isoform sentence ("ENST00000269305 vs canonical ENST00000288602 (TP53)")
for (id in c("ENST00000269305", "ENST00000288602")) {
  x <- tryCatch(fromJSON(paste0("https://rest.ensembl.org/lookup/id/", id, "?content-type=application/json")), error = function(e) NULL)
  if (is.null(x)) cat(id, ": Ensembl lookup failed (network)\n") else cat(id, "->", x$display_name, "| gene", x$Parent, "| canonical:", x$is_canonical, "| species", x$species, "\n")
}
