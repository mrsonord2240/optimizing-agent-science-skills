"""Input 5 (continued): run the three shipped __main__ blocks (henikoff_weights.py, neff.py, mi_apc.py) from a COPY on the REAL Pfam seed FASTA,
and assert their printed numbers against values computed independently in in5_weights_neff_mi.py (Neff 66.08 / 73.00, 73 weight lines summing to 1)."""
import os, re, sys, shutil, subprocess
from common import *
ex = os.path.join(HERE, 'ex5b'); shutil.rmtree(ex, ignore_errors=True); shutil.copytree(SKILL_EX, ex)
shutil.copy(PFAM_FA, os.path.join(ex, 'alignment.fasta'))
env = {**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONDONTWRITEBYTECODE': '1'}
out = {}
for s in ('henikoff_weights.py', 'neff.py', 'mi_apc.py'):
    p = subprocess.run([sys.executable, s], cwd=ex, capture_output=True, text=True, encoding='utf-8', env=env)
    out[s] = p
    print(f'--- {s}: rc={p.returncode}, stdout lines={len(p.stdout.splitlines())}, stderr={p.stderr.strip()[:200]!r}')
    print('\n'.join(p.stdout.splitlines()[:4]), '\n...' if len(p.stdout.splitlines()) > 4 else '', '\n'.join(p.stdout.splitlines()[-3:]))
h = out['henikoff_weights.py'].stdout
ws = [float(x) for x in re.findall(r'^\S+: (\d\.\d{4})$', h, re.M)]
check('henikoff_weights.py prints 73 weights and they sum to ~1', len(ws) == 73 and abs(sum(ws) - 1) < 0.005, f'{len(ws)} weights, sum {sum(ws):.4f}')
tot = re.search(r'Total weight: ([\d.]+)  Effective sequences: ([\d.]+)', h)
check('henikoff_weights.py "Effective sequences" line is printed (1/sum(w^2))', bool(tot), tot.group(0) if tot else 'missing')
n = out['neff.py'].stdout
check('neff.py prints Neff(62%)=66.08 and Neff(80%)=73.00, Neff/L=0.469 (matches independent values)', 'Neff (62% threshold, protein convention): 66.08' in n and 'Neff (80% threshold, nucleotide convention): 73.00' in n and 'Neff/L: 0.469' in n, n.replace('\n', ' | ')[:300])
m = out['mi_apc.py'].stdout
check('mi_apc.py prints 20 top pairs in the "i-j: score" format', len(re.findall(r'^\s+\d+-\s*\d+:\s+-?\d', m, re.M)) == 20, f'{len(re.findall(r"^ +[0-9]+- +[0-9]+: ", m, re.M))} pair lines')
check('mi_apc.py output carries no reliability caveat although Neff/L=0.47 < 1 (Skill: skip APC below Neff/L>1) [FAIL = no caveat]', 'warn' in m.lower() or 'caveat' in m.lower() or 'unreliable' in m.lower())
check('all three examples exit 0 with empty stderr', all(p.returncode == 0 and not p.stderr.strip() for p in out.values()))
summary()
