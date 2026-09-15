# Input 5 (Stress): rooted (non-reversible IQ-TREE) deep20 tree -> subset of 8 taxa -> collapse UFBoot<95 ->
# binary version for a downstream comparative method, in ape/phangorn, with integrity checks. SYNTHETIC data.
suppressPackageStartupMessages({library(ape); library(phangorn)})
tr <- read.tree('nr/rootnr.treefile')
cat('rooted:', is.rooted(tr), ' binary:', is.binary(tr), ' Ntip:', Ntip(tr), '\n')
kids <- Children(tr, Ntip(tr) + 1)
cat('root children tip sets:\n'); for (k in kids) print(sort(extract.clade(tr, k)$tip.label))

keep <- c('X1', 'X3', 'X5', 'X8', 'Y1', 'Y5', 'Y8', 'Y10')
D0 <- cophenetic(tr)[keep, keep]
sub <- drop.tip(tr, setdiff(tr$tip.label, keep))
D1 <- cophenetic(sub)[keep, keep]
cat('drop.tip: max |d_before - d_after| =', max(abs(D0 - D1)), ' rooted:', is.rooted(sub), '\n')
cat('X taxa monophyletic in subset:', is.monophyletic(sub, keep[1:4]), '\n')
print(write.tree(sub))

# Skill recipe for di2multi: zero out low-support branch lengths first, THEN di2multi
sup <- suppressWarnings(as.numeric(sub$node.label))
cat('node labels (rootstrap/UFBoot on subset, computed on FULL taxon set):', sub$node.label, '\n')
low <- which(!is.na(sup) & sup < 95) + Ntip(sub)
cat('internal nodes with support < 95:', length(low), '\n')
col <- sub
col$edge.length[col$edge[, 2] %in% low] <- 0
col <- di2multi(col)
cat('after recipe: Nnode', sub$Nnode, '->', col$Nnode, '| max patristic change =', max(abs(cophenetic(col)[keep, keep] - D1)), '\n')
print(write.tree(col))
# distance-preserving alternative: collapse by moving the branch length to the children
col2 <- sub
for (nd in sort(low, decreasing = TRUE)) {
  e <- which(col2$edge[, 2] == nd); L <- col2$edge.length[e]
  ch <- which(col2$edge[, 1] == nd); col2$edge.length[ch] <- col2$edge.length[ch] + L; col2$edge.length[e] <- 0
}
col2 <- di2multi(col2)
cat('length-pushing collapse: max patristic change =', max(abs(cophenetic(col2)[keep, keep] - D1)), '\n')

# binary tree for downstream: integrate over random resolutions rather than one arbitrary multi2di
set.seed(42)
res <- lapply(1:100, function(i) multi2di(col2, random = TRUE))
class(res) <- 'multiPhylo'
u <- unique(lapply(res, function(t) write.tree(t, digits = 0)))
cat('distinct random resolutions in 100 draws:', length(unique(sapply(res, function(t) paste(sort(prop.part(t) |> sapply(function(p) paste(sort(attr(prop.part(t), 'labels')[p]), collapse='.'))), collapse='|')))), '\n')
cat('all binary:', all(sapply(res, is.binary)), ' zero-length inserted edges in draw 1:', sum(res[[1]]$edge.length == 0), '\n')
write.tree(res, 'deep20_subset_resolutions.nwk')
write.tree(col2, 'deep20_subset_collapsed.nwk')
