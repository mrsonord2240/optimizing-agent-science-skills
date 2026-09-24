#!/bin/bash
# INPUT 3 (edge, REGRESSION of first audit input 3 against the fixed SKILL): "Sort by cell barcode; my BAM may be mislabelled,
#   truncated or have no @HD; how do I verify the sort order for real; tiny memory so it spills."  Synthetic + real.
source /mnt/openscience/audits/bio-alignment-sorting/run/common.sh
W=$WORK/in3; rm -rf $W; mkdir -p $W; cd $W
S=$DATA/synth_multi.unsorted.bam   # SYNTHETIC: 3 contigs, CB tags, unmapped pairs, cross-contig pair
python $RUN/extract_block.py "### Check Sort Order in pysam" python skillfns.py

echo "### 3.1 SKILL: samtools sort -t CB (10x barcode)  [synthetic]"
samtools sort -t CB -o cb.bam $S; echo "rc=$?"
echo "  header: $(so cb.bam)"
eq "SKILL table header for -t" "$(so cb.bam | cut -f3-4)" $'SO:unsorted\tSS:unsorted:CB:coordinate'
cat > cbcheck.py <<'EOP'
import pysam, sys
with pysam.AlignmentFile(sys.argv[1],'rb') as f:
    rs=list(f.fetch(until_eof=True))
def tag(r):
    return r.get_tag('CB') if r.has_tag('CB') else None
seq=[tag(r) for r in rs]
tagged=[t for t in seq if t is not None]
print("tag values non-decreasing (ASCII) among tagged:", tagged==sorted(tagged), "| untagged reads:", seq.count(None))
ok=True; prev=None
for r in rs:
    k=(tag(r) or '', r.reference_id if r.reference_id>=0 else 1<<30, r.reference_start)
    if prev and k[0]==prev[0] and k[1:]<prev[1:]: ok=False
    prev=k
print("position is secondary key within each CB block:", ok)
assert tagged==sorted(tagged) and ok
print("n =", len(rs))
EOP
python cbcheck.py cb.bam
eq "-t CB preserves records" "$(recmd5 cb.bam)" "$(recmd5 $S)"
echo "-- SKILL: 'output cannot be indexed' / '-n, -N and -t output fail samtools index (hts_idx_push errors)' / Common Errors row"
samtools sort -n -o idx_nat.bam $S; samtools sort -N -o idx_asc.bam $S
for f in cb.bam idx_nat.bam idx_asc.bam; do
  samtools index $f 2> ie_$f.txt; rc=$?; echo "  index $f rc=$rc msg: $(head -1 ie_$f.txt)"
  [ $rc -ne 0 ] && echo "  [PASS] $f fails to index" || echo "  [FAIL] $f indexed"
done
echo "  Common Errors row cites: 'NO_COOR reads not in a single block' / 'cannot be indexed':"
grep -a -l 'NO_COOR reads not in a single block' ie_*.txt | tr '\n' ' '; echo "<- files whose index error contains the NO_COOR string"
grep -a -l 'cannot be indexed' ie_*.txt | tr '\n' ' '; echo "<- files whose index error contains 'cannot be indexed'"
samtools sort -t RX -o rx.bam $PD/human/test.paired_end.umi_unsorted.bam; echo "-t RX on real UMI BAM rc=$? header: $(so rx.bam)"
samtools view rx.bam | awk '{for(i=12;i<=NF;i++) if($i ~ /^RX:Z:/){print substr($i,6)}}' > rx.vals
sort -c rx.vals && echo "  [PASS] RX values non-decreasing (ASCII) in -t RX output on REAL data ($(wc -l < rx.vals) tagged of $(nrec rx.bam))" || echo "  [FAIL] RX not sorted"

echo "### 3.2 Mislabelled BAM: header says SO:coordinate but records are shuffled - SKILL 'Check Sort Order' verbatim"
python - <<'EOP'
import pysam
src='/mnt/openscience/audits/bio-alignment-sorting/run/data/shuffled_real.bam'
with pysam.AlignmentFile(src,'rb') as i:
    hd=i.header.to_dict(); rs=list(i)
hd['HD']={'VN':'1.6','SO':'coordinate'}
with pysam.AlignmentFile('liar.bam','wb',header=pysam.AlignmentHeader.from_dict(hd)) as o:
    for r in rs: o.write(r)
EOP
echo "  liar @HD: $(so liar.bam)"
samtools index liar.bam /tmp/check_liar.bai 2> lie.err && echo "  [FAIL] indexable" || echo "  [PASS] SKILL 'samtools index' record test rejects the liar: $(head -1 lie.err)"
samtools quickcheck -v liar.bam; echo "  quickcheck(liar) rc=$? (SKILL does not claim quickcheck detects order; it detects truncation)"
cat > liar_test.py <<'EOP'
from skillfns import is_coordinate_sorted, ensure_coordinate_sorted
import pysam
print("is_coordinate_sorted(liar.bam):", is_coordinate_sorted('liar.bam'))
r = ensure_coordinate_sorted('liar.bam','liar_fixed.bam')
print("ensure_coordinate_sorted(liar.bam) returned:", r, "| sorted now:", is_coordinate_sorted(r))
assert r == 'liar_fixed.bam' and is_coordinate_sorted(r) and not is_coordinate_sorted('liar.bam')
print("PASS")
EOP
python liar_test.py
samtools index liar_fixed.bam && echo "  [PASS] liar_fixed.bam indexes"

