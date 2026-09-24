root <- '/mnt/openscience/audits/bio-pathway-reactome/run/phase2_e66cde9_linux_20260923'
setwd(file.path(root,'outputs'))
source(file.path(root,'source_copy/examples/reactome_gsea.R'))
stopifnot(nrow(results_df)>0, results_df$ID[1]==planted_id)
write.csv(results_df,file.path(root,'outputs','gsea.csv'),row.names=FALSE)
cat('ASSERT gsea_rows=',nrow(results_df),' rank1=',results_df$ID[1],'\n',sep='')
