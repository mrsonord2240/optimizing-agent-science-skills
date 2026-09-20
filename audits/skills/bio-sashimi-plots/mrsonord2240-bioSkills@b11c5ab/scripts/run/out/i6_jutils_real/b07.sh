# writes rmats_JC_results.tsv and rmats_JCEC_results.tsv into --out-dir
micromamba run -n as-viz-gg34 python3 /mnt/openscience/audit-envs/alternative-splicing/tools/src/Jutils/jutils.py convert-results --rmats-dir rmats_output/ --out-dir jutils_out/

# meta.tsv: sample<TAB>condition. Needs >= 2 events passing the cutoffs; writes clustermap*.pdf
micromamba run -n as-viz-gg34 python3 /mnt/openscience/audit-envs/alternative-splicing/tools/src/Jutils/jutils.py heatmap --tsv-file jutils_out/rmats_JC_results.tsv --meta-file meta.tsv --q-value 0.05 --out-dir hm/ --pdf

# bam_list.tsv: sample<TAB>bam<TAB>condition
micromamba run -n as-viz-gg34 python3 /mnt/openscience/audit-envs/alternative-splicing/tools/src/Jutils/jutils.py sashimi --tsv-file jutils_out/rmats_JC_results.tsv --meta-file meta.tsv \
    --gtf /mnt/openscience/audit-envs/alternative-splicing/public-data/rnasplice/reference/genes_chrX.gtf --coordinate X:69508604-69510295 --bam-list bam_list.tsv --out-dir sh/ --pdf

# --tsv-file-list is a FILE with one "path<TAB>label" line per TSV, not a comma-separated list
printf 'jutils_out/rmats_JC_results.tsv\trMATS_JC\njutils_out/rmats_JCEC_results.tsv\trMATS_JCEC\n' > tsv_list.txt   # one line per TSV to compare
micromamba run -n as-viz-gg34 python3 /mnt/openscience/audit-envs/alternative-splicing/tools/src/Jutils/jutils.py venn-diagram --tsv-file-list tsv_list.txt --out-dir vn/
