args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3L) stop("usage: audit_regressions.R <skill-copy> <public-data> <run-dir>")

skill_dir <- normalizePath(args[1], mustWork = TRUE)
public_dir <- normalizePath(args[2], mustWork = TRUE)
run_dir <- normalizePath(args[3], mustWork = TRUE)
out_dir <- file.path(run_dir, "out")
data_dir <- file.path(run_dir, "data")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

suppressPackageStartupMessages({
  library(ComplexHeatmap)
  library(circlize)
  library(grid)
  library(maftools)
})
source(file.path(skill_dir, "scripts", "maf_to_oncoprint.R"))

render_oncoprint <- function(mat, output, top_values = NULL, title = "OncoPrint regression",
                             column_split = NULL) {
  col <- c(Missense = "#56B4E9", Truncating = "#000000", Splice = "#CC79A7",
           Amp = "#D55E00", HomDel = "#0072B2", Fusion = "#009E73")
  alter_fun <- list(
    background = function(x, y, w, h) grid.rect(x, y, w-unit(.4,"mm"), h-unit(.4,"mm"), gp=gpar(fill="#EEEEEE", col=NA)),
    Amp = function(x, y, w, h) grid.rect(x, y, w-unit(.4,"mm"), h-unit(.4,"mm"), gp=gpar(fill=col["Amp"], col=NA)),
    HomDel = function(x, y, w, h) grid.rect(x, y, w-unit(.4,"mm"), h-unit(.4,"mm"), gp=gpar(fill=col["HomDel"], col=NA)),
    Missense = function(x, y, w, h) grid.rect(x, y, w-unit(.4,"mm"), h*.5, gp=gpar(fill=col["Missense"], col=NA)),
    Truncating = function(x, y, w, h) grid.rect(x, y, w-unit(.4,"mm"), h*.33, gp=gpar(fill=col["Truncating"], col=NA)),
    Splice = function(x, y, w, h) grid.rect(x, y, w-unit(.4,"mm"), h*.25, gp=gpar(fill=col["Splice"], col=NA)),
    Fusion = function(x, y, w, h) grid.points(x, y, pch=17, size=unit(2,"mm"), gp=gpar(col=col["Fusion"]))
  )
  ha <- NULL
  if (!is.null(top_values)) {
    annotation_levels <- sort(unique(stats::na.omit(top_values)))
    ha <- HeatmapAnnotation(FAB = top_values,
      col = list(FAB = setNames(grDevices::hcl.colors(length(annotation_levels), "Dark 3"), annotation_levels)))
  }
  ht <- oncoPrint(mat, alter_fun=alter_fun, col=col, top_annotation=ha,
                  row_order=order(-rowSums(mat != "")), remove_empty_columns=FALSE,
                  remove_empty_rows=FALSE, show_pct=TRUE, column_title=title,
                  row_names_gp=gpar(fontsize=8), pct_gp=gpar(fontsize=7),
                  column_split=column_split)
  png(output, width=1800, height=1000, res=150)
  draw(ht, heatmap_legend_side="right", annotation_legend_side="right")
  dev.off()
  stopifnot(file.info(output)$size > 1000)
}

cat("ENV ComplexHeatmap", as.character(packageVersion("ComplexHeatmap")),
    "maftools", as.character(packageVersion("maftools")),
    "circlize", as.character(packageVersion("circlize")), "\n")

# Input 1: canonical TCGA-LAML cohort-complete ComplexHeatmap.
maf_path <- file.path(public_dir, "mutations", "tcga_laml.maf.gz")
clin_path <- file.path(public_dir, "mutations", "tcga_laml_annot.tsv")
maf_df <- read.delim(gzfile(maf_path), comment.char="#", check.names=FALSE, quote="")
clinical <- read.delim(clin_path, check.names=FALSE)
mat1 <- maf_to_oncoprint(maf_df, clinical$Tumor_Sample_Barcode, top=20)
aligned1 <- align_oncoprint_clinical(clinical[nrow(clinical):1,], colnames(mat1))
stopifnot(ncol(mat1) == nrow(clinical), identical(aligned1$Tumor_Sample_Barcode, colnames(mat1)))
stopifnot(all(diff(rowSums(mat1 != "")) <= 0))
render_oncoprint(mat1, file.path(out_dir,"i1_laml_complexheatmap.png"), aligned1$FAB_classification,
                 sprintf("TCGA-LAML cohort complete (N=%d)", ncol(mat1)))
