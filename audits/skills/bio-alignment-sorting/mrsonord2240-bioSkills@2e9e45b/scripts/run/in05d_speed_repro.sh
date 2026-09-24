#!/bin/bash
# INPUT 5d (stress, part 4): fixed SKILL says "collate is not reliably faster: on a 192k-read slice collate took 0.74 s against
# 0.66 s for sort -n". Re-measure sort -n / -N / collate (three invocation forms); byte-level repeat determinism of sort;
# idempotency of re-sorting; @PG accumulation; --write-index. Real 1000G reads x20 (192k records).
source /mnt/openscience/audits/bio-alignment-sorting/run/common.sh
W=$WORK/in5d; rm -rf $W; mkdir -p $W; cd $W
python - <<'EOP'
import pysam, random
random.seed(2)
with pysam.AlignmentFile('/mnt/openscience/audits/bio-alignment-sorting/run/data/shuffled_1000g.bam','rb') as f:
    h=f.header; rs=list(f)
out=[]
for k in range(20): out.extend(rs)
random.shuffle(out)
with pysam.AlignmentFile('in.bam','wb',header=h) as o:
    for r in out: o.write(r)
print('in.bam records', len(out))
EOP
TIMEFORMAT=%R
best() { local b=999; for rep in 1 2 3 4 5; do t=$( { time "$@" >/dev/null 2>&1; } 2>&1 ); b=$(python -c "print(min($b,$t))"); done; echo $b; }
tn=$(best samtools sort -n -T tpn -o sn_nat.bam in.bam)
tN=$(best samtools sort -N -T tpN -o sn_asc.bam in.bam)
tc1=$(best samtools collate -o co1.bam in.bam tpc1)
tc2=$(best bash -c 'samtools collate -O -u in.bam tpc2 > co2.bam')
tc3=$(best samtools collate -T tpc3 -o co3.bam in.bam)
echo "best of 5 wall (s), 192k records, -@ 0:  sort -n ${tn}  sort -N ${tN}  collate -o ${tc1}  collate -O -u ${tc2}  collate -T -o ${tc3}"
python -c "print('collate -o vs sort -n: %.2fx ; collate -O -u vs sort -n: %.2fx   (SKILL: 0.74 s vs 0.66 s, i.e. ~0.9x = not reliably faster)' % ($tn/$tc1, $tn/$tc2))"
echo "-- SAME 192k records but UNIQUE read names (each copy k renamed name_k): the 20x-duplicated names above may be pathological for collate's hash buckets"
python - <<'EOP'
import pysam, random
random.seed(9)
with pysam.AlignmentFile('/mnt/openscience/audits/bio-alignment-sorting/run/data/shuffled_1000g.bam','rb') as f:
    h=f.header; rs=list(f)
out=[]
for k in range(20):
    for r in rs:
        a=pysam.AlignedSegment.from_dict(r.to_dict(), h); a.query_name=r.query_name+'_%d'%k; out.append(a)
random.shuffle(out)
with pysam.AlignmentFile('uniq.bam','wb',header=h) as o:
    for r in out: o.write(r)
print('uniq.bam records', len(out), 'distinct names', len({r.query_name for r in out}))
EOP
u_n=$(best samtools sort -n -T tpun -o un.bam uniq.bam); u_N=$(best samtools sort -N -T tpuN -o uN.bam uniq.bam)
u_c=$(best samtools collate -o uc.bam uniq.bam tpuc); u_cu=$(best bash -c 'samtools collate -O -u uniq.bam tpucu > ucu.bam')
echo "  unique names, best of 5:  sort -n ${u_n}  sort -N ${u_N}  collate -o ${u_c}  collate -O -u ${u_cu}"
python -c "print('  collate -o vs sort -n on unique names: %.2fx' % ($u_n/$u_c))"
echo "-- and the REAL human PE BAM (5644 records, real names), best of 5:"
h_n=$(best samtools sort -n -T tph -o hn.bam $PD/human/test.paired_end.sorted.bam); h_c=$(best samtools collate -o hc.bam $PD/human/test.paired_end.sorted.bam tphc)
echo "  real BAM: sort -n ${h_n}  collate -o ${h_c}"
rm -f uniq.bam un.bam uN.bam uc.bam ucu.bam hn.bam hc.bam
echo "-- collate with -@ 4 vs sort -n -@ 4"
tn4=$(best samtools sort -n -@ 4 -T tpn4 -o sn4.bam in.bam); tc4=$(best samtools collate -@ 4 -o co4.bam in.bam tpc4); echo "  sort -n -@4 ${tn4} ; collate -@4 ${tc4}"
echo "-- byte-level repeat determinism (same command twice, -@ 0 and -@ 4)"
samtools sort -o r1.bam in.bam; samtools sort -o r2.bam in.bam; cmp -s r1.bam r2.bam && echo "  -@ 0: two runs byte-identical" || echo "  -@ 0: BAM bytes differ (expected: @PG CL line carries the output name)"
samtools sort -@ 4 -o r3.bam in.bam
eq "-@ 0 vs -@ 4 record stream" "$(samtools view r1.bam | md5sum)" "$(samtools view r3.bam | md5sum)"
echo "-- idempotency: re-sorting an already coordinate-sorted BAM"
samtools sort -o r5.bam r1.bam
eq "re-sort record stream unchanged" "$(samtools view r5.bam | md5sum)" "$(samtools view r1.bam | md5sum)"
echo "  @PG lines: in=$(samtools view -H in.bam | grep -ac '^@PG') r1=$(samtools view -H r1.bam | grep -ac '^@PG') r5(re-sorted)=$(samtools view -H r5.bam | grep -ac '^@PG')"
echo "-- --write-index (SKILL: 'writes sorted.bam.csi, not .bai'): "
samtools sort --write-index -o wi.bam in.bam; ls wi.bam*; samtools quickcheck -v wi.bam && echo "  quickcheck ok"
samtools sort --write-index -o wi2.bam##idx##wi2.bam.bai in.bam; ls wi2.bam*
rm -f in.bam sn*.bam co*.bam r*.bam wi*.bam tp*
summary
