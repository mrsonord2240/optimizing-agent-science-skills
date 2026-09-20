"""Input 5 (Stress): 'Weight the sequences of the Pfam globin seed (Henikoff), report Neff and Neff/L, and find coevolving column pairs with MI-APC.'
REAL data: Pfam PF00042 seed 73 x 141. Code: SKILL.md henikoff_weights (verbatim) + shipped examples/{henikoff_weights,neff,mi_apc}.py imported from a COPY.
Ground truth: pyhmmer (Easel) weights, hand-rolled independent Henikoff, scipy entropy MI, hmmbuild eff_nseq (in5_hmmbuild.sh)."""
import os, sys, time, shutil, importlib.util, warnings, re
import numpy as np
from Bio import AlignIO
from scipy.stats import spearmanr, entropy
import pyhmmer
from common import *
import skill_md_funcs as F

aln = AlignIO.read(PFAM_STO, 'stockholm')
N, L = len(aln), aln.get_alignment_length()
arr = np.array([list(str(r.seq)) for r in aln])
rows = [str(r.seq) for r in aln]
ex = os.path.join(HERE, 'ex5'); shutil.rmtree(ex, ignore_errors=True); shutil.copytree(SKILL_EX, ex)
def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ex, name + '.py')); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
hw, neffm, mim = load('henikoff_weights'), load('neff'), load('mi_apc')

# ---------- A. Henikoff ----------
w_md = F.henikoff_weights(aln); w_ex = hw.henikoff_weights(aln)
check('SKILL.md henikoff_weights == examples/henikoff_weights.py (two copies agree numerically)', np.allclose(w_md, w_ex))
check('weights sum to 1 and are all finite', abs(w_md.sum() - 1) < 1e-9 and np.isfinite(w_md).all(), f'sum={w_md.sum():.6f}')
def indep_henikoff(rws):
    n = len(rws); w = [0.0] * n
    for j in range(len(rws[0])):
        col = [r[j] for r in rws]
        if '-' in col: continue
        cnt = {}
        for c in col: cnt[c] = cnt.get(c, 0) + 1
        for i, c in enumerate(col): w[i] += 1.0 / (len(cnt) * cnt[c])
    t = sum(w); return np.array([x / t for x in w])
wi = indep_henikoff(rows)
check('SKILL weights == independent textbook Henikoff over gap-free columns (max abs diff < 1e-12)', np.abs(wi - w_md).max() < 1e-12, f'max diff {np.abs(wi - w_md).max():.2e}')
ungapped_cols = int(sum(1 for j in range(L) if '-' not in arr[:, j]))
print(f'gap-free columns used: {ungapped_cols} of {L}; zero-weight sequences: {(w_md == 0).sum()}')
with pyhmmer.easel.MSAFile(PFAM_STO, digital=True) as f:
    msa = f.read()
msa.name = b'pf'
pb = np.array(msa.compute_weights('pb'), dtype=float).copy()
print('pyhmmer pb weights: sum', pb.sum().round(3), 'min', pb.min().round(3), 'max', pb.max().round(3))
pbn = pb / pb.sum()
rho = spearmanr(w_md, pbn).correlation
print(f'Spearman(skill Henikoff, Easel PB) = {rho:.3f}; max abs diff of normalised weights = {np.abs(w_md - pbn).max():.4f}')
check('Easel PB weights sum to N (=73): they are per-sequence weights, NOT an Neff (Skill Neff table treats pb as the Neff baseline)', abs(pb.sum() - N) < 1e-6, f'sum={pb.sum():.3f}')
check('skill Henikoff weights correlate with Easel PB (Spearman > 0.9): same estimator family', rho > 0.9, f'rho={rho:.3f}')
check('skill Henikoff equals Easel PB after normalisation (example docstring claims it matches HMMER) [FAIL = claim overstated]', np.allclose(w_md, pbn, atol=1e-3), f'max diff {np.abs(w_md - pbn).max():.4f}')

class R:  # duck-typed alignment for SYNTHETIC inputs
    def __init__(s, rws): s.rws = rws
    def __len__(s): return len(s.rws)
    def __iter__(s): return iter([type('Rec', (), {'seq': r})() for r in s.rws])
allgap = R(['-CDE', 'A-DE', 'AC-E', 'ACD-'])   # SYNTHETIC: every column contains a gap
with warnings.catch_warnings(record=True) as wl:
    warnings.simplefilter('always')
    wz = F.henikoff_weights(allgap)
print('SYNTH every-column-gappy alignment -> weights', wz, '| warnings:', [str(x.message) for x in wl])
check('SYNTH every column has a gap: function returns finite weights or raises a clear error [FAIL = silent NaN]', bool(np.isfinite(wz).all()), str(wz))

