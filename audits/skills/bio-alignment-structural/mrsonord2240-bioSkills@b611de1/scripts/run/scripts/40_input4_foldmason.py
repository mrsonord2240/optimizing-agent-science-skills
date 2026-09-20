"""Input 4 (Variant B, regression of pre-fix input 4): Foldmason structural MSA of 8 globin + 3 kinase structures with
per-column LDDT.
User prompt: "Build a structural MSA from these 11 PDB structures (globins and kinases) with Foldmason, keep it reproducible,
and give me the per-column LDDT."
Checks: the FIXED examples/foldmason_msa.py (foldmason_msa / summarize / per_column_lddt, incl. its __main__) and the SKILL.md
JSON snippet run verbatim; determinism (--refine-seed 42 twice, --refine-iters 0 twice, unseeded twice); rows == chains; the MSA rows ungap to
the true chain sequences (independent PDB parse); 'scores' key; TM-align residue pairs recovered by the MSA columns (independent method).
Run inside WSL: python scripts/40_input4_foldmason.py   (cwd = run/)"""
import glob, hashlib, json, os, re, shutil, subprocess, sys, time
sys.dont_write_bytecode = True
sys.path.insert(0, 'skill/examples'); sys.path.insert(0, 'scripts')
import foldmason_msa as fm
import alnutil as au

D = 'data/real_pdb/'
w = 'work/in4'; shutil.rmtree(w, ignore_errors=True); os.makedirs(w + '/structures')
def sh(c, **k): return subprocess.run(c, capture_output=True, text=True, **k)
def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()
files = ['1MBN', '1MBO', '1A6M', '1EMY', '1A3N', '1HBA', '1IRD', '2LHB', '1ATP', '1HCK', '2ITZ']
for f in files: shutil.copy(D + f + '.pdb', f'{w}/structures/{f}.pdb')
structs = sorted(glob.glob(w + '/structures/*.pdb')); print(len(structs), 'structure files')
THREE = {'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLN':'Q','GLU':'E','GLY':'G','HIS':'H','ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V'}
true_seq = {}
for f in structs:
    stem = os.path.basename(f)[:-4]
    ca = au.read_ca(f, include_modified=True); chains = sorted({c for c, *_ in ca})
    for c in chains: true_seq[(stem, c)] = ''.join(THREE.get(r, 'X') for cc, n, i, r, x in ca if cc == c)
print('independent chain count with CA atoms: %d chains across %d files' % (len(true_seq), len(structs)))

# ---- (1) the example __main__ style call, twice, in different dirs (seed default 42)
t0 = time.time(); out = {}
for tag in ('a', 'b'):
    d = f'{w}/run_{tag}'; os.makedirs(d)
    out[tag] = fm.foldmason_msa(structs, f'{d}/family_msa', tmp_dir=f'{d}/tmp/', refine_iters=100, report_mode=2)
print('two example runs took %.0fs' % (time.time() - t0)); print(out['a'])
for k in ('amino_msa', 'structural_msa', 'guide_tree', 'report'):
    assert os.path.exists(out['a'][k]) and os.path.getsize(out['a'][k]) > 100, k
assert md5(out['a']['amino_msa']) == md5(out['b']['amino_msa']) and md5(out['a']['structural_msa']) == md5(out['b']['structural_msa'])
print('ASSERT OK: --refine-seed 42 twice -> identical aa md5 %s and 3Di md5 %s' % (md5(out['a']['amino_msa'])[:10], md5(out['a']['structural_msa'])[:10]))

n_seqs, length = fm.summarize(out['a']['amino_msa'])
print('summarize -> rows %d, columns %d' % (n_seqs, length))
assert n_seqs == len(true_seq), (n_seqs, len(true_seq))     # rows == chains
# names + content of rows
rows = {}
name = None
for l in open(out['a']['amino_msa']):
    l = l.rstrip('\n')
    if l.startswith('>'): name = l[1:].split()[0]; rows[name] = ''
    else: rows[name] += l
names = list(rows); print('row names:', names)
assert all(len(v) == length for v in rows.values())
def key_of(nm):
    m = re.match(r'^(.+)_([A-Za-z0-9])$', nm)
    return (m.group(1), m.group(2)) if m and (m.group(1), m.group(2)) in true_seq else (nm, sorted(c for (s, c) in true_seq if s == nm)[0])
