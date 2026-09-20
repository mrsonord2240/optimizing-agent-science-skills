#!/bin/bash
# INPUT 3 (edge): "Sort by cell barcode; my BAM may be mislabelled, truncated or have no @HD; how do I verify the
#   sort order for real; sort with tiny memory so it spills."  Synthetic + real (umi BAM, 1000G).
source /mnt/openscience/audits/bio-alignment-sorting/run/common.sh
W=$WORK/in3; rm -rf $W; mkdir -p $W; cd $W
S=$DATA/synth_multi.unsorted.bam   # SYNTHETIC: 3 contigs, CB tags, unmapped pairs, cross-contig pair

echo "### 3.1 SKILL: samtools sort -t CB (10x barcode)  [synthetic, CB on all but 'half1' pair]"
samtools sort -t CB -o cb.bam $S; echo "rc=$?"
echo "  header: $(so cb.bam)"
cat > cbcheck.py <<'EOF'
import pysam, sys
with pysam.AlignmentFile(sys.argv[1],'rb') as f:
    rs=list(f.fetch(until_eof=True))
def tag(r):
    return r.get_tag('CB') if r.has_tag('CB') else None
seq=[tag(r) for r in rs]
# group order by CB value
seen=[];
for t in seq:
    if not seen or seen[-1]!=t: seen.append(t)
print("CB block sequence:", seen)
tagged=[t for t in seq if t is not None]
print("tag values non-decreasing (ASCII) among tagged:", tagged==sorted(tagged), "| untagged reads:", seq.count(None), "at positions", [i for i,t in enumerate(seq) if t is None][:6])
# position secondary sort within each CB block
ok=True; prev=None
for r in rs:
    k=(tag(r) or '', r.reference_id if r.reference_id>=0 else 1<<30, r.reference_start)
    if prev and k[0]==prev[0] and k[1:]<prev[1:]: ok=False
    prev=k
print("position is secondary key within each CB block:", ok)
assert tagged==sorted(tagged) and ok
print("n =", len(rs))
EOF
python cbcheck.py cb.bam
eq "-t CB preserves records" "$(recmd5 cb.bam)" "$(recmd5 $S)"
samtools index cb.bam 2>&1 | head -2; echo "  (index on tag-sorted output rc=${PIPESTATUS[0]})"
echo "-- on REAL UMI BAM (RX tag, dash-joined UMIs), which has no @HD"
samtools sort -t RX -o rx.bam $PD/human/test.paired_end.umi_unsorted.bam; echo "rc=$?"; echo "  header: $(so rx.bam)"
samtools view rx.bam | awk '{for(i=12;i<=NF;i++) if($i ~ /^RX:Z:/){print substr($i,6)}}' > rx.vals; wc -l < rx.vals | { read n; echo "  RX-tagged records: $n of $(nrec rx.bam)"; }
sort -c rx.vals && echo "  [PASS] RX values non-decreasing (ASCII) in -t RX output" || echo "  [FAIL] RX not sorted"
echo "-- -t CB -n (name secondary)"
samtools sort -t CB -n -o cbn.bam $S; echo "rc=$? header: $(so cbn.bam)"

echo "### 3.2 Mislabelled BAM: header says SO:coordinate but records are shuffled"
python - <<'EOF'
import pysam
src='/mnt/openscience/audits/bio-alignment-sorting/run/data/shuffled_real.bam'
with pysam.AlignmentFile(src,'rb') as i:
    hd=i.header.to_dict(); rs=list(i)
hd['HD']={'VN':'1.6','SO':'coordinate'}
with pysam.AlignmentFile('liar.bam','wb',header=pysam.AlignmentHeader.from_dict(hd)) as o:
    for r in rs: o.write(r)