cat("INPUT1 PASS samples", ncol(mat1), "genes", nrow(mat1), "top", rownames(mat1)[1],
    "freq", rowSums(mat1 != "")[1], "ignored", paste(attr(mat1,"ignored_variant_classifications"), collapse=","), "\n")

# Input 2: maftools quick path with complete colors and denominator check.
maf_obj <- read.maf(maf_path, clinicalData=clinical, verbose=FALSE)
fab_levels <- sort(unique(getClinicalData(maf_obj)$FAB_classification))
fab_cols <- setNames(grDevices::hcl.colors(length(fab_levels), "Dark 3"), fab_levels)
png(file.path(out_dir,"i2_laml_maftools.png"), width=1800, height=900, res=150)
oncoplot(maf_obj, top=20, clinicalFeatures=c("FAB_classification","Overall_Survival_Status"),
         annotationColor=list(FAB_classification=fab_cols, Overall_Survival_Status="Blues"),
         sortByAnnotation=TRUE, removeNonMutated=FALSE)
dev.off()
stopifnot(file.info(file.path(out_dir,"i2_laml_maftools.png"))$size > 1000)
stopifnot(nrow(getClinicalData(maf_obj)) < nrow(clinical))
cat("INPUT2 PASS maftools samples", nrow(getClinicalData(maf_obj)), "cohort", nrow(clinical),
    "complete FAB colors", length(fab_cols), "\n")

# Input 3: archived 30-sample edge cohort regression.
edge_maf <- read.delim(file.path(data_dir,"synth_edge.maf"), check.names=FALSE)
edge_clin <- read.delim(file.path(data_dir,"synth_edge_clin.tsv"), check.names=FALSE)
mat3 <- maf_to_oncoprint(edge_maf, edge_clin$Tumor_Sample_Barcode, top=6)
aligned3 <- align_oncoprint_clinical(edge_clin[nrow(edge_clin):1,], colnames(mat3))
stopifnot(ncol(mat3)==30, any(colSums(mat3 != "")==0), all(diff(rowSums(mat3 != ""))<=0))
stopifnot(identical(aligned3$Tumor_Sample_Barcode, colnames(mat3)))
stopifnot(mat3["TP53","S02"] == "Missense")
empty_error <- try(maf_to_oncoprint(edge_maf[0,], edge_clin$Tumor_Sample_Barcode, genes="TP53"), silent=TRUE)
stopifnot(inherits(empty_error,"try-error"), grepl("all-empty|No mapped", as.character(empty_error), ignore.case=TRUE))
render_oncoprint(mat3, file.path(out_dir,"i3_edge_cohort.png"), title="Synthetic edge cohort (N=30)")
cat("INPUT3 PASS columns", ncol(mat3), "zero-mutation", sum(colSums(mat3 != "")==0),
    "TP53pct", round(100*mean(mat3["TP53",] != "")), "empty guard actionable\n")

# Input 5: archived 600-sample stress case, exact alignment, split panels, log-TMB behavior.
stress_maf <- read.delim(file.path(data_dir,"synth_cohort.maf"), check.names=FALSE)
stress_clin <- read.delim(file.path(data_dir,"synth_cohort_clin.tsv"), check.names=FALSE)
names(stress_clin)[names(stress_clin)=="subtype"] <- "Subtype"
names(stress_clin)[names(stress_clin)=="stage"] <- "Stage"
mat5 <- maf_to_oncoprint(stress_maf, stress_clin$Tumor_Sample_Barcode, top=12)
set.seed(20260927)
aligned5 <- align_oncoprint_clinical(stress_clin[sample(nrow(stress_clin)),], colnames(mat5))
stopifnot(ncol(mat5)==600, identical(aligned5$Tumor_Sample_Barcode,colnames(mat5)))
stopifnot(all(diff(rowSums(mat5 != ""))<=0), all(table(aligned5$Subtype)==c(Basal=180,HER2=120,Luminal=300)))
log_tmb <- log10(aligned5$tmb+1)
stopifnot(max(log_tmb)/median(log_tmb) < 3)
render_oncoprint(mat5, file.path(out_dir,"i5_stress_split.png"), aligned5$Subtype,
                 title="Synthetic 600-sample stress cohort", column_split=aligned5$Subtype)
cat("INPUT5 PASS samples",ncol(mat5),"split",paste(names(table(aligned5$Subtype)),table(aligned5$Subtype),collapse=","),
    "log TMB max/median",round(max(log_tmb)/median(log_tmb),3),"\n")

