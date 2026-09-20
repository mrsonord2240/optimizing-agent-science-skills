"""Input 3 (Edge, regression of pre-fix input 3): Bio.PDB Superimposer on
  (a) myoglobin 1MBN vs 1A6M (153 vs 151 CA, co-numbered, sperm-whale wild type vs recombinant),
  (b) apo/holo calmodulin 1CFD (NMR apo, 148 CA) vs 1CLL (Ca2+-bound crystal, 144 residues + 4 Ca2+ ions named CA),
  (c) refusal cases: 1MBN vs 1A3N-A (different protein family member, not co-numbered), 1MBN vs 1ATP.
User prompt: "Compare apo and holo calmodulin, give me the RMSD of the conformational change, using Biopython."
Checks: the FIXED examples/biopython_superimposer.py (superpose_ca) AND the inline block from SKILL.md (executed verbatim,
extracted from the file), each against my own numpy Kabsch on the same pairing (alnutil.read_ca, ATOM records only) and
against TM-align's RMSD. Run inside WSL: python scripts/30_input3_superimposer.py   (cwd = run/)"""
import os, re, shutil, subprocess, sys
sys.dont_write_bytecode = True
sys.path.insert(0, 'skill/examples'); sys.path.insert(0, 'scripts')
import numpy as np
from Bio.PDB import PDBParser
import biopython_superimposer as bs
import alnutil as au

D = 'data/real_pdb/'
w = 'work/in3'; shutil.rmtree(w, ignore_errors=True); os.makedirs(w)
P = PDBParser(QUIET=True)
def sh(c, **k): return subprocess.run(c, capture_output=True, text=True, **k)

def independent(a, b):
    ra = {(c, n, i): (rn, x) for c, n, i, rn, x in au.read_ca(a)}
    rb = {(c, n, i): (rn, x) for c, n, i, rn, x in au.read_ca(b)}
    keys = sorted(set(ra) & set(rb))
    rmsd, _, _ = au.kabsch(np.array([rb[k][1] for k in keys]), np.array([ra[k][1] for k in keys]))
    return rmsd, len(keys), len(ra), len(rb)

# ---- (a) myoglobin
ref, mob = P.get_structure('r', D + '1MBN.pdb'), P.get_structure('m', D + '1A6M.pdb')
sup, n, mm = bs.superpose_ca(ref, mob)
ind = independent(D + '1MBN.pdb', D + '1A6M.pdb')
tm = sh(['TMalign', D + '1A6M.pdb', D + '1MBN.pdb', '-outfmt', '2']).stdout
tmr = [l.split() for l in tm.splitlines() if l and not l.startswith('#')][0]
print('(a) 1MBN/1A6M example: RMSD %.3f over %d pairs (%d name mismatches) | independent Kabsch %.3f over %d (CA ATOM counts %d/%d) | TM-align RMSD %s Lali %s' % (sup.rms, n, mm, ind[0], ind[1], ind[2], ind[3], tmr[4], tmr[10]))
assert abs(sup.rms - ind[0]) < 5e-3 and n == ind[1] == 151 and abs(float(tmr[4]) - sup.rms) < 0.02

# ---- (b) calmodulin: the 10.83 A claim
ref, mob = P.get_structure('r', D + '1CFD.pdb'), P.get_structure('m', D + '1CLL.pdb')
naive_a = [x for x in ref.get_atoms() if x.get_id() == 'CA' and x.get_parent().id[0] == ' ']
name_ca = {'1CFD': 0, '1CLL': 0}
for k in name_ca:
    s = P.get_structure(k, D + k + '.pdb'); name_ca[k] = sum(1 for x in s[0].get_atoms() if x.get_id() == 'CA')
print('atoms named CA (model 0): ', name_ca, '-> equal counts, so a name-only filter raises no size error (the trap)')
assert name_ca['1CFD'] == name_ca['1CLL'] == 148
sup, n, mm = bs.superpose_ca(ref, mob)
ind = independent(D + '1CFD.pdb', D + '1CLL.pdb')
print('(b) 1CFD/1CLL example: RMSD %.3f over %d pairs, mismatches %d | independent Kabsch %.3f over %d (CA atoms %d/%d)' % (sup.rms, n, mm, ind[0], ind[1], ind[2], ind[3]))
assert n == 144 and abs(sup.rms - 10.829) < 0.01 and abs(ind[0] - 10.829) < 0.01 and ind[1] == 144
# a 2nd independent method: TM-align RMSD is over TM-align's own pairing (not the same pairing), so only a sanity bound
tm = sh(['TMalign', D + '1CLL.pdb', D + '1CFD.pdb', '-outfmt', '2']).stdout
tmr = [l.split() for l in tm.splitlines() if l and not l.startswith('#')][0]
print('    TM-align on the same pair (own pairing): TM1 %s TM2 %s RMSD %s Lali %s  (RMSD lower because it aligns a subset)' % (tmr[2], tmr[3], tmr[4], tmr[10]))
# also the unrefused case: naive pairing by position over all atoms named CA (what the pre-fix example did)
from Bio.PDB import Superimposer
fa = [x for x in ref[0].get_atoms() if x.get_id() == 'CA']; ma = [x for x in mob[0].get_atoms() if x.get_id() == 'CA']
s2 = Superimposer(); s2.set_atoms(fa, ma); print('    naive name-only pairing by position (pre-fix behaviour):', round(s2.rms, 3), 'A over', len(fa))
assert abs(s2.rms - 13.378) < 0.05