echo "-- Contig-order violation (correct POS within contigs, chr2 records before chr1; header SO:coordinate). SKILL: 'samtools index accepts contigs in a different order ... walk the records with pysam'"
python - <<'EOP'
import pysam
h=pysam.AlignmentHeader.from_dict({'HD':{'VN':'1.6','SO':'coordinate'},'SQ':[{'SN':'chr1','LN':5000},{'SN':'chr2','LN':5000}]})
def mk(n,tid,pos):
    a=pysam.AlignedSegment(h); a.query_name=n; a.flag=0; a.reference_id=tid; a.reference_start=pos
    a.mapping_quality=60; a.cigarstring='10M'; a.query_sequence='A'*10; a.query_qualities=pysam.qualitystring_to_array('I'*10); return a
rs=[mk('a',1,10),mk('b',1,20),mk('c',0,10),mk('d',0,20)]
with pysam.AlignmentFile('contigswap.bam','wb',header=h) as o:
    for r in rs: o.write(r)
EOP
samtools index contigswap.bam 2>&1 | head -1; echo "  samtools index on contigswap.bam: $( [ -s contigswap.bam.bai ] && echo 'WRITTEN (SKILL says index accepts this)' || echo FAILED)"
python -c "
from skillfns import is_coordinate_sorted
r=is_coordinate_sorted('contigswap.bam'); print('  is_coordinate_sorted(contigswap.bam) =', r); assert r is False; print('  [PASS] pysam check catches contig-order violation')"
python $RUN/order_check.py contigswap.bam | grep -a n=

echo "### 3.3 Failure modes (exit codes captured directly, not through a pipe)"
samtools sort -o o1.bam does_not_exist.bam 2> e1.txt; echo "  missing input rc=$? msg: $(head -1 e1.txt)"; test -s o1.bam && echo "  (o1.bam exists!)" || echo "  no output file created"
printf 'not a bam\n' > junk.bam; samtools sort -o o2.bam junk.bam 2> e2.txt; echo "  non-BAM input rc=$? msg: $(head -1 e2.txt)"
samtools view -H $PD/human/test.paired_end.sorted.bam | samtools view -b -o hdronly.bam -; samtools sort -o o3.bam hdronly.bam 2> e3.txt; echo "  header-only BAM rc=$? records_out=$(nrec o3.bam)"
samtools sort -o /no/such/dir/o4.bam $S 2> e4.txt; echo "  output dir missing rc=$? msg: $(head -1 e4.txt)"
sz=$(stat -c %s $DATA/shuffled_real.bam); head -c $((sz/2)) $DATA/shuffled_real.bam > trunc.bam
samtools quickcheck -v trunc.bam 2> qc.txt; qcrc=$?; echo "  quickcheck -v (trunc.bam) rc=$qcrc $(head -1 qc.txt)"
samtools sort -o o5.bam trunc.bam 2> e5.txt; rc5=$?; echo "  truncated input sort rc=$rc5 msg: $(tail -2 e5.txt | tr '\n' '|')"
[ "$rc5" != "0" ] && echo "  [PASS] truncated input -> sort exits non-zero rc=$rc5 (SKILL Common Errors 'truncated file' row)" || echo "  [FINDING] sort exit 0 on truncated"
echo "-- SKILL: 'After a long sort, catch truncated/empty output (rc 16 truncated, rc 4 zero-byte)'"
: > zero.bam; samtools quickcheck -v zero.bam; eq "quickcheck zero-byte rc" "$?" "4"
samtools quickcheck -v o5.bam 2>/dev/null; echo "  quickcheck on the truncated-sort leftover o5.bam rc=$? (exists=$( [ -e o5.bam ] && echo yes || echo no))"
head -c $(( $(stat -c %s sorted_ok.bam 2>/dev/null || echo 0) )) /dev/null
samtools sort -o good.bam $DATA/shuffled_real.bam; gsz=$(stat -c %s good.bam); head -c $((gsz-40)) good.bam > good_trunc.bam
samtools quickcheck -v good_trunc.bam; eq "quickcheck truncated-EOF-marker BAM rc" "$?" "16"
echo "-- 'interrupted sort' : kill a running sort"
python - <<'EOP'
import pysam
with pysam.AlignmentFile('/mnt/openscience/audits/bio-alignment-sorting/run/data/shuffled_1000g.bam','rb') as f:
    h=f.header; rs=list(f)
with pysam.AlignmentFile('big.bam','wb',header=h) as o:
    for k in range(40):
        for r in rs: o.write(r)
