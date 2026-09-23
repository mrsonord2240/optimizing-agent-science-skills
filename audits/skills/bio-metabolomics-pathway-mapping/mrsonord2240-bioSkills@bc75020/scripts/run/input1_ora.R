# Input 1 (Canonical): ORA on identified compounds with assay-specific background,
# following bio-metabolomics-pathway-mapping SKILL.md pattern exactly.
suppressMessages(library(MetaboAnalystR))

mSet <- InitDataObjects('conc', 'pathora', FALSE)
mSet <- SetOrganism(mSet, 'hsa')

compounds <- c('Pyruvate','L-Lactate','Citrate','Succinate','Fumarate','L-Alanine',
               'L-Glutamate','L-Glutamine','Malate','Isocitrate','Oxaloacetate','Acetyl-CoA')
mSet <- Setup.MapData(mSet, compounds)
mSet <- CrossReferencing(mSet, 'name')
mSet <- CreateMappingResultTable(mSet)
cat("=== Mapping table ===\n")
print(mSet$dataSet$map.table)

mSet <- SetKEGG.PathLib(mSet, 'hsa', 'current')
mSet <- SetMetabolomeFilter(mSet, FALSE)  # start with the SKILL.md's documented default (inflated background)
mSet <- CalculateOraScore(mSet, 'rbc', 'hyperg')

cat("\n=== ORA result (no background filter) ===\n")
if (!is.null(mSet$analSet$ora.mat)) {
  ora <- as.data.frame(mSet$analSet$ora.mat)
  print(head(ora, 10))
} else {
  cat("mSet$analSet$ora.mat is NULL\n")
}
saveRDS(mSet, "input1_mset.rds")
