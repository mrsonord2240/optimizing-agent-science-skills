"""Input 1 (Canonical, regression of pre-fix input 1): TM-score / RMSD between myoglobin 1MBN and hemoglobin
alpha 1A3N (chain A), real structures, ~25% identity, same globin fold.
User prompt: "Align these two crystal structures with TM-align and report TM-score, RMSD and the superposition.
Then tell me whether they share a fold."
Runs the FIXED examples/tm_align_pairwise.py from the copied skill, then checks by a second method (US-align, my own numpy
Kabsch/TM from TM-align's own alignment, DaliLite as documented in SKILL.md, PyMOL) and checks the -o wording fix.
Run inside WSL: python scripts/10_input1_pairwise.py   (cwd = run/)"""
import os, shutil, subprocess, sys
sys.dont_write_bytecode = True
sys.path.insert(0, 'skill/examples'); sys.path.insert(0, 'scripts')
import tm_align_pairwise as t
import alnutil as au

D = 'data/real_pdb/'
w = 'work/in1'; shutil.rmtree(w, ignore_errors=True); os.makedirs(w)
def sh(c, **k): return subprocess.run(c, capture_output=True, text=True, **k)

shutil.copy(D + '1MBN.pdb', w + '/reference.pdb'); shutil.copy(D + '1A3N.pdb', w + '/mobile.pdb')
cwd = os.getcwd(); os.chdir(w)

# ---- (1) the example exactly as shipped: output_prefix (not file name)
r = t.tm_align('reference.pdb', 'mobile.pdb', output_prefix='superposed')
print('EXAMPLE tm_align ->', r)
assert r['superposed_pdb'] == 'superposed.pdb'
assert os.path.exists('superposed.pdb') and os.path.getsize('superposed.pdb') > 10000, 'superposed.pdb missing/empty'
n_atom = sum(1 for l in open('superposed.pdb') if l.startswith('ATOM'))
print('superposed.pdb ATOM records:', n_atom, '| files:', sorted(f for f in os.listdir('.') if f.startswith('superposed')))
assert n_atom > 1000  # full-atom mobile structure
# (mobile = 1A3N whole file: TMalign reads only chain A -> L1 = 141; reference 1MBN L2 = 153)
assert r['length1'] == 141 and r['length2'] == 153
assert abs(r['tm1'] - 0.9000) < 2e-3 and abs(r['tm2'] - 0.8356) < 2e-3, r
assert 1.4 < r['rmsd'] < 1.7 and r['length_align'] == 141
print('ASSERT OK (values vs TM-align/US-align printed by the tooling agent 0.9000/0.8356/1.56/141)')

# ---- (2) independent numpy: rebuild pairing from TM-align's alignment strings, Kabsch RMSD + TM-scores
ind = au.tmalign_independent('mobile.pdb', 'reference.pdb', 'A', None)
print('INDEPENDENT numpy from TM-align pairing:', {k: round(v, 4) if isinstance(v, float) else v for k, v in ind.items()})
assert ind['lali'] == r['length_align'] and abs(ind['rmsd'] - r['rmsd']) < 0.02, (ind, r)
assert ind['tm_by_1'] <= r['tm1'] + 1e-3 and r['tm1'] - ind['tm_by_1'] < 0.03     # Kabsch-on-all-pairs is a lower bound of TM-align's optimum
assert abs(ind['tm_by_2'] - r['tm2']) < 0.03
print('ASSERT OK: numpy RMSD %.3f vs %.2f, TM (lower bound) %.4f/%.4f vs %.4f/%.4f' % (ind['rmsd'], r['rmsd'], ind['tm_by_1'], ind['tm_by_2'], r['tm1'], r['tm2']))

# ---- (3) US-align second tool
u = t.parse_outfmt2(sh(['USalign', 'mobile.pdb', 'reference.pdb', '-mol', 'prot', '-outfmt', '2']).stdout)
print('USalign:', u)
assert u and abs(u['tm1'] - r['tm1']) < 1e-3 and abs(u['tm2'] - r['tm2']) < 1e-3 and abs(u['rmsd'] - r['rmsd']) < 0.01
print('ASSERT OK: US-align == TM-align')

