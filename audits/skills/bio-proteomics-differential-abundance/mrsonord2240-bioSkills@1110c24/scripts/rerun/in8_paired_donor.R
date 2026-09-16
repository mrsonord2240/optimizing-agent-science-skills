# Input 8 (NEW, variant): paired donor design (6 donors x Unstim/LPS), DEqMS with peptide counts. SYNTHETIC data.
source('F:/OpenScience/audits/bio-proteomics-differential-abundance/rerun/common.R')
X <- as.matrix(read.csv(file.path(RR, 'data', 'paired_donor_log2.csv'), row.names = 1))
sample_info <- read.csv(file.path(RR, 'data', 'paired_donor_samples.csv'))
truth <- read.csv(file.path(RR, 'data', 'paired_donor_truth.csv'))
sample_info$condition <- factor(sample_info$condition, levels = c('Unstim', 'LPS'))
sample_info$batch <- factor(sample_info$donor)   # donor is the blocking factor: goes where the Skill puts batch
protein_matrix <- X[, sample_info$sample]
cat('proteins:', nrow(X), '| missing %:', round(100 * mean(is.na(X)), 1), '\n')

# Skill limma block with the contrast line renamed to this study's levels (LPS - Unstim)
src <- sub('makeContrasts(Treatment - Control, levels = design)', 'makeContrasts(LPS - Unstim, levels = design)',
           readLines(list.files(BLK, pattern = '^b01', full.names = TRUE)), fixed = TRUE)
tf <- tempfile(fileext = '.R'); writeLines(src, tf)
withCallingHandlers(sys.source(tf, envir = globalenv()), warning = function(w) { cat('  [warning]', conditionMessage(w), '\n'); invokeRestart('muffleWarning') })
cat('paired design columns:', paste(colnames(design), collapse = ','), '| rows after filter:', nrow(fit2),
    '| df.residual==0 rows:', sum(fit2$df.residual == 0), '| NA coefficient rows:', sum(is.na(fit2$coefficients[, 1])), '\n')
truth_eval(rownames(results)[results$adj.P.Val < 0.05], truth, 'limma paired (donor in design) BH<0.05')
paired_fit <- fit2

psm_count_per_protein <- setNames(truth$peptides, truth$protein)
run_block('b03')   # DEqMS block verbatim (stopifnot df.residual > 0)

# Adaptation: keep rows with >=1 residual df and estimable contrast, then re-run the DEqMS block
keep <- rownames(paired_fit)[paired_fit$df.residual > 0 & !is.na(paired_fit$coefficients[, 1])]
fit2 <- paired_fit[keep, ]
fit2 <- eBayes(fit2, trend = TRUE, robust = TRUE)
run_block('b03')
if (exists('fit3')) truth_eval(rownames(results)[results$sca.adj.pval < 0.05], truth, 'DEqMS paired, df>0 rows sca.adj.pval<0.05')

# Unpaired comparison (what happens if donor is ignored)
d0 <- model.matrix(~0 + condition, data = sample_info); colnames(d0) <- levels(sample_info$condition)
f0 <- eBayes(contrasts.fit(lmFit(protein_matrix, d0), makeContrasts(LPS - Unstim, levels = d0)), trend = TRUE, robust = TRUE)
t0 <- topTable(f0, number = Inf)
truth_eval(rownames(t0)[t0$adj.P.Val < 0.05], truth, 'limma UNPAIRED (donor ignored) BH<0.05')
