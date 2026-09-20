#!/bin/bash
# Input 7 (adversarial/ambiguous): "Clean my BAM: remove duplicates, keep only unique high-confidence
# properly-paired primary reads, and I will run Manta (SV caller) on it."
set -u
W=$1; mkdir -p $W; cd $W
PD=$AFDATA/derived/planted_dups.bam
echo "== A. 'Remove Duplicates' (SKILL.md: samtools view -F 1024) on a BAM whose duplicates are UNMARKED"
echo "records=$(samtools view -c $PD)  dup-flagged(-f 1024)=$(samtools view -c -f 1024 $PD)  after -F 1024: $(samtools view -c -F 1024 $PD)"
echo "   ground truth (planted): 50 pairs = 100 duplicate reads => expected 400 after true dedup"
echo "== B. Following the Related Skill order (mark first, then filter)"
samtools collate -o c.bam $PD
samtools fixmate -m c.bam fm.bam
samtools sort -o s.bam fm.bam
samtools markdup s.bam md.bam
echo "after markdup: dup-flagged=$(samtools view -c -f 1024 md.bam)  after -F 1024: $(samtools view -c -F 1024 md.bam)  (expected 100 / 400)"
echo "   is any hint in SKILL.md/usage-guide to check dup flags exist before -F 1024?"
grep -n -i -E "mark(ed)? dup|markdup|dup.*flag|not marked|unmarked" $2/SKILL.md $2/usage-guide.md
echo "== C. SV request: SKILL.md says SV callers need supplementary (2048) reads; -F 3332 / -F 2304 / -F 2308 remove them"
S=$3   # synthetic all-flag BAM
echo "supplementary records in synthetic set: $(samtools view -c -f 2048 $S)"
echo "  -F 1024 keeps supp: $(samtools view -c -f 2048 -F 1024 $S)"
echo "  -F 3332 -q 30 keeps supp: $(samtools view -c -f 2048 -F 3332 -q 30 $S)"
echo "  -F 2308 (usage-guide 'most downstream analyses') keeps supp: $(samtools view -c -f 2048 -F 2308 $S)"
echo "  somatic recipe -F 3328 -q 1 keeps supp: $(samtools view -c -f 2048 -F 3328 -q 1 $S)  (SKILL.md text: 'chimeric reads at SVs may carry real somatic SNVs')"
echo "== D. Orphaned mates after read-level filtering (1000g slice), -F 3332 -q 30"
G=$AFDATA/1000g/HG00349.chr20_1400000-1500000.bam
samtools view -F 3332 -q 30 -o f.bam $G
python - <<'PY'
import pysam, collections, sys
def orphans(path):
    c = collections.Counter(); meta = {}
    for r in pysam.AlignmentFile(path):
        if r.is_secondary or r.is_supplementary: continue
        c[r.query_name] += 1
        meta[r.query_name] = r.flag
    # paired, mate mapped (flag&8==0) but only one record present in file
    return sum(1 for q, n in c.items() if n == 1 and meta[q] & 1 and not meta[q] & 8), len(c)
import os
G = os.environ['AFDATA'] + '/1000g/HG00349.chr20_1400000-1500000.bam'
print('single-record templates whose flag says paired+mate-mapped: before filter %d of %d templates; after -F 3332 -q 30: %d of %d' % (orphans(G) + orphans('f.bam')))
PY
echo "   flagstat singletons after filter:"; samtools flagstat f.bam | grep -E "singletons|properly|with itself"
echo "   mentions of fixmate/orphan/singleton in the Skill files:"; grep -n -i -E "fixmate|orphan|singleton" $2/SKILL.md $2/usage-guide.md || echo "   (none)"
echo "== E. 'Count unique: -F 2304 (primary only)' label vs real uniqueness: STAR real BAM primary records with NH>1 under -F 2304"
R=$AFDATA/human/test.rna.paired_end.sorted.bam
echo "   -F 2304 records: $(samtools view -c -F 2304 $R)   of which NH>1: $(samtools view -c -F 2304 -e '[NH] > 1' $R)   (-q 255 records: $(samtools view -c -q 255 $R))"
