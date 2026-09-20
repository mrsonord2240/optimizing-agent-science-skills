#!/usr/bin/env python3
"""Input 9 (NEW, re-auditor 2): the round-2 BAQ and --rf statements, re-derived on data the earlier auditors did not use.
  A. BAQ mapping table of SKILL.md ("BAQ is switched on by fastafile, not by the stepper"): pysam depth AND per-symbol base counts
     vs `samtools mpileup` default / -B / -E, position by position, under BOTH steppers, on
       real  : sarscov2 PE, sarscov2 SE, sarscov2 UMI-PE (vs genome.fasta), 1000G HG00349 chr20 slice with BQ tags added by `samtools calmd -r`
       own   : synthetic indel-near-mismatch BAM (no BQ tag), the same with calmd BQ tags, and with all-'@' BQ tags (BAQ reuse vs -E)
  B. `--rf` (samtools) vs pysam `flag_require` vs bcftools `--lu` / `--nu` / `--rf` on the real sarscov2 PE BAM: any-bit vs all-bit,
     against subsets built independently with pysam.
Every claim is asserted against an independent count; nothing is judged by exit code."""
import os, random, re, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import pysam

I = 9
SC = AFDATA + "/sarscov2"
KEEP = {"ref_fwd", "ref_rev", "*", "#", ">", "<"}


def sam_counts(ref, bam, opts="", region=""):
    mpd, rows, rc, err = mp_rows(ref, bam, opts, region)
    out = {}
    for (c, p), r in mpd.items():
        n, cnt = parse_bases(r[4], r[2]) if r[3] != "0" else (0, Counter())
        out[p] = (int(r[3]), Counter({k: v for k, v in cnt.items() if k in KEEP or (len(k) == 1 and k.isalpha())}))
    return out, rc, err


def py_counts(bam, ref, chrom, start, end, **kw):
    out = {}
    fa = pysam.FastaFile(ref)
    with pysam.AlignmentFile(bam) as b:
        if kw.pop("_fa", False):
            kw["fastafile"] = fa
        for col in b.pileup(chrom, start, end, truncate=True, **kw):
            rb = fa.fetch(chrom, col.pos, col.pos + 1).upper()
            cnt = Counter()
            for pr in col.pileups:
                a = pr.alignment
                rev = a.is_reverse
                if pr.is_refskip:
                    cnt["<" if rev else ">"] += 1
                elif pr.is_del:
                    cnt["*"] += 1
                else:
                    x = a.query_sequence[pr.query_position]
                    if x.upper() == rb:
                        cnt["ref_rev" if rev else "ref_fwd"] += 1
                    else:
                        cnt[x.lower() if rev else x.upper()] += 1
            out[col.pos + 1] = (len(col.pileups), cnt)
    return out


def ndiff(A, B, skipN=None):
    keys = set(A) | set(B)
    return sum(1 for k in keys if A.get(k, (0, Counter())) != B.get(k, (0, Counter())))


