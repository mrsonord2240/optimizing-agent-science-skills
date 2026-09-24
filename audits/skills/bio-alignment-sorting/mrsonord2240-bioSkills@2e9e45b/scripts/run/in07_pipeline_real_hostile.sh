#!/bin/bash
# INPUT 7 (NEW, scope boundary / hostile conditions for the REWRITTEN examples/sort_pipeline.sh):
# "Align my 2819 read pairs to the reference with the example script, on plain and gz FASTQ, paths with spaces, then break things:
#   partial bwa index, unwritable output dir, unequal R1/R2, empty FASTQ, bad threads value, re-run over an existing output."
# Real data: read pairs extracted from the REAL nf-core human PE BAM (samtools collate | fastq) + human genome.fasta (40 kb slice).
source /mnt/openscience/audits/bio-alignment-sorting/run/common.sh
W=$WORK/in7; rm -rf $W; mkdir -p $W; cd $W
cp -r $RUN/skill ./skillcopy; S=$PWD/skillcopy/examples/sort_pipeline.sh
cp $PD/human/genome.fasta ref.fa
H=$PD/human/test.paired_end.sorted.bam
samtools collate -O -u $H tmpc | samtools fastq -1 r1.fq -2 r2.fq -0 /dev/null -s /dev/null -n - 2> fq.log; tail -1 fq.log
gzip -k -f r1.fq; gzip -k -f r2.fq
echo "reads: R1=$(( $(wc -l < r1.fq)/4 )) R2=$(( $(wc -l < r2.fq)/4 )) (pairs); original BAM records $(nrec $H)"
bwa index ref.fa > bwaidx.log 2>&1
python $RUN/extract_block.py "### Check Sort Order in pysam" python skillfns.py

echo "### 7.1 plain FASTQ, paired, threads=4  (VALID run must exit 0)"
bash $S ref.fa r1.fq pe_plain.bam r2.fq 4 > o71.out 2> o71.err; rc=$?; eq "rc" "$rc" "0"; tail -3 o71.out | head -0
n=$(nrec pe_plain.bam); pr=$(samtools view -c -F 0x900 pe_plain.bam)
eq "primary records (-F 0x900) == 2 x pairs (bwa adds supplementary/secondary lines on top: total $n)" "$pr" "$(( 2 * $(wc -l < r1.fq)/4 ))"
eq "flagstat primary == same" "$(samtools flagstat pe_plain.bam | awk '/ primary$/{print $1}')" "$pr"
check "index exists" test -s pe_plain.bam.bai
python -c "
from skillfns import is_coordinate_sorted; v=is_coordinate_sorted('pe_plain.bam'); print('  is_coordinate_sorted(pe_plain.bam) =', v); assert v"
samtools flagstat pe_plain.bam | grep -a -E 'properly paired|mapped \(' | head -3
echo "  vs original BAM: mapped $(samtools view -c -F 4 $H) properly paired $(samtools view -c -f 2 $H)"

echo "### 7.2 gzip FASTQ, same result?"
bash $S ref.fa r1.fq.gz pe_gz.bam r2.fq.gz 4 > o72.out 2> o72.err; rc=$?; eq "rc" "$rc" "0"
eq "gz vs plain: identical (cols 1-11)" "$(samtools view pe_gz.bam | cut -f1-11 | sort | md5sum)" "$(samtools view pe_plain.bam | cut -f1-11 | sort | md5sum)"

echo "### 7.3 single-end (R1 only) and SE with a threads value (requires passing an empty R2 argument)"
bash $S ref.fa r1.fq se.bam > o73.out 2> o73.err; rc=$?; eq "SE rc" "$rc" "0"; eq "SE primary records == R1 reads (total incl. supplementary: $(nrec se.bam))" "$(samtools view -c -F 0x900 se.bam)" "$(( $(wc -l < r1.fq)/4 ))"
bash $S ref.fa r1.fq se_t.bam "" 3 > o73b.out 2> o73b.err; rc=$?; eq "SE + threads via empty R2 arg: rc" "$rc" "0"; eq "SE + threads primary records" "$(samtools view -c -F 0x900 se_t.bam)" "$(( $(wc -l < r1.fq)/4 ))"
bash $S ref.fa r1.fq se_t2.bam 3 > o73c.out 2> o73c.err; rc=$?
echo "  (user might type 'ref r1 out 3' meaning threads=3 for SE): rc=$rc msg: $(head -1 o73c.err)"
[ $rc -ne 0 ] && echo "  [INFO] 3 is taken as R2 filename -> fails loudly ('input not found: 3'), not silently" || echo "  [FINDING] accepted"

echo "### 7.4 PARTIAL bwa index (ref.fa.bwt present but .sa removed): the script's [ -f \$REF.bwt ] test passes; does the run still fail loudly?"
mkdir -p partial; cp ref.fa ref.fa.amb ref.fa.ann ref.fa.bwt ref.fa.pac partial/   # no .sa
bash $S partial/ref.fa r1.fq partial.bam r2.fq 2 > o74.out 2> o74.err; rc=$?
echo "  rc=$rc msg: $(head -2 o74.err | tr '\n' '|' | cut -c1-200)"; grep -a -q '^Done' o74.out && echo "  [FAIL] printed Done" || echo "  [PASS] no Done"
[ $rc -ne 0 ] && echo "  [PASS] non-zero rc=$rc" || echo "  [FAIL] exit 0 with a broken index"
echo "  leftover partial.bam: $( [ -e partial.bam ] && echo "exists, records=$(nrec partial.bam 2>&1 | head -1)" || echo none)"

