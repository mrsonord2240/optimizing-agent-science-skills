# Re-audit: documented method-reference snippets run on the shipped CLI's own output.
#  (a) Visualizing Connections snippet (locus arc plot), (b) Hi-C concordance snippet vs a PLANTED BEDPE.
# Planted truth: 30 loops built from real strong pairs (anchors widened +-3 kb, given in GENOMIC order as a
# HiCCUPS BEDPE would be) + 30 decoy loops on other chr1 coordinates. Expected concordance is computed independently.
suppressPackageStartupMessages({library(GenomicRanges); library(GenomicInteractions); library(Gviz)})
CO <- Sys.getenv("CO"); D <- file.path(CO, "work/reaudit/cli"); setwd(D)
chk <- function(n, ok, d="") cat(if (isTRUE(ok)) "PASS" else "FAIL", n, d, "\n")
strong <- read.delim("cicero_connections.tsv", stringsAsFactors=FALSE)
cat("strong pairs:", nrow(strong), " by chr:", paste(names(table(sub("_.*","",strong$Peak1))), table(sub("_.*","",strong$Peak1)), collapse=" "), "\n")

# (a) verbatim snippet body (Visualizing Connections)
to_gr <- function(x) GRanges(sub('_(\\d+)_(\\d+)$', ':\\1-\\2', x))
sel <- strong[strong$coaccess > 0.5, ]
gi <- GenomicInteractions(anchor1=to_gr(sel$Peak1), anchor2=to_gr(sel$Peak2),
                          counts=as.integer(sel$coaccess * 100))
track <- InteractionTrack(gi, name='co-accessibility > 0.5', chromosome='chr1', start=1e6, end=1.4e6)
png("locus_arcs.png", width=1400, height=500, res=120)
plotTracks(list(GenomeAxisTrack(), track), chromosome='chr1', from=1e6, to=1.4e6)
dev.off()
inwin <- sum(overlapsAny(anchorOne(gi), GRanges("chr1", IRanges(1e6, 1.4e6))))
chk("viz snippet ran; png written", file.size("locus_arcs.png") > 5000, sprintf("%d bytes; %d >0.5 arcs anchored in window (of %d)", file.size("locus_arcs.png"), inwin, length(gi)))

# (b) Hi-C concordance snippet, verbatim, against planted BEDPE
pos <- function(x, i) as.numeric(sapply(strsplit(x, "_"), `[`, i))
set.seed(7)
c1 <- strong[sub("_.*","",strong$Peak1) == "chr1", ]
pick <- c1[sample(nrow(c1), 30), ]
lo <- function(p) pmin(pos(p$Peak1,2), pos(p$Peak2,2))          # genomic order
mk <- function(a, b) {  # peak strings a,b -> genomic-order bedpe row, widened +-3 kb
  sa <- pos(a,2); ea <- pos(a,3); sb <- pos(b,2); eb <- pos(b,3); sw <- sa > sb
  data.frame(c1="chr1", s1=pmax(0, ifelse(sw, sb, sa) - 3000), e1=ifelse(sw, eb, ea) + 3000,
             c2="chr1", s2=pmax(0, ifelse(sw, sa, sb) - 3000), e2=ifelse(sw, ea, eb) + 3000)
}
real <- mk(pick$Peak1, pick$Peak2)
decoy <- data.frame(c1="chr1", s1=round(runif(30, 5e6, 9e6)), e1=0, c2="chr1", s2=0, e2=0)
decoy$e1 <- decoy$s1 + 1000; decoy$s2 <- decoy$s1 + 60000; decoy$e2 <- decoy$s2 + 1000
write.table(rbind(real, decoy), "planted.bedpe", sep="\t", quote=FALSE, row.names=FALSE, col.names=FALSE)
nswap <- sum(pos(pick$Peak1,2) > pos(pick$Peak2,2))
cat(sprintf("planted: 30 real + 30 decoy loops; %d of the 30 picked pairs have Peak1 genomically DOWNSTREAM of Peak2 (lexicographic Peak1<Peak2)\n", nswap))

hic_loops <- makeGenomicInteractionsFromFile('planted.bedpe', type='bedpe',
                                             experiment_name='hiccups', description='HiCCUPS loops')
ci <- GenomicInteractions(anchor1=GRanges(sub('_(\\d+)_(\\d+)$', ':\\1-\\2', strong$Peak1)),
                          anchor2=GRanges(sub('_(\\d+)_(\\d+)$', ':\\1-\\2', strong$Peak2)))
overlap <- countOverlaps(ci, hic_loops) > 0
cat(sprintf('Cicero connections overlapping HiCCUPS loops: %.1f%%\n', 100 * mean(overlap)))

# independent expectation, orientation-agnostic: a strong pair is supported if any loop has one anchor overlapping
# each peak (either way round)
P1 <- to_gr(strong$Peak1); P2 <- to_gr(strong$Peak2)
L1 <- GRanges(rbind(real, decoy)$c1, IRanges(rbind(real, decoy)$s1 + 1, rbind(real, decoy)$e1))
L2 <- GRanges(rbind(real, decoy)$c2, IRanges(rbind(real, decoy)$s2 + 1, rbind(real, decoy)$e2))
sup <- vapply(seq_along(P1), function(i) any((overlapsAny(L1, P1[i]) & overlapsAny(L2, P2[i])) | (overlapsAny(L1, P2[i]) & overlapsAny(L2, P1[i]))), TRUE)
cat(sprintf("independent orientation-agnostic expected: %d supported pairs = %.1f%%; snippet found %d = %.1f%%\n", sum(sup), 100*mean(sup), sum(overlap), 100*mean(overlap)))
chk("Hi-C snippet count equals independent orientation-agnostic count", sum(overlap) == sum(sup), sprintf("%d vs %d", sum(overlap), sum(sup)))
chk("Hi-C snippet finds every planted-supported pair (>=30 real loops -> >=30 pairs)", sum(overlap) >= 30)
# how many supported pairs are genomically swapped relative to Peak1<Peak2 (lexicographic)
swapped <- pos(strong$Peak1,2) > pos(strong$Peak2,2)
cat(sprintf("of %d supported pairs, %d have Peak1 genomically downstream; snippet missed %d supported pairs\n", sum(sup), sum(sup & swapped), sum(sup & !overlap)))
