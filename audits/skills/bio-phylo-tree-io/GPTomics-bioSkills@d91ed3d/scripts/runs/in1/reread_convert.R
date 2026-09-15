suppressPackageStartupMessages({library(treeio); library(ape)})
r <- tryCatch({x <- read.beast.newick("phylo_convert.nwk"); d <- get.data(x); paste("read.beast.newick columns:", paste(names(d), collapse = ","), "posterior:", paste(na.omit(d$posterior), collapse = ","))},
              error = function(e) paste("read.beast.newick ERROR:", conditionMessage(e)))
cat(r, "\n")
r <- tryCatch({a <- read.tree("phylo_convert.nwk"); paste("ape read.tree tips:", paste(a$tip.label, collapse = ","))},
              error = function(e) paste("ape read.tree ERROR:", conditionMessage(e)))
cat(r, "\n")
