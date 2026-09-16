# go-enrichment Input 2 (variant): does omitting universe= matter? A NULL hit list (150 random quantified proteins, no biology)
# is tested with the matched universe (Skill's rule) and with universe omitted (the default whole-annotation background).
# SKILL.md block b01 run verbatim for the correct call; the omission variant drops only the universe argument.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(clusterProfiler); library(org.Hs.eg.db)})
GG <- 'F:/OpenScience/audits/bio-pathway-go-enrichment'
tab <- read.csv(file.path(GG, 'data', 'proteomics_da_table.csv'), colClasses = 'character')
gene_list <- unique(tab$entrez[tab$hit_null == 'TRUE'])
universe_ids <- unique(tab$entrez)
cat('null foreground', length(gene_list), '| universe', length(universe_ids), '\n')
blk <- list.files(file.path(GG, 'runs', 'blocks'), pattern = '^b01', full.names = TRUE)
sys.source(blk, envir = globalenv())            # verbatim: with universe
with_u <- as.data.frame(ego)
src <- readLines(blk); src <- src[!grepl('universe\\s*=', src)]
tf <- tempfile(fileext = '.R'); writeLines(src, tf); sys.source(tf, envir = globalenv())   # same call, universe omitted
no_u <- as.data.frame(ego)
cat('terms at p.adjust<0.05 -- with matched universe:', nrow(with_u), '| with universe omitted:', nrow(no_u), '\n')
if (nrow(no_u)) print(head(no_u[, c('ID', 'Description', 'GeneRatio', 'BgRatio', 'p.adjust')], 10))
if (nrow(no_u)) cat('N in BgRatio with universe omitted:', unique(sapply(strsplit(no_u$BgRatio, '/'), `[`, 2)),
                    '| with universe:', if (nrow(with_u)) unique(sapply(strsplit(with_u$BgRatio, '/'), `[`, 2)) else NA, '\n')
# also: a true-signal list under both backgrounds, to show the universe changes which terms come out, not just how many
gene_list <- unique(tab$entrez[tab$hit_signal == 'TRUE'])
sys.source(blk, envir = globalenv()); sig_u <- as.data.frame(ego)
sys.source(tf, envir = globalenv()); sig_n <- as.data.frame(ego)
cat('signal list: terms with universe', nrow(sig_u), '| without', nrow(sig_n), '| shared IDs', length(intersect(sig_u$ID, sig_n$ID)), '\n')
cat('GO:0002181 p.adjust with universe:', if ('GO:0002181' %in% sig_u$ID) signif(sig_u$p.adjust[sig_u$ID == 'GO:0002181'], 3) else NA,
    '| without universe:', if ('GO:0002181' %in% sig_n$ID) signif(sig_n$p.adjust[sig_n$ID == 'GO:0002181'], 3) else NA, '\n')
