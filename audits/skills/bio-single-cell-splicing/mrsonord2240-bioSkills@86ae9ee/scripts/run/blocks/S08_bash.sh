# SpliZ is a Nextflow pipeline (not a standalone CLI). Configure inputs in a .config
# file (dataname, input_file, libraryType, grouping_level_1/2) - either SICILIAN
# output (SICILIAN=true) or BAMs via a samplesheet CSV + metadata + GTF (SICILIAN=false).
nextflow run salzmanlab/spliz -r main -latest -c spliz.config
