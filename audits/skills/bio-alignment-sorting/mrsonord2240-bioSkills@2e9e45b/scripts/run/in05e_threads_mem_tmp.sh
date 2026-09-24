#!/bin/bash
# INPUT 5e (stress, part 5): thread / memory / temp-file claims in the fixed SKILL:
#  (a) "-@ N adds N threads (N+1 total). Output is identical for any -@."  -> peak thread count (nlwp) of the running sort
#  (b) "-m is per thread, so peak memory is about (-@ + 1) x -m. Values below 1M are rejected. Data beyond the budget spills
#       to temp files and is merged; the result is unchanged."  -> max RSS via /usr/bin/time -v
#  (c) "-T is a PREFIX (temp files are PREFIX.nnnn.bam), not a directory."  -> watch the temp files while a sort runs
# Real 1000G reads x40 (384k records) so the sort runs long enough to observe.
source /mnt/openscience/audits/bio-alignment-sorting/run/common.sh
W=$WORK/in5e; rm -rf $W; mkdir -p $W; cd $W
python - <<'EOP'
import pysam, random
random.seed(5)
with pysam.AlignmentFile('/mnt/openscience/audits/bio-alignment-sorting/run/data/shuffled_1000g.bam','rb') as f:
    h=f.header; rs=list(f)
out=[]
for k in range(40): out.extend(rs)
random.shuffle(out)
with pysam.AlignmentFile('in.bam','wb',header=h) as o:
    for r in out: o.write(r)
print('in.bam records', len(out))
EOP

echo "### (a) thread count: peak NLWP of samtools sort -@ N while it runs (mid-run sampling of /proc)"
peak() { # $1 = -@ value
  samtools sort -@ $1 -m 50M -T pk$1 -o pk$1.bam in.bam 2>/dev/null &
  pid=$!; mx=0
  while kill -0 $pid 2>/dev/null; do
    n=$(awk '/^Threads:/{print $2}' /proc/$pid/status 2>/dev/null); [ -n "$n" ] && [ "$n" -gt "$mx" ] && mx=$n
    sleep 0.05
  done; wait $pid; echo $mx
}
for t in 0 2 4 8; do echo "  -@ $t : peak threads seen = $(peak $t)  (SKILL: N+1 workers = $((t+1)) + main/IO threads if any)"; done
eq "-@ 0 vs -@ 8 identical records" "$(samtools view pk0.bam | md5sum)" "$(samtools view pk8.bam | md5sum)"

echo "### (b) memory: max RSS with -m 20M for -@ 0 / 1 / 3 (SKILL: about (-@+1) x -m; spills the rest)"
for t in 0 1 3; do
  /usr/bin/time -v samtools sort -@ $t -m 20M -T mem$t -o mem$t.bam in.bam 2> tv$t.txt
  echo "  -@ $t -m 20M : max RSS $(awk -F: '/Maximum resident/{gsub(/ /,"",$2); printf "%.0f MB", $2/1024}' tv$t.txt) ; $(grep -a 'merging from' tv$t.txt | head -1)"
done
echo "-- unconstrained default (-m 768M default) for scale:"
/usr/bin/time -v samtools sort -T memd -o memd.bam in.bam 2> tvd.txt; echo "  default: max RSS $(awk -F: '/Maximum resident/{gsub(/ /,"",$2); printf "%.0f MB", $2/1024}' tvd.txt) ; $(grep -a 'merging from' tvd.txt | head -1)"
eq "spilled -m 20M output == default output (records)" "$(samtools view mem0.bam | md5sum)" "$(samtools view memd.bam | md5sum)"
eq "-@ 3 -m 20M output == default output (records)" "$(samtools view mem3.bam | md5sum)" "$(samtools view memd.bam | md5sum)"

echo "### (c) -T prefix: list temp files DURING a spilling sort (-m 5M) with -T tdir/pfx and -T existing-dir"
mkdir -p tdir existing_dir
samtools sort -m 5M -T tdir/pfx -o t1.bam in.bam 2>/dev/null &
pid=$!; seen=""
while kill -0 $pid 2>/dev/null; do f=$(ls tdir 2>/dev/null | head -3 | tr '\n' ' '); [ -n "$f" ] && seen="$f"; sleep 0.05; done; wait $pid
echo "  temp names seen with -T tdir/pfx : $seen"
echo "$seen" | grep -q -E 'pfx\.[0-9]{4}\.bam' && echo "  [PASS] PREFIX.nnnn.bam pattern" || echo "  [FAIL] pattern differs"
samtools sort -m 5M -T existing_dir -o t2.bam in.bam 2>/dev/null &
pid=$!; seen2=""; seen3=""
while kill -0 $pid 2>/dev/null; do f=$(ls existing_dir 2>/dev/null | head -2 | tr '
' ' '); [ -n "$f" ] && seen2="$f"; g=$(ls | grep -a '^existing_dir\.' | head -2 | tr '
' ' '); [ -n "$g" ] && seen3="$g"; sleep 0.05; done; wait $pid
echo "  with -T existing_dir (an existing DIRECTORY): files seen INSIDE the dir during the sort: '$seen2' ; sibling PREFIX.nnnn files in cwd: '$seen3'"
echo "  temp files after completion: $(ls tdir | wc -l) in tdir"
eq "records with -T prefix" "$(samtools view t1.bam | md5sum)" "$(samtools view memd.bam | md5sum)"
rm -f in.bam pk*.bam mem*.bam t1.bam t2.bam
summary
