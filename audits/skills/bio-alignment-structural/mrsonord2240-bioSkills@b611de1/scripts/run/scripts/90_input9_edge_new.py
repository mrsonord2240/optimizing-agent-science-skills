"""Input 9 (NEW, Edge): the corrected Bio.PDB Superimposer / TM-align example on inputs the fixer never listed, and the Common Errors table.
User prompt: "I have wild-type T4 lysozyme and the L99A cavity mutant, and a selenomethionine (MSE) structure of another protein, and an AF model
of PKA that I want to superpose on the crystal structure with Biopython. Also, what happens with a one-residue or ligand-only file?"
 (a) T4L 2LZM vs 181L point mutant: example vs my numpy Kabsch vs TM-align;
 (b) MSE-containing entries: how many CA pairs does the fixed example use vs the residues present (residue.id[0]==' ' drops HETATM MSE)?
 (c) AF model vs crystal by Superimposer (different chain ids / numbering) - refusal or silent?
 (d) degenerate inputs -> tm_align raises with the tool's message; Foldseek/US-align behaviour; Common Errors rows reproduced.
Run inside WSL: python scripts/90_input9_edge_new.py   (cwd = run/)"""
import glob, os, random, shutil, subprocess, sys
sys.dont_write_bytecode = True
sys.path.insert(0, 'skill/examples'); sys.path.insert(0, 'scripts')
import numpy as np
from Bio.PDB import PDBParser, Superimposer
import biopython_superimposer as bs, tm_align_pairwise as t, foldseek_search as fs
import alnutil as au
D = 'data/real_pdb/'; N = 'data/new/'; S = 'data/synthetic/'
w = 'work/in9'; shutil.rmtree(w, ignore_errors=True); os.makedirs(w)
P = PDBParser(QUIET=True)
def sh(c, **k): return subprocess.run(c, capture_output=True, text=True, **k)
def indep(a, b, ca=None, cb=None, inc=False):
    ra = {(c, n, i): x for c, n, i, _, x in au.read_ca(a, ca, include_modified=inc)}; rb = {(c, n, i): x for c, n, i, _, x in au.read_ca(b, cb, include_modified=inc)}
    ks = sorted(set(ra) & set(rb)); return au.kabsch(np.array([rb[k] for k in ks]), np.array([ra[k] for k in ks]))[0], len(ks)

# ---- (a) T4 lysozyme WT vs L99A
sup, n, mm = bs.superpose_ca(P.get_structure('r', N + '2LZM.pdb'), P.get_structure('m', N + '181L.pdb'))
ir, ik = indep(N + '2LZM.pdb', N + '181L.pdb'); tm = t.parse_outfmt2(sh(['TMalign', N + '181L.pdb', N + '2LZM.pdb', '-outfmt', '2']).stdout)
print('(a) 2LZM vs 181L: example RMSD %.3f over %d pairs (%d name mismatches) | numpy %.3f over %d | TM-align RMSD %.2f Lali %d TM %.3f/%.3f' % (sup.rms, n, mm, ir, ik, tm['rmsd'], tm['length_align'], tm['tm1'], tm['tm2']))
assert abs(sup.rms - ir) < 5e-3 and n == ik and n > 150 and sup.rms < 1.0 and 1 <= mm <= 5     # 2LZM pseudo-WT vs 181L: a few real point differences
print('ASSERT OK: point mutant is co-numbered, a few real point-mutant name differences are tolerated, RMSD small')

# ---- (b) MSE entries
print('(b) selenomethionine entries: residues in file vs CA pairs the FIXED example uses (self-superposition of a randomly rotated copy; RMSD must be ~0)')
random.seed(1)
tot_lost = []
for f in sorted(glob.glob(N + 'mse/*.pdb')):
    pid = os.path.basename(f)[:4]
    R = np.linalg.qr(np.random.default_rng(3).normal(size=(3, 3)))[0]
    if np.linalg.det(R) < 0: R[:, 0] *= -1
    rot = w + '/rot_' + os.path.basename(f)        # rotate the coordinate columns of the FILE (Bio.PDB atom.coord does not reach altloc children)
    with open(rot, 'w') as out:
        for line in open(f):
            if line.startswith(('ATOM', 'HETATM')):
                xyz = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])]) @ R.T + np.array([10.0, -5.0, 3.0])
                line = line[:30] + '%8.3f%8.3f%8.3f' % tuple(xyz) + line[54:]
            out.write(line)
    a = P.get_structure('a', f); b = P.get_structure('b', rot)
    n_mse = sum(1 for r in a[0].get_residues() if r.get_resname() == 'MSE'); n_std = sum(1 for r in a[0].get_residues() if r.id[0] == ' ' and 'CA' in r)
    n_mod = sum(1 for r in a[0].get_residues() if r.id[0] != ' ' and r.id[0] != 'W' and 'CA' in r and r.get_resname() != 'CA')
    try:
        s_, k_, m_ = bs.superpose_ca(a, b)
    except ValueError as e:
        print('   %s: refused: %s' % (pid, e)); continue
    print('   %s: %d standard residues + %d HETATM modified residues with CA (MSE %d) -> example paired %d, RMSD %.4f' % (pid, n_std, n_mod, n_mse, k_, s_.rms))
    assert s_.rms < 5e-3
    tot_lost.append((pid, n_mod, n_std + n_mod))