# ------------------------------------------------------------------ data
def make_baq_data():
    """own synthetic BAM: 40 bp reads over a 1,500 bp random reference, ~20x, 40% of reads carry a 1-3 bp indel, plus mismatches
    within 6 bp of the indel and mediocre base qualities (18-30): the situation where BAQ lowers qualities. Seeded."""
    rng = random.Random(9090)
    ref = "".join(rng.choice("ACGT") for _ in range(1500))
    open(f"{DATA}/baq.fa", "w", newline="\n").write(">bq1\n" + "\n".join(ref[i:i + 60] for i in range(0, 1500, 60)) + "\n")
    comp = {"A": "C", "C": "G", "G": "T", "T": "A"}
    recs = []
    for i in range(750):
        pos = rng.randrange(1, 1500 - 60)
        ops = []
        seq = []
        rp = pos
        a = rng.randrange(12, 24)
        kind = rng.random()
        ops.append((a, "M"))
        if kind < 0.2:
            n = rng.randrange(1, 4); ops.append((n, "I")); m = rng.randrange(12, 20); ops.append((m, "M"))
        elif kind < 0.4:
            n = rng.randrange(1, 4); ops.append((n, "D")); m = rng.randrange(12, 20); ops.append((m, "M"))
        else:
            ops.append((rng.randrange(12, 20), "M"))
        cs = ""
        for n, op in ops:
            cs += f"{n}{op}"
            if op == "M":
                for _ in range(n):
                    b = ref[rp - 1]
                    seq.append(comp[b] if rng.random() < 0.06 else b)   # 6% mismatches, dense enough to sit near indels
                    rp += 1
            elif op == "D":
                rp += n
            else:
                seq.extend(rng.choice("ACGT") for _ in range(n))
        qual = "".join(chr(33 + rng.randrange(18, 31)) for _ in seq)
        rev = rng.random() < 0.5
        recs.append([f"b{i}", 16 if rev else 0, "bq1", pos, 60, cs, "*", 0, 0, "".join(seq), qual])
    with open(f"{DATA}/baq.sam", "w", newline="\n") as f:
        f.write("@HD\tVN:1.6\tSO:unsorted\n@SQ\tSN:bq1\tLN:1500\n")
        for r in recs:
            f.write("\t".join(map(str, r)) + "\n")
    sh(f"cd {DATA} && samtools faidx baq.fa && samtools sort -o baq.bam baq.sam && rm baq.sam && samtools index baq.bam", check=True)
    # BQ tags from samtools calmd -r (computed), and an all-'@' variant (BQ = 64 -> no quality reduction)
    sh(f"cd {DATA} && samtools calmd -r -b baq.bam baq.fa > baq_bq.bam 2>/dev/null && samtools index baq_bq.bam", check=True)
    with pysam.AlignmentFile(f"{DATA}/baq.bam") as src, pysam.AlignmentFile(f"{DATA}/baq_zero.bam", "wb", template=src) as dst:
        for a in src.fetch():
            a.set_tag("BQ", "@" * len(a.query_sequence), "Z")
            dst.write(a)
    pysam.index(f"{DATA}/baq_zero.bam")
    # real 1000G slice with computed BQ tags
    sh(f"cd {DATA} && samtools calmd -r -b {AFDATA}/1000g/HG00349.chr20_1400000-1500000.bam {AFDATA}/1000g/chr20_padded_1500000.fa > g1k_bq.bam 2>/dev/null && samtools index g1k_bq.bam", check=True)


make_baq_data()
# public-data\ must stay untouched and the sarscov2 BAMs there are unindexed: work on indexed copies
for nm in ("test.paired_end.sorted.bam", "test.single_end.sorted.bam", "test.paired_end.umi.sorted.bam"):
    sh(f"cp {SC}/{nm} {DATA}/sc_{nm} && samtools index {DATA}/sc_{nm}", check=True)
SCB = lambda nm: f"{DATA}/sc_{nm}"
for f in ("baq_bq.bam", "baq_zero.bam", "g1k_bq.bam"):
    rc, out, _ = sh(f"samtools view {DATA}/{f} | grep -c 'BQ:Z'")
    print(f"{f}: reads with a BQ tag = {out.strip()}")

