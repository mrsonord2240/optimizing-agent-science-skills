# Quant Input 1 (regression): MaxQuant evidence -> MSstats TMP protein matrix. SKILL.md block b01 run verbatim. SYNTHETIC data.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
QQ <- 'F:/OpenScience/audits/bio-proteomics-quantification'
setwd(file.path(QQ, 'rerun', 'work'))
blk <- list.files(file.path(QQ, 'rerun', 'blocks'), pattern = '^b01', full.names = TRUE)
res <- tryCatch({ withCallingHandlers(sys.source(blk, envir = globalenv()),
   warning = function(w) { cat('  [warning]', conditionMessage(w), '\n'); invokeRestart('muffleWarning') }); 'OK' },
   error = function(e) paste('ERROR:', conditionMessage(e)))
cat('[block b01 verbatim]', res, '\n')
cat('evidence rows read:', nrow(evidence), '| data lines in file:', length(readLines('evidence.txt')) - 1,
    '| proteinGroups rows:', nrow(protein_groups), '| lines:', length(readLines('proteinGroups.txt')) - 1, '\n')
pl <- protein_abundance
cat('ProteinLevelData rows:', nrow(pl), '| proteins:', length(unique(pl$Protein)), '| runs:', length(unique(pl$originalRUN)),
    '| NumImputedFeature>0 rows:', sum(pl$NumImputedFeature > 0, na.rm = TRUE), '\n')
med <- tapply(pl$LogIntensities, pl$originalRUN, median, na.rm = TRUE); cat('per-run medians:', round(med, 2), '\n')
truth <- read.csv(file.path(QQ, 'data', 'truth_proteins.csv'))
w <- reshape(pl[, c('Protein', 'originalRUN', 'LogIntensities')], idvar = 'Protein', timevar = 'originalRUN', direction = 'wide')
rownames(w) <- as.character(w$Protein); w <- as.matrix(w[, -1]); colnames(w) <- sub('LogIntensities.', '', colnames(w))
fc <- rowMeans(w[, grep('^T', colnames(w))], na.rm = TRUE) - rowMeans(w[, grep('^C', colnames(w))], na.rm = TRUE)
tt <- truth[match(names(fc), truth$protein), ]; ok <- is.finite(fc) & tt$class != 'on_off'
cat('corr(est log2FC, true) over', sum(ok), 'non-on/off proteins:', round(cor(fc[ok], tt$true_log2fc[ok]), 3), '\n')
saveRDS(processed, file.path(QQ, 'rerun', 'in1_processed.rds'))
cm <- matrix(c(-1, 1), nrow = 1, dimnames = list('T-C', c('Control', 'Treatment')))
gc <- MSstats::groupComparison(contrast.matrix = cm, data = processed, use_log_file = FALSE)$ComparisonResult
cat('groupComparison (MBimpute=FALSE): issue table:', paste(names(table(gc$issue)), table(gc$issue)), '| -Inf log2FC:', sum(gc$log2FC == -Inf, na.rm = TRUE), '\n')
cat('formals(dataProcess) has MBimpute:', 'MBimpute' %in% names(formals(MSstats::dataProcess)), '| formals(groupComparison):', paste(names(formals(MSstats::groupComparison)), collapse = ','), '\n')
