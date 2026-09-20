"""Input 9 (NEW, not a first-audit input; Stress): the parts of the Skill the real Pfam seed cannot exercise, on SYNTHETIC alignments
with planted, hand-known structure (seeded, deterministic).
'(a) My 35-sequence alignment is 30 near-identical clones plus 5 divergent sequences: weight it, tell me the effective number of
sequences, and give me a consensus and conserved columns that do not just follow the over-represented clade.
(b) I have a deep alignment (400 sequences, 120 columns): find coevolving pairs with MI-APC, and tell me when the tool refuses.'
Ground truth: closed-form Henikoff / Neff by hand, planted coupled columns, scipy entropy MI, the SKILL guard L > 100 and Neff/L > 1."""
import os, re, subprocess, sys, warnings
from collections import Counter
import numpy as np
from scipy.stats import entropy
from Bio import AlignIO
from Bio.Align import MultipleSeqAlignment
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from common import *
import skillns

ns, _ = skillns.load()
sys.path.insert(0, EX)
import neff as neff_mod, mi_apc
AA = list('ACDEFGHIKLMNPQRSTVWY')
mk = lambda rows, ids=None: MultipleSeqAlignment([SeqRecord(Seq(s), id=(ids[i] if ids else f's{i}')) for i, s in enumerate(rows)])
env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONIOENCODING': 'utf-8'}

# ================= (a) redundant clade ===================================================================================================
rng = np.random.default_rng(11)
NC, ND, LC = 30, 5, 40
cols_clone, cols_div = [], []
for c in range(LC):
    if c < 6:       # type 1 (6 cols): clones A, all five divergent G          -> unweighted 30/35 A; weighted tie A/G at 0.5
        cols_clone.append('A'); cols_div.append(['G'] * ND)
    elif c < 16:    # type 3 (10 cols): clones A, divergent G,G,G,T,T           -> weighted A = 1/3
        cols_clone.append('A'); cols_div.append(['G', 'G', 'G', 'T', 'T'])
    elif c < 34:    # type 2 (18 cols): clones A, five distinct divergent residues -> weighted A = 1/6
        cols_clone.append('A'); cols_div.append(['C', 'D', 'E', 'F', 'H'])
    else:           # type 0: everybody identical
        cols_clone.append('W'); cols_div.append(['W'] * ND)
clones = [''.join(cols_clone)] * NC
# make the divergent five differ pairwise and from the clones in the type-0 free part: all identical only in the last 10 columns -> identity(div,clone) low
divs = [''.join(cols_div[c][k] for c in range(LC)) for k in range(ND)]
rows = clones + divs
aln = mk(rows, [f'clone{i}' for i in range(NC)] + [f'div{i}' for i in range(ND)])
arr = np.array([list(r) for r in rows])
# --- independent Henikoff by column loop
def hk(a):
    w = np.zeros(a.shape[0])
    for j in range(a.shape[1]):
        c = Counter(a[:, j]); k = len(c)
        for i in range(a.shape[0]): w[i] += 1 / (k * c[a[i, j]])
    return w / w.sum()
w_ind = hk(arr)
w = ns['henikoff_weights'](aln)
print('clone weight each:', w[0], '| divergent weights:', np.round(w[NC:], 4), '| clone group total:', w[:NC].sum())
# hand: per column the clone GROUP gets 1/k of the column: type1 k=2 -> .5 ; type3 k=3 -> 1/3 ; type2 k=6 -> 1/6 ; type0 k=1 -> 30/35 (each of 35 sequences gets 1/35) => (6*.5 + 10/3 + 18*(1/6) + 6*30/35)/40
hand_group = (6 * 0.5 + 10 / 3 + 18 / 6 + 6 * 30 / 35) / 40   # type-0 columns: k = 1, every sequence gets 1/35, the 30 clones get 30/35
check('SKILL henikoff_weights: equals the independent column-loop implementation; sums to 1', np.abs(w - w_ind).max() < 1e-12 and abs(w.sum() - 1) < 1e-12)
check(f'Henikoff clone-group weight equals the closed-form hand value {hand_group:.4f} (was 30/35 = 0.857 unweighted)', abs(w[:NC].sum() - hand_group) < 1e-12 and hand_group < 0.5, f'{w[:NC].sum():.4f}')
n_eff = neff_mod.neff(aln, 0.62)
print('Neff(0.62) =', n_eff)
ident = lambda a, b: (a == b).mean()
mx_div = max(ident(arr[NC + i], arr[NC + j]) for i in range(ND) for j in range(i + 1, ND)); mx_dc = max(ident(arr[NC + i], arr[0]) for i in range(ND))
check(f'Neff(0.62) == 6.0 by hand (30 identical clones = one cluster of 30 -> 1, five singletons; max identity div-div {mx_div:.2f}, div-clone {mx_dc:.2f} both < 0.62)', abs(n_eff - 6.0) < 1e-9 and max(mx_div, mx_dc) < 0.62, f'{n_eff:.6f}')
cu = ns['consensus_sequence'](aln, 0.5); cw = ns['consensus_sequence'](aln, 0.5, weights=w)
print('unweighted consensus @0.5:', cu); print('weighted   consensus @0.5:', cw)
# hand: cols 0-9 unweighted A, weighted A = .5 exactly -> tie A vs G .5/.5 -> first seen (A) kept (>= .5); cols 10-19 unweighted A, weighted A=1/3 -> X; cols 20-29 unweighted A, weighted A 1/6 -> X; cols 30-39 W
check('unweighted consensus follows the clone clade (A in cols 0-33) and weighted consensus does not in cols 6-33 (X = no residue reaches 50%)',
      cu == 'A' * 34 + 'W' * 6 and cw[6:34] == 'X' * 28 and cw[34:] == 'W' * 6, cw)
