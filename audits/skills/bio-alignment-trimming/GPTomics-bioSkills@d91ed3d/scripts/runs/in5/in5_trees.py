"""Input 5: AUDITOR CHECK -- RF to the true tree, branch-length accuracy and support per trimmer."""
import dendropy
from dendropy.calculate import treecompare
from Bio import AlignIO

files = ['input', 'clip_kpic-smart-gap', 'clip_smart-gap', 'clip_kpic-gappy', 'clip_kpi-smart-gap', 'trimal_strictplus',
         'trimal_automated1', 'trimal_gappyout', 'bmge112_h04', 'bmge112_h05', 'bmge200_e04']
tns = dendropy.TaxonNamespace()
truth = dendropy.Tree.get(path='../../data/deep16_true.nwk', schema='newick', taxon_namespace=tns)
truth.is_rooted = False; truth.encode_bipartitions()
L0 = AlignIO.read('input.fasta', 'fasta').get_alignment_length()
print(f'{"method":<22}{"retained":>9}{"RF":>4}{"wRF":>8}{"BLdist":>8}{"TL":>8}{"TL_true":>8}  UFBoot<95  lnL')
for f in files:
    t = dendropy.Tree.get(path=f'tree_{f}.treefile', schema='newick', taxon_namespace=tns)
    t.is_rooted = False; t.encode_bipartitions()
    rf = treecompare.symmetric_difference(truth, t)
    wrf = treecompare.weighted_robinson_foulds_distance(truth, t)
    bl = treecompare.euclidean_distance(truth, t)
    tl, tlt = t.length(), truth.length()
    sup = [float(n.label) for n in t.internal_nodes() if n.label not in (None, '')]
    iq = open(f'tree_{f}.iqtree').read()
    lnl = [l.split(':')[1].split('(')[0].strip() for l in iq.splitlines() if l.startswith('Log-likelihood of the tree')]
    L = AlignIO.read(f + '.fasta', 'fasta').get_alignment_length()
    print(f'{f:<22}{L/L0:>9.1%}{rf:>4}{wrf:>8.3f}{bl:>8.3f}{tl:>8.2f}{tlt:>8.2f}  {sum(s < 95 for s in sup)}/{len(sup)}  {lnl}')
