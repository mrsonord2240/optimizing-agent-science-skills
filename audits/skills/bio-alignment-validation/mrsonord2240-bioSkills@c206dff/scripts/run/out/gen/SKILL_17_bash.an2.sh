samtools idxstats /mnt/openscience/audits/bio-alignment-validation/run/data/idx/real_human_PE.bam | awk '$2>0 && $1!~/^chr[XYM]|^GL|^KI|^chrUn|^chrEBV/ {
    cov[$1] = $3 / $2
}
END {
    n = asort(cov, sorted)
    med = sorted[int(n/2)+1]
    for (c in cov) printf "%s\t%.3f\n", c, cov[c]/med
}'
