library(FRASER); library(BiocParallel)
bp <- if (.Platform$OS.type == 'windows') SerialParam() else MulticoreParam(8)

bam_files <- list.files('bams/', pattern = '\\.bam$', full.names = TRUE)
sample_table <- data.frame(
    sampleID = sub('\\.bam$', '', basename(bam_files)),
    bamFile = bam_files,
    pairedEnd = TRUE
)

# colData must be an S4Vectors DataFrame; a plain data.frame errors on FRASER 2.2.0 and 2.6.1
fds <- FraserDataSet(
    colData = S4Vectors::DataFrame(sample_table),
    workingDir = 'fraser_workdir',
    name = 'rare_disease_cohort'
)

fds <- countRNAData(fds, BPPARAM = bp)
fds <- calculatePSIValues(fds)
fds <- filterExpressionAndVariability(fds, minExpressionInOneSample = 20, minDeltaPsi = 0.0)

fitMetrics(fds) <- 'jaccard'
currentType(fds) <- 'jaccard'

# q: see Choosing q. FRASER 2.6.1: estimateBestQ(); FRASER 2.2.0 has only optimHyperParams()
fds <- estimateBestQ(fds, type = 'jaccard', plot = FALSE)
fds <- FRASER(fds, q = c(jaccard = bestQ(fds, 'jaccard')), implementation = 'PCA', BPPARAM = bp)

all_results <- as.data.frame(results(fds, psiType = 'jaccard', padjCutoff = 0.05, deltaPsiCutoff = 0.1))
patient_results <- all_results[all_results$sampleID == 'PATIENT_001', ]
patient_results <- patient_results[order(patient_results$padjust), ]