mism = []
for nm, seq in rows.items():
    s, c = key_of(nm)
    ts, ug = true_seq[(s, c)], seq.replace('-', '')
    # modified residues (SEP/TPO/MSE, HETATM) are written by the PDB as 'X' in my parse; compare everywhere else
    if len(ts) != len(ug) or any(a != b and a != 'X' for a, b in zip(ts, ug)): mism.append((nm, len(ug), len(ts)))
    elif 'X' in ts: print('  note: %s has %d modified residue(s) (my parse X) that Foldmason writes as %s' % (nm, ts.count('X'), [ug[i] for i, a in enumerate(ts) if a == 'X']))
print('rows whose ungapped sequence != independently parsed chain sequence:', mism)
assert not mism
print('ASSERT OK: all %d rows are chains named <file>_<chain> (single-chain files bare stem) and ungap to the real chain sequences' % len(rows))
assert sum(1 for n in names if re.search(r'_[A-Z]$', n)) > 0 and any(n in [os.path.basename(f)[:-4] for f in structs] for n in names)

# ---- (2) JSON: keys, 'scores' vs per_column_lddt, example function, SKILL.md snippet verbatim
rep = json.load(open(out['a']['report']))
print('JSON keys:', list(rep.keys()), '| entries[0] keys:', list(rep['entries'][0].keys()))
assert set(['entries', 'scores', 'tree', 'statistics']) <= set(rep) and rep.get('per_column_lddt') is None
assert set(['name', 'aa', 'ss', 'ca']) <= set(rep['entries'][0]), 'SKILL says entries rows: name, aa, ss, ca'
scores = fm.per_column_lddt(out['a']['report'], length)
valid = [x for x in scores if x >= 0]
print('per_column_lddt: %d scores, %d columns scored (%d = -1), mean %.3f' % (len(scores), len(valid), scores.count(-1), sum(valid) / len(valid)))
assert len(scores) == length and scores.count(-1) + len(valid) == length and 0 <= min(valid) and max(valid) <= 1
# entries[0].aa equals the FASTA row of the same name
e0 = rep['entries'][0]; print('entries[0].name', e0['name'], '| aa == FASTA row:', e0['aa'] == rows.get(e0['name'], rows.get(e0['name'].split('.')[0])))
skill = open('skill/SKILL.md', encoding='utf-8').read()
blk = [b for b in re.findall(r'```python\n(.*?)```', skill, re.S) if "report['scores']" in b][0]
os.makedirs(w + '/inline', exist_ok=True); shutil.copy(out['a']['report'], w + '/inline/result.json')
open(w + '/inline/blk.py', 'w', encoding='utf-8').write(blk + '\nprint("SNIPPET OK", len(lddt_per_column))\n')
p = sh([sys.executable, '-B', 'blk.py'], cwd=w + '/inline'); print('SKILL.md JSON snippet:', p.stdout.strip(), p.stderr[-200:])
assert 'SNIPPET OK %d' % length in p.stdout
# meaning of scores: globin-only columns should score better than a mixed globin/kinase column set? report the split by ungapped occupancy
occ = [sum(1 for r in rows.values() if r[i] != '-') for i in range(length)]
hi = [s for s, o in zip(scores, occ) if s >= 0 and o >= len(rows) * 0.9]; lo = [s for s, o in zip(scores, occ) if s >= 0 and o < len(rows) * 0.5]
print('mean LDDT, columns >=90%% occupied: %.3f (n=%d) | <50%% occupied: %.3f (n=%d)' % (sum(hi) / max(1, len(hi)), len(hi), sum(lo) / max(1, len(lo)), len(lo)))

# ---- (3) tree and html
from Bio import Phylo
tr = Phylo.read(out['a']['guide_tree'], 'newick'); tips = [t.name for t in tr.get_terminals()]
print('guide tree tips: %d' % len(tips)); assert len(tips) == n_seqs
d = f'{w}/html'; os.makedirs(d)
fm.foldmason_msa(structs, f'{d}/h', tmp_dir=f'{d}/tmp/', refine_iters=0, report_mode=1)
print('report-mode 1 html:', os.path.getsize(d + '/h.html'), 'bytes; startswith <!DOCTYPE/<html:', open(d + '/h.html', errors='ignore').read(200).lower().count('<html') > 0)
assert os.path.getsize(d + '/h.html') > 100000

