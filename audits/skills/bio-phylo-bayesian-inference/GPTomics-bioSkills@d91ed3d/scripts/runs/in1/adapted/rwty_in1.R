# Input 1 topology-convergence check with RWTY, following the Skill:
#   analyze.rwty(list(run1=..., run2=...), burnin=25) then makeplot.treespace
# NB: in rwty 1.0.3 'burnin' is a NUMBER OF SAMPLES, not a percentage (see ?analyze.rwty) -- checked below.
suppressMessages({library(rwty); library(ape); library(phangorn)})
cat("rwty", as.character(packageVersion("rwty")), "\n")
setwd("F:/OpenScience/audits/bio-phylo-bayesian-inference/runs/in1/adapted")
r1 <- load.trees("adapted.run1.t", type = "nexus", format = "mb")
r2 <- load.trees("adapted.run2.t", type = "nexus", format = "mb")
cat("trees per run:", length(r1$trees), length(r2$trees), "\n")
cat("analyze.rwty formals burnin default:", deparse(formals(analyze.rwty)$burnin), "\n")
nb <- round(0.25 * length(r1$trees))
set.seed(1)
res <- analyze.rwty(list(run1 = r1, run2 = r2), burnin = nb, window.size = 200, treespace.points = 100,
                    filename = NA, overwrite = TRUE, fill.color = NA)
cat("names(res):", paste(names(res), collapse = ", "), "\n")
# topological ESS (approximate) per run
tess <- topological.approx.ess(r1, burnin = nb)
cat("approx topological ESS run1:\n"); print(tess)
tess2 <- topological.approx.ess(r2, burnin = nb)
cat("approx topological ESS run2:\n"); print(tess2)
# ASDSF across runs (rwty)
asdsf <- makeplot.asdsf(list(run1 = r1, run2 = r2), burnin = nb, window.size = 200)
png("treespace.png", width = 900, height = 450)
ts <- makeplot.treespace(list(run1 = r1, run2 = r2), burnin = nb, n.points = 100, fill.color = NA)
print(ts$treespace.heatmap)
dev.off()
# compare MAP / consensus with the SIMULATED true tree
truth <- read.tree("F:/OpenScience/audits/bio-phylo-bayesian-inference/data/d12_true.nwk")
con <- read.nexus("adapted.con.tre")
if (inherits(con, "multiPhylo")) con <- con[[1]]
cat("RF(consensus, truth) =", RF.dist(unroot(con), unroot(truth), normalize = FALSE), "\n")
