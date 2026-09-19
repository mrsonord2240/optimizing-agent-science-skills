# Fixed methodology for Input 9: canonicalize each bipartition to the tip-side that
# excludes a fixed reference tip, so re-rooting (which can flip which side is the
# "descendant" set) does not spuriously register a real match as a mismatch.
suppressPackageStartupMessages({library(ape)})

raw <- readLines('data/iq/primates16.treefile')
tr9 <- read.tree(text = raw)
all_tips <- sort(tr9$tip.label)
ref_tip <- 'Homo_sapiens'   # any tip not in the outgroup works as the fixed reference

canon <- function(tipset, all_tips, ref_tip) {
  tipset <- sort(tipset)
  if (ref_tip %in% tipset) {
    paste(setdiff(all_tips, tipset), collapse = ',')  # take the complement so ref_tip is excluded
  } else {
    paste(tipset, collapse = ',')
  }
}

bipart_labels_canon <- function(phy, all_tips, ref_tip) {
  bp <- prop.part(phy)
  labs <- phy$node.label
  out <- list()
  for (i in seq_along(bp)) {
    tipset <- phy$tip.label[bp[[i]]]
    key <- canon(tipset, all_tips, ref_tip)
    if (!is.na(labs[i]) && labs[i] != '') out[[key]] <- labs[i]
  }
  out
}

orig_bp <- bipart_labels_canon(tr9, all_tips, ref_tip)
cat('Original tree: ', length(orig_bp), 'labeled internal splits (of', tr9$Nnode, 'total internal nodes)\n')

check_preserved <- function(rooted, label, all_tips, ref_tip) {
  bp <- prop.part(rooted)
  labs <- rooted$node.label
  correct <- 0; total <- 0; wrong_examples <- c()
  for (i in seq_along(bp)) {
    if (is.na(labs[i]) || labs[i] == '') next
    tipset <- rooted$tip.label[bp[[i]]]
    key <- canon(tipset, all_tips, ref_tip)
    total <- total + 1
    if (!is.null(orig_bp[[key]]) && orig_bp[[key]] == labs[i]) {
      correct <- correct + 1
    } else {
      wrong_examples <- c(wrong_examples, labs[i])
    }
  }
  cat(label, ': ', correct, 'of', total, 'labels on their original bipartition',
      '| mismatched labels:', paste(wrong_examples, collapse=', '), '\n')
}

r_false <- root(tr9, outgroup = c('Microcebus_murinus', 'Otolemur_garnettii'), resolve.root = TRUE, edgelabel = FALSE)
r_true  <- root(tr9, outgroup = c('Microcebus_murinus', 'Otolemur_garnettii'), resolve.root = TRUE, edgelabel = TRUE)

check_preserved(r_false, 'edgelabel=FALSE', all_tips, ref_tip)
check_preserved(r_true,  'edgelabel=TRUE ', all_tips, ref_tip)
