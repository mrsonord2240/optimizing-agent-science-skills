# Investigation: SKILL.md's "graphite route" for SPIA (also shipped verbatim as
# examples/kegg_spia_topology.R) fails when run exactly as documented:
#
#   library(graphite)
#   db <- pathways('hsapiens', 'kegg')
#   db <- convertIdentifiers(db, 'ENTREZID')
#   prepareSPIA(db, 'kegg_hsa_spia')                    # <- SKILL.md's literal text has no dir prefix
#   gr <- runSPIA(de=de_vec, all=universe, 'kegg_hsa_spia')
#
# examples/kegg_spia_topology.R additionally routes the pathwaySetName through
# tempdir(): spia_set <- file.path(tempdir(), 'kegg_hsa_spia'); prepareSPIA(db, spia_set);
# runSPIA(de=de_vec, all=universe, spia_set) -- this is the exact pattern that failed in
# gate8/kegg_spia_topology.out with:
#   "There is no dataset corresponding to the pathway set name: <path>/kegg_hsa_spia
#    Did you forget to run prepareSPIA?"
#
# This script isolates two independent, compounding root causes, confirmed against the
# graphite source both as installed here (1.52.0) and as currently published on
# Bioconductor release (graphite 1.56.0, the version SKILL.md's own "Version Compatibility"
# section declares as its compatibility target) -- i.e. this is not a stale-install artifact.

suppressMessages({library(SPIA); library(graphite); library(clusterProfiler); library(org.Hs.eg.db)})

de <- read.csv('gate8/de_results.csv')
sig <- de[de$padj < 0.05, ]
map <- suppressMessages(bitr(sig$gene, 'SYMBOL', 'ENTREZID', org.Hs.eg.db))
de_vec <- setNames(sig$log2FoldChange[match(map$SYMBOL, sig$gene)], map$ENTREZID)
de_vec <- de_vec[!duplicated(names(de_vec))]
universe <- suppressMessages(bitr(de$gene[!is.na(de$pvalue)], 'SYMBOL', 'ENTREZID', org.Hs.eg.db))$ENTREZID

## --- Root cause 1: runSPIA's own path-existence check is broken for an absolute pathwaySetName ---
cat("=== Root cause 1: runSPIA's dir()-based existence check ===\n")
cat("graphite:::datasetName <- function(pathwaySetName) paste(pathwaySetName, 'SPIA.RData', sep='')\n")
cat("graphite:::runSPIA checks: if (!(datasetName(pathwaySetName) %in% dir())) stop(...)\n")
cat("dir() with NO path argument lists ONLY the current working directory's bare filenames.\n")
cat("When pathwaySetName is built via file.path(tempdir(), 'name') (exactly as SKILL.md and\n")
cat("examples/kegg_spia_topology.R both do), datasetName() returns a FULL ABSOLUTE PATH string,\n")
cat("which can never appear in dir()'s bare-filename listing -- so the check fails 100% of the\n")
cat("time, for any data, on any machine, regardless of whether prepareSPIA actually ran.\n\n")

db <- pathways('hsapiens', 'kegg')
db <- convertIdentifiers(db, 'ENTREZID')
td <- tempdir()
spia_set_abs <- file.path(td, 'kegg_hsa_spia_investigate')
prepareSPIA(db, spia_set_abs)
cat("prepareSPIA wrote the file:", file.exists(paste0(spia_set_abs, "SPIA.RData")), "\n")
r_asdocumented <- tryCatch(
  runSPIA(de=de_vec, all=universe, spia_set_abs, nB=50),
  error=function(e) paste("ERROR:", conditionMessage(e)))
cat("runSPIA() exactly as SKILL.md/examples document it:\n  ", 
    if(is.character(r_asdocumented)) r_asdocumented else "unexpectedly succeeded", "\n\n")

## --- Attempted fix: bare relative name + setwd() to the directory holding the file ---
cat("=== Attempted fix: relative pathwaySetName + matching working directory ===\n")
owd <- getwd()
setwd(td)
spia_set_rel <- 'kegg_hsa_spia_investigate_rel'
prepareSPIA(db, spia_set_rel)
r_fixed <- tryCatch(
  runSPIA(de=de_vec, all=universe, spia_set_rel, nB=50),
  error=function(e) paste("ERROR:", conditionMessage(e)))
setwd(owd)
cat("runSPIA() with the path bug worked around:\n  ",
    if(is.character(r_fixed)) r_fixed else paste("no error, but", nrow(r_fixed), "rows returned"), "\n\n")

## --- Root cause 2: even once the path bug is worked around, ID namespaces don't match ---
cat("=== Root cause 2: convertIdentifiers(db, 'ENTREZID') prefixes node IDs ===\n")
p <- db[["Cell cycle"]]
cat("Sample graphite node IDs after convertIdentifiers(db, 'ENTREZID'):\n")
print(head(nodes(p), 5))
cat("Sample de_vec / universe IDs (as SKILL.md's own bitr()-based ID prep produces them):\n")
print(head(names(de_vec), 5))
cat("\nThese never intersect ('ENTREZID:1017' != '1017'), which is why the 'fixed' call above\n")
cat("returns 0 usable rows even once Root cause 1 is worked around -- a second, independent,\n")
cat("compounding defect. Neither SKILL.md nor examples/kegg_spia_topology.R mentions stripping\n")
cat("or adding the 'ENTREZID:' prefix before calling runSPIA/spia with graphite-converted data.\n")
