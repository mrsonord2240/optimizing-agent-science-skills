"""Input 5 (Stress, regression of first-audit input 5): 'Compute Henikoff sequence weights for the Pfam globin seed, report Neff
and Neff/L at 62% and 80% identity, and find the top coevolving column pairs with MI-APC (tell me if the alignment is deep enough).'
REAL Pfam PF00042 seed. Code = SKILL.md blocks (henikoff_weights, consensus...) exec'd from the file + examples/{henikoff_weights,
neff,mi_apc}.py run from the copy. Ground truth: raw-text parse, pyhmmer/Easel pb, hmmbuild 3.4 eff_nseq (wsl_tools.sh), scipy
entropy MI, real PDB 1MBN contacts."""
import os, re, subprocess, sys, warnings
from collections import Counter
import numpy as np
from scipy.stats import entropy, spearmanr
import pyhmmer
from Bio import AlignIO, Align
from Bio.Align import substitution_matrices
from Bio.PDB import PDBParser
from common import *
import skillns

ns, _ = skillns.load()
aln = AlignIO.read(PFAM_STO, 'stockholm')
raw = {}
for line in open(PFAM_STO, encoding='utf-8'):
    if line.startswith('#') or line.startswith('//') or not line.strip(): continue
    n, s = line.split(); raw[n] = s
arr = np.array([list(s.upper()) for s in raw.values()]); isgap = arr == '.'
N, L = arr.shape
env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONIOENCODING': 'utf-8'}
def run_ex(name, *args, timeout=600):
    return subprocess.run([sys.executable, os.path.join(EX, name), *args], cwd=os.path.join(DATA), capture_output=True, text=True, env=env, timeout=timeout)

# ---------------- Henikoff -------------------------------------------------------------------------------------------------
def indep_henikoff(a, g):
    w = np.zeros(a.shape[0]); used = 0
    for j in range(a.shape[1]):
        if g[:, j].any(): continue
        used += 1
        c = Counter(a[:, j]); k = len(c)
        for i in range(a.shape[0]): w[i] += 1.0 / (k * c[a[i, j]])
    return w / w.sum(), used
wi, used = indep_henikoff(arr, isgap)
w = ns['henikoff_weights'](aln)
print('gap-free columns used:', used, '| weights sum', w.sum(), 'min/max', w.min(), w.max())
check('SKILL.md henikoff_weights == independent textbook Henikoff over the gap-free columns (max abs diff < 1e-12), sums to 1', np.abs(w - wi).max() < 1e-12 and abs(w.sum() - 1) < 1e-12 and used == 72, f'diff {np.abs(w - wi).max():.1e}, {used} columns')
# hand-computed 4 x 5 example: SKILL's doc says the weights sum to 1
from Bio.Align import MultipleSeqAlignment
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
mk = lambda rows: MultipleSeqAlignment([SeqRecord(Seq(s), id=f's{i}') for i, s in enumerate(rows)])
hand = ns['henikoff_weights'](mk(['ACDAF', 'ACDAF', 'ACGCF', 'ACDCF']))
# columns: c0 all A (k=1): each 1/(1*4)=.25 ; c1 all C: .25 ; c2 D,D,G,D: k=2 counts D3 G1 -> D:1/6 G:1/2 ; c3 A,A,C,C: k=2 counts 2,2 -> 1/4 each ; c4 F all .25
exp = np.array([.25 + .25 + 1/6 + .25 + .25, .25 + .25 + 1/6 + .25 + .25, .25 + .25 + 1/2 + .25 + .25, .25 + .25 + 1/6 + .25 + .25]); exp = exp / exp.sum()
check('SYNTH 4 x 5 alignment: Henikoff weights equal the hand computation [7/30, 7/30, 3/10, 7/30] (each of 5 columns contributes 1, weights sum to 1)', np.allclose(hand, exp) and np.allclose(hand, [7/30, 7/30, 3/10, 7/30]), str(np.round(hand, 4)))
try:
    ns['henikoff_weights'](mk(['A-C', 'AG-', '-GC'])); ae = None
