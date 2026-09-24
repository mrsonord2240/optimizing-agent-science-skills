#!/bin/bash
# INPUT 5a (stress, part 1, REGRESSION of first audit 5a against the REWRITTEN example): run examples/sort_pipeline.sh from a
# CLEAN COPY of the fixed Skill, paired + single-end, missing index, missing FASTQ, truncated FASTQ, bwa dying mid-stream;
# plus the SKILL's Python subprocess streaming pattern. Data: real 100-pair SARS-CoV-2 FASTQ + genome.fasta (nf-core).
source /mnt/openscience/audits/bio-alignment-sorting/run/common.sh
W=$WORK/in5a; rm -rf $W; mkdir -p $W; cd $W
cp -r $RUN/skill ./skillcopy      # run/skill is itself a copy of the worktree (never the worktree or external clone)
find skillcopy -type f | sort
cp $PD/sarscov2/genome.fasta ref.fa; cp $PD/sarscov2/test_1.fastq.gz r1.fq.gz; cp $PD/sarscov2/test_2.fastq.gz r2.fq.gz
S=skillcopy/examples/sort_pipeline.sh
ls -l $S | cut -c1-10
bash -n $S && echo "  [PASS] script parses (bash -n)"

echo "### 5a.1 usage message (no args)"
bash $S > usage.out 2>&1; rc=$?; echo "rc=$rc"; cat usage.out
eq "no-args rc" "$rc" "1"

echo "### 5a.2 clean copy, reference NOT bwa-indexed: script must say 'bwa index' (SKILL: prerequisite)"
bash $S ref.fa r1.fq.gz noidx.bam r2.fq.gz 2 > noidx.out 2> noidx.err; rc=$?
echo "rc=$rc"; head -3 noidx.err; echo "  stdout: $(tr '\n' '|' < noidx.out | cut -c1-200)"
[ $rc -ne 0 ] && echo "  [PASS] fails non-zero when the index is missing" || echo "  [FAIL] exit 0 with missing index"
grep -q 'bwa index' noidx.err && echo "  [PASS] error names the remedy (bwa index)" || echo "  [FAIL] no remedy in message"
test -e noidx.bam && echo "  [FAIL] leftover noidx.bam" || echo "  [PASS] no noidx.bam left (fails before aligning)"

echo "### 5a.3 index reference (bwa index), then PAIRED run (threads=2)  -> VALID run must exit 0"
bwa index ref.fa > bwaidx.log 2>&1; ls ref.fa.*
bash $S ref.fa r1.fq.gz pe.bam r2.fq.gz 2 > pe.out 2> pe.err; rc=$?
echo "rc=$rc"; cat pe.out
eq "VALID paired run exits 0" "$rc" "0"
check "pe.bam and index exist" test -s pe.bam -a -s pe.bam.bai
eq "PE @HD SO" "$(so pe.bam | grep -o 'SO:[a-z]*')" "SO:coordinate"
python $RUN/order_check.py pe.bam | grep -a n=
eq "PE record count (100 pairs)" "$(nrec pe.bam)" "200"
bwa mem -t 2 ref.fa r1.fq.gz r2.fq.gz 2>/dev/null | samtools view -c - | { read n; eq "records equal raw bwa output count" "$(nrec pe.bam)" "$n"; }
eq "flagstat primary" "$(samtools flagstat pe.bam | awk '/ primary$/{print $1}')" "200"
grep -a -c 'ERROR' pe.err | { read n; eq "no ERROR on stderr of a valid run" "$n" "0"; }

echo "### 5a.4 SINGLE-end run (R2 omitted) -> exit 0"
bash $S ref.fa r1.fq.gz se.bam > se.out 2> se.err; rc=$?; echo "rc=$rc"; head -4 se.out
eq "VALID single-end run exits 0" "$rc" "0"
eq "SE record count (100 reads)" "$(nrec se.bam)" "100"
eq "SE @HD SO" "$(so se.bam | grep -o 'SO:[a-z]*')" "SO:coordinate"

echo "### 5a.5 THREADS arg vs hard-coded 'samtools sort -@ 4'"
grep -n 'sort -@' $S

echo "### 5a.6 missing R1 FASTQ / missing R2 / missing ref"
bash $S ref.fa /nonexistent_R1.fq.gz missing.bam > miss.out 2> miss.err; rc=$?
echo "  missing R1: rc=$rc msg: $(head -1 miss.err)"; eq "missing R1 rc" "$rc" "1"; test -e missing.bam && echo "  [FAIL] missing.bam created" || echo "  [PASS] no output BAM created"
bash $S ref.fa r1.fq.gz missing2.bam /nonexistent_R2.fq.gz > miss2.out 2> miss2.err; rc=$?
echo "  missing R2: rc=$rc msg: $(head -1 miss2.err)"; eq "missing R2 rc" "$rc" "1"
bash $S /nonexistent_ref.fa r1.fq.gz missing3.bam > miss3.out 2> miss3.err; rc=$?
echo "  missing ref: rc=$rc msg: $(head -1 miss3.err)"; eq "missing ref rc" "$rc" "1"

