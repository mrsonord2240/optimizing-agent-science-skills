#!/bin/bash
# INPUT 5c (stress, part 3): measure the SKILL's "Compression Level Decision" table (size and wall time vs default -l 6)
# on real 1000G reads x20 (192k records, record-shuffled). Single thread (-@ 0) to keep timings comparable, 3 reps each.
source /mnt/openscience/audits/bio-alignment-sorting/run/common.sh
W=$WORK/in5c; rm -rf $W; mkdir -p $W; cd $W
python - <<'EOF'
import pysam, random
random.seed(1)
with pysam.AlignmentFile('/mnt/openscience/audits/bio-alignment-sorting/run/data/shuffled_1000g.bam','rb') as f:
    h=f.header; rs=list(f)
out=[]
for k in range(20): out.extend(rs)
random.shuffle(out)
with pysam.AlignmentFile('in.bam','wb',header=h) as o:
    for r in out: o.write(r)
print('in.bam records', len(out))
EOF
TIMEFORMAT=%R
declare -A SZ TM
for lv in 0 1 6 9; do
  best=999999
  for rep in 1 2 3; do
    t=$( { time samtools sort -l $lv -T tp$lv -o l$lv.bam in.bam 2>/dev/null; } 2>&1 )
    best=$(python -c "print(min($best,$t))")
  done
  SZ[$lv]=$(stat -c %s l$lv.bam); TM[$lv]=$best
done
best=999999
for rep in 1 2 3; do t=$( { time samtools sort -u -T tpu -o lu.bam in.bam 2>/dev/null; } 2>&1 ); best=$(python -c "print(min($best,$t))"); done
SZu=$(stat -c %s lu.bam); TMu=$best
python - <<EOF
sz={0:${SZ[0]},1:${SZ[1]},6:${SZ[6]},9:${SZ[9]}}; tm={0:${TM[0]},1:${TM[1]},6:${TM[6]},9:${TM[9]}}
claims={0:("+200-400% size","0% time"),1:("~+30% size","~+10% time"),6:("baseline","baseline"),9:("-2-5% size","+50-100% time")}
print("level  bytes      size_vs_l6   best_wall_s  time_vs_l6   SKILL claim (size / time)")
for lv in (0,1,6,9):
    print(f"-l {lv}   {sz[lv]:>9}  {100*(sz[lv]/sz[6]-1):>+8.1f}%   {tm[lv]:>8.2f}    {100*(tm[lv]/tm[6]-1):>+8.1f}%   {claims[lv][0]} / {claims[lv][1]}")
print("-u     ", ${SZu}, f"{100*(${SZu}/sz[6]-1):+.1f}%", ${TMu}, "s ; identical to -l 0 size:", ${SZu}==sz[0])
EOF
eq "-l 0 records == -l 6 records" "$(samtools view l0.bam | md5sum)" "$(samtools view l6.bam | md5sum)"
eq "-l 9 records == -l 6 records" "$(samtools view l9.bam | md5sum)" "$(samtools view l6.bam | md5sum)"
echo "-- default level: is plain 'samtools sort' == -l 6 bytes?"; samtools sort -T tpd -o ld.bam in.bam; echo "default size $(stat -c %s ld.bam) vs -l 6 $(stat -c %s l6.bam)"
echo "-- pipe claim: 'WRONG' (default compression between stages) vs 'RIGHT' (-u) for fixmate|sort on name-sorted input"
samtools sort -n -o ns.bam in.bam
best_w=999; best_r=999
for rep in 1 2 3; do
  t=$( { time samtools fixmate -m ns.bam - 2>/dev/null | samtools sort -T tpw -o w.bam 2>/dev/null; } 2>&1 ); best_w=$(python -c "print(min($best_w,$t))")
  t=$( { time samtools fixmate -m -u ns.bam - 2>/dev/null | samtools sort -T tpr -o r.bam 2>/dev/null; } 2>&1 ); best_r=$(python -c "print(min($best_r,$t))")
done
echo "  best wall: default-compression pipe ${best_w}s ; -u pipe ${best_r}s"
eq "both pipes give identical records" "$(samtools view w.bam | md5sum)" "$(samtools view r.bam | md5sum)"
rm -f in.bam l0.bam l1.bam l6.bam l9.bam lu.bam ld.bam ns.bam w.bam r.bam tp*
summary
