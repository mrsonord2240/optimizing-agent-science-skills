# bioconda: flair isoquant minimap2 samtools bedtools gffread sqanti3 rmats-long ultra_bioinformatics
conda install -c conda-forge -c bioconda flair isoquant minimap2 samtools bedtools gffread   # SQANTI3 (Python 3.11 + R) and rMATS-long: give each its own env
# R: BiocManager::install(c('bambu', 'IsoformSwitchAnalyzeR', 'DRIMSeq', 'stageR'))
# PacBio (single-cell block only): conda install -c bioconda pbskera lima isoseq
