#!/usr/bin/env python3
"""Input 5 (Stress / multi-part, REAL data): 'Run the Skill's library-typed flag cheat-sheet on real ARTIC amplicon, RNA-seq (spliced) and
1000G germline data, and diagnose reference mismatches.'  Every flag row is run; outputs are verified against independent pysam /
samtools depth computations; error paths are run against deliberately mismatched references."""
import os, re, shutil, sys, time
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from snippets import load_functions
import pysam

I = 5
P = AFDATA
ART = P + "/sarscov2/sars-cov-2_v5.3.2.nanopore.bam"; ARTREF = P + "/sarscov2/MN908947.3.fasta"
ILL = P + "/sarscov2/test.paired_end.sorted.bam"; ILLREF = P + "/sarscov2/genome.fasta"
RNA = HUMAN + "/test.rna.paired_end.sorted.bam"; HREF = HUMAN + "/genome.fasta"
G1K = P + "/1000g/HG00349.chr20_1400000-1500000.bam"; G1KREF = P + "/1000g/chr20_padded_1500000.fa"
W = WORK + "/in05"; os.makedirs(W, exist_ok=True)
# public-data is read-only for us: copy the two un-indexed BAMs and index the copies
for src, name in ((ART, "artic.bam"), (RNA, "rna.bam")):
    shutil.copy(src, W + "/" + name)
    sh(f"samtools index {W}/{name}", check=True)
ART = W + "/artic.bam"; RNA = W + "/rna.bam"

def expected_depth(bam, contig, min_q=0, min_mq=0, count_del=True):
    """independent per-position depth from pysam records: excluded flags UNMAP,SECONDARY,QCFAIL,DUP ; baseQ>=min_q ; deleted refs counted"""
    exp = Counter()
    for a in pysam.AlignmentFile(bam).fetch(contig):
        if a.is_unmapped or a.is_secondary or a.is_qcfail or a.is_duplicate or a.mapping_quality < min_mq:
            continue
        for qp, rp in a.get_aligned_pairs():
            if rp is None:
                continue
            if qp is None:
                if count_del:
                    exp[rp + 1] += 1
            elif a.query_qualities[qp] >= min_q:
                exp[rp + 1] += 1
    return exp

# ---------------- A. cheat-sheet: every row runs (accepted flags, non-empty output, no 'invalid option')
rows_cs = [
    ("Short-read germline WGS", "-q 20 -Q 20 -d 0"),
    ("Short-read tumor WGS", "-q 1 -Q 13 -d 0 -B"),
    ("Amplicon viral (ARTIC)", "-aa -A -d 600000 -B -Q 20"),
    ("Capture / exome", "-q 20 -Q 20 -d 250"),
    ("Long-read ONT R10.4+", "-q 30 -Q 0 -B -d 0"),
    ("PacBio HiFi", "-q 20 -Q 0 -B -d 0"),
    ("RNA-seq variants", "-q 20 -Q 20 -B -d 0"),
    ("Forensic / aDNA", "-q 0 -Q 0 -A -d 0 -B"),
]
for label, fl in rows_cs:
    rc, out, err = sh(f"samtools mpileup -f {HREF} {fl} -r chr22:1952-4617 {HUMAN}/test.paired_end.sorted.bam")
    n = len(mpileup_rows(out))
    check(I, f"cheat-sheet row '{label}': `{fl}` accepted, produces rows", rc == 0 and n > 1000 and "invalid" not in err.lower(), f"rc={rc} rows={n} stderr={err.strip()[:80]!r}")
rc, out, err = sh(f"bcftools mpileup -f {HREF} -q 30 -Q 0 -B -d 0 --max-BQ 30 -r chr22:3000 {HUMAN}/test.paired_end.sorted.bam | tail -1 | cut -f1-2")
check(I, "ONT row: `bcftools mpileup ... -q 30 -Q 0 -B -d 0 --max-BQ 30` accepted (bcftools has -d 0)", rc == 0 and out.startswith("chr22"), (out + err).strip()[:100])

# ---------------- B. ARTIC nanopore amplicon BAM (MN908947.3): -aa -A -d 600000 -B -Q 20
t = time.time()
rc, out, err = sh(f"samtools mpileup -f {ARTREF} -aa -A -d 600000 -B -Q 20 {ART}")
rows = mpileup_rows(out)
print(f"ARTIC -aa rows={len(rows)} in {time.time()-t:.1f}s")
check(I, "ARTIC row emits one line per genome position (29903 rows, MN908947.3)", len(rows) == 29903 and rows[0][1] == "1" and rows[-1][1] == "29903", f"{len(rows)} rows")
exp = expected_depth(ART, "MN908947.3", min_q=20, count_del=False)
diff = []
for r in rows:
    nd = parse_bases(r[4], r[2])[1]["*"] if r[3] != "0" else 0
    if int(r[3]) - nd != exp.get(int(r[1]), 0):
        diff.append((int(r[1]), int(r[3]), nd, exp.get(int(r[1]), 0)))
