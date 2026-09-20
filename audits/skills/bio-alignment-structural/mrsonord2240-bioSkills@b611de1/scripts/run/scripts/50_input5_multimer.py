"""Input 5 (Stress, regression of pre-fix input 5 + new complexes): multi-chain complexes.
User prompt: "Is the hemoglobin dimer 1IRD contained in the tetramer 1A3N, and how similar are the two tetramers 1A3N / 1HBA /
2HHB? Then search 1A3N against a folder of complexes and cluster them, with Foldseek-Multimer."
Checks the corrected SKILL.md multimer text: US-align -mm 1 -ter 0 (via examples/tm_align_pairwise.py multimer=True) against my own
numpy chain-mapping Kabsch/TM; easy-multimersearch (report columns, --multimer-tm-threshold rejected, --alignment-type 1);
easy-multimercluster on a directory vs file list vs glob; -mm 4 remedy removed / MSTA claim; no --byresi text left.
Run inside WSL: python scripts/50_input5_multimer.py   (cwd = run/)"""
import glob, itertools, os, re, shutil, subprocess, sys
sys.dont_write_bytecode = True
sys.path.insert(0, 'skill/examples'); sys.path.insert(0, 'scripts')
import numpy as np
import tm_align_pairwise as t
import alnutil as au

D = 'data/real_pdb/'; N = 'data/new/'
w = 'work/in5'; shutil.rmtree(w, ignore_errors=True); os.makedirs(w)
def sh(c, **k): return subprocess.run(c, capture_output=True, text=True, **k)
skill = open('skill/SKILL.md', encoding='utf-8').read()

# ---- (1) example function in multimer mode: 1IRD (dimer, mobile) vs 1A3N (tetramer, reference)
r = t.tm_align(D + '1A3N.pdb', D + '1IRD.pdb', multimer=True)
print('example tm_align(multimer=True) 1IRD -> 1A3N:', r)
assert abs(r['tm1'] - 0.9769) < 2e-3 and abs(r['tm2'] - 0.4943) < 2e-3 and r['length_align'] in (285, 286) and abs(r['rmsd'] - 0.94) < 0.05
print('ASSERT OK: 0.977 (by dimer) / 0.494 (by tetramer), RMSD 0.94, Lali %d as SKILL.md states' % r['length_align'])

# ---- (2) independent numpy: chain-assignment search (alpha->A/C, beta->B/D) with residue pairing by number
def chains(path):
    ca = au.read_ca(path); out = {}
    for c, n, i, rn, x in ca: out.setdefault(c, []).append((rn, x))
    return out
def pair_by_sequence(m, r):
    """pair two chains' residues by the ungapped shift that maximises identical residue names (chains are the same protein with different numbering)"""
    best = (-1, 0)
    for sft in range(-10, 11):
        ident = sum(1 for k in range(len(m)) if 0 <= k + sft < len(r) and m[k][0] == r[k + sft][0])
        best = max(best, (ident, sft))
    sft = best[1]
    return [(m[k][1], r[k + sft][1]) for k in range(len(m)) if 0 <= k + sft < len(r) and m[k][0] == r[k + sft][0]]
def complex_kabsch(mob, ref, assign):
    P, Q = [], []
    for mc, rc in assign.items():
        for pm, qr in pair_by_sequence(mob[mc], ref[rc]): P.append(pm); Q.append(qr)
    P, Q = np.array(P), np.array(Q)
    rmsd, R, tr = au.kabsch(P, Q); moved = P @ R.T + tr
    return rmsd, len(P), au.tm_score(moved, Q, sum(len(v) for v in mob.values())), au.tm_score(moved, Q, sum(len(v) for v in ref.values()))
