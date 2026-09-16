# Pipeline Input 2 (variant): DIA-NN 1.9 report.parquet -> SKILL.md "DIA-NN Workflow" block verbatim, then limma as the text directs. SYNTHETIC.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(limma))
PP <- 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline'
setwd(file.path(PP, 'runs', 'work2'))
blk <- list.files(file.path(PP, 'runs', 'blocks'), pattern = '^b05', full.names = TRUE)
res <- tryCatch({ suppressMessages(sys.source(blk, envir = globalenv())); 'OK' }, error = function(e) paste('ERROR:', conditionMessage(e)))
cat('[DIA-NN block verbatim]', res, '\n')
m <- as.data.frame(protein_matrix); rownames(m) <- m$Protein.Group; m <- as.matrix(m[, -1])
cat('matrix:', dim(m), '| LOWCONF groups:', sum(grepl('^LOWCONF', rownames(m))), '| zero cells:', sum(m == 0, na.rm = TRUE), '\n')
L <- log2(m)   # "PG.MaxLFQ path: log2-transform and go straight to limma"
cat('-Inf cells after log2 as directed:', sum(is.infinite(L)), '\n')
si <- read.csv('sample_annotation.csv'); cn <- sub('_DIA$', '', colnames(L)); colnames(L) <- cn
si <- si[match(cn, si$sample), ]; si$condition <- factor(si$condition)
d <- model.matrix(~0 + condition + batch, data = si); colnames(d)[1:2] <- levels(si$condition)
fit <- tryCatch(eBayes(contrasts.fit(lmFit(L, d), makeContrasts(conditionTreatment = Treatment - Control, levels = d)), trend = TRUE, robust = TRUE),
                error = function(e) { cat('limma on the -Inf matrix ERROR:', conditionMessage(e), '\n'); NULL })
L2 <- L; L2[is.infinite(L2)] <- NA
fit2 <- eBayes(contrasts.fit(lmFit(L2, d), makeContrasts(Treatment - Control, levels = d)), trend = FALSE)
tt <- topTable(fit2, number = Inf); truth <- read.csv(file.path(PP, 'data', 'truth_proteins.csv'), na.strings = character(0))
s <- rownames(tt)[tt$adj.P.Val < 0.05]; cl <- truth$class[match(s, truth$protein)]
cat('after agent 0 -> NA: limma BH<0.05', length(s), '| null', sum(cl == 'null', na.rm = TRUE), '\n')
