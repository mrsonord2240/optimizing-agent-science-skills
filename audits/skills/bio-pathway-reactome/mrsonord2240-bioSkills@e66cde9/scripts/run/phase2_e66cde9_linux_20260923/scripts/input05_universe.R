root <- '/mnt/openscience/audits/bio-pathway-reactome/run/phase2_e66cde9_linux_20260923'
d <- read.csv(file.path(root,'outputs','ora.csv'))
stopifnot(nrow(d)==20, all(c('BgRatio','FoldEnrichment','p.adjust') %in% names(d)), grepl('/',d$BgRatio[1],fixed=TRUE))
cat('ASSERT universe_result_columns_and_ratio\n')
