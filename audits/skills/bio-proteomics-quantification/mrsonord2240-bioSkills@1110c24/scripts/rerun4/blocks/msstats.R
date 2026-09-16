library(MSstats)

# quote = '' and comment.char = '': MaxQuant text fields contain apostrophes (5'-nucleotidase); default
# quoting silently truncates the table with only an 'EOF within quoted string' warning
evidence <- read.table('evidence.txt', sep = '\t', header = TRUE, quote = '', comment.char = '')
protein_groups <- read.table('proteinGroups.txt', sep = '\t', header = TRUE, quote = '', comment.char = '')
stopifnot(nrow(evidence) == length(readLines('evidence.txt')) - 1)  # every data line was read

maxquant_input <- MaxQtoMSstatsFormat(
    evidence = evidence,
    proteinGroups = protein_groups,
    annotation = read.csv('annotation.csv')
)

# TMP = Tukey median polish. MBimpute = FALSE: no censoring model (censoredInt has no effect), and on/off
# proteins later come out of groupComparison as log2FC -Inf / issue 'oneConditionMissing'.
# MBimpute = TRUE is the AFT censored-imputation route (censoredInt = 'NA' marks NA intensities as censored).
processed <- dataProcess(maxquant_input, normalization = 'equalizeMedians',
                         summaryMethod = 'TMP', censoredInt = 'NA', MBimpute = FALSE)

protein_abundance <- processed$ProteinLevelData
