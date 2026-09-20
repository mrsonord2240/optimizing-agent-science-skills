# rmats2sashimiplot plots every row: keep only significant events (columns found by header name)
awk -F'\t' 'NR==1{for(i=1;i<=NF;i++)c[$i]=i; print; next}
    $c["FDR"]<0.05 && ($c["IncLevelDifference"]>0.1 || $c["IncLevelDifference"]<-0.1)' \
    rmats_output/SE.MATS.JC.txt > sig.SE.MATS.JC.txt

# group file: "label: first-last", 1-based over the --b1 replicates then the --b2 replicates
printf 'Control: 1-3\nTreatment: 4-6\n' > grouping.gf

rmats2sashimiplot \
    --b1 G1_rep1.bam,G1_rep2.bam,G1_rep3.bam \
    --b2 G2_rep1.bam,G2_rep2.bam,G2_rep3.bam \
    --event-type SE \
    -e sig.SE.MATS.JC.txt \
    --l1 Control \
    --l2 Treatment \
    -o sashimi_rmats \
    --exon_s 1 \
    --intron_s 5 \
    --group-info grouping.gf \
    --color '#1f77b4,#ff7f0e'

n_events=$(( $(wc -l < sig.SE.MATS.JC.txt) - 1 ))
n_pdf=$(find sashimi_rmats/Sashimi_plot -name '*.pdf' -size +0 2>/dev/null | wc -l)
[ "$n_pdf" -eq "$n_events" ] || { echo "rmats2sashimiplot wrote $n_pdf of $n_events figures" >&2; exit 1; }