fu = {c for c, _, _ in ns['find_conserved_positions'](aln, 0.8)}; fw = {c for c, _, _ in ns['find_conserved_positions'](aln, 0.8, weights=w)}
check('conserved columns at 0.8: unweighted calls all 40 (clade columns 0-33 + identical 34-39); weighted keeps only the 6 all-identical columns (34-39)', fu == set(range(40)) and fw == set(range(34, 40)), f'{len(fu)} vs {len(fw)}')

# ================= (b) deep alignment, planted coupling =================================================================================
N, L = 400, 120
rng = np.random.default_rng(2026)
P = rng.dirichlet(np.full(20, 0.6), size=L)                      # per-column residue distribution (independent columns)
X = np.array([rng.choice(20, size=N, p=P[j]) for j in range(L)]).T  # N x L residue indices
def couple(i, j, noise, seed):
    r = np.random.default_rng(seed); perm = r.permutation(20)
    Xj = perm[X[:, i]]; flip = r.random(N) < noise
    X[flip, j] = r.integers(0, 20, flip.sum()); X[~flip, j] = Xj[~flip]
couple(10, 60, 0.10, 1); couple(25, 90, 0.15, 2)
deep_rows = [''.join(AA[k] for k in row) for row in X]
deep = mk(deep_rows)
AlignIO.write(deep, os.path.join(DATA, 'syn_deep400x120.fasta'), 'fasta')
darr = np.array([list(r) for r in deep_rows]); dg = np.zeros(darr.shape, bool)
nf = neff_mod.neff(deep, 0.62)
print(f'deep alignment {N} x {L}: Neff(0.62) = {nf:.1f}, Neff/L = {nf / L:.2f}')
check('SYNTH deep alignment satisfies the guard: L = 120 > 100 and Neff/L > 1 (Neff ~ N for independent sequences)', mi_apc.apc_applicable(deep)[0] and nf / L > 1, f'Neff/L {nf / L:.2f}')
with warnings.catch_warnings(record=True) as wr:
    warnings.simplefilter('always')
    mi_ap = mi_apc.mi_matrix_apc(deep)
check('mi_matrix_apc on the deep alignment raises no warning (guard passes)', len(wr) == 0, str([str(x.message) for x in wr]))
iu = np.triu_indices(L, 1)
order = np.argsort(-mi_ap[iu])
top = [(int(iu[0][k]), int(iu[1][k]), round(float(mi_ap[iu][k]), 3)) for k in order[:5]]
print('top 5 MI-APC pairs:', top)
check('planted pairs are recovered: (10,60) ranks 1st and (25,90) ranks 2nd of 7140 pairs', (top[0][0], top[0][1]) == (10, 60) and (top[1][0], top[1][1]) == (25, 90), str(top[:3]))
# independent MI + APC
def indep_mi(a, min_pairs=20):
    n, l = a.shape; codes = np.zeros(a.shape, int)
    for j in range(l):
        u = {ch: k for k, ch in enumerate(sorted(set(a[:, j])))}; codes[:, j] = [u[c] for c in a[:, j]]
    mi = np.zeros((l, l))
    for i in range(l):
        for j in range(i + 1, l):
            ci, cj = codes[:, i], codes[:, j]; joint = np.bincount(ci * 20 + cj, minlength=400).astype(float)
            mi[i, j] = mi[j, i] = entropy(np.bincount(ci), base=2) + entropy(np.bincount(cj), base=2) - entropy(joint[joint > 0], base=2)
    return mi
