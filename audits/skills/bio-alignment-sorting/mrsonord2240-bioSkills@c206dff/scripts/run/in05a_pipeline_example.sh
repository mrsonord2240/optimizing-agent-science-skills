#!/bin/bash
# INPUT 5a (stress, part 1): run the shipped examples/sort_pipeline.sh from a CLEAN COPY of the Skill, paired + single-end,
# with a missing index, missing FASTQ, and truncated FASTQ; plus the SKILL's Python subprocess streaming pattern.
# Data: real 100-pair SARS-CoV-2 FASTQ + genome.fasta (nf-core).  No pysam/pipefail assumptions.
source /mnt/openscience/audits/bio-alignment-sorting/run/common.sh
W=$WORK/in5a; rm -rf $W; mkdir -p $W; cd $W
cp -r /mnt/openscience/external/mrsonord2240__bioSkills/alignment-files/alignment-sorting ./skillcopy   # READ-ONLY source, copy lives in run/work
find skillcopy -type f | sort
cp $PD/sarscov2/genome.fasta ref.fa; cp $PD/sarscov2/test_1.fastq.gz r1.fq.gz; cp $PD/sarscov2/test_2.fastq.gz r2.fq.gz
S=skillcopy/examples/sort_pipeline.sh
ls -l $S | cut -c1-10
bash -n $S && echo "  [PASS] script parses (bash -n)"

echo "### 5a.1 usage message (no args)"
bash $S > usage.out 2>&1; echo "rc=$?"; cat usage.out

echo "### 5a.2 clean copy, reference NOT bwa-indexed (script never indexes; docs never say to)"
bash $S ref.fa r1.fq.gz noidx.bam r2.fq.gz 2 > noidx.out 2> noidx.err; rc=$?
echo "rc=$rc"; head -3 noidx.err; echo "  stdout: $(tr '\n' '|' < noidx.out | cut -c1-200)"
[ $rc -ne 0 ] && echo "  [PASS] fails non-zero when the index is missing" || echo "  [FAIL] exit 0 with missing index"
test -e noidx.bam && echo "  leftover noidx.bam: $(nrec noidx.bam 2>&1 | head -1)" || echo "  no noidx.bam left"

echo "### 5a.3 index reference (bwa index), then PAIRED run (threads=2)"
bwa index ref.fa > bwaidx.log 2>&1; ls ref.fa.*
bash $S ref.fa r1.fq.gz pe.bam r2.fq.gz 2 > pe.out 2> pe.err; rc=$?
echo "rc=$rc"; cat pe.out
check "pe.bam and index exist" test -s pe.bam -a -s pe.bam.bai
eq "PE @HD SO" "$(so pe.bam | grep -o 'SO:[a-z]*')" "SO:coordinate"
python $RUN/order_check.py pe.bam | grep -a n=
eq "PE record count (100 pairs)" "$(nrec pe.bam)" "200"
# independent truth: same alignment without the script
bwa mem -t 2 ref.fa r1.fq.gz r2.fq.gz 2>/dev/null | samtools view -c - | { read n; eq "records equal raw bwa output count" "$(nrec pe.bam)" "$n"; }
eq "flagstat mapped" "$(samtools flagstat pe.bam | awk '/ mapped \(/ && !/primary/{print $1}')" "200"

echo "### 5a.4 SINGLE-end run (R2 omitted)"
bash $S ref.fa r1.fq.gz se.bam > se.out 2> se.err; rc=$?; echo "rc=$rc"; cat se.out | head -6
eq "SE record count (100 reads)" "$(nrec se.bam)" "100"
eq "SE @HD SO" "$(so se.bam | grep -o 'SO:[a-z]*')" "SO:coordinate"

echo "### 5a.5 THREADS arg vs hard-coded 'samtools sort -@ 4'"
grep -n 'sort -@' $S
echo "  (bwa -t \$THREADS is user-controlled; sort -@ 4 is fixed regardless of the 5th argument)"

echo "### 5a.6 FAILURE MASKING: missing R1 FASTQ (no set -o pipefail; only the LAST pipeline stage's status is seen)"
bash $S ref.fa /nonexistent_R1.fq.gz missing.bam > miss.out 2> miss.err; rc=$?
echo "rc=$rc"; head -3 miss.err; echo "  stdout: $(tr '\n' '|' < miss.out | cut -c1-260)"
test -e missing.bam && echo "  missing.bam exists, records=$(nrec missing.bam)" || echo "  no missing.bam"
[ $rc -eq 0 ] && echo "  [FINDING] script exited 0 (\"Done\") although alignment failed" || echo "  [PASS] script exited $rc on missing FASTQ"

echo "### 5a.7 FAILURE MASKING: truncated gzip FASTQ (real data cut in half)"
sz=$(stat -c %s r1.fq.gz); head -c $((sz/2)) r1.fq.gz > r1_trunc.fq.gz
bash $S ref.fa r1_trunc.fq.gz trunc.bam > tr.out 2> tr.err; rc=$?
echo "rc=$rc"; tail -3 tr.err; echo "  records in trunc.bam: $(nrec trunc.bam 2>/dev/null) (input FASTQ had 100 reads)"
echo "  [INFO] bwa itself returns 0 on a gz cut mid-stream (bwa/zlib behaviour), so pipefail would not change this; the example does no read-count check"


echo "### 5a.7b SIMULATED aligner crash mid-stream (PATH shim: real bwa output cut after 60 lines, then exit 3) -- does the example notice? (no pipefail)"
mkdir -p shim; REALBWA=$(which bwa)
printf '#!/bin/bash
%s "$@" | head -n 60
exit 3
' "$REALBWA" > shim/bwa; chmod +x shim/bwa
PATH=$PWD/shim:$PATH bash $S ref.fa r1.fq.gz crash.bam > crash.out 2> crash.err; rc=$?
echo "  script rc=$rc ; stdout: $(grep -a -c Done crash.out) 'Done' line(s) ; records in crash.bam: $(nrec crash.bam 2>/dev/null) (input has 100 reads)"
if [ $rc -eq 0 ]; then echo "  [FINDING] aligner exited 3 but the example exited 0, printed Done and left a truncated BAM (set -e without pipefail only sees the last stage)"; else echo "  [PASS] script propagated the failure rc=$rc"; fi
echo "  same pipeline with 'set -o pipefail' added:"
sed 's/^set -e$/set -eo pipefail/' $S > shim/sort_pipefail.sh
PATH=$PWD/shim:$PATH bash shim/sort_pipefail.sh ref.fa r1.fq.gz crash2.bam > crash2.out 2> crash2.err; echo "  rc=$? (expect non-zero)"

echo "### 5a.8 SKILL python streaming pattern (subprocess shell=True check=True) - same failure mode?"
cat > pystream.py <<'EOF'
import subprocess
ok = subprocess.run('bwa mem ref.fa r1.fq.gz | samtools sort -o py_ok.bam', shell=True, check=True)
print('good input: returncode', ok.returncode)
try:
    subprocess.run('bwa mem ref.fa /nonexistent_R1.fq.gz | samtools sort -o py_bad.bam', shell=True, check=True)
    print('bad input: NO EXCEPTION raised by check=True')
except subprocess.CalledProcessError as e:
    print('bad input: CalledProcessError rc', e.returncode)
EOF
python pystream.py 2> pystream.err; tail -2 pystream.err
echo "  py_bad.bam records: $(nrec py_bad.bam 2>/dev/null)"
summary
