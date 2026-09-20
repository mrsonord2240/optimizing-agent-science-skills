import pyfaidx
fa = pyfaidx.Fasta('/mnt/openscience/audit-envs/alternative-splicing/public-data/longread/flair_test/genome.fa')
print(list(fa.keys()))
for p in (7676154, 7674859, 7674858):
    print('chr17:%d ref base = %s  context %s' % (p, fa['chr17'][p-1:p].seq.upper(), fa['chr17'][p-6:p+5].seq.upper()))
