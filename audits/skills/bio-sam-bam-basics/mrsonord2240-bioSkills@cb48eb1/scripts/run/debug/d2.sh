cd /mnt/openscience/audits/bio-sam-bam-basics/run/data/in7
samtools view hand.sam | awk -F'\t' '{print $1, $2, NF}' | head -3
samtools view c3.sam | awk -F'\t' '{print $1, $2, NF}' | head -3
samtools view c3.sam | awk -F'\t' 'NF>11{print $1,$2,$12,$13}' | sort | uniq -c | head
samtools view hand.sam | awk -F'\t' 'NF>11{print $1,$2,$12,$13}' | sort | uniq -c | head
echo == mm2 eqx CRAM
A=/mnt/openscience/audits/bio-sam-bam-basics/run/data/aln
ls $A 2>/dev/null | head -3
