source /mnt/openscience/audits/bio-atac-seq-atac-peak-calling/reaudit-run/scripts/env.sh
# Independently re-derive the script's split command on rep1 and verify disjointness, pair integrity, coverage.
W=$R/disjoint; rm -rf $W; mkdir -p $W; cd $W
samtools view -b -s 1.5 -U h2.bam -o h1.bam $E1
for f in h1 h2; do samtools view $f.bam | cut -f1 | sort -u > $f.names; done
samtools view $E1 | cut -f1 | sort -u > all.names
echo "reads: total=$(samtools view -c $E1) h1=$(samtools view -c h1.bam) h2=$(samtools view -c h2.bam)"
echo "names: all=$(wc -l < all.names) h1=$(wc -l < h1.names) h2=$(wc -l < h2.names) shared=$(comm -12 h1.names h2.names | wc -l) union=$(sort -u h1.names h2.names | wc -l)"
echo "flag-1 reads (paired) : $(samtools view -c -f1 $E1) of $(samtools view -c $E1)"
# pair integrity: count of names appearing in only one half's records with count 1 while original had 2
samtools view $E1 | cut -f1 | sort | uniq -c | awk '{c[$1]++} END{for(k in c)print "orig name multiplicity",k,c[k]}'
samtools view h1.bam | cut -f1 | sort | uniq -c | awk '{c[$1]++} END{for(k in c)print "h1 name multiplicity",k,c[k]}'
