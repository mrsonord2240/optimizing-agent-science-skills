for chr in chr1 chr2 chr3; do
    fwd=$(samtools view -c -F 16 /mnt/openscience/audits/bio-alignment-validation/run/data/idx/real_1000g_chr20.bam $chr)
    rev=$(samtools view -c -f 16 /mnt/openscience/audits/bio-alignment-validation/run/data/idx/real_1000g_chr20.bam $chr)
    echo "$chr: F=$fwd R=$rev ratio=$(echo "scale=2; $fwd/$rev" | bc)"
done
