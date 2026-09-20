"""Input 2 (variant A): find structural homologs of myoglobin 1MBN with Foldseek using the Skill's
examples/foldseek_search.py (foldseek_search + parse_results) against
 (a) a custom target DB of 13 real PDBs (ground truth known), (b) real CATH50, (c) real AFDB Swiss-Prot.
Asserts on parsed content, not exit code. Run inside WSL, cwd = run/."""
import sys, os, subprocess, math, glob
sys.dont_write_bytecode = True
sys.path.insert(0, 'skill/examples')
import foldseek_search as fs
import tm_align_pairwise as t

DB = '/mnt/openscience/audit-envs/alignment/public-data/foldseek-db/'
D = 'data/real_pdb/'
w = 'work/in2'; os.makedirs(w, exist_ok=True)
Q = D+'1MBN.pdb'

# ---------- (a) custom DB of real PDBs (query itself excluded so it cannot be trivially first)
targets = [p for p in sorted(glob.glob(D+'*.pdb')) if not p.endswith(('1MBN.pdb', 'AF-P02185-F1.pdb'))]
subprocess.run(['foldseek', 'createdb', *targets, w+'/custom', '-v', '1'], check=True)
for at in (2, 1):
    out = f'{w}/custom_at{at}.m8'
    fs.foldseek_search(Q, w+'/custom', out, tmp_dir=f'{w}/tmp_c{at}', alignment_type=at)
    hits = fs.parse_results(out)
    print(f'--- custom DB alignment-type {at}: {len(hits)} rows; first 8:')
    for h in hits[:8]:
        print('  %-14s E=%-9.2e alnTM=%.3f qTM=%.3f tTM=%.3f lddt=%.3f alnlen=%d id=%.1f' % (h['target'][:14], h['evalue'], h['alntmscore'], h['qtmscore'], h['ttmscore'], h['lddt'], h['alnlen'], h['pident']))
    names = [h['target'] for h in hits]
    globins = ('1MBO', '1A6M', '1EMY', '1A3N', '1HBA', '1IRD', '2LHB')
    top = [n.split('.pdb')[0].split('_')[0] for n in names[:3]]
    assert all(n in ('1MBO', '1A6M', '1EMY') for n in top), top      # myoglobins first
    conf = [h for h in hits if h['alntmscore'] > 0.5 and h['evalue'] < 1e-3]
    nonglob = {h['target'].split('.pdb')[0].split('_')[0] for h in conf} - set(globins)
    print(f'   confident (alnTM>0.5,E<1e-3): {len(conf)}, non-globin among them: {sorted(nonglob)}')
    assert not nonglob, nonglob                                       # no kinase / toxin false positive
    # all rows parsed with exactly 10 columns (parse_results would have warned/skipped otherwise)
    assert len(hits) == sum(1 for _ in open(out))
print('ASSERT OK: custom DB ranks myoglobins first, no non-globin passes the alnTM>0.5,E<1e-3 filter, 10 columns parse')

# independent check of Foldseek alnTM with TM-align on the same pair 1MBN vs 1A3N chain A
h = [x for x in fs.parse_results(f'{w}/custom_at1.m8') if x['target'].startswith('1A3N')]
print('foldseek --alignment-type 1 rows for 1A3N:', [(x['target'], x['alntmscore'], x['qtmscore'], x['ttmscore'], x['alnlen']) for x in h])
tm = t.parse_outfmt2(subprocess.run(['TMalign', D+'1MBN.pdb', D+'1A3N.pdb', '-outfmt', '2'], capture_output=True, text=True, check=True).stdout)
print('TMalign 1MBN vs 1A3N-A: tm(1MBN)=%.4f tm(1A3N-A)=%.4f Lali=%d' % (tm['tm1'], tm['tm2'], tm['length_align']))
best = max(h, key=lambda x: x['alntmscore'])
assert abs(best['qtmscore'] - tm['tm1']) < 0.05 and abs(best['ttmscore'] - tm['tm2']) < 0.05, (best, tm)
print('ASSERT OK: Foldseek --alignment-type 1 qTM/tTM within 0.05 of TM-align')

# ---------- (b) CATH50 and (c) AFDB Swiss-Prot with the Skill's function + default alignment type 2
for name in ('CATH50', 'Alphafold_Swiss-Prot'):
    out = f'{w}/{name}.m8'
    fs.foldseek_search(Q, DB+name, out, tmp_dir=f'{w}/tmp_{name}', alignment_type=2)
    hits = fs.parse_results(out)
    print(f'--- {name}: {len(hits)} rows')
    for h in hits[:5]:
        print('  %-28s E=%-9.2e alnTM=%.3f lddt=%.3f alnlen=%d id=%.1f' % (h['target'][:28], h['evalue'], h['alntmscore'], h['lddt'], h['alnlen'], h['pident']))
    conf = [h for h in hits if h['alntmscore'] > 0.5 and h['evalue'] < 1e-3]
    print(f'   confident homologs: {len(conf)}')
    assert len(hits) > 100 and conf
    if name.startswith('Alpha'):
        assert hits[0]['target'].startswith('AF-P02185'), hits[0]     # sperm whale myoglobin = the query's own protein
        assert hits[0]['pident'] > 99 and hits[0]['alntmscore'] > 0.98
        # check: AF model vs 1MBN with TM-align
        tm = t.parse_outfmt2(subprocess.run(['TMalign', Q, D+'AF-P02185-F1.pdb', '-outfmt', '2'], capture_output=True, text=True, check=True).stdout)
        print('   TMalign 1MBN vs AF-P02185-F1 (downloaded model):', tm['tm1'], tm['tm2'], tm['rmsd'], tm['length_align'])
        assert tm['tm1'] > 0.95
        # is the 100%-id hit really a myoglobin? count MYG in names
        print('   MYG_-like hits in top 20 (by AFDB Swiss-Prot names):', sum('P0218' in h['target'] or 'P0214' in h['target'] for h in hits[:20]))
print('ASSERT OK: AFDB Swiss-Prot top hit is AF-P02185 (sperm whale myoglobin), 100% id, alnTM>0.98; TM-align on downloaded model agrees')
