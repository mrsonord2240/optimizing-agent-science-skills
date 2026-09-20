"""INPUT 5 (Stress, SYNTHETIC alignment - seed 20260920): 300 x 300 protein MSA with clades, terminal gaps and internal gap blocks;
plus a 2000 x 300 alignment for the 'vectorized' identity matrix claim. Correctness vs count-based / numpy references, and timing.
Prompt: "I have a 300-sequence protein alignment. Compute the full identity matrix, average conservation profile, sum-of-pairs
score against BLOSUM62 and the Kimura distance matrix." Run from run/."""
import os, sys, time, itertools, json, shutil
import numpy as np
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'skill', 'examples'))
import ref
from Bio import AlignIO
from Bio.Align import substitution_matrices
import identity_matrix as IM, kimura_protein_distance as KP
import skill_blocks
RES = {}
def check(name, ok, detail=''):
    RES[name] = (bool(ok), detail); print(f'CHECK {name}: {"PASS" if ok else "FAIL"}  {detail}')

def synth(n, L, seed):
    rng = np.random.default_rng(seed)
    aa = np.array(list(ref.AA20)); p = np.array([ref.ROB_TRUE[a] for a in ref.AA20]); p /= p.sum()
    root = rng.choice(aa, L, p=p)
    def mut(s, rate):
        s = s.copy(); m = rng.random(L) < rate; s[m] = rng.choice(aa, m.sum(), p=p); return s
    clades = [mut(root, .35) for _ in range(8)]
    rows = []
    for i in range(n):
        s = mut(clades[i % 8], .12)
        if rng.random() < .2: s[:rng.integers(3, 25)] = '-'              # N-terminal gap
        if rng.random() < .2: s[L - rng.integers(3, 25):] = '-'          # C-terminal gap
        if rng.random() < .15:
            a = rng.integers(20, L - 40); s[a:a + rng.integers(2, 12)] = '-'   # internal gap block
        rows.append(''.join(s))
    return rows

D = os.path.join(HERE, 'data')
rows = synth(300, 300, 20260920)
with open(os.path.join(D, 'synthetic_stress_300x300.fasta'), 'w') as o:
    for i, r in enumerate(rows): o.write(f'>syn{i}\n{r}\n')
big = synth(2000, 300, 20260921)
with open(os.path.join(D, 'synthetic_stress_2000x300.fasta'), 'w') as o:
    for i, r in enumerate(big): o.write(f'>syn{i}\n{r}\n')
wd = os.path.join(HERE, 'work_in5'); shutil.rmtree(wd, ignore_errors=True); os.makedirs(wd); os.chdir(wd)
shutil.copy(os.path.join(D, 'synthetic_stress_300x300.fasta'), 'alignment.fasta')
aln = AlignIO.read('alignment.fasta', 'fasta'); N, L = len(aln), aln.get_alignment_length()
ns, log = skill_blocks.run_all(verbose=False)
A = np.array([list(r) for r in rows])

# identity matrix
t = time.time(); M = IM.identity_matrix_vectorized(aln); t_id = time.time() - t
eq = (A[:, None, :] == A[None, :, :]); ng = (A != '-')
mt = (eq & ng[:, None, :] & ng[None, :, :]).sum(2); den = (ng[:, None, :] | ng[None, :, :]).sum(2)
Mref = mt / den
np.fill_diagonal(Mref, 1.0)
check('S1 identity_matrix_vectorized == numpy 3-D broadcast reference (300x300)', np.abs(M - Mref).max() < 1e-12, f'{t_id:.2f}s')
# Doolittle-vs-Skill PID1 impact where 20% of sequences have terminal gaps
sub = list(range(0, 300, 6)); dd = []
for a, b in itertools.combinations(sub, 2):
    dd.append(M[a, b] - ref.pid_ref(rows[a], rows[b])['PID1'])
