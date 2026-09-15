# Input 4 (Variant B): compositional heterogeneity, SYNTHETIC comp8.fa. The agent follows the fixed Skill: try the
# stationary correction, meet the NaN row in Common Errors, report the NaN pairs, switch to logdet/paralin or njs().
library(ape); library(phangorn)
aln <- read.dna('../../data/comp8.fa', format = 'fasta'); rownames(aln) <- trimws(rownames(aln))
true <- read.tree('../../data/comp8_true.nwk'); rf <- function(t) RF.dist(unroot(t), unroot(true), normalize = FALSE)
d_k80 <- dist.dna(aln, model = 'K80')
r <- tryCatch(nj(d_k80), error = function(e) conditionMessage(e)); cat('nj(K80):', if (is.character(r)) r else 'ran', '\n')
m <- as.matrix(d_k80); w <- which(is.nan(m), arr.ind = TRUE)
cat('K80 NaN pairs:', unique(apply(w, 1, function(i) paste(sort(rownames(m)[i]), collapse = '-'))), '\n')
cat('max p among NaN pairs:', round(max(as.matrix(dist.dna(aln, 'raw'))[w]), 3), '\n')
cat('RF (max 10): K80 njs', rf(njs(d_k80)), '| TN93 bionjs', rf(bionjs(dist.dna(aln, 'TN93'))),
    '| logdet NJ', rf(nj(dist.dna(aln, 'logdet'))), '| paralin FastME', rf(fastme.bal(dist.dna(aln, 'paralin'))), '\n')
method <- function(x) nj(dist.dna(x, model = 'logdet'))
tree <- method(aln); set.seed(42); b <- boot.phylo(tree, aln, method, B = 200, quiet = TRUE)
cat('LogDet NJ bootstrap %:', round(100 * b / 200), '| node in true tree:', prop.clades(unroot(tree), unroot(true), rooted = FALSE), '\n')
