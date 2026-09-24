micromamba run -n as-rleaf Rscript $LEAFCUTTER/scripts/leafcutter_ds.R --num_threads 4 -i 3 -g 3 -c 10 \
    --exon_file gencode_exons.txt.gz \
    lck_perind_numers.counts.gz groups.txt -o ds_results
