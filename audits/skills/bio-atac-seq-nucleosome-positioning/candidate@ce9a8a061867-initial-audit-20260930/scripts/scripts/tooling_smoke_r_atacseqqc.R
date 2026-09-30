# Known-good ATACseqQC route (readBamFile asMates=TRUE) to show the surfaces behind nucleosome_analysis.R work in the lane env.
suppressPackageStartupMessages({library(ATACseqQC);library(GenomicAlignments);library(TxDb.Hsapiens.UCSC.hg38.knownGene);library(BSgenome.Hsapiens.UCSC.hg38);library(GenomicRanges);library(ChIPpeakAnno)})
bam <- file.path(Sys.getenv("ATACDATA"), "encode/GM12878_rep1_filtered.chr1_1-30000000.bam")
stopifnot(file.exists(bam))
chk <- function(n, ok, info="") {cat(if (ok) "PASS" else "FAIL", n, info, "\n"); if(!ok) quit(status=1)}
tss <- read.delim(file.path(Sys.getenv("ATACDATA"),"annotation/gencode_v29_protein_coding_tss.chr1.bed"), header=FALSE)
tss <- tss[tss$V2>1.2e6 & tss$V2<29e6,]
txs <- transcripts(TxDb.Hsapiens.UCSC.hg38.knownGene); txs <- keepSeqlevels(txs, "chr1", pruning.mode="coarse")
txs <- txs[start(txs)>1.2e6 & end(txs)<29e6]
chk("txs on chr1 slice", length(txs)>100, length(txs))
which <- GRanges("chr1", IRanges(1.2e6, 29e6))
gal <- readBamFile(bam, asMates=TRUE, bigFile=FALSE); gal <- gal[seqnames(unlist(gal, use.names=FALSE)[cumsum(elementNROWS(gal))]) == "chr1"]
chk("readBamFile asMates", length(gal)>1e5, length(gal))
sh <- shiftGAlignmentsList(gal)
chk("shiftGAlignmentsList returns flattened GAlignments (2 per pair)", is(sh,"GAlignments") && length(sh)>=1.9*length(gal), length(sh))
objs <- splitGAlignmentsByCut(sh, txs=txs, genome=BSgenome.Hsapiens.UCSC.hg38)
print(sapply(objs, length))
chk("split classes NucleosomeFree + mononucleosome non-empty", length(objs$NucleosomeFree)>1e3 && length(objs$mononucleosome)>1e3)
cv <- lapply(objs[c("NucleosomeFree","mononucleosome")], coverage)
tsg <- promoters(txs, upstream=1000, downstream=1000)
tsg <- tsg[seqnames(tsg)=="chr1" & start(tsg)>0]
sig <- featureAlignedSignal(cvglists=cv, feature.gr=tsg[1:200], upstream=1000, downstream=1000)
m <- sapply(sig, function(x) colMeans(x)); print(dim(m))
nfr <- m[, "NucleosomeFree"]; mono <- m[, "mononucleosome"]  # 100 tiles x 20 bp over +-1 kb
r <- mean(nfr[46:55]) / mean(c(nfr[1:10], nfr[91:100]))
chk("NFR signal higher at TSS centre than flank", is.finite(r) && r > 1.5, sprintf("%.2f", r))
cat("mono centre/flank", mean(mono[46:55])/mean(c(mono[1:10], mono[91:100])), "
")