except ValueError as e:
    ae = str(e)
check('SYNTH every column has a gap: henikoff_weights raises ValueError with a pointer to pyhmmer/trimming (was silent NaN)', ae is not None and 'pyhmmer' in ae, ae)
check('henikoff_weights accepts "." gaps (skips those columns like "-")', np.allclose(ns['henikoff_weights'](mk(['AC.', 'ACD', 'AGD'])), ns['henikoff_weights'](mk(['AC-', 'ACD', 'AGD']))))

# ---------------- Easel pb: SKILL prose vs pyhmmer ------------------------------------------------------------------------------
with pyhmmer.easel.MSAFile(PFAM_STO, digital=True) as f:
    msa = f.read()
pb = np.array(msa.compute_weights(method='pb'), dtype=float)
bl = np.array(msa.compute_weights(method='blosum'), dtype=float)
print('pb sum', pb.sum(), '| blosum sum', bl.sum())
check('pyhmmer compute_weights pb and blosum weights sum to N = 73 (the SKILL snippet comment: "equals the number of sequences N, not an Neff")', abs(pb.sum() - 73) < 1e-9 and abs(bl.sum() - 73) < 1e-9)
rho = spearmanr(w, pb)[0]; mad = np.abs(w - pb / pb.sum()).max()
print(f'Spearman(skill Henikoff, Easel pb) = {rho:.3f}; max abs diff after rescaling pb to sum 1 = {mad:.4f}')
check('SKILL.md numbers reproduced: Spearman 0.909 and max abs difference 0.0091', abs(rho - 0.909) < 0.0005 and abs(mad - 0.0091) < 0.00005, f'{rho:.4f}, {mad:.5f}')
# SKILL prose: pb ignores gaps column by column, consensus columns only (>= 50% residues), divides by the residue count, rescales to N.
canon = set('ACDEFGHIKLMNPQRSTVWY'); iscan = np.vectorize(lambda c: c in canon)(arr)
cons = (~isgap).sum(0) / N >= 0.5
e = np.zeros(N)
for j in np.flatnonzero(cons):
    col = arr[:, j]; m = iscan[:, j]; c = Counter(col[m]); k = len(c)
    for i in np.flatnonzero(m): e[i] += 1.0 / (k * c[col[i]])
e = e / iscan[:, cons].sum(1); e = e * N / e.sum()
print('my Easel-pb reimplementation (consensus columns, canonical residues, /residue count, sum N) vs pyhmmer: max abs diff', np.abs(e - pb).max())
check('the SKILL.md description of Easel pb (gap-ignoring, consensus columns >= 50% residues, divided by residue count, rescaled to sum N) is CORRECT: an independent implementation reproduces pyhmmer to 1e-9', np.abs(e - pb).max() < 1e-9)
sk = open(os.path.join(SKILL, 'SKILL.md'), encoding='utf-8').read()
check('SKILL.md no longer says pb "includes gaps as a residue type" (was contradictory)', 'includes gaps' not in sk and 'considers only "consensus" columns' in sk)

# ---------------- Neff -----------------------------------------------------------------------------------------------------
sys.path.insert(0, EX)
import neff as neff_mod
def indep_neff(a, thr):
    n = a.shape[0]; size = np.ones(n)
    for i in range(n):
        for j in range(i + 1, n):
            m = (a[i] != '.') & (a[j] != '.')
            if m.sum() and (a[i][m] == a[j][m]).sum() / m.sum() >= thr: size[i] += 1; size[j] += 1
    return (1 / size).sum()