def best_assignment(mob_path, ref_path):
    mob, ref = chains(mob_path), chains(ref_path)
    best = None
    for perm in itertools.permutations(ref.keys(), len(mob)):
        a = dict(zip(mob.keys(), perm))
        # only pair chains of similar length (same subunit type)
        if any(abs(len(mob[m]) - len(ref[a[m]])) > 5 for m in a): continue
        res = complex_kabsch(mob, ref, a)
        if best is None or res[3] + res[2] > best[1][3] + best[1][2]: best = (a, res)
    return best
a, res = best_assignment(D + '1IRD.pdb', D + '1A3N.pdb')
print('INDEPENDENT chain-mapping Kabsch 1IRD->1A3N: assign %s  RMSD %.3f over %d pairs, TM(by dimer) %.4f, TM(by tetramer) %.4f' % (a, *res))
assert abs(res[0] - r['rmsd']) < 0.1 and res[1] in (285, 286, 287) and abs(res[2] - r['tm1']) < 0.02 and abs(res[3] - r['tm2']) < 0.02
print('ASSERT OK: numpy independent RMSD/TM agree with US-align')

# ---- (3) tetramer vs tetramer (incl. NEW 2HHB), US-align via the example and by numpy
for ref_id, mob_id in (('1A3N', '1HBA'), ('1A3N', '2HHB')):
    mp = D + '1HBA.pdb' if mob_id == '1HBA' else N + '2HHB.pdb'
    rr = t.tm_align(D + ref_id + '.pdb', mp, multimer=True)
    a, res = best_assignment(mp, D + ref_id + '.pdb')
    print('%s vs %s: US-align TM %.4f/%.4f RMSD %.2f Lali %d | numpy TM %.4f/%.4f RMSD %.2f' % (mob_id, ref_id, rr['tm1'], rr['tm2'], rr['rmsd'], rr['length_align'], res[2], res[3], res[0]))
    assert rr['tm1'] > 0.95 and rr['tm2'] > 0.95 and abs(res[2] - rr['tm1']) < 0.02
# dimer vs the NEW tetramer too
rr = t.tm_align(N + '2HHB.pdb', D + '1IRD.pdb', multimer=True); print('1IRD in 2HHB:', rr['tm1'], rr['tm2']); assert rr['tm1'] > 0.95 and 0.4 < rr['tm2'] < 0.6

# ---- (4) -mm 4 claim and stale text
p = sh(['USalign', D + '1IRD.pdb', D + '1A3N.pdb', '-mm', '4', '-ter', '0'])
print('USalign -mm 4 (two complexes) rc=%d stdout head=%r' % (p.returncode, p.stdout[:200].replace('\n', ' | ')))
hlp = sh(['USalign', '-h']).stdout
i = hlp.index('4: MSTA'); print('USalign -h:', ' '.join(hlp[i:i + 160].split()))
assert 'MSTA' in hlp
print('stale strings in SKILL.md/usage-guide.md:', {s: (s in skill or s in open('skill/usage-guide.md', encoding='utf-8').read()) for s in ('byresi', 'multimer-tm-threshold 0.5', 'mm 4 -')})
assert 'byresi' not in skill
print('-mm 4 mentioned in SKILL.md only as:', [l.strip()[:150] for l in skill.splitlines() if '-mm 4' in l])

# ---- (5) Foldseek-Multimer commands from SKILL.md
cx = ['1A3N', '1HBA', '1ATP', '1HCK', '1DIW', '2ITZ', '2LHB', '1MBN']
os.makedirs(w + '/dir'); [shutil.copy(D + c + '.pdb', f'{w}/dir/{c}.pdb') for c in cx]; shutil.copy(N + '2HHB.pdb', w + '/dir/2HHB.pdb')
p = sh(['foldseek', 'easy-multimersearch', D + '1IRD.pdb', w + '/dir', w + '/s1', w + '/tmp1', '-v', '1']); print('easy-multimersearch rc', p.returncode)
rep = [l.split('\t') for l in open(w + '/s1_report').read().splitlines()]
print('s1_report: %d rows, %d columns' % (len(rep), len(rep[0]))); assert len(rep[0]) == 9
best = {}
for row in rep:
    k = row[1]; q, tt = float(row[4]), float(row[5])
    if k not in best or q > best[k][0]: best[k] = (q, tt, row[2], row[3])
