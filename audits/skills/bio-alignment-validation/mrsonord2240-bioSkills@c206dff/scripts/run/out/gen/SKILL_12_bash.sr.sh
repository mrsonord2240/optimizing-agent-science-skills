forward=$(samtools view -c -F 16 /mnt/openscience/audits/bio-alignment-validation/run/data/idx/real_human_PE.bam)
reverse=$(samtools view -c -f 16 /mnt/openscience/audits/bio-alignment-validation/run/data/idx/real_human_PE.bam)
echo "Forward: $forward"
echo "Reverse: $reverse"
ratio=$(echo "scale=4; $forward / $reverse" | bc)
echo "F/R ratio: $ratio"
