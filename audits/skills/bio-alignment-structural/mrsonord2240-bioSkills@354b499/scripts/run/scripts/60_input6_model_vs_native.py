"""Input 6 (scope boundary): evaluate an AlphaFold model against its crystal structure and pre-filter low-pLDDT residues.
User prompt: "Superpose AF-P02185 (AFDB model, real download) on the crystal structure 1MBN; give TM-score, RMSD, GDT-TS
and lDDT and say whether the model is 'correct'; also mask low-pLDDT residues before Foldseek indexing (p53 AF model)."
Skill gives TM-align/US-align/Foldseek; says GDT-TS is 'not reported by TM-align/Foldseek' (no tool named that is installed).
Checks: TM-align vs US-align vs PyMOL; TMscore (Zhang-lab, extra tool) for GDT-TS; Foldseek lddt column; createdb masking.
Run inside WSL, cwd = run/."""
import sys, os, subprocess, shutil, re
sys.dont_write_bytecode = True
sys.path.insert(0, 'skill/examples'); import tm_align_pairwise as t
D = 'data/real_pdb/'; w = 'work/in6'; shutil.rmtree(w, ignore_errors=True); os.makedirs(w)
def sh(c): return subprocess.run(c, capture_output=True, text=True)
AF, N = D+'AF-P02185-F1.pdb', D+'1MBN.pdb'

a = t.parse_outfmt2(sh(['TMalign', AF, N, '-outfmt', '2']).stdout); u = t.parse_outfmt2(sh(['USalign', AF, N, '-mol', 'prot', '-outfmt', '2']).stdout)
print('TMalign  AF->1MBN', a); print('USalign', u)
assert abs(a['tm1']-u['tm1']) < 0.002 and a['tm1'] > 0.97 and a['rmsd'] < 1.2
print('ASSERT OK: TM-align == US-align; model is same-fold/near-native (TM %.3f, RMSD %.2f over %d)' % (max(a['tm1'], a['tm2']), a['rmsd'], a['length_align']))

# GDT-TS: not obtainable with any tool the Skill names as installable; TMscore (same lab) prints it.
out = sh(['TMscore', AF, N]).stdout
gdt = re.search(r'GDT-TS-score=\s*([\d.]+)', out); print('TMscore GDT-TS line:', gdt.group(0) if gdt else 'NOT FOUND')
print([l for l in out.splitlines() if 'TM-score' in l or 'RMSD' in l][:3])
# note: TMscore assumes same residue numbering; 1MBN numbers residues differently from AF (Met0?) -> check with TMalign-derived alignment too
assert gdt and float(gdt.group(1)) > 0.5
# TMscore pairs by residue number; 1MBN numbers Val as 1, AF numbers Met as 1 -> off-by-one.  Renumber AF (drop Met1, shift -1):
rows = [l for l in open(AF) if l.startswith('ATOM')]
with open(w+'/AF_shift.pdb', 'w') as f:
    for l in rows:
        n = int(l[22:26])
        if n == 1: continue
        f.write(l[:22] + '%4d' % (n-1) + l[26:])
out2 = sh(['TMscore', w+'/AF_shift.pdb', N]).stdout
g2 = re.search(r'GDT-TS-score=\s*([\d.]+)', out2); r2 = re.search(r'RMSD of\s+the common residues=\s*([\d.]+)', out2)
print('TMscore after fixing the off-by-one numbering: GDT-TS', g2.group(1), 'RMSD', r2.group(1))
assert float(g2.group(1)) > 0.9 and float(r2.group(1)) < 1.5
print('NOTE: naive TMscore gave GDT-TS %s (RMSD 3.86) for a model TM-align scores 0.98 -> residue-numbering trap' % gdt.group(1))

# Foldseek lddt column, single-target DB
shutil.copy(N, w+'/1MBN.pdb'); sh(['foldseek', 'createdb', w+'/1MBN.pdb', w+'/n', '-v', '1'])
p = sh(['foldseek', 'easy-search', AF, w+'/n', w+'/r.m8', w+'/tmp', '--format-output', 'query,target,alntmscore,lddt,alnlen,pident'])
print('foldseek model->native:', open(w+'/r.m8').read().strip())
lddt = float(open(w+'/r.m8').read().split('\t')[3]); assert lddt > 0.6      # SKILL's 'correctly modelled' cutoff
print('ASSERT OK: Foldseek lddt %.3f > 0.6 cutoff' % lddt)

# ---- pLDDT masking (SKILL.md line 184): does --mask-bfactor-threshold 70 change the DB? p53 has long disordered tails
P53 = D+'AF-P04637-F1.pdb'
sh(['foldseek', 'createdb', P53, w+'/p_plain', '-v', '1']); m = sh(['foldseek', 'createdb', '--mask-bfactor-threshold', '70.0', P53, w+'/p_mask', '-v', '1'])
print('createdb masked rc', m.returncode, (m.stderr or '')[-200:])
def dump(db, out):
    # raw 3Di sequence DB data file: each entry is <seq>, newline, NUL
    raw = open(db + '_ss', 'rb').read()
    return raw.replace(bytes([0]), b'').replace(bytes([10]), b'').decode()
s1, s2 = dump(w+'/p_plain', w+'/plain.fa'), dump(w+'/p_mask', w+'/mask.fa')
print('3Di seq lengths plain/masked:', len(s1), len(s2), '| differing positions:', sum(x != y for x, y in zip(s1, s2)), '| lowercase in masked:', sum(c.islower() for c in s2), 'X in masked', s2.count('X'))
r1 = sh(['foldseek', 'easy-search', P53, w+'/p_mask', w+'/pm.m8', w+'/tmp2', '--format-output', 'query,target,evalue,bits,alntmscore,alnlen'])
r0 = sh(['foldseek', 'easy-search', P53, w+'/p_plain', w+'/pp.m8', w+'/tmp3', '--format-output', 'query,target,evalue,bits,alntmscore,alnlen'])
print('self-search plain :', open(w+'/pp.m8').read().strip()); print('self-search masked:', open(w+'/pm.m8').read().strip())
