#!/usr/bin/env python3
"""Input 5 (Stress, REGRESSION of pre-fix input 5, REAL data only): the library-typed flag cheat sheet on the real ARTIC nanopore BAM,
the real spliced RNA-seq BAM and the 1000G germline BAM, plus the reference-mismatch / index / region errors the fixed 'Common Errors'
table quotes. Depths are checked against independent pysam-record counts; message texts against real tool output."""
import os, re, shutil, sys, time
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from snippets import load_functions
import pysam

I = 5
P = AFDATA
ART0 = P + "/sarscov2/sars-cov-2_v5.3.2.nanopore.bam"; ARTREF = P + "/sarscov2/MN908947.3.fasta"
ILLREF = P + "/sarscov2/genome.fasta"           # MT192765.1: does NOT hold the ARTIC contig
RNA0 = HUMAN + "/test.rna.paired_end.sorted.bam"
G1K = P + "/1000g/HG00349.chr20_1400000-1500000.bam"; G1KREF = P + "/1000g/chr20_padded_1500000.fa"
W = WORK + "/t05"; os.makedirs(W, exist_ok=True)
SK = open(SKILL + "/SKILL.md", encoding="utf-8").read()
for src, name in ((ART0, "artic.bam"), (RNA0, "rna.bam")):     # public-data is read-only: index copies
    shutil.copy(src, W + "/" + name)
    sh(f"samtools index {W}/{name}", check=True)
ART, RNA = W + "/artic.bam", W + "/rna.bam"


def expected_depth(bam, contig, min_q=0, min_mq=0, count_del=True):
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


# A. cheat-sheet rows: extracted from the SKILL.md table (not retyped), every one run on the real human slice
tab = re.findall(r"^\| ([^|]+) \| `([^`]+)`[^|]*\|$", SK[SK.index("### Library-Typed Flags Cheat Sheet"):SK.index("## Variant Calling Pipeline")], flags=re.M)
tab = [(a.strip(), b) for a, b in tab if a.strip() not in ("Library",)]
print("cheat-sheet rows read from SKILL.md:", tab)
check(I, "cheat sheet has the 8 library rows and no row caps depth at 250 (`-d 250` absent)", len(tab) == 8 and not any("-d 250" in f for _, f in tab), [(a, f) for a, f in tab])
for label, fl in tab:
    rc, out, err = sh(f"samtools mpileup -f {HREF} {fl} -r chr22:1952-4617 {HBAM}")
    n = len(mpileup_rows(out))
    check(I, f"cheat-sheet row '{label}': `{fl}` accepted, produces rows", rc == 0 and n > 1000 and "invalid" not in err.lower(), f"rc={rc} rows={n}")
rc, out, err = sh(f"bcftools mpileup -f {HREF} -q 30 -Q 0 -B -d 0 --max-BQ 30 -r chr22:3000 {HBAM} | tail -1 | cut -f1-2")
check(I, "ONT row for bcftools (`-q 30 -Q 0 -B -d 0 --max-BQ 30`) is accepted", rc == 0 and out.startswith("chr22"), (out + err).strip()[:80])

# B. ARTIC
t = time.time()
rc, out, err = sh(f"samtools mpileup -f {ARTREF} -aa -A -d 600000 -B -Q 20 {ART}")
rows = mpileup_rows(out)
check(I, "ARTIC row: 29903 rows (one per genome position), MN908947.3", len(rows) == 29903 and rows[0][1] == "1" and rows[-1][1] == "29903", f"{len(rows)} rows in {time.time() - t:.1f}s")
exp = expected_depth(ART, "MN908947.3", min_q=20, count_del=False)
diff = [(int(r[1]), int(r[3]), exp.get(int(r[1]), 0)) for r in rows if int(r[3]) - (parse_bases(r[4], r[2])[1]["*"] if r[3] != "0" else 0) != exp.get(int(r[1]), 0)]
check(I, "ARTIC depth (minus '*' slots) == independent pysam count of aligned bases with baseQ>=20 at all 29903 positions", not diff, f"{len(diff)} differ {diff[:3]}")
zeros = sum(1 for r in rows if r[3] == "0")
rows_a = mpileup_rows(sh(f"samtools mpileup -f {ARTREF} -a -A -d 600000 -B -Q 20 {ART}")[1])
rows_n = mpileup_rows(sh(f"samtools mpileup -f {ARTREF} -A -d 600000 -B -Q 20 {ART}")[1])
check(I, "Options table: `-a` = `-aa` for a single-contig reference (29903 rows either way); without -a/-aa the zero-depth positions vanish", len(rows_a) == 29903 and len(rows_n) == 29903 - zeros and zeros > 0, f"-a {len(rows_a)}, none {len(rows_n)}, zero-depth {zeros}")
rc, out, err = sh(f"samtools mpileup -f {ARTREF} -q 30 -Q 0 -B -d 0 {ART}")
expq = expected_depth(ART, "MN908947.3", min_q=0, min_mq=30)
mr = {int(r[1]): int(r[3]) for r in mpileup_rows(out)}
check(I, "ONT row `-q 30 -Q 0 -B -d 0` depth == independent count of MAPQ>=30 reads at every position", all(mr.get(p, 0) == expq[p] for p in expq) and mr, f"positions with data {len(mr)}")
# -A on the amplicon data: are there paired-not-proper reads? nanopore: no. record only.

