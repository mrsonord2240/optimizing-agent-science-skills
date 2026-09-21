# g3viz: SKILL.md block / example section 6 as written, then the working route (readMAF -> g3Lollipop). Checks the JSON embedded in the HTML.
suppressMessages({library(maftools); library(data.table); library(jsonlite); library(g3viz); library(htmlwidgets)})
D <- "F:/OpenScience/audits/bio-data-visualization-lollipop-protein-maps/data/"
setwd("F:/OpenScience/audits/bio-data-visualization-lollipop-protein-maps/run/out")
try_ <- function(label, expr) { cat("\n==== ", label, "\n"); tryCatch(withCallingHandlers(expr, warning=function(w){cat("WARNING:", conditionMessage(w), "\n"); invokeRestart("muffleWarning")}), error=function(e){cat("ERROR:", conditionMessage(e), "\n"); NULL}) }
cat("exists hgvspChange2protein:", exists("hgvspChange2protein"), " | g3viz has:", paste(grep("hgvsp|protein", getNamespaceExports("g3viz"), ignore.case = TRUE, value = TRUE), collapse = ","), "\n")
maf <- read.maf(paste0(D, "synthetic_lollipop.maf"), verbose = FALSE)

# G1: as written in SKILL.md and example
try_("G1 hgvspChange2protein(maf, gene='TP53') as written", {
  mutation_data <- hgvspChange2protein(maf, gene = 'TP53')
})
try_("G1b g3Lollipop.theme(theme.name='nature')", { th <- g3Lollipop.theme(theme.name = 'nature'); cat("theme ok, class:", class(th), "\n") })

# G2: the route that exists: readMAF() on the file, then g3Lollipop()
mut <- try_("G2 readMAF(protein.change.col='HGVSp_Short')", readMAF(paste0(D, "synthetic_lollipop.maf"), protein.change.col = "HGVSp_Short"))
print(head(mut[mut$Hugo_Symbol == "TP53", c("Hugo_Symbol", "HGVSp_Short", "Variant_Classification", "Mutation_Class", "AA_Position")], 8))
cat("AA_Position NA count for TP53:", sum(is.na(mut$AA_Position[mut$Hugo_Symbol == "TP53"])), "\n")
print(mut[mut$Hugo_Symbol == "TP53" & (is.na(mut$AA_Position) | mut$HGVSp_Short %in% c("p.Arg175His","p.=","p.M1?","p.*394Wext*?","p.X125_splice")), c("HGVSp_Short", "Mutation_Class", "AA_Position")][!duplicated(mut$HGVSp_Short[mut$Hugo_Symbol == "TP53" & (is.na(mut$AA_Position) | mut$HGVSp_Short %in% c("p.Arg175His","p.=","p.M1?","p.*394Wext*?","p.X125_splice"))]), ])

w <- try_("G2 g3Lollipop TP53 (nature theme) [may need network for Pfam/UniProt]", {
  g3Lollipop(mut, gene.symbol = "TP53", protein.change.col = "HGVSp_Short", plot.options = g3Lollipop.theme(theme.name = "nature"), output.filename = "G2_TP53_g3viz")
})
cat("html written:", file.exists("G2_TP53_g3viz.html"), " size:", if (file.exists("G2_TP53_g3viz.html")) file.size("G2_TP53_g3viz.html") else NA, "\n")
if (!is.null(w)) {
  x <- w$x
  cat("names(x):", paste(names(x), collapse = ","), "\n")
  d <- x$data
  cat("class(data):", class(d), " n =", length(d), "\n")
  dd <- if (is.character(d)) fromJSON(d) else d
  print(str(dd, max.level = 1));
  if (!is.null(x$domainData)) { cat("domain data / protein length as embedded:\n"); print(x$domainData) }
  if (!is.null(x$transcript)) print(x$transcript)
}
