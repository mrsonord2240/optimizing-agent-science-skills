# Regression re-run of the original audit's Input 5 (prevalence-filter sensitivity,
# 10% vs 25%, ALDEx2 x LinDA consensus) -- code paths unchanged by the fix (only
# the LinDA formula/coercion and ALDEx2 seeding changed, both exercised here).

setwd('F:/OpenScience/audits/bio-microbiome-differential-abundance')
library(phyloseq); library(ALDEx2); library(MicrobiomeStat)

truth <- read.delim('data/asvtable/truth_da.tsv', stringsAsFactors = FALSE)
planted <- truth$ASV[truth$role != 'null']

run_at <- function(prv_cut) {
  ps <- readRDS('data/asvtable/phyloseq_object.rds')
  keep <- filter_taxa(ps, function(x) sum(x > 0) >= prv_cut * nsamples(ps), TRUE)
  ps <- keep
  counts <- as.matrix(otu_table(ps)); if (!taxa_are_rows(ps)) counts <- t(counts)
  groups <- as.character(sample_data(ps)$Group)
  set.seed(42)
  res <- aldex(counts, groups, mc.samples = 128, test = 't', effect = TRUE, denom = 'all')
  sig_aldex <- rownames(res)[res$we.eBH < 0.05 & abs(res$effect) > 1]

  otu <- as.data.frame(otu_table(ps)); if (!taxa_are_rows(ps)) otu <- t(otu)
  meta <- data.frame(as(sample_data(ps), 'data.frame'))
  fit <- linda(feature.dat = otu, meta.dat = meta, formula = '~ Group + Age',
               feature.dat.type = 'count', prev.filter = prv_cut, alpha = 0.05)
  sig_linda <- rownames(fit$output[[1]])[fit$output[[1]]$reject]

  confident <- intersect(sig_aldex, sig_linda)
  tp <- sum(confident %in% planted); fp <- sum(!(confident %in% planted))
  cat(sprintf('prv_cut=%.2f: %d taxa retained; ALDEx2 sig=%d LinDA sig=%d consensus=%d TP=%d/%d FP=%d\n',
              prv_cut, ntaxa(ps), length(sig_aldex), length(sig_linda), length(confident), tp, length(planted), fp))
  confident
}

c10 <- run_at(0.10)
c25 <- run_at(0.25)
cat('Stable across both filters:', identical(sort(c10), sort(c25)), '\n')
cat('Present at 10% but not 25%:', paste(setdiff(c10, c25), collapse=', '), '\n')
cat('Present at 25% but not 10%:', paste(setdiff(c25, c10), collapse=', '), '\n')