# ---- (4) determinism claims: refine-iters 0 twice; unseeded 100 twice
def cli(tag, extra):
    d = f'{w}/{tag}'; os.makedirs(d)
    p = sh(['foldmason', 'easy-msa', *structs, f'{d}/r', f'{d}/tmp', *extra, '-v', '1'])
    assert p.returncode == 0, p.stderr[-300:]
    return f'{d}/r_aa.fa'
z1, z2 = cli('z1', ['--refine-iters', '0']), cli('z2', ['--refine-iters', '0'])
print('--refine-iters 0 twice: identical =', md5(z1) == md5(z2), md5(z1)[:10])
assert md5(z1) == md5(z2)
u = [cli(f'u{i}', ['--refine-iters', '100']) for i in range(3)]
print('unseeded --refine-iters 100 x3 md5:', [md5(x)[:10] for x in u], '| columns:', [fm.summarize(x)[1] for x in u])
s = [cli(f's{i}', ['--refine-iters', '100', '--refine-seed', '7']) for i in range(2)]
print('--refine-seed 7 x2 identical:', md5(s[0]) == md5(s[1]), '| seed 7 vs seed 42 identical:', md5(s[0]) == md5(out['a']['amino_msa']))
assert md5(s[0]) == md5(s[1])
n_diff = len({md5(x) for x in u}); print('distinct unseeded outputs:', n_diff, 'of 3')
def ap(fa):
    R, nm = {}, None
    for l in open(fa):
        l = l.rstrip('\n')
        if l.startswith('>'): nm = l[1:].split()[0]; R[nm] = ''
        else: R[nm] += l
    idx = {n: 0 for n in R}; out = set()
    L = len(next(iter(R.values())))
    for c in range(L):
        col = [(n, idx[n]) for n, s in R.items() if s[c] != '-']
        for n, s in R.items():
            if s[c] != '-': idx[n] += 1
        for a in range(len(col)):
            for b in range(a + 1, len(col)): out.add((col[a], col[b]))
    return out
A, B = ap(u[0]), ap(u[1])
print('unseeded aligned-pair overlap: |A|=%d |B|=%d shared %.1f%% of A' % (len(A), len(B), 100 * len(A & B) / len(A)))

# ---- (5) independent check: fraction of TM-align residue pairs (1MBN vs 1A3N chain A) that Foldmason aligns in the same column
ind = subprocess.run(['TMalign', f'{w}/structures/1A3N.pdb', f'{w}/structures/1MBN.pdb'], capture_output=True, text=True).stdout
s1, _, s2 = au.parse_tmalign_alignment(ind); tp = au.pairs_from_alignment(s1, s2)   # (i in 1A3N chain A, j in 1MBN), 0-based over CA lists
ra = rows['1A3N_A']; rb = rows['1MBN']
cols_a = [c for c, ch in enumerate(ra) if ch != '-']; cols_b = [c for c, ch in enumerate(rb) if ch != '-']
hit = sum(1 for i, j in tp if cols_a[i] == cols_b[j])
print('TM-align residue pairs 1MBN/1A3N-A: %d; same MSA column in Foldmason: %d (%.0f%%)' % (len(tp), hit, 100 * hit / len(tp)))
assert hit / len(tp) > 0.7

# ---- (6) Common Errors row: single structure
os.makedirs(f'{w}/one', exist_ok=True)
p = sh(['foldmason', 'easy-msa', f'{w}/structures/1MBN.pdb', f'{w}/one/r', f'{w}/one/tmp', '-v', '1'])
print('single structure: rc=%d tail=%r' % (p.returncode, (p.stdout + p.stderr).strip()[-160:]))
p = sh(['foldmason', 'version']); q = sh(['foldmason', '--version']); print('foldmason version ->', p.stdout.strip(), '| --version rc', q.returncode)
print('ALL ASSERTIONS OK')
