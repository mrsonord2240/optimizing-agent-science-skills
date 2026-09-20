"""Input 2 (Variant A, regression of pre-fix input 2): Foldseek homolog search of myoglobin 1MBN.
User prompt: "Search my myoglobin structure against AlphaFoldDB (Swiss-Prot), CATH50 and my own folder of structures, give
the best structural hits and how many are confident homologs. Also try the TM-align refinement mode."
Uses the FIXED examples/foldseek_search.py functions (foldseek_search / parse_results / confident_hits, cap warning),
then checks by a second method: TMalign on the top AFDB hit's model, my own reading of the raw table, and the SKILL's
--alignment-type 1 E-value statement.
Run inside WSL: python scripts/20_input2_foldseek.py   (cwd = run/)"""
import glob, math, os, shutil, subprocess, sys
sys.dont_write_bytecode = True
sys.path.insert(0, 'skill/examples'); sys.path.insert(0, 'scripts')
import foldseek_search as fs
import tm_align_pairwise as t

D = 'data/real_pdb/'; DB = '/mnt/openscience/audit-envs/alignment/public-data/foldseek-db/'
w = 'work/in2'; shutil.rmtree(w, ignore_errors=True); os.makedirs(w + '/targets')
def sh(c, **k): return subprocess.run(c, capture_output=True, text=True, **k)
for f in glob.glob(D + '*.pdb'):
    if 'AF-' not in os.path.basename(f) and not os.path.basename(f).startswith('1MBN'):
        shutil.copy(f, w + '/targets/')     # 1MBN is the query, not a target ... 1MBO/1A6M/1EMY are the myoglobin targets
shutil.copy(D + '1MBN.pdb', w + '/query.pdb')
n_targets = len(glob.glob(w + '/targets/*.pdb')); print('custom target folder: %d PDB files' % n_targets)

def run(tag, database, at, max_seqs):
    m8 = f'{w}/{tag}.m8'
    fs.foldseek_search(w + '/query.pdb', database, m8, tmp_dir=f'{w}/tmp_{tag}/', alignment_type=at, max_seqs=max_seqs)
    hits = fs.parse_results(m8)
    return hits

# ---- (A) custom folder, both alignment types
h2 = run('custom2', w + '/targets', 2, 200); h1 = run('custom1', w + '/targets', 1, 200)
for name, hits, at in (('type2', h2, 2), ('type1', h1, 1)):
    conf = fs.confident_hits(hits, at)
    print(f'{name}: rows={len(hits)} confident={len(conf)}; top:', [(h['target'][:14], '%.2g' % h['evalue'], '%.3f' % h['alntmscore'], h['pident']) for h in hits[:5]])
top2 = h2[0]
assert top2['target'].startswith('1MBO') and top2['alntmscore'] > 0.99 and top2['pident'] > 80
# all confident targets must be globins (independent ground truth from the PDB ids: globin family ids)
globins = ('1MBO', '1A6M', '1EMY', '1A3N', '1HBA', '1IRD', '2LHB', '1MBN')
conf2 = fs.confident_hits(h2, 2); conf1 = fs.confident_hits(h1, 1)
bad = [h['target'] for h in conf2 + conf1 if not h['target'].startswith(globins)]
print('non-globin confident hits:', bad)
assert not bad, bad
assert len(conf1) >= len(conf2) >= 8
# the old-filter behaviour the SKILL claims is broken under type 1
old = [h for h in h1 if h['evalue'] < 1e-3 and h['alntmscore'] > 0.5]
ev = [h['evalue'] for h in h1 if h['alntmscore'] > 0.5]
print('type 1: old filter (E<1e-3 and alnTM>0.5) keeps %d; alnTM>0.5 rows %d; their E-values %.2f..%.2f' % (len(old), len(ev), min(ev), max(ev)))
assert len(old) == 0 and len(ev) > 8 and min(ev) > 0.05
print('ASSERT OK: SKILL claim "E-values are meaningless under --alignment-type 1; an evalue < 1e-3 filter returns 0 hits" reproduced; new filter keeps %d' % len(conf1))

# ---- (B) real CATH50 and AFDB Swiss-Prot, type 2, max_seqs=200 (example default)
for tag, db in (('cath', DB + 'CATH50'), ('afdb', DB + 'Alphafold_Swiss-Prot')):
    hits = run(tag, db, 2, 200)
    print(f'{tag}: rows={len(hits)}; top3:', [(h['target'][:26], '%.1e' % h['evalue'], '%.3f' % h['alntmscore'], h['pident']) for h in hits[:3]])
    if len(hits) >= 200:
        print(f'  cap warning would print (as in example __main__): {len(hits)} rows = the --max-seqs cap')
    globals()['hits_' + tag] = hits