DS = [  # name, bam, ref, contig, start, end (0-based half open), note
    ("real sarscov2 PE", SCB("test.paired_end.sorted.bam"), SC + "/genome.fasta", "MT192765.1", 0, 29829),
    ("real sarscov2 SE", SCB("test.single_end.sorted.bam"), SC + "/genome.fasta", "MT192765.1", 0, 29829),
    ("real sarscov2 UMI-PE", SCB("test.paired_end.umi.sorted.bam"), SC + "/genome.fasta", "MT192765.1", 0, 29829),
    ("real 1000G + calmd BQ tags", f"{DATA}/g1k_bq.bam", AFDATA + "/1000g/chr20_padded_1500000.fa", "chr20", 1400000, 1500000),
    ("own indel-dense, no BQ tag", f"{DATA}/baq.bam", f"{DATA}/baq.fa", "bq1", 0, 1500),
    ("own + calmd BQ tags", f"{DATA}/baq_bq.bam", f"{DATA}/baq.fa", "bq1", 0, 1500),
    ("own + all-'@' BQ tags", f"{DATA}/baq_zero.bam", f"{DATA}/baq.fa", "bq1", 0, 1500),
]
# mapping: (samtools opts, label, list of (pysam label, kwargs))
MAP = [
    ("", "default (-f)", [("fastafile", dict(_fa=True))]),
    ("-B", "-B", [("no fastafile", {}), ("fastafile + compute_baq=False", dict(_fa=True, compute_baq=False))]),
    ("-E", "-E", [("fastafile + redo_baq=True", dict(_fa=True, redo_baq=True))]),
]
disc = {}
ALLRES = {}
for name, bam, ref, c, s, e in DS:
    reg = f"{c}:{s + 1}-{e}"
    S = {}
    for so, lab, _ in MAP:
        S[lab], rc, err = sam_counts(ref, bam, so, reg)
    tot = {lab: sum(v[0] for v in S[lab].values()) for lab in S}
    d_defB, d_defE, d_BE = ndiff(S["default (-f)"], S["-B"]), ndiff(S["default (-f)"], S["-E"]), ndiff(S["-B"], S["-E"])
    disc[name] = (d_defB, d_defE, d_BE)
    print(f"{name}: positions {len(S['default (-f)'])}; samtools default vs -B differ at {d_defB}, default vs -E {d_defE}, -B vs -E {d_BE}; depth sums {tot}")
    # steppers: None = no stepper argument (pysam 0.24.1's real default), 'samtools', 'all' (the Skill calls this "the default")
    res = {}
    for stepper in (None, "samtools", "all"):
        bad, n_maps = [], 0
        for so, lab, pys in MAP:
            for plab, kw in pys:
                n_maps += 1
                skw = {} if stepper is None else {"stepper": stepper}
                P = py_counts(bam, ref, c, s, e, **skw, **dict(kw))
                nd = ndiff(S[lab], P)
                if nd:
                    bad.append((lab, plab, nd))
        res[stepper] = (bad, n_maps)
        ALLRES.setdefault(stepper, []).append((name, bad))
    for stepper in (None, "samtools"):
        bad, n_maps = res[stepper]
        check(I, f"BAQ table on {name}, stepper={'(no argument)' if stepper is None else stepper}: {n_maps} (mpileup option, pysam arguments) mappings equal samtools in depth and per-symbol counts at every position", not bad, bad[:4])
# discrimination: the comparison must be able to fail
check(I, "discrimination: default != -B on the own indel-dense BAM and on real 1000G+BQ (else the BAQ mapping test proves nothing)",
      disc["own indel-dense, no BQ tag"][0] > 0, disc)
check(I, "discrimination: with all-'@' BQ tags samtools default == -B (tag reused) but -E differs (recomputed): pysam fastafile == default, redo_baq == -E",
      disc["own + all-'@' BQ tags"][0] == 0 and disc["own + all-'@' BQ tags"][1] > 0, disc["own + all-'@' BQ tags"])

# ---- SKILL.md statement under test: "With fastafile BAQ is applied under either stepper ('all', the default, or 'samtools')"; table row `-f` note "either stepper"
allbad = [(n, b) for n, b in ALLRES["all"] if b]
print("stepper='all' mismatches per dataset:", [(n, [(x[0], x[1], x[2]) for x in b][:3]) for n, b in ALLRES["all"]])
# BAQ-specific: on single-end data (no overlap/orphan effects) stepper='all' + fastafile must equal mpileup default if the claim is true
se_all = dict(ALLRES["all"])
check(I, "SKILL claim 'BAQ applied under either stepper': fastafile + stepper='all' equals `samtools mpileup -f` (BAQ on) on the single-end datasets (own baq.bam, sarscov2 SE) -- no overlap/orphan effects can explain a difference",
      not any(x[0] == "default (-f)" for x in se_all["own indel-dense, no BQ tag"]) and not any(x[0] == "default (-f)" for x in se_all["real sarscov2 SE"]),
      {"own": [x for x in se_all["own indel-dense, no BQ tag"] if x[0] == "default (-f)"], "sc SE": [x for x in se_all["real sarscov2 SE"] if x[0] == "default (-f)"]})
