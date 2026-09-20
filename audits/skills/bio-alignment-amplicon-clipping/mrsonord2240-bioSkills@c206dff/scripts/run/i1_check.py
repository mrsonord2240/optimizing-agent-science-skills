"""Input 1 checker: independent oracle for the real ARTIC run. Runs in WSL env python (pysam 0.24.1).
Oracle (not the tool's own output): from the primer BED alone,
  * a clipped forward read must start (0-based) exactly at some + primer END,
  * a clipped reverse read must end (0-based excl) exactly at some - primer START,
  * MD/NM recomputed from reference + CIGAR + SEQ must equal calmd's tags.
"""
import sys, collections
import pysam

D = "/mnt/openscience/audit-envs/alignment-files/public-data/sarscov2"
OUT = "/mnt/openscience/audits/bio-alignment-amplicon-clipping/run/out/i1"
inp = pysam.AlignmentFile(f"{D}/sars-cov-2_v5.3.2.nanopore.bam")
clip_raw = pysam.AlignmentFile(f"{OUT}/clipped.bam")
fin = pysam.AlignmentFile(f"{OUT}/clipped_final.bam")
ref = pysam.FastaFile(f"{D}/MN908947.3.fasta")
prim = [l.split("\t") for l in open(f"{D}/v5.3.2.primer.bed") if l.strip()]
plus_end = collections.defaultdict(int); minus_start = collections.defaultdict(int)
for c, s, e, name, pool, strand, seq in [p[:7] for p in prim]:
    (plus_end if strand == "+" else minus_start)[int(e) if strand == "+" else int(s)] += 1

def key(r):
    return (r.query_name, r.flag, r.query_sequence)  # read name is unique for SE; flag+seq to be safe

orig = {key(r): r for r in inp.fetch(until_eof=True)}
n_changed = n_fwd_ok = n_fwd_bad = n_rev_ok = n_rev_bad = 0
bad_examples = []
unchanged = 0
for r in clip_raw.fetch(until_eof=True):
    o = orig[key(r)]
    if r.cigarstring == o.cigarstring and r.reference_start == o.reference_start:
        unchanged += 1; continue
    n_changed += 1
    if not r.is_reverse:
        if r.reference_start in plus_end: n_fwd_ok += 1
        else: n_fwd_bad += 1; bad_examples.append((r.query_name[:8], r.reference_start, o.reference_start))
    else:
        if r.reference_end in minus_start: n_rev_ok += 1
        else: n_rev_bad += 1; bad_examples.append((r.query_name[:8], r.reference_end, o.reference_end))
print(f"reads unchanged by ampliconclip: {unchanged}; changed: {n_changed}")
print(f"ORACLE fwd clipped start == a + primer end: ok={n_fwd_ok} bad={n_fwd_bad}; rev clipped end == a - primer start: ok={n_rev_ok} bad={n_rev_bad}")
print("bad examples:", bad_examples[:5])

# --- MD/NM oracle on calmd output
def md_nm(read):
    seq = read.query_sequence; rs = ref.fetch(read.reference_name).upper()
    qpos = 0; rpos = read.reference_start; md = []; run = 0; nm = 0
    for op, ln in read.cigartuples:
        if op in (0, 7, 8):
            for i in range(ln):
                q, t = seq[qpos + i].upper(), rs[rpos + i]
                if q == t or q == "N" and False: run += 1
                else:
                    md.append(str(run)); md.append(t); run = 0; nm += 1
            qpos += ln; rpos += ln
        elif op == 1: qpos += ln; nm += ln
        elif op == 2:
            md.append(str(run)); md.append("^" + rs[rpos:rpos + ln]); run = 0; rpos += ln; nm += ln
        elif op == 4: qpos += ln
    md.append(str(run))
    return "".join(md), nm
bad_md = bad_nm = tot = 0
for r in fin.fetch(until_eof=True):
    tot += 1
    md, nm = md_nm(r)
    if r.get_tag("MD") != md: bad_md += 1
    if r.get_tag("NM") != nm: bad_nm += 1
print(f"calmd MD/NM vs independent recompute over {tot} reads: MD mismatches={bad_md}, NM mismatches={bad_nm}")

# --- what does raw ampliconclip do with NM/MD?
has_nm = has_md = 0
for r in clip_raw.fetch(until_eof=True):
    has_nm += r.has_tag("NM"); has_md += r.has_tag("MD")
print(f"raw ampliconclip output: NM present on {has_nm}/4916, MD present on {has_md}/4916 (input NM 4916, MD 0)")

# --- residual primer bases: how many final reads still start inside a + primer / end inside a - primer
lefts = [(int(p[1]), int(p[2])) for p in prim if p[5].strip() == "+"]
rights = [(int(p[1]), int(p[2])) for p in prim if p[5].strip() == "-"]
res = 0; res_ex = []
for r in fin.fetch(until_eof=True):
    if not r.is_reverse:
        if any(s <= r.reference_start < e - 0 for s, e in lefts): res += 1; res_ex.append((r.query_name[:8], r.reference_start))
    else:
        if any(s < r.reference_end <= e for s, e in rights): res += 1; res_ex.append((r.query_name[:8], r.reference_end))
print(f"reads whose aligned 5' end still lies inside a primer footprint after clipping: {res}", res_ex[:5])
