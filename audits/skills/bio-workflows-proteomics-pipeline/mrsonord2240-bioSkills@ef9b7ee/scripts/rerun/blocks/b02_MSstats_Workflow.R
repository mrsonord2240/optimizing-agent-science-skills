library(MSstats)

# From MaxQuant. quote = '' and comment.char = '' are REQUIRED: MaxQuant text fields contain
# apostrophes (5'-nucleotidase) and '#', and the read.table defaults silently truncate the table
# with nothing but an 'EOF within quoted string' warning -- here 2954 of 10369 evidence rows and
# 62 of 296 proteins. Check the row count; do not trust the warning to stop you.
evidence <- read.table('evidence.txt', sep = '\t', header = TRUE, quote = '', comment.char = '')
proteinGroups <- read.table('proteinGroups.txt', sep = '\t', header = TRUE, quote = '', comment.char = '')
stopifnot(nrow(evidence) == length(readLines('evidence.txt')) - 1,
          nrow(proteinGroups) == length(readLines('proteinGroups.txt')) - 1)
annotation <- read.csv('annotation.csv')

# Convert to MSstats format
msstats_input <- MaxQtoMSstatsFormat(evidence = evidence,
                                      proteinGroups = proteinGroups,
                                      annotation = annotation)

# Process data
processed <- dataProcess(msstats_input, normalization = 'equalizeMedians',
                         summaryMethod = 'TMP', censoredInt = 'NA')

# Comparison. +1 on the numerator: Treatment=+1, Control=-1 so log2FC = Treatment - Control
# (positive = up in Treatment), matching the label and the limma makeContrasts(Treatment-Control) path.
comparison <- matrix(c(-1, 1), nrow = 1)
rownames(comparison) <- 'Treatment_vs_Control'
colnames(comparison) <- c('Control', 'Treatment')

results <- groupComparison(contrast.matrix = comparison, data = processed)
