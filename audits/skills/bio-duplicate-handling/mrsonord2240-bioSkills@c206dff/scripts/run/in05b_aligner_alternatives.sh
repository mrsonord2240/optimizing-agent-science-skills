#!/bin/bash
# Input 5 (part b): SKILL.md 'Alternative: From Aligner' (bwa-mem2|samblaster|samtools sort), Picard command, tool-table names.
# Data: nf-core sarscov2 test_1/test_2.fastq.gz (100 real read pairs) + 20 SYNTHETIC clones (renamed copies of pairs 1-20) -> truth: 20 dup pairs
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
source /mnt/openscience/audits/bio-duplicate-handling/run/common.sh
P=/mnt/openscience/audit-envs/alignment-files/public-data/sarscov2
cd $W; rm -rf in05b; mkdir in05b; cd in05b
cp $P/genome.fasta ref.fa
python - <<PY
import gzip
for n in (1, 2):
    recs = []
    with gzip.open("$P/test_%d.fastq.gz" % n, "rt") as f:
        lines = f.read().splitlines()
    recs = [lines[i:i+4] for i in range(0, len(lines), 4)]
    out = open("R%d.fq" % n, "w")
    for r in recs: out.write("\n".join(r) + "\n")
    for i, r in enumerate(recs[:20]):          # SYNTHETIC clones -> exact PCR-duplicate pairs
        h = r[0].split()[0] + f"_clone{i}"
        out.write("\n".join([h, r[1], r[2], r[3]]) + "\n")
print("wrote R1.fq/R2.fq: 100 real pairs + 20 synthetic clone pairs")
PY
bwa-mem2 index ref.fa >/dev/null 2>&1; echo "index files: $(ls ref.fa.* | wc -l)"
echo "### SKILL.md 'BWA-MEM2 with samblaster' verbatim (ref.fa R1.fq R2.fq)"
bwa-mem2 mem ref.fa R1.fq R2.fq 2>/dev/null | \
    samblaster 2>samblaster.log | \
    samtools sort -o marked.bam
echo "exit codes ${PIPESTATUS[*]}"; tail -2 samblaster.log | head -1
echo "[check] records $(samtools view -c marked.bam); flagged $(samtools view -c -f 1024 marked.bam) (truth: 40 reads = 20 pairs, if all clones align properly)"
samtools flagstat marked.bam | grep -E 'in total|duplicates|properly'
echo "[check] flagged read names all clones? $(samtools view -f 1024 marked.bam | cut -f1 | grep -c clone) of $(samtools view -c -f 1024 marked.bam)"
echo "### cross-check: samtools pipeline on the same alignments (no samblaster)"
bwa-mem2 mem ref.fa R1.fq R2.fq 2>/dev/null | samtools sort -o plain.bam
samtools sort -n -o p_ns.bam plain.bam; samtools fixmate -m p_ns.bam p_fm.bam; samtools sort -o p_cs.bam p_fm.bam; samtools markdup p_cs.bam p_m.bam
echo "  samtools markdup flagged $(samtools view -c -f 1024 p_m.bam)"
picard MarkDuplicates I=plain.bam O=p_pic.bam M=p_pic.txt >/dev/null 2>&1; echo "  picard flagged $(samtools view -c -f 1024 p_pic.bam)"
echo "### SKILL.md Picard command (java -jar picard.jar ...) -> the equivalent picard wrapper with the same key=value args, OPTICAL_DUPLICATE_PIXEL_DISTANCE=2500"
picard MarkDuplicates I=plain.bam O=pk.bam M=pk.txt OPTICAL_DUPLICATE_PIXEL_DISTANCE=2500 2>&1 | grep -ciE 'exception|error' | sed 's/^/  error lines: /'; echo "  flagged $(samtools view -c -f 1024 pk.bam)"
echo "### class names in tool table exist in Picard 3.5.0"
picard UmiAwareMarkDuplicatesWithMateCigar --help 2>&1 | head -3
which pbmarkdup bammarkduplicates2 2>&1 | head -2; echo "(pbmarkdup / biobambam2 not installed in env: table rows for those are NOT executed)"
