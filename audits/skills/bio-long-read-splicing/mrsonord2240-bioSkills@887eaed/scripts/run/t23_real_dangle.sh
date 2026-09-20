#!/bin/bash
# NEW input 9: the SKILL's ONT recipe on REAL reads at several --junc-bonus values. Counts (a) alignments with an intron next to a soft clip (SKILL awk, verbatim),
# (b) junction observations on annotated introns, (c) whether `flair correct` survives and how many reads it keeps. Real cDNA: LRGASP WTC-11 (FLAIR test set, 1883 reads).
# Real direct RNA: SG-NEx A549 (bambu extdata BAM -> reads via samtools fastq, chr9:1-1e6).
R=/mnt/openscience/audits/bio-long-read-splicing/run; P=/mnt/openscience/audit-envs/alternative-splicing/public-data/longread
O=$R/out/real_dangle; rm -rf $O; mkdir -p $O; cd $O; export PYTHONDONTWRITEBYTECODE=1
cp $P/flair_test/genome.fa cdna_ref.fa; cp $P/flair_test/input/basic.annotation.gtf cdna.gtf; gzip -c $P/flair_test/input/basic.reads.fa > cdna.fa.gz
gffread cdna.gtf --bed -o cdna.bed12
B=$P/bambu_extdata
cp $B/Homo_sapiens.GRCh38.dna_sm.primary_assembly_chr9_1_1000000.fa drna_ref.fa; cp $B/Homo_sapiens.GRCh38.91_chr9_1_1000000.gtf drna.gtf
samtools fastq -F 2308 $B/SGNex_A549_directRNA_replicate5_run1_chr9_1_1000000.bam 2>/dev/null | gzip > drna.fq.gz
gffread drna.gtf --bed -o drna.bed12
echo "cdna reads: $(zcat cdna.fa.gz | grep -c '>')  drna reads: $(zcat drna.fq.gz | awk 'NR%4==1' | wc -l)"
cat > annot_frac.py <<'PY'
import sys, pysam
# fraction of intron observations (N ops, primary) that match an annotated intron of the BED12
bed, bam = sys.argv[1:3]
ann = set()
for ln in open(bed):
    f = ln.split("\t"); s = int(f[1]); sz = list(map(int, f[10].strip(",").split(","))); st = list(map(int, f[11].strip(",").split(",")))
    for i in range(len(sz) - 1): ann.add((f[0], s + st[i] + sz[i], s + st[i + 1]))
tot = hit = 0
for r in pysam.AlignmentFile(bam).fetch(until_eof=True):
    if r.is_unmapped or r.is_secondary or r.is_supplementary: continue
    pos = r.reference_start
    for op, n in r.cigartuples:
        if op == 3: tot += 1; hit += (r.reference_name, pos, pos + n) in ann; pos += n
        elif op in (0, 2, 7, 8): pos += n
print("%d/%d = %.1f%%" % (hit, tot, 100.0 * hit / tot))
PY
run() { # tag ref reads bed preset bonus
  minimap2 -ax $5 --secondary=no --junc-bed $4 ${6:+--junc-bonus $6} -t 8 $2 $3 2>/dev/null | samtools sort -o $1.bam - 2>/dev/null; samtools index $1.bam
  d=$(samtools view -F 2308 $1.bam | awk '$6 ~ /N[0-9]+S$/ || $6 ~ /^[0-9]+S[0-9]+N/' | wc -l)
  echo "$1: spliced primary $(samtools view -F 2308 -c $1.bam) ; dangling(intron next to soft clip) $d ; annotated-intron observations $(asenv as-lr python annot_frac.py $4 $1.bam)"
}
for b in "" 12 14 15 16 17 18 20; do run cdna_b${b:-default} cdna_ref.fa cdna.fa.gz cdna.bed12 "splice -k14" $b; done
for b in "" 16 17 18 20; do run drna_b${b:-default} drna_ref.fa drna.fq.gz drna.bed12 "splice -uf -k14" $b; done
echo "--- flair correct (BED12 from the alignment; -f annotation; the SKILL's block without junction_tab) on real cDNA at each bonus"
for b in default 15 16 17 18 20; do
  bedtools bamtobed -bed12 -i cdna_b$b.bam > cdna_b$b.bed
  flair correct -q cdna_b$b.bed -f cdna.gtf -o fc_cdna_$b -t 8 > fc_cdna_$b.log 2>&1; rc=$?
  echo "flair correct cdna bonus $b: rc=$rc corrected $(wc -l < fc_cdna_${b}_all_corrected.bed 2>/dev/null) inconsistent $(wc -l < fc_cdna_${b}_all_inconsistent.bed 2>/dev/null) ; $(grep -a -m1 -E 'Error|Traceback' fc_cdna_$b.log)"
done
for b in default 16 17 18 20; do
  bedtools bamtobed -bed12 -i drna_b$b.bam > drna_b$b.bed
  flair correct -q drna_b$b.bed -f drna.gtf -o fc_drna_$b -t 8 > fc_drna_$b.log 2>&1; rc=$?
  echo "flair correct drna bonus $b: rc=$rc corrected $(wc -l < fc_drna_${b}_all_corrected.bed 2>/dev/null) inconsistent $(wc -l < fc_drna_${b}_all_inconsistent.bed 2>/dev/null) ; $(grep -a -m1 -E 'Error|Traceback' fc_drna_$b.log)"
done
