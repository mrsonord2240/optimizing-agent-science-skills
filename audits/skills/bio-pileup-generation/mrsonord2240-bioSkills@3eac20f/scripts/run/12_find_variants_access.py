#!/usr/bin/env python3
"""Input 10 (NEW, re-auditor 2): round-2 `find_variants` N handling, the restored Access Reads print, soft-masked reference, the shipped example
and `allele_counts`, on a planted BAM of my own (bundles of reads with exact depth/alt counts, hand-derived truth) plus real data
(1000G HG00349 chr20 slice, sarscov2 PE).  Independent method: decode of `samtools mpileup -B -Q 20` text with my own parser
(common.parse_bases) and, for the planted SNVs, `bcftools mpileup | bcftools call`."""
import ast, contextlib, io, os, random, re, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from snippets import load_functions, block_containing
import pysam

I = 10
funcs = load_functions("SKILL.md")
find_variants, allele_counts, allele_frequency = funcs["find_variants"], funcs["allele_counts"], funcs["allele_frequency"]
SC = AFDATA + "/sarscov2"

# ------------------------------------------------------------------ planted data
rng = random.Random(5150)
L = 1300
ref = [rng.choice("ACGT") for _ in range(L)]
for p in range(300, 305):
    ref[p - 1] = "N"                                    # reference N block (1-based 300-304)
for p in range(700, 761):
    ref[p - 1] = ref[p - 1].lower()                     # soft-masked block 700-760
refs = "".join(ref)
open(f"{DATA}/pv.fa", "w", newline="\n").write(">pv1\n" + "\n".join(refs[i:i + 60] for i in range(0, L, 60)) + "\n")
alt_of = lambda b: {"A": "G", "C": "T", "G": "A", "T": "C"}[b.upper()]
recs = []
truth = {}       # 1-based pos -> dict(ref, alt, depth (non-N, Q>=20), alt_count)


def bundle(name, site, depth, mods, qual=30, mapq=60, readlen=50):
    """`depth` reads all spanning `site` (1-based); mods = {read index: {pos: (base, qual, mapq_override)}}"""
    for k in range(depth):
        start = max(1, site - 5 - (k * 37) % 40)
        seq = list(refs[start - 1:start - 1 + readlen].upper().replace("N", "C"))
        ql = [qual] * readlen
        mq = mapq
        for pos, (b, q, m) in mods.get(k, {}).items():
            if start <= pos < start + readlen:
                seq[pos - start] = b
                if q is not None:
                    ql[pos - start] = q
                if m is not None:
                    mq = m
        rev = (k % 2 == 1)
        recs.append([f"{name}_{k}", 16 if rev else 0, "pv1", start, mq, f"{readlen}M", "*", 0, 0, "".join(seq), "".join(chr(33 + q) for q in ql)])


