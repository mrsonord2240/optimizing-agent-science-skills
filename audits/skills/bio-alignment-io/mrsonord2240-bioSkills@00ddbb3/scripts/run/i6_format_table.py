"""INPUT 6 (Scope boundary, regression + extension). Verify EVERY cell class of the SKILL's Format Coverage Map against Biopython 1.88 / pyhmmer 0.12.3,
using real files where available (Pfam seed, Biopython test MSF/Mauve files) and tiny SYNTHETIC PSL/chain one-liners."""
import io, os, importlib
import Bio, pyhmmer
from Bio import Align, AlignIO
from Bio.AlignIO import _FormatToIterator as AIO_R, _FormatToWriter as AIO_W
from common import *
os.chdir(DATA)
print('Biopython', Bio.__version__, 'pyhmmer', pyhmmer.__version__)
print('AlignIO readers:', sorted(AIO_R)); print('AlignIO writers:', sorted(AIO_W)); print('Bio.Align.formats:', Align.formats)
def has(mod, cls):
    try: return hasattr(importlib.import_module(f'Bio.Align.{mod}'), cls)
    except Exception: return False
BA = {f: (has(f, 'AlignmentIterator'), has(f, 'AlignmentWriter')) for f in Align.formats}
print('Bio.Align (reader, writer):', BA)
T = ok
print('--- table rows: AlignIO column')
_a = AlignIO.read(str(PFAM), 'stockholm')
for _f in ['fasta', 'clustal', 'phylip-relaxed', 'phylip-sequential', 'stockholm', 'nexus']:
    _b = io.StringIO()
    try:
        for _r in _a: _r.annotations['molecule_type'] = 'protein'
        AlignIO.write(_a[:6, :], _b, _f); T(len(_b.getvalue()) > 100, f'AlignIO.write({_f}) works (registry-independent: fasta/stockholm dispatch via SeqIO)')
    except Exception as e: T(False, f'AlignIO.write {_f}: {type(e).__name__}: {str(e)[:80]}')
T({'clustal', 'phylip', 'phylip-relaxed', 'phylip-sequential', 'nexus', 'maf', 'stockholm', 'msf'} <= set(AIO_R) | {'stockholm'}, 'AlignIO readers registry covers clustal/phylip*/nexus/maf/msf (fasta+stockholm via SeqIO)')
T('a2m' not in AIO_R and 'a2m' not in AIO_W and 'a3m' not in AIO_R, "AlignIO has no 'a2m'/'a3m' (table: '--')")
T('emboss' in AIO_R and 'fasta-m10' in AIO_R and 'mauve' in AIO_R, 'AlignIO readers include emboss, fasta-m10, mauve')
print('   AlignIO msf reader present?', 'msf' in AIO_R, '(table says AlignIO MSF = R)')
T('mauve' in AIO_W and 'fasta-m10' not in AIO_W and 'emboss' not in AIO_W, 'AlignIO writers: mauve yes; emboss / fasta-m10 no (table: "Mauve also W")')
print('--- Bio.Align column')
for f in ['fasta', 'clustal', 'phylip', 'stockholm', 'nexus', 'maf', 'a2m', 'msf', 'mauve']:
    T(f in Align.formats, f"Bio.Align.formats includes '{f}': (reader, writer)={BA.get(f)}")
T(BA['msf'] == (True, False), f"msf is read-only in Bio.Align {BA['msf']} (table: MSF 'R')")
T(BA['a2m'] == (True, True), f"a2m has reader AND writer in Bio.Align {BA['a2m']} (round-2 table: A2M 'R (padded A2M), W (needs column_annotations[state])')")
T(BA['mauve'] == (True, True), 'Bio.Align mauve R/W (table: "Mauve also W")')
T('fasta-m10' not in Align.formats and 'emboss' in Align.formats, "Bio.Align: 'emboss' yes, no fasta-m10 (table: 'no FASTA-m10')")
for f in ['psl', 'chain', 'bed', 'sam', 'exonerate', 'bigmaf', 'bigpsl', 'bigbed']:
    T(BA[f][0] and BA[f][1], f'Bio.Align {f} reader+writer present {BA[f]} (round-2 table row: PSL / chain / BED / SAM / exonerate / bigMaf / bigPsl / bigBed "R/W")')
for f in ['hhr', 'tabular']:
    T(BA[f] == (True, False), f'Bio.Align {f} is read-only {BA[f]} (round-2 table row "HHR / tabular (BLAST) R only")')
