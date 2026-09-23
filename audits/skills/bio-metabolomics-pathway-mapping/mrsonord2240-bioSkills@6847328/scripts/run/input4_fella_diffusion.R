# Input 4 (Variant B): FELLA network-diffusion mechanism query on identified KEGG compounds,
# following bio-metabolomics-pathway-mapping SKILL.md pattern exactly.
t0 <- Sys.time()
suppressMessages(library(FELLA))
setwd("F:/OpenScience/audits/bio-metabolomics-pathway-mapping/run")

cat("Building KEGG graph (live KEGG REST) ...\n"); flush.console()
graph <- buildGraphFromKEGGREST(organism = 'hsa')
cat("Graph built at", format(Sys.time()-t0), "\n")

buildDataFromGraph(keggdata.graph = graph, databaseDir = 'fella_hsa', internalDir = FALSE)
fella.data <- loadKEGGdata(databaseDir = 'fella_hsa', internalDir = FALSE)
cat("Data loaded at", format(Sys.time()-t0), "\n")

# Same 6 KEGG compound IDs successfully cross-referenced in Input 1 (TCA-cycle-adjacent)
cpd_ids <- c('C00022','C00186','C00158','C00042','C00122','C00041')
analysis <- defineCompounds(compounds = cpd_ids, data = fella.data)
cat("Excluded (unmapped) compounds:\n")
print(getExcluded(analysis))

analysis <- runDiffusion(object = analysis, data = fella.data, approx = 'normality')
results <- generateResultsTable(object = analysis, data = fella.data, method = 'diffusion', threshold = 0.05)
cat("Results table class:", class(results), "\n")
print(head(results, 15))
cat("Total elapsed:", format(Sys.time()-t0), "\n")
