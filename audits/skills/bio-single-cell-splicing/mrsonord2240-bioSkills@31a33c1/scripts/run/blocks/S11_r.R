library(Sierra)

FindPeaks(
    output.file = 'peaks.txt',
    gtf.file = 'annotation.gtf',
    bamfile = 'possorted_genome_bam.bam',
    junctions.file = 'junctions.bed'      # regtools BED or STAR SJ.out.tab
)

# CountPeaks writes a MEX directory and returns NULL; read it back
CountPeaks(
    peak.sites.file = 'peaks.txt',
    gtf.file = 'annotation.gtf',
    bamfile = 'possorted_genome_bam.bam',
    whitelist.file = 'barcodes.tsv',
    output.dir = 'peak_counts/'
)
counts <- ReadPeakCounts(data.dir = 'peak_counts/')     # peak x cell sparse matrix

# AnnotatePeaksFromGTF also writes a file (returns NULL)
AnnotatePeaksFromGTF(
    peak.sites.file = 'peaks.txt',
    gtf.file = 'annotation.gtf',
    output.file = 'peak_annotations.txt'
)
peak.annotations <- read.table('peak_annotations.txt', header = TRUE, sep = '\t',
                               row.names = 1, stringsAsFactors = FALSE)

# cell_identities: named vector, barcode -> population. Use NewPeakSCE: DUTest on a
# NewPeakSeurat object fails with SeuratObject >= 5 (GetAssayData `slot` is defunct).
# min.cells/min.peaks default to 10/200: a small peak set then drops every cell and DUTest errors (invalid 'row.names' length)
peaks.sce <- NewPeakSCE(peak.data = counts, annot.info = peak.annotations, cell.idents = cell_identities,
                        min.cells = 0, min.peaks = 0)

apa_results <- DUTest(peaks.sce, population.1 = 'ctrl', population.2 = 'trt')   # gene_name, padj, Log2_fold_change per peak
