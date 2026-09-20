proper=$(samtools view -c -f 2 /mnt/openscience/audits/bio-alignment-validation/run/data/idx/real_1000g_chr20.bam)
mapped=$(samtools view -c -F 4 /mnt/openscience/audits/bio-alignment-validation/run/data/idx/real_1000g_chr20.bam)
rate=$(echo "scale=4; $proper / $mapped * 100" | bc)
echo "Proper pairing rate: ${rate}%"
