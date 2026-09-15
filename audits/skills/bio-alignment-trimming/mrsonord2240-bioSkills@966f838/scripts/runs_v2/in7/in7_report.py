"""Input 7 report: retention vs the Skill's 20%/40% rule, UFBoot, and AUDITOR RF to the true tree."""
import dendropy
from dendropy.calculate import treecompare
from Bio import AlignIO

tns = dendropy.TaxonNamespace()
truth = dendropy.Tree.get(path='../../data/prot15_true.nwk', schema='newick', taxon_namespace=tns)
truth.is_rooted = False; truth.encode_bipartitions()
L0 = AlignIO.read('input.fasta', 'fasta').get_alignment_length()
print(f'{"alignment":<11}{"cols":>6}{"retained":>9}  rule                     UFBoot>=95  meanUFB  RF_true  wRF')
for f in ['input', 'smartgap', 'strictplus', 'kpism', 'kpi', 'nogaps']:
    L = AlignIO.read(f + '.fasta', 'fasta').get_alignment_length()
    r = L / L0
    rule = 'light' if r > 0.8 else ('>40% removed: too aggressive' if r < 0.6 else '20-40% removed')
    t = dendropy.Tree.get(path=f't_{f}.contree', schema='newick', taxon_namespace=tns)
    t.is_rooted = False; t.encode_bipartitions()
    sup = [float(n.label) for n in t.internal_nodes() if n.label not in (None, '')]
    ml = dendropy.Tree.get(path=f't_{f}.treefile', schema='newick', taxon_namespace=tns)
    ml.is_rooted = False; ml.encode_bipartitions()
    rf = treecompare.symmetric_difference(truth, ml)
    wrf = treecompare.weighted_robinson_foulds_distance(truth, ml)
    print(f'{f:<11}{L:>6}{r:>9.1%}  {rule:<25}{sum(s >= 95 for s in sup):>4}/{len(sup):<6}{sum(sup)/len(sup):>7.1f}{rf:>8}{wrf:>7.3f}')
