skill <- "F:/OpenScience/wt/experimental-design-power-analysis/experimental-design/power-analysis"
for (f in c(file.path(skill,"examples/rnaseq_power.R"), file.path(skill,"examples/scrna_pseudobulk_power.R"))) parse(f)
for (pkg in c("RNASeqPower","PROPER","edgeR","pwr")) { suppressPackageStartupMessages(library(pkg,character.only=TRUE));cat(sprintf("%s=%s\n",pkg,packageVersion(pkg))) }
cat("ENV_AND_PARSE=PASS\n")
