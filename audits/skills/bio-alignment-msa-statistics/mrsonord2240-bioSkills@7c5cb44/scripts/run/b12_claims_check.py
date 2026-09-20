"""Spot-checks of SKILL.md factual claims against the installed Biopython 1.88, each asserting on observed output.
Run from run/:  PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python b12_claims_check.py"""
import os, sys, subprocess, re, io, contextlib
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import battery as B, skill_blocks, msa_utils
from Bio.Align import substitution_matrices
import Bio
RES = {}
def check(name, ok, detail=''):
    RES[name] = (bool(ok), detail); print(f'CHECK {name}: {"PASS" if ok else "FAIL"}  {detail}')
print('Biopython', Bio.__version__)
BL = substitution_matrices.load('BLOSUM62')
res = {}
for a in ['U', 'J', 'a', '.', 'X', '*', 'B', 'Z']:
    try:
        BL[a, 'A']; res[a] = 'ok'
    except Exception as e:
        res[a] = type(e).__name__
check('SKILL.md: BLOSUM62 Array has B,Z,X,* and raises IndexError for U, J, lower case and "."', all(res[k] == 'ok' for k in 'XBZ*') and all(res[k] == 'IndexError' for k in ['U', 'J', 'a', '.']), str(res))
check('SKILL.md: substitution_matrices.load returns a Bio Array (not a dict)', type(BL).__name__ == 'Array', type(BL).__name__)
from Bio import Align
aln_new = Align.read(os.path.join(HERE, 'data', 'seed_norm.fasta'), 'fasta')
try:
    aln_new.get_alignment_length(); r = 'has it'
except AttributeError as e:
    r = f'AttributeError: {e}'
check("SKILL.md/Common Errors: Bio.Align.read() Alignment has no get_alignment_length (exact message)", "'Alignment' object has no attribute 'get_alignment_length'" in r, r)
from Bio import AlignIO
a_old = AlignIO.read(os.path.join(HERE, 'data', 'seed_norm.fasta'), 'fasta')
check('AlignIO.read returns an object with get_alignment_length() and alignment[:, i] (the documented path)', a_old.get_alignment_length() == 141 and len(a_old[:, 0]) == 73, type(a_old).__name__)
# built-in .substitutions snippet (block 8): no '-' row/column
W = os.path.join(HERE, 'work_b12'); os.makedirs(W, exist_ok=True); os.chdir(W)
import shutil; shutil.copy(os.path.join(HERE, 'data', 'seed_dot.fasta'), 'alignment.fasta')
ns, log = skill_blocks.run_all(verbose=False)
b8 = [l for l in log if l[0] == 8][0]
first = b8[3].strip().splitlines()[0].split()
check("SKILL.md .substitutions snippet output has no '-' row/column and 20+ residue letters", b8[2] == 'OK' and '-' not in first and len(first) >= 20, f'header {first}')
# ROBINSON sum and published values
check('ROBINSON_BACKGROUND sums to 1.0 and has 20 letters', abs(sum(msa_utils.ROBINSON_BACKGROUND.values()) - 1.0) < 1e-9 and len(msa_utils.ROBINSON_BACKGROUND) == 20, f'{sum(msa_utils.ROBINSON_BACKGROUND.values()):.6f}')
check('SKILL.md text "Trp 1.3%, Leu 9.0%" matches the table', abs(msa_utils.ROBINSON_BACKGROUND['W'] - 0.0133) < 1e-4 and abs(msa_utils.ROBINSON_BACKGROUND['L'] - 0.09019) < 1e-4, '')
import math
check('Quick Reference: max IC protein = -log2(rarest) ~ 6.2 bits, DNA 2 bits', abs(-math.log2(min(msa_utils.ROBINSON_BACKGROUND.values())) - 6.23) < 0.01 and abs(-math.log2(0.25) - 2) < 1e-12, f'{-math.log2(min(msa_utils.ROBINSON_BACKGROUND.values())):.3f}')
# CLI method argument: identity_matrix.py <file> pid1 vs independent mean
import numpy as np, itertools
p = subprocess.run([sys.executable, '-B', 'identity_matrix.py', os.path.join(HERE, 'data', 'seed_dot.fasta'), 'pid1'], cwd=B.EX, capture_output=True, text=True, encoding='utf-8', env=dict(os.environ, PYTHONIOENCODING='utf-8'))
m = re.search(r'Average pairwise identity: ([\d.]+)%', p.stdout)
rows = [str(r.seq) for r in msa_utils.load_alignment(os.path.join(HERE, 'data', 'seed_dot.fasta'))]
vals = [B.pid_span_ref(rows[a], rows[b])[0] for a, b in itertools.combinations(range(len(rows)), 2)]
check('identity_matrix.py <file> pid1 prints its method label and the independent mean PID1 (19.6%)', p.returncode == 0 and 'PID1' in p.stdout and m and abs(float(m.group(1)) - 100 * np.mean(vals)) < 0.05, f'{m.group(1) if m else None}% vs {100*np.mean(vals):.2f}%')
p = subprocess.run([sys.executable, '-B', 'identity_matrix.py', os.path.join(HERE, 'data', 'seed_dot.fasta'), 'pid9'], cwd=B.EX, capture_output=True, text=True, encoding='utf-8')
check('identity_matrix.py rejects an unknown method with a clear ValueError', p.returncode != 0 and 'method must be one of' in p.stderr, p.stderr.strip().splitlines()[-1][:100])
os.chdir(HERE); shutil.rmtree(W, ignore_errors=True)
import json
json.dump({k: list(v) for k, v in RES.items()}, open(os.path.join(HERE, 'results_b12.json'), 'w'), indent=1)
print('\nSUMMARY', sum(v[0] for v in RES.values()), 'of', len(RES), 'checks PASS')