for k, v in sorted(best.items(), key=lambda kv: -kv[1][0])[:4]: print('  target %-5s best qTM %.3f tTM %.3f query chains %s target chains %s' % (k, *v))
assert abs(best['1A3N'][0] - 0.981) < 0.01 and abs(best['1A3N'][1] - 0.492) < 0.01 and best['1A3N'][2] == 'A,B'
assert best['2HHB'][0] > 0.95 and best['1HBA'][0] > 0.95
assert all(best[k][0] < 0.2 for k in best if k in ('1ATP', '1HCK', '2ITZ', '1DIW'))
print('ASSERT OK: report qTM/tTM 0.981/0.492 for 1IRD in 1A3N (US-align 0.977/0.494); 2HHB, 1HBA >0.95; non-globins <0.2')
chain_rows = open(w + '/s1').read().count('\n'); print('result (chain-level) rows:', chain_rows)
# tmscore threshold flag on search
p = sh(['foldseek', 'easy-multimersearch', D + '1IRD.pdb', w + '/dir', w + '/s2', w + '/tmp2', '--multimer-tm-threshold', '0.5'])
print('easy-multimersearch --multimer-tm-threshold rc=%d msg=%r' % (p.returncode, (p.stdout + p.stderr).strip()[-120:])); assert p.returncode != 0
p = sh(['foldseek', 'easy-multimersearch', D + '1IRD.pdb', w + '/dir', w + '/s3', w + '/tmp3', '--alignment-type', '1', '-v', '1'])
rep3 = [l.split('\t') for l in open(w + '/s3_report').read().splitlines()]
b3 = {}
for row in rep3:
    if row[1] not in b3 or float(row[4]) > b3[row[1]][0]: b3[row[1]] = (float(row[4]), float(row[5]))
print('--alignment-type 1 (Foldseek-MM-TM): rc %d, 1A3N best qTM/tTM %s' % (p.returncode, b3['1A3N'])); assert p.returncode == 0 and b3['1A3N'][0] > 0.95

# ---- (6) easy-multimercluster: directory vs file list vs glob (SKILL: file list/glob clusters only the last file, exit 0)
def cl(tag, inputs):
    p = sh(['foldseek', 'easy-multimercluster', *inputs, f'{w}/{tag}', f'{w}/tmp_{tag}', '--multimer-tm-threshold', '0.65', '-v', '1'])
    fn = f'{w}/{tag}_cluster.tsv'
    rows = [l.split('\t') for l in open(fn).read().splitlines()] if os.path.exists(fn) else []
    return p.returncode, rows
rc, rows = cl('cdir', [w + '/dir']); print('cluster on DIRECTORY rc', rc, 'rows', len(rows)); clu = {}
for rep_, mem in rows: clu.setdefault(rep_, []).append(mem)
for k, v in clu.items(): print('   ', k, '->', sorted(v))
assert rc == 0 and len(rows) >= 9
tetra = [v for v in clu.values() if any(m.startswith('1A3N') for m in v)][0]
print('1A3N cluster members:', sorted(tetra)); assert any(m.startswith('2HHB') for m in tetra) and any(m.startswith('1HBA') for m in tetra)
rc2, rows2 = cl('clist', sorted(glob.glob(w + '/dir/*.pdb')))
print('cluster on FILE LIST (%d files) rc %d rows %d: %s' % (len(glob.glob(w + '/dir/*.pdb')), rc2, len(rows2), rows2[:3]))
assert rc2 == 0 and len(rows2) < len(rows), 'SKILL claim: file list clusters only the last file'
rc3, rows3 = cl('cthree', [w + '/dir/1A3N.pdb', w + '/dir/1HBA.pdb', w + '/dir/2HHB.pdb'])
print('cluster on 3 files rc %d rows %d %s' % (rc3, len(rows3), rows3))
print('ASSERT OK: SKILL.md claim "file list or glob clusters only the last file, still exits 0" reproduced; directory input clusters all')

