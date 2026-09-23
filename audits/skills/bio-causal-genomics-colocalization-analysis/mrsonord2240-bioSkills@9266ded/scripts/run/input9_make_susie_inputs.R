# Fresh, self-consistent genotype -> sumstats -> LD input for scripts/coloc_susie.R.
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1) stop("usage: input9_make_susie_inputs.R <outdir>")
outdir <- args[[1]]; dir.create(outdir, recursive=TRUE, showWarnings=FALSE)
set.seed(150926); nind <- 1800L; nsnp <- 180L; causal <- 90L
R0 <- .78^abs(outer(seq_len(nsnp), seq_len(nsnp), "-")); G <- scale(matrix(rnorm(nind * nsnp), nind, nsnp) %*% chol(R0))
y1 <- .36 * G[,causal] + rnorm(nind); y2 <- .48 * G[,causal] + rnorm(nind)
ss <- function(y) do.call(rbind, lapply(seq_len(nsnp), function(j) summary(lm(y ~ G[,j]))$coefficients[2,1:2]))
s1 <- ss(y1); s2 <- ss(y2); snp <- sprintf("rs%d", seq_len(nsnp)); pos <- sort(sample(40000000:41000000, nsnp))
g <- data.frame(SNP=snp, CHR=1L, POS=pos, BETA=s1[,1], SE=s1[,2]); e <- data.frame(SNP=snp, CHR=1L, POS=pos, BETA=s2[,1], SE=s2[,2])
ld <- cor(G); rownames(ld) <- snp; colnames(ld) <- snp
write.table(g, file.path(outdir,"gwas.tsv"), sep="\t", quote=FALSE, row.names=FALSE)
write.table(e, file.path(outdir,"eqtl.tsv"), sep="\t", quote=FALSE, row.names=FALSE)
write.table(cbind(SNP=snp, ld), file.path(outdir,"ld.tsv"), sep="\t", quote=FALSE, row.names=FALSE)
cat(sprintf("PLANTED_SHARED=%s\n", snp[causal]))
