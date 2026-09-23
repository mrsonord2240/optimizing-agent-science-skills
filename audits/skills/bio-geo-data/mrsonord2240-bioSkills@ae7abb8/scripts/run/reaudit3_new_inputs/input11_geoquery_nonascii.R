# Input 11 (re-auditor NEW, mine): the Skill claims Python (GEOparse/Entrez) and R (GEOquery)
# are interchangeable parity paths ("Both contain the same content" for SOFT/MINiML; GEOquery
# recommended as the "more reliable" choice). Nobody in this audit lineage has tested the R path
# against a series matrix with real non-ASCII content -- only against all-ASCII GSE470. This
# checks whether R's getGEO() has an equivalent encoding trap on Windows, independent of the
# Python-side fix.

library(GEOquery)

path <- "GSE283260_matrix.txt.gz"
cat("Using path:", path, "\n")

gse <- getGEO(filename = path)

cat("class(gse):", class(gse), "\n")
cat("dim(exprs(gse)):", dim(exprs(gse)), "\n")
cat("nrow(pData(gse)):", nrow(pData(gse)), "\n")
cat("Series_geo_accession:", gse@experimentData@other$geo_accession, "\n")

# Look for non-ASCII content in the characteristics / title fields, to confirm R actually reads
# through the same non-ASCII bytes Python's parse_series_matrix() decoded via errors='replace'.
title_val <- gse@experimentData@title
cat("Series title:", title_val, "\n")
raw_bytes <- charToRaw(title_val)
nonascii <- raw_bytes[as.integer(raw_bytes) >= 0x80]
cat("Non-ASCII bytes in title (count):", length(nonascii), "\n")

# Scan all pData columns and the title/summary fields for any non-ASCII byte, to see whether R's
# default read path even encounters the same bytes Python's fixed parser had to errors='replace'.
all_text <- c(as.character(unlist(pData(gse))), title_val, gse@experimentData@abstract)
combined <- paste(all_text, collapse = " ")
raw_all <- charToRaw(combined)
nonascii_all <- raw_all[as.integer(raw_all) >= 0x80]
cat("Non-ASCII bytes across all read fields (count):", length(nonascii_all), "\n")
cat("Sys.getlocale():", Sys.getlocale(), "\n")
cat("RESULT: getGEO() completed without error.\n")
