# Determinism probe: shipped bulk pipeline (with evidence depth patch) run twice with different RNG seeds, no set.seed as in the Skill script.
suppressPackageStartupMessages({library(chromVAR); library(motifmatchr); library(BSgenome.Hsapiens.UCSC.hg38); library(JASPAR2024); library(TFBSTools); library(SummarizedExperiment); library(GenomicRanges); library(RSQLite)})
O <- file.path(Sys.getenv("MD"), "evidence/../work"); inp <- "/mnt/openscience/audits/bio-atac-seq-motif-deviation/outputs"
peaks <- read.table(file.path(inp,'peaks.bed'), col.names=c('chr','start','end'))
pr <- GRanges(peaks$chr, IRanges(peaks$start+1, peaks$end))
cm <- as.matrix(read.delim(file.path(inp,'counts.tsv'), row.names=1))
se <- SummarizedExperiment(assays=list(counts=cm), rowRanges=pr)
colData(se)$depth <- read.delim(file.path(inp,'depth.tsv'), row.names=1)[colnames(se),1]
se <- addGCBias(se, genome=BSgenome.Hsapiens.UCSC.hg38)
se <- filterSamples(se, min_depth=1500, min_in_peaks=0.15, shiny=FALSE)
se <- filterPeaks(se, non_overlapping=TRUE, min_fragments_per_peak=10)
sq <- dbConnect(SQLite(), db(JASPAR2024::JASPAR2024()))
pfm <- getMatrixSet(sq, opts=list(collection='CORE', tax_group='vertebrates'))
mi <- matchMotifs(pfm, se, genome=BSgenome.Hsapiens.UCSC.hg38, p.cutoff=5e-5)
runz <- function(seed){ set.seed(seed); bg <- getBackgroundPeaks(se, niterations=50); z <- deviationScores(computeDeviations(se, mi, bg)); z }
z1 <- runz(1); z2 <- runz(2)
cat("dim", dim(z1), "\nmax|dz| between runs:", max(abs(z1-z2)), "\ncor:", cor(as.numeric(z1), as.numeric(z2)), "\n")
cat("median |dz|:", median(abs(z1-z2)), " 95th:", quantile(abs(z1-z2), .95), "\n")
v1 <- apply(z1,1,sd); v2 <- apply(z2,1,sd); t1 <- names(sort(v1,TRUE))[1:20]; t2 <- names(sort(v2,TRUE))[1:20]
cat("top20 sd overlap:", length(intersect(t1,t2)), "\n")
lm <- function(z){ g <- factor(rep(c("c","t"),each=3)); library(limma); tt <- topTable(eBayes(lmFit(z, model.matrix(~g))), coef=2, number=Inf); rownames(tt)[tt$adj.P.Val<.05 & abs(tt$logFC)>=.5] }
s1 <- lm(z1); s2 <- lm(z2); cat("sig sets:", length(s1), length(s2), "jaccard", length(intersect(s1,s2))/length(union(s1,s2)), "\n")
# depth semantic check: FRiP-like ratio the filter uses
fr <- colSums(assay(se))/colData(se)$depth; print(round(fr,3))
