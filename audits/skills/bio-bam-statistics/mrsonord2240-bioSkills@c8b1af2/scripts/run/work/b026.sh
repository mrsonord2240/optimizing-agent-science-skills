while read -r chrom start end _; do
    case $chrom in ''|'#'*|track*|browser*) continue;; esac   # skip BED header lines
    samtools coverage -H -r "$chrom:$((start+1))-$end" /mnt/openscience/audits/bio-bam-statistics/run/data/planted_depth.bam
done < /mnt/openscience/audits/bio-bam-statistics/run/data/planted_depth.regions.bed
