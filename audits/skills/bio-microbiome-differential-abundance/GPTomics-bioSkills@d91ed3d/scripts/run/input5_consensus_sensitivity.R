# Input 5 (Stress/multi-part): "Run the full consensus panel (ALDEx2, ANCOM-BC2, LinDA) and
# check whether the headline result is sensitive to the prevalence filter, moving it from
# 10% to 25% as the SKILL.md's Tips section explicitly instructs to verify."
suppressMessages({
  library(phyloseq)
  library(ALDEx2)
  library(ANCOMBC)
  library(MicrobiomeStat)
})

ps <- readRDS('F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/datagen/asvtable/phyloseq_object.rds')
truth <- read.delim('F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/datagen/asvtable/truth_da.tsv', stringsAsFactors = FALSE)
true_pos <- truth$ASV[truth$role != 'null']

run_panel <- function(ps, prv_cut, label) {
  keep <- filter_taxa(ps, function(x) sum(x > 0) >= prv_cut * nsamples(ps), TRUE)
  cat(sprintf('\n=== prv_cut=%.2f (%s): %d taxa retained ===\n', prv_cut, label, ntaxa(keep)))
  counts <- as.matrix(otu_table(keep)); if (!taxa_are_rows(keep)) counts <- t(counts)
  groups <- as.character(sample_data(keep)$Group)
  set.seed(1)
  aldex_out <- aldex(counts, groups, mc.samples = 128, test = 't', effect = TRUE, denom = 'all')
  sig_aldex <- rownames(aldex_out)[aldex_out$we.eBH < 0.05 & abs(aldex_out$effect) > 1]

  meta <- data.frame(as(sample_data(keep), 'data.frame'))
  fit_linda <- linda(feature.dat = as.data.frame(counts), meta.dat = meta,
                      formula = '~ Group', feature.dat.type = 'count', prev.filter = 0, alpha = 0.05)
  res_linda <- fit_linda$output[[1]]
  sig_linda <- rownames(res_linda)[res_linda$reject]

  confident <- intersect(sig_aldex, sig_linda)
  tp <- sum(confident %in% true_pos); fp <- sum(!(confident %in% true_pos)); fn <- length(true_pos) - tp
  cat(sprintf('ALDEx2 sig=%d, LinDA sig=%d, consensus=%d | TP=%d/%d FP=%d FN=%d\n',
              length(sig_aldex), length(sig_linda), length(confident), tp, length(true_pos), fp, fn))
  list(ntaxa = ntaxa(keep), consensus = confident, tp = tp, fp = fp, fn = fn)
}

r10 <- run_panel(ps, 0.10, 'default')
r25 <- run_panel(ps, 0.25, 'stricter')

cat('\n=== SENSITIVITY CHECK (SKILL.md Tips: "confirm the headline result survives 10% -> 25%") ===\n')
cat('Consensus set at 10%:', length(r10$consensus), 'taxa\n')
cat('Consensus set at 25%:', length(r25$consensus), 'taxa\n')
lost_to_filter <- setdiff(true_pos, colnames(otu_table(filter_taxa(ps, function(x) sum(x > 0) >= 0.25 * nsamples(ps), TRUE))))
cat('Planted true-positive taxa REMOVED from testing entirely by the stricter 25% filter (never got a chance):',
    length(lost_to_filter), '->', paste(lost_to_filter, collapse=', '), '\n')
cat('Consensus stable across both filters:', setequal(r10$consensus, r25$consensus), '\n')
if (!setequal(r10$consensus, r25$consensus)) {
  cat('  Present at 10% but not 25%:', paste(sort(setdiff(r10$consensus, r25$consensus)), collapse=', '), '\n')
  cat('  Present at 25% but not 10%:', paste(sort(setdiff(r25$consensus, r10$consensus)), collapse=', '), '\n')
}
