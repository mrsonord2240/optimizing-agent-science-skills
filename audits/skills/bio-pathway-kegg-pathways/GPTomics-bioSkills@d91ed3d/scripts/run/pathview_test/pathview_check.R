suppressMessages(library(pathview))
de <- read.csv('../../data/SYNTHETIC_de_results.csv')
vals <- setNames(de$log2FoldChange, de$entrez)
vals <- vals[!is.na(names(vals))]
out <- tryCatch({
  pathview(gene.data=vals, pathway.id='04110', species='hsa', gene.idtype='entrez',
           kegg.dir=tempdir(), limit=list(gene=3))
}, error=function(e) paste("ERROR:", conditionMessage(e)))
if (is.character(out)) cat(out, "\n") else cat("pathview returned object, class:", class(out), "\n")
cat("files in cwd after call:\n")
print(list.files(pattern="hsa04110"))
