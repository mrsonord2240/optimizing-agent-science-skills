forward=$(samtools view -c -F 2324 /mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.sorted.bam)          # mapped, primary, forward
reverse=$(samtools view -c -f 16 -F 2308 /mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.sorted.bam)    # mapped, primary, reverse
echo "Forward: $forward"
echo "Reverse: $reverse"
awk -v f="$forward" -v r="$reverse" 'BEGIN{if (f+r) printf "Forward fraction: %.3f\n", f/(f+r)}'
