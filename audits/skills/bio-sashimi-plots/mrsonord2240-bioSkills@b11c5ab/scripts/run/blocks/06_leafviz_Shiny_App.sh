# annotation_code = prefix of four files (_all_exons.txt.gz, _all_introns.bed.gz, _fiveprime.bed.gz, _threeprime.bed.gz);
# build them from the GTF version used in the differential analysis
perl leafcutter/leafviz/gtf2leafcutter.pl -o annot annotation.gtf

# groups.txt = the support file given to leafcutter_ds.R (sample <TAB> condition)
Rscript leafcutter/leafviz/prepare_results.R \
    -o leafviz.RData \
    -m groups.txt \
    leafcutter_perind_numers.counts.gz \
    ds_results_cluster_significance.txt \
    ds_results_effect_sizes.txt \
    annot

# runApp() uses the working directory: start from leafviz/, pass the .RData by absolute path
cd leafcutter/leafviz && Rscript run_leafviz.R /abs/path/leafviz.RData    # prints "Listening on http://127.0.0.1:<port>"
