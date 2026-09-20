#!/bin/bash
# INPUT 2 (variant A): "Sort by read name and run the duplicate-marking workflow; then extract paired FASTQ.
#   Also I need to know whether `sort -n` is a strict lexicographic order like the table says."
# Real data: derived/planted_dups.bam (real reads, 50 planted pairs -> 100 dup reads; Picard=50 pairs), human PE BAM.
source /mnt/openscience/audits/bio-alignment-sorting/run/common.sh
W=$WORK/in2; rm -rf $W; mkdir -p $W; cd $W
PL=$PD/derived/planted_dups.bam
ndup() { samtools view -c -f 1024 "$1"; }
echo "planted: records=$(nrec $PL) dup-flagged-in-input=$(ndup $PL) SO=$(so $PL)"

echo "### 2.1 SKILL 'Re-sort by Name for Duplicate Marking' (4 commands, verbatim)"
samtools sort -n -o namesorted.bam $PL
samtools fixmate -m namesorted.bam fixmate.bam
samtools sort -o sorted.bam fixmate.bam
samtools markdup -s sorted.bam marked.bam 2> markdup_stats.txt; cat markdup_stats.txt | head -12
eq "SKILL workflow: duplicate reads flagged" "$(ndup marked.bam)" "100"
eq "final @HD SO" "$(so marked.bam | grep -o 'SO:[a-z]*')" "SO:coordinate"
samtools index marked.bam && check "marked.bam indexes" test -s marked.bam.bai
eq "namesorted.bam @HD" "$(so namesorted.bam | grep -o 'SO:[a-z]*')" "SO:queryname"
echo "-- Picard 3.5.0 ground truth on the SAME input:"
picard MarkDuplicates -I $PL -O picard_marked.bam -M picard_metrics.txt --VALIDATION_STRINGENCY SILENT > picard.log 2>&1
grep -a -A1 '^LIBRARY' picard_metrics.txt | cut -f1-9 | head -3
eq "Picard flags same number of reads" "$(ndup picard_marked.bam)" "100"
# same set of duplicate-marked NAMES? (Picard and samtools may pick different mate of the tie; compare name sets)
samtools view -f 1024 marked.bam | cut -f1 | sort -u > s_dupnames.txt
samtools view -f 1024 picard_marked.bam | cut -f1 | sort -u > p_dupnames.txt
echo "  unique dup-flagged QNAMEs: samtools=$(wc -l < s_dupnames.txt) picard=$(wc -l < p_dupnames.txt) common=$(comm -12 s_dupnames.txt p_dupnames.txt | wc -l)"

echo "### 2.2 SKILL collate -> fixmate -> sort -> markdup pipeline (verbatim, lines 98-101)"
samtools collate -O -u $PL tmp_prefix | \
    samtools fixmate -m -u - - | \
    samtools sort -u - | \
    samtools markdup - out.bam
eq "collate pipeline: duplicate reads flagged" "$(ndup out.bam)" "100"
eq "collate pipeline final SO" "$(so out.bam | grep -o 'SO:[a-z]*')" "SO:coordinate"

echo "### 2.3 usage-guide piped workflow (verbatim, with -@)"
samtools sort -n -@ 4 $PL | \
    samtools fixmate -m -@ 4 - - | \
    samtools sort -@ 4 - | \
    samtools markdup -@ 4 - final.bam
eq "usage-guide pipeline duplicates" "$(ndup final.bam)" "100"
samtools index final.bam && check "final.bam indexed" test -s final.bam.bai

echo "### 2.4 Prerequisite ground truth: skip name/collate step (coordinate input straight into fixmate -m)"
samtools fixmate -m $PL nofix.bam 2> nofix.err; head -3 nofix.err
samtools sort -o nofix.sorted.bam nofix.bam; samtools markdup nofix.sorted.bam nofix.marked.bam 2> nofix.markdup.err; head -3 nofix.markdup.err
grep -q 'Coordinate sorted, require grouped/sorted by queryname' nofix.err && echo "  [PASS] fixmate -m on coordinate-sorted input REFUSES loudly (SKILL table 'name (or collate)' is a real prerequisite); no output produced" || echo "  [FAIL] fixmate did not refuse"
test -s nofix.bam && echo "  [FAIL] nofix.bam was written" || echo "  [PASS] no partial nofix.bam"
echo "### 2.5 Real human PE BAM: samtools workflow vs Picard (natural dup rate, informational)"
H=$PD/human/test.paired_end.sorted.bam
samtools sort -n -o h_n.bam $H && samtools fixmate -m h_n.bam h_f.bam && samtools sort -o h_s.bam h_f.bam && samtools markdup h_s.bam h_m.bam
picard MarkDuplicates -I $H -O h_pic.bam -M h_pic.txt --VALIDATION_STRINGENCY SILENT > h_pic.log 2>&1
echo "  samtools dup-flagged: $(ndup h_m.bam)   Picard dup-flagged: $(ndup h_pic.bam)   input already flagged: $(ndup $H)"