EOF
echo "  liar @HD: $(so liar.bam)"
cp $RUN/skill/usage-guide.md ./ug.md
cat > liar_test.py <<'EOF'
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
r = ensure_coordinate_sorted('liar.bam','liar_fixed.bam')
print("ensure_coordinate_sorted(liar.bam) returned:", r, "(=> no re-sort; header trusted)")
EOF
python liar_test.py
samtools index liar.bam 2>&1 | head -2; echo "  samtools index on liar.bam: $( [ -s liar.bam.bai ] && echo 'index WRITTEN' || echo 'index FAILED')"
echo "-- SKILL awk verification snippet (verbatim) on: sorted / shuffled / liar"
samtools sort -o good.bam $DATA/shuffled_real.bam
awkchk() { samtools view "$1" | awk '$3!=c {c=$3; prev=0} $4<prev {exit 1} {prev=$4}'; echo $?; }
eq "awk snippet: truly sorted BAM -> 0" "$(awkchk good.bam)" "0"
eq "awk snippet: shuffled BAM -> 1" "$(awkchk $DATA/shuffled_real.bam)" "1"
eq "awk snippet: header-liar BAM -> 1 (catches what header check misses)" "$(awkchk liar.bam)" "1"
samtools sort -o g1000.bam $DATA/shuffled_1000g.bam
eq "awk snippet: multi-contig real 1000G sorted BAM -> 0 (no false 'unsorted')" "$(awkchk g1000.bam)" "0"
echo "-- awk snippet blind spot: correct POS within contigs but CONTIGS out of header order (chr2 records before chr1)"
python - <<'EOF'
import pysam
src='good.bam'
h=pysam.AlignmentHeader.from_dict({'HD':{'VN':'1.6','SO':'coordinate'},'SQ':[{'SN':'chr1','LN':5000},{'SN':'chr2','LN':5000}]})
def mk(n,tid,pos):
    a=pysam.AlignedSegment(h); a.query_name=n; a.flag=0; a.reference_id=tid; a.reference_start=pos
    a.mapping_quality=60; a.cigarstring='10M'; a.query_sequence='A'*10; a.query_qualities=pysam.qualitystring_to_array('I'*10); return a
rs=[mk('a',1,10),mk('b',1,20),mk('c',0,10),mk('d',0,20)]   # chr2 before chr1
with pysam.AlignmentFile('contigswap.bam','wb',header=h) as o:
    for r in rs: o.write(r)
EOF
eq "awk snippet on contig-order-violating BAM (false pass = 0)" "$(awkchk contigswap.bam)" "0"
samtools index contigswap.bam 2>&1 | head -1; echo "  samtools index on contigswap.bam: $( [ -s contigswap.bam.bai ] && echo WRITTEN || echo FAILED)"
python $RUN/order_check.py contigswap.bam | grep -a n=
echo "  ==> awk snippet reports 'sorted' (0) and samtools index still writes an index, but independent (tid,pos) check says coordinate_sorted=False: the snippet cannot see contig-order violations"

echo "### 3.3 Failure modes (exit codes captured directly, not through a pipe)"
samtools sort -o o1.bam does_not_exist.bam 2> e1.txt; echo "  missing input rc=$? msg: $(head -1 e1.txt)"; test -s o1.bam && echo "  (o1.bam exists!)" || echo "  no output file created"
printf 'not a bam\n' > junk.bam; samtools sort -o o2.bam junk.bam 2> e2.txt; echo "  non-BAM input rc=$? msg: $(head -1 e2.txt)"
samtools view -H $PD/human/test.paired_end.sorted.bam | samtools view -b -o hdronly.bam -; samtools sort -o o3.bam hdronly.bam 2> e3.txt; echo "  header-only BAM rc=$? records_out=$(nrec o3.bam) msg: $(head -1 e3.txt)"
samtools sort -o /no/such/dir/o4.bam $S 2> e4.txt; echo "  output dir missing rc=$? msg: $(head -1 e4.txt)"
# truncated input
sz=$(stat -c %s $DATA/shuffled_real.bam); head -c $((sz/2)) $DATA/shuffled_real.bam > trunc.bam
samtools quickcheck trunc.bam 2> qc.txt; echo "  quickcheck(trunc.bam) rc=$? $(head -1 qc.txt)"
samtools sort -o o5.bam trunc.bam 2> e5.txt; rc5=$?; echo "  truncated input sort rc=$rc5 msg: $(tail -2 e5.txt | tr '\n' '|')"
if [ -e o5.bam ]; then echo "  o5.bam written: records=$(nrec o5.bam 2>/dev/null) (input had 5644); quickcheck(o5.bam) rc=$(samtools quickcheck o5.bam; echo $?)"; fi
[ "$rc5" = "0" ] && echo "  [FINDING] truncated input: sort exit 0 (silent partial output)" || echo "  [PASS] truncated input -> sort exits non-zero rc=$rc5"
echo "-- 'interrupted sort' (SKILL Common Errors: truncated file): kill a running sort"
for i in $(seq 1 25); do cat $DATA/shuffled_1000g.bam; done > /dev/null   # warm cache only
python - <<'EOF'
import pysam
rs=[]
with pysam.AlignmentFile('/mnt/openscience/audits/bio-alignment-sorting/run/data/shuffled_1000g.bam','rb') as f:
    h=f.header; rs=list(f)