print('--- functional round trips through Bio.Align')
aln = AlignIO.read(str(PFAM), 'stockholm'); AlignIO.write(aln, 'pf.fasta', 'fasta'); AlignIO.write(aln, 'pf.clustal', 'clustal'); AlignIO.write(aln, 'pf.phy', 'phylip-relaxed')
ref = [str(r.seq).upper().replace('.', '-') for r in aln]
for f, fmt in [('pf.fasta', 'fasta'), ('pf.clustal', 'clustal')]:
    a = Align.read(f, fmt); T(a.shape == (73, 141) and [str(x).upper() for x in a] == ref, f'Align.read({fmt}) shape {a.shape}, rows identical to source')
    buf = io.StringIO(); Align.write(a, buf, fmt)
    back = AlignIO.read(io.StringIO(buf.getvalue()), fmt)
    T([str(x.seq).upper() for x in back] == ref, f'Align.write({fmt}) -> AlignIO re-read identical')
# Bio.Align 'phylip' on the SKILL-recommended relaxed output (long real ids)
try: Align.read('pf.phy', 'phylip'); T(False, 'Align.read(phylip) accepted a relaxed file with long ids')
except ValueError as e: T(True, f'Align.read(phylip) on AlignIO phylip-relaxed output with real long Pfam ids -> ValueError (loud): {str(e)[:70]}  [SKILL table lists Bio.Align PHYLIP R/W without saying it is strict-only]')
a = Align.read('pf.fasta', 'fasta'); buf = io.StringIO(); Align.write(a, buf, 'phylip'); back = Align.read(io.StringIO(buf.getvalue()), 'phylip')
T(back.shape == (73, 141) and [x.id for x in back.sequences][0] == 'GLB2_LUMTE', f'Align.write(phylip) truncates ids to 10 chars silently: {[x.id for x in back.sequences][:2]}')
plain = '# STOCKHOLM 1.0\nseq1 ACGT-ACGT\nseq2 ACGTAACGT\n//\n'
try:
    a = Align.read(io.StringIO(plain), 'stockholm'); T(a.shape == (2, 9), f'Align.read plain (no annotations) stockholm works: {a.shape}')
except Exception as e: T(False, f'Align.read plain stockholm: {type(e).__name__}: {str(e)[:90]}')
try:
    Align.read('synthetic_rna.sto', 'stockholm'); print('info: Align.read(annotated synthetic RNA sto) works')
except Exception as e: print('info: Align.read(annotated synthetic RNA sto) ->', type(e).__name__, str(e)[:60])
try:
    a = Align.read(io.StringIO(plain), 'stockholm'); Align.write(a, io.StringIO(), 'stockholm'); T(False, 'Align.write stockholm on plain-read Alignment worked (table says W = AttributeError)')
except Exception as e: T(True, f"Align.write stockholm on plain-read Alignment fails: {type(e).__name__}: {str(e)[:80]} (table: W AttributeError)")
try:
    a = Align.read('pf.fasta', 'fasta'); Align.write(a, io.StringIO(), 'nexus'); T(False, 'Align.write nexus without molecule type unexpectedly worked')
except Exception as e: T(True, f'Align.write(nexus) of FASTA-read Alignment fails: {type(e).__name__}: {str(e)[:70]} (table: "write needs a molecule type")')
AlignIO.convert(str(PFAM), 'stockholm', 'pf_prot.nex', 'nexus', molecule_type='protein')
try:
    a = Align.read('pf_prot.nex', 'nexus'); T(a.shape == (73, 141), f'Align.read nexus {a.shape}')
except Exception as e: T(False, f'Align.read nexus: {type(e).__name__}: {str(e)[:80]}')
print('--- round-2 A2M writer claim: needs column_annotations[state]')
fa = Align.read('pf.fasta', 'fasta')
try: Align.write(fa, io.StringIO(), 'a2m'); T(False, 'Align.write a2m on a FASTA-read Alignment worked (table says it needs column_annotations[state])')
except Exception as e: T(True, f'Align.write(a2m) on FASTA-read Alignment fails: {type(e).__name__}: {str(e)[:80]}')
try:
    pa = Align.read(str(HERE/'data'/'a2m'/'pf.a2m'), 'a2m'); buf = io.StringIO(); Align.write(pa, buf, 'a2m'); back = Align.read(io.StringIO(buf.getvalue()), 'a2m')
    T(back.shape == pa.shape == (73, back.shape[1]) and [str(x) for x in back] == [str(x) for x in pa], f'A2M read (reformat.pl padded) -> write -> re-read identical {back.shape}; annotation keys {list(pa.column_annotations)}')