rb = lambda p: refs[p - 1].upper()
# 120: 8 of 20 alt (0.40)
bundle("s120", 120, 20, {k: {120: (alt_of(rb(120)), 30, None)} for k in range(8)}); truth[120] = dict(alt=alt_of(rb(120)), depth=20, alt_count=8)
# 220: depth 9, 5 alt -> below min_depth=10
bundle("s220", 220, 9, {k: {220: (alt_of(rb(220)), 30, None)} for k in range(5)})
# 300-304: reference N; reads carry real bases there (old code reported N>A ...)
bundle("s300", 302, 15, {k: {p: ("A", 30, None) for p in range(300, 305)} for k in range(15)})
# 420: read-base N in 3 of 20 reads, rest match: no variant (old code: ref>N at 15%)
bundle("s420", 420, 20, {k: {420: ("N", 30, None)} for k in range(3)})
# 520: 3 N + 2 alt of 20: non-N depth 17, alt 2/17 = 0.1176
bundle("s520", 520, 20, {**{k: {520: ("N", 30, None)} for k in range(3)}, **{k: {520: (alt_of(rb(520)), 30, None)} for k in range(3, 5)}}); truth[520] = dict(alt=alt_of(rb(520)), depth=17, alt_count=2)
# 620: exactly 2 of 20 = 0.10 -> reported (>=)
bundle("s620", 620, 20, {k: {620: (alt_of(rb(620)), 30, None)} for k in range(2)}); truth[620] = dict(alt=alt_of(rb(620)), depth=20, alt_count=2)
# 1050: 1 of 21 = 0.048 -> not reported (placed >= 100 bp from every other bundle so no neighbour read adds depth)
bundle("s1050", 1050, 21, {0: {1050: (alt_of(rb(1050)), 30, None)}})
# 720: soft-masked reference, 10 of 20 alt
bundle("s720", 720, 20, {k: {720: (alt_of(rb(720)), 30, None)} for k in range(10)}); truth[720] = dict(alt=alt_of(rb(720)), depth=20, alt_count=10)
# 820/821 adjacent SNVs in the same 10 reads
bundle("s820", 820, 20, {k: {820: (alt_of(rb(820)), 30, None), 821: (alt_of(rb(821)), 30, None)} for k in range(10)})
truth[820] = dict(alt=alt_of(rb(820)), depth=20, alt_count=10); truth[821] = dict(alt=alt_of(rb(821)), depth=20, alt_count=10)
# 900: 6 alt reads with base quality 10 (excluded at min_base_quality=20)
bundle("s900", 900, 20, {k: {900: (alt_of(rb(900)), 10, None)} for k in range(6)})
# 1000: 5 alt reads with MAPQ 0 (included by default, excluded with min_mapping_quality=1)
bundle("s1000", 1000, 20, {k: {1000: (alt_of(rb(1000)), 30, 0)} for k in range(5)})
truth_mq0 = dict(alt=alt_of(rb(1000)), depth=20, alt_count=5)
# 1150: SNV 10 of 20, used for region-edge tests
bundle("s1150", 1150, 20, {k: {1150: (alt_of(rb(1150)), 30, None)} for k in range(10)}); truth[1150] = dict(alt=alt_of(rb(1150)), depth=20, alt_count=10)
# 1250: a 2 bp insertion after 1250 in 10 reads (indel-only site: SNV finder must report nothing)
for k in range(20):
    start = 1250 - 20 - k % 5
    s_ = refs[start - 1:1250].upper()
    tail = refs[1250:1250 + 20].upper()
    if k < 10:
        cig, seq = f"{len(s_)}M2I20M", s_ + "GT" + tail
    else:
        cig, seq = f"{len(s_) + 20}M", s_ + tail
    recs.append([f"ins_{k}", 0 if k % 2 == 0 else 16, "pv1", start, 60, cig, "*", 0, 0, seq, "".join(chr(33 + 30) for _ in seq)])
with open(f"{DATA}/pv.sam", "w", newline="\n") as f:
    f.write("@HD\tVN:1.6\tSO:unsorted\n@SQ\tSN:pv1\tLN:1300\n")
    for r in recs:
        f.write("\t".join(map(str, r)) + "\n")
sh(f"cd {DATA} && samtools faidx pv.fa && samtools sort -o pv.bam pv.sam && rm pv.sam && samtools index pv.bam", check=True)
PV, PVREF = f"{DATA}/pv.bam", f"{DATA}/pv.fa"

# ---- independent decode of samtools mpileup -B -Q 20 -> the expected find_variants output
def decode_variants(bam, reff, chrom, start, end, min_depth=10, min_alt_freq=0.1, opts="-B -Q 20", drop_N_ref=True):
    mpd, rows, rc, err = mp_rows(reff, bam, opts, f"{chrom}:{start + 1}-{end}")
    out = []
    for (c, p), r in sorted(mpd.items(), key=lambda kv: kv[0][1]):
        if r[3] == "0" or (drop_N_ref and r[2].upper() == "N"):
            continue
        n, cnt = parse_bases(r[4], r[2])
        alle = Counter()
        for k, v in cnt.items():
            if k == "ref_fwd" or k == "ref_rev":
                alle[r[2].upper()] += v
            elif len(k) == 1 and k.isalpha() and k.upper() != "N":
                alle[k.upper()] += v
        tot = sum(alle.values())
        if tot < min_depth:
            continue
        for b, k in alle.items():
            if b != r[2].upper() and k / tot >= min_alt_freq:
                out.append((p, r[2].upper(), b, tot, k))
    return out