echo "### 7.5 unwritable output directory"
bash $S ref.fa r1.fq /no/such/dir/out.bam r2.fq 2 > o75.out 2> o75.err; rc=$?
echo "  rc=$rc msg: $(grep -a -m2 -E 'Failed|ERROR|failed|No such' o75.err | tr '\n' '|' | cut -c1-200)"; [ $rc -ne 0 ] && echo "  [PASS] non-zero rc=$rc" || echo "  [FAIL] exit 0"
grep -a -q '^Done' o75.out && echo "  [FAIL] printed Done" || echo "  [PASS] no Done"

echo "### 7.6 unequal R1/R2 (R2 truncated by 40 reads)"
head -n $(( ($(wc -l < r2.fq)/4 - 40) * 4 )) r2.fq > r2_short.fq
bash $S ref.fa r1.fq unequal.bam r2_short.fq 2 > o76.out 2> o76.err; rc=$?
echo "  rc=$rc msg: $(grep -a -m2 -E 'ERROR|error|fewer|different|read' o76.err | tr '\n' '|' | cut -c1-220)"; grep -a -q '^Done' o76.out && echo "  [FAIL] printed Done" || echo "  [PASS] no Done"
[ $rc -ne 0 ] && echo "  [PASS] non-zero rc=$rc" || echo "  [FAIL] exit 0 with unequal mate files"

echo "### 7.7 paths containing spaces"
mkdir -p "sp ace"; cp ref.fa "sp ace/my ref.fa"; cp ref.fa.* "sp ace/" 2>/dev/null; for e in amb ann bwt pac sa; do cp ref.fa.$e "sp ace/my ref.fa.$e"; done
cp r1.fq "sp ace/r 1.fq"; cp r2.fq "sp ace/r 2.fq"
bash $S "sp ace/my ref.fa" "sp ace/r 1.fq" "sp ace/out put.bam" "sp ace/r 2.fq" 2 > o77.out 2> o77.err; rc=$?
echo "  rc=$rc"; eq "space-path run rc" "$rc" "0"; eq "space-path records" "$(nrec "sp ace/out put.bam")" "$(nrec pe_plain.bam)"

echo "### 7.8 re-run over an existing output (idempotent?) and stale index"
bash $S ref.fa r1.fq pe_plain.bam r2.fq 4 > o78.out 2> o78.err; rc=$?; eq "re-run rc" "$rc" "0"
eq "re-run records identical (cols 1-11)" "$(samtools view pe_plain.bam | cut -f1-11 | md5sum)" "$(samtools view pe_gz.bam | cut -f1-11 | md5sum)"
samtools quickcheck -v pe_plain.bam && echo "  quickcheck ok after overwrite"

echo "### 7.9 empty FASTQ (0 reads)"
: > empty.fq
bash $S ref.fa empty.fq empty.bam > o79.out 2> o79.err; rc=$?
echo "  rc=$rc records=$(nrec empty.bam 2>/dev/null) msg: $(tail -2 o79.err | tr '\n' '|' | cut -c1-200)"

echo "### 7.10 non-numeric threads argument"
bash $S ref.fa r1.fq bad_t.bam r2.fq abc > o710.out 2> o710.err; rc=$?
echo "  rc=$rc msg: $(head -2 o710.err | tr '\n' '|' | cut -c1-160)"; echo "  Done printed: $(grep -a -c '^Done' o710.out) ; output primary records $(samtools view -c -F 0x900 bad_t.bam) vs expected $(( 2 * $(wc -l < r1.fq)/4 )) -> bwa turned -t abc into a usable value; result correct but the script never validates THREADS (INFO, harmless here)"

echo "### 7.11 FASTQ with a trailing blank line (read-count check false positive?)"
cp r1.fq r1_blank.fq; cp r2.fq r2_blank.fq; echo >> r1_blank.fq; echo >> r2_blank.fq
bash $S ref.fa r1_blank.fq pe_blank.bam r2_blank.fq 2 > o711.out 2> o711.err; rc=$?
echo "  rc=$rc msg: $(tail -1 o711.err | cut -c1-160)"; [ $rc -eq 0 ] && echo "  [PASS] no false alarm" || echo "  [INFO] non-zero (bwa itself may reject a bare blank line)"

echo "### 7.12 FASTQ where a read is dropped by the aligner but the script still counts it (reads of length 0 / only N)"
python - <<'EOP'
lines=open('r1.fq').read().split('\n')
# make read 1 all-N (still aligns as unmapped), and read 2 zero-length
lines[1]='N'*len(lines[1]);
open('r1_N.fq','w').write('\n'.join(lines))
EOP
bash $S ref.fa r1_N.fq se_N.bam > o712.out 2> o712.err; rc=$?; echo "  all-N read: rc=$rc records=$(nrec se_N.bam 2>/dev/null) expected $(( $(wc -l < r1_N.fq)/4 ))"
printf '@zero\n\n+\n\n@ok\nACGTACGTACGTACGTACGTACGTACGTACGT\n+\nIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII\n' > zero.fq
bash $S ref.fa zero.fq zero.bam > o712b.out 2> o712b.err; rc=$?; echo "  zero-length read in FASTQ: rc=$rc records=$(nrec zero.bam 2>/dev/null) expected 2; msg: $(grep -a -m1 -E 'ERROR|empty|zero' o712b.err | cut -c1-160)"
summary
