# Input 5: SKILL step 9 (MR forest) on REAL data: MendelianRandomization::ldlc/chdlodds (28 lipid SNPs, Waterworth 2010 + CARDIoGRAM)
suppressMessages(library(MendelianRandomization))
D <- "F:/OpenScience/audits/bio-data-visualization-forest-funnel-plots"
bx <- ldlc; bxse <- ldlcse; by <- chdlodds; byse <- chdloddsse
cat("n SNPs:", length(bx), "\n")
# ---- example step 9, verbatim names (note: 'mr_input <- mr_input(...)' shadows the function) ----
mr_input <- mr_input(bx = bx, bxse = bxse, by = by, byse = byse)
mr_results <- mr_allmethods(mr_input)
print(mr_results)
suppressWarnings({ g <- mr_forest(mr_input, methods = c('ivw', 'wmedian', 'mbe', 'egger')) })
cat("class:", class(g), "\n")
png(file.path(D, "figs/in5_mr_forest.png"), width = 1000, height = 900, res = 110); print(g); dev.off()
# a second call after the shadowing: does mr_input() still work?
r <- try(mr_input(bx = bx, bxse = bxse, by = by, byse = byse), silent = TRUE); cat("second call to mr_input() after shadowing:", if (inherits(r, "try-error")) conditionMessage(attr(r, "condition")) else "OK", "\n")
rm(mr_input)
# Skill claim: 'Report MR-Egger intercept alongside main estimate'
e <- mr_egger(mr_input(bx = bx, bxse = bxse, by = by, byse = byse)); cat(sprintf("Egger slope=%.4f int=%.4f (p=%.3f)\n", e@Estimate, e@Intercept, e@Pleio.pval))
iv <- mr_ivw(mr_input(bx = bx, bxse = bxse, by = by, byse = byse)); cat(sprintf("IVW pkg est=%.6f se=%.6f\n", iv@Estimate, iv@StdError))
write.csv(data.frame(bx, bxse, by, byse), file.path(D, "data/mr_ldlc_chd.csv"), row.names = FALSE)