echo "### 5a.7 truncated gzip FASTQ (real data cut in half): read-count check"
sz=$(stat -c %s r1.fq.gz); head -c $((sz/2)) r1.fq.gz > r1_trunc.fq.gz
bash $S ref.fa r1_trunc.fq.gz trunc.bam > tr.out 2> tr.err; rc=$?
echo "rc=$rc"; tail -3 tr.err; echo "  records in trunc.bam: $(nrec trunc.bam 2>/dev/null)"
echo "  gzip -t: $(gzip -t r1_trunc.fq.gz 2>&1 | head -1)"
[ $rc -ne 0 ] && echo "  [PASS] truncated FASTQ -> non-zero rc=$rc" || echo "  [FINDING] truncated FASTQ exits 0"

echo "### 5a.8 SIMULATED aligner crash mid-stream (PATH shim: real bwa output cut after 60 lines, then exit 3)"
mkdir -p shim; REALBWA=$(which bwa)
printf '#!/bin/bash\n%s "$@" | head -n 60\nexit 3\n' "$REALBWA" > shim/bwa; chmod +x shim/bwa
PATH=$PWD/shim:$PATH bash $S ref.fa r1.fq.gz crash.bam > crash.out 2> crash.err; rc=$?
echo "  script rc=$rc ; 'Done' lines: $(grep -a -c '^Done' crash.out) ; records in crash.bam: $(nrec crash.bam 2>/dev/null)"
eq "bwa exits 3 mid-stream -> script exits 3" "$rc" "3"
grep -a -q '^Done' crash.out && echo "  [FAIL] printed Done" || echo "  [PASS] did not print Done"
echo "-- shim that exits 0 after truncating the stream (aligner dies quietly; only the read-count check can catch it)"
printf '#!/bin/bash\n%s "$@" | head -n 60\nexit 0\n' "$REALBWA" > shim/bwa
PATH=$PWD/shim:$PATH bash $S ref.fa r1.fq.gz quiet.bam > quiet.out 2> quiet.err; rc=$?
echo "  script rc=$rc msg: $(tail -1 quiet.err)"; eq "quiet truncation caught by read-count check (rc 1)" "$rc" "1"
echo "  leftover quiet.bam records: $(nrec quiet.bam 2>/dev/null) (partial BAM left on disk after failure; index present: $( [ -e quiet.bam.bai ] && echo yes || echo no))"
echo "-- shim that dies before printing anything"
printf '#!/bin/bash\nexit 7\n' > shim/bwa
PATH=$PWD/shim:$PATH bash $S ref.fa r1.fq.gz dead.bam > dead.out 2> dead.err; rc=$?
echo "  script rc=$rc msg: $(head -2 dead.err | tr '\n' '|')"; [ $rc -ne 0 ] && echo "  [PASS] bwa dies at start -> script non-zero (rc=$rc: rightmost failing stage, samtools sort: no header)" || echo "  [FAIL] exit 0 when bwa died at start"

echo "### 5a.9 SKILL Python streaming snippet, extracted verbatim from '### Stream Sort from Aligner'"
python $RUN/extract_block.py "### Stream Sort from Aligner" python stream_snip.py
cat > pystream.py <<'EOP'
import subprocess, re, sys
src = open('stream_snip.py', encoding='utf-8').read()
ok_src  = src.replace('bwa mem ref.fa reads.fq | samtools sort -o aligned.bam', 'bwa mem ref.fa r1.fq.gz | samtools sort -o py_ok.bam')
bad_src = src.replace('bwa mem ref.fa reads.fq | samtools sort -o aligned.bam', 'bwa mem ref.fa /nonexistent_R1.fq.gz | samtools sort -o py_bad.bam')
assert ok_src != src and bad_src != src
exec(ok_src); print('good input: completed without exception')
try:
    exec(bad_src); print('bad input: NO EXCEPTION raised')
except subprocess.CalledProcessError as e:
    print('bad input: CalledProcessError rc', e.returncode)
EOP
python pystream.py 2> pystream.err; tail -2 pystream.err
echo "-- shim bwa exit 3 mid-stream through the SKILL snippet (the case the old shell=True form hid):"
printf '#!/bin/bash\n%s "$@" | head -n 60\nexit 3\n' "$REALBWA" > shim/bwa
sed 's#bwa mem ref.fa reads.fq | samtools sort -o aligned.bam#bwa mem ref.fa r1.fq.gz | samtools sort -o py_shim.bam#' stream_snip.py > stream_shim.py
PATH=$PWD/shim:$PATH python stream_shim.py 2>/dev/null && echo "  [FAIL] no exception on crashed aligner" || echo "  [PASS] snippet raised (rc!=0) on aligner crash"
summary
