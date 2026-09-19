# Input 1 (Canonical): "I have an ASV table (phyloseq object) with control vs treated
# groups. Find differentially abundant taxa - run two compositionally-aware methods and
# give me the consensus." Follows SKILL.md's default workflow: ALDEx2 first, then a second
# tool (ANCOM-BC2), BH q < 0.05, effect floor |1| for ALDEx2, consensus = intersection.
suppressMessages({
  library(phyloseq)
  library(ALDEx2)
  library(ANCOMBC)
})

ps <- readRDS('F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/datagen/asvtable/phyloseq_object.rds')
truth <- read.delim('F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/datagen/asvtable/truth_da.tsv', stringsAsFactors = FALSE)

# Prevalence filter per SKILL.md: taxa present in >=10% of samples
keep <- filter_taxa(ps, function(x) sum(x > 0) >= 0.10 * nsamples(ps), TRUE)
cat('Taxa after prevalence filter (10%):', ntaxa(keep), 'of', ntaxa(ps), '\n')

counts <- as.matrix(otu_table(keep))
if (!taxa_are_rows(keep)) counts <- t(counts)
groups <- as.character(sample_data(keep)$Group)

set.seed(1)
aldex_out <- aldex(counts, groups, mc.samples = 128, test = 't', effect = TRUE, denom = 'all')
sig_aldex <- rownames(aldex_out)[aldex_out$we.eBH < 0.05 & abs(aldex_out$effect) > 1]
cat('\nALDEx2 significant (we.eBH<0.05 & |effect|>1):', length(sig_aldex), '\n')
cat(' ', paste(sort(sig_aldex), collapse=', '), '\n')

anc_out <- ancombc2(data = keep, fix_formula = 'Group', rand_formula = NULL,
                     p_adj_method = 'BH', prv_cut = 0.10, lib_cut = 1000,
                     group = 'Group', struc_zero = TRUE, pseudo_sens = TRUE,
                     global = FALSE, pairwise = FALSE, n_cl = 1)
res <- anc_out$res
dcol <- grep('^diff_Group', names(res), value = TRUE)[1]
sscol <- sub('^diff_', 'passed_ss_', dcol)
cat('\nANCOM-BC2 diff column used:', dcol, '/ passed_ss column:', sscol, '\n')
sig_ancombc_raw <- res$taxon[res[[dcol]]]
sig_ancombc_robust <- res$taxon[res[[dcol]] & res[[sscol]]]
cat('ANCOM-BC2 significant (diff only):', length(sig_ancombc_raw), '\n')
cat('ANCOM-BC2 significant AND passed_ss (robust):', length(sig_ancombc_robust), '\n')
cat(' ', paste(sort(sig_ancombc_robust), collapse=', '), '\n')

confident <- intersect(sig_aldex, sig_ancombc_robust)
exploratory <- union(sig_aldex, sig_ancombc_robust)
cat('\nConsensus intersection (high-confidence):', length(confident), '\n')
cat(' ', paste(sort(confident), collapse=', '), '\n')
cat('Union (exploratory):', length(exploratory), '\n')

# --- Ground truth comparison ---
true_pos <- truth$ASV[truth$role != 'null']
true_null <- truth$ASV[truth$role == 'null']
cat('\n=== GROUND TRUTH CHECK ===\n')
cat('True DA taxa (planted):', length(true_pos), '->', paste(true_pos, collapse=', '), '\n')

eval_recovery <- function(sig, label) {
  tp <- sum(sig %in% true_pos)
  fp <- sum(sig %in% true_null)
  fn <- sum(!(true_pos %in% sig))
  cat(sprintf('%s: TP=%d/%d planted recovered, FP=%d (called sig but truly null), FN=%d missed\n',
              label, tp, length(true_pos), fp, fn))
  cat('  Recovered:', paste(sort(intersect(sig, true_pos)), collapse=', '), '\n')
  cat('  Missed:', paste(sort(setdiff(true_pos, sig)), collapse=', '), '\n')
  cat('  False positives (in null set):', paste(sort(intersect(sig, true_null)), collapse=', '), '\n')
}
eval_recovery(sig_aldex, 'ALDEx2')
eval_recovery(sig_ancombc_robust, 'ANCOM-BC2 (robust)')
eval_recovery(confident, 'Consensus (intersection)')

# Direction check for consensus hits
if (length(confident) > 0) {
  cat('\nDirection check (consensus hits):\n')
  for (tx in confident) {
    truth_fc <- truth$true_fc_treated_vs_control[truth$ASV == tx]
    aldex_eff <- aldex_out[tx, 'effect']
    cat(sprintf('  %s: truth_fc=%.2f (%s), aldex2 effect=%.3f (%s)\n', tx, truth_fc,
                ifelse(truth_fc>1,'should be UP in treated', ifelse(truth_fc<1,'should be DOWN in treated','null')),
                aldex_eff, ifelse(aldex_eff>0,'ALDEx2 says UP','ALDEx2 says DOWN')))
  }
}
