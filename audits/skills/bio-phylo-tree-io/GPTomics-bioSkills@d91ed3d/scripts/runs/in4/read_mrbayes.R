# Input 4, R route: treeio read.mrbayes on the .con.tre; ape read.nexus on the posterior .t. SYNTHETIC.
suppressPackageStartupMessages({library(treeio); library(ape)})
m <- read.mrbayes("../../data/mb10.con.tre")
tb <- as_tibble(m)
cat("read.mrbayes columns:", paste(names(tb), collapse = ", "), "\n")
print(head(as.data.frame(tb[!is.na(tb$prob) & tb$node > 10, c("node", "prob", "prob_stddev")]), 9))
p1 <- read.nexus("../../data/mb10.run1.t")
cat("ape read.nexus run1 class:", class(p1), "length:", length(p1), "\n")
