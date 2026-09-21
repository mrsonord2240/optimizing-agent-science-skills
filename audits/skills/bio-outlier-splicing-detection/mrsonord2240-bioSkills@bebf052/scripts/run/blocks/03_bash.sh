for bam in *.bam; do
    regtools junctions extract -a 8 -m 50 -s XS "$bam" -o "${bam%.bam}.junc"
done

ls *.junc > juncfiles.txt
python leafcutter_cluster_regtools.py -j juncfiles.txt -o leafcutter -m 50 -l 500000

leafcutterMD.R \
    --num_threads 4 \
    --output_prefix patient_outlier \
    leafcutter_perind_numers.counts.gz
