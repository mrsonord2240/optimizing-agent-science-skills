"""Input 2 (Variant A): fixed Skill's Bio.Phylo read/inspect/split loop VERBATIM (path only) on SYNTHETIC iq10.treefile."""
from Bio import Phylo

tree = Phylo.read('../../data/iq10.treefile', 'newick')          # exactly one tree; raises if 0 or >1
out = []                                                         # auditor
for clade in tree.get_nonterminals():
    print(clade.confidence, clade.name)          # confirm the support landed in .confidence, not .name
    if clade.confidence is None and clade.name and '/' in clade.name:   # IQ-TREE -B + --alrt: '98.5/100' stays in .name
        sh_alrt, ufboot = (float(v) for v in clade.name.split('/')[-2:])   # last field = UFBoot
        out.append((sh_alrt, ufboot, ','.join(sorted(t.name for t in clade.get_terminals()))))
# ---- auditor ----
for sh, uf, tips in out:
    print(f'{sh:6.1f} {uf:6.1f} {"STRONG" if sh >= 80 and uf >= 95 else "weak":6s} {tips}')
print('split', len(out), 'labels; joint-rule pass', sum(sh >= 80 and uf >= 95 for sh, uf, _ in out))
