samtools idxstats /mnt/openscience/audit-envs/alignment-files/public-data/1000g/HG00349.chr20_1400000-1500000.bam | /usr/bin/mawk '$2>0 && $3>0 && $1 ~ /^(chr)?[0-9]+$/ {print $1, $3/$2}' \
  | sort -k2,2g \
  | /usr/bin/mawk '{c[NR]=$1; v[NR]=$2} END {
      if (NR==0) { print "no autosomes with reads" > "/dev/stderr"; exit 1 }
      med = v[int(NR/2)+1]
      for (i=1; i<=NR; i++) printf "%s\t%.3f\n", c[i], v[i]/med }'
