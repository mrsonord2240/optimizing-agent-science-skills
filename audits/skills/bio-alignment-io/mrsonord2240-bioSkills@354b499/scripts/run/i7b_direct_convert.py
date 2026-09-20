"""Input 7 (Adversarial/ambiguous): 'Convert my Clustal alignment to PHYLIP format' -- the SKILL's *Direct Conversion* snippet uses strict 'phylip'; run it on the REAL Pfam alignment (73 ids like GLB2_LUMTE/31-141)."""
import pathlib
from Bio import AlignIO
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m)
d = pathlib.Path(__file__).parent/'data'
try:
    AlignIO.convert(d/'pf.clustal', 'clustal', d/'direct.phy', 'phylip')       # VERBATIM SKILL pattern (direct conversion, strict phylip)
    b = AlignIO.read(d/'direct.phy', 'phylip'); ids = [r.id for r in b]
    ok(len(set(ids)) == 73, f'strict phylip convert ok, {len(set(ids))} unique of {len(ids)} ids; sample {ids[:3]}')
except Exception as e:
    ok(False, f'strict phylip direct conversion of real Pfam alignment: {type(e).__name__}: {e}')
ref = AlignIO.read(d/'pf.clustal', 'clustal'); short = [r.id[:10] for r in ref]
import collections; dup = [k for k, v in collections.Counter(short).items() if v > 1]; print('10-char prefix collisions in the real alignment:', dup[:5], len(dup))