n62, n80 = neff_mod.neff(aln, 0.62), neff_mod.neff(aln, 0.80)
print(f'examples/neff.py: Neff(0.62) = {n62:.4f}, Neff(0.80) = {n80:.4f}; independent {indep_neff(arr, 0.62):.4f} / {indep_neff(arr, 0.80):.4f}')
check('neff() equals an independent pure-python implementation at 0.62 (66.08) and 0.80 (73.00)', abs(n62 - indep_neff(arr, 0.62)) < 1e-9 and abs(n80 - indep_neff(arr, 0.80)) < 1e-9 and round(n62, 2) == 66.08 and round(n80, 2) == 73.0)
hm = open(os.path.join(DATA, 'hmmbuild_out.txt'), encoding='utf-8').read()
eff = float(re.search(r'^\s*1\s+pf\s+73\s+141\s+117\s+([0-9.]+)', hm, re.M).group(1))
print('hmmbuild 3.4 eff_nseq:', eff)
check('SKILL.md Neff table rows reproduced by my own runs: Neff 66.08, pb weight sum 73.0, hmmbuild eff_nseq 6.35', round(n62, 2) == 66.08 and abs(pb.sum() - 73) < 1e-9 and abs(eff - 6.35) < 1e-9, f'{n62:.2f} / {pb.sum():.1f} / {eff}')
check('SKILL.md states the three numbers differ ~10-fold and to report which estimator was used', 'differ 10-fold' in sk and 'Always report which estimator was used' in sk)
ex_neff = run_ex('neff.py', PFAM_STO)
print(ex_neff.stdout, ex_neff.stderr[-200:])
check('examples/neff.py prints Neff 66.08 / 73.00 and Neff/L 0.469 and says Neff/L is below the rule (Neff/L > 1)', ex_neff.returncode == 0 and '66.08' in ex_neff.stdout and '73.00' in ex_neff.stdout and '0.469' in ex_neff.stdout and 'is below the Skill rule of thumb for MI-APC / DCA (Neff/L > 1)' in ex_neff.stdout)
allsrc = {f: open(os.path.join(EX, f), encoding='utf-8').read() for f in os.listdir(EX) if f.endswith('.py')}
stale = [f for f, t in allsrc.items() if re.search(r'Neff/L\s*>\s*0\.5|Neff/L > 0\.5|0\.5 sufficient', t)] + (['SKILL.md'] if re.search(r'Neff/L\s*>\s*0\.5', sk) else [])
check('the Neff/L threshold is stated ONE way everywhere (Neff/L > 1): no stale "> 0.5" in SKILL.md or any example', not stale, str(stale))
ex_h = run_ex('henikoff_weights.py', PFAM_STO)
lines = ex_h.stdout.splitlines()
wt = [float(l.rsplit(':', 1)[1]) for l in lines if re.match(r'^\S+/\d+-\d+: 0\.\d+', l)]
print('\n'.join(lines[:2]), '...', lines[-1])
check('examples/henikoff_weights.py prints 73 weights that match the independent weights to 4 dp, and labels the last figure Kish effective sample size (not "Effective sequences")',
      ex_h.returncode == 0 and len(wt) == 73 and np.allclose(wt, np.round(wi, 4), atol=6e-5) and 'Kish effective sample size' in lines[-1] and 'Effective sequences' not in ex_h.stdout, lines[-1])
check('Kish ESS printed equals 1/sum(w^2) computed independently', f'{1 / (wi ** 2).sum():.2f}' in lines[-1], f'{1 / (wi ** 2).sum():.2f}')

# ---------------- MI-APC ----------------------------------------------------------------------------------------------------
import mi_apc
def indep_mi_matrix(a, g, min_pairs=20):
    n, l = a.shape
    codes = np.zeros(a.shape, dtype=int);
    for j in range(l):
        u = {ch: k for k, ch in enumerate(sorted(set(a[:, j])))}
        codes[:, j] = [u[ch] for ch in a[:, j]]
    mi = np.zeros((l, l)); valid = np.zeros((l, l), bool)
    for i in range(l):
        for j in range(i + 1, l):
            m = ~g[:, i] & ~g[:, j]
            if m.sum() < min_pairs: continue
            ci, cj = codes[m, i], codes[m, j]
            _, ii = np.unique(ci, return_inverse=True); _, jj = np.unique(cj, return_inverse=True)
            joint = np.bincount(ii * (jj.max() + 1) + jj).astype(float)
            hi = entropy(np.bincount(ii), base=2); hj = entropy(np.bincount(jj), base=2); hij = entropy(joint[joint > 0], base=2)
            mi[i, j] = mi[j, i] = hi + hj - hij; valid[i, j] = valid[j, i] = True
    return mi, valid
