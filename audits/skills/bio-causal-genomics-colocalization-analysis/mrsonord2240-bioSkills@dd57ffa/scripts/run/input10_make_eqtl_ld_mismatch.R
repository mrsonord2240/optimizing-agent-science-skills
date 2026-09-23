# Adversarial test for the documented two-trait LD-consistency guard.  The GWAS
# remains the self-consistent Input 9 data, while eQTL z-scores come from a
# separately simulated identity-LD genotype panel but are paired with Input 9 LD.
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) stop("usage: input10_make_eqtl_ld_mismatch.R <input9-dir> <outdir>")
in9 <- args[[1]]; outdir <- args[[2]]; dir.create(outdir, recursive=TRUE, showWarnings=FALSE)
gwas <- read.delim(file.path(in9, "gwas.tsv"), stringsAsFactors=FALSE)
ld <- as.matrix(read.delim(file.path(in9, "ld.tsv"), row.names=1, check.names=FALSE))
set.seed(101026); nind <- 1800L; nsnp <- nrow(gwas); causal <- 90L
G_bad <- scale(matrix(rnorm(nind * nsnp), nind, nsnp))
y_bad <- .48 * G_bad[, causal] + rnorm(nind)
fits <- do.call(rbind, lapply(seq_len(nsnp), function(j) summary(lm(y_bad ~ G_bad[,j]))$coefficients[2,1:2]))
eqtl <- gwas; eqtl$BETA <- fits[,1]; eqtl$SE <- fits[,2]
lam_bad <- susieR::estimate_s_rss(z=eqtl$BETA / eqtl$SE, R=ld, n=nind)
cat(sprintf("EQTL_LAMBDA_WITH_WRONG_LD=%.6f\n", lam_bad))
stopifnot(lam_bad > .05)
write.table(gwas, file.path(outdir,"gwas.tsv"), sep="\t", quote=FALSE, row.names=FALSE)
write.table(eqtl, file.path(outdir,"eqtl.tsv"), sep="\t", quote=FALSE, row.names=FALSE)
write.table(cbind(SNP=rownames(ld), ld), file.path(outdir,"ld.tsv"), sep="\t", quote=FALSE, row.names=FALSE)
