"""Input 8 (NEW, not a first-audit input; Variant B): real files the fixer never saw.
'I have (a) hmmalign output for 8 globins against the Pfam globin profile (Stockholm with "." gaps, lowercase inserts, PP lines) and its
A2M version, (b) a MAFFT alignment of six mammalian HBB coding sequences, softmasked in places, and (c) the Pfam Ras seed (PF00071,
downloaded from EBI). Give me match-only columns, conserved columns, a consensus per file, gap counts, weights, and keep the PP/RF
annotation through cleaning.'
REAL data throughout: hmmalign 3.4 output (wsl_tools.sh), RefSeq HBB CDS + MAFFT 7.526, Pfam PF00071 seed. Ground truth: my own
parse of the raw text, the profile length (LENG 117), the RF line, biology (start codon, P-loop). Code = SKILL.md blocks."""
import io, os, re, subprocess, sys
from collections import Counter
import numpy as np
from Bio import AlignIO, SeqIO
from Bio.Align import MultipleSeqAlignment
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from common import *
import skillns

ns, log = skillns.load()
env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONIOENCODING': 'utf-8'}
def run_ex(name, *args):
    return subprocess.run([sys.executable, os.path.join(EX, name), *args], cwd=DATA, capture_output=True, text=True, env=env, timeout=900)
def parse_raw(path):
    seqs, gr, gc = {}, {}, {}
    for line in open(path, encoding='utf-8'):
        line = line.rstrip('\n')
        if not line or line.startswith('# STOCKHOLM') or line.startswith('//') or line.startswith('#=GS') or line.startswith('#=GF'): continue
        if line.startswith('#=GR'):
            _, n, tag, s = line.split(None, 3); gr[(n, tag)] = s
        elif line.startswith('#=GC'):
            _, tag, s = line.split(None, 2); gc[tag] = s
        else:
            n, s = line.split(None, 1); seqs[n] = s.strip()
    return seqs, gr, gc

# ============ A. hmmalign output (real HMMER Stockholm) ==================================================================================
STO = os.path.join(DATA, 'hmmalign_globins8.sto')
seqs, gr, gc = parse_raw(STO)
names = list(seqs); L = len(next(iter(seqs.values())))
raw = np.array([list(s) for s in seqs.values()])
print(f'A. hmmalign: {len(names)} seqs x {L} columns; raw chars: {sorted(set(raw.ravel()))}; GC keys {list(gc)}; GR keys {sorted({t for _, t in gr})}')
aln = AlignIO.read(STO, 'stockholm')
seen = sorted({c for r in aln for c in str(r.seq)})
print('   Biopython alphabet:', ''.join(seen), '| column_annotations:', list(aln.column_annotations), '| letter_annotations of row 0:', list(aln[0].letter_annotations))
isgap = np.isin(raw, ['.', '-'])
check('A. hmmalign Stockholm: shape from Biopython == raw file (8 x %d); gap characters "." and "-" are both gaps in the raw file' % L, (len(aln), aln.get_alignment_length()) == (8, L) and {'.', '-'} <= set(raw[isgap]))
gp = ns['gaps_per_column'](aln)
check('A. gaps_per_column == independent count of "." + "-" over the raw file, every column', gp == list(isgap.sum(0)), f'total {sum(gp)} vs {int(isgap.sum())}')
up = np.char.upper(raw)
def indep_cons(thr, amb='X'):
    o = []
    for j in range(L):
        c = Counter(up[~isgap[:, j], j])
        if not c: o.append('-'); continue
        t, n = c.most_common(1)[0]; o.append(t if n / len(names) >= thr else amb)
    return ''.join(o)
