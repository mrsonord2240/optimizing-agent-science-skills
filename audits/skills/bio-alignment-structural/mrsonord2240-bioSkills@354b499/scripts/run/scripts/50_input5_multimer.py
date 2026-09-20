"""Input 5 (stress / multi-part): multi-chain complexes + clustering + database-scale multimer claims in SKILL.md.
 (1) examples/tm_align_pairwise.py tm_align(multimer=True) = USalign -mm 1 -ter 0, on hemoglobin tetramer 1A3N vs dimer 1IRD
     and tetramer 1A3N vs tetramer 1HBA (Trp37Arg mutant, must give TM ~1);
 (2) SKILL.md "-mm 4 -byresi 0 for different stoichiometry" claim;
 (3) foldseek easy-multimersearch exactly as in SKILL.md, including --multimer-tm-threshold 0.5, and easy-multimercluster;
 (4) foldseek easy-cluster --tmscore-threshold 0.5 on 14 real PDBs: expect globins together, kinases together, toxin alone.
Run inside WSL, cwd = run/."""
import sys, os, shutil, subprocess, glob, collections
sys.dont_write_bytecode = True
sys.path.insert(0, 'skill/examples')
import tm_align_pairwise as t
D = 'data/real_pdb/'
w = 'work/in5'; shutil.rmtree(w, ignore_errors=True); os.makedirs(w)
def sh(cmd, **k): return subprocess.run(cmd, capture_output=True, text=True, **k)

# (1) monomer TM-align example function in multimer mode
r = t.tm_align(D+'1A3N.pdb', D+'1IRD.pdb', multimer=True)      # cmd = USalign 1IRD 1A3N -mm 1 -ter 0
print('USalign -mm 1 -ter 0  1IRD(dimer, mobile) vs 1A3N(tetramer, ref):', r)
assert r['length1'] == 287 - 1 or r['length1'] > 250
print('  L1=%d L2=%d Lali=%d TM(by dimer)=%.4f TM(by tetramer)=%.4f' % (r['length1'], r['length2'], r['length_align'], r['tm1'], r['tm2']))
assert r['tm1'] > 0.9 and 0.4 < r['tm2'] < 0.6          # dimer aligns fully into tetramer; tetramer is half covered
r2 = t.tm_align(D+'1A3N.pdb', D+'1HBA.pdb', multimer=True)
print('USalign -mm 1 -ter 0 1HBA vs 1A3N (both tetramers):', r2)
assert r2['tm1'] > 0.95 and r2['tm2'] > 0.95
print('ASSERT OK: dimer-in-tetramer gives TM ~0.97/0.49 (whole-complex TM depends on which complex normalises); tetramer vs mutant tetramer ~1.0')
o = sh(['USalign', D+'1IRD.pdb', D+'1A3N.pdb', '-mm', '1', '-ter', '0']).stdout
print('\n'.join(l for l in o.splitlines() if 'TM-score' in l or 'Aligned' in l or 'Chain' in l)[:800])
# the SKILL says: "For different stoichiometries ... use -mm 4 and -byresi 0"
p = sh(['USalign', D+'1IRD.pdb', D+'1A3N.pdb', '-mm', '4', '-byresi', '0', '-ter', '0'])
print('USalign -mm 4 -byresi 0 rc=%d\nstdout[:600]=%s\nstderr[:600]=%s' % (p.returncode, p.stdout[:600], p.stderr[:600]))
mm4_ok = ('TM-score' in p.stdout) and ('Aligned length' in p.stdout)
print('  -mm 4 (MSTA = multiple chains -> consensus) produced a pairwise complex TM-score table:', mm4_ok)

# (3) Foldseek-Multimer
cx = ['1A3N', '1HBA', '1IRD', '1ATP', '1HCK', '1DIW', '2ITZ', '2LHB', '1MBN']
for c in cx: shutil.copy(D+c+'.pdb', f'{w}/{c}.pdb')
p = sh(['foldseek', 'createdb', *[f'{w}/{c}.pdb' for c in cx], f'{w}/cdb', '-v', '1']); print('createdb rc', p.returncode)
a = sh(['foldseek', 'easy-multimersearch', w+'/1A3N.pdb', w+'/cdb', w+'/mm1', w+'/tmp1'])
print('easy-multimersearch (SKILL line 118 form) rc=%d, out lines=%s' % (a.returncode, sum(1 for _ in open(w+'/mm1')) if os.path.exists(w+'/mm1') else None))
print(open(w+'/mm1').read()[:600] if os.path.exists(w+'/mm1') else a.stdout[-500:]+a.stderr[-500:])
b = sh(['foldseek', 'easy-multimersearch', w+'/1A3N.pdb', w+'/cdb', w+'/mm2', w+'/tmp2', '--multimer-tm-threshold', '0.5'])
print('easy-multimersearch ... --multimer-tm-threshold 0.5 (SKILL line 119) rc=%d' % b.returncode)
print((b.stdout+b.stderr).strip()[-500:])
b2 = sh(['foldseek', 'easy-multimersearch', w+'/1A3N.pdb', w+'/cdb', w+'/mm3', w+'/tmp3', '--alignment-type', '1'])
print('easy-multimersearch --alignment-type 1 (=Foldseek-MM-TM?) rc=%d' % b2.returncode, open(w+'/mm3').read()[:300] if os.path.exists(w+'/mm3') else '')
c = sh(['foldseek', 'easy-multimercluster', *[f'{w}/{x}.pdb' for x in cx], w+'/mc', w+'/tmpc', '--multimer-tm-threshold', '0.65'])
print('easy-multimercluster (SKILL line 121) rc=%d' % c.returncode, (c.stdout+c.stderr)[-300:] if c.returncode else '')
for f in sorted(glob.glob(w+'/mc_*')): print(' ', f, open(f).read()[:400].replace('\n', ' | '))

# (4) easy-cluster --tmscore-threshold 0.5 on all-real PDB set
allp = sorted(x for x in glob.glob(D+'*.pdb') if 'AF-' not in x and '1CFD' not in x and '1CLL' not in x and '1UBQ' not in x and '1PGA' not in x)
d = sh(['foldseek', 'easy-cluster', *allp, w+'/cl', w+'/tmpcl', '--tmscore-threshold', '0.5'])
print('easy-cluster rc', d.returncode)
cl = collections.defaultdict(list)
for l in open(w+'/cl_cluster.tsv'):
    rep, mem = l.split()[:2]; cl[os.path.basename(rep).split('.pdb')[0]].append(os.path.basename(mem).split('.pdb')[0])
for k, v in cl.items(): print('  cluster rep', k, '->', v)
def fam(x):
    s = x[:4]
    return 'globin' if s in ('1MBN','1A6M','1MBO','1EMY','1A3N','1HBA','1IRD','2LHB') else ('kinase' if s in ('1ATP','1HCK','2ITZ') else 'other')
mixed = {k: v for k, v in cl.items() if len({fam(x) for x in v + [k]}) > 1}
print('mixed-family clusters:', mixed)
assert not mixed
print('ASSERT OK: no cluster mixes globin/kinase/toxin at TM>0.5')
