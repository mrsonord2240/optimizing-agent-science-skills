root <- '/mnt/openscience/audits/bio-pathway-reactome/run/phase2_e66cde9_linux_20260923'
setwd(file.path(root,'outputs'))
source(file.path(root,'source_copy/examples/reactome_ora.R'))
stopifnot(nrow(results_df)>0)
write.csv(results_df,file.path(root,'outputs','ora.csv'),row.names=FALSE)
cat('ASSERT ora_rows=',nrow(results_df),'\n',sep='')
