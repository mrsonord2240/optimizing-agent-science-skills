library(GenomicSEM)

# Step 1: Munge sumstats (one-time; produces .sumstats.gz files). GenomicSEM::munge()
# or LDSC's own munge_sumstats.py both work; either way, verify HapMap3-alignment first.
files <- c('raw/trait1.txt', 'raw/trait2.txt', 'raw/trait3.txt')
hm3 <- 'w_hm3.snplist'  # HapMap3 SNP list
trait_names <- c('trait1', 'trait2', 'trait3')
N <- c(150000, 200000, 175000)
munge(files = files, hm3 = hm3, trait.names = trait_names, N = N)

# Step 2: LDSC produces both S (genetic covariance) and V (sampling covariance)
traits <- c('trait1.sumstats.gz', 'trait2.sumstats.gz', 'trait3.sumstats.gz')
ldsc_results <- ldsc(
    traits = traits,
    sample.prev = c(0.5, 0.5, NA),    # case prevalence; NA for continuous
    population.prev = c(0.05, 0.05, NA),
    ld = 'eur_w_ld_chr/',
    wld = 'eur_w_ld_chr/',
    trait.names = trait_names
)
# ldsc_results$S = genetic covariance; ldsc_results$V = sampling covariance

# Step 3a: Common-factor CFA via DWLS
cf_fit <- commonfactor(covstruc = ldsc_results, estimation = 'DWLS')
print(cf_fit$modelfit)  # CFI, RMSEA, SRMR, chi-square
print(cf_fit$results)   # loadings + SEs

# Step 3b: Alternative -- user-specified two-factor model (>=3 indicators per factor)
# Identification rule: each factor needs >= 3 indicators OR one anchor loading fixed
# to 1 plus factor variance free. A factor with a single indicator is NOT identified.
model_syntax <- '
    F1 =~ NA*trait1 + trait2 + trait3
    F2 =~ NA*trait4 + trait5 + trait6
    F1 ~~ 1*F1
    F2 ~~ 1*F2
    F1 ~~ F2
'
user_fit <- usermodel(covstruc = ldsc_results, model = model_syntax, estimation = 'DWLS')