c50 = ns['consensus_sequence'](aln, 0.5)
check('A. consensus_sequence(0.5) on the mixed-case hmmalign alignment == independent case-folded consensus (X placeholder)', c50 == indep_cons(0.5), c50[:60] + '...')
cons_all = ns['find_conserved_positions'](aln, 1.0)
ind_cons = [(j, Counter(up[~isgap[:, j], j]).most_common(1)[0][0]) for j in range(L) if (~isgap[:, j]).all() and len(set(up[:, j])) == 1]
check('A. fully conserved columns == independent (columns where all 8 rows hold the same residue, case-folded)', [(a, b) for a, b, _ in cons_all] == ind_cons, f'{len(ind_cons)} columns')
# proximal His of MYG_PHYMC: 0-based index 93 of the UniProt sequence -> column -> His in every row (all globins)
myg = [r for r in aln if 'MYG_PHYMC' in r.id][0]
s2a, a2s = ns['coordinate_map'](myg)
col = int(s2a[93])
colres = [str(r.seq)[col] for r in aln]
print('   MYG_PHYMC residue index 93 -> column', col, '| residues in that column:', ''.join(colres))
check('A. coordinate_map on lowercase/"-"-mixed hmmalign row: residue index 93 (proximal His) lands in a column where all 8 globins have H', set(c.upper() for c in colres) == {'H'} and str(myg.seq)[col] == 'H')
seq_ungapped = ''.join(c for c in str(myg.seq) if c.isalpha())
uni = {r.id.split('|')[2]: str(r.seq) for r in SeqIO.parse(GLOBINS_FA, 'fasta')}['MYG_PHYMC']
check('A. hmmalign row ungapped == the UniProt sequence (no residue lost or invented) and coordinate_map has exactly that many residues', seq_ungapped.upper() == uni and len(s2a) == len(uni))
# cleaning keeps PP / RF
cl = ns['remove_gappy_columns'](aln, 0.5)
keep = [j for j in range(L) if isgap[:, j].mean() < 0.5]
print('   remove_gappy_columns(0.5):', cl.get_alignment_length(), 'of', L, '| column_annotations', {k: v[:30] for k, v in cl.column_annotations.items()})
pp_key = [k for k in aln[0].letter_annotations][0]
ok_pp = all(cl[i].letter_annotations[pp_key] == ''.join(gr[(n, 'PP')][j] for j in keep) for i, n in enumerate(names))
ok_gc = all(cl.column_annotations[k] == ''.join(gc[t][j] for j in keep) for k, t in [('reference_annotation', 'RF')] if k in cl.column_annotations)
check('A. after remove_gappy_columns: every row\'s PP letter-annotation and the RF column annotation equal the raw-file lines sliced to the kept columns', ok_pp and ok_gc and cl.get_alignment_length() == len(keep), f'{cl.get_alignment_length()} columns kept, GR key {pp_key}')
buf = io.StringIO(); AlignIO.write(cl, buf, 'stockholm'); t = buf.getvalue()
check('A. cleaned hmmalign alignment written as Stockholm keeps the #=GR PP lines and the RF/PP_cons #=GC lines', t.count(' PP ') >= 8 and '#=GC RF' in t and '#=GC PP_cons' in t, f'PP lines {t.count(" PP ")}')
# A2M version from hmmalign --outformat a2m: real HMMER 3.4 output is NOT padded (A3M-like), so AlignIO cannot read it
import a2m_a3m_io
sys.path.insert(0, EX)
a2m_recs = list(SeqIO.parse(os.path.join(DATA, 'hmmalign_globins8.a2m'), 'fasta'))
lens = [len(r.seq) for r in a2m_recs]
print('   hmmalign --outformat a2m row lengths:', lens, '| "." characters:', sum(str(r.seq).count('.') for r in a2m_recs))
try:
    AlignIO.read(os.path.join(DATA, 'hmmalign_globins8.a2m'), 'fasta'); a2m_err = None
except ValueError as e:
    a2m_err = str(e)
check('A. OBSERVATION on real HMMER 3.4 output: `hmmalign --outformat a2m` rows are NOT padded (lengths differ, no "." characters), so the SKILL example AlignIO.read(..., "fasta") raises ValueError on it',
      len(set(lens)) > 1 and a2m_err is not None and all('.' not in str(r.seq) for r in a2m_recs), f'{a2m_err}; lengths {sorted(set(lens))}')
pex = run_ex('a2m_a3m_io.py', os.path.join(DATA, 'hmmalign_globins8.a2m'))
print('   shipped examples/a2m_a3m_io.py on the real hmmalign A2M: rc =', pex.returncode, '|', pex.stderr.strip().splitlines()[-1] if pex.stderr.strip() else '')
check('A. the shipped examples/a2m_a3m_io.py handles real `hmmalign --outformat a2m` output (rc 0, prints 117 match columns)  [expected to FAIL: it reads with AlignIO, which needs padded rows]', pex.returncode == 0 and '117 match columns' in pex.stdout, f'rc {pex.returncode}: {pex.stderr.strip().splitlines()[-1] if pex.stderr.strip() else ""}')
mo = a2m_a3m_io.match_only_columns(a2m_recs)      # the helper itself iterates records, so it still works on the unpadded file
n_match_rf = gc['RF'].count('x')
check('A. match_only_columns applied to the unpadded HMMER A2M records: every row has exactly 117 match columns (= profile LENG = RF x count)', {len(m) for m in mo} == {117} and n_match_rf == 117, f'{sorted({len(m) for m in mo})}')
rf_cols = [j for j, ch in enumerate(gc['RF']) if ch == 'x']
rf_rows = [''.join(seqs[n][j] for j in rf_cols).replace('.', '-').upper() for n in names]
check('A. the A2M match-only strings equal the Stockholm RF-column strings (two hmmalign outputs, same 117 columns, case-folded)', [m.upper() for m in mo] == rf_rows)
import pyhmmer
with pyhmmer.easel.MSAFile(os.path.join(DATA, 'hmmalign_globins8.a2m'), format='a2m') as f:
    padded = f.read()
