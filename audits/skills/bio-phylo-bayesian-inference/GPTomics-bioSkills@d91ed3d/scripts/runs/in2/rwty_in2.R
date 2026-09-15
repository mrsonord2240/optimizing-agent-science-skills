# Input 2: topology convergence of the user's (SYNTHETIC, deliberately under-run) chains with RWTY, as the Skill directs.
# rwty 1.0.3: burnin = NUMBER OF TREES (not percent), so 25% of 401 samples = 100.
suppressMessages({library(rwty)})
setwd("F:/OpenScience/audits/bio-phylo-bayesian-inference/runs/in2")
r1 <- load.trees("user.run1.t", type = "nexus", format = "mb")
r2 <- load.trees("user.run2.t", type = "nexus", format = "mb")
n <- length(r1$trees); nb <- round(0.25 * n)
cat("trees per run:", n, length(r2$trees), " burnin(trees):", nb, "\n")
set.seed(2)
cat("approx topological ESS run1:\n"); print(topological.approx.ess(r1, burnin = nb))
cat("approx topological ESS run2:\n"); print(topological.approx.ess(r2, burnin = nb))
ts <- makeplot.treespace(list(run1 = r1, run2 = r2), burnin = nb, n.points = 100, fill.color = NA)
png("treespace_in2.png", width = 900, height = 450); print(ts$treespace.plot); dev.off()
cat("done\n")