dd = np.array(dd)
print(f'   Skill PID1 (example/identity matrix) minus Doolittle PID1 over {len(dd)} pairs: mean {100*dd.mean():+.2f} pts, min {100*dd.min():+.2f} pts')
check('S2 Skill PID1 == Doolittle internal-gap PID1 when terminal gaps present', np.abs(dd).max() < 1e-9, f'max under-estimate {100*-dd.min():.1f} pts')
# naive double loop timing (SKILL: fine for hundreds)
t = time.time(); s = 0
for a, b in itertools.combinations(range(100), 2): s += ns['pairwise_identity'](rows[a], rows[b], 'pid4')
t_naive100 = time.time() - t
print(f'   naive pairwise_identity pid4: {t_naive100:.2f}s for 4,950 pairs (N=100) -> extrapolated N=300: {t_naive100*44850/4950:.0f}s, N=2000: {t_naive100*1999000/4950/60:.0f} min')
# conservation profile
t = time.time(); prof = ns['conservation_profile'](aln, window=10); t_prof = time.time() - t
cons = np.array([ref.conservation_ref(''.join(A[:, k])) for k in range(L)])
kk = 150; check('S3 conservation_profile value == mean(cols[i-5..i+4])', abs(prof[kk] - cons[kk-5:kk+5].mean()) < 1e-9, f'{t_prof:.1f}s')
# SP score vs count-based
BL = substitution_matrices.load('BLOSUM62'); idx = {a: i for i, a in enumerate(ref.AA20)}
Bm = np.array([[BL[a, b] for b in ref.AA20] for a in ref.AA20], float)
def sp_counts(A):
    tot = 0.0
    for k in range(A.shape[1]):
        c = np.zeros(20)
        for ch in A[:, k]:
            if ch != '-': c[idx[ch]] += 1
        tot += 0.5 * (c @ Bm @ c - (c * np.diag(Bm)).sum())
    return tot
t = time.time(); sp = ns['sum_of_pairs'](aln); t_sp = time.time() - t
spr = sp_counts(A)
check('S4 sum_of_pairs (BLOSUM62) == count-based reference', abs(sp - spr) < 1e-6, f'Skill {sp} vs ref {spr}; Skill time {t_sp:.0f}s for {N*(N-1)//2*L/1e6:.0f}M residue pairs')
t = time.time(); asc = ns['alignment_score'](aln); t_asc = time.time() - t
print(f'   alignment_score {asc} in {t_asc:.0f}s')
# Kimura all pairs
t = time.time(); K = np.zeros((N, N))
for a, b in itertools.combinations(range(N), 2): K[a, b] = K[b, a] = KP.kimura_protein_distance(rows[a], rows[b])
t_k = time.time() - t
sat = int(np.isinf(K[np.triu_indices(N, 1)]).sum()); print(f'   Kimura all-pairs {t_k:.0f}s; saturated (inf) pairs: {sat}/{N*(N-1)//2}')
kref = np.array([ref.kimura_ref(rows[a], rows[b]) for a, b in itertools.combinations(range(0, 300, 10), 2)]); ksk = np.array([K[a, b] for a, b in itertools.combinations(range(0, 300, 10), 2)])
ok = np.isfinite(ksk) & np.isfinite(kref); check('S5 Kimura == reference on finite pairs (sampled)', np.abs(ksk[ok] - kref[ok]).max() < 1e-9, f'{ok.sum()} pairs')
# 2000 x 300 identity matrix speed
shutil.copy(os.path.join(D, 'synthetic_stress_2000x300.fasta'), 'big.fasta')
b_aln = AlignIO.read('big.fasta', 'fasta')
t = time.time(); Mb = IM.identity_matrix_vectorized(b_aln); t_big = time.time() - t
Ab = np.array([list(r) for r in big]); i, j = 17, 1503
mm = ((Ab[i] == Ab[j]) & (Ab[i] != '-')).sum(); dn = ((Ab[i] != '-') | (Ab[j] != '-')).sum()
check('S6 2000x300 identity matrix finishes and spot-checks', abs(Mb[i, j] - mm / dn) < 1e-12 and Mb.shape == (2000, 2000), f'{t_big:.1f}s')
print(f'   avg identity example formula: (M.sum()-n)/(n(n-1)) = {(Mb.sum()-2000)/(2000*1999)*100:.2f}%')
RES['_timing'] = (True, f'id300 {t_id:.2f}s prof {t_prof:.1f}s sp {t_sp:.0f}s asc {t_asc:.0f}s kim {t_k:.0f}s id2000 {t_big:.1f}s')
json.dump(RES, open(os.path.join(HERE, 'results_in5.json'), 'w'), indent=1)
print('SUMMARY', sum(v[0] for v in RES.values()), 'of', len(RES))
