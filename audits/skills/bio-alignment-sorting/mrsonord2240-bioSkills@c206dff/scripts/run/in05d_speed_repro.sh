#!/bin/bash
# INPUT 5d (stress, part 4): SKILL claim "collate ~3-10x faster than sort -n"; byte-level repeat determinism of sort;
# idempotency of re-sorting; @PG accumulation. Real 1000G reads x20 (192k records).
source /mnt/openscience/audits/bio-alignment-sorting/run/common.sh
W=$WORK/in5d; rm -rf $W; mkdir -p $W; cd $W
python - <<'EOF'
import pysam, random
random.seed(2)
with pysam.AlignmentFile('/mnt/openscience/audits/bio-alignment-sorting/run/data/shuffled_1000g.bam','rb') as f:
    h=f.header; rs=list(f)
out=[]
for k in range(20): out.extend(rs)
random.shuffle(out)
with pysam.AlignmentFile('in.bam','wb',header=h) as o:
    for r in out: o.write(r)
EOF
TIMEFORMAT=%R
tn=999; tc=999; tN=999; tcu=999
for rep in 1 2 3; do
  t=$( { time samtools sort -n -T tpn -o sn.bam in.bam 2>/dev/null; } 2>&1 ); tn=$(python -c "print(min($tn,$t))")
  t=$( { time samtools sort -N -T tpN -o sN.bam in.bam 2>/dev/null; } 2>&1 ); tN=$(python -c "print(min($tN,$t))")
  t=$( { time samtools collate -T tpc -o co.bam in.bam 2>/dev/null; } 2>&1 ); tc=$(python -c "print(min($tc,$t))")
  t=$( { time samtools collate -u -O in.bam tpcu 2>/dev/null > cou.bam; } 2>&1 ); tcu=$(python -c "print(min($tcu,$t))")
done
echo "best wall (s), 192k records, -@ 0:  sort -n ${tn}  sort -N ${tN}  collate ${tc}  collate -u -O ${tcu}"
python -c "print('speed-up collate vs sort -n: %.1fx ; collate -u -O vs sort -n: %.1fx  (SKILL claim: ~3-10x)' % ($tn/$tc, $tn/$tcu))"
echo "-- byte-level repeat determinism (same command twice, -@ 0 and -@ 4)"
samtools sort -o r1.bam in.bam; samtools sort -o r2.bam in.bam; cmp -s r1.bam r2.bam && echo "  [PASS] -@ 0: two runs byte-identical" || echo "  [INFO] -@ 0: BAM bytes differ"
samtools sort -@ 4 -o r3.bam in.bam; samtools sort -@ 4 -o r4.bam in.bam; cmp -s r3.bam r4.bam && echo "  [PASS] -@ 4: two runs byte-identical" || echo "  [INFO] -@ 4: BAM bytes differ"
eq "-@ 0 vs -@ 4 record stream" "$(samtools view r1.bam | md5sum)" "$(samtools view r3.bam | md5sum)"
echo "-- idempotency: re-sorting an already coordinate-sorted BAM"
samtools sort -o r5.bam r1.bam
eq "re-sort record stream unchanged" "$(samtools view r5.bam | md5sum)" "$(samtools view r1.bam | md5sum)"
echo "  @PG lines: in=$(samtools view -H in.bam | grep -ac '^@PG') r1=$(samtools view -H r1.bam | grep -ac '^@PG') r5(re-sorted)=$(samtools view -H r5.bam | grep -ac '^@PG')"
samtools sort --no-PG -o r6.bam r5.bam; echo "  with --no-PG: @PG lines=$(samtools view -H r6.bam | grep -ac '^@PG')"
echo "-- --write-index (samtools >=1.16; not in SKILL): sort + index in one pass"
samtools sort --write-index -o wi.bam##idx##wi.bam.bai in.bam; ls -la wi.bam.bai | cut -c1-60; samtools quickcheck wi.bam && echo "  quickcheck ok"
rm -f in.bam sn.bam sN.bam co.bam cou.bam r*.bam wi.bam tp*
summary
