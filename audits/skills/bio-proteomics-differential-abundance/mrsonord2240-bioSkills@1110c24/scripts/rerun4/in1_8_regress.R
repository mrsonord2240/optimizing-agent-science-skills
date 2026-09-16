# Inputs 1, 2, 3, 5, 8 regression: limma / treat / DEqMS / ashr / proDA blocks
# VERBATIM from the fork's SKILL.md, on the 4v4 batch set and the 6-donor paired set.
suppressPackageStartupMessages({library(limma); library(DEqMS); library(proDA); library(ashr)})
DD <- 'F:/OpenScience/audits/bio-proteomics-differential-abundance/data'
DW <- 'F:/OpenScience/audits/bio-proteomics-differential-abundance/rerun4'
B <- function(f) paste(readLines(file.path(DW, 'blocks', f)), collapse = '\n')

# The only substitution made anywhere below: the contrast level NAMES, because the
# paired set's conditions are LPS/Unstim rather than Treatment/Control. Nothing else
# in any block is altered.
CONTRAST <- c(up = 'Treatment', down = 'Control')
run_blocks <- function(env, files) for (f in files) {
  txt <- B(f)
  txt <- gsub('Treatment - Control',
              paste(CONTRAST[['up']], '-', CONTRAST[['down']]), txt, fixed = TRUE)
  eval(parse(text = txt), envir = env)
}

fdr <- function(sig_names, truth) {
  fp <- sum(truth$class[match(sig_names, truth$protein)] == 'null', na.rm = TRUE)
  c(calls = length(sig_names), fp = fp, fdr = 100 * fp / max(1, length(sig_names)))
}

# ---------------- Input 1/2/5: 4 v 4 with a batch effect -----------------------
cat('=== Inputs 1, 2, 5 (regression): 4v4 proteinGroups with batch ===\n')
pg <- read.table(file.path(DD, 'proteinGroups.txt'), sep = '\t', header = TRUE, quote = '', comment.char = '')
si <- read.csv(file.path(DD, 'sample_annotation.csv'), stringsAsFactors = FALSE)
truth <- read.csv(file.path(DD, 'truth_proteins.csv'), stringsAsFactors = FALSE)
icols <- grep('^LFQ.intensity', colnames(pg), value = TRUE)
if (!length(icols)) icols <- grep('^Intensity\\.', colnames(pg), value = TRUE)
M <- as.matrix(pg[, icols]); rownames(M) <- pg$Majority.protein.IDs
colnames(M) <- sub('^(LFQ\\.intensity\\.|Intensity\\.)', '', icols)
M[M == 0] <- NA; M <- log2(M)
M <- sweep(M, 2, apply(M, 2, median, na.rm = TRUE)) + median(apply(M, 2, median, na.rm = TRUE))
si <- si[match(colnames(M), si[[1]]), ]
sample_info <- data.frame(condition = si$condition, batch = factor(si$batch))
cat('matrix in:', dim(M), '\n')

env <- new.env()
assign('protein_matrix', M, env); assign('sample_info', sample_info, env)
run_blocks(env, 'limma.R')
res <- get('results', env)
cat('after valid-value + estimability filter:', nrow(get('protein_matrix', env)), 'rows\n')
s <- rownames(res)[res$adj.P.Val < 0.05]
cat('limma eBayes(trend, robust):', paste(sprintf('%s=%g', names(fdr(s, truth)), fdr(s, truth)), collapse = ' '), '\n')

run_blocks(env, 'treat.R')
rt <- get('results', env)
st <- rownames(rt)[rt$adj.P.Val < 0.05]
cat('treat(log2(1.2))          :', paste(sprintf('%s=%g', names(fdr(st, truth)), fdr(st, truth)), collapse = ' '), '\n')

pep <- pg$Peptides; names(pep) <- pg$Majority.protein.IDs
assign('psm_count_per_protein', pmax(pep, 1), env)
run_blocks(env, 'deqms.R')
rd <- get('results', env)
sd_ <- rd$gene[rd$sca.adj.pval < 0.05]
if (is.null(sd_)) sd_ <- rownames(rd)[rd$sca.adj.pval < 0.05]
cat('DEqMS spectraCounteBayes  :', paste(sprintf('%s=%g', names(fdr(sd_, truth)), fdr(sd_, truth)), collapse = ' '), '\n')

run_blocks(env, 'fc_report.R')
cat('ashr: shrunk', length(get('shrunken_fc', env)),
    '| PosteriorMean exactly 0:', sum(get('shrunken_fc', env) == 0), '\n')

# ---------------- Input 8: 6 paired donors (pass 3's estimability filter) -------
cat('\n=== Input 8 (regression of the pass-3 P1): 6-donor paired design ===\n')
pd <- read.csv(file.path(DD, 'paired_donor_log2.csv'), row.names = 1, check.names = FALSE)
ps <- read.csv(file.path(DD, 'paired_donor_samples.csv'), stringsAsFactors = FALSE)
pt <- read.csv(file.path(DD, 'paired_donor_truth.csv'), stringsAsFactors = FALSE)
ps <- ps[match(colnames(pd), ps[[1]]), ]
si2 <- data.frame(condition = ps$condition, batch = factor(ps$donor))
e2 <- new.env()
assign('protein_matrix', as.matrix(pd), e2); assign('sample_info', si2, e2)
CONTRAST <- c(up = 'LPS', down = 'Unstim')
run_blocks(e2, 'limma.R')
r2 <- get('results', e2)
cat('rows in', nrow(pd), '-> after filters', nrow(get('protein_matrix', e2)),
    '-> tested', nrow(r2), '\n')
s2 <- rownames(r2)[r2$adj.P.Val < 0.05]
cat('limma paired (donor as batch):', paste(sprintf('%s=%g', names(fdr(s2, pt)), fdr(s2, pt)), collapse = ' '), '\n')
np <- sum(rowSums(is.na(get('fit', e2)$coefficients)) > 0)
cat('  non-estimable rows dropped by the pass-3 filter:',
    nrow(get('protein_matrix', e2)) - nrow(r2), '\n')

cnt <- rowSums(!is.na(pd)); names(cnt) <- rownames(pd)
assign('psm_count_per_protein', pmax(cnt, 1), e2)
run_blocks(e2, 'deqms.R')
rd2 <- get('results', e2)
sd2 <- rd2$gene[rd2$sca.adj.pval < 0.05]
if (is.null(sd2)) sd2 <- rownames(rd2)[rd2$sca.adj.pval < 0.05]
cat('DEqMS paired                 :', paste(sprintf('%s=%g', names(fdr(sd2, pt)), fdr(sd2, pt)), collapse = ' '), '\n')

# what the filter is worth: same fit without it
cat('\n  control: the same design WITHOUT the estimability filter\n')
f3 <- lmFit(as.matrix(pd), model.matrix(~0 + condition + batch, data = si2))
colnames(f3$design)[1:2] <- levels(factor(si2$condition))
cm <- makeContrasts(contrasts = paste(levels(factor(si2$condition))[2], '-', levels(factor(si2$condition))[1]), levels = f3$design)
f4 <- tryCatch(eBayes(contrasts.fit(f3, cm), trend = TRUE, robust = TRUE),
               error = function(e) {cat('   eBayes ERROR:', conditionMessage(e), '\n'); NULL})
if (!is.null(f4)) {
  r4 <- topTable(f4, coef = 1, number = Inf, adjust.method = 'BH')
  s4 <- rownames(r4)[r4$adj.P.Val < 0.05]
  cat('  ', paste(sprintf('%s=%g', names(fdr(s4, pt)), fdr(s4, pt)), collapse = ' '), '\n')
}