assert len(hits_afdb) == 200 and len(hits_cath) == 200, (len(hits_afdb), len(hits_cath))
assert hits_afdb[0]['target'].startswith('AF-P02185') and hits_afdb[0]['alntmscore'] > 0.98 and hits_afdb[0]['pident'] > 99
assert 'AF-P02185' in hits_afdb[0]['target']
# with the cap lifted the true count appears (example says default is 1000)
full = run('afdb_full', DB + 'Alphafold_Swiss-Prot', 2, 1000)
print('AFDB Swiss-Prot with --max-seqs 1000: rows =', len(full), '| confident (alnTM>0.5,E<1e-3):', len(fs.confident_hits(full, 2)))
assert len(full) > 200
help_txt = sh(['foldseek', 'easy-search', '-h']).stdout
line = [l for l in help_txt.splitlines() if '--max-seqs' in l][0]
print('help:', line.strip()); assert '1000' in line
# type 1 on AFDB
a1 = run('afdb1', DB + 'Alphafold_Swiss-Prot', 1, 200)
c1 = fs.confident_hits(a1, 1); c1old = [h for h in a1 if h['evalue'] < 1e-3 and h['alntmscore'] > 0.5]
print('AFDB type 1: rows %d confident(alnTM>0.5) %d, old-filter %d; top: %s' % (len(a1), len(c1), len(c1old), [(h['target'][:20], '%.2f' % h['evalue'], '%.3f' % h['alntmscore']) for h in a1[:3]]))
assert len(c1) > len(c1old)

# ---- (C) second method: TM-align of the top AFDB hit's model against the query
r = t.tm_align(D + '1MBN.pdb', D + 'AF-P02185-F1.pdb')       # AF model = mobile
tm_top = max(r['tm1'], r['tm2'])
print('TMalign AF-P02185 model vs 1MBN:', r)
assert abs(tm_top - hits_afdb[0]['alntmscore']) < 0.02 and r['tm1'] > 0.97
print('ASSERT OK: Foldseek top AFDB hit alnTM %.4f vs TM-align %.4f/%.4f' % (hits_afdb[0]['alntmscore'], r['tm1'], r['tm2']))

# a negative control: kinase 1ATP must not hit globin targets with confidence (custom folder)
shutil.copy(D + '1ATP.pdb', w + '/kin.pdb')
fs.foldseek_search(w + '/kin.pdb', w + '/targets', w + '/kin.m8', tmp_dir=w + '/tmp_kin/', alignment_type=2, max_seqs=200)
kh = fs.parse_results(w + '/kin.m8'); kc = fs.confident_hits(kh, 2)
print('1ATP kinase query vs custom folder: confident hits ->', sorted(h['target'][:6] for h in kc))
assert kc and all(h['target'].startswith(('1HCK', '2ITZ', '1ATP')) for h in kc), 'non-kinase confident hit'
print('ASSERT OK: kinase query -> only kinase confident hits')

# ---- (D) other Foldseek commands in SKILL.md: easy-cluster and createdb --mask-bfactor-threshold and --format-output line
p = sh(['foldseek', 'easy-cluster', *sorted(glob.glob(w + '/targets/*.pdb')), w + '/cl', w + '/tmpcl', '--tmscore-threshold', '0.5', '-v', '1'])
print('easy-cluster rc', p.returncode); cl = {}
for l in open(w + '/cl_cluster.tsv'):
    a, b = l.split()[:2]; cl.setdefault(a, []).append(b)
for k, v in cl.items(): print('  cluster', k, '->', sorted(x[:6] for x in v))
def fam(x): return 'globin' if x[:4] in globins else ('kinase' if x[:4] in ('1ATP', '1HCK', '2ITZ') else 'other')
mixed = [k for k, v in cl.items() if len({fam(x) for x in v + [k]}) > 1]
assert p.returncode == 0 and not mixed, mixed
p = sh(['foldseek', 'easy-search', w + '/query.pdb', w + '/targets', w + '/cols.m8', w + '/tmpc', '--format-output', 'query,target,evalue,alntmscore,qtmscore,ttmscore,lddt,bits'])
row = open(w + '/cols.m8').readline().rstrip('\n').split('\t')
print('custom --format-output row:', row); assert len(row) == 8
p = sh(['foldseek', 'createdb', '--mask-bfactor-threshold', '70.0', D + 'AF-P04637-F1.pdb', w + '/p53m', '-v', '1'])
print('createdb --mask-bfactor-threshold 70.0 rc', p.returncode, 'files', len(glob.glob(w + '/p53m*')))
assert p.returncode == 0 and len(glob.glob(w + '/p53m*')) >= 10
print('version cmd from SKILL.md:', sh(['foldseek', 'version']).stdout.strip(), '| --version rc:', sh(['foldseek', '--version']).returncode)