except Exception as e: T(False, f'A2M read/write round trip: {type(e).__name__}: {str(e)[:100]}')
print('--- round-2 PHYLIP cell: Bio.Align phylip strict-only. Strict 10-char file reads; relaxed file with long ids raises')
strict = chr(10).join([' 2 8', 'seqone    ACGTACGT', 'seqtwo    ACGTACGA', ''])
try: a = Align.read(io.StringIO(strict), 'phylip'); T(a.shape == (2, 8), f'Align.read(phylip) reads a strict 10-char-name file: {a.shape}')
except Exception as e: T(False, f'Align.read strict phylip: {type(e).__name__}: {str(e)[:90]}')
print('--- MSF / Mauve real files')
try:
    a = Align.read('W_prot.msf', 'msf'); T(a.shape[0] > 1, f'Align.read(msf) real GCG MSF works: {a.shape}')
except Exception as e: T(False, f'Align.read msf: {type(e).__name__}: {str(e)[:100]}')
try:
    a = AlignIO.read('W_prot.msf', 'msf'); T(True, 'AlignIO.read msf works')
except Exception as e: print('info: AlignIO.read(W_prot.msf,"msf") ->', type(e).__name__, str(e)[:70], '(table says AlignIO MSF = R)')
try:
    n = sum(1 for _ in AlignIO.parse('mauve_simple.xmfa', 'mauve')); T(n >= 1, f'AlignIO mauve real XMFA parsed {n} blocks')
except Exception as e: T(False, f'AlignIO mauve: {type(e).__name__}: {str(e)[:80]}')
try:
    n = sum(1 for _ in Align.parse('mauve_simple.xmfa', 'mauve')); T(n >= 1, f'Align mauve real XMFA parsed {n} alignments')
except Exception as e: T(False, f'Align mauve: {type(e).__name__}: {str(e)[:80]}')
print('--- PSL / chain (SYNTHETIC one-liners), read + write')
psl = '30\t0\t0\t0\t0\t0\t0\t0\t+\tq1\t50\t5\t35\tchr1\t200\t100\t130\t1\t30,\t5,\t100,\n'; open('s.psl', 'w').write(psl)
a = list(Align.parse('s.psl', 'psl')); T(len(a) == 1 and a[0].coordinates.tolist() == [[100, 130], [5, 35]], f'PSL parsed coordinates {a[0].coordinates.tolist()} (target 100-130, query 5-35)')
buf = io.StringIO(); Align.write(a, buf, 'psl'); T('q1' in buf.getvalue() and 'chr1' in buf.getvalue(), 'PSL written back with q1/chr1')
open('s.chain', 'w').write('chain 1000 chr1 200 + 100 130 q1 50 + 5 35 1\n30\n\n')
a = list(Align.parse('s.chain', 'chain')); T(len(a) == 1, f'chain parsed {a[0].coordinates.tolist()}')
print('--- NOT-in-Biopython table: none of HAL / net / AXT / GFA / rGFA / GAF is a format')
for f in ['hal', 'net', 'axt', 'gfa', 'rgfa', 'gaf']:
    T(f not in Align.formats and f not in AIO_R and f not in AIO_W, f'{f}: absent from Bio.Align.formats, AlignIO readers and writers')
print('--- Bio.Align.formats entries the table does not mention:', sorted(set(Align.formats) - {'fasta', 'clustal', 'phylip', 'stockholm', 'nexus', 'maf', 'a2m', 'msf', 'mauve', 'emboss', 'psl', 'chain', 'bed', 'sam'}))
print('--- pyhmmer.easel format column')
try:
    with pyhmmer.easel.MSAFile('pf.fasta', format='nosuch') as f: pass
except Exception as e: print('pyhmmer format error text:', str(e)[:260])
with pyhmmer.easel.MSAFile('pf.fasta', format='afa', digital=True) as mf: m = mf.read()
for fmt in ['afa', 'stockholm', 'a2m', 'pfam', 'clustal', 'phylip', 'phylips']:
    try:
        b = io.BytesIO(); m.write(b, fmt); T(len(b.getvalue()) > 1000, f'pyhmmer MSA.write(format={fmt!r}) wrote {len(b.getvalue())} bytes')
    except Exception as e: T(False, f'pyhmmer MSA.write {fmt}: {type(e).__name__}: {str(e)[:80]}')
for fmt in ['nexus', 'maf', 'a3m', 'msf']:
    try:
        m.write(io.BytesIO(), fmt); T(False, f'pyhmmer wrote {fmt} (table says "--")')
    except Exception as e: T(True, f'pyhmmer has no {fmt}: {type(e).__name__} (table: "--")')
summary()
