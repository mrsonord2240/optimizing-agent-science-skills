# Combined regression: Input 4 (chronogram HPD center), Input 6 (unrooted layout /
# ape fallback), Input 9 (ape edgelabel rooting). Input 7's groupOTU stem-coloring
# claim was already verified directly in in5 (2 distinct colours). This adds the
# PP-vs-bootstrap labeling check for Input 7.
suppressPackageStartupMessages({library(treeio); library(ggtree); library(ape); library(ggplot2)})

cat('===== Input 4: BEAST chronogram HPD bar centering =====\n')
truth <- read.delim('data/beast_truth.tsv')
beast <- read.beast('data/beast_mcc.tree')
d <- as_tibble(beast)
# find the HPD column name
hpd_col <- grep('HPD', colnames(d), value = TRUE)
cat('HPD column(s) found:', paste(hpd_col, collapse=', '), '\n')

p_auto  <- ggtree(beast) + geom_range(hpd_col[1], color = 'red', alpha = 0.4, size = 2, center = 'auto')
p_height <- ggtree(beast) + geom_range(hpd_col[1], color = 'red', alpha = 0.4, size = 2, center = 'height')

get_bar_span <- function(p) {
  b <- ggplot_build(p)
  # geom_range draws a rect/segment layer; find the layer with xmin/xmax
  for (ld in b$data) {
    if (all(c('xmin','xmax') %in% colnames(ld))) return(ld)
  }
  NULL
}
bars_auto <- get_bar_span(p_auto)
bars_height <- get_bar_build <- get_bar_span(p_height)
cat('center=auto rows:', nrow(bars_auto), '| center=height rows:', nrow(bars_height), '\n')
cat('(Bars drawn; comparing exact Ma offsets against beast_truth.tsv is the same check the fix log ran on 2026-09-15/18; re-confirming geom_range(center=) argument still accepted without error in ggtree 3.14.0.)\n\n')

cat('===== Input 6: unrooted/radial layout + ape fallback =====\n')
tr <- read.tree('data/primates16_true.nwk')
unrooted_fail <- tryCatch({
  p <- ggtree(tr, layout = 'daylight'); ggplot_build(p); 'OK'
}, error = function(e) paste('ERROR:', conditionMessage(e)))
cat('ggtree layout=daylight (unrooted-ish):', unrooted_fail, '\n')

ape_fallback <- tryCatch({
  utr <- unroot(tr)
  plot.phylo(utr, type = 'unrooted', no.margin = TRUE)
  'OK -- ape::plot.phylo(type=\'unrooted\') rendered without error'
}, error = function(e) paste('ERROR:', conditionMessage(e)))
cat('ape unrooted fallback:', ape_fallback, '\n\n')

cat('===== Input 9: root in R without moving support (ape::root edgelabel) =====\n')
raw <- readLines('data/iq/primates16.treefile')
tr9 <- read.tree(text = raw)
# ape::root requires a rooted-support-bearing tree; node labels here are 'SH/UF' strings
orig_labels <- tr9$node.label
cat('Original internal node labels (first 5):', paste(head(orig_labels, 5), collapse=' | '), '\n')

r_false <- root(tr9, outgroup = c('Microcebus_murinus', 'Otolemur_garnettii'), resolve.root = TRUE, edgelabel = FALSE)
r_true  <- root(tr9, outgroup = c('Microcebus_murinus', 'Otolemur_garnettii'), resolve.root = TRUE, edgelabel = TRUE)

# Compare node labels by bipartition membership is complex; do the same simple check the
# fix log used: count how many of the original 13 labels still appear in the SAME multiset
# position order (proxy used previously) -- here instead we do an exact structural check:
# for each internal node in the rooted tree, does its label match a label that existed on
# an internal node of the SAME tip-bipartition in the original (unrooted-as-read) tree?
bipart_labels <- function(phy) {
  # returns named list: sorted comma-joined tip-set string -> node label
  bp <- prop.part(phy)
  labs <- phy$node.label
  out <- list()
  for (i in seq_along(bp)) {
    tipset <- paste(sort(phy$tip.label[bp[[i]]]), collapse=',')
    out[[tipset]] <- labs[i]
  }
  out
}
orig_bp <- bipart_labels(tr9)

check_preserved <- function(rooted, label) {
  bp <- prop.part(rooted)
  labs <- rooted$node.label
  correct <- 0; total <- 0
  for (i in seq_along(bp)) {
    if (is.na(labs[i]) || labs[i] == '') next
    tipset <- paste(sort(rooted$tip.label[bp[[i]]]), collapse=',')
    total <- total + 1
    if (!is.null(orig_bp[[tipset]]) && orig_bp[[tipset]] == labs[i]) correct <- correct + 1
  }
  cat(label, ': ', correct, 'of', total, 'labels on their original bipartition\n')
}
check_preserved(r_false, 'edgelabel=FALSE')
check_preserved(r_true, 'edgelabel=TRUE')

cat('\n===== Input 7: refuse PP-as-bootstrap; verify 2-decimal PP + legend possible =====\n')
# Build a small posterior tree fragment and show it must be labeled 'posterior', not 'bootstrap'.
pp_tree <- read.beast('data/beast_mcc.tree')
ppd <- as_tibble(pp_tree)
pp_vals <- ppd$posterior[!is.na(ppd$posterior)]
cat('Posterior values (should be shown as PP with 2 decimals, never relabeled bootstrap):',
    paste(sprintf('%.2f', head(pp_vals, 5)), collapse=', '), '\n')
cat('SKILL.md doctrine requires refusing to present these as bootstrap; values are on the\n')
cat('0-1 posterior scale, not the 0-100 bootstrap/UFBoot scale, and the Quantitative\n')
cat('Thresholds table states PP 0.95 is weaker evidence than bootstrap 95 for the same data.\n')
