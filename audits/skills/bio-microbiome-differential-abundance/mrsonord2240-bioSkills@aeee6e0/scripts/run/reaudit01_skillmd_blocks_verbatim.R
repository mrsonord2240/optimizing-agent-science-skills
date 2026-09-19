# Re-audit: run every code block from the FIXED SKILL.md verbatim, in the order
# they appear, against the real fixture (phyloseq_object.rds, 200 taxa x 40
# samples, 17 planted DA taxa). Blocks are copy-pasted from
# F:\OpenScience\wt\mb-da\microbiome\differential-abundance\SKILL.md exactly as
# written (only file paths and truth-loading are re-auditor additions).

setwd('F:/OpenScience/audits/bio-microbiome-differential-abundance')
truth <- read.delim('data/asvtable/truth_da.tsv', stringsAsFactors = FALSE)
truth$true_fc_treated_vs_control <- as.numeric(truth$true_fc_treated_vs_control)
planted <- truth$ASV[truth$role != 'null']
cat('Planted DA taxa (from truth_da.tsv):', length(planted), '\n')

score <- function(hits, label) {
  tp <- sum(hits %in% planted)
  fp <- sum(!(hits %in% planted))
  fn <- length(planted) - tp
  cat(sprintf('%-14s sig=%d  TP=%d/%d  FP=%d  FN=%d\n', label, length(hits), tp, length(planted), fp, fn))
  invisible(list(tp = tp, fp = fp, fn = fn))
}

## ---- Filter Before Testing (verbatim) ----
library(phyloseq)
ps <- readRDS('data/asvtable/phyloseq_object.rds')
# prv_cut 0.10: a feature must appear in >= 10% of samples; raising to 0.25 removes more tests
# (smaller BH correction, more power on survivors) but discards rare-but-real taxa - a declared choice
keep <- filter_taxa(ps, function(x) sum(x > 0) >= 0.10 * nsamples(ps), TRUE)
cat('Taxa after prv_cut=0.10 filter:', ntaxa(keep), '(from', ntaxa(ps), ')\n\n')
ps <- keep   # re-auditor addition: use the filtered object downstream, as the Skill's own flow implies

## ---- ALDEx2 (verbatim) ----
cat('=== ALDEx2 ===\n')
library(ALDEx2)
counts <- as.matrix(otu_table(ps))            # integer counts, taxa in ROWS
if (!taxa_are_rows(ps)) counts <- t(counts)
groups <- as.character(sample_data(ps)$Group)

set.seed(42)   # required for bit-reproducible results run-to-run, not just a larger mc.samples
# mc.samples 128: standard Monte-Carlo draws; 256+ for publication (more stable expected p)
res <- aldex(counts, groups, mc.samples = 128, test = 't', effect = TRUE, denom = 'all')
# we.eBH = Welch expected BH-adjusted p (report this, NOT we.ep); wi.eBH = Wilcoxon equivalent
# effect = median standardized effect = median(diff.btw / max(diff.win)); the primary decision variable
hits <- res[res$we.eBH < 0.05 & abs(res$effect) > 1, ]   # q AND effect floor (Gloor: gate on effect, not p alone)
sig_aldex_v1 <- rownames(hits)
score(sig_aldex_v1, 'ALDEx2 (run1)')

# re-auditor addition: reproducibility check -- re-run with the SAME seed and confirm bit-identical hits
set.seed(42)
res_rep <- aldex(counts, groups, mc.samples = 128, test = 't', effect = TRUE, denom = 'all')
hits_rep <- res_rep[res_rep$we.eBH < 0.05 & abs(res_rep$effect) > 1, ]
sig_aldex_v2 <- rownames(hits_rep)
cat('ALDEx2 seed=42 reproducibility: identical hit set across 2 runs =', identical(sort(sig_aldex_v1), sort(sig_aldex_v2)),
    '; identical effect column =', identical(res$effect, res_rep$effect), '\n\n')

## ---- ANCOM-BC2 (verbatim) ----
cat('=== ANCOM-BC2 ===\n')
library(ANCOMBC)
out <- ancombc2(data = ps, fix_formula = 'Group + Age + Sex',
                rand_formula = NULL,        # '(1 | SubjectID)' for repeated measures - see Failure Modes
                p_adj_method = 'BH',        # DEFAULT is 'holm'; set 'BH' deliberately for FDR
                prv_cut = 0.10, lib_cut = 1000,
                group = 'Group', struc_zero = TRUE, pseudo_sens = TRUE,
                global = FALSE, pairwise = FALSE, n_cl = 2)
res2 <- out$res
dcol <- grep('^diff_Group', names(res2), value = TRUE)[1]
robust <- res2[res2[[dcol]] & res2[[sub('^diff_', 'passed_ss_', dcol)]], ]
sig_ancombc <- robust$taxon
score(sig_ancombc, 'ANCOM-BC2')
cat('\n')

