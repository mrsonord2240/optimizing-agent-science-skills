#!/usr/bin/env python3
"""(Re-used UNCHANGED from the pre-fix audit as regression data.) SYNTHETIC planted-truth data for the bio-pileup-generation audit (nothing here is real data).

Writes into run/data/:
  syn.fa(.fai)      reference: synA (1000 bp random, seed 42), synB (500 bp, NO reads), synC (300 bp, reads only 1-50)
  syn.sam -> syn.bam   planted reads on synA/synC (see TRUTH below), sorted+indexed
  truth.json           the planted design (positions are 1-based) plus per-read specs used by 01_truth_pileup.py
  deep.fa / deep.bam   synD 100 bp, 9000 identical reads at pos 1 (max-depth test)
  multi.fa / multi.bam 11 contigs chr1..chr11 (200 bp), each with 12 reads incl. a 6/12 SNP at pos 100 (parallel-loop test)
  s1.bam / s2.bam      two samples (RG SM:s1 / SM:s2) on synA with different SNP fractions at pos 100 (multi-sample test)
Everything is deterministic (seeded).
"""
import json, os, random, subprocess, sys

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(OUT, exist_ok=True)
rng = random.Random(42)


def rand_seq(n):
    return "".join(rng.choice("ACGT") for _ in range(n))


def alt_of(b):
    return {"A": "G", "C": "T", "G": "A", "T": "C"}[b]


def write_fa(path, contigs):
    with open(path, "w", newline="\n") as f:
        for name, seq in contigs.items():
            f.write(f">{name}\n")
            for i in range(0, len(seq), 60):
                f.write(seq[i:i + 60] + "\n")


refs = {"synA": rand_seq(1000), "synB": rand_seq(500), "synC": rand_seq(300)}
write_fa(os.path.join(OUT, "syn.fa"), refs)
A = refs["synA"]

records = []  # dicts: name, flag, ref, pos, mapq, cigar, seq, qual, rnext, pnext, tlen, tags
truth = {"notes": "1-based positions; ref bases from syn.fa", "events": {}}


def ref_slice(ref, pos, n):  # 1-based start
    return refs[ref][pos - 1:pos - 1 + n]


def add(name, flag, ref, pos, cigar, seq, qual=None, mapq=60, rnext="*", pnext=0, tlen=0, rg=None):
    if qual is None:
        qual = "I" * len(seq)  # Q40
    records.append(dict(name=name, flag=flag, ref=ref, pos=pos, mapq=mapq, cigar=cigar, seq=seq, qual=qual,
                        rnext=rnext, pnext=pnext, tlen=tlen, rg=rg))


def subst(seq, idx0, base=None):
    s = list(seq)
    s[idx0] = base or alt_of(s[idx0])
    return "".join(s)


# --- 1. SNP at synA:100 : 20 fwd + 20 rev reads 81..130; alt in 6 fwd + 4 rev  => ref 30 / alt 10
snp_pos = 100
snp_ref = A[snp_pos - 1]
snp_alt = alt_of(snp_ref)
for i in range(20):
    seq = ref_slice("synA", 81, 50)
    if i < 6:
        seq = subst(seq, snp_pos - 81, snp_alt)
    add(f"snpF{i}", 0, "synA", 81, "50M", seq)
for i in range(20):
    seq = ref_slice("synA", 81, 50)
    if i < 4:
        seq = subst(seq, snp_pos - 81, snp_alt)
    add(f"snpR{i}", 16, "synA", 81, "50M", seq)
truth["events"]["snp"] = dict(pos=snp_pos, ref=snp_ref, alt=snp_alt, ref_fwd=14, ref_rev=16, alt_fwd=6, alt_rev=4, depth=40)

# --- 2. Insertion after synA:200 : reads start 171, 30M2I18M ; 5 ins reads (3F 2R) + 5 plain reads
ins_seq2 = "AC"
for i in range(5):
    flag = 0 if i < 3 else 16
    base = ref_slice("synA", 171, 30) + ins_seq2 + ref_slice("synA", 201, 18)
    add(f"insR{i}", flag, "synA", 171, "30M2I18M", base)
for i in range(5):
    add(f"insN{i}", 0, "synA", 171, "50M", ref_slice("synA", 171, 50))
truth["events"]["ins"] = dict(after_pos=200, seq="AC", n_ins_reads=5, n_ins_fwd=3, n_ins_rev=2, depth_at_200=10)

# --- 3. Deletion synA:251-253 : reads start 221, 30M3D20M ; 4 del reads (2F 2R) + 4 plain reads
for i in range(4):
    flag = 0 if i < 2 else 16
    seq = ref_slice("synA", 221, 30) + ref_slice("synA", 254, 20)
    add(f"delR{i}", flag, "synA", 221, "30M3D20M", seq)