mi_i, valid_i = indep_mi_matrix(arr, isgap)
def indep_apc(mi, valid):
    l = mi.shape[0]; off = valid & ~np.eye(l, dtype=bool)
    cm = np.array([mi[k, off[k]].mean() if off[k].any() else 0.0 for k in range(l)])
    tot = mi[off].mean()
    return mi - np.outer(cm, cm) / tot
with warnings.catch_warnings(record=True) as wrec:
    warnings.simplefilter('always')
    got = mi_apc.mi_matrix_apc(aln)
print('mi_matrix_apc default on the seed: warnings =', [str(x.message) for x in wrec])
ok_flag, npl, msg = mi_apc.apc_applicable(aln)
check('mi_matrix_apc(seed) WARNS (L=141, Neff/L=0.47) and returns RAW MI equal to independent scipy-entropy MI (max abs diff < 1e-9)',
      len(wrec) == 1 and 'Neff/L=0.47' in str(wrec[0].message) and 'RAW MI' in str(wrec[0].message) and not ok_flag and np.abs(got - mi_i).max() < 1e-9, f'{np.abs(got - mi_i).max():.1e}')
forced = mi_apc.mi_matrix_apc(aln, force=True)
check('mi_matrix_apc(force=True) returns MI - APC equal to the independent APC (Dunn 2008 definition) to 1e-9', np.abs(forced - indep_apc(mi_i, valid_i)).max() < 1e-9, f'{np.abs(forced - indep_apc(mi_i, valid_i)).max():.1e}')
check('MI matrix symmetric; raw MI non-negative (up to fp)', np.allclose(got, got.T) and got.min() > -1e-9)
p = run_ex('mi_apc.py', PFAM_STO)
print(p.stdout, p.stderr[-300:])
check('mi_apc.py on the seed exits 0, prints the WARNING (Neff/L=0.47), ranks RAW MI, prints the shuffled null and the count above it',
      p.returncode == 0 and 'WARNING: L=141, Neff/L=0.47' in p.stdout and 'raw MI' in p.stdout and 'column-shuffled null max' in p.stdout and re.search(r'\d+ of the top 20 exceed the null', p.stdout) is not None)
