import gffutils
for n in ['canon','all']:
    db = gffutils.FeatureDB(f'out/db_{n}/gencode.v45.annotation.db')
    print(n, {t: db.count_features_of_type(t) for t in db.featuretypes()})
    g = [g for g in db.features_of_type('gene') if g.attributes.get('gene_name',[''])[0]=='DMD']
    print(len(g), g[0].id, g[0].start, g[0].end, g[0].strand)
    ex = list(db.region(seqid='chrX', start=g[0].start, end=g[0].end, featuretype='exon'))
    print('exons in region', len(ex), 'unique ends', len({e.end for e in ex if e.strand=='+'}), 'strands', {e.strand for e in ex})
    kids = list(db.children(g[0].id, featuretype='exon'))
    print('children exons', len(kids))
