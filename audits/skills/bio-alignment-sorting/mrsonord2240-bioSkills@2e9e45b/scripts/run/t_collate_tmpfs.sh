#!/bin/bash
# Is collate slow only because temp files land on the /mnt (9p) mount? Re-time in WSL-native /tmp (ext4).
source /mnt/openscience/audits/bio-alignment-sorting/run/common.sh
T=/tmp/af_sort_audit_collate; rm -rf $T; mkdir -p $T; cd $T
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
tn=$(best samtools sort -n -T tpn -o sn_nat.bam in.bam); tc=$(best samtools collate -o co.bam in.bam tpc); tcu=$(best bash -c 'samtools collate -O -u in.bam tpcu > cou.bam')
echo "in /tmp (ext4): sort -n ${tn}  collate -o ${tc}  collate -O -u ${tcu}   (SKILL: sort -n 0.66 s, collate 0.74 s)"
python -c "print('collate/sort -n time ratio in /tmp: %.2f' % ($tc/$tn))"
echo "same commands with temp prefix on /mnt/openscience, input+output in /tmp:"
tc2=$(best samtools collate -o co2.bam in.bam /mnt/openscience/audits/bio-alignment-sorting/run/work/tpc_mnt); echo "  collate with prefix on /mnt: ${tc2}"
cd /; rm -rf $T; rm -f /mnt/openscience/audits/bio-alignment-sorting/run/work/tpc_mnt*
