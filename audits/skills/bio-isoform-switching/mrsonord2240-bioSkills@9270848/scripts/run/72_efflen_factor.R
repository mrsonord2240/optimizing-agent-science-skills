# Which length gives the Skill's 'median(length)/length ranges 0.019-205 across 5,895 isoforms'? Length or EffectiveLength (sample 1)?
PD <- "F:/OpenScience/audit-envs/alternative-splicing/public-data"
q <- read.delim(file.path(PD, "rnasplice/salmon/ERR188383/quant.sf"), stringsAsFactors = FALSE)
cat("isoforms in quant.sf:", nrow(q), "\n")
for (nm in c("Length", "EffectiveLength")) { v <- q[[nm]]; fac <- median(v) / v; cat(sprintf("%-16s median %.0f | factor range %.3f - %.1f\n", nm, median(v), min(fac), max(fac))) }