for i in range(4):
    add(f"delN{i}", 0, "synA", 221, "50M", ref_slice("synA", 221, 50))
truth["events"]["del"] = dict(first_deleted=251, last_deleted=253, deleted_seq=ref_slice("synA", 251, 3),
                              n_del_reads=4, n_del_fwd=2, n_del_rev=2, depth_at_250=8, depth_at_251=8)

# --- 4. Splice : reads start 301, 25M200N25M ; 3 reads (2F 1R); pos 326..525 are ref-skips
for i in range(3):
    flag = 0 if i < 2 else 16
    seq = ref_slice("synA", 301, 25) + ref_slice("synA", 526, 25)
    add(f"spl{i}", flag, "synA", 301, "25M200N25M", seq)
truth["events"]["splice"] = dict(skip_first=326, skip_last=525, n_fwd=2, n_rev=1)

# --- 5. Low MAPQ: 5 reads MAPQ 5 + 5 reads MAPQ 60 at 601..650
for i in range(5):
    add(f"lowmq{i}", 0, "synA", 601, "50M", ref_slice("synA", 601, 50), mapq=5)
for i in range(5):
    add(f"okmq{i}", 0, "synA", 601, "50M", ref_slice("synA", 601, 50), mapq=60)
truth["events"]["mapq"] = dict(region="601-650", low_mapq_reads=5, ok_reads=5)

# --- 6. Low base quality at synA:725 : 10 reads at 701..750, 6 of them carry an alt base at Q5 (all others Q40)
bq_pos = 725
bq_ref = A[bq_pos - 1]
bq_alt = alt_of(bq_ref)
for i in range(10):
    seq = ref_slice("synA", 701, 50)
    qual = "I" * 50
    if i < 6:
        seq = subst(seq, bq_pos - 701, bq_alt)
        qual = qual[:bq_pos - 701] + "&" + qual[bq_pos - 701 + 1:]  # '&' = Q5
    add(f"lowbq{i}", 0 if i % 2 == 0 else 16, "synA", 701, "50M", seq, qual)
truth["events"]["lowbq"] = dict(pos=bq_pos, ref=bq_ref, alt=bq_alt, n_low_q_alt=6, n_ref_q40=4, depth=10)

# --- 7. Flag filters at 801..850: 10 normal, 3 DUP(1024), 2 SECONDARY(256), 1 QCFAIL(512), 2 UNMAPPED(4)
for i in range(10):
    add(f"flgN{i}", 0, "synA", 801, "50M", ref_slice("synA", 801, 50))
for i in range(3):
    add(f"flgDup{i}", 1024, "synA", 801, "50M", ref_slice("synA", 801, 50))
for i in range(2):
    add(f"flgSec{i}", 256, "synA", 801, "50M", ref_slice("synA", 801, 50))
add("flgQc0", 512, "synA", 801, "50M", ref_slice("synA", 801, 50))
for i in range(2):
    add(f"flgUn{i}", 4, "synA", 801, "*", ref_slice("synA", 801, 50), mapq=0)
truth["events"]["flags"] = dict(region="801-850", default_depth=10, with_ff0_depth=16, note="unmapped never piled up")

# --- 8. Overlapping proper pairs (5 pairs): R1 901..950 fwd (99), R2 921..970 rev (147); overlap 921..950;
#        at 930 R2 carries an alt base (conflict) with Q40 too. Default: overlap removal -> depth 5 at 930; -x -> 10.
ov_pos = 930
ov_ref = A[ov_pos - 1]
ov_alt = alt_of(ov_ref)
for i in range(5):
    r1 = ref_slice("synA", 901, 50)
    r2 = subst(ref_slice("synA", 921, 50), ov_pos - 921, ov_alt)
    add(f"pair{i}", 99, "synA", 901, "50M", r1, rnext="=", pnext=921, tlen=70)
    add(f"pair{i}", 147, "synA", 921, "50M", r2, rnext="=", pnext=901, tlen=-70)
truth["events"]["overlap"] = dict(pos=ov_pos, ref=ov_ref, alt=ov_alt, pairs=5, depth_with_x=10, depth_default=5)

# --- 9. Orphans: 4 reads flag 65 (paired, first, mate mapped, NOT proper) at 971..1000 (30M) on synA
for i in range(4):
    add(f"orph{i}", 65, "synA", 971, "30M", ref_slice("synA", 971, 30), rnext="=", pnext=100, tlen=0)
truth["events"]["orphan"] = dict(region="971-1000", default_depth=0, with_A_depth=4)

# --- 10. Soft-clipped reads at 401..445 (5S45M), 3 reads: soft clip must not appear in pileup
for i in range(3):
    seq = "TTTTT" + ref_slice("synA", 401, 45)
    add(f"sc{i}", 0, "synA", 401, "5S45M", seq)

