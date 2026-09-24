# Input 6: SKILL.md SSD route (Generate_SSD_SetID, Open_SSD, SKAT.SSD.All) on PLINK files. SYNTHETIC data.
suppressMessages(library(SKAT))
cat("SKAT", as.character(packageVersion("SKAT")), "\n")
Generate_SSD_SetID("wes.bed", "wes.bim", "wes.fam", "setid.txt", "wes.SSD", "wes.SSD.info")
SSD.INFO <- Open_SSD("wes.SSD", "wes.SSD.info")
cat("SSD sets:", SSD.INFO$nSets, " samples:", SSD.INFO$nSample, "\n")
fam <- read.table("wes.fam")
covar_df <- read.delim("../../data/covar_skat.tsv"); covar_df$phenotype <- covar_df$Y
stopifnot(identical(as.character(fam$V2), as.character(covar_df$IID)))
obj <- SKAT_Null_Model(phenotype ~ age + sex + PC1 + PC2, out_type = 'D', data = covar_df)
# SKILL.md call as printed
all_skat <- SKAT.SSD.All(SSD.INFO, obj)
# SKAT-O with the Skill's weights
all_skato <- SKAT.SSD.All(SSD.INFO, obj, method = "SKATO", weights.beta = c(1, 25))
Close_SSD()
r <- merge(all_skat$results[, c("SetID", "P.value", "N.Marker.All", "N.Marker.Test")],
           all_skato$results[, c("SetID", "P.value")], by = "SetID", suffixes = c(".skat", ".skato"))
ref <- read.delim("skat_results_matrix.tsv")   # per-gene matrix run from input 2 (post-fix re-run)
m <- merge(r, ref, by.x = "SetID", by.y = "gene")
m <- m[order(m$P.value.skato), ]
print(format(head(m[, c("SetID", "N.Marker.Test", "P.value.skat", "skat", "P.value.skato", "skato")], 8), digits = 3), row.names = FALSE)
cat("max |log10 p| difference SSD vs matrix: SKAT", signif(max(abs(log10(m$P.value.skat) - log10(m$skat))), 3),
    " SKAT-O", signif(max(abs(log10(m$P.value.skato) - log10(m$skato))), 3), "\n")
