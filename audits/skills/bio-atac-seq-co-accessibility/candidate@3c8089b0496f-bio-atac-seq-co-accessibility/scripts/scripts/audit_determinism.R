# Audit run: repeat the shipped run_cicero_pipeline() (chr1-only genome_df substitution, no seed set by the Skill)
# and compare with the first run (evidence res_chr1.rds). Tests result determinism without any seed.
suppressPackageStartupMessages({library(Matrix)})
CO <- Sys.getenv("CO"); SKILL <- Sys.getenv("SKILL")
W <- file.path(CO, "work", "audit_det"); dir.create(W, recursive=TRUE, showWarnings=FALSE); setwd(W)
file.copy(file.path(CO, "work/patched/gencode_v29_protein_coding_tss.bed"), ".", overwrite=TRUE)
src <- readLines(file.path(SKILL, "scripts/cicero_workflow.R"))
src <- src[seq_len(grep("^args <- commandArgs", src)[1] - 1)]
n <- grep("chrs <- chrs\\[!grepl", src); stopifnot(length(n) == 1)
src[n] <- paste0(src[n], "; chrs <- chrs[chrs=='chr1']")
eval(parse(text=src))
m <- readRDS(file.path(CO, "work/input/peak_matrix.rds"))
pm <- read.delim(file.path(CO, "work/input/peak_metadata.tsv"), row.names=1)
cm <- read.delim(file.path(CO, "work/input/cell_metadata.tsv"), row.names=1)
res <- run_cicero_pipeline(m, pm, cm, output_prefix="rep2")
saveRDS(res, "res_rep2.rds")
a <- readRDS(file.path(CO, "work/chr1/res_chr1.rds"))$conns
b <- res$conns
key <- function(d) paste(d$Peak1, d$Peak2)
ka <- key(a); kb <- key(b)
common <- intersect(ka, kb)
ia <- match(common, ka); ib <- match(common, kb)
sa <- a$coaccess[ia]; sb <- b$coaccess[ib]
ok <- !is.na(sa) & !is.na(sb)
cat(sprintf("DET rows run1=%d run2=%d common=%d\n", nrow(a), nrow(b), length(common)))
cat(sprintf("DET strong run1=%d run2=%d\n", sum(a$coaccess > 0.25, na.rm=TRUE), sum(b$coaccess > 0.25, na.rm=TRUE)))
cat(sprintf("DET pearson=%.4f spearman=%.4f maxabsdiff=%.4f identical=%s\n", cor(sa[ok], sb[ok]), cor(sa[ok], sb[ok], method="spearman"),
            max(abs(sa[ok]-sb[ok])), isTRUE(all.equal(sa[ok], sb[ok]))))
sa_set <- ka[a$coaccess > 0.25 & !is.na(a$coaccess)]; sb_set <- kb[b$coaccess > 0.25 & !is.na(b$coaccess)]
cat(sprintf("DET strong-set jaccard=%.4f\n", length(intersect(sa_set, sb_set)) / length(union(sa_set, sb_set))))
