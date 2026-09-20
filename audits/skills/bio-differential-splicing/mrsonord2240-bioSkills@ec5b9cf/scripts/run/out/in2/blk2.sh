# Strand comes from the XS tag: the BAMs need it (STAR --outSAMstrandField intronMotif); without XS regtools writes strand '?' and leafcutter drops every junction
for bam in *.bam; do
    regtools junctions extract -a 8 -m 50 -s XS "$bam" -o "${bam%.bam}.junc"
done
ls *.junc > juncfiles.txt

# LEAFCUTTER = a clone of github.com/davidaknowles/leafcutter (the R package does not install these scripts on PATH)
python $LEAFCUTTER/clustering/leafcutter_cluster_regtools.py \
    -j juncfiles.txt \
    -o leafcutter \
    -m 50 \
    -l 500000
