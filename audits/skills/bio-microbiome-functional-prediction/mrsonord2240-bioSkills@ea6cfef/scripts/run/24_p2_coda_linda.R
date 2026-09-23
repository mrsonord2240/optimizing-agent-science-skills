.libPaths(c("F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/R-lib", .libPaths()))
suppressMessages({ library(ALDEx2); library(Maaslin2); library(MicrobiomeStat) })
base <- "F:/OpenScience/audits/bio-microbiome-functional-prediction/work/p2-final-20260923"
paths <- read.delim(gzfile(file.path(base, "picrust2_out_documented/pathways_out/path_abun_unstrat.tsv.gz")), row.names=1, check.names=FALSE)
meta <- read.delim("F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/public-data/moving-pictures/sample_metadata.tsv")
meta <- meta[-1, ]; colnames(meta)[1] <- "sample_id"; rownames(meta) <- meta$sample_id
groups <- meta[colnames(paths), "body.site"]
keep <- groups %in% c("gut", "left palm")
x <- as.matrix(paths[, keep]); storage.mode(x) <- "numeric"; grp <- factor(groups[keep])
cat("pathways=", nrow(x), " samples=", ncol(x), " groups=", paste(names(table(grp)), table(grp), collapse=","), "\n", sep="")
set.seed(123)
a <- aldex(round(x), as.character(grp), mc.samples=128, test="t", effect=TRUE, denom="all")
ah <- rownames(a)[a$we.eBH < 0.05]
cat("aldex2_significant=", length(ah), "\n", sep="")
mi <- as.data.frame(t(x)); mm <- data.frame(body_site=as.character(grp), row.names=colnames(x))
mdir <- file.path(base, "maaslin2_p2")
fit <- Maaslin2(mi, mm, output=mdir, fixed_effects="body_site", normalization="TSS", transform="LOG", min_prevalence=0.1, plot_heatmap=FALSE, plot_scatter=FALSE)
mh <- unique(read.delim(file.path(mdir, "significant_results.tsv"))$feature)
cat("maaslin2_significant=", length(mh), " naive_intersection=", length(intersect(ah,mh)), " normalized_intersection=", length(intersect(make.names(ah),make.names(mh))), "\n", sep="")
lf <- linda(feature.dat=as.data.frame(x), meta.dat=mm, formula="~body_site", feature.dat.type="proportion", prev.filter=0.1)
cat("linda_rows=", nrow(lf$output[[1]]), " expected_filtered=", sum(rowSums(x>0)<2), "\n", sep="")
