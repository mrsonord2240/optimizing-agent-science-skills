"""Input 4 (variant B): structural MSA of a mixed family (8 globin structures + 3 kinases) with the Skill's
examples/foldmason_msa.py run UNMODIFIED as a subprocess from work/in4/ (structures/*.pdb, as its __main__ expects),
then the SKILL.md --report-mode 2 / per_column_lddt recipe. Asserts on MSA content vs TM-align ground truth.
Run inside WSL, cwd = run/."""
import sys, os, shutil, subprocess, json, glob, re
sys.dont_write_bytecode = True
D = 'data/real_pdb/'
w = 'work/in4'; shutil.rmtree(w, ignore_errors=True); os.makedirs(w+'/structures')
GLOBINS = ['1MBN', '1A6M', '1MBO', '1EMY', '1A3N', '1HBA', '1IRD', '2LHB']
KINASES = ['1ATP', '1HCK', '2ITZ']
for i in GLOBINS + KINASES: shutil.copy(D+i+'.pdb', f'{w}/structures/{i}.pdb')

p = subprocess.run([sys.executable, os.path.abspath('skill/examples/foldmason_msa.py')], cwd=w, capture_output=True, text=True)
print('example rc', p.returncode); print(p.stdout[-700:]); print(p.stderr[-300:] if p.returncode else '')
files = sorted(os.listdir(w)); print('files:', files)
for f in ('family_msa_aa.fa', 'family_msa_3di.fa', 'family_msa.html'):
    assert os.path.getsize(f'{w}/{f}') > 0, f
nw = [f for f in files if f.endswith(('.nw', '.newick'))]
print('guide tree files (SKILL says result.nw):', nw, '| other:', [f for f in files if 'family_msa' in f])

def fasta(path):
    d, k = {}, None
    for l in open(path):
        l = l.rstrip()
        if l.startswith('>'): k = l[1:].split()[0]; d[k] = ''
        elif k: d[k] += l
    return d
aa, di = fasta(f'{w}/family_msa_aa.fa'), fasta(f'{w}/family_msa_3di.fa')
print('n seqs in aa MSA:', len(aa), sorted(aa)); L = {len(s) for s in aa.values()}; print('column counts:', L)
assert len(L) == 1 and L == {len(s) for s in di.values()}
print('SUMMARY as printed by example says n_seqs = chains, not files: files=%d chains=%d' % (len(GLOBINS+KINASES), len(aa)))

# --- ground-truth check 1: sequences in MSA == real SEQRES-derived chain sequences? (residue counts vs CA counts)
from Bio.PDB import PDBParser
P = PDBParser(QUIET=True)
for name, s in list(aa.items()):
    stem, _, ch = name.partition('_')
    st = P.get_structure('x', f'{D}{stem}.pdb')[0]
    chains = {c.id: sum(1 for r in c if 'CA' in r and r.get_resname() != 'CA') for c in st}  # incl. modified residues (SEP/TPO in 1ATP)
    ungapped = len(s.replace('-', ''))
    if ch in chains: assert ungapped == chains[ch], (name, ungapped, chains[ch])
    elif len(chains) == 1: assert ungapped == list(chains.values())[0], (name, ungapped, chains)
print('ASSERT OK: ungapped MSA row length == number of residues with CA in the corresponding PDB chain for every row')

# --- ground-truth check 2: pairwise alignment 1MBN vs 1A3N_A implied by the MSA vs TM-align's own alignment
def pairs(a, b):
    i = j = 0; out = set()
    for x, y in zip(a, b):
        if x != '-': i += 1
        if y != '-': j += 1
        if x != '-' and y != '-': out.add((i, j))
    return out
mb = [k for k in aa if k.startswith('1MBN')][0]; ha = [k for k in aa if k.startswith('1A3N_A')][0]
fm = pairs(aa[mb], aa[ha])
o = subprocess.run(['TMalign', D+'1MBN.pdb', D+'1A3N.pdb', '-outfmt', '1'], capture_output=True, text=True).stdout.splitlines()
seqs = [l for l in o if l and not l.startswith(('>', '#', '(', 'Name', 'Total')) and set(l) <= set('ACDEFGHIKLMNPQRSTVWY-:.*XBZUO') and len(l) > 100]
print('TMalign -outfmt 1 lines kept:', len(seqs))
tm = pairs(seqs[0], seqs[2]) if len(seqs) >= 3 else pairs(seqs[0], seqs[1])
inter = len(fm & tm); print(f'Foldmason aligned pairs {len(fm)}, TM-align {len(tm)}, shared {inter}')
assert inter / max(len(tm), 1) > 0.7, inter
print('ASSERT OK: >70%% of TM-align residue pairs (1MBN/1A3N-A) are also aligned pairs in the Foldmason MSA (%.0f%%)' % (100*inter/len(tm)))

# --- ground truth 3: family structure in the guide tree / MSA identity: globins closer to each other than to kinases
def ident(a, b):
    m = t = 0
    for x, y in zip(a, b):
        if x != '-' and y != '-': t += 1; m += (x == y)
    return m / t if t else 0.0
g = [k for k in aa if k[:4] in GLOBINS]; k_ = [k for k in aa if k[:4] in KINASES]
import itertools
gg = [ident(aa[a], aa[b]) for a, b in itertools.combinations(g, 2)]; gk = [ident(aa[a], aa[b]) for a in g for b in k_]
print('mean id globin-globin %.2f | globin-kinase %.2f' % (sum(gg)/len(gg), sum(gk)/len(gk)))
assert sum(gg)/len(gg) > sum(gk)/len(gk)

# --- SKILL.md per-column LDDT recipe, --report-mode 2
subprocess.run(['foldmason', 'easy-msa', *sorted(glob.glob(w+'/structures/*.pdb')), w+'/result', w+'/tmp2', '--report-mode', '2'], check=True, capture_output=True)
print('report-mode 2 files:', sorted(f for f in os.listdir(w) if f.startswith('result')))
report = json.load(open(w+'/result.json'))
print('JSON top-level keys:', list(report))
lddt_per_column = report.get('per_column_lddt')      # SKILL.md line 220 verbatim
print("SKILL recipe report.get('per_column_lddt') ->", lddt_per_column)
sc = report['scores']; print('report["scores"]: n=%d, min=%.3f max=%.3f; n_columns in aa MSA=%d' % (len(sc), min(sc), max(sc), len(fasta(w+'/result_aa.fa')[list(fasta(w+'/result_aa.fa'))[0]])))
assert lddt_per_column is None and len(sc) == len(aa[mb])