# Input 6: return schema and independent Fisher check for somaticInteractions.
png(file.path(out_dir,"i6_interactions.png"), width=1400, height=1200, res=150)
si <- somaticInteractions(maf_obj, top=20, pvalue=c(.05,.01), fontSize=.7)
dev.off()
required_si <- c("gene1","gene2","pValue","oddsRatio","00","01","11","10","pAdj","Event")
stopifnot(all(required_si %in% names(si)), nrow(si)>0)
first <- si[1]
tab <- matrix(c(first$`11`, first$`10`, first$`01`, first$`00`), nrow=2)
p_ind <- fisher.test(tab)$p.value
stopifnot(abs(p_ind-first$pValue) < 1e-10)
write.csv(si, file.path(out_dir,"i6_interactions.csv"), row.names=FALSE)
cat("INPUT6 PASS rows", nrow(si), "columns", paste(required_si,collapse=","),
    "first fisher delta", format(abs(p_ind-first$pValue),scientific=TRUE), "\n")

# Input 7: adversarial ID mismatch/unmapped classes/denominator manipulation.
bad_clin <- edge_clin
bad_clin$Tumor_Sample_Barcode <- paste0("X", bad_clin$Tumor_Sample_Barcode)
bad_align <- try(align_oncoprint_clinical(bad_clin, colnames(mat3)), silent=TRUE)
stopifnot(inherits(bad_align,"try-error"), grepl("missing matrix sample",as.character(bad_align)))
silent_only <- edge_maf
silent_only$Variant_Classification <- "Silent"
silent_err <- try(maf_to_oncoprint(silent_only, edge_clin$Tumor_Sample_Barcode, genes="TP53"), silent=TRUE)
stopifnot(inherits(silent_err,"try-error"))
cohort_pct <- rowSums(mat3 != "")/ncol(mat3)
altered_only_pct <- rowSums(mat3 != "")/sum(colSums(mat3 != "")>0)
stopifnot(any(abs(cohort_pct-altered_only_pct)>.01))
cat("INPUT7 PASS ID mismatch rejected; unmapped-only rejected; TP53 cohort pct",
    round(100*cohort_pct["TP53"]), "altered-only", round(100*altered_only_pct["TP53"]), "\n")

# Input 8 (new): all alteration classes via the canonical additional_calls seam.
samples8 <- sprintf("C%02d",1:12)
maf8 <- data.frame(Hugo_Symbol=c("TP53","TP53","KRAS","RB1","EGFR"),
                   Tumor_Sample_Barcode=c("C01","C01","C02","C03","C04"),
                   Variant_Classification=c("Missense_Mutation","Missense_Mutation","Splice_Site","Nonsense_Mutation","Silent"))
extra8 <- data.frame(Hugo_Symbol=c("MYC","CDKN2A","ALK","TP53","MYC"),
                     Tumor_Sample_Barcode=c("C05","C06","C07","C01","C05"),
                     alteration_class=c("Amp","HomDel","Fusion","Amp","Amp"))
mat8 <- maf_to_oncoprint(maf8, samples8, genes=c("TP53","KRAS","RB1","MYC","CDKN2A","ALK"), additional_calls=extra8)
stopifnot(mat8["TP53","C01"]=="Amp;Missense", mat8["KRAS","C02"]=="Splice",
          mat8["RB1","C03"]=="Truncating", mat8["MYC","C05"]=="Amp",
          mat8["CDKN2A","C06"]=="HomDel", mat8["ALK","C07"]=="Fusion")
stopifnot(sum(colSums(mat8 != "")==0)==6, identical(attr(mat8,"ignored_variant_classifications"),"Silent"))
clin8 <- data.frame(Tumor_Sample_Barcode=rev(samples8), Group=rep(c("A","B"),6))
stopifnot(identical(align_oncoprint_clinical(clin8,colnames(mat8))$Tumor_Sample_Barcode,colnames(mat8)))
dup_err <- try(maf_to_oncoprint(maf8,c(samples8,"C01")),silent=TRUE)
unknown_class_err <- try(maf_to_oncoprint(maf8,samples8,additional_calls=transform(extra8,alteration_class="Gain")),silent=TRUE)
stopifnot(inherits(dup_err,"try-error"),inherits(unknown_class_err,"try-error"))
render_oncoprint(mat8, file.path(out_dir,"i8_new_all_classes.png"), title="All six alteration classes")
cat("INPUT8 PASS all six classes, duplicate collapse, six zero-mutation samples, invalid cohort/class rejected\n")

cat("ALL R REGRESSIONS PASS\n")