check(I, "ARTIC depth column minus '*' slots == independent pysam count of aligned bases with baseQ>=20 at all 29903 positions (note: -Q also thins the '*' deletion slots)", not diff, f"{len(diff)} differ e.g. {diff[:3]}")
zeros = sum(1 for r in rows if r[3] == "0")
rc, out_a, _ = sh(f"samtools mpileup -f {ARTREF} -a -A -d 600000 -B -Q 20 {ART}")
rows_a = mpileup_rows(out_a)
check(I, "SKILL: '-aa is required for ARTIC' -- plain `-a` already emits the same 29903 rows for a single-contig BAM", len(rows_a) == len(rows), f"-a rows={len(rows_a)} vs -aa rows={len(rows)} ({zeros} zero-depth positions in both)")
rc, out_n, _ = sh(f"samtools mpileup -f {ARTREF} -A -d 600000 -B -Q 20 {ART}")
check(I, "without -a/-aa the zero-depth positions are missing (consensus would skip them)", len(mpileup_rows(out_n)) == 29903 - zeros, f"{len(mpileup_rows(out_n))} rows, expected {29903 - zeros}")
# ONT row on same data
rc, out, err = sh(f"samtools mpileup -f {ARTREF} -q 30 -Q 0 -B -d 0 {ART}")
expq = expected_depth(ART, "MN908947.3", min_q=0, min_mq=30)
mr = {int(r[1]): int(r[3]) for r in mpileup_rows(out)}
diff = [p for p in expq if mr.get(p, 0) != expq[p]]
print("MAPQ dist ARTIC:", Counter(a.mapping_quality for a in pysam.AlignmentFile(ART)))
check(I, "ONT row `-q 30 -Q 0 -B -d 0` depth == independent count of MAPQ>=30 reads", not diff and mr, f"{len(diff)} differ; positions with data={len(mr)}")
# what do the default excluded flags / secondary do here?  (ARTIC data has none) skip

# ---------------- C. real spliced RNA-seq BAM: '>' '<' symbols and the SKILL pysam counter
rc, out, err = sh(f"samtools mpileup -f {HREF} -q 20 -Q 20 -B -d 0 {RNA}")
rr = mpileup_rows(out)
gt = sum(parse_bases(r[4], r[2])[1][">"] for r in rr); lt = sum(parse_bases(r[4], r[2])[1]["<"] for r in rr)
star = sum(parse_bases(r[4], r[2])[1]["*"] for r in rr)
print(f"RNA-seq mpileup: '>' slots={gt} '<' slots={lt} '*' slots={star} rows={len(rr)}")
check(I, "RNA-seq row: spliced reads appear as '>'/'<' in the base column (Skill table)", gt + lt > 0, f"{gt} '>' and {lt} '<'")
# Skill's pysam allele_counts at an intronic position with many ref-skips
skill = load_functions("SKILL.md"); ac = skill["allele_counts"]
best = max(rr, key=lambda r: parse_bases(r[4], r[2])[1][">"] + parse_bases(r[4], r[2])[1]["<"])
p = int(best[1]); n, c = parse_bases(best[4], best[2])
cnt = ac(RNA, "chr22", p - 1)
print("position with most ref-skips:", p, "mpileup '>'/'<'/'*':", c[">"], c["<"], c["*"], "| SKILL allele_counts:", cnt)
check(I, "SKILL allele_counts at a real intron position does NOT report ref-skips as 'DEL' (mpileup: '*' = 0 real deletions here)", cnt.get("DEL", 0) == c["*"], f"allele_counts DEL={cnt.get('DEL')} vs mpileup real deletions '*'={c['*']}, '>'+'<'={c['>'] + c['<']}")

# ---------------- D. 1000G germline row + default excluded flags (101 pre-flagged duplicates)
rc, out, err = sh(f"samtools mpileup -f {G1KREF} -q 20 -Q 20 -d 0 -r chr20:1400001-1500000 {G1K}")
g = mpileup_rows(out)
print("1000G default germline row rows:", len(g), err.strip()[:80])
ref = pysam.FastaFile(G1KREF)
okref = all(ref.fetch("chr20", int(r[1]) - 1, int(r[1])).upper() == r[2] for r in g[:2000])
check(I, "1000G germline row: rows produced and ref column == FASTA", len(g) > 1000 and okref, f"{len(g)} rows")
_, o1, _ = sh(f"samtools mpileup -f {G1KREF} -B -x -A -Q 0 -q 0 -d 0 -r chr20:1400001-1500000 {G1K}")
_, o2, _ = sh(f"samtools mpileup -f {G1KREF} -B -x -A -Q 0 -q 0 -d 0 --ff 0 -r chr20:1400001-1500000 {G1K}")
d1 = sum(int(r[3]) for r in mpileup_rows(o1)); d2 = sum(int(r[3]) for r in mpileup_rows(o2))
ndup = sum(1 for a in pysam.AlignmentFile(G1K).fetch("chr20", 1400000, 1500000) if a.is_duplicate)
exp = expected_depth(G1K, "chr20", min_q=0)
mr = {int(r[1]): int(r[3]) for r in mpileup_rows(o1)}
diff = [p for p in mr if mr[p] != exp.get(p, 0)]
check(I, "1000G: all-filters-off mpileup depth == independent pysam count at every position", not diff, f"{len(diff)} differ (windowed to reads overlapping region)")
check(I, "1000G: default flags silently drop the pre-flagged duplicates (Skill never says so): sum depth default-excl < --ff 0", d2 > d1, f"sum depth {d1} vs {d2}; {ndup} duplicate-flagged reads overlap the region")

