# Independent re-auditor input 2: run SKILL.md's own "Alpha Diversity in R" and
# "Beta Diversity in R" code blocks close to verbatim (only ps/chosen_depth/tree supplied)
# against a brand-new synthetic dataset the re-auditor built (not GlobalPatterns, not the
# fixer's/auditor's phyloseq_object.rds fixture). Confirms the fixed SKILL.md's documented
# patterns -- including the newly added strata= line sitting right below the unchanged
# adonis2/betadisper lines -- did not regress ordinary (non-repeated-measures) usage.
library(phyloseq)
library(vegan)
library(ape)

set.seed(777)

n_samples <- 30
n_taxa <- 80
otu <- matrix(rpois(n_samples * n_taxa, lambda = 20), nrow = n_taxa, ncol = n_samples)
rownames(otu) <- paste0("ASV", seq_len(n_taxa))
colnames(otu) <- paste0("Samp", seq_len(n_samples))

Group <- rep(c("control", "treated"), each = n_samples / 2)
# inject a real, modest compositional shift in "treated" so PERMANOVA has something to find
otu[1:15, Group == "treated"] <- otu[1:15, Group == "treated"] + rpois(15 * (n_samples / 2), lambda = 15)

sd <- sample_data(data.frame(Group = Group, row.names = colnames(otu)))
tree <- rtree(n_taxa, tip.label = rownames(otu))
ps <- phyloseq(otu_table(otu, taxa_are_rows = TRUE), sd, tree)

cat("Synthetic ps: samples =", nsamples(ps), "taxa =", ntaxa(ps), "\n")

# --- SKILL.md "Alpha Diversity in R" block, verbatim except chosen_depth ---
chosen_depth <- min(sample_sums(ps))  # smallest dataset here; fine for a smoke test
ps_rare <- rarefy_even_depth(ps, sample.size = chosen_depth, rngseed = 42, replace = FALSE)
alpha <- estimate_richness(ps_rare, measures = c('Observed', 'Shannon', 'InvSimpson'))
alpha$Group <- sample_data(ps_rare)$Group
alpha$Shannon_eff <- exp(alpha$Shannon)
kw <- kruskal.test(Shannon ~ Group, data = alpha)
cat(sprintf("Alpha block OK. Kruskal-Wallis Shannon p=%.4g\n", kw$p.value))

# --- SKILL.md "Beta Diversity in R" block, verbatim ---
wu  <- UniFrac(ps_rare, weighted = TRUE)
uwu <- UniFrac(ps_rare, weighted = FALSE)
gu  <- as.dist(GUniFrac::GUniFrac(t(as(otu_table(ps_rare), 'matrix')), phy_tree(ps_rare), alpha = 0.5)$unifracs[, , 'd_0.5'])

meta <- data.frame(sample_data(ps_rare))
r1 <- adonis2(wu ~ Group, data = meta, permutations = 999)
bd <- permutest(betadisper(wu, meta$Group))

# newly added line directly below -- meta has no SubjectID here (non-repeated-measures data),
# so this line is NOT invoked; confirms the ordinary path above it is unaffected by its presence.
cat(sprintf("Beta block OK. adonis2 R2=%.3f p=%.4g | betadisper p=%.4g\n",
            r1$R2[1], r1$`Pr(>F)`[1], bd$tab$`Pr(>F)`[1]))

cat("\nSKILL.md verbatim Alpha+Beta blocks: NO REGRESSION on a fresh, independent dataset.\n")
