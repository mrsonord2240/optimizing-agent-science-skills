# Genome-wide mean and breadth: -aa puts every reference position in the denominator.
# For a region use `samtools depth -a -r chr1:1000-2000 /mnt/openscience/audits/bio-bam-statistics/run/data/planted_depth.bam` in the same pipe.
samtools depth -a /mnt/openscience/audits/bio-bam-statistics/run/data/planted_depth.bam | awk '
    {s += $3; n++; if ($3 >= 10) c10++; if ($3 >= 20) c20++}
    END {if (!n) {print "no positions (empty BAM or no @SQ)" > "/dev/stderr"; exit 1}
         printf "mean %.2fx  >=10x %.2f%%  >=20x %.2f%%\n", s/n, c10/n*100, c20/n*100}'