def fv_tuples(vs):
    return sorted((v["pos"], v["ref"], v["alt"], v["depth"], v["alt_count"]) for v in vs)


fv = find_variants(PV, PVREF, "pv1", 0, L)
exp_dec = sorted(decode_variants(PV, PVREF, "pv1", 0, L))
truth[1000] = truth_mq0   # min_mapping_quality defaults to 0: the 5 MAPQ-0 alt reads count
by_hand = sorted((p, rb(p), t["alt"], t["depth"], t["alt_count"]) for p, t in truth.items())
print("find_variants:", fv_tuples(fv)); print("decode of mpileup:", exp_dec); print("by hand:", by_hand)
check(I, "find_variants on the planted BAM == the planted truth (8 SNVs, exact depth and alt count): 120 (8/20), 520 (2/17 after 3 read-N dropped), 620 (exactly 0.10 kept), 720 (soft-masked ref), 820+821 (adjacent), 1000 (5 MAPQ-0 alt reads, default min_mapping_quality=0), 1150",
      fv_tuples(fv) == by_hand, f"got {fv_tuples(fv)}")
check(I, "find_variants == independent decode of samtools mpileup -B -Q 20 (own parser), same thresholds", fv_tuples(fv) == exp_dec, f"decode {exp_dec}")
nonSNV = [v for v in fv if v["pos"] in (220, 300, 301, 302, 303, 304, 420, 1050, 900, 1000, 1250)]
check(I, "no false calls at the negative sites: depth 9 (220), reference-N block (300-304), read-N only (420), 1/21 (1050), Q10 alt (900), MAPQ0 alt (1000 at default min_mapping_quality=0 is a TRUE call, see next), insertion-only site (1250)",
      not [v for v in nonSNV if v["pos"] != 1000] , [v for v in nonSNV if v["pos"] != 1000])
check(I, "no variant has ref or alt 'N' (round-2 claim: reference-N skipped, read-N not counted as an allele nor in the depth)", all("N" not in (v["ref"], v["alt"]) for v in fv), [v for v in fv if "N" in (v["ref"], v["alt"])])
check(I, "soft-masked reference: site 720 reported with an upper-case ref base", any(v["pos"] == 720 and v["ref"] == refs[719].upper() for v in fv), [v for v in fv if v["pos"] == 720])
fv0 = find_variants(PV, PVREF, "pv1", 0, L, min_base_quality=5)
check(I, "**pileup_kw honoured: min_base_quality=5 brings the Q10 alt site 900 back (6/20 = 0.30, depth 20)", any((v["pos"], v["depth"], v["alt_count"]) == (900, 20, 6) for v in fv0), [v for v in fv0 if v["pos"] == 900])
check(I, "default min_mapping_quality=0: MAPQ 0 reads carrying alt are counted (site 1000 reported 5/20); min_mapping_quality=1 drops them (site absent)",
      any((v["pos"], v["depth"], v["alt_count"]) == (1000, 20, 5) for v in fv) and not any(v["pos"] == 1000 for v in find_variants(PV, PVREF, "pv1", 0, L, min_mapping_quality=1)),
      [v for v in fv if v["pos"] == 1000])
