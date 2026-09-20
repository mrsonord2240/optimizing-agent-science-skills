# Input 3 real-data leg: SKILL.md Bambu block on REAL ONT direct-RNA (SG-NEx A549, chr9:1-1e6, Ensembl 91 GTF), NDR 0.1 / 0.05 / 0.3.
# Second method: pysam-free R check = reads overlapping each gene via GenomicAlignments::summarizeOverlaps, and IsoQuant (iq_real) transcript counts.
D <- "F:/OpenScience/audits/bio-long-read-splicing/run"
B <- "F:/OpenScience/audit-envs/alternative-splicing/public-data/longread/bambu_extdata"
W <- paste0(D, "/out/bambu_real"); dir.create(W, showWarnings = FALSE); setwd(W)
file.copy(list.files(B, full.names = TRUE), W)           # copy: never write into public-data
suppressMessages({library(bambu); library(SummarizedExperiment)})
bam <- "SGNex_A549_directRNA_replicate5_run1_chr9_1_1000000.bam"
gtf <- "Homo_sapiens.GRCh38.91_chr9_1_1000000.gtf"
fa <- "Homo_sapiens.GRCh38.dna_sm.primary_assembly_chr9_1_1000000.fa"
ann <- prepareAnnotations(gtf)
out <- list()
for (ndr in c(0.05, 0.1, 0.3)) {
  se <- suppressMessages(bambu(reads = bam, annotations = ann, genome = fa, NDR = ndr, ncore = 1))
  cnt <- assays(se)$counts[, 1]
  rr <- rowRanges(se)
  novel <- grepl("^Bambu", names(rr))
  cat(sprintf("NDR=%.2f: %d transcripts (%d novel); total transcript count %.1f; novel count %.1f\n", ndr, length(rr), sum(novel), sum(cnt), sum(cnt[novel])))
  out[[as.character(ndr)]] <- se
}
se <- out[["0.1"]]
writeBambuOutput(se, path = "bambu_output/")
cat("writeBambuOutput files:", paste(list.files("bambu_output"), collapse = ", "), "\n")
gene_counts <- transcriptToGeneExpression(se)
cat("gene_counts class:", class(gene_counts), " dim:", dim(gene_counts), "\n")
tx <- assays(se)$counts[, 1]
# compare with IsoQuant on the same BAM
iq <- read.table(paste0(D, "/out/isoquant/iq_real/real/real.transcript_counts.tsv"), header = TRUE, sep = "\t", comment.char = "#", stringsAsFactors = FALSE)
names(iq)[1:2] <- c("id", "count")
common <- intersect(names(tx), iq$id)
b <- tx[common]; i <- iq$count[match(common, iq$id)]
keep <- (b + i) > 0
cat(sprintf("annotated transcripts with counts in bambu or IsoQuant: %d; Spearman(bambu,IsoQuant)=%.3f ; totals bambu(annotated)=%.1f IsoQuant(annotated)=%.1f\n", sum(keep), suppressWarnings(cor(b[keep], i[keep], method = "spearman")), sum(b), sum(i)))
# independent total: primary aligned reads in the BAM overlapping any annotated exon
suppressMessages({library(GenomicAlignments); library(rtracklayer)})
ga <- readGAlignments(bam, param = ScanBamParam(flag = scanBamFlag(isSecondaryAlignment = FALSE, isSupplementaryAlignment = FALSE, isUnmappedQuery = FALSE)))
cat("primary mapped reads in BAM (GenomicAlignments):", length(ga), "\n")
ex <- import(gtf); ex <- ex[ex$type == "exon"]
seqlevelsStyle(ex) <- "NCBI"
hits <- overlapsAny(granges(ga), ex, ignore.strand = FALSE)
cat("  overlapping annotated exons on the same strand:", sum(hits), "\n")
cat("bambu total count (all transcripts, NDR0.1):", sum(tx), "\n")
