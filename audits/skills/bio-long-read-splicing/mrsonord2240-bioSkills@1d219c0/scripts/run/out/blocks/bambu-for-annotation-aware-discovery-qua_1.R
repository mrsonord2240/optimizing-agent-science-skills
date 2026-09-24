library(bambu)

bam_files <- c('sample1.bam', 'sample2.bam', 'sample3.bam')
genome <- 'reference.fa'
gtf <- 'gencode.v45.annotation.gtf'

bambuAnnotations <- prepareAnnotations(gtf)

se <- bambu(
    reads = bam_files,
    annotations = bambuAnnotations,
    genome = genome,
    NDR = 0.1,
    ncore = 8   # BiocParallel workers; on Windows R use ncore = 1
)

writeBambuOutput(se, path = 'bambu_output/')

tx_counts <- as.data.frame(assays(se)$counts)
gene_counts <- transcriptToGeneExpression(se)
