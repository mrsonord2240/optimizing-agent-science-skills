#!/bin/bash
# Input 8 (NEW, auditor's own truth; adversarial/ambiguous request): "my capture library has duplex UMIs in RX; dedup it with the UMIs, call
# consensus, duplex if possible". SYNTHETIC planted duplex-UMI BAM (20_make_planted_umi.py): 210 pairs, truth
#   80 strand-aware families, 110 exact-UMI families, 50 duplex molecules (30 duplex + 20 collision molecules at shared coordinates).
# The fixer's blocks are extracted VERBATIM: umi_tools bulk paired, fgbio (mated -> adjacency -> molecular consensus; paired -> duplex), Picard UmiAware.
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
source /mnt/openscience/audits/bio-duplicate-handling/run/common.sh
cd $W; rm -rf in08; mkdir in08; cd in08
strip() { sed 's/\x1b\[[0-9;]*m//g'; }
python $RUN/20_make_planted_umi.py raw.bam
echo "### 8a coordinate-only tools on the UMI library (what an agent that ignores the UMI section would do): truth = 260 dup reads if UMI-aware (80 of 210 pairs kept)"
samtools sort -n -o qn.bam raw.bam; samtools fixmate -m qn.bam mated0.bam; samtools sort -o cs.bam mated0.bam
samtools markdup cs.bam plain.bam; echo "  samtools markdup (no UMI): flagged $(flagged plain.bam) reads = $(( $(flagged plain.bam)/2 )) pairs -> keeps $(( 210 - $(flagged plain.bam)/2 )) pairs"
picard MarkDuplicates I=cs.bam O=pic.bam M=pic.txt >/dev/null 2>&1; echo "  Picard MarkDuplicates (no UMI): flagged $(flagged pic.bam) reads -> keeps $(( 210 - $(flagged pic.bam)/2 )) pairs"
samtools markdup --barcode-tag RX cs.bam bc.bam; echo "  samtools markdup --barcode-tag RX: flagged $(flagged bc.bam) reads = $(( $(flagged bc.bam)/2 )) pairs -> keeps $(( 210 - $(flagged bc.bam)/2 )) pairs (exact-UMI truth 110)"
echo "### 8b umi_tools bulk paired block, verbatim (raw.bam in cwd)"
mkdir ut; cd ut; cp ../raw.bam .
blk "### umi_tools dedup" 1 > ut_block.sh
sed -n '/^# Bulk UMI, paired-end/,$p' ut_block.sh > ut_bulk.sh; cat ut_bulk.sh
bash ut_bulk.sh > ut.out 2> ut.err; echo "  exit=$? dedup.bam records $(samtools view -c dedup.bam) = $(( $(samtools view -c dedup.bam)/2 )) pairs (truth 80 strand-aware pairs)"
sed 's/--method=directional/--method=unique/' ut_bulk.sh > ut_unique.sh; sed -i 's#dedup.bam#dedup_unique.bam#' ut_unique.sh; bash ut_unique.sh >/dev/null 2>&1; echo "  --method=unique: $(( $(samtools view -c dedup_unique.bam)/2 )) pairs (truth 110)"
cd ..
echo "### 8c fgbio block, verbatim"
mkdir fg; cd fg; cp ../raw.bam .
blk "### fgbio consensus (bulk UMI / ctDNA, best practice for low-VAF detection)" 1 > fg_block.sh
bash -e fg_block.sh > fg.out 2> fg.err; echo "  block exit=$?"; strip < fg.err | grep -iE 'exception|fatal' | head -2
python - <<'PY'
import pysam, json, re
truth = json.load(open("../raw.bam.truth.json"))
def mi_groups(p, strip_strand=False):
    s = set()
    for r in pysam.AlignmentFile(p, check_sq=False):
        mi = r.get_tag("MI")
        s.add(re.sub(r"/[AB]$", "", mi) if strip_strand else mi)
    return len(s)
def count(p): return sum(1 for _ in pysam.AlignmentFile(p, check_sq=False))
g, gd = "grouped.bam", "grouped_duplex.bam"
print(f"  mated.bam {count('mated.bam')} records (input 420)")
print(f"  grouped (adjacency): records {count(g)}, MI groups {mi_groups(g)}  (truth strand-aware families {truth['families_strand_aware']})")
print(f"  grouped_duplex (paired): records {count(gd)}, MI groups incl. /A/B {mi_groups(gd)}, base MI groups {mi_groups(gd, True)}  (truth duplex molecules {truth['duplex_molecules']})")
print(f"  consensus.bam (single-strand): {count('consensus.bam')} records = {count('consensus.bam')//2} pairs (truth {truth['families_strand_aware']})")
print(f"  duplex.bam: {count('duplex.bam')} records = {count('duplex.bam')//2} pairs (truth {truth['duplex_molecules']})")
# strand assignment check: for the 30 duplex molecules all copies share the base MI with 3 top (/A) + 2 bottom (/B)
from collections import defaultdict
strand = defaultdict(lambda: defaultdict(set))
for r in pysam.AlignmentFile(gd, check_sq=False):
    m = re.match(r"S1m(\d+)([tb])(\d)", r.query_name)
    if m: strand[m.group(1)][re.sub(r"^\d+/", "", r.get_tag("MI"))].add((m.group(2)))
ok = sum(1 for k, v in strand.items() if len(v) == 2 and all(len(x) == 1 for x in v.values()))
print(f"  duplex molecules whose /A and /B each contain only one physical strand: {ok} of {len(strand)}")
PY
echo "  consensus/duplex reads unmapped: $(samtools view -F 4 consensus.bam | wc -l) mapped in consensus, $(samtools view -F 4 duplex.bam | wc -l) in duplex"
cd ..
echo "### 8d Picard UmiAware block, verbatim (coordsort_fixmate.bam = coordinate-sorted fixmate output)"
mkdir pu; cd pu; cp ../cs.bam coordsort_fixmate.bam
blk "### Picard UMI-aware marking" 1 > pu.sh; bash pu.sh > pu.out 2> pu.err; echo "  exit=$? flagged $(flagged marked.bam) reads = $(( $(flagged marked.bam)/2 )) pairs -> keeps $(( 210 - $(flagged marked.bam)/2 )) pairs (truth 80)"
grep -iE 'exception|error' pu.err | head -2
grep -v '^#' umi_metrics.txt | head -3 | cut -f1-12
cd ..
