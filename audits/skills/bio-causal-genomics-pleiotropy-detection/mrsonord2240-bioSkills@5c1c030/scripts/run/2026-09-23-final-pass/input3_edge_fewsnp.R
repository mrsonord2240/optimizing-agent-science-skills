# Input 3 (Edge/boundary, REGRESSION of pre-fix Input 3) -- "I only have 3 SNPs in tight
# LD at my drug-target locus. Run MR-Egger and MR-PRESSO on this cis-MR instrument set."
# Tests SKILL.md's Common Errors table entry: "MR-PRESSO crashes with 'Not enough
# intrumental variables' | Fewer than 4 SNPs | Need >=4 for PRESSO; for cis-MR with few
# SNPs use colocalization" -- unchanged by the fix pass; regression check.

library(TwoSampleMR)
library(MRPRESSO)

dat <- readRDS('F:/OpenScience/audits/bio-causal-genomics-pleiotropy-detection/data/synth_3snp.rds')
cat('n SNPs:', nrow(dat), '\n\n')

cat('=== IVW + Egger (SKILL.md flags Egger as underpowered <10 SNPs) ===\n')
res <- mr(dat, method_list = c('mr_ivw', 'mr_egger_regression'))
print(res[, c('method','nsnp','b','se','pval')])

cat('\n=== MR-PRESSO on 3 SNPs (SKILL.md predicts a crash) ===\n')
result <- tryCatch({
  mr_presso(BetaOutcome='beta.outcome', BetaExposure='beta.exposure',
            SdOutcome='se.outcome', SdExposure='se.exposure',
            OUTLIERtest=TRUE, DISTORTIONtest=TRUE,
            data=dat, NbDistribution=1000, SignifThreshold=0.05)
}, error = function(e) {
  cat('ERROR (as SKILL.md Common Errors table predicts):', conditionMessage(e), '\n')
  NULL
})
if (is.null(result)) {
  cat('CONFIRMED (regression holds): PRESSO does not run below its documented 4-SNP minimum, matching the SKILL.md warning.\n')
  cat('Correct next step per SKILL.md: use colocalization (causal-genomics/colocalization-analysis), not PRESSO.\n')
} else {
  cat('PRESSO returned a result despite n=3 -- inconsistent with the documented minimum; inspect output:\n')
  print(result$`MR-PRESSO results`$`Global Test`)
}
