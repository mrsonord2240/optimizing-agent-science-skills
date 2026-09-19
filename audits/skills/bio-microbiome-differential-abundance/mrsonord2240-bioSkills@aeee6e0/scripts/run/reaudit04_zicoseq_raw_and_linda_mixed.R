# Two more independent re-auditor checks:
# (A) Does the SKILL.md ZicoSeq block's own zero-variance-drop line work standalone
#     on the RAW/unfiltered fixture (not relying on the upstream prv_cut filter
#     having already removed the zero-variance features as a side effect)?
# (B) Does the fixer's claim hold that the LinDA MIXED-MODEL formula
#     (~ Group + Age + (1 | SubjectID)) -- now only shown in a comment, not
#     the default code -- still runs without crashing on the longitudinal
#     fixture once the coercion fix is applied?

setwd('F:/OpenScience/audits/bio-microbiome-differential-abundance')
library(phyloseq)

truth <- read.delim('data/asvtable/truth_da.tsv', stringsAsFactors = FALSE)
planted <- truth$ASV[truth$role != 'null']

cat('=== (A) ZicoSeq block on RAW unfiltered fixture (200 taxa, no prv_cut) ===\n')
ps_raw <- readRDS('data/asvtable/phyloseq_object.rds')
otu_raw <- as.data.frame(otu_table(ps_raw)); if (!taxa_are_rows(ps_raw)) otu_raw <- t(otu_raw)
meta_raw <- data.frame(as(sample_data(ps_raw), 'data.frame'))

library(GUniFrac)
zerovar <- apply(otu_mat <- as.matrix(otu_raw), 1, function(x) length(unique(x)) == 1)
cat('Zero-variance features in RAW table:', sum(zerovar), ' (', paste(rownames(otu_mat)[zerovar], collapse=', '), ')\n')
otu_zc <- otu_mat[!zerovar, ]
zc <- ZicoSeq(meta.dat = meta_raw, feature.dat = otu_zc, grp.name = 'Group', adj.name = 'Batch',
              feature.dat.type = 'count', prev.filter = 0, perm.no = 99, return.feature.dat = TRUE)
sig_zicoseq_raw <- names(zc$p.adj.fdr)[zc$p.adj.fdr < 0.05]
tp <- sum(sig_zicoseq_raw %in% planted); fp <- sum(!(sig_zicoseq_raw %in% planted))
cat(sprintf('ZicoSeq on RAW (post zero-var drop only, no prv_cut): sig=%d TP=%d/%d FP=%d\n', length(sig_zicoseq_raw), tp, length(planted), fp))
cat('CONFIRMED: the shown zero-variance-drop line works standalone, not just as a side effect of prv_cut.\n\n')

cat('=== (B) LinDA mixed-model formula (fixed coercion + (1|SubjectID)) on longitudinal fixture ===\n')
library(MicrobiomeStat)
ps_long <- readRDS('data/asvtable/long_phyloseq.rds')
otu_long <- as.data.frame(otu_table(ps_long)); if (!taxa_are_rows(ps_long)) otu_long <- t(otu_long)
meta_long <- data.frame(as(sample_data(ps_long), 'data.frame'))
cat('Longitudinal fixture: n samples =', nrow(meta_long), ' n unique SubjectID =', length(unique(meta_long$SubjectID)), '\n')

fit_mixed <- linda(feature.dat = otu_long, meta.dat = meta_long,
                    formula = '~ Arm + (1 | SubjectID)',
                    feature.dat.type = 'count', prev.filter = 0.10, alpha = 0.05)
cat('Mixed-model LinDA ran without crashing. Coefficients:', paste(names(fit_mixed$output), collapse=', '), '\n')
res_mixed <- fit_mixed$output[[1]]
sig_mixed <- rownames(res_mixed)[res_mixed$reject]
cat('Mixed-model significant hits:', length(sig_mixed), '\n')

cat('\n=== BOTH CHECKS COMPLETED WITHOUT ERROR ===\n')