# ---- (7) speed: US-align vs Foldseek-Multimer on 60 real oligomers + the planted tetramers
tg = w + '/bench'; os.makedirs(tg)
for f in glob.glob(N + 'complexes/*.pdb'): shutil.copy(f, tg)
for c in ('1HBA', '2HHB'): shutil.copy((D if c == '1HBA' else N) + c + '.pdb', tg)
targets = sorted(glob.glob(tg + '/*.pdb')); print('benchmark targets:', len(targets))
import time
t0 = time.time(); us = {}
for f in targets:
    o = sh(['USalign', D + '1A3N.pdb', f, '-mm', '1', '-ter', '0', '-outfmt', '2'], timeout=600).stdout
    row = [l.split() for l in o.splitlines() if l and not l.startswith('#')]
    if row: us[os.path.basename(f)[:4]] = (float(row[0][2]), float(row[0][3]))
t_us = time.time() - t0
t0 = time.time(); p = sh(['foldseek', 'easy-multimersearch', D + '1A3N.pdb', tg, w + '/b1', w + '/tmpb1', '-v', '1']); t_fs = time.time() - t0
t0 = time.time(); sh(['foldseek', 'createdb', tg, w + '/bdb', '-v', '1']); t_db = time.time() - t0
t0 = time.time(); p = sh(['foldseek', 'easy-multimersearch', D + '1A3N.pdb', w + '/bdb', w + '/b2', w + '/tmpb2', '-v', '1']); t_fs2 = time.time() - t0
print('SPEED: US-align -mm 1 x %d pairs: %.1f s (%.2f s/pair) | foldseek easy-multimersearch on the directory: %.1f s | createdb %.1f s + search on prebuilt DB: %.1f s' % (len(targets), t_us, t_us / len(targets), t_fs, t_db, t_fs2))
print('SPEED RATIO US-align / Foldseek (directory, includes createdb): %.1fx ; (prebuilt DB, search only): %.1fx' % (t_us / t_fs, t_us / t_fs2))
fsb = {}
for l in open(w + '/b1_report').read().splitlines():
    x = l.split('\t')
    if x[1] not in fsb or float(x[4]) > fsb[x[1]][0]: fsb[x[1]] = (float(x[4]), float(x[5]))
common = sorted(set(us) & set(fsb)); print('targets scored by both: %d of %d (Foldseek reports only those passing its prefilter: %d)' % (len(common), len(us), len(fsb)))
# what does US-align find that Foldseek-MM never reports? (TM > 0.5 by either normalisation)
miss = [k for k in us if max(us[k]) > 0.5 and k not in fsb]; print('US-align pairs with max TM > 0.5 missing from Foldseek report:', miss)
top_us = sorted(((max(v), k) for k, v in us.items()), reverse=True)[:5]; print('US-align top5 (max TM):', [(k, round(v, 3)) for v, k in top_us])
top_fs = sorted(((max(v), k) for k, v in fsb.items()), reverse=True)[:5]; print('Foldseek top5 (max TM):', [(k, round(v, 3)) for v, k in top_fs])
diffs = [abs(us[k][0] - fsb[k][0]) for k in common]
print('|TM(query-normalised) US-align - Foldseek|: median %.3f max %.3f over %d shared targets' % (np.median(diffs), max(diffs), len(common)))
open(w + '/speed.tsv', 'w').write('n_targets\tt_usalign\tt_foldseek_dir\tt_createdb\tt_foldseek_db\n%d\t%.2f\t%.2f\t%.2f\t%.2f\n' % (len(targets), t_us, t_fs, t_db, t_fs2))
print('DONE')