# region edges (0-based half-open)
e1 = find_variants(PV, PVREF, "pv1", 1149, 1150)
e2 = find_variants(PV, PVREF, "pv1", 1150, 1151)
e3 = find_variants(PV, PVREF, "pv1", 819, 821)
check(I, "region edges (0-based [start,end), truncate=True): [1149,1150) -> the 1150 SNV only; [1150,1151) -> nothing; [819,821) -> 820 and 821", [v["pos"] for v in e1] == [1150] and e2 == [] and [v["pos"] for v in e3] == [820, 821], ([v["pos"] for v in e1], e2, [v["pos"] for v in e3]))
rc, out, err = sh(f"bcftools mpileup -B -Q 20 -a FORMAT/AD -f {PVREF} {PV} 2>/dev/null | bcftools call -mv 2>/dev/null | grep -v '^#' | cut -f2,4,5")
called = {int(l.split()[0]) for l in out.splitlines()}
print("bcftools call positions:", sorted(called))
check(I, "second method: bcftools mpileup | call -mv calls the strong planted SNVs (120, 720, 820, 821, 1150) and nothing in the reference-N block 300-304 or at the read-N site 420",
      {120, 720, 820, 821, 1150} <= called and not (called & {300, 301, 302, 303, 304, 420}), sorted(called))

# ---- allele_counts / allele_frequency on the same data (documented behaviour)
ac420 = allele_counts(PV, "pv1", 419)
ac1250 = allele_counts(PV, "pv1", 1249)
ac120 = allele_counts(PV, "pv1", 119)
print("allele_counts pv1:420", ac420, "| pv1:120", ac120, "| pv1:1250", ac1250)
check(I, "allele_counts at 120 = {ref:12, alt:8}; the insertion site 1250 counts no indel (documented 'SNVs only'): all 20 reads counted as the ref base", ac120 == {rb(120): 12, alt_of(rb(120)): 8} and sum(ac1250.values()) == 20 and len(ac1250) == 1, (ac120, ac1250))
print("NOTE allele_counts at 420 counts the read-base N as an allele:", ac420, "| allele_frequency:", allele_frequency(PV, "pv1", 419))

# ---- restored Access Reads snippet on a REAL position: (qname, strand, base) set == samtools --output-extra QNAME,FLAG decode
snip = block_containing("SKILL.md", "if pileup_read.is_refskip:\n                print('  Reference skip')")
BAMSE = DATA + "/sc_test.paired_end.sorted.bam"
SREF = SC + "/genome.fasta"
fvr = find_variants(BAMSE, SREF, "MT192765.1", 0, 29829, min_depth=2, min_alt_freq=0.3)
print("real sarscov2 PE find_variants(min_depth=2, min_alt_freq=0.3):", len(fvr), fvr[:2])
dec_r = sorted(decode_variants(BAMSE, SREF, "MT192765.1", 0, 29829, min_depth=2, min_alt_freq=0.3))
check(I, f"real sarscov2 PE (genome.fasta): find_variants == independent decode of mpileup -B -Q 20 over the whole genome ({len(fvr)} SNVs)", fv_tuples(fvr) == dec_r and len(fvr) > 0, (len(dec_r), fv_tuples(fvr)[:2], dec_r[:2]))
site = fvr[0]["pos"]
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(compile(snip.replace("input.bam", BAMSE).replace("'chr1', 1000000, 1000001", f"'MT192765.1', {site - 1}, {site}"), "<snip>", "exec"), {})
out = buf.getvalue()
got = Counter(re.findall(r"^  (\S+) ([+-]) ([ACGT]) \(Q(\d+)\)", out, flags=re.M))
got_set = {(a, b, c) for (a, b, c, d) in got}
rc, txt, _ = sh(f"samtools mpileup -B --output-extra QNAME,FLAG -f {SREF} -r MT192765.1:{site}-{site} {BAMSE}")
row = txt.strip().split("\t")
n, _c = parse_bases(row[4], row[2])
toks = []
i = 0
s5 = row[4]
while i < len(s5):
    ch = s5[i]
    if ch == "^":
        i += 2; continue
    if ch == "$":
        i += 1; continue
    if ch in "+-":
        m = re.match(r"[+-](\d+)", s5[i:]); i += len(m.group(0)) + int(m.group(1)); continue
    toks.append(ch); i += 1
