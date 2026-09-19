.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(demuxmix))
suppressPackageStartupMessages(library(tools))
db <- Rd_db('demuxmix')
rd <- db[['demuxmix.Rd']]
if (is.null(rd)) rd <- db[[grep('demuxmix', names(db), value = TRUE)[1]]]
Rd2txt(rd)