print('big.bam records', len(rs)*40)
EOP
timeout -s KILL 0.8 samtools sort -m 20M -T bigpfx -o killed.bam big.bam 2> ek.txt; echo "  sort killed mid-run rc=$?"
[ -e killed.bam ] && { samtools quickcheck -v killed.bam; echo "  quickcheck(killed.bam) rc=$? size=$(stat -c %s killed.bam)"; } || echo "  no killed.bam"
rm -f big.bam bigpfx*

echo "### 3.4 -m minimum and real spill (SKILL: -m >= 1M; -T PREFIX; results unchanged by spilling)"
mkdir -p tmpd
samtools sort -m 100K -T tmpd/pfx -o spill.bam $DATA/shuffled_real.bam 2> spill.err; echo "-m 100K rc=$? msg: $(head -1 spill.err)"
grep -a -q 'less than the minimum required (1M)' spill.err && echo "  [PASS] message text matches SKILL Common Errors row" || echo "  [FAIL] message differs"
python - <<'EOP'
import pysam
with pysam.AlignmentFile('/mnt/openscience/audits/bio-alignment-sorting/run/data/shuffled_1000g.bam','rb') as f:
    h=f.header; rs=list(f)
with pysam.AlignmentFile('big5.bam','wb',header=h) as o:
    for k in range(5):
        for r in rs: o.write(r)
print('big5.bam records', len(rs)*5)
EOP
samtools sort -T tmpd/pfx -o big5_mem.bam big5.bam
samtools sort -m 1M -T tmpd/pfx -o big5_spill.bam big5.bam 2> spill.err; echo "-m 1M rc=$? : $(grep -a merging spill.err | head -1)"
eq "spilled sort (-m 1M, temp files) == in-memory sort (records, order)" "$(samtools view big5_spill.bam | md5sum)" "$(samtools view big5_mem.bam | md5sum)"
eq "temp files cleaned up" "$(ls tmpd | wc -l)" "0"
rm -f big5.bam big5_mem.bam big5_spill.bam

echo "### 3.5 Determinism: -@ 0 / 4 / 8 give identical record streams"
for t in 0 4 8; do samtools sort -@ $t -o det$t.bam $S; done
eq "-@ 0 vs -@ 4" "$(samtools view det0.bam | md5sum)" "$(samtools view det4.bam | md5sum)"
eq "-@ 0 vs -@ 8" "$(samtools view det0.bam | md5sum)" "$(samtools view det8.bam | md5sum)"

echo "### 3.6 Unmapped reads: unmapped last; mate-placed unmapped read stays next to mate"
samtools sort -o synth.sorted.bam $S
python $RUN/order_check.py synth.sorted.bam | grep -a n=
eq "fully-unmapped reads (RNAME *) at end" "$(samtools view synth.sorted.bam | awk '$3=="*"' | wc -l)" "10"
python -c "
from skillfns import is_coordinate_sorted
print('  is_coordinate_sorted(synth.sorted.bam) =', is_coordinate_sorted('synth.sorted.bam')); assert is_coordinate_sorted('synth.sorted.bam')"

echo "### 3.7 template-coordinate (SKILL block + claim: without MC tags the sort stops with 'no MC tag. Please run samtools fixmate on file first.')"
# synthetic has NO MC tags; the real nf-core BAM may already carry MC
echo "  MC tags in synthetic: $(samtools view $S | grep -ac 'MC:Z:') ; in real shuffled_real.bam: $(samtools view $DATA/shuffled_real.bam | grep -ac 'MC:Z:')"
samtools sort --template-coordinate -o tc_nomc.bam $S 2> tc_nomc.err; echo "  synthetic without MC: rc=$? msg: $(head -1 tc_nomc.err)"
grep -a -q 'no MC tag. Please run samtools fixmate on file first.' tc_nomc.err && echo "  [PASS] exact SKILL message" || echo "  [FAIL] message"
samtools sort --template-coordinate -o tc_real.bam $DATA/shuffled_real.bam 2> tc_real.err; echo "  real BAM (has MC): rc=$? header: $(so tc_real.bam) msg: $(head -1 tc_real.err)"
echo "-- SKILL block verbatim: fixmate -m namesorted.bam fixmate.bam ; sort --template-coordinate -o tc.bam fixmate.bam"
samtools sort -n -o namesorted.bam $S
samtools fixmate -m namesorted.bam fixmate.bam
samtools sort --template-coordinate -o tc.bam fixmate.bam; echo "  rc=$? header: $(so tc.bam)"
eq "SKILL header for template-coordinate" "$(so tc.bam | cut -f3-5)" $'SO:unsorted\tSS:unsorted:template-coordinate\tGO:query'
eq "records preserved" "$(recmd5 tc.bam)" "$(recmd5 fixmate.bam)"
samtools index tc.bam 2>&1 | head -1; echo "  [info] index on template-coordinate output rc=${PIPESTATUS[0]}"
summary
