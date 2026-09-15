.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Input 1 (Canonical) - MSstats TMP summarization of a MaxQuant evidence.txt, following SKILL.md lines 76-90 verbatim
setwd('F:/OpenScience/audits/bio-proteomics-quantification/data')
suppressPackageStartupMessages(library(MSstats))
cat('MSstats', as.character(packageVersion('MSstats')), '\n')

## ---- Step A: the Skill's reading call, verbatim (default quote = "\"'", comment.char = "#")
ev_skill <- read.table('evidence.txt', sep = '\t', header = TRUE)
pg_skill <- read.table('proteinGroups.txt', sep = '\t', header = TRUE)
cat('read.table (Skill as written): evidence rows =', nrow(ev_skill), '| proteinGroups rows =', nrow(pg_skill), '\n')
## reference: quote = '' and comment.char = '' (what MaxQuant tables need)
ev_ok <- read.table('evidence.txt', sep = '\t', header = TRUE, quote = '', comment.char = '', check.names = TRUE)
pg_ok <- read.table('proteinGroups.txt', sep = '\t', header = TRUE, quote = '', comment.char = '', check.names = TRUE)
cat('read.table (quote=\'\', comment.char=\'\'): evidence rows =', nrow(ev_ok), '| proteinGroups rows =', nrow(pg_ok), '\n')
cat('pandas reference: evidence 10369, proteinGroups 1560\n')
bad <- ev_skill[grepl("'", ev_skill$Protein.names), c('Sequence', 'Protein.names', 'Raw.file', 'Intensity')]
cat('Skill-read rows whose Protein.names contains an apostrophe:', nrow(bad), '\n')
if (nrow(bad)) { cat('first mangled Protein.names value (truncated to 200 chars):\n'); cat(substr(bad$Protein.names[1], 1, 200), '\n') }
lost <- setdiff(unique(ev_ok$Leading.razor.protein), unique(ev_skill$Leading.razor.protein))
cat('proteins present in the correct read but missing from the Skill read:', length(lost), '\n')
cat('Skill-read: raw files =', paste(sort(unique(ev_skill$Raw.file)), collapse = ','), '\n')

annot <- read.csv('annotation_msstats.csv')

## ---- Step B: MaxQtoMSstatsFormat + dataProcess exactly as the Skill writes it (on the Skill's read)
run_pipeline <- function(ev, pg, tag) {
  cat('\n==== pipeline on', tag, '====\n')
  t0 <- Sys.time()
  mi <- tryCatch(MaxQtoMSstatsFormat(evidence = ev, proteinGroups = pg, annotation = annot, use_log_file = FALSE),
                 error = function(e) { cat('MaxQtoMSstatsFormat ERROR:', conditionMessage(e), '\n'); NULL })
  if (is.null(mi)) return(NULL)
  cat('MSstats input rows:', nrow(mi), '| proteins:', length(unique(mi$ProteinName)), '\n')
  pr <- tryCatch(dataProcess(mi, normalization = 'equalizeMedians', summaryMethod = 'TMP',
                             censoredInt = 'NA', MBimpute = FALSE, use_log_file = FALSE),
                 error = function(e) { cat('dataProcess ERROR:', conditionMessage(e), '\n'); NULL })
  if (is.null(pr)) return(NULL)
  pa <- pr$ProteinLevelData
  cat('ProteinLevelData rows:', nrow(pa), '| proteins:', length(unique(pa$Protein)), '| runs:', length(unique(pa$RUN)),
      '| NA LogIntensities:', sum(is.na(pa$LogIntensities)), '| secs:', round(as.numeric(Sys.time() - t0, units = 'secs'), 1), '\n')
  pa
}
pa_skill <- run_pipeline(ev_skill, pg_skill, 'Skill read.table (default quote)')
pa_ok <- run_pipeline(ev_ok, pg_ok, 'quote-safe read.table')

if (!is.null(pa_ok)) {
  wide <- tidyr::pivot_wider(as.data.frame(pa_ok[, c('Protein', 'originalRUN', 'LogIntensities')]),
                             names_from = originalRUN, values_from = LogIntensities)
  cat('\nprotein x run matrix (quote-safe):', nrow(wide), 'x', ncol(wide) - 1, '\n')
  print(head(as.data.frame(wide), 4), digits = 4)
  med <- apply(as.matrix(wide[, -1]), 2, median, na.rm = TRUE)
  cat('per-run median log2 after equalizeMedians:\n'); print(round(med, 3))
  saveRDS(pa_ok, 'F:/OpenScience/audits/bio-proteomics-quantification/runs/in1_protein_level.rds')
  # recovery check against truth: log2FC T-C vs true_log2fc
  truth <- read.csv('truth_proteins.csv')
  m <- as.matrix(wide[, -1]); rownames(m) <- wide$Protein
  lfc <- rowMeans(m[, grep('^T', colnames(m)), drop = FALSE], na.rm = TRUE) - rowMeans(m[, grep('^C', colnames(m)), drop = FALSE], na.rm = TRUE)
  prot1 <- sub(';.*', '', names(lfc))
  tt <- truth[match(prot1, truth$protein), ]
  ok <- is.finite(lfc) & tt$class %in% c('up', 'down', 'null')
  cat('corr(estimated log2FC, true log2FC) over', sum(ok), 'non-on/off proteins:', round(cor(lfc[ok], tt$true_log2fc[ok]), 3), '\n')
  cat('on/off proteins in evidence:', sum(tt$class == 'on_off', na.rm = TRUE),
      '| of which have a finite TMP T-mean:', sum(tt$class == 'on_off' & is.finite(rowMeans(m[, grep('^T', colnames(m)), drop = FALSE], na.rm = TRUE)), na.rm = TRUE), '\n')
}

## ---- Lead 2: where does MSstats' AFT live? (dataProcess vs groupComparison)
cat('\nformals(dataProcess) containing impute/censor:', paste(grep('impute|censor|maxQuantile', names(formals(dataProcess)), value = TRUE), collapse = ', '), '\n')
cat('formals(groupComparison):', paste(names(formals(groupComparison)), collapse = ', '), '\n')
