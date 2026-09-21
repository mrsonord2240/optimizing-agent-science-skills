# Install via bioconda (DROP is not on PyPI)
mamba create -n drop_env -c conda-forge -c bioconda drop --override-channels
conda activate drop_env

mkdir my_diagnostic_run && cd my_diagnostic_run
drop init          # takes no project-name argument; run it in the empty directory

# Edit config.yaml (checked on DROP 1.6.1): fill sampleAnnotation, geneAnnotation, genome, root, htmlOutputPath;
#  aberrantSplicing: run: true   (implementation: PCA, FRASER_version: "FRASER2", padjCutoff 0.1, deltaPsiCutoff 0.1)
#  aberrantExpression: run: true (implementation: autoencoder)
#  mae: run: true                (needs RNA BAMs matched to a VCF)

snakemake aberrantSplicing --cores 16    # or aberrantExpression / mae; no --use-conda: DROP's rules have no conda: directives
