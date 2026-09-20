"""INPUT 5 (stress, SYNTHETIC data from the first audit: numpy seed 20260920/21, 8 clades, 20% N-terminal + 20% C-terminal
gap runs, 15% internal gap blocks): 300 x 300 and 2000 x 300 protein alignments.
Prompt: "I have a 300-sequence protein alignment. Compute the full identity matrix, average conservation profile,
sum-of-pairs score against BLOSUM62 and the Kimura distance matrix."   (+ 2000 x 300 identity matrix)
Run from run/:  PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python b08_input5_stress.py"""
import os, sys, json, time, shutil, io, contextlib, itertools
from collections import Counter
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import battery as B, skill_blocks, numpy as np
import msa_utils, identity_matrix as IM
from Bio.Align import substitution_matrices
RES = {}
def check(name, ok, detail=''):
    RES[name] = (bool(ok), detail); print(f'CHECK {name}: {"PASS" if ok else "FAIL"}  {detail}')
D = os.path.join(HERE, 'data')
f300 = os.path.join(D, 'synthetic_stress_300x300.fasta'); f2000 = os.path.join(D, 'synthetic_stress_2000x300.fasta')
t0 = time.time()
o = B.run_battery(f300, 'fasta', 'protein', 'stress300', max_pairs=4000, check=check, out_cli=False)
print(f'battery 300x300 {time.time()-t0:.1f}s', o)
# SKILL.md blocks verbatim (sum_of_pairs on 13M residue pairs) vs a count-based BLOSUM62 SP (no pair loop)
W = os.path.join(HERE, 'work_b08'); shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
shutil.copy(f300, os.path.join(W, 'alignment.fasta')); cwd = os.getcwd(); os.chdir(W)
t0 = time.time(); ns, log = skill_blocks.run_all(verbose=False); tb = time.time() - t0
errs = [(i, st) for i, f, st, out in log if st.startswith('ERROR')]
check('300x300: all non-stub SKILL.md blocks run verbatim', not errs, f'{errs}; total {tb:.0f}s')
aln = ns['alignment']; BL = substitution_matrices.load('BLOSUM62')
rows = [str(r.seq) for r in aln]
tot = 0.0
for col in zip(*rows):
    cnt = Counter(c for c in col if c != '-'); ks = sorted(cnt)
    for i, a in enumerate(ks):
        tot += cnt[a] * (cnt[a] - 1) / 2 * BL[a, a]
        for b in ks[i + 1:]:
            tot += cnt[a] * cnt[b] * BL[a, b]
sp = ns['sum_of_pairs'](aln)
check('300x300: sum_of_pairs == count-based BLOSUM62 SP (independent, no pair loop)', abs(sp - tot) < 1e-6, f'{sp} vs {tot}')
check('300x300: alignment_score == count-based simple SP (gap/gap = 0)', ns['alignment_score'](aln) == o['simple_sp_ref'], f"{o['simple_sp_ref']}")
os.chdir(cwd); shutil.rmtree(W, ignore_errors=True)
# the shipped CLI (argv path) at 300x300: time
import subprocess
for f in ['identity_matrix.py', 'conservation_profile.py', 'entropy_analysis.py', 'kimura_protein_distance.py']:
    t0 = time.time()
    p = subprocess.run([sys.executable, '-B', f, f300], cwd=B.EX, capture_output=True, text=True, encoding='utf-8', timeout=900, env=dict(os.environ, PYTHONIOENCODING='utf-8'))
    check(f'300x300 CLI {f} rc 0, prints a mean', p.returncode == 0 and any(k in p.stdout for k in ('Average', 'Mean')), f'{time.time()-t0:.1f}s stderr {p.stderr.strip()[:80]!r}')
# 2000 x 300 identity matrix
aln2 = msa_utils.load_alignment(f2000)
rows2 = [str(r.seq) for r in aln2]
for m in ('pid1', 'pid4'):
    t0 = time.time(); M = IM.identity_matrix_vectorized(aln2, m); dt = time.time() - t0
    rng = np.random.default_rng(1); worst = 0.0
    for _ in range(3000):
        a, b = rng.choice(len(rows2), 2, replace=False)
        worst = max(worst, abs(M[a, b] - B.pid_span_ref(rows2[a], rows2[b])[['pid1', 'pid2', 'pid3', 'pid4'].index(m)]))
    check(f'2000x300 identity matrix {m}: completes, 3000 sampled pairs == numpy reference, symmetric', worst < 1e-12 and np.allclose(M, M.T, equal_nan=True) and np.isfinite(M).all(), f'{dt:.0f}s; max diff {worst:.1e}')
json.dump({k: list(v) for k, v in RES.items()}, open(os.path.join(HERE, 'results_b08.json'), 'w'), indent=1)
print('\nSUMMARY', sum(v[0] for v in RES.values()), 'of', len(RES), 'checks PASS')