# --- 11. synC reads 1..50 (10 reads): synB has none; synC 51..300 zero depth
for i in range(10):
    add(f"cC{i}", 0, "synC", 1, "50M", ref_slice("synC", 1, 50))
truth["events"]["zero"] = dict(synB_len=500, synC_len=300, synC_covered="1-50")

# ---- write SAM
def write_sam(path, recs, contig_lens, sm=None):
    with open(path, "w", newline="\n") as f:
        f.write("@HD\tVN:1.6\tSO:unsorted\n")
        for c, n in contig_lens.items():
            f.write(f"@SQ\tSN:{c}\tLN:{n}\n")
        f.write(f"@RG\tID:{sm or 'rg1'}\tSM:{sm or 'sample1'}\tPL:ILLUMINA\n")
        for r in recs:
            tags = f"RG:Z:{sm or 'rg1'}"
            f.write("\t".join(map(str, [r["name"], r["flag"], r["ref"], r["pos"], r["mapq"], r["cigar"], r["rnext"],
                                        r["pnext"], r["tlen"], r["seq"], r["qual"], tags])) + "\n")


lens = {k: len(v) for k, v in refs.items()}
write_sam(os.path.join(OUT, "syn.sam"), records, lens)
json.dump({"truth": truth, "records": records, "lens": lens}, open(os.path.join(OUT, "truth.json"), "w"), indent=1)


def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode != 0:
        print("CMD FAIL", cmd, r.stderr)
        sys.exit(1)
    return r.stdout


sh(f"cd {OUT} && samtools faidx syn.fa && samtools sort -o syn.bam syn.sam && samtools index syn.bam")

# ---- deep.bam
dref = {"synD": rand_seq(100)}
write_fa(os.path.join(OUT, "deep.fa"), dref)
recs = []
for i in range(9000):
    recs.append(dict(name=f"d{i}", flag=0, ref="synD", pos=1, mapq=60, cigar="50M", seq=dref["synD"][:50], qual="I" * 50,
                     rnext="*", pnext=0, tlen=0, rg=None))
write_sam(os.path.join(OUT, "deep.sam"), recs, {"synD": 100})
sh(f"cd {OUT} && samtools faidx deep.fa && samtools sort -o deep.bam deep.sam && samtools index deep.bam && rm deep.sam")

# ---- multi.bam : chr1..chr11
mref = {f"chr{i}": rand_seq(200) for i in range(1, 12)}
write_fa(os.path.join(OUT, "multi.fa"), mref)
recs = []
for c, s in mref.items():
    ref_b = s[99]
    alt_b = alt_of(ref_b)
    for i in range(12):
        seq = s[75:125]  # 76..125
        if i < 6:
            seq = seq[:24] + alt_b + seq[25:]  # pos 100 is index 24 in 76..125
        recs.append(dict(name=f"{c}_r{i}", flag=0 if i % 2 == 0 else 16, ref=c, pos=76, mapq=60, cigar="50M", seq=seq,
                         qual="I" * 50, rnext="*", pnext=0, tlen=0, rg=None))
write_sam(os.path.join(OUT, "multi.sam"), recs, {k: 200 for k in mref})
sh(f"cd {OUT} && samtools faidx multi.fa && samtools sort -o multi.bam multi.sam && samtools index multi.bam && rm multi.sam")
json.dump({c: dict(pos=100, ref=s[99], alt=alt_of(s[99])) for c, s in mref.items()}, open(os.path.join(OUT, "multi_truth.json"), "w"))

# ---- s1.bam / s2.bam : synA 81..130, SNP at 100 with 3/20 (s1) and 12/20 (s2) alt reads
for sm, n_alt in (("s1", 3), ("s2", 12)):
    recs = []
    for i in range(20):
        seq = ref_slice("synA", 81, 50)
        if i < n_alt:
            seq = subst(seq, snp_pos - 81, snp_alt)
        recs.append(dict(name=f"{sm}_r{i}", flag=0 if i % 2 == 0 else 16, ref="synA", pos=81, mapq=60, cigar="50M",
                         seq=seq, qual="I" * 50, rnext="*", pnext=0, tlen=0, rg=None))
    write_sam(os.path.join(OUT, f"{sm}.sam"), recs, {"synA": 1000, "synB": 500, "synC": 300}, sm=sm)
    sh(f"cd {OUT} && samtools sort -o {sm}.bam {sm}.sam && samtools index {sm}.bam && rm {sm}.sam")

print("data written:", sorted(os.listdir(OUT)))
print("SNP synA:%d %s>%s" % (snp_pos, snp_ref, snp_alt))