check(I, "SKILL claim \"stepper 'all' is the default\": the pysam call with NO stepper argument behaves like stepper='all' on every dataset (it does not: it equals 'samtools')",
      all(dict(ALLRES[None])[n] == dict(ALLRES["all"])[n] for n, *_ in DS),
      "no-arg == 'samtools' on all datasets: " + str(all(dict(ALLRES[None])[n] == dict(ALLRES["samtools"])[n] for n, *_ in DS)) + "; 'all' differs from the no-arg call on: " + ", ".join(n for n, b in ALLRES["all"] if b))

# ---- -B and -E cannot be combined
rc, out, err = sh(f"samtools mpileup -B -E -f {DATA}/baq.fa {DATA}/baq.bam")
check(I, "SKILL: `-B` and `-E` cannot be combined (samtools rejects the pair, prints nothing)", rc != 0 and out.strip() == "", f"rc={rc} stderr={err.strip()[:100]!r}")

# ------------------------------------------------------------------ B: --rf
PE, REF = SCB("test.paired_end.sorted.bam"), SC + "/genome.fasta"
flags = Counter(a.flag for a in pysam.AlignmentFile(PE))
print("flags in sarscov2 PE BAM:", dict(flags))


def bcf_dp(bam, extra):
    rc, out, err = sh(f"bcftools mpileup -f {REF} -A -B -Q 0 -q 0 -d 1000000 {extra} {bam} | bcftools query -f '%POS\\t%INFO/DP\\n'")
    return {int(a): int(b) for a, b in (ln.split("\t") for ln in out.splitlines() if ln.strip())}, err


def subset(mask, allbits):
    p = f"{WORK}/sub_{mask}_{'all' if allbits else 'any'}.bam"
    n = 0
    with pysam.AlignmentFile(PE) as src, pysam.AlignmentFile(p, "wb", template=src) as dst:
        for a in src:
            if (a.flag & mask) == mask if allbits else (a.flag & mask) != 0:
                dst.write(a); n += 1
    pysam.index(p)
    return p, n


BASE, _ = bcf_dp(PE, "")
print("bcftools unfiltered DP sum", sum(BASE.values()))
for mask in (16, 64, 128, 65, 99, 3):
    pa, na = subset(mask, False)
    pl, nl = subset(mask, True)
    A, _ = bcf_dp(pa, "")
    L, _ = bcf_dp(pl, "")
    lu, _ = bcf_dp(PE, f"--lu {mask}")
    nu, _ = bcf_dp(PE, f"--nu {mask}")
    rfb, _ = bcf_dp(PE, f"--rf {mask}")
    print(f"mask {mask}: any-bit subset {na} reads (DP sum {sum(A.values())}), all-bit subset {nl} reads (DP sum {sum(L.values())}); bcftools --lu {sum(lu.values())} --nu {sum(nu.values())} --rf {sum(rfb.values())}")
    check(I, f"bcftools --lu {mask} == any-bit subset (independent pysam subset), per position; --nu {mask} == all-bit subset; bcftools --rf {mask} == --lu {mask}",
          lu == A and nu == L and rfb == lu, f"sums lu={sum(lu.values())} any={sum(A.values())} nu={sum(nu.values())} all={sum(L.values())} rf={sum(rfb.values())}")
    # samtools --rf vs pysam flag_require, depth + counts
    S, rc, _ = sam_counts(REF, PE, f"-B --rf {mask}", "")
    P = py_counts(PE, REF, "MT192765.1", 0, 29829, flag_require=mask)
    check(I, f"samtools mpileup --rf {mask} == pysam flag_require={mask} (depth and per-symbol counts, {len(S)} positions)", ndiff(S, P) == 0, f"differing {ndiff(S, P)}")
    # samtools --rf equals the any-bit subset (mpileup -B on the subset with default flags)
    S2, _, _ = sam_counts(REF, pa, "-B", "")
    check(I, f"samtools --rf {mask} == plain mpileup of the independent any-bit subset (any-bit semantics)", ndiff(S, S2) == 0, f"differing {ndiff(S, S2)}")
    if mask in (65, 99, 3):
        check(I, f"discrimination for mask {mask}: any-bit and all-bit subsets differ ({na} vs {nl} reads), so the row's `--nu` warning is non-trivial", na != nl, (na, nl))
summary(I)
