# Input 9 (NEW, Variant): "estimate alpha, do not assume" -- the fixed Skill says it but gives no code. The agent
# estimates alpha (phangorn ML on a BIONJ start), plugs it into the Skill's method-once pattern, bootstraps with the
# same method. SYNTHETIC deep12.fa (true alpha 0.4).
library(ape); library(phangorn)
aln <- read.dna('../../data/deep12.fa', format = 'fasta'); rownames(aln) <- trimws(rownames(aln))
true <- read.tree('../../data/deep12_true.nwk'); rf <- function(t) RF.dist(unroot(t), unroot(true), normalize = FALSE)
start <- bionj(dist.dna(aln, 'TN93'))
fit <- optim.pml(pml(start, phyDat(aln), k = 4), model = 'GTR', optGamma = TRUE, optEdge = TRUE,
                 rearrangement = 'none', control = pml.control(trace = 0))
alpha <- fit$shape
cat('estimated alpha', round(alpha, 3), '(simulated 0.4)\n')
method <- function(x) fastme.bal(dist.dna(x, model = 'TN93', gamma = alpha), nni = TRUE, spr = TRUE)
tree <- method(aln); set.seed(42); b <- boot.phylo(tree, aln, method, B = 200, quiet = TRUE)
cat('RF estimated-alpha FastME', rf(tree), '| alpha 0.5 FastME', rf(fastme.bal(dist.dna(aln, 'TN93', gamma = 0.5), nni = TRUE, spr = TRUE)), '(max 18)\n')
cat('bootstrap %:', round(100 * b / 200), '\n')
cat('ML GTR+G4 on BIONJ start with NNI (routing check):', rf(optim.pml(fit, rearrangement = 'NNI', control = pml.control(trace = 0))$tree), '\n')
