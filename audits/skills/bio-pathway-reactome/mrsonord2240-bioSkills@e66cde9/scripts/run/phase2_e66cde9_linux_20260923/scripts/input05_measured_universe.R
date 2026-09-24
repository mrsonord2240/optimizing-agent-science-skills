library(ReactomePA)
library(clusterProfiler)
library(org.Hs.eg.db)

sig_symbols <- c('CDK1','CCNB1','CCNB2','CDC20','BUB1','MAD2L1','PLK1','AURKA','AURKB','CDC25C',
                 'CCNA2','CDK2','E2F1','MCM2','MCM3','MCM4','MCM5','MCM6','MCM7','ORC1')
set.seed(42)
all_symbols <- keys(org.Hs.eg.db, keytype = 'SYMBOL')
measured_symbols <- unique(c(sig_symbols, sample(setdiff(all_symbols, sig_symbols), 3000 - length(sig_symbols))))
sig_entrez <- bitr(sig_symbols, fromType = 'SYMBOL', toType = 'ENTREZID', OrgDb = org.Hs.eg.db)$ENTREZID
universe <- bitr(measured_symbols, fromType = 'SYMBOL', toType = 'ENTREZID', OrgDb = org.Hs.eg.db)$ENTREZID

with_universe <- enrichPathway(gene = sig_entrez, organism = 'human', universe = universe,
                               pvalueCutoff = 0.05, qvalueCutoff = 0.2,
                               minGSSize = 10, maxGSSize = 500, readable = TRUE)
without_universe <- enrichPathway(gene = sig_entrez, organism = 'human',
                                  pvalueCutoff = 0.05, qvalueCutoff = 0.2,
                                  minGSSize = 10, maxGSSize = 500, readable = TRUE)
stopifnot(!is.null(with_universe), nrow(as.data.frame(with_universe)) > 0,
          !is.null(without_universe), nrow(as.data.frame(without_universe)) > 0)

with_df <- as.data.frame(with_universe)
without_df <- as.data.frame(without_universe)
with_denominator <- as.numeric(sub('.*/', '', with_df$BgRatio[1]))
without_denominator <- as.numeric(sub('.*/', '', without_df$BgRatio[1]))
stopifnot(with_denominator < without_denominator)
write.csv(data.frame(route = c('measured_universe', 'implicit_default'),
                     bg_ratio = c(with_df$BgRatio[1], without_df$BgRatio[1]),
                     denominator = c(with_denominator, without_denominator),
                     top_id = c(with_df$ID[1], without_df$ID[1])),
          file.path('/mnt/openscience/audits/bio-pathway-reactome/run/phase2_e66cde9_linux_20260923/outputs',
                    'input05_measured_universe.csv'), row.names = FALSE)
cat('ASSERT measured_universe_nonempty rows=', nrow(with_df), '\n', sep = '')
cat('ASSERT implicit_default_nonempty rows=', nrow(without_df), '\n', sep = '')
cat('ASSERT measured_bg_denominator=', with_denominator,
    ' default_bg_denominator=', without_denominator, '\n', sep = '')
