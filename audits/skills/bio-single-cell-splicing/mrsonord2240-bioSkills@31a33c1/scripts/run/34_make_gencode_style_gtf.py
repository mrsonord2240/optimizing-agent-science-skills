"""Make a GENCODE-style GTF (adds one `gene` row per gene_id with gene_type/gene_name) from the Ensembl chrX GTF, which has no gene rows. Contigs get the chr prefix so they match the rMATS tables."""
import re, collections, sys
src, dst = sys.argv[1], sys.argv[2]
rows = [l.rstrip('\n').split('\t') for l in open(src) if not l.startswith('#')]
g = collections.OrderedDict()
for r in rows:
    a = dict(re.findall(r'(\w+) "([^"]*)"', r[8])); gid = a['gene_id']
    s, e = int(r[3]), int(r[4])
    if gid not in g: g[gid] = [r[0], r[6], s, e, a.get('gene_name', gid), a.get('gene_biotype', a.get('gene_type', 'NA'))]
    else: g[gid][2] = min(g[gid][2], s); g[gid][3] = max(g[gid][3], e)
with open(dst, 'w') as f:
    for gid, (c, st, s, e, nm, bt) in g.items():
        f.write(f'chr{c}\tENSEMBL\tgene\t{s}\t{e}\t.\t{st}\t.\tgene_id "{gid}"; gene_type "{bt}"; gene_name "{nm}";\n')
    for r in rows:
        r[0] = 'chr' + r[0]; f.write('\t'.join(r) + '\n')
print('genes', len(g), 'lines', len(g) + len(rows))