# C. real RNA-seq with the fixed helpers
rc, out, err = sh(f"samtools mpileup -f {HREF} -q 20 -Q 20 -B -d 0 {RNA}")
rr = mpileup_rows(out)
cnt = [(parse_bases(r[4], r[2])[1], r) for r in rr]
gt = sum(c[">"] for c, _ in cnt); lt = sum(c["<"] for c, _ in cnt); star = sum(c["*"] for c, _ in cnt)
print(f"RNA-seq mpileup: '>' {gt} '<' {lt} '*' {star} rows {len(rr)}")
check(I, "RNA-seq row: '>' / '<' present (Skill table)", gt > 0 and lt > 0)
skill = load_functions("SKILL.md"); ac = skill["allele_counts"]
top = sorted(cnt, key=lambda x: -(x[0][">"] + x[0]["<"]))[:40]
bad = []
for c, r in top:
    p = int(r[1])
    got = ac(RNA, "chr22", p - 1, min_mapping_quality=20, min_base_quality=20)
    want = Counter()
    for k, v in c.items():
        if len(k) == 1 and k.upper() in "ACGT":
            want[k.upper()] += v
    want[r[2].upper()] += c["ref_fwd"] + c["ref_rev"]
    want["DEL"] += c["*"] + c["#"]
    want = {k: v for k, v in want.items() if v}
    if got != want:
        bad.append((p, got, want))
print("40 positions with the most ref-skips: allele_counts vs mpileup -B parse; mismatches:", bad[:3])
check(I, "allele_counts at the 40 real intron positions with most ref-skips == mpileup -B -q20 -Q20 parse; 'DEL' equals real '*' only (was DEL=54 at chr22:25548 pre-fix)", not bad, bad[:2])
best = top[0]
p = int(best[1][1]); got = ac(RNA, "chr22", p - 1, min_mapping_quality=20, min_base_quality=20)
print("top ref-skip position", p, best[0][">"], best[0]["<"], "| allele_counts", got)
# whole-BAM no DEL inflation
tot_del_skill = tot_del_mp = 0
for c, r in cnt[::20]:
    tot_del_mp += c["*"]
    tot_del_skill += ac(RNA, "chr22", int(r[1]) - 1, min_mapping_quality=20, min_base_quality=20).get("DEL", 0)
check(I, "DEL counts summed over 1/20 of all RNA-seq positions: allele_counts == mpileup '*' total", tot_del_skill == tot_del_mp, f"{tot_del_skill} vs {tot_del_mp}")

