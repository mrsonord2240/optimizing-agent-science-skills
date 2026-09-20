"""Input 4b: A2M/A3M conventions on REAL hmmalign output (data/globins_hmm.a2m from i4b_hmmalign.sh) + pyhmmer.easel format claims."""
import pathlib, io
from Bio import AlignIO, Align
import pyhmmer
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m)
here = pathlib.Path(__file__).parent; a2m = here/'data'/'globins_hmm.a2m'
raw = [l for l in a2m.read_text().splitlines()]
seqs = {}; cur=None
for l in raw:
    if l.startswith('>'): cur=l[1:].split()[0]; seqs[cur]=''
    else: seqs[cur]+=l
lens = {k: len(v) for k,v in seqs.items()}; print('raw a2m row lengths', sorted(set(lens.values())), 'contains "." :', any('.' in v for v in seqs.values()))
print('--- A. SKILL snippet: AlignIO.read(a2m, "fasta") on real hmmalign A2M')
try:
    al = AlignIO.read(a2m, 'fasta'); print('read', len(al), al.get_alignment_length())
    match_only = [''.join(c for c in str(r.seq) if c.isupper() or c == '-') for r in al]     # VERBATIM from SKILL
    ok(all(len(m)==117 for m in match_only), f'match-only lengths {[len(m) for m in match_only]} (HMM LENG=117)')
except Exception as e:
    ok(False, f'AlignIO.read(a2m,"fasta") failed: {type(e).__name__}: {e}')
print('--- B. SKILL claim: "A2M pads inserts across rows so it loads as a rectangular MSA" -> is real hmmalign A2M rectangular?')
ok(len(set(lens.values()))==1, f'rows equal length? {sorted(set(lens.values()))}')
print('--- C. match-state extraction directly on the ragged rows (no AlignIO) recovers 117?')
mm = {k: ''.join(c for c in v if c.isupper() or c in '-') for k,v in seqs.items()}
ok(all(len(x)==117 for x in mm.values()), f'match-only per-row lengths {sorted(set(len(x) for x in mm.values()))}')
print('--- D. pyhmmer reads real hmmalign A2M (format a2m)')
with pyhmmer.easel.MSAFile(str(a2m), format='a2m', digital=True) as mf: m = mf.read()
ok(len(m.sequences) == 8, f'pyhmmer a2m read: {len(m.sequences)} seqs (attribute nseq/alen do not exist in pyhmmer 0.12.3: {hasattr(m, "nseq")}/{hasattr(m, "alen")})')
print('--- E. Bio.Align a2m on the real (unpadded) hmmalign output')
try: a = Align.read(a2m, 'a2m'); print('Align.read a2m ->', a.shape)
except Exception as e: print('Align.read(hmmalign a2m) ->', type(e).__name__, str(e)[:100])
print('--- F. formats table vs Biopython 1.88')
from Bio.AlignIO import _FormatToIterator, _FormatToWriter
print('AlignIO readers:', sorted(_FormatToIterator)); print('AlignIO writers:', sorted(_FormatToWriter)); print('Bio.Align.formats:', Align.formats)
