# Fresh input for scripts/coloc_abf.R; all values are synthetic; planted SNP rs311.
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1) stop("usage: input8_make_abf_inputs.R <outdir>")
outdir <- args[[1]]; dir.create(outdir, recursive=TRUE, showWarnings=FALSE)
set.seed(92662026); n <- 600L; causal <- 311L
pos <- sort(sample(10000000:11000000, n)); snp <- sprintf("rs%d", seq_len(n)); maf <- runif(n, .08, .45)
g <- data.frame(SNP=snp, CHR=10L, POS=pos, A1="A", A2="G", MAF=maf, BETA=rnorm(n, 0, .012), SE=runif(n, .015, .025))
e <- data.frame(SNP=snp, CHR=10L, POS=pos, A1="A", A2="G", MAF=maf, BETA=rnorm(n, 0, .018), SE=runif(n, .02, .04))
g$BETA[causal] <- .28; e$BETA[causal] <- .52
write.table(g, file.path(outdir,"gwas.tsv"), sep="\t", quote=FALSE, row.names=FALSE)
write.table(e, file.path(outdir,"eqtl.tsv"), sep="\t", quote=FALSE, row.names=FALSE)
cat(sprintf("PLANTED_SHARED=%s\n", snp[causal]))
