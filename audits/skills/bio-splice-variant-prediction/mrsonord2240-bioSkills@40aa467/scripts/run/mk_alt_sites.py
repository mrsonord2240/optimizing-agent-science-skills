"""Independent test of the Skill's Pangolin mask table row 'sites annotated only in non-canonical transcripts'.
DMD is on the MINUS strand. Splice-site variants = the intron base next to an exon boundary (gene-strand G of GT/AG -> A),
i.e. genomic C>T. Pick 5 sites present in the all-transcript DB but not in the canonical DB (seeded random pick, not the fixer's
sites) and 3 shared sites as controls. REF asserted (genomic C)."""
import random, gffutils
from pyfaidx import Fasta
fa = Fasta('/mnt/openscience/as-spvp-scratch/g38/hg38_chr17_chrX.upper.fa')
def sites(path):
    db = gffutils.FeatureDB(path)
    g = [g for g in db.features_of_type('gene') if g.attributes.get('gene_name', [''])[0] == 'DMD'][0]
    tx = {}
    for e in db.children(g.id, featuretype='exon'):
        tx.setdefault(e.attributes['transcript_id'][0], []).append((e.start, e.end))
    don, acc = set(), set()
    for t, ex in tx.items():
        ex.sort(reverse=True)            # minus strand: gene order = descending genomic
        for i, (s, e) in enumerate(ex):
            if i < len(ex) - 1: don.add(s - 1)      # donor +1 lies at genomic s-1
            if i > 0: acc.add(e + 1)                # acceptor -1 lies at genomic e+1
    return don, acc
dc, ac = sites('out/db_canon/gencode.v45.annotation.db')
da, aa = sites('out/db_all/gencode.v45.annotation.db')
alt = sorted([('donor', p) for p in da - dc - ac - aa if False] + [('donor', p) for p in (da - dc)] + [('acceptor', p) for p in (aa - ac)])
shared = sorted([('donor', p) for p in da & dc] + [('acceptor', p) for p in aa & ac])
print('DMD donors all/canon', len(da), len(dc), '| acceptors all/canon', len(aa), len(ac), '| alt-only sites', len(alt), '| shared', len(shared))
random.seed(7)
pick = [('altonly',) + x for x in sorted(random.sample(alt, 5), key=lambda x: x[1])] + \
       [('canonical',) + x for x in sorted(random.sample(shared, 3), key=lambda x: x[1])]
out = ['##fileformat=VCFv4.2', '##contig=<ID=chrX,length=156040895>', '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO']
for tag, kind, p in pick:
    ref = str(fa['chrX'][p - 1:p]).upper()
    print(tag, kind, p, 'REF', ref)
    assert ref == 'C', (p, ref)
    out.append(f'chrX\t{p}\tDMD_{kind}_{tag}_{p}\tC\tT\t.\t.\t.')
open('data/dmd_sites.vcf', 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
