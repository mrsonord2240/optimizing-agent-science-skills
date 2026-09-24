# Quantify the SKILL.md outlier rule (Pvalue < 0.05/nrow) vs MR-PRESSO's own rule (Pvalue <= SignifThreshold; P already Bonferroni-adjusted)
suppressMessages({library(TwoSampleMR); library(MRPRESSO)})
args <- commandArgs(TRUE); d <- args[1]
truth <- read.delim(file.path(d, "truth_snps.tsv"), stringsAsFactors = FALSE)
ex <- read_exposure_data(file.path(d, "exposure_gwas.tsv"), sep = "\t", snp_col = "SNP", beta_col = "BETA", se_col = "SE",
  effect_allele_col = "A1", other_allele_col = "A2", eaf_col = "EAF", pval_col = "P", samplesize_col = "N")
ex <- subset(ex, pval.exposure < 5e-8)
oy <- read_outcome_data(file.path(d, "outcome_gwas.tsv"), snps = ex$SNP, sep = "\t", snp_col = "SNP", beta_col = "BETA", se_col = "SE",
  effect_allele_col = "A1", other_allele_col = "A2", eaf_col = "EAF", pval_col = "P", samplesize_col = "N")
dat <- harmonise_data(ex, oy, action = 2)
set.seed(42)
pr <- mr_presso(BetaOutcome = "beta.outcome", BetaExposure = "beta.exposure", SdOutcome = "se.outcome", SdExposure = "se.exposure",
  OUTLIERtest = TRUE, DISTORTIONtest = TRUE, data = dat, NbDistribution = 3000, SignifThreshold = 0.05)
ot <- pr$`MR-PRESSO results`$`Outlier Test`
p <- as.numeric(gsub("<", "", ot$Pvalue))
bad <- truth$planted_invalid[match(dat$SNP, truth$SNP)]
skill_rule <- which(p < 0.05 / nrow(dat)); presso_rule <- which(p <= 0.05)
cat(sprintf("planted invalid in set: %d\nSKILL.md rule (p < 0.05/n): flagged %d, true pos %d\nPRESSO own rule (p <= 0.05): flagged %d, true pos %d\n",
  sum(bad), length(skill_rule), sum(bad[skill_rule]), length(presso_rule), sum(bad[presso_rule])))
