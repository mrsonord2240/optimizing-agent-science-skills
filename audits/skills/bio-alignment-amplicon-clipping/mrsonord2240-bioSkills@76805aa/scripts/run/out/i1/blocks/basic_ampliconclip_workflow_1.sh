# 0. BAM header and BED must share a contig name (ARTIC BEDs: MN908947.3; nf-core/viralrecon
#    Illumina BAMs: MT192765.1 -- they do not pair). Empty output = mismatch, stop.
comm -12 <(samtools view -H input.bam | awk -F'\t' '$1=="@SQ"{sub("SN:","",$2); print $2}' | sort) \
         <(awk '!/^#/{print $1}' primers.bed | sort -u)

# 1. Soft-clip primers (reversible). -f keeps the stats; "TOTAL CLIPPED: 0" means BED and BAM do not match.
samtools ampliconclip --both-ends --strand --soft-clip -f clip.stats \
    -b primers.bed input.bam -o clipped.bam
cat clip.stats

# 2. Re-sort and re-pair (CIGARs changed -- mate info needs refresh)
samtools sort -n clipped.bam | \
    samtools fixmate -m - - | \
    samtools sort -o sorted.bam -

# 3. Restore MD/NM (clipped reads lose them). Do NOT hide stderr: with a wrong reference calmd prints
#    "fail to find sequence", exits 0 and writes no MD.
samtools calmd -b sorted.bam reference.fa > clipped_final.bam
samtools index clipped_final.bam

# 4. Verify: every mapped read has MD, and no read still begins/ends inside a primer
samtools view -c -F 4 clipped_final.bam
samtools view clipped_final.bam | awk 'index($0, "\tMD:Z:"){n++} END{print n+0}'
python examples/check_primer_residual.py clipped_final.bam primers.bed --three-prime   # exit 1 if any remain
