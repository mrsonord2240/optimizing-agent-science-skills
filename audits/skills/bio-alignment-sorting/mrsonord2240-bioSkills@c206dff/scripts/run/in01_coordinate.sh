#!/bin/bash
# INPUT 1 (canonical): "My aligner output is unsorted. Coordinate-sort it, confirm the sort order, index it."
# Real data: shuffled copies of real nf-core BAMs + the real UMI BAM that has no @HD.
source /mnt/openscience/audits/bio-alignment-sorting/run/common.sh
W=$WORK/in1; rm -rf $W; mkdir -p $W; cd $W
echo "### 1.1 inputs"
so $DATA/shuffled_real.bam; nrec $DATA/shuffled_real.bam
echo "umi_unsorted @HD lines: $(samtools view -H $PD/human/test.paired_end.umi_unsorted.bam | grep -ac '^@HD')"

echo "### 1.2 SKILL: samtools sort -o sorted.bam input.bam  (REAL data, shuffled)"
samtools sort -o sorted.bam $DATA/shuffled_real.bam
eq "@HD says SO:coordinate" "$(so sorted.bam)" $'@HD	VN:1.6	SO:coordinate'
python $RUN/order_check.py sorted.bam | tee oc_sorted.txt
grep -q 'coordinate_sorted=True' oc_sorted.txt && echo "  [PASS] independent pysam check: coordinate order" || echo "  [FAIL] independent order"
eq "record multiset preserved vs input" "$(recmd5 sorted.bam)" "$(recmd5 $DATA/shuffled_real.bam)"
eq "record multiset == original coord-sorted BAM" "$(recmd5 sorted.bam)" "$(recmd5 $PD/human/test.paired_end.sorted.bam)"
# ordering vs original (ties may differ): compare first 4 cols of ordered stream
samtools view sorted.bam | cut -f3,4 > a.txt; samtools view $PD/human/test.paired_end.sorted.bam | cut -f3,4 > b.txt
cmp -s a.txt b.txt && echo "  [PASS] (contig,pos) sequence identical to original sorted BAM" || echo "  [FAIL] (contig,pos) differs"

echo "### 1.3 SKILL: sort + index (Quick Reference)"
samtools sort -o out.bam $DATA/shuffled_real.bam && samtools index out.bam
check "out.bam.bai exists" test -s out.bam.bai
eq "idxstats chr22 mapped" "$(samtools idxstats out.bam | awk '$1=="chr22"{print $3}')" "5642"
eq "idxstats unmapped placed (*)" "$(samtools idxstats out.bam | awk '$1=="*"{print $4}')" "2"

echo "### 1.4 SKILL flags: -@ 8 -m 4G -T -l -O bam; results must equal default sort"
samtools sort -@ 8 -m 4G -o t8.bam $DATA/shuffled_real.bam
eq "-@ 8 -m 4G same records" "$(samtools view t8.bam | md5sum)" "$(samtools view sorted.bam | md5sum)"
mkdir -p /tmp/sort_tmp_dir_test
samtools sort -T /tmp/sort_tmp -o tT.bam $DATA/shuffled_real.bam
eq "-T /tmp/sort_tmp (nonexistent dir as PREFIX) works, same records" "$(samtools view tT.bam | md5sum)" "$(samtools view sorted.bam | md5sum)"
samtools sort -T /tmp/sort_tmp_dir_test -o tT2.bam $DATA/shuffled_real.bam 2>&1 | head -3
echo "  (-T with an EXISTING DIRECTORY as value: rc=$? ; see next line for output)"; test -s tT2.bam && echo "  tT2.bam written, records=$(nrec tT2.bam)" || echo "  tT2.bam not written"
ls /tmp | grep -a 'sort_tmp' | head
samtools sort -l 1 -o l1.bam $DATA/shuffled_real.bam
samtools sort -O bam -o Obam.bam $DATA/shuffled_real.bam
eq "-l 1 same records" "$(samtools view l1.bam | md5sum)" "$(samtools view sorted.bam | md5sum)"
eq "-O bam same records" "$(samtools view Obam.bam | md5sum)" "$(samtools view sorted.bam | md5sum)"

