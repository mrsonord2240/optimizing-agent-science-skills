# INPUT 4 (Variant B) - "Convert my expression matrix into a per-sample
# pathway-activity matrix with GSVA so I can cluster samples and correlate the
# scores with survival." (verbatim from the Skill's usage-guide Example Prompts)
#
# Code = SKILL.md "Per-Sample Scores: ssGSEA and GSVA" block, VERBATIM.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
D <- 'F:/OpenScience/audits/bio-pathway-gsea/data'; R <- 'F:/OpenScience/audits/bio-pathway-gsea/runs'
suppressPackageStartupMessages({library(msigdbr)})
cat('GSVA installed version:', as.character(packageVersion('GSVA')),
    '(SKILL.md says ">= 1.50 uses the parameter-object API" and that GSVA is',
    'not installed in its own reference environment)\n')

expr_matrix <- as.matrix(read.csv(file.path(D, 'SYNTHETIC_logcpm_matrix.csv'), row.names = 1))
meta <- read.csv(file.path(D, 'SYNTHETIC_sample_metadata.csv'))
cat('SYNTHETIC logCPM matrix:', nrow(expr_matrix), 'genes x', ncol(expr_matrix), 'samples;',
    'groups:', paste(table(meta$group), names(table(meta$group)), collapse=' / '), '\n')

h <- msigdbr(species = 'Homo sapiens', collection = 'H')
gene_sets <- split(as.character(h$ncbi_gene), h$gs_name)
gene_sets <- lapply(gene_sets, function(g) intersect(unique(g), rownames(expr_matrix)))
gene_sets <- gene_sets[lengths(gene_sets) >= 10]
cat('Hallmark sets with >=10 genes on this matrix:', length(gene_sets), '\n\n')

# ---------------- SKILL.md block, VERBATIM --------------------------------
# GSVA >= 1.50 / Bioc 3.18 parameter-object API (older method= signature errors)
library(GSVA)
gsva_scores  <- gsva(gsvaParam(expr_matrix, gene_sets))      # unsupervised per-sample set scores
ssgsea_scores <- gsva(ssgseaParam(expr_matrix, gene_sets))   # ssGSEA via the same dispatch
# ---------------------------------------------------------------------------
cat('\ngsva_scores  :', nrow(gsva_scores), 'sets x', ncol(gsva_scores), 'samples | class',
    class(gsva_scores)[1], '\n')
cat('ssgsea_scores:', nrow(ssgsea_scores), 'sets x', ncol(ssgsea_scores), 'samples\n')

# The SKILL.md says the OLD signature errors - check that claim directly.
old <- tryCatch({ gsva(expr_matrix, gene_sets, method = 'ssgsea'); 'old signature WORKED' },
                error = function(e) paste('old signature ERROR:', conditionMessage(e)))
cat('\n[claim check]', substr(old, 1, 160), '\n')

# Does the per-sample score carry the planted contrast? (no p-value is produced)
g <- meta$group[match(colnames(gsva_scores), meta$sample)]
for (nm in c('HALLMARK_OXIDATIVE_PHOSPHORYLATION','HALLMARK_E2F_TARGETS')) {
  s <- gsva_scores[nm, ]
  cat(sprintf('\n%s\n  GSVA   control mean %+.3f | treated mean %+.3f | delta %+.3f\n',
      nm, mean(s[g=='control']), mean(s[g=='treated']), mean(s[g=='treated'])-mean(s[g=='control'])))
  s2 <- ssgsea_scores[nm, ]
  cat(sprintf('  ssGSEA control mean %+.3f | treated mean %+.3f | delta %+.3f\n',
      mean(s2[g=='control']), mean(s2[g=='treated']), mean(s2[g=='treated'])-mean(s2[g=='control'])))
}
cat('\nAny per-set p-value column produced by gsva()?',
    is.matrix(gsva_scores) || inherits(gsva_scores,'ExpressionSet'),
    '-> output is a score matrix only, as the SKILL.md states\n')

# downstream use the user asked for: clustering
hc <- hclust(dist(t(gsva_scores)))
cat('\nhierarchical clustering of samples on GSVA scores, 2-group cut vs true labels:\n')
print(table(cut = cutree(hc, 2), truth = g))
write.csv(gsva_scores,   file.path(R, 'in4_gsva_scores.csv'))
write.csv(ssgsea_scores, file.path(R, 'in4_ssgsea_scores.csv'))
cat('\nEXIT OK\n')