# ---------- B. Neff ----------
t0 = time.time(); n62 = neffm.neff(aln, 0.62); n80 = neffm.neff(aln, 0.80); dt = time.time() - t0
print(f'skill Neff(0.62)={n62:.2f}  Neff(0.80)={n80:.2f}  L={L}  Neff/L={n62 / L:.3f}  ({dt:.1f}s)')
def indep_neff(rws, thr):
    n = len(rws); cs = [1] * n
    for i in range(n):
        for j in range(i + 1, n):
            pos = [k for k in range(len(rws[0])) if rws[i][k] != '-' and rws[j][k] != '-']
            if not pos: continue
            idn = sum(1 for k in pos if rws[i][k] == rws[j][k]) / len(pos)
            if idn >= thr: cs[i] += 1; cs[j] += 1
    return sum(1.0 / c for c in cs)
check('skill neff(0.62) == independent pure-python implementation', abs(indep_neff(rows, 0.62) - n62) < 1e-9, f'{indep_neff(rows, 0.62):.4f} vs {n62:.4f}')
check('skill neff(0.80) == independent implementation', abs(indep_neff(rows, 0.80) - n80) < 1e-9)
with pyhmmer.easel.MSAFile(PFAM_STO, digital=True) as f:
    msa2 = f.read()
msa2.name = b'pf2'
bl = np.array(msa2.compute_weights('blosum', max_identity=0.62), dtype=float)
print('Easel BLOSUM(0.62) weight sum:', bl.sum().round(3))
check('Easel BLOSUM weights also sum to N: any pyhmmer compute_weights() output needs conversion to an Neff, which the Skill never states', abs(bl.sum() - N) < 1e-6)
hb = os.path.join(HERE, 'data', 'hmmbuild_out.txt')
effn = None
if os.path.exists(hb):
    txt = open(hb, encoding='utf-8').read()
    m = re.search(r'^\s*1\s+\S+\s+(\d+)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)', txt, re.M)   # idx name nseq alen mlen eff_nseq re/pos
    effn = float(m.group(4)) if m else None
print('hmmbuild eff_nseq (entropy-weighted Neff, what HMMER reports):', effn, '| skill Neff(0.62)=', round(n62, 2), 'Neff(0.80)=', round(n80, 2))
check('hmmbuild eff_nseq parsed from real hmmbuild output', effn is not None)
if effn:
    ratio = n62 / effn
    print(f'ratio skill Neff(0.62) / hmmbuild eff_nseq = {ratio:.2f}; ratio to sum of pb weights (N=73) = {n62 / pb.sum():.2f}')
    check('skill Neff(0.62) is within the 0.5-3x band of the sum of HMMER pb weights (the Skill table "baseline")', 0.5 <= n62 / pb.sum() <= 3.0, f'ratio {n62 / pb.sum():.2f}')
    check('Skill says estimators differ "often 2-3x": skill Neff(0.62) vs the Neff HMMER actually reports (hmmbuild eff_nseq) within 3x [FAIL = 10x, understated]', 0.33 <= ratio <= 3.0, f'ratio {ratio:.2f} (eff_nseq {effn})')
check("Neff/L computed and below the skill's DCA thresholds (0.5) on this real seed => the Skill's own guard says do NOT apply APC", n62 / L < 0.5, f'Neff/L={n62 / L:.3f}')

# ---------- C. MI-APC ----------
t0 = time.time(); C = mim.mi_matrix_apc(aln); dt = time.time() - t0
print(f'mi_apc.py: matrix {C.shape}, {dt:.1f}s')
def indep_mi(a, b):
    m = (a != '-') & (b != '-')
    if m.sum() < 20: return None
    a, b = a[m], b[m]
    keys = {}
    for x, y in zip(a, b): keys[(x, y)] = keys.get((x, y), 0) + 1
    def H(v):
        c = {}
        for x in v: c[x] = c.get(x, 0) + 1
        return entropy(list(c.values()), base=2)
    return H(a) + H(b) - entropy(list(keys.values()), base=2)
MI = np.zeros((L, L)); val = np.zeros((L, L), bool)
for i in range(L):
    for j in range(i + 1, L):
        v = indep_mi(arr[:, i], arr[:, j])
        if v is not None: MI[i, j] = MI[j, i] = v; val[i, j] = val[j, i] = True
