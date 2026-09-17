# 3-SNP cis-MR-style instrument set (edge case: below MR-PRESSO's documented
# minimum of 4 SNPs -- SKILL.md Common Errors: "MR-PRESSO crashes with 'Not enough
# intrumental variables' | Fewer than 4 SNPs | Need >=4 for PRESSO; for cis-MR with
# few SNPs use colocalization").
set.seed(777)
n <- 3
dat <- data.frame(
  SNP = paste0('rs', 1:n),
  beta.exposure = c(0.08, 0.06, 0.07), se.exposure = c(0.01, 0.012, 0.009),
  beta.outcome  = c(0.03, 0.02, 0.025), se.outcome  = c(0.012, 0.014, 0.011),
  effect_allele.exposure = rep('A', n), other_allele.exposure = rep('G', n),
  effect_allele.outcome = rep('A', n), other_allele.outcome = rep('G', n),
  eaf.exposure = c(0.3, 0.4, 0.35), eaf.outcome = c(0.3, 0.4, 0.35),
  id.exposure = rep('exposure', n), id.outcome = rep('outcome', n),
  exposure = rep('CisExposure', n), outcome = rep('CisOutcome', n),
  mr_keep = rep(TRUE, n), stringsAsFactors = FALSE)
saveRDS(dat, 'F:/OpenScience/audits/bio-causal-genomics-pleiotropy-detection/data/synth_3snp.rds')
write.csv(dat, 'F:/OpenScience/audits/bio-causal-genomics-pleiotropy-detection/data/synth_3snp.csv', row.names = FALSE)
cat('3-SNP synthetic dataset written.\n')
