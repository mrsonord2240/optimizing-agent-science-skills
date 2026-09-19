# Follow-up: does ZicoSeq actually crash on RAW (unfiltered) counts, confirming the trap
# TOOLS.md documented, and does SKILL.md give the reader any way to know this before hitting it?
suppressMessages({ library(phyloseq); library(GUniFrac) })
ps <- readRDS('F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/datagen/asvtable/phyloseq_object.rds')
otu <- as.matrix(otu_table(ps)); if (!taxa_are_rows(ps)) otu <- t(otu)
meta <- data.frame(as(sample_data(ps), 'data.frame'))
n_zerovar <- sum(apply(otu, 1, function(x) length(unique(x)) == 1))
cat('Zero-variance features in RAW unfiltered table (200 taxa):', n_zerovar, '\n')
result <- tryCatch({
  ZicoSeq(meta.dat = meta, feature.dat = otu, grp.name = 'Group', feature.dat.type = 'count',
          prev.filter = 0, perm.no = 99)
  'SUCCEEDED'
}, error = function(e) paste('CRASHED:', conditionMessage(e)))
cat('Result on raw unfiltered table:', result, '\n')