echo "### 1.5 SKILL: CRAM output  samtools sort -O cram --reference ref.fa -o sorted.cram input.bam"
samtools sort -O cram --reference $PD/human/genome.fasta -o sorted.cram $DATA/shuffled_real.bam; echo "rc=$?"
ls -la sorted.cram
eq "CRAM record count" "$(samtools view -c -T $PD/human/genome.fasta sorted.cram)" "5644"
eq "CRAM @HD" "$(samtools view -H -T $PD/human/genome.fasta sorted.cram | grep -a '^@HD' | head -1)" $'@HD	VN:1.6	SO:coordinate'
samtools index sorted.cram && check "CRAM index made" test -s sorted.cram.crai
echo "-- CRAM without --reference on a sorted BAM with SQ M5: does it fail loudly?"
samtools sort -O cram -o noref.cram $DATA/shuffled_real.bam 2>&1 | head -3; ls -la noref.cram 2>&1 | head -1

echo "### 1.6 Real 1000G multi-contig BAM (full GRCh38 header with alts)"
samtools sort -o s1000.bam $DATA/shuffled_1000g.bam
python $RUN/order_check.py s1000.bam | tee oc_1000.txt
grep -q 'coordinate_sorted=True' oc_1000.txt && echo "  [PASS] 1000G coordinate order (tid,pos, unmapped last)" || echo "  [FAIL] 1000G order"
eq "1000G record multiset" "$(recmd5 s1000.bam)" "$(recmd5 $PD/1000g/HG00349.chr20_1400000-1500000.bam)"
samtools index s1000.bam && check "1000G index" test -s s1000.bam.bai

echo "### 1.7 Real UMI BAM: unsorted, NO @HD line"
samtools sort -o umi_sorted.bam $PD/human/test.paired_end.umi_unsorted.bam
so umi_sorted.bam
python $RUN/order_check.py umi_sorted.bam | tee oc_umi.txt
grep -q 'coordinate_sorted=True' oc_umi.txt && echo "  [PASS] umi sorted" || echo "  [FAIL] umi sorted"
samtools index umi_sorted.bam && echo "  [PASS] umi_sorted indexes" || echo "  [FAIL] cannot index"
echo "-- index on the raw no-@HD file (what happens if user skips sort):"
samtools index $PD/human/test.paired_end.umi_unsorted.bam /tmp/x.bai 2>&1 | head -2

echo "### 1.8 pysam.sort (SKILL) == CLI"
cat > pysort.py <<'EOF'
import pysam, hashlib
pysam.sort('-o', 'py_sorted.bam', '/mnt/openscience/audits/bio-alignment-sorting/run/data/shuffled_real.bam')
pysam.sort('-@', '4', '-m', '2G', '-T', '/tmp/sortpfx', '-o', 'py_sorted2.bam', '/mnt/openscience/audits/bio-alignment-sorting/run/data/shuffled_real.bam')
def recs(p):
    with pysam.AlignmentFile(p,'rb') as f:
        return [r.to_string() for r in f.fetch(until_eof=True)]
a, b, c = recs('py_sorted.bam'), recs('py_sorted2.bam'), recs('sorted.bam')
print("pysam.sort == CLI:", a == c, "| pysam.sort(-@ -m -T) == CLI:", b == c, "| n=", len(a))
assert a == c and b == c
with pysam.AlignmentFile('py_sorted.bam','rb') as bam:
    hd = bam.header.get('HD', {})
    print('Sort order:', hd.get('SO','unknown'))
EOF
python pysort.py
echo "### 1.9 usage-guide get_sort_order / ensure_coordinate_sorted (verbatim)"
cat > usage_guide_fns.py <<'EOF'
import pysam
def get_sort_order(bam_path):
    with pysam.AlignmentFile(bam_path, 'rb') as bam:
        hd = bam.header.get('HD', {})
        return hd.get('SO', 'unknown')
def ensure_coordinate_sorted(input_bam, output_bam):
    order = get_sort_order(input_bam)
    if order == 'coordinate':
        return input_bam
    pysam.sort('-o', output_bam, input_bam)
    return output_bam
D='/mnt/openscience/audits/bio-alignment-sorting/run/data/'
P='/mnt/openscience/audit-envs/alignment-files/public-data/human/'
print('umi_unsorted:', get_sort_order(P+'test.paired_end.umi_unsorted.bam'))
print('shuffled_real:', get_sort_order(D+'shuffled_real.bam'))
print('sorted.bam:', get_sort_order('sorted.bam'))
r = ensure_coordinate_sorted(D+'shuffled_real.bam', 'ens.bam'); print('ensure ->', r)
assert r == 'ens.bam' and get_sort_order('ens.bam') == 'coordinate'
r2 = ensure_coordinate_sorted('sorted.bam', 'never.bam'); print('ensure(sorted) ->', r2); assert r2 == 'sorted.bam'
EOF
python usage_guide_fns.py
summary
