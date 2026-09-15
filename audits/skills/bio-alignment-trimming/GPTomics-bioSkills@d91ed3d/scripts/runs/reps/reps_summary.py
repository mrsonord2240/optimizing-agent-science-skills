"""AUDITOR CHECK: retention and RF-to-truth per method across the 10 SYNTHETIC replicates."""
import dendropy
from dendropy.calculate import treecompare
from Bio import AlignIO

methods = ['untrimmed', 'smartgap', 'kpicsg', 'kpisg', 'strictplus', 'gappyout']
tns = dendropy.TaxonNamespace()
truth = dendropy.Tree.get(path='../../data/prot15_true.nwk', schema='newick', taxon_namespace=tns)
truth.is_rooted = False; truth.encode_bipartitions()
res = {m: [] for m in methods}
print(f'{"rep":<5}' + ''.join(f'{m:>22}' for m in methods))
for i in range(1, 11):
    row = f'{i:02d}   '
    L0 = AlignIO.read(f'rep{i:02d}.untrimmed.fasta', 'fasta').get_alignment_length()
    for m in methods:
        L = AlignIO.read(f'rep{i:02d}.{m}.fasta', 'fasta').get_alignment_length()
        t = dendropy.Tree.get(path=f't_rep{i:02d}.{m}.treefile', schema='newick', taxon_namespace=tns)
        t.is_rooted = False; t.encode_bipartitions()
        rf = treecompare.symmetric_difference(truth, t)
        res[m].append((L / L0, rf))
        row += f'{L/L0:>12.1%} RF={rf:<6}'
    print(row)
print('\nmethod        mean_retention  mean_RF  total_RF  reps_retention<0.7  reps_removed>40%')
for m in methods:
    r = res[m]
    print(f'{m:<13} {sum(x for x,_ in r)/10:>13.1%} {sum(y for _,y in r)/10:>8.2f} {sum(y for _,y in r):>9} '
          f'{sum(x < 0.7 for x,_ in r):>19} {sum(x < 0.6 for x,_ in r):>17}')
