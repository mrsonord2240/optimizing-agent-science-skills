"""Input 7 (Adversarial): user insists on rooting with the single distant outgroup FarOut and calling a lineage
'earliest diverging'.  Root as asked, then run the Skill's checks (ingroup monophyly of known groups, support of
deep nodes, outgroup-free comparison) and score against the TRUE root/ingroup split."""
import sys, subprocess, shutil
sys.path.insert(0, '..')
from io import StringIO
from Bio import Phylo
from rootsplit import score

PY = sys.executable
T = r'F:\OpenScience\audit-envs\molecular-phylogenetics-analyst\tools'
A = ['I%d' % i for i in range(1, 8)] + ['Fast8']
B = ['I9', 'I10', 'I11', 'I12', 'I13', 'I14']

tree = Phylo.read('../../data/far15_ml.treefile', 'newick')
print('FarOut terminal branch length:', round(tree.find_any(name='FarOut').branch_length, 3))
tree.root_with_outgroup({'name': 'FarOut'})
ingroup = tree.common_ancestor(*[tree.find_any(name=n) for n in A + B])
print('ingroup basal split:', [sorted(x.name for x in c.get_terminals()) if len(c.get_terminals()) < 4 else f'{len(c.get_terminals())} taxa' for c in ingroup.clades],
      '| label on the deepest ingroup branch:', [c.name for c in ingroup.clades])
print('clade A (I1-I7,Fast8) monophyletic:', bool(tree.is_monophyletic([tree.find_any(name=n) for n in A])))
print('clade B (I9-I14) monophyletic:', bool(tree.is_monophyletic([tree.find_any(name=n) for n in B])))
Phylo.draw_ascii(tree)

# outgroup-free comparison on the ingroup-only tree (Skill: run MAD and MinVar and prefer agreement)
ing = Phylo.read('../../data/far15_ml.treefile', 'newick')
ing.prune('FarOut')
Phylo.write(ing, 'ingroup14.nwk', 'newick')
r = subprocess.run([PY, T + r'\mad\mad\mad.py', 'ingroup14.nwk'], capture_output=True, text=True)
print('MAD on Bio.Phylo output:', [l for l in r.stdout.splitlines() if 'Corrupt' in l or 'AI =' in l])
# Bio.Phylo writes a root branch length ':0;' that MAD 2.2 rejects; strip it and rerun
txt = open('ingroup14.nwk').read().strip().replace('):0;', ');')
open('ingroup14.nwk', 'w').write(txt + '\n')
r = subprocess.run([PY, T + r'\mad\mad\mad.py', 'ingroup14.nwk'], capture_output=True, text=True)
print('MAD after stripping root length:', [l.strip() for l in r.stdout.splitlines() if 'MAD =' in l or 'AI =' in l])
subprocess.run([PY, T + r'\MinVar-Rooting-master\FastRoot.py', '-i', 'ingroup14.nwk', '-m', 'MV', '-o', 'ingroup14_mv.nwk'], capture_output=True)
mid = Phylo.read('ingroup14.nwk', 'newick'); mid.root_at_midpoint()
for lab, t in [('FarOut outgroup', Phylo.read(StringIO(tree.format('newick')), 'newick')),
               ('midpoint', mid),
               ('MAD', Phylo.read('ingroup14.nwk.rooted', 'newick')),
               ('MinVar', Phylo.read('ingroup14_mv.nwk', 'newick'))]:
    if lab == 'FarOut outgroup':
        t.prune('FarOut')
    print(f'{lab:16s}', score(t, A))