names, flg = row[6].split(","), row[7].split(",")
exp_set = set()
for tk, nm, fl in zip(toks, names, flg):
    strand = "-" if int(fl) & 16 else "+"
    base = row[2].upper() if tk in ".," else tk.upper()
    exp_set.add((nm, strand, base))
print(f"Access Reads at MT192765.1:{site}: snippet {len(got_set)} reads, samtools {len(exp_set)}; first line: {out.splitlines()[0] if out else ''}")
check(I, f"restored Access Reads snippet at real MT192765.1:{site}: {len(exp_set)} (read name, strand, base) tuples == samtools mpileup --output-extra QNAME,FLAG decode; depth line equals column 4",
      got_set == exp_set and f"Depth: {row[3]}" in out and len(exp_set) >= 2, (len(got_set), len(exp_set), sorted(got_set ^ exp_set)[:3]))

# ---- real 1000G chr20 slice: find_variants vs decode
G1, GREF = AFDATA + "/1000g/HG00349.chr20_1400000-1500000.bam", AFDATA + "/1000g/chr20_padded_1500000.fa"
fvg = find_variants(G1, GREF, "chr20", 1400000, 1500000)
decg = sorted(decode_variants(G1, GREF, "chr20", 1400000, 1500000))
print("1000G find_variants:", len(fvg), "decode:", len(decg), fvg[:2])
check(I, f"real 1000G HG00349 chr20:1400001-1500000: find_variants == independent decode of mpileup -B -Q 20 ({len(decg)} SNVs at min_depth 10, alt >= 0.1)", fv_tuples(fvg) == decg and len(decg) > 0, (len(fvg), len(decg), sorted(set(fv_tuples(fvg)) ^ set(decg))[:3]))
# the round-1 code (before the N fix) is not available; instead confirm that reference-N positions occur in that real slice and are skipped
rc, txt, _ = sh(f"samtools mpileup -B -Q 20 -f {GREF} -r chr20:1400001-1400200 {G1} | awk '$3==\"N\"' | wc -l")
print("reference-N pileup rows in chr20:1400001-1400200 of the real slice:", txt.strip())

# ---- shipped example from the copy
EX = SKILL + "/examples/allele_counts.py"
rc, out, err = sh(f"cd {WORK} && python {EX} {PV} pv1:120")
check(I, "examples/allele_counts.py (copy) pv1:120 -> depth 20, ref 12 / alt 8", rc == 0 and "Total depth: 20" in out and f"{rb(120)}: 12" in out and f"{alt_of(rb(120))}: 8" in out, out.replace("\n", "|"))
rc, out, err = sh(f"cd {WORK} && python {EX} {PV} pv1:1000")
check(I, "example applies MAPQ >= 20: pv1:1000 counts the 15 reads with MAPQ 60 only (5 MAPQ-0 alt reads dropped)", "Total depth: 15" in out and alt_of(rb(1000)) not in out.replace("Position", ""), out.replace("\n", "|"))
rc, out, err = sh(f"cd {WORK} && python {EX} {SC}/test.paired_end.sorted.bam MT192765.1:100 2>&1; echo rc=$?")
check(I, "example on the UNINDEXED public sarscov2 BAM: one-line 'Error: ... has no index (run: samtools index ...)', no traceback", "no index" in out and "Traceback" not in out and len(out.strip().splitlines()) == 2, out.strip()[:200])
rc, out, err = sh(f"cd {WORK} && python {EX} {PV} pv1:100-200 2>&1; python {EX} {PV} nochr:5 2>&1; python {EX} {PV} pv1:0 2>&1")
check(I, "example: range, unknown contig and position 0 each give one 'Error:' line and no traceback", out.count("Error:") == 3 and "Traceback" not in out, out.strip().replace("\n", "|")[:300])
summary(I)