cm = np.array([MI[k, val[k]].mean() if val[k].any() else 0 for k in range(L)])
apc = np.outer(cm, cm) / MI[val].mean()
ref = MI - apc
check('MI-APC matrix == independent scipy-entropy MI (H(a)+H(b)-H(a,b)) minus APC, max abs diff < 1e-9', np.abs(C - ref).max() < 1e-9, f'max diff {np.abs(C - ref).max():.2e}')
check('MI-APC symmetric', np.allclose(C, C.T))
check('raw MI is non-negative (up to fp)', bool((MI >= -1e-12).all()))
iu = np.triu_indices(L, 1)
top = sorted(zip(C[iu], iu[0], iu[1]), reverse=True)[:20]
print('top5 MI-APC pairs:', [(int(i), int(j), round(float(s), 3)) for s, i, j in top[:5]])
print('sequence separations of top 20:', [int(abs(i - j)) for _, i, j in top])
src = open(os.path.join(ex, 'mi_apc.py'), encoding='utf-8').read()
main_src = src.split("__main__")[1]
check("shipped mi_apc.py enforces the SKILL.md guard ('apply APC only when L>100 and Neff/L>1') [FAIL = applies APC unconditionally, no warning]", ('neff' in main_src.lower()) or ('warn' in main_src.lower()))
class Aln2:
    def __init__(s, a): s.a = a
    def __len__(s): return s.a.shape[0]
    def __iter__(s): return iter([type('Rec', (), {'seq': ''.join(r)})() for r in s.a])
null_max = []
for seed in range(5):
    rng = np.random.default_rng(seed)
    sh = np.array([rng.permutation(arr[:, j]) for j in range(L)]).T
    Cs = mim.mi_matrix_apc(Aln2(sh)); null_max.append(float(Cs[iu].max()))
print(f'real top MI-APC {C[iu].max():.3f} vs column-shuffled null top (5 seeds) {np.round(null_max, 3)}')
check('real max MI-APC exceeds the max over 5 column-shuffled nulls (signal above noise) [FAIL = indistinguishable from noise at Neff/L<0.5]', C[iu].max() > max(null_max), f'{C[iu].max():.3f} vs {max(null_max):.3f}')

# contact enrichment against REAL 1MBN using the seed row most similar to 1MBN
from Bio.PDB import PDBParser
from Bio.Align import PairwiseAligner, substitution_matrices
from Bio.PDB.Polypeptide import three_to_index, index_to_one
chain = PDBParser(QUIET=True).get_structure('m', r'F:\OpenScience\audit-envs\alignment\public-data\structures\1MBN.pdb')[0]['A']
resl = [r for r in chain if r.id[0] == ' ']
pseq = ''.join(index_to_one(three_to_index(r.get_resname())) for r in resl)
pa = PairwiseAligner(); pa.substitution_matrix = substitution_matrices.load('BLOSUM62'); pa.open_gap_score = -10; pa.extend_gap_score = -0.5; pa.mode = 'global'
best = max(range(N), key=lambda i: pa.score(pseq, rows[i].replace('-', '')))
bseq = rows[best].replace('-', '')
al = pa.align(pseq, bseq)[0]
m_r = {}
for (a0, a1), (b0, b1) in zip(*al.aligned):
    for k in range(a1 - a0): m_r[b0 + k] = a0 + k
s2a, a2s = F.coordinate_map(aln[best])
# col2res maps alignment column -> 1MBN residue index
col2res = {}
for bseq_idx, pdb_idx in m_r.items():
    col2res[int(s2a[bseq_idx])] = pdb_idx
ident = sum(1 for k, v in m_r.items() if bseq[k] == pseq[v]) / len(m_r)
print(f'best seed row {aln[best].id} ~ 1MBN: {len(m_r)} mapped residues, {ident * 100:.0f}% identity')
cache = {}
def contact(ci, cj):
    ri, rj = col2res[ci], col2res[cj]
    if (ri, rj) not in cache:
        cache[(ri, rj)] = min(np.linalg.norm(a.coord - b.coord) for a in resl[ri] for b in resl[rj] if a.element != 'H' and b.element != 'H') < 8.0
    return cache[(ri, rj)]
mapped = sorted(((C[i, j], i, j) for i in range(L) for j in range(i + 6, L) if i in col2res and j in col2res and val[i, j]), reverse=True)
topk = mapped[:30]
prec = float(np.mean([contact(i, j) for _, i, j in topk]))
base = float(np.mean([contact(i, j) for _, i, j in mapped[::max(1, len(mapped) // 400)]]))
print(f'top-30 MI-APC pairs (|i-j|>=6, mapped to 1MBN): contact precision {prec:.2f} vs all-pair baseline {base:.2f} (8 A heavy-atom)')
mapped_raw = sorted(((MI[i, j], i, j) for i in range(L) for j in range(i + 6, L) if i in col2res and j in col2res and val[i, j]), reverse=True)
prec_raw = float(np.mean([contact(i, j) for _, i, j in mapped_raw[:30]]))
print(f'top-30 RAW MI contact precision {prec_raw:.2f} (Skill says raw MI is preferable when L<100 or Neff/L<1)')
check('MI-APC top-30 contact precision vs 1MBN exceeds all-pair baseline (measured, not a Skill claim)', prec > base, f'{prec:.2f} vs baseline {base:.2f}')
summary()
