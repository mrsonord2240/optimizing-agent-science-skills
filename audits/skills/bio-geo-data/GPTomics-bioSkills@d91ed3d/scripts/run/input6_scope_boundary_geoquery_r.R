# Input 6 (Scope Boundary): "Use R's GEOquery (the Skill's documented
# 'more reliable' choice for supplementary-file work) to load GSE470 from the
# already-downloaded series matrix file, and cross-validate exprs()/pData()
# dimensions against the Python series-matrix parser's result (expr.shape ==
# (12625, 12) from Input 3). This pushes slightly outside the Skill's most
# common Python-first path into its parallel R-first path, to check both are
# actually consistent as the Skill claims ('Both contain the same content').

library(GEOquery)

path <- "F:/OpenScience/audit-envs/database-access/public-data/geo-data/GSE470_series_matrix.txt.gz"
gse <- getGEO(filename = path)

cat("class(gse):", class(gse), "\n")
cat("dim(exprs(gse)):", dim(exprs(gse)), "\n")
cat("nrow(pData(gse)):", nrow(pData(gse)), "\n")
cat("annotation(gse):", annotation(gse), "\n")
cat("Series_geo_accession:", gse@experimentData@other$geo_accession, "\n")

# Cross-check against Python's expr.shape == (12625, 12) from Input 3
py_shape <- c(12625, 12)
r_shape <- dim(exprs(gse))
match_ok <- all(py_shape == r_shape)
cat("Python parse_series_matrix() shape:", py_shape, "\n")
cat("R GEOquery exprs() shape:          ", r_shape, "\n")
cat("Shapes match:", match_ok, "\n")