prow = list(padded.alignment)
print('   pyhmmer MSAFile(format="a2m") padded widths:', sorted({len(x) for x in prow}), '| first row start:', prow[0][:40])
check('A. the SKILL hand-off (pyhmmer MSAFile(format="a2m")) does pad the unpadded HMMER A2M to a rectangle, and its match-only columns equal the 117 RF columns',
      len({len(x) for x in prow}) == 1 and [m.upper() for m in a2m_a3m_io.match_only_columns([SeqRecord(Seq(x), id=str(i)) for i, x in enumerate(prow)])] == rf_rows)
nl = ns['normalize_alignment'](MultipleSeqAlignment([SeqRecord(Seq(x), id=str(i)) for i, x in enumerate(prow)]), upper=False)
check('A. normalize_alignment(upper=False) on the padded A2M keeps lowercase insert states and maps "." -> "-"', any(c.islower() for c in str(nl[0].seq)) and '.' not in str(nl[0].seq))
# Henikoff on the hmmalign alignment vs independent
def hk(a, g):
    w = np.zeros(a.shape[0]); used = 0
    for j in range(a.shape[1]):
        if g[:, j].any(): continue
        used += 1; c = Counter(a[:, j]); k = len(c)
        for i in range(a.shape[0]): w[i] += 1 / (k * c[a[i, j]])
    return w / w.sum(), used
wi, used = hk(up, isgap); wsk = ns['henikoff_weights'](aln)
check('A. henikoff_weights on the hmmalign alignment (mixed case, "." and "-") equals independent weights; only gap-free columns used', np.abs(wsk - wi).max() < 1e-12 and used > 50, f'{used} gap-free columns of {L}')

# ============ B. real nucleotide alignment: six HBB CDS, MAFFT ==============================================================================
dna = AlignIO.read(os.path.join(DATA, 'hbb6_cds_mafft.fasta'), 'fasta')
d = np.array([list(str(r.seq).upper()) for r in dna]); dg = d == '-'; nd, ld = d.shape
print(f'B. HBB CDS alignment {nd} x {ld}; alphabet {sorted(set(d.ravel()))}')
check('B. real DNA alignment is detected as nucleotide; consensus placeholder is N, and the start codon column triple is ATG', ns['is_nucleotide'](dna) and ns['consensus_sequence'](dna, 0.5)[:3] == 'ATG')
cd = ns['consensus_sequence'](dna, 0.5)
def indep_dna(thr):
    o = []
    for j in range(ld):
        c = Counter(d[~dg[:, j], j])
        if not c: o.append('-'); continue
        t, n = c.most_common(1)[0]; o.append(t if n / nd >= thr else 'N')
    return ''.join(o)
check('B. DNA consensus 0.5 and 1.0 equal the independent consensus', cd == indep_dna(0.5) and ns['consensus_sequence'](dna, 1.0) == indep_dna(1.0))
# soft-mask 25% of bases (seeded) -> results must not change (case-insensitive)
rng = np.random.default_rng(3)
mask_rows = []
from Bio.Align import MultipleSeqAlignment
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
for r in dna:
    s = list(str(r.seq).upper()); low = rng.random(len(s)) < 0.25
    mask_rows.append(SeqRecord(Seq(''.join(ch.lower() if lo and ch != '-' else ch for ch, lo in zip(s, low))), id=r.id))
soft = MultipleSeqAlignment(mask_rows)
print('   soft-masked row 0:', str(soft[0].seq)[:60])
check('B. 25% soft-masked (lowercase) version of the same alignment gives the identical consensus, conserved columns and Henikoff weights',
      ns['consensus_sequence'](soft, 0.5) == cd and ns['find_conserved_positions'](soft, 1.0) == ns['find_conserved_positions'](dna, 1.0) and np.allclose(ns['henikoff_weights'](soft), ns['henikoff_weights'](dna)))
n_full = len(ns['find_conserved_positions'](dna, 1.0)); ind_full = sum(1 for j in range(ld) if not dg[:, j].any() and len(set(d[:, j])) == 1)
check('B. count of fully conserved nucleotide columns == independent', n_full == ind_full, f'{n_full} of {ld}')
import neff as neff_mod
def indep_neff(a, thr):
    n = a.shape[0]; size = np.ones(n)
    for i in range(n):
        for j in range(i + 1, n):
            m = (a[i] != '-') & (a[j] != '-')
            if m.sum() and (a[i][m] == a[j][m]).sum() / m.sum() >= thr: size[i] += 1; size[j] += 1
    return (1 / size).sum()
