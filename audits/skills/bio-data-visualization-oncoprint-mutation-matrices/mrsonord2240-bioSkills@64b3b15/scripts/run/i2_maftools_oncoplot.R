source("helpers.R")
library(svglite)
DV <- Sys.getenv("DV")
mf <- file.path(DV, "public-data/mutations/tcga_laml.maf.gz")
ann <- read.delim(file.path(DV, "public-data/mutations/tcga_laml_annot.tsv"), stringsAsFactors=FALSE)
# ---- independent truth (base R on the raw MAF) ----
df <- read_maf_df(mf)
nonsil <- df[!df$Variant_Classification %in% c("Silent","Intron","RNA","IGR","3'UTR","5'UTR","3'Flank","5'Flank"),]
samp_cnt <- sort(tapply(nonsil$Tumor_Sample_Barcode, nonsil$Hugo_Symbol, function(z) length(unique(z))), decreasing=TRUE)
var_cnt  <- sort(table(nonsil$Hugo_Symbol), decreasing=TRUE)
cat("independent top20 by MUTATED SAMPLES:", paste0(names(samp_cnt)[1:20], ":", samp_cnt[1:20]), "\n")
cat("independent top20 by VARIANT COUNT  :", paste0(names(var_cnt)[1:20], ":", var_cnt[1:20]), "\n")

# ---- Skill block 2, adapted only for data ----
# first, the naive call (numeric Overall_Survival_Status, no colour given) -> record what happens
maf0 <- read.maf(maf = mf, clinicalData = ann)
e0 <- try(oncoplot(maf=maf0, top=5, clinicalFeatures=c('FAB_classification','Overall_Survival_Status'), annotationColor=list(FAB_classification=c(M0='#0072B2')), sortByAnnotation=TRUE, removeNonMutated=FALSE), silent=TRUE)
cat("naive numeric-feature call:", if (inherits(e0,'try-error')) paste('ERROR:', conditionMessage(attr(e0,'condition'))) else 'ok', "
")
ann$Overall_Survival_Status <- ifelse(ann$Overall_Survival_Status==1, 'Dead', 'Alive')
maf <- read.maf(maf = mf, clinicalData = ann)
fabcol <- c(M0='#0072B2', M1='#D55E00', M2='#009E73', M3='#F0E442', M4='#CC79A7', M5='#56B4E9', M6='#999999', M7='#E69F00')
svglite("out/i2.svg", width=14, height=8)
r <- try(oncoplot(maf = maf, top = 20, clinicalFeatures = c('FAB_classification', 'Overall_Survival_Status'),
         annotationColor = list(FAB_classification = fabcol, Overall_Survival_Status = c(Alive='#FFFFCC', Dead='#BD0026')),
         sortByAnnotation = TRUE, removeNonMutated = FALSE))
dev.off()
png("out/i2.png", width=1600, height=900, res=110)
oncoplot(maf = maf, top = 20, clinicalFeatures = c('FAB_classification', 'Overall_Survival_Status'),
         annotationColor = list(FAB_classification = fabcol, Overall_Survival_Status = c(Alive='#FFFFCC', Dead='#BD0026')), sortByAnnotation = TRUE, removeNonMutated = FALSE)
dev.off()
P <- parse_svg("out/i2.svg"); tx <- P$txt
cat("class of oncoplot return:", class(r), "\n")
# gene labels: strings equal to known gene symbols, at left; order by y
g_all <- unique(df$Hugo_Symbol)
gl <- tx[tx$label %in% g_all,]; gl <- gl[order(gl$y),]
cat("drawn genes top->bottom:", gl$label, "\n")
pc <- tx[grepl("^[0-9]+%$", tx$label),]; pc <- pc[order(pc$y),]
cat("drawn pct labels       :", pc$label, "\n")
gs <- getGeneSummary(maf); print(head(gs[,1:9],22))
cat("maftools MutatedSamples for drawn order:", gs$MutatedSamples[match(gl$label, gs$Hugo_Symbol)], "\n")
cat("independent sample counts for drawn order:", samp_cnt[gl$label], "\n")
cat("expected pct from independent samples/193:", paste0(round(samp_cnt[gl$label]/193*100), "%"), "\n")
cat("number of sample columns declared:", maf@summary$summary[maf@summary$ID=="Samples"], "\n")
# how many columns drawn? count background rects of the body
R <- P$rect; R <- R[!is.na(R$fill),]
print(sort(table(R$fill), decreasing=TRUE)[1:8])
# ---- default maftools class colours vs drawn ----
print(maftools:::get_vcColors())
# Skill's annotationColor for a subset of levels only (as shown in SKILL.md: 2 of 3 subtypes, 2 of 4 stages)
r2 <- try({png("out/i2b.png", width=1200, height=700); oncoplot(maf=maf, top=10, clinicalFeatures='FAB_classification',
       annotationColor=list(FAB_classification=c(M0='#0072B2', M1='#D55E00')), sortByAnnotation=TRUE, removeNonMutated=FALSE); dev.off()})
cat("partial annotationColor result class:", class(r2), "\n")