with pysam.AlignmentFile('big.bam','wb',header=h) as o:
    for k in range(40):
        for r in rs: o.write(r)
print('big.bam records', len(rs)*40)
EOF
timeout -s KILL 0.8 samtools sort -m 20M -T bigpfx -o killed.bam big.bam 2> ek.txt; echo "  sort killed mid-run rc=$?"
ls -la killed.bam 2>&1 | head -1; ls bigpfx* 2>/dev/null | head -3
[ -e killed.bam ] && { samtools quickcheck killed.bam; echo "  quickcheck(killed.bam) rc=$? (non-zero => detectably truncated)"; }
samtools quickcheck good.bam && echo "  quickcheck(good.bam) rc=0"
rm -f big.bam bigpfx*

echo "### 3.4 -m minimum and real spill (SKILL: -m per thread; -T prefix)"
mkdir -p tmpd
samtools sort -m 100K -T tmpd/pfx -o spill.bam $DATA/shuffled_real.bam 2> spill.err; echo "-m 100K rc=$? $(head -1 spill.err)"
[ -e spill.bam ] && echo "  spill.bam exists" || echo "  no output written for -m below 1M (SKILL never states the 1M floor)"
python - <<'EOF2'
import pysam
with pysam.AlignmentFile('/mnt/openscience/audits/bio-alignment-sorting/run/data/shuffled_1000g.bam','rb') as f:
    h=f.header; rs=list(f)
with pysam.AlignmentFile('big5.bam','wb',header=h) as o:
    for k in range(5):
        for r in rs: o.write(r)
print('big5.bam records', len(rs)*5)
EOF2
samtools sort -T tmpd/pfx -o big5_mem.bam big5.bam
samtools sort -m 1M -T tmpd/pfx -o big5_spill.bam big5.bam 2> spill.err; echo "-m 1M rc=$? : $(grep -a merging spill.err | head -1)"
eq "spilled sort (-m 1M, temp files) == in-memory sort (records, order)" "$(samtools view big5_spill.bam | md5sum)" "$(samtools view big5_mem.bam | md5sum)"
eq "temp files cleaned up" "$(ls tmpd | wc -l)" "0"
rm -f big5.bam big5_mem.bam big5_spill.bam

echo "### 3.5 Determinism: 3 runs at -@ 0 / 4 / 8 give identical record streams"
for t in 0 4 8; do samtools sort -@ $t -o det$t.bam $S; done
eq "-@ 0 vs -@ 4" "$(samtools view det0.bam | md5sum)" "$(samtools view det4.bam | md5sum)"
eq "-@ 0 vs -@ 8" "$(samtools view det0.bam | md5sum)" "$(samtools view det8.bam | md5sum)"

echo "### 3.6 Sort order with unmapped reads: unmapped last; mate-placed unmapped read stays next to mate"
samtools sort -o synth.sorted.bam $S
python $RUN/order_check.py synth.sorted.bam | grep -a n=
samtools view synth.sorted.bam | awk '$3=="*"' | wc -l | { read n; eq "fully-unmapped reads (RNAME *) at end" "$n" "10"; }
samtools view synth.sorted.bam | tail -10 | cut -f3 | sort -u | tr '\n' ' '; echo " <- RNAME of last 10 records"
samtools view synth.sorted.bam | grep -a -w '^half1' | cut -f1-4

echo "### 3.7 template-coordinate: SKILL says 'recommended for fgbio' but gives no command"
samtools sort --template-coordinate -o tc.bam $DATA/shuffled_real.bam 2> tc.err; echo "rc=$? $(head -2 tc.err | tr '\n' '|')"
echo "  (raw shuffled input, no fixmate) header: $(so tc.bam 2>/dev/null)"
samtools sort -n -o tcn.bam $S && samtools fixmate -m tcn.bam tcf.bam && samtools sort --template-coordinate -o tc2.bam tcf.bam 2> tc2.err; echo "  after collate/fixmate rc=$? $(head -1 tc2.err)"; echo "  header: $(so tc2.bam)"
summary
