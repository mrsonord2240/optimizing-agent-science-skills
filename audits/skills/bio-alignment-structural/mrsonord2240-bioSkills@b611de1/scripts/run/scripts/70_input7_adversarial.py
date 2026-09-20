"""Input 7 (Adversarial, regression of pre-fix input 7): "Ubiquitin (1UBQ) and protein G B1 (1PGA) have TM > 0.5, so they are homologs - give me the p-value."
Checks the FIXED SKILL.md: does it (a) refuse to equate fold with homology and admit no p-value is printed, (b) give the safer fold call
min(TM1,TM2), (c) guard chains < 60 residues, and does the numeric claim "with max, 3 of 86 different-fold pairs exceeded 0.5 (1PGA vs three kinases
0.505-0.544); with min none (136 pairs)" reproduce on real PDB entries.
Run inside WSL: python scripts/70_input7_adversarial.py   (cwd = run/)"""
import glob, itertools, os, shutil, subprocess, sys
sys.dont_write_bytecode = True
sys.path.insert(0, 'skill/examples'); sys.path.insert(0, 'scripts')
import tm_align_pairwise as t
D = 'data/real_pdb/'; w = 'work/in7'; shutil.rmtree(w, ignore_errors=True); os.makedirs(w)
def sh(c, **k): return subprocess.run(c, capture_output=True, text=True, **k)

r = t.tm_align(D + '1PGA.pdb', D + '1UBQ.pdb')       # mobile 1UBQ (76), reference 1PGA (56)
print('1UBQ vs 1PGA:', r)
lo = min(r['length1'], r['length2']); tmin, tmax = min(r['tm1'], r['tm2']), max(r['tm1'], r['tm2'])
print('min TM %.3f max TM %.3f shorter chain %d -> interpret(min): %s | interpret(max) old-style: %s' % (tmin, tmax, lo, t.interpret_tmscore(tmin, lo), t.interpret_tmscore(tmax, lo)))
assert tmax < 0.55 and tmin < 0.5 and t.interpret_tmscore(tmax, lo).startswith('chain < 60')
# second method: US-align + Foldseek + DaliLite
u = t.parse_outfmt2(sh(['USalign', D + '1UBQ.pdb', D + '1PGA.pdb', '-mol', 'prot', '-outfmt', '2']).stdout)
assert abs(u['tm1'] - r['tm1']) < 2e-3 and abs(u['tm2'] - r['tm2']) < 2e-3
os.makedirs(w + '/t'); shutil.copy(D + '1PGA.pdb', w + '/t/'); shutil.copy(D + '1UBQ.pdb', w + '/q.pdb')
sh(['foldseek', 'easy-search', w + '/q.pdb', w + '/t', w + '/fs.m8', w + '/tmp', '--format-output', 'query,target,evalue,alntmscore,pident', '-v', '1']); print('Foldseek 1UBQ->1PGA:', open(w + '/fs.m8').read().strip() or '<no hit>')
dd = w + '/dali'; os.makedirs(dd + '/DAT')
shutil.copy(D + '1UBQ.pdb', dd + '/1ubq.pdb'); shutil.copy(D + '1PGA.pdb', dd + '/1pga.pdb'); cwd = os.getcwd(); os.chdir(dd)
for c in (['import.pl', '--pdbfile', '1ubq.pdb', '--pdbid', '1ubq', '--dat', 'DAT/'], ['import.pl', '--pdbfile', '1pga.pdb', '--pdbid', '1pga', '--dat', 'DAT/'], ['dali.pl', '--cd1', '1ubqA', '--cd2', '1pgaA', '--dat1', 'DAT/', '--dat2', 'DAT/', '--title', 'x', '--outfmt', 'summary']): sh(c)
res = open('1ubqA.txt').read(); print('DALI:', [l for l in res.splitlines() if l.strip().startswith('1:') and 'pga' in l]); os.chdir(cwd)
# is there any p-value in the tools' output? (SKILL: "no tool here prints one")
full = sh(['TMalign', D + '1UBQ.pdb', D + '1PGA.pdb']).stdout + sh(['USalign', D + '1UBQ.pdb', D + '1PGA.pdb']).stdout
print('"p-value" / "P-value" in TMalign+USalign full output:', 'p-value' in full.lower())
assert 'p-value' not in full.lower()
skill = open('skill/SKILL.md', encoding='utf-8').read()
i = skill.index('### TM-score Threshold Caveats'); print('SKILL text:', skill[i:i + 620].replace('\n', ' '))
print('SKILL says fold != homology:', 'not proof of homology' in skill, '| says no p-value printed:', 'no tool here prints a p-value' in skill)

# ---- the numeric claim: max vs min rule over real entries (first chain of each; TM-align reads first chain)
fold = {'1MBN': 'globin', '1MBO': 'globin', '1A6M': 'globin', '1EMY': 'globin', '1A3N': 'globin', '1HBA': 'globin', '1IRD': 'globin', '2LHB': 'globin', 'AF-P02185-F1': 'globin',
        '1ATP': 'kinase', '1HCK': 'kinase', '2ITZ': 'kinase', '1CFD': 'EF-hand', '1CLL': 'EF-hand', '1UBQ': 'b-grasp', '1PGA': 'b-grasp', '1DIW': 'toxin'}
rows = []
for a, b in itertools.combinations(fold, 2):
    x = t.parse_outfmt2(sh(['TMalign', D + a + '.pdb', D + b + '.pdb', '-outfmt', '2']).stdout)
    rows.append((a, b, fold[a] == fold[b], max(x['tm1'], x['tm2']), min(x['tm1'], x['tm2']), min(x['length1'], x['length2'])))
diff = [x for x in rows if not x[2]]; same = [x for x in rows if x[2]]
fpmax = [x for x in diff if x[3] > 0.5]; fpmin = [x for x in diff if x[4] > 0.5]
print('pairs: %d total, %d known-different-fold, %d same-fold' % (len(rows), len(diff), len(same)))
print('false same-fold calls, max rule: %d ->' % len(fpmax), [(a, b, round(m, 3)) for a, b, s, m, n, L in fpmax])
print('false same-fold calls, min rule: %d ->' % len(fpmin), [(a, b, round(n, 3)) for a, b, s, m, n, L in fpmin])
print('same-fold pairs recognised (>0.5): max rule %d/%d, min rule %d/%d' % (sum(x[3] > .5 for x in same), len(same), sum(x[4] > .5 for x in same), len(same)))
missed = [(a, b, round(n, 3), round(m, 3)) for a, b, s, m, n, L in same if n <= 0.5]; print('same-fold pairs missed by min rule:', missed)
assert len(fpmax) >= 1 and len(fpmin) == 0
print('ASSERT OK: min rule gives 0 false same-fold calls where max gives %d (SKILL: 3 of 86, 1PGA vs kinases)' % len(fpmax))

# ---- SKILL claim: a synthetic 10-residue helix scores 0.846 vs myoglobin normalised by its own length
h = t.tm_align(D + '1MBN.pdb', 'data/synthetic/helix10.pdb'); print('helix10 vs 1MBN:', h)
print('  interpret(max=%.3f, L=%d): %s' % (max(h['tm1'], h['tm2']), min(h['length1'], h['length2']), t.interpret_tmscore(max(h['tm1'], h['tm2']), min(h['length1'], h['length2']))))
assert abs(max(h['tm1'], h['tm2']) - 0.846) < 0.02 and t.interpret_tmscore(max(h['tm1'], h['tm2']), 10).startswith('chain < 60')
print('ASSERT OK: 0.846 short-helix trap reproduced and the example guard fires')
