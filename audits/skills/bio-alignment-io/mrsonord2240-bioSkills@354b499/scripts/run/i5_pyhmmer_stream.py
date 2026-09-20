"""Input 5 (Stress/complex): pyhmmer streaming section of SKILL.md, VERBATIM, on a multi-family Stockholm built from REAL Pfam PF00042 seed
(repeated 3x under different names to imitate a Pfam-A.full-style multi-alignment file) + pyhmmer format-support claims."""
import pathlib, re, io
import pyhmmer
from Bio import AlignIO
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m)
here = pathlib.Path(__file__).parent
src = pathlib.Path(r'F:\OpenScience\audit-envs\alignment\public-data\msa\PF00042_seed.sto').read_text(encoding='utf-8')
multi = ''.join(re.sub(r'(#=GF ID\s+)Globin', rf'\g<1>Globin_copy{i}', src) for i in range(3))
(here/'data'/'Pfam-mini.sto').write_text(multi, encoding='utf-8')
print('--- A. SKILL streaming snippet, verbatim')
try:
    with pyhmmer.easel.MSAFile(str(here/'data'/'Pfam-mini.sto'), digital=True) as msa_file:
        n = 0
        for msa in msa_file:
            if msa.nseq < 50:
                continue
            weights = msa.compute_weights(method='pb')
            print(msa.name.decode(), msa.nseq, msa.alen, f'sum_w={sum(weights):.1f}'); n += 1
    ok(n == 3, f'{n} families printed')
except Exception as e:
    ok(False, f'verbatim SKILL snippet failed: {type(e).__name__}: {e}')
print('--- B. corrected against pyhmmer 0.12.3 API')
with pyhmmer.easel.MSAFile(str(here/'data'/'Pfam-mini.sto'), digital=True) as mf:
    fams = list(mf)
ok(len(fams)==3, f'{len(fams)} families streamed')
m = fams[0]
print('name type', type(m.name), m.name, '| nseq', len(m.sequences), '| alignment len', len(m.alignment[0]) if hasattr(m,'alignment') and m.alignment else None)
for meth in ['compute_weights']:
    try:
        import inspect; print(meth, inspect.signature(getattr(m, meth)) if hasattr(getattr(m, meth),'__text_signature__') else getattr(m, meth).__doc__[:300])
    except Exception as e: print('sig', e)
try:
    w = m.compute_weights(method='pb'); print('compute_weights(method=pb) ->', type(w))
except Exception as e: print('compute_weights(method="pb") ->', type(e).__name__, e)
try:
    w = m.sequence_weights; print('sequence_weights attr type', type(w), 'first', list(w)[:3] if w else w)
except Exception as e: print('sequence_weights ->', type(e).__name__, e)
try:
    m.compute_weights(); ok(True, 'compute_weights() no-arg ok'); w = list(m.sequence_weights); print('sum of weights', round(sum(w),2))
except Exception as e: print('no-arg compute_weights', type(e).__name__, e)

print('--- C. pyhmmer format claims: write real Pfam seed via AlignIO in each format, read with MSAFile(format=...)')
ref = AlignIO.read(r'F:\OpenScience\audit-envs\alignment\public-data\msa\PF00042_seed.sto', 'stockholm')
for bio_fmt, py_fmt in [('fasta','afa'),('clustal','clustal'),('phylip-relaxed','phylip'),('stockholm','stockholm')]:
    f = here/'data'/f'pf.{bio_fmt}'; AlignIO.write(ref, f, bio_fmt)
    try:
        with pyhmmer.easel.MSAFile(str(f), format=py_fmt, digital=True) as mf: mm = mf.read()
        print(f'{py_fmt:10s} read -> {len(mm.sequences)} seqs')
    except Exception as e: print(f'{py_fmt:10s} read -> {type(e).__name__}: {str(e)[:90]}')
try:
    with pyhmmer.easel.MSAFile(str(here/'data'/'globins_hmm.a2m'), format='a3m', digital=True) as mf: mf.read()
except Exception as e: print('format="a3m" ->', type(e).__name__, str(e)[:160])
with pyhmmer.easel.MSAFile(str(here/'data'/'globins_hmm.a2m'), format='a2m', digital=True) as mf: a2 = mf.read()
ok(len(a2.sequences)==8, f'a2m read OK by pyhmmer: {len(a2.sequences)} seqs; per-seq lengths {sorted(set(len(s) for s in a2.sequences))}')
print('--- D. MSA.write formats (SKILL: fasta/stockholm/a2m R/W)')
for fmt in ['afa','stockholm','a2m','pfam','clustal','phylip','a3m']:
    try:
        bio = io.BytesIO(); fams[0].write(bio, fmt); print(fmt, 'write ->', len(bio.getvalue()), 'bytes')
    except Exception as e: print(fmt, 'write ->', type(e).__name__, str(e)[:100])