n80 = neff_mod.neff(dna, 0.80)
mi_id = min(((d[i] == d[j]) & ~dg[i] & ~dg[j]).sum() / (~dg[i] & ~dg[j]).sum() for i in range(nd) for j in range(i + 1, nd))
check(f'B. Neff at the 0.80 nucleotide convention == independent; all six orthologs are >= 0.80 identical pairwise (min {mi_id:.3f}), so they form one cluster and Neff = 1', abs(n80 - indep_neff(d, 0.80)) < 1e-9 and mi_id >= 0.8 and abs(n80 - 1.0) < 1e-9, f'{n80:.6f}')
p = run_ex('consensus_sequence.py', os.path.join(DATA, 'hbb6_cds_mafft.fasta'))
lines = p.stdout.splitlines(); got50 = lines[lines.index('Consensus (50% threshold):') + 1]
check('B. shipped consensus_sequence.py on the DNA FASTA: rc 0 and its 50% consensus == independent (N placeholder)', p.returncode == 0 and got50 == indep_dna(0.5), p.stderr[-200:])

# ============ C. Pfam Ras seed (real, new family, from EBI) ======================================================================================
RAS = os.path.join(DATA, 'PF00071_seed.sto')
rs, rgr, rgc = parse_raw(RAS)
rn = list(rs); rL = len(rs[rn[0]])
rr = np.array([list(s.upper()) for s in rs.values()]); rg = np.isin(rr, ['.', '-'])
ras = AlignIO.read(RAS, 'stockholm')
print(f'C. Ras seed: {len(ras)} x {ras.get_alignment_length()}; raw gap chars {sorted(set(rr[rg]))}')
check('C. Ras seed: shape and IDs equal the raw file', (len(ras), ras.get_alignment_length()) == (len(rn), rL) and [r.id for r in ras] == rn)
check('C. Ras gaps_per_column == independent count; total gap cells equal', ns['gaps_per_column'](ras) == list(rg.sum(0)))
def indep_r(thr):
    o = []
    for j in range(rL):
        c = Counter(rr[~rg[:, j], j])
        if not c: o.append('-'); continue
        t, n = c.most_common(1)[0]; o.append(t if n / len(rn) >= thr else 'X')
    return ''.join(o)
cr = ns['consensus_sequence'](ras, 0.5)
check('C. Ras consensus (0.5) == independent', cr == indep_r(0.5))
print('   Ras consensus 0.5:', cr)
check('C. biology: the P-loop GxxxxGK[ST] is recovered by the 50% consensus of the Ras seed', re.search(r'G.{4}GK', cr) is not None, re.search(r'G.{4}GK.', cr).group(0) if re.search(r'G.{4}GK.', cr) else 'not found')
fc = ns['find_conserved_positions'](ras, 0.9)
ind = [(j, *Counter(rr[~rg[:, j], j]).most_common(1)[0]) for j in range(rL) if rg[:, j].any() or True]
ind = [(j, t) for j, t, n in ind if n / len(rn) >= 0.9 - 1e-12]
check('C. Ras conserved (>=0.9) columns == independent', [(a, b) for a, b, _ in fc] == ind, f'{len(ind)} columns')
wr = ns['henikoff_weights'](ras); wri, ur = hk(rr, rg)
check('C. Ras Henikoff weights == independent (gap-free columns only)', np.abs(wr - wri).max() < 1e-12, f'{ur} gap-free columns')
nr = neff_mod.neff(ras, 0.62)
pm = run_ex('mi_apc.py', RAS)
print(pm.stdout[:400], pm.stderr[-300:])
npl = nr / rL
check('C. mi_apc.py on the Ras seed: the guard fires exactly when the SKILL rule says (L > 100 and Neff/L > 1): warning present iff the rule fails; matches my own Neff/L', pm.returncode == 0 and (('WARNING' in pm.stdout) == (not (rL > 100 and npl > 1))), f'L={rL} Neff={nr:.2f} Neff/L={npl:.2f}; WARNING in output: {"WARNING" in pm.stdout}')
m = re.search(r'WARNING: L=(\d+), Neff/L=([0-9.]+)', pm.stdout)
check('C. the L and Neff/L printed by the warning equal my own numbers', m is not None and int(m.group(1)) == rL and abs(float(m.group(2)) - round(npl, 2)) < 0.006, m.group(0) if m else 'no warning')
summary()
