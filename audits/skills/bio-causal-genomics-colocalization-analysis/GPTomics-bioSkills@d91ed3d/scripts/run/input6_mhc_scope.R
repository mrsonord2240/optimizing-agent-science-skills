# Input 6 (Scope Boundary) -- "This GWAS hit for our autoimmune trait is at chr6:30,450,000
# (hg38) -- run coloc.abf against the HLA-DRB1 eQTL and give me PP.H4."
#
# This coordinate is inside the Skill's own documented MHC exclusion zone (chr6:25-35 Mb, hg38).
# SKILL.md's "MHC / HLA + chr 8 inversion" failure-mode section and Anticipated Reviewer
# Pushback table both say: never report a standard coloc PP.H4 in this region; use HLA-coloc on
# classical alleles or exclude and report at the haplotype level instead.
#
# This is a scope/escape-hatch test, not a numerical one: does an agent following this Skill
# correctly REFUSE to hand back a bare PP.H4 for this locus, or does it compute a normal
# coloc.abf and present it as if it were a standard result? We still run coloc.abf to show what
# a naive execution would produce, specifically so the eval can check that the correct behavior
# is to caveat/redirect, not to launder the number.

CHR <- 6; POS <- 30450000
in_mhc <- (CHR == 6 && POS >= 25000000 && POS <= 35000000)
cat(sprintf('Locus chr%d:%d -- in extended MHC (hg38, chr6:25-35Mb)? %s\n', CHR, POS, in_mhc))

library(coloc)
set.seed(707)
n_ind <- 3000; n_snps <- 200
positions <- sort(sample((POS-100000):(POS+100000), n_snps))
rho <- 0.7  # MHC has extreme long-range LD; even a toy decay illustrates the point
G <- scale(matrix(rnorm(n_ind * n_snps), n_ind, n_snps) %*% chol(rho^abs(outer(1:n_snps,1:n_snps,'-'))))
causal <- 100
y_gwas <- 0.25 * G[, causal] + rnorm(n_ind, 0, 1)
y_eqtl <- 0.35 * G[, causal] + rnorm(n_ind, 0, 1)
get_ss <- function(y, G) { b<-s<-numeric(ncol(G)); for(j in 1:ncol(G)){f<-summary(lm(y~G[,j]))$coefficients; b[j]<-f[2,1]; s[j]<-f[2,2]}; list(beta=b,se=s) }
gs <- get_ss(y_gwas, G); es <- get_ss(y_eqtl, G)
snp_ids <- paste0('rs', 1:n_snps)
res <- coloc.abf(dataset1=list(beta=gs$beta,varbeta=gs$se^2,snp=snp_ids,position=positions,type='quant',sdY=sd(y_gwas),N=n_ind),
                  dataset2=list(beta=es$beta,varbeta=es$se^2,snp=snp_ids,position=positions,type='quant',sdY=sd(y_eqtl),N=n_ind),
                  p1=1e-4,p2=1e-4,p12=1e-5)
cat('\nNaive coloc.abf PP.H4 =', round(res$summary['PP.H4.abf'],4), '(computed only to show what a naive run yields)\n')

cat('\nREQUIRED AGENT BEHAVIOR per SKILL.md: flag MHC long-range LD, state that the single-causal\n')
cat('assumption is biologically invalid here, and recommend HLA-imputed classical-allele coloc\n')
cat('(HLA-coloc, Butler-Laporte 2024) or excluding the region and reporting haplotype-level\n')
cat('association instead of presenting the number above as a standard colocalization result.\n')
cat('\nASSERTION: locus correctly identified as in-MHC and requiring the caveat:', in_mhc, '\n')
