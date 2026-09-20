"""INPUT 5 (Stress, regression). (a) multi-alignment I/O snippets; (b) pyhmmer streaming snippet VERBATIM on a multi-family Stockholm built from the
REAL Pfam PF00042 seed (x3 under different #=GF ID, imitating Pfam-A.full); (c) PAML route prep: 6 REAL HBB CDS -> MAFFT (WSL) -> AlignIO -> sequential/relaxed."""
import io, os, re, contextlib
import pyhmmer
from Bio import AlignIO
from common import *
os.chdir(DATA)
src = PFAM.read_text(encoding='utf-8')
multi = ''.join(re.sub(r'(#=GF ID\s+)Globin', rf'\g<1>Globin_copy{i}', src) for i in range(3))
open('Pfam-mini.sto', 'w', encoding='utf-8').write(multi)
print('--- (a) multi-alignment snippets')
n = 0
for alignment in AlignIO.parse('Pfam-mini.sto', 'stockholm'):
    n += 1
ok(n == 3, f'AlignIO.parse stockholm yields {n} alignments')
alignments = list(AlignIO.parse('Pfam-mini.sto', 'stockholm')); ok(all((len(a), a.get_alignment_length()) == (73, 141) for a in alignments), 'each 73x141')
count = AlignIO.write(alignments, 'multi_out.sto', 'stockholm'); ok(count == 3 and len(list(AlignIO.parse('multi_out.sto', 'stockholm'))) == 3, f'write multiple stockholm: {count}, re-parse 3')
count = AlignIO.write(alignments, 'multi_out.phy', 'phylip-relaxed'); ok(count == 3 and len(list(AlignIO.parse('multi_out.phy', 'phylip-relaxed'))) == 3, 'multi phylip-relaxed round trip 3')
with open('handle_out.aln', 'w') as handle: AlignIO.write(alignments[0], handle, 'clustal')
b = AlignIO.read('handle_out.aln', 'clustal'); ok([str(x.seq).upper().replace('.', '-') for x in b] == [str(x.seq).upper().replace('.', '-') for x in alignments[0]], 'write-to-handle clustal round trip residues identical')
print('--- (b) pyhmmer streaming snippet VERBATIM')
code = block('Streaming Large Stockholm').replace("'Pfam-A.full'", "'Pfam-mini.sto'")
buf = io.StringIO()
with contextlib.redirect_stdout(buf): exec(code, {})
out = buf.getvalue(); print(out)
lines = [l for l in out.splitlines() if l.strip()]
ok(len(lines) == 3 and all(re.match(r'Globin_copy\d 73 141 sum_w=73\.0', l) for l in lines), 'snippet printed 3 rows "Globin_copyN 73 141 sum_w=73.0" (weights sum to n seqs, as the SKILL states)')
with pyhmmer.easel.MSAFile('Pfam-mini.sto', digital=True) as mf: fams = list(mf)
ok(isinstance(fams[0].name, str) and not hasattr(fams[0], 'nseq') and not hasattr(fams[0], 'alen'), f'msa.name is {type(fams[0].name).__name__}; no .nseq/.alen (as SKILL comment says); pyhmmer {pyhmmer.__version__}')
w = fams[0].compute_weights(method='pb'); print('compute_weights type', type(w).__name__)
ok(abs(sum(list(w)) - 73) < 1e-6 if w is not None else False, 'sum of PB weights == n sequences (SKILL: "weights sum to the number of sequences (not Neff)")')
print('--- pyhmmer format table claims (afa / clustal / phylip / stockholm read of the real Pfam alignment)')
ref = AlignIO.read(str(PFAM), 'stockholm')
for bio_fmt, py_fmt in [('fasta','afa'), ('clustal','clustal'), ('phylip','phylip'), ('phylip-sequential','phylips'), ('stockholm','stockholm')]:
    f = f'pf_{bio_fmt}.txt'; AlignIO.write(ref, f, bio_fmt)
    try:
        with pyhmmer.easel.MSAFile(f, format=py_fmt, digital=True) as mf: m = mf.read()
        ok(len(m.sequences) == 73, f'pyhmmer format={py_fmt!r} reads Biopython-written {bio_fmt}: {len(m.sequences)} seqs')
    except Exception as e: ok(False, f'pyhmmer format={py_fmt!r}: {type(e).__name__}: {str(e)[:80]}')
try:
    AlignIO.write(ref, 'pf_relaxed.txt', 'phylip-relaxed')
    with pyhmmer.easel.MSAFile('pf_relaxed.txt', format='phylip', digital=True) as mf: mf.read()
    print('info: pyhmmer phylip reads Biopython phylip-relaxed too')
except Exception as e: print('info (not a SKILL claim): pyhmmer format="phylip" on Biopython phylip-relaxed ->', type(e).__name__, str(e)[:80])
print('--- (c) PAML route: alignment prep (MAFFT run by i5_align.sh)')
summary()
