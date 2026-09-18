# Input 5 (regression of pre-fix Input 7's FCR half) -- runs the SKILL.md "False Coverage
# Rate -- CIs on a Selected Set" code block VERBATIM against a freshly simulated selected set
# (independent of the pre-fix audit's own selected set, per the re-audit brief).
set.seed(4471)
m <- 4000
n_alt <- 400
true_effect <- rep(0, m)
alt_idx <- sample(m, n_alt)
true_effect[alt_idx] <- rnorm(n_alt, mean = 2.0, sd = 0.4) * sample(c(-1,1), n_alt, TRUE)

se <- rep(1, m)
estimate <- true_effect + rnorm(m, 0, se)
z0 <- estimate / se
pvalues <- 2 * (1 - pnorm(abs(z0)))
padj <- p.adjust(pvalues, method = 'BH')

# ---- SKILL.md code block, verbatim ----
q <- 0.05
R <- sum(padj < q)
m_total <- length(pvalues)
fcr_level  <- 1 - q * R / m_total
alpha_fcr  <- 1 - fcr_level
z          <- qnorm(1 - alpha_fcr / 2)
ci_lower   <- estimate[padj < q] - z * se[padj < q]
ci_upper   <- estimate[padj < q] + z * se[padj < q]
# ---- end verbatim block ----

sel_truth <- true_effect[padj < q]
naive_z <- qnorm(0.975)
naive_lower <- estimate[padj < q] - naive_z * se[padj < q]
naive_upper <- estimate[padj < q] + naive_z * se[padj < q]

naive_cov <- mean(sel_truth >= naive_lower & sel_truth <= naive_upper)
fcr_cov   <- mean(sel_truth >= ci_lower & sel_truth <= ci_upper)

cat(sprintf("Selected set R = %d out of m = %d\n", R, m_total))
cat(sprintf("FCR-adjusted level = %.4f (z = %.3f) vs naive z = %.3f\n", fcr_level, z, naive_z))
cat(sprintf("naive 95%% CI coverage on selected set : %.4f\n", naive_cov))
cat(sprintf("FCR-adjusted CI coverage on selected set: %.4f\n", fcr_cov))
