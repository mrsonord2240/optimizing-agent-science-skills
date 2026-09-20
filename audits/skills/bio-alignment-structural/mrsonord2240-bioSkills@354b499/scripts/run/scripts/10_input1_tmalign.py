"""Input 1 (canonical): TM-score / RMSD between myoglobin 1MBN and hemoglobin alpha (1A3N chain A).
Runs the Skill's own examples/tm_align_pairwise.py functions (from the copied skill), then cross-checks
against an independent second tool (US-align) and asserts ground truth.
Ground truth (real structures): 1MBN vs 1A3N-A same globin fold, ~25% seq id, RMSD ~1.5 A over ~141 CA;
1MBN vs 1ATP (kinase) different fold, TM < 0.5.
Run inside WSL: python scripts/10_input1_tmalign.py  (cwd = run/)"""
import sys, subprocess, shutil, os
sys.dont_write_bytecode = True
sys.path.insert(0, 'skill/examples')
import tm_align_pairwise as t

D = 'data/real_pdb/'
w = 'work/in1'; os.makedirs(w, exist_ok=True)
res = {}

# --- as a user would run the example: files named reference.pdb / mobile.pdb
shutil.copy(D+'1MBN.pdb', w+'/reference.pdb'); shutil.copy(D+'1A3N.pdb', w+'/mobile.pdb')
cwd = os.getcwd(); os.chdir(w)
r = t.tm_align('reference.pdb', 'mobile.pdb', output_pdb='superposed.pdb')
print('EXAMPLE tm_align dict:', r)
print('files after -o superposed.pdb:', sorted(f for f in os.listdir('.') if f.startswith('superposed')))
assert not os.path.exists('superposed.pdb'), 'unexpected: superposed.pdb exists'
assert os.path.exists('superposed.pdb.pdb')
os.chdir(cwd)

# ground-truth asserts (globin fold)
assert r['length1'] == 141 and r['length2'] == 153, (r['length1'], r['length2'])  # mobile=1A3N-A(141), reference=1MBN(153)
assert 0.89 < r['tm1'] < 0.91 and 0.83 < r['tm2'] < 0.84, r  # tm1 normalised by mobile (1A3N-A, 141), tm2 by reference 1MBN (153)
assert 1.3 < r['rmsd'] < 1.8 and r['length_align'] >= 135, r
print('ASSERT OK: tm1/tm2/rmsd/Lali match tooling-agent value (0.8356/0.9000/1.56/141) and expected globin fold')

# --- independent second tool: US-align on same pair (same order)
u = subprocess.run(['USalign', w+'/mobile.pdb', w+'/reference.pdb', '-mol', 'prot', '-outfmt', '2'],
                   capture_output=True, text=True, check=True).stdout
ur = t.parse_outfmt2(u)
print('USalign:', ur)
assert abs(ur['tm1']-r['tm1']) < 0.002 and abs(ur['tm2']-r['tm2']) < 0.002 and abs(ur['rmsd']-r['rmsd']) < 0.02
print('ASSERT OK: US-align == TM-align on monomer pair')

# --- shorter-chain claim: max(tm1,tm2) is the one normalised by the shorter chain
short_is_1 = r['length1'] < r['length2']
assert (max(r['tm1'], r['tm2']) == r['tm1']) == short_is_1
print('ASSERT OK: larger TM is the one normalised by shorter chain (L1=%d,L2=%d)' % (r['length1'], r['length2']))

# --- interpret_tmscore on this pair
tm_short = max(r['tm1'], r['tm2'])
print('interpret_tmscore(%.3f) -> %s' % (tm_short, t.interpret_tmscore(tm_short)))

# --- negative control: globin vs kinase (different fold)
neg = t.parse_outfmt2(subprocess.run(['TMalign', D+'1MBN.pdb', D+'1ATP.pdb', '-outfmt', '2'], capture_output=True, text=True, check=True).stdout)
print('1MBN vs 1ATP:', neg, '->', t.interpret_tmscore(max(neg['tm1'], neg['tm2'])))
assert max(neg['tm1'], neg['tm2']) < 0.5
# --- positive control: kinase homologs PKA vs CDK2 (real known relationship)
pos = t.parse_outfmt2(subprocess.run(['TMalign', D+'1ATP.pdb', D+'1HCK.pdb', '-outfmt', '2'], capture_output=True, text=True, check=True).stdout)
print('1ATP vs 1HCK:', pos, '->', t.interpret_tmscore(max(pos['tm1'], pos['tm2'])))
assert 0.6 < pos['tm1'] < 0.8 and pos['rmsd'] < 3.2
print('ASSERT OK: kinase pair same fold, globin-vs-kinase different fold')
# --- documented flags: -a T, -u/-L
o = subprocess.run(['TMalign', D+'1MBN.pdb', D+'1A3N.pdb', '-a', 'T', '-outfmt', '2'], capture_output=True, text=True).stdout
print('-a T -outfmt 2 stdout:\n', o)
o = subprocess.run(['TMalign', D+'1MBN.pdb', D+'1A3N.pdb', '-a', 'T'], capture_output=True, text=True).stdout
print([l for l in o.splitlines() if 'TM-score' in l])
