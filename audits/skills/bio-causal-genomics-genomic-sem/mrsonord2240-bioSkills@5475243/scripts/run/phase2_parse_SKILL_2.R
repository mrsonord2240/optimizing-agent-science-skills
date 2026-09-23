# Prepare per-SNP betas and SEs across all input GWAS
ss <- sumstats(
    files = c('raw/trait1.txt', 'raw/trait2.txt', 'raw/trait3.txt'),
    ref = 'reference.1000G.maf.0.005.txt',
    trait.names = trait_names,
    se.logit = c(TRUE, TRUE, FALSE),     # TRUE if trait is logistic-scale (case-control); FALSE if continuous
    OLS = c(FALSE, FALSE, TRUE),
    linprob = c(FALSE, FALSE, FALSE),
    N = N,
    info.filter = 0.9,                   # standard imputation INFO threshold
    maf.filter = 0.01
)

saveRDS(ldsc_results, 'ldsc_results.rds'); saveRDS(ss, 'sumstats_snps.rds')
