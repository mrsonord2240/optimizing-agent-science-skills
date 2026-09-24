import glob, os, pysam
from skillfns import is_coordinate_sorted, ensure_coordinate_sorted
fixable=[p for p in sorted(glob.glob('neg/*.bam')) if 'templcoord' not in p or True]
bad=0
for p in fixable:
    out='fixed_'+os.path.basename(p)
    r=ensure_coordinate_sorted(p,out)
    ok=is_coordinate_sorted(r)
    idx_ok=True
    try: pysam.index(r)
    except Exception as e: idx_ok=False
    was=is_coordinate_sorted(p)
    print("  %-34s was_sorted=%-5s -> returned %-38s now_sorted=%s indexes=%s" % (os.path.basename(p), was, r, ok, idx_ok))
    if not (ok and idx_ok): bad+=1
print("ensure_coordinate_sorted failures:", bad)
assert bad==0
