"""Input 1 oracle (independent of ampliconclip's own stats). WSL env python, pysam.
Usage: s1_oracle.py <out/i1 dir>  (after s1_real_artic.sh). Checks, from the primer BED alone:
  * every read end that ampliconclip --both-ends --strand moved lands exactly on a primer boundary of the right strand
    (fwd 5 prime start == a '+' primer END; fwd 3 prime end == a '-' primer START;
     rev 5 prime end == a '-' primer START; rev 3 prime start == a '+' primer END)
  * MD/NM in the final BAM equal an independent recompute from reference + CIGAR + SEQ
  * raw output has no NM/MD on clipped reads; final has MD on all"""
import collections, pysam, sys
W = sys.argv[1]
orig = pysam.AlignmentFile(f"{W}/input.bam"); raw = pysam.AlignmentFile(f"{W}/clipped.bam"); fin = pysam.AlignmentFile(f"{W}/clipped_final.bam")
ref = pysam.FastaFile(f"{W}/reference.fa")
prim = [l.rstrip("\n").split("\t") for l in open(f"{W}/primers.bed") if l.strip()]
plus_end = {int(p[2]) for p in prim if p[5] == "+"}; minus_start = {int(p[1]) for p in prim if p[5] == "-"}
o = {(r.query_name, r.flag, r.query_sequence): r for r in orig.fetch(until_eof=True)}
c = collections.Counter(); bad = []
for r in raw.fetch(until_eof=True):
    x = o[(r.query_name, r.flag, r.query_sequence)]
    left_moved = r.reference_start != x.reference_start; right_moved = r.reference_end != x.reference_end
    if left_moved:
        ok = (r.reference_start in plus_end)
        c["left ok" if ok else "left BAD"] += 1
        if not ok: bad.append((r.query_name, "L", r.reference_start))
    if right_moved:
        ok = (r.reference_end in minus_start)
        c["right ok" if ok else "right BAD"] += 1
        if not ok: bad.append((r.query_name, "R", r.reference_end))
    if not left_moved and not right_moved: c["unchanged"] += 1
    c["raw has NM"] += r.has_tag("NM"); c["raw has MD"] += r.has_tag("MD")
print("boundary oracle:", dict(c)); print("bad examples:", bad[:5])
def md_nm(read):
    seq = read.query_sequence; rs = ref.fetch(read.reference_name).upper(); q = 0; p = read.reference_start; md = []; run = 0; nm = 0
    for op, ln in read.cigartuples:
        if op in (0, 7, 8):
            for i in range(ln):
                a, t = seq[q + i].upper(), rs[p + i]
                if a == t: run += 1
                else: md += [str(run), t]; run = 0; nm += 1
            q += ln; p += ln
        elif op == 1: q += ln; nm += ln
        elif op == 2: md += [str(run), "^" + rs[p:p + ln]]; run = 0; p += ln; nm += ln
        elif op == 4: q += ln
    md.append(str(run)); return "".join(md), nm
bm = bn = tot = nomd = 0
for r in fin.fetch(until_eof=True):
    tot += 1
    if not r.has_tag("MD"): nomd += 1; continue
    md, nm = md_nm(r); bm += r.get_tag("MD") != md; bn += r.get_tag("NM") != nm
print(f"final BAM: reads={tot} without MD={nomd} MD mismatches vs recompute={bm} NM mismatches={bn}")
