"""Input 8 (NEW, Variant B): remote-homology workflow on protein kinases (PKA 1ATP-E, CDK2 1HCK, EGFR-family 2ITZ, plus the AFDB v6 models of
human PKA P17612 and CDK2 P24941 downloaded by 49_fetch_new_data.py) - none of these was used by the fixer's regression set except 1ATP/1HCK in tm_align.
User prompt: "PKA and CDK2 share ~25% identity. Do they share a fold? Find PKA's structural neighbours in AlphaFoldDB Swiss-Prot and CATH50, build a
structural MSA of the kinases, score the AF CDK2 model against the crystal structure (GDT-TS), and tell me which tool to use for the twilight-fold case."
Everything the SKILL documents for this workflow is executed: example tm_align, DALI block, Foldseek search + confident_hits, Foldmason example, MUSTANG row, TMscore -seq.
Run inside WSL: python scripts/80_input8_kinases_new.py   (cwd = run/)"""
import glob, os, re, shutil, subprocess, sys, urllib.request, hashlib
sys.dont_write_bytecode = True
sys.path.insert(0, 'skill/examples'); sys.path.insert(0, 'scripts')
import numpy as np
import tm_align_pairwise as t, foldseek_search as fs, foldmason_msa as fm
import alnutil as au
D = 'data/real_pdb/'; N = 'data/new/'; DB = '/mnt/openscience/audit-envs/alignment/public-data/foldseek-db/'
w = 'work/in8'; shutil.rmtree(w, ignore_errors=True); os.makedirs(w)
def sh(c, **k): return subprocess.run(c, capture_output=True, text=True, **k)
def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()[:10]

# ---- (1) pairwise: PKA vs CDK2 (twilight, same fold)
r = t.tm_align(D + '1HCK.pdb', D + '1ATP.pdb'); print('example tm_align 1ATP(E) vs 1HCK:', r)
ind = au.tmalign_independent(D + '1ATP.pdb', D + '1HCK.pdb', 'E', None)
u = t.parse_outfmt2(sh(['USalign', D + '1ATP.pdb', D + '1HCK.pdb', '-mol', 'prot', '-outfmt', '2']).stdout)
print('independent numpy:', {k: round(v, 4) if isinstance(v, float) else v for k, v in ind.items()}, '| US-align first row TM', u['tm1'], u['tm2'], u['rmsd'])
assert abs(r['tm1'] - 0.6805) < 0.01 and abs(r['tm2'] - 0.7659) < 0.01 and abs(r['rmsd'] - 2.85) < 0.05 and r['length_align'] == 254
assert abs(ind['rmsd'] - r['rmsd']) < 0.02 and abs(ind['lali'] - r['length_align']) == 0 and abs(u['tm1'] - r['tm1']) < 2e-3
print('ASSERT OK: TM %.3f/%.3f RMSD %.2f Lali %d confirmed by US-align and numpy; fold call (min TM, L=%d): %s' % (r['tm1'], r['tm2'], r['rmsd'], r['length_align'], min(r['length1'], r['length2']), t.interpret_tmscore(min(r['tm1'], r['tm2']), min(r['length1'], r['length2']))))
# sequence identity of the structural alignment must be twilight (the reason to use structure)
assert r['idali'] < 0.35, r['idali']

# ---- (2) DALI per the SKILL DaliLite block, PKA vs CDK2
dd = w + '/dali'; os.makedirs(dd + '/DAT'); shutil.copy(D + '1ATP.pdb', dd + '/1atp.pdb'); shutil.copy(D + '1HCK.pdb', dd + '/1hck.pdb'); cwd = os.getcwd(); os.chdir(dd)
for c in (['import.pl', '--pdbfile', '1atp.pdb', '--pdbid', '1atp', '--dat', 'DAT/'], ['import.pl', '--pdbfile', '1hck.pdb', '--pdbid', '1hck', '--dat', 'DAT/'],
          ['dali.pl', '--cd1', '1atpE', '--cd2', '1hckA', '--dat1', 'DAT/', '--dat2', 'DAT/', '--title', 'pka_cdk2', '--outfmt', 'summary']): sh(c)
res = open('1atpE.txt').read(); os.chdir(cwd)
ln = [l for l in res.splitlines() if '1hck' in l and l.strip().startswith('1:')]; print('DALI:', ln)
assert ln and abs(float(ln[0].split()[2]) - 24.1) < 0.3
print('ASSERT OK: DALI Z 24.1 (SKILL band > 20 = definitely homologous) though TM is only 0.68/0.77 - consistent with the SKILL table')

