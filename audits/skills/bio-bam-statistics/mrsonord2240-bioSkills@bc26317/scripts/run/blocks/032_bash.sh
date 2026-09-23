   samtools view -F 2308 input.bam | awk -F'\t' '
       {n++; c = $6
        while (match(c, /^[0-9]+[MIDNSHP=X]/)) {
            len = substr(c, 1, RLENGTH-1) + 0; op = substr(c, RLENGTH, 1); c = substr(c, RLENGTH+1)
            if (op ~ /[MIS=X]/) q += len; if (op == "S") s += len}}
       END {if (!n || !q) {print "no primary mapped reads: nothing to compute" > "/dev/stderr"; exit 1}
            printf "soft-clipped bases: %d of %d (%.2f%%)\n", s, q, s/q*100}'