# ---- (c) refusals
for a, b, why in (('1MBN', '1A3N', 'co-chain, different numbering'), ('1MBN', '1ATP', 'no shared chain id'), ('1MBN', '2LHB', 'other globin')):
    try:
        r = bs.superpose_ca(P.get_structure('r', D + a + '.pdb'), P.get_structure('m', D + b + '.pdb'))
        print(f'(c) {a} vs {b} ({why}): NO refusal, RMSD {r[0].rms:.2f} over {r[1]} pairs, mismatches {r[2]}')
    except ValueError as e:
        print(f'(c) {a} vs {b} ({why}): ValueError -> {str(e)[:110]}')

# ---- (d) the inline SKILL.md block, extracted and executed verbatim
skill = open('skill/SKILL.md', encoding='utf-8').read()
blocks = re.findall(r'```python\n(.*?)```', skill, re.S)
blk = [b for b in blocks if 'Superimposer' in b][0]
os.makedirs(w + '/inline', exist_ok=True)
shutil.copy(D + '1CLL.pdb', w + '/inline/mobile.pdb'); shutil.copy(D + '1CFD.pdb', w + '/inline/reference.pdb')
open(w + '/inline/blk.py', 'w', encoding='utf-8').write(blk)
p = sh([sys.executable, '-B', 'blk.py'], cwd=w + '/inline')
print('(d) SKILL.md inline block on 1CFD/1CLL ->', p.stdout.strip(), p.stderr[-300:])
assert 'RMSD: 10.829 A over 144 CA pairs' in p.stdout
shutil.copy(D + '1A3N.pdb', w + '/inline/mobile.pdb'); shutil.copy(D + '1MBN.pdb', w + '/inline/reference.pdb')
p = sh([sys.executable, '-B', 'blk.py'], cwd=w + '/inline')
print('    inline block on 1MBN vs 1A3N (not homologous numbering) ->', (p.stdout.strip() or '<empty>'), '|', p.stderr.strip().splitlines()[-1][:160] if p.stderr.strip() else '')
shutil.copy(D + '1A6M.pdb', w + '/inline/mobile.pdb')
p = sh([sys.executable, '-B', 'blk.py'], cwd=w + '/inline')
print('    inline block on 1MBN/1A6M ->', p.stdout.strip())
assert 'RMSD: 0.483 A over 151' in p.stdout
# silent-wrong case for the inline block: 1MBN vs 1A3N pairs by number with no name check
shutil.copy(D + '1A3N.pdb', w + '/inline/mobile.pdb')
p = sh([sys.executable, '-B', 'blk.py'], cwd=w + '/inline')
print('    NOTE inline block, 1MBN vs 1A3N: rc=%d stdout=%r' % (p.returncode, p.stdout.strip()))

# ---- (e) the example script's __main__ from a clean dir
os.makedirs(w + '/main', exist_ok=True)
shutil.copy(D + '1CLL.pdb', w + '/main/mobile.pdb'); shutil.copy(D + '1CFD.pdb', w + '/main/reference.pdb')
p = sh([sys.executable, '-B', '../../../skill/examples/biopython_superimposer.py'], cwd=w + '/main')
print('(e) example __main__ rc=%d\n%s%s' % (p.returncode, p.stdout, p.stderr[-300:]))
assert p.returncode == 0 and 'Superposed 144 CA pairs' in p.stdout and os.path.exists(w + '/main/mobile_superposed.pdb')
# superposed file really superposed: recompute RMSD from the written structure with numpy
sp = au.read_ca(w + '/main/mobile_superposed.pdb'); rf = au.read_ca(w + '/main/reference.pdb')
da = {(c, n, i): x for c, n, i, _, x in sp}; db = {(c, n, i): x for c, n, i, _, x in rf}
ks = sorted(set(da) & set(db)); r = float(np.sqrt(np.mean([np.sum((da[k] - db[k]) ** 2) for k in ks])))
print('    RMSD recomputed from the written mobile_superposed.pdb (no further fitting): %.3f over %d' % (r, len(ks)))
assert abs(r - 10.829) < 0.01
print('ALL ASSERTIONS OK')
