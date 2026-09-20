"""Judge the SKILL.md sentence "three unseeded --refine-iters 100 runs gave three different MSAs (377-378 columns, only 74% of
aligned pairs shared; homologous pairs 88%)": re-measure with the same metric (mean per-sequence-pair Jaccard of aligned residue pairs
between unseeded runs) on (A) the 5-structure set the first audit used and (B) the 11-structure set of input 4 (three unseeded runs
already in work/in4/u0..u2).  Run inside WSL (cwd = run/, after 40_input4_foldmason.py)."""
import glob, itertools, os, shutil, subprocess, sys, hashlib
sys.dont_write_bytecode = True
D = 'data/real_pdb/'
def fa(p):
    d = {}; k = None
    for l in open(p):
        l = l.strip()
        if l.startswith('>'): k = l[1:].split()[0]; d[k] = ''
        elif k: d[k] += l
    return d
def pairs(x, y):
    i = j = 0; o = set()
    for c, d in zip(x, y):
        if c != '-': i += 1
        if d != '-': j += 1
        if c != '-' and d != '-': o.add((i, j))
    return o
def jacc(paths, fam=None):
    runs = [fa(p) for p in paths]; allj, same, cross = [], [], []
    for a, b in itertools.combinations(range(len(runs)), 2):
        for p, q in itertools.combinations(list(runs[0]), 2):
            s, t = pairs(runs[a][p], runs[a][q]), pairs(runs[b][p], runs[b][q]); j = len(s & t) / max(len(s | t), 1)
            allj.append(j)
            if fam: (same if fam(p) == fam(q) else cross).append(j)
    m = lambda x: sum(x) / len(x) if x else float('nan')
    return m(allj), m(same), m(cross)
def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()[:8]
fam = lambda n: 'k' if n.startswith(('1ATP', '1HCK', '2ITZ')) else 'g'

# (B) 11-structure set, runs from input 4
B = [f'work/in4/u{i}/r_aa.fa' for i in range(3)]
mB = jacc(B, fam)
print('(B) 11 structures (19 chain rows), 3 unseeded runs: md5', [md5(p) for p in B], '| mean per-pair Jaccard %.3f, same-family %.3f, cross-family %.3f, columns %s' % (*mB, [len(next(iter(fa(p).values()))) for p in B]))
# (A) 5-structure set
w = 'work/var5'; shutil.rmtree(w, ignore_errors=True); os.makedirs(w + '/s')
five = ['1MBN', '1A3N', '2LHB', '1ATP', '1HCK']
for f in five: shutil.copy(D + f + '.pdb', f'{w}/s/{f}.pdb')
paths = []
for i in range(3):
    o = f'{w}/u{i}'; os.makedirs(o)
    p = subprocess.run(['foldmason', 'easy-msa', *sorted(glob.glob(w + '/s/*.pdb')), o + '/r', o + '/tmp', '--refine-iters', '100', '-v', '1'], capture_output=True, text=True)
    assert p.returncode == 0; paths.append(o + '/r_aa.fa')
mA = jacc(paths, fam)
print('(A) 5 structures (9 chain rows), 3 unseeded runs: md5', [md5(p) for p in paths], '| mean per-pair Jaccard %.3f, same-family %.3f, cross-family %.3f, columns %s' % (*mA, [len(next(iter(fa(p).values()))) for p in paths]))
print('SKILL.md states 74%% shared / 88%% homologous / 377-378 columns.')
