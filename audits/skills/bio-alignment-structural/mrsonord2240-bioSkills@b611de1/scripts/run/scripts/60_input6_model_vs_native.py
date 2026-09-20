"""Input 6 (Scope Boundary, regression of pre-fix input 6): evaluate an AlphaFold model against its crystal structure and pre-filter low-pLDDT residues.
User prompt: "Superpose the AFDB model of sperm-whale myoglobin (AF-P02185) on the crystal structure 1MBN; give TM-score, RMSD, GDT-TS
and lDDT and say whether the model is correct. Also mask low-pLDDT residues before Foldseek indexing (p53 AF model)."
Checks the FIXED SKILL.md text: TM-align/US-align/Foldseek numbers, the documented `TMscore model native -seq` GDT-TS command and its residue-number trap
(0.508/0.593 default vs 0.985/0.980/0.705 with -seq), my own numpy GDT-TS lower bound, and the --mask-bfactor-threshold claim.
Run inside WSL: python scripts/60_input6_model_vs_native.py   (cwd = run/)"""
import os, re, shutil, subprocess, sys
sys.dont_write_bytecode = True
sys.path.insert(0, 'skill/examples'); sys.path.insert(0, 'scripts')
import numpy as np
import tm_align_pairwise as t
import alnutil as au
D = 'data/real_pdb/'; w = 'work/in6'; shutil.rmtree(w, ignore_errors=True); os.makedirs(w)
def sh(c, **k): return subprocess.run(c, capture_output=True, text=True, **k)
AF, NAT = D + 'AF-P02185-F1.pdb', D + '1MBN.pdb'

a = t.tm_align(NAT, AF); u = t.parse_outfmt2(sh(['USalign', AF, NAT, '-mol', 'prot', '-outfmt', '2']).stdout)
print('example tm_align AF->1MBN:', a); print('USalign:', u)
assert abs(a['tm2'] - 0.9804) < 2e-3 and abs(a['tm1'] - u['tm1']) < 2e-3 and a['rmsd'] < 1.0
ind = au.tmalign_independent(AF, NAT)
print('numpy Kabsch from TM-align pairing:', {k: round(v, 4) if isinstance(v, float) else v for k, v in ind.items()})
assert abs(ind['rmsd'] - a['rmsd']) < 0.02 and abs(ind['tm_by_2'] - a['tm2']) < 0.02
print('ASSERT OK: TM %.4f/%.4f, RMSD %.2f over %d; numpy agrees; interpretation: %s' % (a['tm1'], a['tm2'], a['rmsd'], a['length_align'], t.interpret_tmscore(min(a['tm1'], a['tm2']), min(a['length1'], a['length2']))))

# ---- GDT-TS exactly as SKILL.md documents
o1 = sh(['TMscore', AF, NAT]).stdout; o2 = sh(['TMscore', AF, NAT, '-seq']).stdout
def grab(o):
    f = lambda pat: float(re.search(pat, o).group(1))
    return dict(tm=f(r'TM-score\s*=\s*([\d.]+)'), gdt=f(r'GDT-TS-score=\s*([\d.]+)'), rmsd=f(r'RMSD of\s+the common residues=\s*([\d.]+)'), n=int(f(r'Number of residues in common=\s*(\d+)')))
g1, g2 = grab(o1), grab(o2)
print('TMscore default:', g1); print('TMscore -seq   :', g2)
assert abs(g1['gdt'] - 0.5082) < 0.01 and abs(g1['tm'] - 0.593) < 0.01, 'SKILL: default GDT-TS 0.508 / TM 0.593'
assert abs(g2['gdt'] - 0.9853) < 0.01 and abs(g2['tm'] - 0.9804) < 0.005 and abs(g2['rmsd'] - 0.705) < 0.02 and g2['n'] == 153
# second method: GDT-TS from the TM-align superposition (a lower bound of the LGA-optimised score)
r1, r2 = au.read_ca(AF), au.read_ca(NAT)
s1, _, s2 = au.parse_tmalign_alignment(sh(['TMalign', AF, NAT]).stdout); pr = au.pairs_from_alignment(s1, s2)
P = np.array([r1[i][4] for i, _ in pr]); Q = np.array([r2[j][4] for _, j in pr])
_, R, tr = au.kabsch(P, Q); d = np.linalg.norm(P @ R.T + tr - Q, axis=1)
gdt = np.mean([(d < c).sum() / len(r2) for c in (1, 2, 4, 8)])
print('independent GDT-TS (TM-align/Kabsch superposition, native length %d): %.4f  (TMscore -seq: %.4f; numeric lower bound expected)' % (len(r2), gdt, g2['gdt']))
assert gdt <= g2['gdt'] + 0.01 and g2['gdt'] - gdt < 0.06
print('ASSERT OK: GDT-TS 0.985 documented value reproduced by TMscore -seq and independently bounded; default (numbering-paired) run shows the documented trap (0.508)')

# ---- Foldseek lddt column (SKILL: >0.6 correctly modelled)
shutil.copy(NAT, w + '/1MBN.pdb'); sh(['foldseek', 'createdb', w + '/1MBN.pdb', w + '/n', '-v', '1'])
sh(['foldseek', 'easy-search', AF, w + '/n', w + '/r.m8', w + '/tmp', '--format-output', 'query,target,alntmscore,lddt,alnlen,pident', '-v', '1'])
row = open(w + '/r.m8').read().split('\t'); print('Foldseek model->native:', row)
assert float(row[3]) > 0.6 and float(row[2]) > 0.95

# ---- pLDDT masking
P53 = D + 'AF-P04637-F1.pdb'
low = {}
for l in open(P53):
    if l.startswith('ATOM') and l[12:16].strip() == 'CA': low[int(l[22:26])] = float(l[60:66])
n_low = sum(v < 70 for v in low.values()); print('p53 AF model: %d residues, %d with pLDDT (B-factor) < 70' % (len(low), n_low))
sh(['foldseek', 'createdb', P53, w + '/p_plain', '-v', '1']); m = sh(['foldseek', 'createdb', '--mask-bfactor-threshold', '70.0', P53, w + '/p_mask', '-v', '1'])
dump = lambda db: open(db + '_ss', 'rb').read().replace(bytes([0]), b'').replace(bytes([10]), b'').decode()
s1, s2 = dump(w + '/p_plain'), dump(w + '/p_mask')
diff = sum(x != y for x, y in zip(s1, s2)); print('masked DB: rc %d, 3Di length plain/masked %d/%d, positions that differ %d, X count masked %d' % (m.returncode, len(s1), len(s2), diff, s2.count('X')))
idx_low = [i for i, k in enumerate(sorted(low)) if low[k] < 70]
print('   changed positions are exactly the low-pLDDT residues:', [i for i, (x, y) in enumerate(zip(s1, s2)) if x != y] == idx_low, '| letters written at masked positions:', sorted({s2[i] for i in idx_low}))
assert [i for i, (x, y) in enumerate(zip(s1, s2)) if x != y] == idx_low
assert m.returncode == 0 and len(s1) == len(s2) == len(low) and diff == n_low
print('ASSERT OK: --mask-bfactor-threshold 70 changed exactly the %d low-pLDDT positions (independent count from B-factors: %d)' % (diff, n_low))
# with the mask on the 3Di of low pLDDT residues is not random letters any more: self search still finds the model
sh(['foldseek', 'easy-search', P53, w + '/p_mask', w + '/pm.m8', w + '/tm2', '--format-output', 'query,target,evalue,alntmscore,alnlen', '-v', '1']); print('self-search on masked DB:', open(w + '/pm.m8').read().strip())