# ---- (4) SKILL.md claims about flags
o = sh(['TMalign', 'mobile.pdb', 'reference.pdb', '-o', 'sup'])
assert os.path.exists('sup.pdb') and any(f.startswith('sup') and f.endswith('.pml') for f in os.listdir('.'))
print('TMalign -o sup ->', sorted(f for f in os.listdir('.') if f.startswith('sup')))
o = sh(['TMalign', 'mobile.pdb', 'reference.pdb', '-o', 'sup2.pdb'])
assert os.path.exists('sup2.pdb.pdb') and not os.path.exists('sup2.pdb'), 'doc claim: -o sup.pdb writes sup.pdb.pdb'
print('ASSERT OK: -o takes a prefix and appends .pdb (sup2.pdb -> sup2.pdb.pdb)')
p = sh(['TMalign', 'mobile.pdb', 'reference.pdb', '-outfmt', '2', '-a', 'T'])
rows = [l for l in p.stdout.splitlines() if l and not l.startswith('#')]
print('-outfmt 2 -a T rc=%d rows=%d msg=%r' % (p.returncode, len(rows), (p.stdout + p.stderr)[:200]))
p = sh(['TMalign', 'mobile.pdb', 'reference.pdb', '-a', 'T'])
tm_avg = [l for l in p.stdout.splitlines() if 'TM-score=' in l]
print('-a T (full output):', tm_avg)
assert len(tm_avg) == 3 and 'average' in tm_avg[2].lower()
print('ASSERT OK: -a T adds a third TM-score normalised by the average length; -outfmt 2 -a T gives no data row')
p = sh(['TMalign', 'mobile.pdb', 'reference.pdb', '-outfmt', '2', '-L', '100'])
rows = [l for l in p.stdout.splitlines() if l and not l.startswith('#')]
print('-outfmt 2 -L 100 rows=%d msg=%r' % (len(rows), (p.stdout + p.stderr)[:160]))
# the Common Errors row says "-L N was passed -> TM-score normalised by a fixed length"
p = sh(['TMalign', 'mobile.pdb', 'reference.pdb', '-L', '100'])
print('-L 100 (full output) TM lines:', [l for l in p.stdout.splitlines() if 'TM-score=' in l])

# ---- (5) fold call as the example prints it
print('interpret min(TM1,TM2)=%.3f, shorter L=%d ->' % (min(r['tm1'], r['tm2']), min(r['length1'], r['length2'])),
      t.interpret_tmscore(min(r['tm1'], r['tm2']), min(r['length1'], r['length2'])))
assert t.interpret_tmscore(0.8356, 141) == 'very similar topology' and t.interpret_tmscore(0.9, 40).startswith('chain < 60')
# example __main__ block from a clean directory (files named as the example expects)
m = sh([sys.executable, '-B', '-c', 'import sys; sys.path.insert(0, "../../skill/examples"); import runpy; runpy.run_path("../../skill/examples/tm_align_pairwise.py", run_name="__main__")'])
print('EXAMPLE __main__ rc=%d\n%s%s' % (m.returncode, m.stdout, m.stderr[-400:]))
assert m.returncode == 0 and 'Superposed mobile structure: superposed.pdb' in m.stdout and 'RMSD: 1.56 A over 141' in m.stdout

# ---- (6) DaliLite block copied from SKILL.md (in its own directory)
os.chdir(cwd); dd = w + '/dali'; os.makedirs(dd + '/DAT', exist_ok=True)
shutil.copy(D + '1MBN.pdb', dd + '/1mbn.pdb'); shutil.copy(D + '1A3N.pdb', dd + '/1a3n.pdb')
os.chdir(dd)
for c in (['import.pl', '--pdbfile', '1mbn.pdb', '--pdbid', '1mbn', '--dat', 'DAT/'], ['import.pl', '--pdbfile', '1a3n.pdb', '--pdbid', '1a3n', '--dat', 'DAT/'],
          ['dali.pl', '--cd1', '1mbnA', '--cd2', '1a3nA', '--dat1', 'DAT/', '--dat2', 'DAT/', '--title', 'mb_hb', '--outfmt', 'summary']):
    p = sh(c); print(' '.join(c), 'rc', p.returncode)
res = open('1mbnA.txt').read() if os.path.exists('1mbnA.txt') else ''
print('1mbnA.txt:\n', res[:600])
line = [l for l in res.splitlines() if '1a3n-A' in l]
assert line and '20.3' in line[0] and ' 141 ' in line[0], 'DALI Z 20.3 / lali 141 documented line not reproduced'
print('ASSERT OK: DaliLite Z=20.3, rmsd 1.6, lali 141 as documented; note DALI hit list also holds the 1mbn self-hit:', [l for l in res.splitlines() if l.strip().startswith('1:')])
os.chdir(cwd)

# ---- (7) PyMOL headless line from SKILL.md 'Visualisation and Inspection'
pw = w + '/pymol'; os.makedirs(pw)
shutil.copy(D + '1MBN.pdb', pw + '/reference.pdb'); shutil.copy(D + '1A3N.pdb', pw + '/mobile.pdb')
p = sh(['pymol', '-cq', '-d', 'load reference.pdb; load mobile.pdb; super mobile, reference; ray 800,600; png fig.png'], cwd=pw)
print('pymol rc', p.returncode, (p.stdout + p.stderr)[-500:])
print('fig.png exists:', os.path.exists(pw + '/fig.png'), os.path.getsize(pw + '/fig.png') if os.path.exists(pw + '/fig.png') else 0)
p2 = sh(['pymol', '-cq', '-d', 'load reference.pdb; load mobile.pdb; print(cmd.super("mobile and chain A","reference")); print(cmd.cealign("reference","mobile and chain A"))'], cwd=pw)
print('pymol super/cealign:', [l for l in p2.stdout.splitlines() if l.strip()][-4:])