# ---------------- E. error paths named in the Skill: mismatched references, missing index, missing fai
def run_err(cmd):
    rc, out, err = sh(cmd)
    return rc, len(mpileup_rows(out)), err.strip()
rc, n, err = run_err(f"samtools mpileup -f {ILLREF} -r MN908947.3:100-110 {ART}")  # MT192765.1 fasta, MN908947.3 BAM
print("ARTIC BAM + MT192765.1 FASTA (contig missing from ref):", rc, n, err[:250])
check(I, "wrong-reference case: message names the missing contig", "MN908947.3" in err and "not found" in err, f"rc={rc} rows={n} err={err[:150]!r}")
check(I, "wrong-reference case: exits non-zero (an agent following the Skill's `> pileup.txt` would otherwise accept the output)", rc != 0, f"rc={rc}; still emitted {n} rows for the 10 bp region with reference base N: {sh(f'samtools mpileup -f {ILLREF} -r MN908947.3:100-102 {ART} 2>/dev/null')[1].strip()[:70]!r}")
check(I, "Skill troubleshooting text 'No sequences in common' is the message users will actually see", "No sequences in common" in err, f"actual: {err.splitlines()[1][:100] if len(err.splitlines())>1 else err[:100]!r}")
rcb, ob, eb = sh(f"bcftools mpileup -f {ILLREF} -r MN908947.3:100-110 {ART} | head -30 | grep -v '^##' | head -3")
print("bcftools mpileup mismatched ref:", rcb, ob.strip()[:200], "|", eb.strip()[:250])
rc2, n2, err2 = run_err(f"samtools mpileup -f {ILLREF} {ART} | head -3")
print("same without -r:", rc2, n2, err2[:250])
rcx, outx, errx = sh(f"samtools mpileup -f {ILLREF} {ART} > {W}/mism.txt; echo rc=$?")
print("no -r, full BAM:", outx.strip(), errx.strip()[:250], os.path.getsize(W + "/mism.txt"))
check(I, "mismatched reference, whole BAM, output redirected as in the Skill (`> pileup.txt`): exit status non-zero", "rc=0" not in outx, f"{outx.strip()[-6:]} pileup.txt size={os.path.getsize(W + '/mism.txt')} bytes of rows with reference N")
shutil.copy(HREF, W + "/nofai.fa")
rc, out, err = sh(f"samtools mpileup -f {W}/nofai.fa -r chr22:3000-3001 {HUMAN}/test.paired_end.sorted.bam")
print("FASTA without .fai:", rc, out.strip()[:80], err.strip()[:150], os.path.exists(W + "/nofai.fa.fai"))
check(I, "reference without .fai: samtools builds it on the fly (so Skill's 'Reference must be indexed' is advice, not a hard requirement)", rc == 0 and os.path.exists(W + "/nofai.fa.fai"), f"rc={rc}, fai created={os.path.exists(W + '/nofai.fa.fai')}")
shutil.copy(HUMAN + "/test.paired_end.sorted.bam", W + "/noidx.bam")
rc, out, err = sh(f"samtools mpileup -f {HREF} -r chr22:3000-3001 {W}/noidx.bam")
print("BAM without .bai and -r:", rc, err.strip()[:200])
check(I, "-r on a BAM without index fails with a clear error", rc != 0 and ("index" in err.lower() or "fail" in err.lower()), f"rc={rc} {err.strip()[:150]!r}")
rc, out, err = sh(f"python -c \"import pysam;b=pysam.AlignmentFile('{W}/noidx.bam');list(b.pileup('chr22',2999,3001))\"")
print("pysam pileup without index:", rc, err.strip()[-160:])
check(I, "pysam pileup on an unindexed BAM raises (Skill 'What the Agent Will Do' step 1 says verify indexed)", rc != 0, err.strip()[-120:])

# ---------------- F. Windows-side reality for the Skill's pysam code (no wheel) : recorded, not executed
print("NOTE: pysam has no Windows wheel (TOOLS.md); all pysam snippets were executed in WSL science.")

# ---------------- G. multi-part: multiple BAMs, -b list, and depth per file cap
rc, out, err = sh(f"samtools mpileup -f {HREF} -r chr22:3000-3002 {HUMAN}/test.paired_end.sorted.bam {HUMAN}/test.paired_end.sorted.bam {HUMAN}/test.paired_end.sorted.bam")
r = mpileup_rows(out)
check(I, "three BAMs -> 3 + 3*3 = 12 columns", all(len(x) == 12 for x in r), Counter(len(x) for x in r))
summary(I)
