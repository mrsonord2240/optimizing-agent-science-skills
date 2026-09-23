# Fresh synthetic cis-eQTL MR plus coloc execution for the Skill's triangulation workflow.
suppressPackageStartupMessages({ library(TwoSampleMR); library(coloc) })
set.seed(20260923)
n <- 30L
snps <- paste0('rs', seq_len(n))
eaf <- runif(n, 0.08, 0.45)
bx <- rnorm(n, 0.08, 0.015)
bx[10] <- 0.35
sexp <- rep(0.015, n)
by <- 0.28 * bx + rnorm(n, 0, 0.018)
seout <- rep(0.02, n)
exposure <- data.frame(SNP=snps, beta.exposure=bx, se.exposure=sexp,
                       effect_allele.exposure='A', other_allele.exposure='G',
                       eaf.exposure=eaf, pval.exposure=2*pnorm(-abs(bx/sexp)),
                       samplesize.exposure=500, exposure='GENE1_Whole_Blood', id.exposure='eqtl-gene1')
outcome <- data.frame(SNP=snps, beta.outcome=by, se.outcome=seout,
                      effect_allele.outcome='A', other_allele.outcome='G',
                      eaf.outcome=eaf, pval.outcome=2*pnorm(-abs(by/seout)),
                      samplesize.outcome=100000, outcome='trait', id.outcome='gwas-trait')
harm <- harmonise_data(exposure, outcome)
mr_out <- mr(harm, method_list='mr_ivw')
fstat <- min((harm$beta.exposure / harm$se.exposure)^2)
if (nrow(mr_out) != 1L || !is.finite(mr_out$b) || fstat <= 10) stop('MR assertions failed')
shared <- coloc.abf(
  dataset1=list(beta=by, varbeta=seout^2, N=100000, type='quant', MAF=eaf, snp=snps),
  dataset2=list(beta=bx, varbeta=sexp^2, N=500, type='quant', MAF=eaf, snp=snps))
pp4 <- unname(shared$summary['PP.H4.abf'])
if (!is.finite(pp4) || pp4 < 0.7) stop('coloc PP.H4 assertion failed')
write.table(mr_out, 'F:/OpenScience/audits/bio-causal-genomics-transcriptome-wide-association/data/finalpass_mr.tsv', sep='\t', quote=FALSE, row.names=FALSE)
write.table(shared$results, 'F:/OpenScience/audits/bio-causal-genomics-transcriptome-wide-association/data/finalpass_coloc.tsv', sep='\t', quote=FALSE, row.names=FALSE)
cat(sprintf('MR IVW beta=%.4f p=%.3g; minimum F=%.2f; coloc PP.H4=%.4f\n', mr_out$b, mr_out$pval, fstat, pp4))
