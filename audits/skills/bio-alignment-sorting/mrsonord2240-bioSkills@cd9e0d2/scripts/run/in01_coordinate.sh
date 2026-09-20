#!/bin/bash
# INPUT 1 (canonical, REGRESSION of first audit input 1 + new SKILL text):
# "My aligner output is unsorted. Coordinate-sort it, confirm the sort order, index it. 8 threads, fixed memory, CRAM too."
# Real data: shuffled copies of real nf-core BAMs + the real UMI BAM that has no @HD.
source /mnt/openscience/audits/bio-alignment-sorting/run/common.sh
W=$WORK/in1; rm -rf $W; mkdir -p $W; cd $W
echo "### 1.1 inputs"
so $DATA/shuffled_real.bam; nrec $DATA/shuffled_real.bam
echo "umi_unsorted @HD lines: $(samtools view -H $PD/human/test.paired_end.umi_unsorted.bam | grep -ac '^@HD')"

echo "### 1.2 SKILL: samtools sort -o sorted.bam input.bam  (REAL data, shuffled)"
samtools sort -o sorted.bam $DATA/shuffled_real.bam
eq "@HD says SO:coordinate" "$(so sorted.bam)" $'@HD\tVN:1.6\tSO:coordinate'
python $RUN/order_check.py sorted.bam | tee oc_sorted.txt
grep -q 'coordinate_sorted=True' oc_sorted.txt && echo "  [PASS] independent pysam check: coordinate order" || echo "  [FAIL] independent order"
eq "record multiset preserved vs input" "$(recmd5 sorted.bam)" "$(recmd5 $DATA/shuffled_real.bam)"
eq "record multiset == original coord-sorted BAM" "$(recmd5 sorted.bam)" "$(recmd5 $PD/human/test.paired_end.sorted.bam)"
samtools view sorted.bam | cut -f3,4 > a.txt; samtools view $PD/human/test.paired_end.sorted.bam | cut -f3,4 > b.txt
cmp -s a.txt b.txt && echo "  [PASS] (contig,pos) sequence identical to original sorted BAM" || echo "  [FAIL] (contig,pos) differs"

echo "### 1.3 SKILL: sort --write-index (NEW text: 'writes sorted.bam.csi, not .bai') and sort then index"
samtools sort --write-index -o wi.bam $DATA/shuffled_real.bam; echo "rc=$?"; ls wi.bam*
check "wi.bam.csi exists" test -s wi.bam.csi
check "wi.bam.bai NOT written (SKILL: csi not bai)" test ! -e wi.bam.bai
eq "idxstats via csi: chr22 mapped" "$(samtools idxstats wi.bam | awk '$1=="chr22"{print $3}')" "5642"
samtools sort -o out.bam $DATA/shuffled_real.bam && samtools index out.bam
check "out.bam.bai exists" test -s out.bam.bai
eq "idxstats chr22 mapped" "$(samtools idxstats out.bam | awk '$1=="chr22"{print $3}')" "5642"
eq "idxstats unmapped placed (*)" "$(samtools idxstats out.bam | awk '$1=="*"{print $4}')" "2"

echo "### 1.4 SKILL flags: -@ 8 -m 4G -T -l -O bam; results must equal default sort"
samtools sort -@ 8 -m 4G -o t8.bam $DATA/shuffled_real.bam
eq "-@ 8 -m 4G same records" "$(samtools view t8.bam | md5sum)" "$(samtools view sorted.bam | md5sum)"
samtools sort -T /tmp/sort_tmp -o tT.bam $DATA/shuffled_real.bam
eq "-T /tmp/sort_tmp (nonexistent dir as PREFIX) works, same records" "$(samtools view tT.bam | md5sum)" "$(samtools view sorted.bam | md5sum)"
samtools sort -l 1 -o l1.bam $DATA/shuffled_real.bam
samtools sort -O bam -o Obam.bam $DATA/shuffled_real.bam
eq "-l 1 same records" "$(samtools view l1.bam | md5sum)" "$(samtools view sorted.bam | md5sum)"
eq "-O bam same records" "$(samtools view Obam.bam | md5sum)" "$(samtools view sorted.bam | md5sum)"

