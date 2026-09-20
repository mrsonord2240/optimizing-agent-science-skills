# writes rmats_JC_results.tsv and rmats_JCEC_results.tsv into --out-dir
python3 jutils.py convert-results --rmats-dir rmats_output/ --out-dir jutils_out/

# meta.tsv: sample<TAB>condition. Needs >= 2 events passing the cutoffs; writes clustermap*.pdf
python3 jutils.py heatmap --tsv-file jutils_out/rmats_JC_results.tsv --meta-file meta.tsv --q-value 0.05 --out-dir hm/ --pdf

# bam_list.tsv: sample<TAB>bam<TAB>condition
python3 jutils.py sashimi --tsv-file jutils_out/rmats_JC_results.tsv --meta-file meta.tsv \
    --gtf annotation.gtf --coordinate chr1:1000-2000 --bam-list bam_list.tsv --out-dir sh/ --pdf

# --tsv-file-list is a FILE with one "path<TAB>label" line per TSV, not a comma-separated list
printf 'jutils_out/rmats_JC_results.tsv\trMATS_JC\njutils_out/rmats_JCEC_results.tsv\trMATS_JCEC\n' > tsv_list.txt   # one line per TSV to compare
python3 jutils.py venn-diagram --tsv-file-list tsv_list.txt --out-dir vn/
