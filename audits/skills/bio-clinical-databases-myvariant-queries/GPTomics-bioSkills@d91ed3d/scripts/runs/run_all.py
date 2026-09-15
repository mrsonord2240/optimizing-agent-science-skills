# myvariant.info audit driver: one function per input, output to in<N>/out.txt. Live myvariant.info (BioThings),
# 2026-09-15, myvariant client 1.0.0. SKILL.md code verbatim below (marked); shipped example via git copy.
import contextlib, importlib.util, io, json, os, sys, time, traceback
import requests
import myvariant
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------- SKILL.md verbatim blocks ----------------
mv = myvariant.MyVariantInfo()

CLINICAL_FIELDS = [
    'clinvar.clinical_significance',
    'clinvar.review_status',
    'clinvar.variant_id',
    'gnomad_exome.faf95',
    'gnomad_exome.af.af',
    'gnomad_exome.an.an',
    'gnomad_genome.faf95',
    'gnomad_genome.af.af',
    'dbsnp.rsid',
    'dbnsfp.alphamissense.score',
    'dbnsfp.alphamissense.pred',
    'dbnsfp.revel.score',
    'dbnsfp.cadd.phred',
    'dbnsfp.spliceai.master_pred',
    'dbnsfp.spliceai.ds_max',
    'cosmic.cosmic_id',
    'civic.openCravatUrl',
    '_meta'
]

def annotate_variant_list(hgvs_list):
    '''Batch-annotate variants with ClinVar / gnomAD / dbNSFP / COSMIC / CIViC fields.'''
    chunked = [hgvs_list[i:i+1000] for i in range(0, len(hgvs_list), 1000)]
    rows = []
    versions = None
    for chunk in chunked:
        results = mv.getvariants(chunk, fields=CLINICAL_FIELDS)
        for r in results:
            if versions is None and r.get('_meta'):
                versions = {src: meta.get('version') for src, meta in r['_meta'].get('src', {}).items()}
            clinvar = r.get('clinvar', {}) or {}
            gnomad_e = r.get('gnomad_exome', {}) or {}
            gnomad_g = r.get('gnomad_genome', {}) or {}
            dbnsfp = r.get('dbnsfp', {}) or {}
            faf95 = (gnomad_e.get('faf95', {}) or gnomad_g.get('faf95', {})) or {}
            rows.append({
                'variant': r.get('query'),
                'clinvar_sig': clinvar.get('clinical_significance'),
                'clinvar_review': clinvar.get('review_status'),
                'gnomad_grpmax_faf95': faf95.get('popmax'),
                'grpmax_ancestry': faf95.get('popmax_population'),
                'gnomad_af': gnomad_e.get('af', {}).get('af') or gnomad_g.get('af', {}).get('af'),
                'rsid': r.get('dbsnp', {}).get('rsid'),
                'alphamissense': dbnsfp.get('alphamissense', {}).get('score'),
                'revel': dbnsfp.get('revel', {}).get('score'),
                'cadd_phred': dbnsfp.get('cadd', {}).get('phred'),
                'spliceai_ds_max': dbnsfp.get('spliceai', {}).get('ds_max')
            })
    return pd.DataFrame(rows), versions

def find_pathogenic_in_gene(gene_symbol, max_results=500):
    '''Find ClinVar P/LP variants in a gene.'''
    query = f'clinvar.gene.symbol:{gene_symbol} AND '\
            'clinvar.clinical_significance:(Pathogenic OR "Likely pathogenic")'
    hits = mv.query(query, size=max_results, fields=['_id', 'clinvar.clinical_significance',
                                                       'clinvar.review_status'])
    return hits.get('hits', [])

def find_high_cadd_in_region(chrom, start, end, min_cadd=25):
    '''Find variants in region with CADD phred above threshold.'''
    query = f'chrom:{chrom} AND hg19.start:[{start} TO {end}] AND '\
            f'dbnsfp.cadd.phred:>{min_cadd}'
    return mv.query(query, size=500, fields=['_id', 'dbnsfp.cadd.phred', 'clinvar.clinical_significance'])

def find_alphamissense_pathogenic(gene, min_score=0.564):
    '''Find AlphaMissense pathogenic missense in a gene.'''
    query = f'dbnsfp.genename:{gene} AND dbnsfp.alphamissense.score:>{min_score}'
    return mv.query(query, size=500, fields=['_id', 'dbnsfp.alphamissense', 'clinvar.clinical_significance'])
# ---------------- end SKILL.md blocks ----------------

spec = importlib.util.spec_from_file_location('ex', os.path.join(HERE, 'query_myvariant.upstream_copy.py'))
ex = importlib.util.module_from_spec(spec); spec.loader.exec_module(ex)
nap = lambda: time.sleep(0.5)


