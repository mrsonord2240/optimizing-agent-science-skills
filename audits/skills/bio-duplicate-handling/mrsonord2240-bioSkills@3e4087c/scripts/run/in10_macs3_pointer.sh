#!/bin/bash
# Side check (not scored as an input): the ChIP row says "MARK, do not remove; then use peak caller's auto-dup logic (macs3 --keep-dup auto)".
# Question: does macs3 honour the 0x400 flag itself, i.e. does a duplicate-MARKED BAM behave differently from the unmarked one, and is --keep-dup a real flag?
# macs3 is not in the env; install into a throwaway venv under work/ (pip, public PyPI), never into the shared env.
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
source /mnt/openscience/audits/bio-duplicate-handling/run/common.sh
cd $W; rm -rf in10; mkdir in10; cd in10
python -m venv v >/dev/null 2>&1 && ./v/bin/pip install -q macs3 2>&1 | tail -2
./v/bin/macs3 --version 2>&1 | head -1
./v/bin/macs3 callpeak --help 2>&1 | grep -A6 -- '--keep-dup' | head -14
# data: SYNTHETIC SE ChIP-like BAM: 2 000 reads in a 300 bp pileup ("peak") + background; each read start duplicated x5 at 200 positions
python - <<'PY'
import pysam, random
r = random.Random(1)
h = pysam.AlignmentHeader.from_dict({"HD": {"VN": "1.6", "SO": "coordinate"}, "SQ": [{"SN": "chr22", "LN": 40001}]})
recs = []
def add(name, pos, flag=0):
    a = pysam.AlignedSegment(h); a.query_name = name; a.flag = flag; a.reference_id = 0; a.reference_start = pos; a.mapping_quality = 60
    a.cigartuples = [(0, 50)]; a.query_sequence = "".join(r.choice("ACGT") for _ in range(50)); a.query_qualities = pysam.qualitystring_to_array("I" * 50); recs.append(a)
n = 0
for i in range(150):                       # a "peak" of unique starts
    for k in range(3): add("p%d_%d" % (i, k), 10000 + i * 2)   # 3 reads per start = "duplicates" that are real signal at a strong site
for i in range(600): add("b%d" % i, r.randrange(0, 39900))
recs.sort(key=lambda a: a.reference_start)
with pysam.AlignmentFile("chip.bam", "wb", header=h) as o:
    for a in recs: o.write(a)
print("chip.bam", len(recs))
PY
cp chip.bam unmarked.bam
samtools sort -n -o ns.bam chip.bam; samtools fixmate -m ns.bam fm.bam; samtools sort -o cs.bam fm.bam; samtools markdup cs.bam marked.bam
echo "marked.bam flagged: $(flagged marked.bam) of $(samtools view -c marked.bam)"
for auto in auto all 1; do
  for f in unmarked marked; do
    ./v/bin/macs3 callpeak -t $f.bam -f BAM -g 40001 -n ${f}_$auto --keep-dup $auto --nomodel --extsize 100 -q 0.5 >/dev/null 2> ${f}_$auto.log
    echo "keep-dup=$auto $f: $(grep -m1 'tags after filtering in treatment' ${f}_$auto.log | sed 's/.*INFO  @ //' ) | $(grep -m1 'Redundant rate of treatment' ${f}_$auto.log | sed 's/.*INFO  @ //') | peaks: $(grep -vc '^#\|^$\|^chr.*start' ${f}_${auto}_peaks.narrowPeak 2>/dev/null)"
  done
done
