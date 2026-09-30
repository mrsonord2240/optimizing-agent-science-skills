# Audit run: 'Visualizing Connections' snippet verbatim (bare plotTracks(track)) vs locus-restricted, on real Cicero output
suppressPackageStartupMessages({library(GenomicRanges); library(GenomicInteractions); library(Gviz)})
CO <- Sys.getenv("CO"); out <- file.path(CO, "work/audit_viz"); dir.create(out, showWarnings=FALSE, recursive=TRUE)
strong <- readRDS(file.path(CO, "work/chr1/res_chr1.rds"))$strong
gi <- GenomicInteractions(anchor1=GRanges(sub('_(\\d+)_(\\d+)$', ':\\1-\\2', strong$Peak1)),
                          anchor2=GRanges(sub('_(\\d+)_(\\d+)$', ':\\1-\\2', strong$Peak2)),
                          counts=as.integer(strong$coaccess * 100))
track <- InteractionTrack(gi, name='co-accessibility')
png(file.path(out, "verbatim_bare.png"), width=1400, height=500, res=120)
r <- try(plotTracks(track), silent=TRUE); dev.off()
cat("bare plotTracks(track):", if (inherits(r, "try-error")) trimws(as.character(r)) else "no error", "; file bytes", file.size(file.path(out, "verbatim_bare.png")), "\n")
# locus-restricted view around ISG15/AGRN region with a gene-scale window and the higher stringent cutoff
sel <- which(strong$coaccess > 0.5)
gi2 <- GenomicInteractions(anchor1=GRanges(sub('_(\\d+)_(\\d+)$', ':\\1-\\2', strong$Peak1[sel])), anchor2=GRanges(sub('_(\\d+)_(\\d+)$', ':\\1-\\2', strong$Peak2[sel])), counts=as.integer(strong$coaccess[sel]*100))
track2 <- InteractionTrack(gi2, name='coaccess>0.5', chromosome="chr1", start=1e6, end=1.4e6)
png(file.path(out, "locus_0.5.png"), width=1400, height=500, res=120)
plotTracks(list(GenomeAxisTrack(), track2), chromosome="chr1", from=1e6, to=1.4e6); dev.off()
cat("locus 0.5 arcs in window:", sum(overlapsAny(anchorOne(gi2), GRanges("chr1", IRanges(1e6, 1.4e6)))), "\n")
