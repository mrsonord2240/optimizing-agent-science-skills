for (p in c("GSVA","limma","fgsea","clusterProfiler","msigdbr","optparse","pheatmap","ggplot2","dplyr","data.table","GSEABase","reshape2","tidyr","tibble","org.Hs.eg.db","ggpubr","corrplot","Hmisc","RColorBrewer","cowplot","stringr","readr","jsonlite","R6","ggcorrplot","reshape","circlize","ComplexHeatmap")) {
 ok <- suppressWarnings(suppressMessages(require(p, character.only=TRUE, quietly=TRUE)))
 cat(p, ok, if(ok) as.character(packageVersion(p)), "\n")}