def in1():
    """Canonical: 'Annotate BRAF V600E and three rsIDs with ClinVar, gnomAD grpmax FAF95, AlphaMissense, REVEL, CADD,
    SpliceAI; record source versions.'"""
    ids = ['chr7:g.140453136A>T', 'rs121913529', 'rs1800566', 'rs104894155']
    df, versions = annotate_variant_list(ids)
    print('SKILL.md annotate_variant_list:'); print(df.to_string(index=False))
    print('versions from per-record _meta:', versions)
    raw = mv.getvariant('chr7:g.140453136A>T', fields=['_meta', 'clinvar', 'dbnsfp.alphamissense', 'gnomad_exome.faf95'])
    print('raw keys:', sorted(raw.keys()) if raw else raw)
    print('raw clinvar keys:', sorted((raw or {}).get('clinvar', {}).keys())[:25])
    print('raw gnomad_exome:', json.dumps((raw or {}).get('gnomad_exome'))[:300])
    print('raw dbnsfp.alphamissense:', json.dumps((raw or {}).get('dbnsfp'))[:300])
    nap()
    print('\n== shipped example __main__ ==')
    src = open(os.path.join(HERE, 'query_myvariant.upstream_copy.py')).read().split("if __name__ == '__main__':")[1]
    exec(compile('\n'.join(l[4:] for l in src.splitlines()), 'example_main', 'exec'), ex.__dict__)


def in2():
    """Variant A: 'Find all ClinVar Pathogenic / Likely pathogenic variants in BRCA1.'"""
    hits = find_pathogenic_in_gene('BRCA1')
    print('SKILL.md find_pathogenic_in_gene(BRCA1) hits:', len(hits)); nap()
    for q in ('clinvar.gene.symbol:BRCA1', 'clinvar.gene.symbol:BRCA1 AND clinvar.rcv.clinical_significance:Pathogenic',
              'clinvar.gene.symbol:BRCA1 AND clinvar.clinical_significance:Pathogenic'):
        r = mv.query(q, size=1, fields='clinvar.rcv.clinical_significance'); nap()
        print(f'total for {q!r}: {r.get("total")}')
    h = ex.find_pathogenic_in_gene('BRCA1', min_star=2)
    print('example find_pathogenic_in_gene(BRCA1, min_star=2): total', h.get('total'), 'hits', len(h.get('hits', [])))


def in3():
    """Edge: 'Pull high-CADD variants around BRAF V600E and a variant given by rsID that is multi-allelic.'"""
    r = find_high_cadd_in_region('7', 140453100, 140453200); nap()
    print('SKILL.md find_high_cadd_in_region(7, 140453100-140453200 hg19) total:', r.get('total'), [h['_id'] for h in r.get('hits', [])[:5]])
    r = find_high_cadd_in_region('7', 140753300, 140753400); nap()
    print('same function with GRCh38 coordinates total:', r.get('total'))
    print('field probe dbnsfp.cadd vs cadd.phred for BRAF V600E:')
    g = mv.getvariant('chr7:g.140453136A>T', fields=['dbnsfp.cadd', 'cadd.phred']); nap()
    print('  ', json.dumps(g)[:300])
    rs = mv.getvariants(['rs334'], fields='dbsnp.rsid', scopes='dbsnp.rsid'); nap()
    print('rs334 by scopes=dbsnp.rsid ->', [x.get('_id') for x in rs])
    rs2 = mv.getvariants(['rs334'], fields='dbsnp.rsid'); nap()
    print('rs334 with default scopes (as in SKILL annotate_variant_list) ->', [(x.get('query'), x.get('notfound'), x.get('_id')) for x in rs2])


def in4():
    """Variant B: 'AlphaMissense-pathogenic missense in BRAF, with source versions for the methods section.'"""
    r = find_alphamissense_pathogenic('BRAF'); nap()
    print('SKILL.md find_alphamissense_pathogenic(BRAF) total:', r.get('total'), [h['_id'] for h in r.get('hits', [])[:3]])
    print('example metadata_versions (first 12):', dict(list(ex.metadata_versions().items())[:12])); nap()
    meta = requests.get('https://myvariant.info/v1/metadata', timeout=30).json()
    print('metadata src keys include dbnsfp/clinvar/gnomad_exome:', [k for k in ('dbnsfp', 'clinvar', 'gnomad_exome', 'cadd') if k in meta.get('src', {})])
    print('dbnsfp version:', meta.get('src', {}).get('dbnsfp', {}).get('version'), '| clinvar:', meta.get('src', {}).get('clinvar', {}).get('version'))


def in5():
    """Stress / adversarial: '1,500 variants in one POST, then call PP3_Strong for my patient from AlphaMissense > 0.564.'"""
    ids = [f'chr7:g.{140453000 + i}A>T' for i in range(1500)]
    r = requests.post('https://myvariant.info/v1/variant', data={'ids': ','.join(ids), 'fields': 'dbsnp.rsid'}, timeout=120)
    try:
        j = r.json(); print('raw POST 1500 ids: HTTP', r.status_code, type(j).__name__, (len(j) if isinstance(j, list) else json.dumps(j)[:200]))
    except Exception:
        print('raw POST 1500 ids: HTTP', r.status_code, r.text[:200])
    nap()
    res = mv.getvariants(ids, fields='dbsnp.rsid')
    print('client getvariants(1500 ids) returned records:', len(res))


for name in ('in1', 'in2', 'in3', 'in4', 'in5'):
    os.makedirs(os.path.join(HERE, name), exist_ok=True)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            globals()[name]()
        except Exception:
            traceback.print_exc(file=buf)
    open(os.path.join(HERE, name, 'out.txt'), 'w', encoding='utf-8').write(buf.getvalue())
    print(f'######## {name}\n' + buf.getvalue()[:4000])
