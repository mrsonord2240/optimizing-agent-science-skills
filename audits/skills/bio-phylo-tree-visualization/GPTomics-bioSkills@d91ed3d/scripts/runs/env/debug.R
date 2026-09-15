suppressPackageStartupMessages({library(treeio); library(ggtree); library(ggplot2); library(ape)})
iq <- read.iqtree("../../data/iq/primates16.treefile")
iq_r <- treeio::root(iq, outgroup = c("Microcebus_murinus", "Otolemur_garnettii"), edgelabel = TRUE)
cat("rooted tip labels:", head(as.phylo(iq_r)$tip.label, 4), "\n")
splitkey <- function(tips, all) { s <- sort(tips); o <- sort(setdiff(all, tips)); if (length(o) < length(s) || (length(o)==length(s) && o[1] < s[1])) s <- o; paste(s, collapse=",") }
smap <- function(td) { ph <- as.phylo(td); tb <- as_tibble(td); all <- ph$tip.label; out <- c()
  for (i in which(tb$node > Ntip(ph) & !is.na(tb$UFboot))) { n <- tb$node[i]
    tips <- ph$tip.label[unlist(phangorn::Descendants(ph, n, "tips"))]
    out[splitkey(tips, all)] <- paste0(tb$SH_aLRT[i], "/", tb$UFboot[i]) }
  out }
before <- smap(iq); after <- smap(iq_r)
k <- union(names(before), names(after))
cmp <- data.frame(split = substr(k, 1, 60), before = before[k], after = after[k], row.names = NULL)
print(cmp); cat("mismatched splits after treeio::root(edgelabel=TRUE):", sum(cmp$before != cmp$after | is.na(cmp$before) | is.na(cmp$after)), "\n")
cat("MRCA via tidytree on treedata:\n"); print(tryCatch(MRCA(iq_r, "Homo_sapiens", "Macaca_mulatta"), error = function(e) conditionMessage(e)))
print(tryCatch(MRCA(iq_r, c("Homo_sapiens", "Macaca_mulatta")), error = function(e) conditionMessage(e)))
cat("ape::getMRCA:", getMRCA(as.phylo(iq_r), c("Homo_sapiens", "Macaca_mulatta")), "\n")
for (lay in c("daylight", "equal_angle", "ape", "circular", "unrooted")) {
  r <- tryCatch({ p <- ggtree(iq, layout = lay); ggsave(paste0("lay_", lay, ".png"), p, width = 4, height = 4, dpi = 60); "OK" },
                error = function(e) conditionMessage(e))
  cat("layout", lay, ":", substr(r, 1, 120), "\n")
}
cat("ggplot2", as.character(packageVersion("ggplot2")), " ggtree", as.character(packageVersion("ggtree")), "\n")
