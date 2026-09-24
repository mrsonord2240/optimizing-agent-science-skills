import pysam, sys
with pysam.AlignmentFile(sys.argv[1],'rb') as f:
    rs=list(f.fetch(until_eof=True))
def tag(r):
    return r.get_tag('CB') if r.has_tag('CB') else None
seq=[tag(r) for r in rs]
tagged=[t for t in seq if t is not None]
print("tag values non-decreasing (ASCII) among tagged:", tagged==sorted(tagged), "| untagged reads:", seq.count(None))
ok=True; prev=None
for r in rs:
    k=(tag(r) or '', r.reference_id if r.reference_id>=0 else 1<<30, r.reference_start)
    if prev and k[0]==prev[0] and k[1:]<prev[1:]: ok=False
    prev=k
print("position is secondary key within each CB block:", ok)
assert tagged==sorted(tagged) and ok
print("n =", len(rs))
