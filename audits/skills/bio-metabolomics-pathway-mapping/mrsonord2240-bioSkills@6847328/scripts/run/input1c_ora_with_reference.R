suppressMessages(library(MetaboAnalystR))
mSet <- InitDataObjects('conc', 'pathora', FALSE)
mSet <- SetOrganism(mSet, 'hsa')
compounds <- c('Pyruvate','L-Lactate','Citrate','Succinate','Fumarate','L-Alanine',
               'L-Glutamate','L-Glutamine','Malate','Isocitrate','Oxaloacetate','Acetyl-CoA')
mSet <- Setup.MapData(mSet, compounds)
mSet <- CrossReferencing(mSet, 'name')
mSet <- CreateMappingResultTable(mSet)
mSet <- SetKEGG.PathLib(mSet, 'hsa', 'current')
mSet <- SetMetabolomeFilter(mSet, TRUE)
mSet <- Setup.KEGGReferenceMetabolome(mSet, "F:/OpenScience/audits/bio-metabolomics-pathway-mapping/data/input1_reference_metabolome_synthetic.txt")
cat("metabo.ref.info:", mSet$dataSet$metabo.ref.info, "\n")
mSet <- CalculateOraScore(mSet, 'rbc', 'hyperg')
cat("\n=== ORA with real reference metabolome (n=320 synthetic) ===\n")
if (!is.null(mSet$analSet$ora.mat)) {
  print(as.data.frame(mSet$analSet$ora.mat)[,c("Raw p","FDR")])
} else {
  cat("ora.mat is NULL; last error:\n")
  print(mSet$msgSet$current.msg)
}