## ---- LinDA (verbatim, FIXED) ----
cat('=== LinDA (fixed coercion + fixed-effects-only formula) ===\n')
library(MicrobiomeStat)
otu <- as.data.frame(otu_table(ps)); if (!taxa_are_rows(ps)) otu <- t(otu)
# as.data.frame(sample_data(ps)) alone keeps phyloseq's S4 "sample_data" class (it is an
# identity op, not a real coercion) and linda() dies deep inside on that; force a true data.frame:
meta <- data.frame(as(sample_data(ps), 'data.frame'))
fit <- linda(feature.dat = otu, meta.dat = meta,
             formula = '~ Group + Age',   # add '+ (1 | SubjectID)' for repeated/paired samples -> mixed model
             feature.dat.type = 'count', prev.filter = 0.10, alpha = 0.05)
result_tab <- fit$output[[1]]   # names(fit$output) are the model-matrix coefficient columns (e.g. 'Grouptreated' - the factor level keeps its case); per-feature: log2FoldChange, lfcSE, stat, pvalue, padj, reject
cat('LinDA ran without crashing. Coefficient used:', names(fit$output)[1], '\n')
sig_linda <- rownames(result_tab)[result_tab$reject]
score(sig_linda, 'LinDA (fixed)')
cat('\n')

## ---- MaAsLin2 (verbatim) ----
cat('=== MaAsLin2 ===\n')
library(Maaslin2)
otu_cols <- as.data.frame(t(otu))
sink(tempfile())  # suppress Maaslin2's very verbose internal logging
fit_m2 <- Maaslin2(input_data = otu_cols, input_metadata = meta,
                output = tempfile('maaslin2_out'), fixed_effects = c('Group', 'Age'),
                random_effects = c('SubjectID'),
                normalization = 'TSS', transform = 'LOG', analysis_method = 'LM',
                min_prevalence = 0.10, max_significance = 0.05)
sink()
m2res <- fit_m2$results
m2res_group <- m2res[m2res$metadata == 'Group', ]
sig_maaslin2 <- m2res_group$feature[m2res_group$qval < 0.05]
score(sig_maaslin2, 'MaAsLin2')
cat('\n')

## ---- MaAsLin3 (verbatim) ----
cat('=== MaAsLin3 ===\n')
library(maaslin3)
sink(tempfile())
fit3 <- maaslin3(input_data = as.data.frame(t(otu)), input_metadata = meta,
                 output = tempfile('maaslin3_out'), fixed_effects = c('Group'),
                 normalization = 'TSS', transform = 'LOG',
                 plot_summary_plot = FALSE, plot_associations = FALSE)
sink()
res3 <- fit3$fit_data_abundance$results
res3 <- res3[res3$metadata == 'Group', ]
sig_maaslin3 <- res3$feature[res3$qval_individual < 0.05]
score(sig_maaslin3, 'MaAsLin3')
cat('\n')

## ---- ZicoSeq (verbatim, FIXED) ----
cat('=== ZicoSeq (fixed: zero-variance drop) ===\n')
library(GUniFrac)
zerovar <- apply(otu_mat <- as.matrix(otu), 1, function(x) length(unique(x)) == 1)
cat('Zero-variance features found after prv_cut=0.10 filter already applied upstream:', sum(zerovar), '\n')
otu_zc <- otu_mat[!zerovar, ]   # ZicoSeq crashes on zero-variance features - see Common Errors
zc <- ZicoSeq(meta.dat = meta, feature.dat = otu_zc, grp.name = 'Group', adj.name = 'Batch',
              feature.dat.type = 'count', prev.filter = 0, perm.no = 99, return.feature.dat = TRUE)
sig_zicoseq <- names(zc$p.adj.fdr)[zc$p.adj.fdr < 0.05]
score(sig_zicoseq, 'ZicoSeq')
cat('\n')

## ---- DESeq2 (verbatim caveat block) ----
cat('=== DESeq2 (caveat-only) ===\n')
library(DESeq2)
dds <- phyloseq_to_deseq2(ps, ~ Group)
dds <- estimateSizeFactors(dds, type = 'poscounts')   # NOT the default median-of-ratios - that is what collapses on zeros
dds <- suppressMessages(DESeq(dds))
sig_deseq2 <- rownames(results(dds, alpha = 0.05))[which(results(dds)$padj < 0.05)]
score(sig_deseq2, 'DESeq2')
cat('\n')

## ---- Consensus (verbatim) ----
cat('=== Consensus (ALDEx2 x LinDA, as the Skill\'s own Consensus block shows) ===\n')
sig_aldex <- sig_aldex_v1
confident  <- intersect(sig_aldex, sig_linda)   # high-confidence
exploratory <- union(sig_aldex, sig_linda)       # report with the tool that found each
score(confident, 'Consensus')
cat('Exploratory (union) size:', length(exploratory), '\n')

cat('\n=== ALL BLOCKS COMPLETED WITHOUT ERROR ===\n')
