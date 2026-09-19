# Input 2 (Variant A): "Run ANCOM-BC2 with age and sex as covariates, set p_adjust to BH,
# and only report hits that pass the pseudo-count sensitivity analysis (passed_ss)."
# Also tests the documented default-vs-BH p_adj_method gotcha (SKILL.md: default is 'holm').
suppressMessages({
  library(phyloseq)
  library(ANCOMBC)
})

ps <- readRDS('F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/datagen/asvtable/phyloseq_object.rds')
truth <- read.delim('F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/datagen/asvtable/truth_da.tsv', stringsAsFactors = FALSE)
true_pos <- truth$ASV[truth$role != 'null']

keep <- filter_taxa(ps, function(x) sum(x > 0) >= 0.10 * nsamples(ps), TRUE)

# (a) DEFAULT p_adj_method left unset -> should be 'holm' per SKILL.md; verify.
out_default <- ancombc2(data = keep, fix_formula = 'Group + Age + Sex', rand_formula = NULL,
                         prv_cut = 0.10, lib_cut = 1000, group = 'Group',
                         struc_zero = TRUE, pseudo_sens = TRUE, global = FALSE, pairwise = FALSE, n_cl = 1)
cat('Default p_adj_method result columns present. Checking q-values are sparser than BH run below...\n')

# (b) explicit BH as SKILL.md instructs
out_bh <- ancombc2(data = keep, fix_formula = 'Group + Age + Sex', rand_formula = NULL,
                    p_adj_method = 'BH', prv_cut = 0.10, lib_cut = 1000, group = 'Group',
                    struc_zero = TRUE, pseudo_sens = TRUE, global = FALSE, pairwise = FALSE, n_cl = 1)
res_d <- out_default$res
res_b <- out_bh$res
dcol <- grep('^diff_Group', names(res_b), value = TRUE)[1]
sscol <- sub('^diff_', 'passed_ss_', dcol)
cat('Coefficient column:', dcol, '\n')

sig_default <- res_d$taxon[res_d[[dcol]]]
sig_bh_robust <- res_b$taxon[res_b[[dcol]] & res_b[[sscol]]]
cat('\nSignificant under DEFAULT (holm) p_adj:', length(sig_default), '\n')
cat('Significant under explicit BH AND passed_ss:', length(sig_bh_robust), '\n')
cat('BH set is superset-ish of holm (expected, holm is stricter):', all(sig_default %in% res_b$taxon[res_b[[dcol]]]), '\n')

cat('\n=== GROUND TRUTH CHECK (covariate-adjusted model) ===\n')
tp <- sum(sig_bh_robust %in% true_pos); fp <- sum(!(sig_bh_robust %in% true_pos))
fn <- length(true_pos) - tp
cat(sprintf('TP=%d/%d, FP=%d, FN=%d\n', tp, length(true_pos), fp, fn))
cat('Recovered:', paste(sort(intersect(sig_bh_robust, true_pos)), collapse=', '), '\n')
cat('Missed:', paste(sort(setdiff(true_pos, sig_bh_robust)), collapse=', '), '\n')
cat('False positives:', paste(sort(setdiff(sig_bh_robust, true_pos)), collapse=', '), '\n')

# Check Age/Sex coefficients are NOT spuriously significant on this fixture (no planted
# age/sex effect) -- a sanity check the covariate adjustment isn't introducing noise.
agecol <- grep('^diff_Age', names(res_b), value = TRUE)
if (length(agecol) > 0) {
  cat('\nAge-associated hits (should be ~0, no planted age effect):', sum(res_b[[agecol[1]]]), '\n')
}