lost = [(p, m, tot) for p, m, tot in tot_lost if m]
print('    => residues silently left out of the RMSD: %s' % [(p, '%d of %d = %.0f%%' % (m, tot, 100 * m / tot)) for p, m, tot in lost])
skill = open('skill/SKILL.md', encoding='utf-8').read()
print('    SKILL.md warns about MSE/modified residues:', any(k in skill for k in ('MSE', 'selenomethionine', 'modified residue', 'HETATM')))

# ---- (c) AF model vs crystal structure through the Superimposer
for a_, b_, why in ((D + '1ATP.pdb', N + 'AF-P17612-F1.pdb', 'PKA crystal (chain E, numbering 1-350) vs human PKA AF model (chain A)'), (D + '1HCK.pdb', N + 'AF-P24941-F1.pdb', 'CDK2 crystal (chain A) vs CDK2 AF model (chain A)')):
    try:
        s_, k_, m_ = bs.superpose_ca(P.get_structure('r', a_), P.get_structure('m', b_))
        ik = indep(a_, b_)
        print('(c) %s: RMSD %.3f over %d pairs (%d name mismatches) | numpy %.3f over %d' % (why, s_.rms, k_, m_, ik[0], ik[1]))
    except ValueError as e:
        print('(c) %s: ValueError -> %s' % (why, str(e)[:150]))
# TM-align does it regardless of chain ids
x = t.parse_outfmt2(sh(['TMalign', N + 'AF-P17612-F1.pdb', D + '1ATP.pdb', '-outfmt', '2']).stdout); print('    TM-align PKA AF model vs 1ATP-E: TM %.3f/%.3f RMSD %.2f Lali %d' % (x['tm1'], x['tm2'], x['rmsd'], x['length_align']))

# ---- (d) degenerate inputs
for f, msg in ((S + 'one_residue.pdb', 'Sequence is too short'), (S + 'ligand_only.pdb', 'Cannot parse file')):
    try:
        t.tm_align(D + '1MBN.pdb', f); print('(d) %s: NO error' % f); raise SystemExit('tm_align did not raise')
    except RuntimeError as e:
        print('(d) tm_align(1MBN, %s) -> RuntimeError: %s' % (os.path.basename(f), str(e)[:170])); assert msg in str(e)
    raw = sh(['TMalign', f, D + '1MBN.pdb', '-outfmt', '2']); print('    raw TMalign rc=%d, data rows=%d' % (raw.returncode, sum(1 for l in raw.stdout.splitlines() if l.strip() and not l.startswith('#'))))
    assert raw.returncode == 0
u = sh(['USalign', S + 'one_residue.pdb', D + '1MBN.pdb', '-mol', 'prot', '-outfmt', '2']); print('    USalign one_residue rc=%d (SKILL: can segfault)' % u.returncode)
# Foldseek query of one residue
shutil.copy(S + 'one_residue.pdb', w + '/one.pdb'); os.makedirs(w + '/tg'); shutil.copy(D + '1MBO.pdb', w + '/tg')
p = sh(['foldseek', 'easy-search', w + '/one.pdb', w + '/tg', w + '/one.m8', w + '/tmp', '-v', '1']); print('    Foldseek one-residue query: rc=%d rows=%d' % (p.returncode, len(open(w + '/one.m8').read().splitlines()) if os.path.exists(w + '/one.m8') else -1))
p = sh(['foldseek', 'easy-search', D + '1MBN.pdb', '/nonexistent/db', w + '/x.m8', w + '/tmp2', '-v', '1']); print('    Foldseek wrong DB path: rc=%d msg=%r' % (p.returncode, (p.stdout + p.stderr).strip()[-90:])); assert p.returncode == 1 and 'does not exist' in (p.stdout + p.stderr)
# Bio.PDB 'Fixed and moving atom lists differ in size'
a = P.get_structure('a', D + '1MBN.pdb'); b = P.get_structure('b', D + '1A6M.pdb')
fa_, ma_ = [x for x in a.get_atoms() if x.id == 'CA'], [x for x in b.get_atoms() if x.id == 'CA']
try:
    Superimposer().set_atoms(fa_, ma_); print('    Bio.PDB unequal lists: no error?')
except Exception as e:
    print('    Bio.PDB unequal CA lists ->', type(e).__name__, str(e)[:80]); assert 'differ in size' in str(e)
# the fix: paired superposition works on those two files
print('    fixed pairing on same two files: RMSD %.3f over %d' % (bs.superpose_ca(a, b)[0].rms, bs.superpose_ca(P.get_structure('a', D + '1MBN.pdb'), P.get_structure('b', D + '1A6M.pdb'))[1]))
# confident_hits input robustness: empty and NaN rows
print('    confident_hits([]) ->', fs.confident_hits([], 2), '| parse_results on an empty file ->', end=' ')
open(w + '/empty.m8', 'w').close(); print(fs.parse_results(w + '/empty.m8'))
print('ALL ASSERTIONS OK')
