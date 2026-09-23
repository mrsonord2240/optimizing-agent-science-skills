# GenomicSEM is GitHub-only
remotes::install_github('GenomicSEM/GenomicSEM')

# Pin lavaan to 0.6.19 -- lavaan >=0.7.0 breaks usermodel()/commonfactorGWAS()/userGWAS()
# (see Version Compatibility). install_github above may pull a newer lavaan as a dependency;
# always run this line after it, and re-run it if packageVersion('lavaan') drifts to >=0.7.
remotes::install_version('lavaan', version = '0.6-19')

# Dependencies
install.packages(c('Matrix', 'gdata'))

# Optional companions
remotes::install_github('MRCIEU/TwoSampleMR')  # for downstream MR using factor GWAS as exposure
