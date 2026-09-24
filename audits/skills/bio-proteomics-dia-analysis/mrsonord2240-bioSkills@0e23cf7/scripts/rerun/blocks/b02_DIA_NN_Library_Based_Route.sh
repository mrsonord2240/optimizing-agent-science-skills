diann \
    --f sample1.mzML --f sample2.mzML \
    --lib spectral_library.parquet --fasta uniprot_human.fasta \
    --out diann_out/report.parquet \
    --qvalue 0.01 --matrices \
    --mass-acc 15 --mass-acc-ms1 15 \
    --reanalyse --smart-profiling \
    --threads 8
