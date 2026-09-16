# Input 1 (regression): MaxQuant LFQ 4 v 4 with two acquisition days. SYNTHETIC data.
source('F:/OpenScience/audits/bio-proteomics-differential-abundance/rerun/common.R')
truth <- read.csv(file.path(RR, 'data', 'truth_proteins.csv'))
mq <- load_maxquant_lfq()
sample_info <- read.csv(file.path(RR, 'data', 'sample_annotation.csv'))
protein_matrix <- mq$matrix[, sample_info$sample]
cat('matrix before Skill filter:', dim(protein_matrix), '| all-NA rows:', sum(rowSums(!is.na(protein_matrix)) == 0), '\n')
all_rows <- rownames(protein_matrix)

run_block('b01')   # limma block verbatim (valid-value filter, design with batch, eBayes trend+robust, topTable)
cat('rows after Skill valid-value filter:', nrow(protein_matrix), '| design cols:', paste(colnames(design), collapse = ','), '\n')
removed <- setdiff(all_rows, rownames(protein_matrix))
rc <- truth$class[match(removed, truth$protein)]
cat('removed by filter:', length(removed), '| by class:', paste(names(table(rc)), table(rc), collapse = ' '), '\n')
truth_eval(rownames(results)[results$adj.P.Val < 0.05], truth, 'limma trend+robust ~0+condition+batch BH<0.05')
cat('prior df range:', range(fit2$df.prior), '| s2.prior varies with intensity:', length(unique(round(fit2$s2.prior, 6))) > 1, '\n')

run_block('b02')   # treat block verbatim
truth_eval(rownames(results)[results$adj.P.Val < 0.05], truth, 'treat(lfc=log2 1.2, trend, robust) BH<0.05')
cat('fit_treat df.prior median:', median(fit_treat$df.prior), '\n')

psm_count_per_protein <- mq$peptides
run_block('b03')   # DEqMS block verbatim
truth_eval(rownames(results)[results$sca.adj.pval < 0.05], truth, 'DEqMS (Razor+unique peptides) sca.adj.pval<0.05')

run_block('b06')   # ashr block verbatim
cat('ashr: shrunk', length(shrunken_fc), 'of', nrow(fit2), '| PosteriorMean exactly 0:', sum(shrunken_fc == 0), '\n')

# Report the removed-by-filter proteins separately, as the Approach text directs
res_tab <- topTable(fit2, coef = 1, number = Inf, adjust.method = 'BH')
cond <- factor(sample_info$condition)
onoff <- removed[rowSums(!is.na(mq$matrix[removed, sample_info$sample[cond == 'Control'], drop = FALSE])) >= 3 &
                 rowSums(!is.na(mq$matrix[removed, sample_info$sample[cond == 'Treatment'], drop = FALSE])) == 0]
oc <- truth$class[match(onoff, truth$protein)]
cat('detected in >=3/4 Control, 0/4 Treatment:', length(onoff), '| classes:', paste(names(table(oc)), table(oc), collapse = ' '), '\n')
write.csv(res_tab, file.path(RR, 'rerun', 'in1_limma_results.csv'))