# ---- (3) Foldseek: PKA vs AFDB Swiss-Prot and CATH50 through the example functions
shutil.copy(D + '1ATP.pdb', w + '/pka.pdb')
res_ = {}
for tag, db in (('afdb', DB + 'Alphafold_Swiss-Prot'), ('cath', DB + 'CATH50')):
    fs.foldseek_search(w + '/pka.pdb', db, f'{w}/{tag}.m8', tmp_dir=f'{w}/tmp_{tag}/', alignment_type=2, max_seqs=1000)
    res_[tag] = fs.parse_results(f'{w}/{tag}.m8')
for tag, hits in res_.items():
    qs = sorted({h['query'] for h in hits}); print(tag, 'rows', len(hits), 'queries', qs)
qE = [q for q in {h['query'] for h in res_['afdb']} if q.endswith('E')][0]
afE = [h for h in res_['afdb'] if h['query'] == qE]; caE = [h for h in res_['cath'] if h['query'] == qE]
print('AFDB top5 for %s:' % qE, [(h['target'][:18], '%.1e' % h['evalue'], '%.3f' % h['alntmscore'], h['pident']) for h in afE[:5]])
print('CATH top3:', [(h['target'], '%.1e' % h['evalue'], '%.3f' % h['alntmscore']) for h in caE[:3]])
conf = fs.confident_hits(afE, 2); print('AFDB confident hits (alnTM>0.5, E<1e-3): %d of %d rows (rows==cap 1000? %s)' % (len(conf), len(afE), len(afE) >= 1000))
assert afE[0]['target'].startswith('AF-P05132') or afE[0]['target'].startswith('AF-P17612') or 'KAPC' in afE[0]['target'] or afE[0]['pident'] > 90
assert any('1.10.510.10' in h['target'] for h in caE[:20]), 'CATH protein kinase-like superfamily 1.10.510.10 not in top 20'
# second method: TM-align on the AFDB hit models (downloaded, public)
checked = 0
for h in [x for x in afE if x['pident'] < 100 and re.match(r'AF-[A-Z0-9]+-F1-model', x['target'])][:5]:   # canonical entries only (isoform names AF-<acc>-<n>-F1 skipped)
    acc = re.match(r'AF-([A-Z0-9]+)-F1', h['target']).group(1); dest = f'{w}/{acc}.pdb'
    try:
        urllib.request.urlretrieve(f'https://alphafold.ebi.ac.uk/files/AF-{acc}-F1-model_v6.pdb', dest)
    except Exception as e:
        print('  download failed', acc, e); continue
    x = t.parse_outfmt2(sh(['TMalign', dest, D + '1ATP.pdb', '-outfmt', '2']).stdout)   # 1ATP first chain = E
    print('  Foldseek %-24s alnTM %.3f pident %5.1f | TM-align TM(by AF) %.3f TM(by 1ATP) %.3f RMSD %.2f Lali %d' % (h['target'][:24], h['alntmscore'], h['pident'], x['tm1'], x['tm2'], x['rmsd'], x['length_align']))
    assert max(x['tm1'], x['tm2']) > 0.7; checked += 1
assert checked >= 3
print('ASSERT OK: %d top AFDB hits confirmed as kinase-fold by TM-align' % checked)

# ---- (4) Foldmason kinase structural MSA through the example (seed default) twice + MUSTANG row
kin = [D + '1ATP.pdb', D + '1HCK.pdb', D + '2ITZ.pdb', N + 'AF-P17612-F1.pdb', N + 'AF-P24941-F1.pdb']
outs = []
for tag in 'ab':
    o = f'{w}/fm_{tag}'; os.makedirs(o); outs.append(fm.foldmason_msa(kin, f'{o}/k', tmp_dir=f'{o}/tmp/', refine_iters=100, report_mode=2))
n, L = fm.summarize(outs[0]['amino_msa']); sc = fm.per_column_lddt(outs[0]['report'], L)
print('Foldmason kinases: %d files -> %d chain rows x %d columns; per-column LDDT scored %d/%d mean %.3f; md5 seed42 x2: %s %s' % (len(kin), n, L, sum(x >= 0 for x in sc), L, np.mean([x for x in sc if x >= 0]), md5(outs[0]['amino_msa']), md5(outs[1]['amino_msa'])))
assert md5(outs[0]['amino_msa']) == md5(outs[1]['amino_msa']) and n == 6 and np.mean([x for x in sc if x >= 0]) > 0.6
# independent: TM-align pairs PKA(1ATP-E) / CDK2 (1HCK): fraction in same Foldmason column
rows = {}; nm = None
for l in open(outs[0]['amino_msa']):
    l = l.rstrip('\n')
    if l.startswith('>'): nm = l[1:].split()[0]; rows[nm] = ''
    else: rows[nm] += l
