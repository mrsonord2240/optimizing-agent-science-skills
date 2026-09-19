# Input 9 (NEW): the fixed Skill says root with ape::root(..., edgelabel = TRUE) to keep node-held support on the right
# branch. Check label placement by bipartition for edgelabel FALSE vs TRUE on the SYNTHETIC IQ-TREE primate treefile.
suppressPackageStartupMessages(library(ape))
tr <- read.tree('../../data/iq/primates16.treefile')
og <- c('Microcebus_murinus', 'Otolemur_garnettii')
key <- function(tips, all) { a <- sort(tips); b <- sort(setdiff(all, tips)); if (length(a) < length(b) || (length(a) == length(b) && a[1] < b[1])) paste(a, collapse = ',') else paste(b, collapse = ',') }
labmap <- function(t) {
  all <- t$tip.label; out <- c()
  for (n in (Ntip(t) + 1):(Ntip(t) + t$Nnode)) {
    l <- t$node.label[n - Ntip(t)]
    if (!is.na(l) && nzchar(l)) out[key(extract.clade(t, n)$tip.label, all)] <- l
  }
  out
}
before <- labmap(tr)
for (el in c(FALSE, TRUE)) {
  r <- root(tr, outgroup = og, resolve.root = TRUE, edgelabel = el)
  after <- labmap(r)
  common <- intersect(names(before), names(after))
  moved <- sum(before[common] != after[common])
  lost <- length(setdiff(names(before), names(after)))
  cat(sprintf('edgelabel = %-5s labels compared %d, on a different split %d, not placed %d\n', el, length(common), moved, lost))
}
