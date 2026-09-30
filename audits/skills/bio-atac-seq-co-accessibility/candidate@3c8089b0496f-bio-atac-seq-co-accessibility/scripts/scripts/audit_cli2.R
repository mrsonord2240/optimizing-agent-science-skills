suppressPackageStartupMessages({library(Matrix); library(monocle3)})
I <- file.path(Sys.getenv("CO"), "work/input")
pm <- read.delim(file.path(I, "peak_metadata.tsv"), row.names=1); cm <- read.delim(file.path(I, "cell_metadata.tsv"), row.names=1)
pat <- readMM(file.path(I, "peak_matrix.mtx"))
ss <- summary(pat); num <- sparseMatrix(i=ss$i, j=ss$j, x=c(2, rep(1, nrow(ss)-1)), dims=dim(pat))  # explicit numeric 0/1 matrix, as a count export would be
tf <- tempfile(fileext=".mtx"); writeMM(as(num, "CsparseMatrix"), tf)
cat("header numeric mtx:", readLines(tf, 1), "\n")
rd <- readMM(tf); cat("readMM(numeric) class:", class(rd), " has dimnames:", !is.null(unlist(dimnames(rd))), "\n")
try1 <- function(lbl, m) { r <- try(new_cell_data_set(m, cell_metadata=cm, gene_metadata=pm), silent=TRUE)
  cat(sprintf("%-58s %s\n", lbl, if (inherits(r,"try-error")) trimws(sub("Error : ","",as.character(r))) else sprintf("OK %d x %d", nrow(r), ncol(r)))) }
try1("A pattern mtx as readMM returns (shipped CLI path)", pat)
try1("B numeric mtx as readMM returns (shipped CLI path)", rd)
m3 <- as(rd, "CsparseMatrix"); try1("C numeric, converted to dgCMatrix, no dimnames", m3)
dimnames(m3) <- list(rownames(pm), rownames(cm)); try1("D numeric dgCMatrix + dimnames from metadata (diagnostic)", m3)
