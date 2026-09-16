# Input 9 regression: the MSstats feature-level block VERBATIM, plus the
# MBimpute comparison and the msqrobAggregate peptide-level block.
suppressPackageStartupMessages({library(MSstats); library(QFeatures); library(msqrob2); library(MsCoreUtils)})
DD <- 'F:/OpenScience/audits/bio-proteomics-differential-abundance/data'
DW <- 'F:/OpenScience/audits/bio-proteomics-differential-abundance/rerun4'
truth <- read.csv(file.path(DD, 'truth_proteins.csv'), stringsAsFactors = FALSE)
isnull <- setNames(truth$class == 'null', truth$protein)

evidence <- read.table(file.path(DD, 'evidence.txt'), sep = '\t', header = TRUE,
                       quote = '', comment.char = '')
protein_groups <- read.table(file.path(DD, 'proteinGroups.txt'), sep = '\t', header = TRUE,
                             quote = '', comment.char = '')
annotation <- read.csv(file.path(DD, 'annotation_msstats.csv'), stringsAsFactors = FALSE)

cat('=== MSstats block verbatim (MBimpute = FALSE, as shipped) ===\n')
env <- new.env()
for (v in c('evidence', 'protein_groups', 'annotation')) assign(v, get(v), env)
suppressMessages(suppressWarnings(sys.source(file.path(DW, 'blocks', 'msstats.R'), envir = env)))
tested <- get('tested', env); undet <- get('undetected', env)
tested$null <- isnull[tested$Protein]
sig <- tested[tested$adj.pvalue < 0.05, ]
fp <- sum(sig$null, na.rm = TRUE)
cat(sprintf('tested %d | oneConditionMissing %d | calls %d | FP %d | realized FDR %.1f%% | median log2FC %+0.3f\n',
            nrow(tested), nrow(undet), nrow(sig), fp, 100 * fp / max(1, nrow(sig)),
            median(tested$log2FC, na.rm = TRUE)))
cat('true up/dn among calls:', sum(!sig$null & sig$log2FC > 0, na.rm = TRUE), '/',
    sum(!sig$null & sig$log2FC < 0, na.rm = TRUE), '\n')
cat('infinite log2FC rows in the full result:',
    sum(!is.finite(get('res', env)$log2FC)), '\n')

cat('\n=== the same route with MBimpute = TRUE (the auditor 21.2% setting) ===\n')
input <- MaxQtoMSstatsFormat(evidence = evidence, proteinGroups = protein_groups,
                             annotation = annotation, use_log_file = FALSE)
proc2 <- suppressMessages(dataProcess(input, normalization = 'equalizeMedians', summaryMethod = 'TMP',
                                      censoredInt = 'NA', MBimpute = TRUE, use_log_file = FALSE))
contrast <- matrix(c(-1, 1), nrow = 1, dimnames = list('Treatment-Control', c('Control', 'Treatment')))
r2 <- suppressMessages(groupComparison(contrast.matrix = contrast, data = proc2,
                                       use_log_file = FALSE)$ComparisonResult)
r2$Protein <- as.character(r2$Protein)
t2 <- r2[is.finite(r2$log2FC) & !is.na(r2$adj.pvalue), ]
t2$null <- isnull[t2$Protein]
s2 <- t2[t2$adj.pvalue < 0.05, ]
cat(sprintf('tested %d | calls %d | FP %d | realized FDR %.1f%% | median log2FC %+0.3f\n',
            nrow(t2), nrow(s2), sum(s2$null, na.rm = TRUE),
            100 * sum(s2$null, na.rm = TRUE) / max(1, nrow(s2)), median(t2$log2FC, na.rm = TRUE)))

cat('\n=== the centring guard on the MSstats table ===\n')
CENT <- paste(readLines(file.path(DW, 'blocks', 'centring.R')), collapse = '\n')
g <- new.env(); assign('tested', tested, g)
cat(tryCatch({eval(parse(text = CENT), envir = g); 'PASSES'},
             error = function(e) paste('STOPS:', conditionMessage(e))), '\n')

cat('\n=== msqrobAggregate peptide-level block verbatim ===\n')
ann <- annotation
ev <- evidence[!(evidence$Reverse %in% '+') & !(evidence$Potential.contaminant %in% '+') &
                 !is.na(evidence$Intensity) & evidence$Intensity > 0, ]
ev$feature <- paste(ev$Modified.sequence, ev$Charge, sep = '_')
runs <- as.character(ann$Raw.file)
agg <- aggregate(Intensity ~ feature + Raw.file + Leading.razor.protein, data = ev, FUN = sum)
wide <- reshape(agg, idvar = c('feature', 'Leading.razor.protein'), timevar = 'Raw.file', direction = 'wide')
colnames(wide) <- sub('Intensity.', '', colnames(wide), fixed = TRUE)
peptide_wide <- wide[, c('feature', 'Leading.razor.protein', runs)]
names(peptide_wide)[2] <- 'protein'
sample_info <- data.frame(run = runs, condition = ann$Condition, stringsAsFactors = FALSE)
e2 <- new.env()
assign('peptide_wide', peptide_wide, e2); assign('sample_info', sample_info, e2); assign('runs', runs, e2)
suppressMessages(suppressWarnings(sys.source(file.path(DW, 'blocks', 'msqrob2.R'), envir = e2)))
summ <- get('res', e2)
summ$null <- isnull[summ$protein]
ss <- summ[!is.na(summ$adjPval) & summ$adjPval < 0.05, ]
cat(sprintf('summarized msqrob:      tested %3d | calls %3d | FP %2d | median posterior df %.1f\n',
            nrow(summ), nrow(ss), sum(ss$null, na.rm = TRUE), median(summ$df, na.rm = TRUE)))
ok <- tryCatch({
  suppressMessages(suppressWarnings(sys.source(file.path(DW, 'blocks', 'msqrob_aggregate.R'), envir = e2)))
  TRUE}, error = function(e) {cat('msqrobAggregate ERROR:', conditionMessage(e), '\n'); FALSE})
if (ok) {
  pe <- get('pe', e2)
  r3 <- rowData(pe[['proteinLmer']])$conditionTreatment
  r3$protein <- rownames(pe[['proteinLmer']])
  r3$null <- isnull[r3$protein]
  r3 <- r3[!is.na(r3$adjPval), ]
  s3 <- r3[r3$adjPval < 0.05, ]
  cat(sprintf('msqrobAggregate (lmer): tested %3d | calls %3d | FP %2d | median posterior df %.1f | median logFC %+0.3f\n',
              nrow(r3), nrow(s3), sum(s3$null, na.rm = TRUE), median(r3$df, na.rm = TRUE),
              median(r3$logFC, na.rm = TRUE)))
}

cat('\n=== the ridge = TRUE claim on a two-group design ===\n')
cat(tryCatch({
  suppressMessages(msqrobAggregate(get('pe', e2), i = 'peptideLog', fcol = 'protein',
                                   name = 'ridgeTest', formula = ~condition + (1 | sample) + (1 | feature),
                                   ridge = TRUE)); 'NO ERROR'},
  error = function(e) paste('ERROR:', conditionMessage(e))), '\n')
