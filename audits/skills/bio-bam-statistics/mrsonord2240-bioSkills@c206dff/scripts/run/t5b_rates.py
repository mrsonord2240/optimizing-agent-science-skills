import csv, sys
sys.path.insert(0, '.')
from truth import counts
print('sample | batch-loop Mapped/Total | true primary-mapped/primary | QC-fail records dropped by loop | secondary+supp counted as "mapped" by loop')
for r in csv.DictReader(open('work/batch/summary.tsv'), delimiter='\t'):
    T = counts(f"work/batch/{r['Sample']}.bam")
    loop = 100 * int(r['Mapped']) / int(r['Total'])
    true = 100 * T['primary_mapped'] / T['primary']
    print(f"{r['Sample']:16s} {loop:6.2f}%   {true:6.2f}%   qcfail_dropped={T['qcfail']:3d}   nonprimary_in_loop={T['secondary']+T['supplementary']}")
