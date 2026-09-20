"""Input 3 (edge): the Skill's examples/biopython_superimposer.py on real structure pairs where residue
correspondence is NOT trivially positional. Run the example script UNMODIFIED as a subprocess (from a copy in
work/in3/<case>/ with reference.pdb, mobile.pdb), parse what it prints, and compare with a ground-truth
computed independently (residue-number matched CA of the first model, ATOM records only) and with TM-align.
Cases: (A) 1MBN vs 1A6M myoglobin (153 vs 151 CA)  (B) apo/holo calmodulin 1CFD (NMR, 20 models) vs 1CLL (holo,
4 Ca2+ ions named 'CA').  Run inside WSL, cwd = run/."""
import sys, os, shutil, subprocess, re
sys.dont_write_bytecode = True
import numpy as np
from Bio.PDB import PDBParser, Superimposer
D = 'data/real_pdb/'
EX = os.path.abspath('skill/examples/biopython_superimposer.py')

def run_example(ref, mob, tag):
    w = f'work/in3/{tag}'; shutil.rmtree(w, ignore_errors=True); os.makedirs(w)
    shutil.copy(D+ref, w+'/reference.pdb'); shutil.copy(D+mob, w+'/mobile.pdb')
    p = subprocess.run([sys.executable, EX], cwd=w, capture_output=True, text=True)
    print(f'--- example on {tag}: rc={p.returncode}\n{p.stdout.strip()[:900]}\n{p.stderr.strip()[-400:]}')
    m = re.search(r'Superposed (\d+) CA atoms\s+RMSD: ([\d.]+)', p.stdout)
    return int(m.group(1)), float(m.group(2)), p.stdout

def truth(ref, mob, model=0):
    """residue-number-matched ATOM-record CA of one model each; the honest answer to 'same protein, RMSD?'"""
    P = PDBParser(QUIET=True)
    def cas(f):
        s = P.get_structure('x', D+f)[model]
        return {(c.id, r.id[1], r.id[2]): r['CA'] for c in s for r in c if r.id[0] == ' ' and 'CA' in r}
    a, b = cas(ref), cas(mob)
    common = sorted(set(a) & set(b))
    sup = Superimposer(); sup.set_atoms([a[k] for k in common], [b[k] for k in common])
    return len(common), sup.rms

def tmalign(ref, mob):
    o = subprocess.run(['TMalign', D+mob, D+ref, '-outfmt', '2'], capture_output=True, text=True).stdout
    f = [l for l in o.splitlines() if not l.startswith('#') and l.strip()][0].split()
    return float(f[2]), float(f[3]), float(f[4]), int(f[10])

# ---- Case A
n, rms, _ = run_example('1MBN.pdb', '1A6M.pdb', 'A_1MBN_1A6M')
tn, trms = truth('1MBN.pdb', '1A6M.pdb')
print(f'CASE A example: n={n} RMSD={rms:.3f} | residue-matched truth: n={tn} RMSD={trms:.3f} | TMalign: {tmalign("1MBN.pdb","1A6M.pdb")}')
print('  CA counts: 1MBN', len(list(PDBParser(QUIET=True).get_structure("a", D+"1MBN.pdb").get_atoms())), '(all atoms)')
caA = {'1MBN': [a for a in PDBParser(QUIET=True).get_structure('a', D+'1MBN.pdb').get_atoms() if a.get_id() == 'CA'],
       '1A6M': [a for a in PDBParser(QUIET=True).get_structure('b', D+'1A6M.pdb').get_atoms() if a.get_id() == 'CA']}
print('  n CA id atoms: 1MBN', len(caA['1MBN']), '1A6M', len(caA['1A6M']),
      '| non-C-alpha atoms named CA (hetero flag):', [(k, [a.get_parent().get_resname() for a in v if a.get_parent().id[0] != " "]) for k, v in caA.items()])
resA = {k: [a.get_parent().id[1] for a in v[:3]] for k, v in caA.items()}
print('  first residue numbers', resA)
assert abs(rms - trms) < 0.15, (rms, trms)   # positional truncation happens to be right for this pair
print('ASSERT OK (case A): example RMSD within 0.15 A of residue-matched ground truth')

# ---- Case B: apo vs holo calmodulin (the usage-guide's own prompt: "Compare apo and holo conformations")
n, rms, out = run_example('1CLL.pdb', '1CFD.pdb', 'B_calmodulin_apo_holo')
tn, trms = truth('1CLL.pdb', '1CFD.pdb')
print(f'CASE B example: n={n} RMSD={rms:.3f} | residue-matched, model 1, ATOM only truth: n={tn} RMSD={trms:.3f} | TMalign: {tmalign("1CLL.pdb","1CFD.pdb")}')
P = PDBParser(QUIET=True)
s_apo, s_holo = P.get_structure('a', D+'1CFD.pdb'), P.get_structure('b', D+'1CLL.pdb')
ca_apo = [a for a in s_apo.get_atoms() if a.get_id() == 'CA']; ca_holo = [a for a in s_holo.get_atoms() if a.get_id() == 'CA']
ions = [a for a in ca_holo if a.get_parent().id[0] != ' ']
print(f'  models in apo={len(s_apo)}; example CA list sizes apo={len(ca_apo)} holo={len(ca_holo)}; Ca2+ ions counted as C-alpha in holo={len(ions)} ({set(a.get_parent().get_resname() for a in ions)})')
assert len(ions) == 4
# what the example silently did: all-model, ion-contaminated, positional pairing.  It cannot be a correct apo/holo RMSD:
assert n > 2*tn or abs(rms - trms) > 1.0, 'example unexpectedly agrees with truth'
print('ASSERT OK (case B): example RMSD differs from the residue-matched ground truth by %.1f A and pairs %d CA vs %d true pairs' % (abs(rms-trms), n, tn))
