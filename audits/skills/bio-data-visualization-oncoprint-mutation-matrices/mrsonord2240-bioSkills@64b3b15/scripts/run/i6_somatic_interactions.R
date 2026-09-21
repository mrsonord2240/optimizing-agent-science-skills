source("helpers.R")
DV <- Sys.getenv("DV")
run_si <- function(mafobj, top, tag, genes=NULL) {
  png(paste0("out/i6_", tag, ".png"), width=1000, height=1000, res=110)
  si <- if (is.null(genes)) somaticInteractions(maf = mafobj, top = top, pvalue = c(0.05, 0.01), fontSize = 0.7) else somaticInteractions(maf = mafobj, genes = genes, pvalue = c(0.05, 0.01), fontSize = 0.7)
  dev.off()
  cat("[", tag, "] return class:", paste(class(si), collapse="/"), " dim:", paste(dim(si), collapse="x"), " columns:", paste(colnames(si), collapse=","), "\n")
  write.csv(as.data.frame(si), paste0("out/i6_", tag, "_si.csv"), row.names=FALSE)
  si
}
# (a) LAML, Skill call top = 20
laml <- read.maf(file.path(DV, "public-data/mutations/tcga_laml.maf.gz"), verbose=FALSE)
si_a <- run_si(laml, 20, "laml")
# (b) synthetic planted cohort (N=600)
syn <- read.maf("data/synth_cohort.maf", verbose=FALSE)
si_b <- run_si(syn, NULL, "synth", genes=c("TP53","MYC","BRAF","NRAS","KRAS","EGFR","PIK3CA","CDH1","GATA3","ERBB2"))
# (c) small cohort N=20: first 20 samples of the synthetic cohort
smp <- sort(unique(read_maf_df("data/synth_cohort.maf")$Tumor_Sample_Barcode))
clin <- read.delim("data/synth_cohort_clin.tsv"); s20 <- clin$Tumor_Sample_Barcode[1:20]
syn20 <- subsetMaf(syn, tsb=s20, verbose=FALSE)
si_c <- run_si(syn20, NULL, "synth20", genes=c("TP53","MYC","BRAF","NRAS","KRAS","EGFR","PIK3CA","CDH1"))
writeLines(s20, "out/i6_s20.txt")
# maftools' own per-pair record for a sanity peek
print(head(as.data.frame(si_b)[order(as.data.frame(si_b)$pValue), ], 6))
# Skill's small-cohort recipe: exact-binomial CI per gene (binom.test) and Haldane-Anscombe OR on 2x2 with zero cell
g <- as.data.frame(getGeneSummary(syn20))[, c("Hugo_Symbol","MutatedSamples")]
g <- head(g[g$Hugo_Symbol %in% c("TP53","MYC","BRAF","NRAS","KRAS","EGFR","PIK3CA","CDH1"),], 8)
ci <- t(sapply(g$MutatedSamples, function(k) { b <- binom.test(k, 20); c(b$conf.int) }))
out <- data.frame(g, freq=g$MutatedSamples/20, lo=ci[,1], hi=ci[,2]); print(out, digits=3)
write.csv(out, "out/i6_cp_R.csv", row.names=FALSE)