# D. 1000G
rc, out, err = sh(f"samtools mpileup -f {G1KREF} -q 20 -Q 20 -d 0 -r chr20:1400001-1500000 {G1K}")
g = mpileup_rows(out)
ref = pysam.FastaFile(G1KREF)
check(I, "1000G germline row: rows and ref column == FASTA", len(g) > 1000 and all(ref.fetch("chr20", int(r[1]) - 1, int(r[1])).upper() == r[2] for r in g[:2000]), f"{len(g)} rows")
o1 = mpileup_rows(sh(f"samtools mpileup -f {G1KREF} -B -x -A -Q 0 -q 0 -d 0 -r chr20:1400001-1500000 {G1K}")[1])
o2 = mpileup_rows(sh(f"samtools mpileup -f {G1KREF} -B -x -A -Q 0 -q 0 -d 0 --ff 0 -r chr20:1400001-1500000 {G1K}")[1])
d1, d2 = sum(int(r[3]) for r in o1), sum(int(r[3]) for r in o2)
exp = expected_depth(G1K, "chr20", min_q=0)
mr = {int(r[1]): int(r[3]) for r in o1}
check(I, "1000G: all-filters-off depth == independent pysam count at every position", all(mr[p] == exp.get(p, 0) for p in mr))
check(I, "Options table: default --ff drops pre-flagged duplicates (Skill: 'Pre-flagged duplicates vanish from depth'): sum depth --ff 0 > default", d2 > d1, f"{d1} -> {d2}")
# E. errors (real messages)
rc, out, err = sh(f"samtools mpileup -f {ILLREF} -r MN908947.3:100-110 {ART}")
rows_m = mpileup_rows(out)
check(I, "Common Errors row 1: reference lacks the contig -> '[E::faidx_adjust_position] The sequence \"MN908947.3\" was not found', EXIT STATUS 0, rows with reference N",
      rc == 0 and '[E::faidx_adjust_position] The sequence "MN908947.3" was not found' in err and rows_m and all(r[2] == "N" for r in rows_m) and "exit status 0" in SK, f"rc={rc} rows={len(rows_m)} err={err.strip()[:100]!r}")
rc, o, e = sh(f"cd {W}; samtools view -H artic.bam | grep '^@SQ' | cut -f2 | sed 's/SN://' > bam_contigs.txt; cut -f1 {ILLREF}.fai > ref_contigs.txt; comm -23 <(sort bam_contigs.txt) <(sort ref_contigs.txt)")
check(I, "Skill's contig pre-check (`samtools view -H | grep '^@SQ'` vs `cut -f1 ref.fa.fai`) detects the mismatch: BAM contig MN908947.3 missing from reference", o.strip() == "MN908947.3", o.strip())
check(I, "Common Errors row 2: samtools mpileup without -f -> reference column N, rc 0; bcftools refuses", mpileup_rows(sh(f"samtools mpileup -r MN908947.3:100-101 {ART}")[1])[0][2] == "N" and "requires the --fasta-ref option" in sh(f"bcftools mpileup -r MN908947.3:100 {ART} 2>&1 | head -2")[1])
shutil.copy(HBAM, W + "/noidx.bam")
rc, out, err = sh(f"samtools mpileup -f {HREF} -r chr22:3000-3001 {W}/noidx.bam")
check(I, "Common Errors row 4: '[E::idx_find_and_load] Could not retrieve index file for' on an unindexed BAM with -r", rc != 0 and "[E::idx_find_and_load] Could not retrieve index file for" in err and "[E::idx_find_and_load] Could not retrieve index file for" in SK, err.strip()[:150])
rc, out, err = sh(f"python -c \"import pysam;b=pysam.AlignmentFile('{W}/noidx.bam');list(b.pileup('chr22',2999,3001))\"")
check(I, "pysam pileup on unindexed BAM raises (Skill: BAM must be indexed for bam.pileup())", rc != 0 and "index" in err.lower(), err.strip()[-100:])
rc, out, err = sh(f"samtools view {HBAM} chr22:16570000-16590000 | head -2; samtools mpileup -f {HREF} -r chr22:16570000-16590000 {HBAM}")
check(I, "Common Errors 'Empty output | Region has no reads': the check `samtools view in.bam region | head` returns nothing and mpileup prints nothing", out.strip() == "", out.strip()[:50])
shutil.copy(HREF, W + "/nofai.fa")
rc, out, err = sh(f"samtools mpileup -f {W}/nofai.fa -r chr22:3000-3001 {HBAM}")
print("FASTA without .fai:", rc, os.path.exists(W + "/nofai.fa.fai"))
check(I, "Version Compatibility: 'The reference must be indexed' — samtools builds a missing .fai itself (advice, not a hard requirement); statement stays true for pysam.FastaFile", rc == 0 and os.path.exists(W + "/nofai.fa.fai"))
r = mpileup_rows(sh(f"samtools mpileup -f {HREF} -r chr22:3000-3002 {HBAM} {HBAM} {HBAM}")[1])
check(I, "three BAMs -> 3 + 3*3 = 12 columns", all(len(x) == 12 for x in r))
sh(f"rm -rf {W}")
summary(I)