mi_i = indep_mi(darr)
off = ~np.eye(L, dtype=bool); cm = np.array([mi_i[k, off[k]].mean() for k in range(L)]); apc_i = np.outer(cm, cm) / mi_i[off].mean()
check('MI-APC of the deep alignment == independent scipy-entropy MI minus Dunn-2008 APC (max abs diff < 1e-9)', np.abs(mi_ap - (mi_i - apc_i)).max() < 1e-9, f'{np.abs(mi_ap - (mi_i - apc_i)).max():.1e}')
# hand-checkable MI values on tiny columns: [A,A,B,B] vs [C,C,D,D] -> 1 bit ; vs [C,D,C,D] -> 0 ; 3:1 split -> 0.8113
tiny = np.array([list('AACC'), list('AACD'), list('BBDC'), list('BBDD')])   # cols: 0 = A,A,B,B ; 1 = A,A,B,B ; 2 = C,C,D,D ...
from mi_apc import mi_from_array
mt, _ = mi_from_array(np.array([list('ACC'), list('ACD'), list('BDC'), list('BDD')]), min_pairs=4)
check('MI by hand: [A,A,B,B] vs [C,C,D,D] = 1 bit, vs [C,D,C,D] = 0 bits', abs(mt[0, 1] - 1.0) < 1e-12 and abs(mt[0, 2] - 0.0) < 1e-12, f'{mt[0, 1]:.4f} {mt[0, 2]:.4f}')
nm, _ = mi_from_array(np.array([list('AC'), list('AC'), list('AC'), list('BD')]), min_pairs=4)
check('MI by hand: 3:1 perfectly coupled split = H(0.75,0.25) = 0.8113 bits', abs(nm[0, 1] - 0.8112781244591328) < 1e-12, f'{nm[0, 1]:.6f}')
# CLI run from the copy
p = subprocess.run([sys.executable, os.path.join(EX, 'mi_apc.py'), os.path.join(DATA, 'syn_deep400x120.fasta')], cwd=DATA, capture_output=True, text=True, env=env, timeout=1800)
lines = p.stdout.splitlines()
print('\n'.join(lines[:5]), '\n...', lines[-1], p.stderr[-200:])
first = [l for l in lines if re.match(r'\s+\d+-\s*\d+:', l)][:2]
null_max = float(re.search(r'null max = ([0-9.]+)', p.stdout).group(1)); n_above = int(re.search(r'(\d+) of the top 20 exceed', p.stdout).group(1))
pairs_cli = [tuple(map(int, re.match(r'\s+(\d+)-\s*(\d+):', l).groups())) for l in lines if re.match(r'\s+\d+-\s*\d+:', l)]
check('mi_apc.py CLI on the deep alignment: rc 0, no WARNING, labelled MI-APC, top two pairs are 10-60 and 25-90, both > 5x the shuffled null, and they are the only flagged-above-null pairs among the leaders',
      p.returncode == 0 and 'WARNING' not in p.stdout and 'MI-APC' in lines[0] and pairs_cli[:2] == [(10, 60), (25, 90)] and top[0][2] > 5 * null_max and top[1][2] > 5 * null_max and n_above >= 2,
      f'null max {null_max}; {n_above} of top 20 above null; cli pairs {pairs_cli[:3]}')
# null scale: independent column shuffle of the same alignment
r2 = np.random.default_rng(5); sh = darr.copy()
for k in range(L): sh[:, k] = r2.permutation(sh[:, k])
mis = indep_mi(sh); cms = np.array([mis[k, off[k]].mean() for k in range(L)]); aps = mis - np.outer(cms, cms) / mis[off].mean()
print('independent shuffled max MI-APC:', aps[iu].max(), '| shipped null:', null_max)
check('the shipped null is the right scale (within a factor of 2 of an independent column-shuffle max MI-APC) and far below the planted signal', 0.5 < null_max / aps[iu].max() < 2 and null_max < 0.3 * top[1][2], f'{null_max} vs {aps[iu].max():.3f}')

# ================= guard boundaries =================================================================================================
d100 = mk([r[:100] for r in deep_rows]); d101 = mk([r[:101] for r in deep_rows])
ok100, npl100, m100 = mi_apc.apc_applicable(d100); ok101, npl101, m101 = mi_apc.apc_applicable(d101)
print('L=100:', ok100, m100, '| L=101:', ok101)
check('guard boundary: L = 100 refuses (needs L > 100), L = 101 passes (same Neff/L > 1)', (not ok100) and ok101 and npl100 > 1 and npl101 > 1)
with warnings.catch_warnings(record=True) as w100:
    warnings.simplefilter('always'); r100 = mi_apc.mi_matrix_apc(d100)
check('L = 100: mi_matrix_apc warns and returns raw MI (not corrected); force=True gives MI-APC that differs', len(w100) == 1 and np.allclose(r100, indep_mi(darr[:, :100])) and not np.allclose(r100, mi_apc.mi_matrix_apc(d100, force=True)))
# Neff/L < 1 with L > 100: 400 rows made of only 60 distinct sequences (each repeated) -> Neff = 60 -> Neff/L = 0.5
uniq = deep_rows[:60]; red = mk([uniq[i % 60] for i in range(400)])
ok_r, npl_r, msg_r = mi_apc.apc_applicable(red)
print('redundant 400 = 60 x ~6.7 copies:', msg_r)
check('redundant alignment (400 rows, 60 distinct): Neff = 60, Neff/L = 0.50 -> guard refuses despite 400 sequences (raw row count is not depth)', (not ok_r) and abs(neff_mod.neff(red) - 60) < 1e-9 and abs(npl_r - 0.5) < 1e-9, f'{msg_r}')
summary()