top_line = [l for l in p.stdout.splitlines() if re.match(r'\s+\d+-\s*\d+:', l)][0]
null_max = float(re.search(r'null max = ([0-9.]+)', p.stdout).group(1))
top_pairs_flagged = sum('(<= null)' in l for l in p.stdout.splitlines())
n_above = int(re.search(r'(\d+) of the top 20 exceed the null', p.stdout).group(1))
print('top line:', top_line, '| null max', null_max, '| flagged <= null:', top_pairs_flagged, '| above null:', n_above)
iu = np.triu_indices(L, 1); best = mi_i[iu].max()
check('top raw-MI pair printed by mi_apc.py equals the independent maximum of raw MI (2.627 bits) and is <= the null, so 0 of 20 pairs are called', abs(float(top_line.split(':')[1].split()[0]) - best) < 5e-4 and best <= null_max and n_above == 0, f'{best:.3f} vs null {null_max}')
# the null itself: a real null must be a max over pair MI of shuffled data -- recompute independently (same seed stream is impl detail; check its scale)
rng = np.random.default_rng(123); sh = arr.copy()
for k in range(L): sh[:, k] = rng.permutation(sh[:, k])
mis, _ = indep_mi_matrix(sh, sh == '.')
print('independent shuffled max raw MI (1 shuffle, my seed):', mis[iu].max())
check('the printed null is the right scale: within 25% of an independent column-shuffle max raw MI', abs(mis[iu].max() - null_max) / null_max < 0.25, f'{mis[iu].max():.3f} vs {null_max}')
# SKILL claim: "on the PF00042 seed (L = 141, Neff/L = 0.47) the best MI-APC pair (0.603 bits) scored below the best column-shuffled pair (0.616), and none of the top 30 pairs were 1MBN contacts"
mapc = forced; best_apc = mapc[iu].max()
null_apc = mi_apc.column_shuffled_null(aln, apc=True)
print(f'forced MI-APC best pair {best_apc:.3f}; column_shuffled_null(apc=True, seed 0, best of 5) = {null_apc:.3f}')
check('SKILL.md figure "best MI-APC pair 0.603 bits" reproduced', abs(best_apc - 0.603) < 0.0006, f'{best_apc:.4f}')
check('SKILL.md figure "best column-shuffled pair 0.616": the shipped null (seed 0, best of 5) gives that number?', abs(null_apc - 0.616) < 0.0006, f'{null_apc:.4f}')
check('best MI-APC pair is below the shipped null (the qualitative claim: noise at Neff/L 0.47)', best_apc < null_apc)
# contact ground truth from PDB 1MBN
struct = PDBParser(QUIET=True).get_structure('m', PDB_1MBN)[0]['A']
res = [r for r in struct if r.id[0] == ' ']
aa3 = {'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C', 'GLN': 'Q', 'GLU': 'E', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K', 'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S', 'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'}
pdb_seq = ''.join(aa3[r.get_resname()] for r in res)
al = Align.PairwiseAligner(mode='local'); al.substitution_matrix = substitution_matrices.load('BLOSUM62'); al.open_gap_score = -10; al.extend_gap_score = -0.5
best_row = max(range(N), key=lambda i: al.score(''.join(c for c in raw[list(raw)[i]] if c.isalpha()).upper(), pdb_seq))
rowseq = ''.join(c for c in raw[list(raw)[best_row]] if c.isalpha()).upper()
a1 = al.align(rowseq, pdb_seq)[0]
row2pdb = {}
for (r0, r1), (p0, p1) in zip(*a1.aligned):
    for k in range(r1 - r0): row2pdb[r0 + k] = p0 + k
rowcols = [c for c in range(L) if not isgap[best_row, c]]
col2res = {rowcols[k]: v for k, v in row2pdb.items() if k < len(rowcols)}
ident = sum(rowseq[k] == pdb_seq[v] for k, v in row2pdb.items()) / max(1, len(row2pdb))
print(f'best seed row {list(raw)[best_row]} maps {len(col2res)} columns to 1MBN, identity {ident:.2f}')
dist = {}
def contact(a, b):
    ra, rb = res[a], res[b]
    return min((x - y) for x in ra for y in rb) < 8.0
def cmap(ci, cj):
    a, b = col2res[ci], col2res[cj]
    key = (min(a, b), max(a, b))
    if key not in dist: dist[key] = contact(*key)
    return dist[key]
pairs = [(i, j) for i in col2res for j in col2res if i < j and abs(col2res[i] - col2res[j]) >= 6]
base = np.mean([cmap(i, j) for i, j in pairs])
def precision(score, k=30):
    order = sorted(((score[i, j], i, j) for i, j in pairs), reverse=True)[:k]
    return np.mean([cmap(i, j) for _, i, j in order])
p_apc, p_raw = precision(forced), precision(got)
print(f'contact precision top-30 (8 A heavy atoms, sep >= 6): MI-APC {p_apc:.2f}, raw MI {p_raw:.2f}, all-pair baseline {base:.2f}')
check('SKILL.md claim "none of the top 30 pairs were 1MBN contacts" (MI-APC on the seed) reproduced with my own contact map (8 A heavy-atom, |i-j| >= 6)', p_apc == 0.0, f'precision {p_apc:.2f} vs baseline {base:.2f}')

# ---------------- Neff/L guard on a real DEEP alignment is not available offline; the deep-alignment path is in in9 (synthetic, planted coupling)
summary()
