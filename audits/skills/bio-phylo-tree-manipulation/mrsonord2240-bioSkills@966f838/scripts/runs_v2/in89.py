"""NEW inputs (SYNTHETIC far15 / og16 IQ-TREE trees).
in8: user supplies FarOut + I13 as 'the outgroups' (not monophyletic in truth or ML tree) -> the fixed snippet's
     else-branch should refuse; also OutA+OutB-like check on far15 with FarOut alone.
in9: Bio.Phylo-written rooted tree -> the Skill's MAD strip regex VERBATIM -> mad.py; also the raw file."""
import re, subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rootsplit import score
from Bio import Phylo
PY = sys.executable
MAD = sys.argv[2]
part = sys.argv[1]
if part == 'in8':
    for og_names in (['FarOut', 'I13'], ['FarOut']):
        tree = Phylo.read('../data/far15_ml.treefile', 'newick')
        outgroup = [{'name': n} for n in og_names]
        tree.root_with_outgroup({'name': 'I1'})
        if tree.is_monophyletic([tree.find_any(**o) for o in outgroup]):
            stem = tree.common_ancestor(*outgroup).branch_length
            tree.root_with_outgroup(*outgroup, outgroup_branch_length=stem / 2)
            print(og_names, 'rooted:', score(tree, og_names), '| root children', len(tree.root.clades))
        else:
            print(og_names, '-> outgroup not monophyletic: root placement is unreliable, re-check taxon choice')
    t = Phylo.read('../data/far15_true.nwk', 'newick')
    print('truth: FarOut sister to ingroup; I13 in clade B:', sorted(x.name for x in t.root.clades[0].get_terminals())[:3])
else:
    tree = Phylo.read('in1/og16_rooted.nwk', 'newick')
    Phylo.write(tree, 'in9_biophylo.nwk', 'newick')
    nwk = open('in9_biophylo.nwk').read().strip()
    print('Bio.Phylo tail:', repr(nwk[-30:]))
    open('in9_stripped.nwk', 'w', newline='\n').write(re.sub(r'\):[0-9.eE+-]+;$', ');', nwk) + '\n')   # Skill regex
    print('stripped tail:', repr(open('in9_stripped.nwk').read().strip()[-30:]))
    for f in ('in9_biophylo.nwk', 'in9_stripped.nwk'):
        r = subprocess.run([PY, MAD, f], capture_output=True, text=True)
        out = (r.stdout + r.stderr).strip().splitlines()
        print(f, 'exit', r.returncode, '|', [l for l in out if 'MAD' in l or 'Corrupt' in l or 'AI' in l][:3])