echo "### 1.5 SKILL: CRAM output  samtools sort -O cram --reference ref.fa -o sorted.cram input.bam"
samtools sort -O cram --reference $PD/human/genome.fasta -o sorted.cram $DATA/shuffled_real.bam; echo "rc=$?"
ls -la sorted.cram
eq "CRAM record count" "$(samtools view -c -T $PD/human/genome.fasta sorted.cram)" "5644"
eq "CRAM @HD" "$(samtools view -H -T $PD/human/genome.fasta sorted.cram | grep -a '^@HD' | head -1)" $'@HD\tVN:1.6\tSO:coordinate'
samtools index sorted.cram && check "CRAM index made" test -s sorted.cram.crai

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

echo "### 1.8 SKILL 'Check Sort Order' text, executed as written (NEW)"
echo "-- header hint:"; samtools view -H sorted.bam | grep "^@HD"
echo "-- 'Verify Records' block verbatim (samtools index input.bam /tmp/check.bai && echo indexable) on sorted / shuffled / umi_unsorted:"
for f in sorted.bam $DATA/shuffled_real.bam $PD/human/test.paired_end.umi_unsorted.bam; do
  rm -f /tmp/check.bai
  if samtools index $f /tmp/check.bai 2>/tmp/idx.err && echo "indexable" >/dev/null; then echo "  $(basename $f): indexable (bai size $(stat -c %s /tmp/check.bai))"; else echo "  $(basename $f): NOT indexable: $(head -1 /tmp/idx.err)"; fi
done
samtools quickcheck -v sorted.bam; eq "quickcheck sorted.bam rc" "$?" "0"
samtools quickcheck -v $DATA/shuffled_real.bam; eq "quickcheck shuffled (well-formed but unsorted) rc: does NOT flag order" "$?" "0"

echo "### 1.9 SKILL pysam.sort == CLI ; SKILL pysam is_coordinate_sorted / ensure_coordinate_sorted (verbatim extraction)"
python $RUN/extract_block.py "### Check Sort Order in pysam" python skillfns.py
cat > pysort.py <<'EOP'
import pysam, hashlib
from skillfns import is_coordinate_sorted, ensure_coordinate_sorted
D='/mnt/openscience/audits/bio-alignment-sorting/run/data/'
pysam.sort('-o', 'py_sorted.bam', D+'shuffled_real.bam')
pysam.sort('-@', '4', '-m', '2G', '-T', '/tmp/sortpfx', '-o', 'py_sorted2.bam', D+'shuffled_real.bam')
def recs(p):
    with pysam.AlignmentFile(p,'rb') as f:
        return [r.to_string() for r in f.fetch(until_eof=True)]
a, b, c = recs('py_sorted.bam'), recs('py_sorted2.bam'), recs('sorted.bam')
print("pysam.sort == CLI:", a == c, "| pysam.sort(-@ -m -T) == CLI:", b == c, "| n=", len(a)); assert a == c and b == c
print("is_coordinate_sorted: sorted.bam", is_coordinate_sorted('sorted.bam'), "| shuffled", is_coordinate_sorted(D+'shuffled_real.bam'))
assert is_coordinate_sorted('sorted.bam') and not is_coordinate_sorted(D+'shuffled_real.bam')
r = ensure_coordinate_sorted(D+'shuffled_real.bam', 'ens.bam'); print('ensure(shuffled) ->', r)
assert r == 'ens.bam' and is_coordinate_sorted('ens.bam')
r2 = ensure_coordinate_sorted('sorted.bam', 'never.bam'); print('ensure(sorted) ->', r2); assert r2 == 'sorted.bam'
# the SKILL's stated point: a mislabelled SO:coordinate BAM must be re-sorted
with pysam.AlignmentFile(D+'shuffled_real.bam','rb') as i:
    hd=i.header.to_dict(); rs=list(i)
hd['HD']={'VN':'1.6','SO':'coordinate'}
with pysam.AlignmentFile('liar.bam','wb',header=pysam.AlignmentHeader.from_dict(hd)) as o:
    for x in rs: o.write(x)
r3 = ensure_coordinate_sorted('liar.bam','liar_fixed.bam'); print('ensure(liar) ->', r3)
assert r3 == 'liar_fixed.bam' and is_coordinate_sorted('liar_fixed.bam')
print("PASS: all pysam assertions")
EOP
python pysort.py
samtools index liar_fixed.bam && echo "  [PASS] liar_fixed.bam indexes"; samtools idxstats liar_fixed.bam | head -2
for f in sorted.bam s1000.bam umi_sorted.bam; do python -c "
from skillfns import is_coordinate_sorted; print('  is_coordinate_sorted($f) =', is_coordinate_sorted('$f'))"; done
summary
