suppressMessages(library(lipidr))
print(lipidr:::normalize_istd)
cat("\n=== lipid_maps_db istd rows sample ===\n")
db <- lipidr:::lipid_maps_db
print(head(db[db$istd == TRUE, c("Molecule","Class","istd")], 20))
