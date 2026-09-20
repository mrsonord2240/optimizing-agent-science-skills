#!/usr/bin/env python
"""Independent ground-truth order checker (does NOT use samtools sort logic; pysam only reads).
usage: order_check.py file.bam
prints: header SO/GO/SS, n records, coordinate_sorted (tid,pos non-decreasing, unmapped last),
        queryname_ascii_sorted, queryname_natural_sorted, and a record-multiset md5 (order independent).
"""
import sys, re, hashlib
import pysam

def natkey(s):
    # digit runs compare numerically, other runs bytewise (mirrors samtools strnum_cmp intent)
    return [(0, int(t)) if t.isdigit() else (1, t) for t in re.findall(r"\d+|\D+", s)]

def main(path):
    with pysam.AlignmentFile(path, "rb", check_sq=False) as f:
        hd = f.header.to_dict().get("HD", {})
        recs = list(f.fetch(until_eof=True))
    coord = True; ascii_ok = True; nat_ok = True
    prev = None; pn = None
    for r in recs:
        k = (r.reference_id if r.reference_id >= 0 else 1 << 30, r.reference_start)
        if prev is not None and k < prev:
            coord = False
        prev = k
        if pn is not None:
            if r.query_name.encode() < pn.encode():
                ascii_ok = False
            if natkey(r.query_name) < natkey(pn):
                nat_ok = False
        pn = r.query_name
    sig = hashlib.md5("\n".join(sorted(r.to_string() for r in recs)).encode()).hexdigest()
    print(f"{path}\n  HD={hd}\n  n={len(recs)} coordinate_sorted={coord} qname_ascii={ascii_ok} qname_natural={nat_ok} multiset_md5={sig}")

if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
