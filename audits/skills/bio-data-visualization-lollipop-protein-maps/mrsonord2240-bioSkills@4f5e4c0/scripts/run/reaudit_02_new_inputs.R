# Independent new-input tests for the corrected lollipop-map skill.
# Usage: r.sh reaudit_02_new_inputs.R <worktree> <outdir>
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 2L)
worktree <- normalizePath(args[[1L]], winslash = "/", mustWork = TRUE)
out <- normalizePath(args[[2L]], winslash = "/", mustWork = FALSE)
dir.create(out, recursive = TRUE, showWarnings = FALSE)

suppressPackageStartupMessages({
  library(data.table)
  library(maftools)
  library(trackViewer)
  library(GenomicRanges)
})

skill_file <- file.path(worktree, "data-visualization", "lollipop-protein-maps", "SKILL.md")
example_file <- file.path(worktree, "data-visualization", "lollipop-protein-maps", "examples", "lollipop_phd.R")
stopifnot(file.exists(skill_file), file.exists(example_file))
skill_text <- paste(readLines(skill_file, warn = FALSE), collapse = "\n")
example_text <- paste(readLines(example_file, warn = FALSE), collapse = "\n")

protein_position <- function(change) {
  x <- trimws(as.character(change))
  take <- function(pattern, x) {
    hits <- regmatches(x, regexec(pattern, x))
    vapply(hits, function(h) if (length(h) >= 2L) as.integer(h[[2L]]) else NA_integer_, integer(1))
  }
  out <- take("^p\\.[A-Z*](\\d+)", x)
  out[grepl("^p\\.[A-Z][0-9]+\\?$", x)] <- NA_integer_
  missing <- is.na(out)
  out[missing] <- take("^p\\.[A-Z][a-z]{2}(\\d+)", x[missing])
  out
}

# New input A: a valid MAF whose available column is Protein_Change, with a
# duplicate sample, three-letter notation, stop extension, and an unknown class.
maf_path <- file.path(out, "protein_change_only.maf")
maf_dt <- data.table(
  Hugo_Symbol = "TP53", Entrez_Gene_Id = 7157L, Center = "reaudit",
  NCBI_Build = "GRCh38", Chromosome = "17", Start_Position = 1:7,
  End_Position = 1:7, Strand = "+", Variant_Classification = c(
    "Missense_Mutation", "Missense_Mutation", "Missense_Mutation",
    "Translation_Start_Site", "Nonstop_Mutation", "RNA", "Silent"),
  Variant_Type = "SNP", Reference_Allele = "C", Tumor_Seq_Allele1 = "C",
  Tumor_Seq_Allele2 = "T", Tumor_Sample_Barcode = c("A", "A", "B", "C", "D", "E", "F"),
  Protein_Change = c("p.R175H", "p.R175H", "p.Arg175His", "p.M1?", "p.*394Wext*?", "p.Gly12Asp", "p.=")
)
fwrite(maf_dt, maf_path, sep = "\t")
maf <- read.maf(maf_path, verbose = FALSE)
change_col <- intersect(c("HGVSp_Short", "Protein_Change", "AAChange"), names(maf@data))
stopifnot(identical(change_col, "Protein_Change"))
stopifnot(identical(protein_position(c("p.R175H", "p.Arg175His", "p.*394Wext*?", "p.M1?", "p.=", "")), c(175L, 175L, 394L, NA_integer_, NA_integer_, NA_integer_)))

# The standard maftools route must accept the selected non-HGVSp column.
pdf(file.path(out, "protein_change_maftools.pdf"), width = 8, height = 4)
result <- lollipopPlot(maf = maf, gene = "TP53", AACol = change_col, refSeqID = "NM_000546", printCount = TRUE,
                       colors = c(Missense_Mutation = "#D55E00", Translation_Start_Site = "#999999", Nonstop_Mutation = "#E69F00"))
dev.off()
stopifnot(file.exists(file.path(out, "protein_change_maftools.pdf")), file.info(file.path(out, "protein_change_maftools.pdf"))$size > 1000L, inherits(result, "data.table"))

# New input B: reproduce safe trackViewer aggregation/palette behavior without
# factor-indexing; unmapped class becomes Other and residue labels are retained.
calls <- as.data.table(maf@data)
calls[, aa_pos := protein_position(get(change_col))]
bad <- calls[is.na(aa_pos)]
calls <- calls[!is.na(aa_pos) & aa_pos >= 1L & aa_pos <= 393L]
class_col <- c(Missense_Mutation = "#D55E00", Translation_Start_Site = "#999999", Nonstop_Mutation = "#E69F00", Other = "#666666")
calls[, plot_class := fifelse(as.character(Variant_Classification) %in% names(class_col), as.character(Variant_Classification), "Other")]
summary <- calls[, .(count = .N, class = plot_class[1L], residue = unique(sub("^p\\.", "", get(change_col)))[1L]), by = aa_pos]
snps <- GRanges("TP53", IRanges(summary$aa_pos, width = 1L), color = unname(class_col[as.character(summary$class)]), score = summary$count)
names(snps) <- ifelse(summary$count >= 2L, summary$residue, "")
features <- GRanges("TP53", IRanges(c(1L, 102L, 325L, 368L), c(44L, 292L, 356L, 387L), names = c("Transactivation", "DNA binding", "Oligomerization", "Basic")), fill = c("#56B4E9", "#0072B2", "#009E73", "#CC79A7"), height = 0.04)
pdf(file.path(out, "protein_change_trackviewer.pdf"), width = 10, height = 4)
lolliplot(snps, features, ylab = "Mutation-row count", xaxis = TRUE, yaxis = TRUE, legend = list(labels = names(class_col), col = unname(class_col)))
dev.off()
stopifnot(!anyNA(mcols(snps)$color), identical(as.character(mcols(snps)$color[1L]), "#D55E00"), names(snps)[1L] == "R175H", file.info(file.path(out, "protein_change_trackviewer.pdf"))$size > 1000L)

# Verify recurrence semantics and the short-isoform warning guidance itself.
rows_at_175 <- nrow(maf_dt[Protein_Change %in% c("p.R175H", "p.Arg175His")])
unique_samples_at_r175h <- uniqueN(maf_dt[Protein_Change == "p.R175H", Tumor_Sample_Barcode])
stopifnot(rows_at_175 == 3L, unique_samples_at_r175h == 1L)
stopifnot(grepl("Deduplicate a duplicate call on `Tumor_Sample_Barcode \\+ HGVSp`", skill_text), grepl("Compare the largest parsed position with the plotted protein length first", skill_text), grepl("g3viz.*1.2.0.*archived from CRAN", skill_text), grepl("saveWidget", example_text), !grepl("pyLollipop|Bio\\.PDB", skill_text))
cat("NEW_INPUTS_PASS\n")
cat("change_col=", change_col, " parsed_positions=175,175,394,NA,NA,NA bad_rows=", nrow(bad), " rows_at_175=", rows_at_175, " unique_r175h_samples=", unique_samples_at_r175h, "\n", sep = "")