print('rows:', {k: len(v.replace('-', '')) for k, v in rows.items()})
s1, _, s2 = au.parse_tmalign_alignment(sh(['TMalign', D + '1ATP.pdb', D + '1HCK.pdb']).stdout); tp = au.pairs_from_alignment(s1, s2)
ca_ = [c for c, ch in enumerate(rows['1ATP_E']) if ch != '-']; cb_ = [c for c, ch in enumerate(rows['1HCK']) if ch != '-']
hit = sum(1 for i, j in tp if ca_[i] == cb_[j]); print('TM-align pairs PKA/CDK2: %d, same Foldmason column: %d (%.0f%%)' % (len(tp), hit, 100 * hit / len(tp)))
print('   (informational: globins gave 90% in input 4; twilight kinases lower - MSA columns are a consensus of 6 rows, TM-align optimises one pair)'); assert hit / len(tp) > 0.4
# MUSTANG row from SKILL.md
mu = w + '/mustang'; os.makedirs(mu)
for f in (D + '1HCK.pdb', N + 'AF-P17612-F1.pdb', N + 'AF-P24941-F1.pdb'): shutil.copy(f, mu)
p = sh(['mustang-3.2.3', '-i', '1HCK.pdb', 'AF-P17612-F1.pdb', 'AF-P24941-F1.pdb', '-o', 'out', '-F', 'fasta'], cwd=mu)
print('MUSTANG rc', p.returncode, sorted(os.listdir(mu)))
mr = {}; nm = None
for l in open(mu + '/out.afasta'):
    l = l.rstrip('\n')
    if l.startswith('>'): nm = l[1:].split()[0]; mr[nm] = ''
    else: mr[nm] += l
print('MUSTANG rows:', {k: (len(v), len(v.replace('-', ''))) for k, v in mr.items()})
assert p.returncode == 0 and len(mr) == 3 and os.path.exists(mu + '/out.pdb')
ks = list(mr); ident = sum(1 for a_, b_ in zip(mr[ks[1]], mr[ks[2]]) if a_ == b_ and a_ != '-') ; nal = sum(1 for a_, b_ in zip(mr[ks[1]], mr[ks[2]]) if a_ != '-' and b_ != '-')
print('MUSTANG PKA-model vs CDK2-model identity over aligned columns: %d/%d = %.0f%%' % (ident, nal, 100 * ident / nal)); assert 0.15 < ident / nal < 0.45
print('ASSERT OK: SKILL MUSTANG command writes out.afasta (3 rows) + out.pdb; PKA/CDK2 identity in the twilight range')

# ---- (5) GDT-TS of the AF CDK2 model vs the crystal structure via the documented TMscore command
AF = N + 'AF-P24941-F1.pdb'; NAT = D + '1HCK.pdb'
o = sh(['TMscore', AF, NAT, '-seq']).stdout
g = dict(tm=float(re.search(r'TM-score\s*=\s*([\d.]+)', o).group(1)), gdt=float(re.search(r'GDT-TS-score=\s*([\d.]+)', o).group(1)), rmsd=float(re.search(r'RMSD of\s+the common residues=\s*([\d.]+)', o).group(1)), n=int(re.search(r'Number of residues in common=\s*(\d+)', o).group(1)))
print('TMscore -seq CDK2 model vs 1HCK:', g)
r1, r2 = au.read_ca(AF), au.read_ca(NAT, 'A')
s1, _, s2 = au.parse_tmalign_alignment(sh(['TMalign', AF, NAT]).stdout); pr = au.pairs_from_alignment(s1, s2)
P = np.array([r1[i][4] for i, _ in pr]); Q = np.array([r2[j][4] for _, j in pr]); _, R, tr = au.kabsch(P, Q); d = np.linalg.norm(P @ R.T + tr - Q, axis=1)
gdt = np.mean([(d < c).sum() / len(r2) for c in (1, 2, 4, 8)]); print('independent GDT-TS lower bound (native length %d): %.4f' % (len(r2), gdt))
assert gdt <= g['gdt'] + 0.01 and g['gdt'] - gdt < 0.08 and g['gdt'] > 0.5
tm = t.parse_outfmt2(sh(['TMalign', AF, NAT, '-outfmt', '2']).stdout); print('TM-align AF CDK2 model vs 1HCK:', tm['tm1'], tm['tm2'], tm['rmsd'])
assert abs(tm['tm2'] - g['tm']) < 0.03
print('ALL ASSERTIONS OK')
