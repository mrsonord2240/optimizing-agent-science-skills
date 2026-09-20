"""Input 7 (adversarial / ambiguous): user prompt "My 76-aa ubiquitin (1UBQ) and 56-aa protein G B1 domain (1PGA) give TM > 0.5 with TM-align,
so per your table they share a fold; the other TM > 0.8 row says 'homologous'. Please confirm they are homologs and give the
p-value for TM = 0.5." Ground truth (SCOP/CATH): both beta-grasp folds, different superfamilies, NOT homologs;
DaliLite Z = 2.8 (see logs/11_dali_pymol.txt: 'candidate', below the 8+ 'probable homology' band).
Checks what the Skill's numbers/functions say and whether the Skill can produce the length-aware p-value it recommends.
Run inside WSL, cwd = run/."""
import sys, subprocess, shutil, os
sys.dont_write_bytecode = True
sys.path.insert(0, 'skill/examples'); import tm_align_pairwise as t
D = 'data/real_pdb/'
def tm(a, b, tool='TMalign'):
    cmd = [tool, D+a, D+b, '-outfmt', '2'] + (['-mol', 'prot'] if tool == 'USalign' else [])
    return t.parse_outfmt2(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)
r = tm('1PGA.pdb', '1UBQ.pdb'); u = tm('1PGA.pdb', '1UBQ.pdb', 'USalign')
print('TMalign 1PGA vs 1UBQ:', r); print('USalign               :', u)
assert abs(r['tm1']-u['tm1']) < 0.003
best = max(r['tm1'], r['tm2'])
print('interpret_tmscore(max) ->', t.interpret_tmscore(best), '| tm normalised by shorter (1PGA, L=%d)=%.3f' % (r['length1'], r['tm1']))
# null: same short chain vs unrelated real structures, both normalisations
null = []
for x in ('1MBN', '1ATP', '1DIW', '2ITZ', '1HCK', '1CLL', '1HBA'):
    q = tm('1PGA.pdb', x+'.pdb'); null.append((x, q['tm1'], q['tm2'], q['rmsd'], q['length_align']))
    print('  1PGA vs %s: TM(by 1PGA, L=56)=%.3f TM(by %s)=%.3f RMSD=%.2f Lali=%d' % (x, q['tm1'], x, q['tm2'], q['rmsd'], q['length_align']))
print('max over null of larger-TM (Skill-recommended metric):', max(max(a, b) for _, a, b, _, _ in null))
# foldseek significance
w = 'work/in7'; shutil.rmtree(w, ignore_errors=True); os.makedirs(w)
subprocess.run(['foldseek', 'createdb', D+'1UBQ.pdb', w+'/ubq', '-v', '1'], capture_output=True)
subprocess.run(['foldseek', 'easy-search', D+'1PGA.pdb', w+'/ubq', w+'/r.m8', w+'/tmp', '--format-output', 'query,target,evalue,bits,alntmscore,lddt,alnlen,pident', '-e', '1000'], capture_output=True)
print('foldseek 1PGA -> 1UBQ (-e 1000):', open(w+'/r.m8').read().strip() or 'NO HIT')
# does any shipped tool print a TM-score p-value? (Skill: use Xu & Zhang 2010 Gumbel p-value)
o = subprocess.run(['TMalign', D+'1PGA.pdb', D+'1UBQ.pdb'], capture_output=True, text=True).stdout
print('TMalign prints a p-value:', 'p-value' in o.lower() or 'p=' in o.lower())
o2 = subprocess.run(['USalign', D+'1PGA.pdb', D+'1UBQ.pdb'], capture_output=True, text=True).stdout
print('USalign prints a p-value:', 'p-value' in o2.lower())
print([l for l in o2.splitlines() if 'TM-score' in l])
# ASSERTS: ground truth = same fold (beta-grasp) but NOT homologous; Skill's TM>0.5 rule alone is right about fold, its '>0.8 (homologous)' row is the risky one
assert 0.3 < best < 0.75