echo "### 2.6 sort -n vs -N vs Picard queryname on names read1..read1000 (synthetic, mixed digit widths)"
S=$DATA/synth_multi.unsorted.bam
samtools sort -n -o n_nat.bam $S; samtools sort -N -o n_asc.bam $S
picard SortSam -I $S -O n_pic.bam -SORT_ORDER queryname > pic_sort.log 2>&1
for f in n_nat n_asc n_pic; do echo "-- $f: $(so $f.bam)"; python $RUN/order_check.py $f.bam | grep n=; done
samtools view n_nat.bam | cut -f1 | uniq | head -14 | tr '\n' ' '; echo "   <- sort -n first 14 names"
samtools view n_asc.bam | cut -f1 | uniq | head -14 | tr '\n' ' '; echo "   <- sort -N first 14 names"
samtools view n_pic.bam | cut -f1 | uniq | head -14 | tr '\n' ' '; echo "   <- Picard queryname first 14 names"
samtools view n_nat.bam | cut -f1 > nat.names; samtools view n_asc.bam | cut -f1 > asc.names; samtools view n_pic.bam | cut -f1 > pic.names
cmp -s nat.names asc.names && echo "  [FAIL] -n order == -N order" || echo "  [PASS] -n order differs from -N (ASCII) order => sort -n is NOT lexicographic in samtools 1.24 (SKILL table says it is)"
cmp -s asc.names pic.names && echo "  [PASS] -N order == Picard queryname order (name column)" || echo "  [INFO] -N differs from Picard order"
cmp -s nat.names pic.names && echo "  [INFO] -n order == Picard" || echo "  [PASS] -n differs from Picard queryname order"
echo "-- Picard ValidateSamFile on the samtools -n output (does a Picard step accept it?):"
picard ValidateSamFile -I n_nat.bam --MODE SUMMARY > val_nat.txt 2>&1; grep -a -v '^\[' val_nat.txt | tail -6
picard ValidateSamFile -I n_asc.bam --MODE SUMMARY > val_asc.txt 2>&1; echo "-- ...and -N output:"; grep -a -v '^\[' val_asc.txt | tail -4

echo "### 2.7 Real human name.sorted.bam (from nf-core): which order?"
python $RUN/order_check.py $PD/human/test.paired_end.name.sorted.bam | grep -a -E 'HD|n='

echo "### 2.8 collate properties (SKILL: mates adjacent; between-mate order undefined; -o form in Quick Reference)"
samtools collate -O $PL tmp2 > collated.bam
echo "  collated @HD: $(so collated.bam)"
# every QNAME contiguous?
samtools view collated.bam | cut -f1 | uniq | sort | uniq -d | wc -l | { read n; eq "QNAMEs appearing in >1 non-contiguous block" "$n" "0"; }
eq "collate preserves record multiset" "$(recmd5 collated.bam)" "$(recmd5 $PL)"
echo "-- Quick Reference form: samtools collate -o out.bam in.bam (no prefix)"
samtools collate -o qr_out.bam $PL; echo "rc=$?"; ls qr_out.bam && eq "qr_out.bam records" "$(nrec qr_out.bam)" "500"
ls | grep -a -c 'tmp' | { read n; echo "  temp files left behind matching tmp*: $n"; }

echo "### 2.9 collate -> fastq (SKILL, verbatim, with -n) and usage-guide variant (no -n)"
samtools collate -O -u $PL tmp_prefix | samtools fastq -1 R1.fq.gz -2 R2.fq.gz -0 /dev/null -s /dev/null -n - 2> fq.log; tail -2 fq.log
r1=$(zcat R1.fq.gz | awk 'NR%4==1' | wc -l); r2=$(zcat R2.fq.gz | awk 'NR%4==1' | wc -l)
eq "R1 reads == 250 pairs" "$r1" "250"; eq "R2 reads == 250 pairs" "$r2" "250"
zcat R1.fq.gz | awk 'NR%4==1' | tr -d '@' | sed 's#/[12]$##' > r1.names; zcat R2.fq.gz | awk 'NR%4==1' | tr -d '@' | sed 's#/[12]$##' > r2.names
cmp -s r1.names r2.names && echo "  [PASS] R1/R2 names pair in identical order" || echo "  [FAIL] R1/R2 names misordered"
echo "  R1 first header (with -n): $(zcat R1.fq.gz | head -1)"
samtools collate -u -O $PL /tmp/collate | samtools fastq -1 R1b.fq -2 R2b.fq -0 /dev/null -s /dev/null - 2> fqb.log; tail -1 fqb.log
echo "  R1 first header (usage-guide, no -n): $(head -1 R1b.fq)   R1 reads=$(awk 'NR%4==1' R1b.fq | wc -l)"
summary
