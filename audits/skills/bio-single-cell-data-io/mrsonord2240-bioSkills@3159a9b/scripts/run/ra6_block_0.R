install.packages('Seurat')
# Conversion (prefer maintained tools; SeuratDisk is abandoned):
remotes::install_github('scverse/anndataR')          # pure-R h5ad/zarr I/O + conversion; requires R >= 4.5
BiocManager::install('zellkonverter')                # SCE <-> AnnData
remotes::install_github('cellgeni/schard')           # robust pure-R h5ad reading
