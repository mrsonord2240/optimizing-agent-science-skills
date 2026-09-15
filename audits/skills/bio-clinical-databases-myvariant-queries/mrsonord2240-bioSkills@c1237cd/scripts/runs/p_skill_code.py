# SKILL.md Python blocks 2-3 verbatim at fork commit mrsonord2240/bioSkills@c1237cdbc9bb199947696f3909de26a55d259116 (re-audit 2026-09-15)
import myvariant
import pandas as pd
import requests

mv = myvariant.MyVariantInfo()

CLINICAL_FIELDS = [
    'clinvar.rcv.clinical_significance',   # ClinVar significance lives under clinvar.rcv[]
    'clinvar.rcv.review_status',
    'clinvar.variant_id',
    'gnomad_exome.af.af',                  # gnomAD 2.1.1 (GRCh37); myvariant has no FAF95
    'gnomad_exome.an.an',
    'gnomad_genome.af.af',
    'dbsnp.rsid',
    'dbnsfp.alphamissense.score',
    'dbnsfp.alphamissense.pred',
    'dbnsfp.revel.score',
    'cadd.phred',                          # top-level CADD source, not dbnsfp.cadd
    'cosmic.cosmic_id',                    # no SpliceAI field in myvariant (only cadd.dst2splice)
    'civic.openCravatUrl'
]

def source_versions():
    '''Instance-wide per-source versions; records carry no _meta.'''
    meta = requests.get('https://myvariant.info/v1/metadata', timeout=30).json()
    return {name: src.get('version') for name, src in meta.get('src', {}).items()}

def _as_list(value):
    return value if isinstance(value, list) else ([value] if value is not None else [])

def annotate_variant_list(hgvs_list):
    '''Batch-annotate variants with ClinVar / gnomAD 2.1.1 / dbNSFP / CADD / COSMIC fields.

    getvariants() chunks the list itself. A multi-allelic rsID returns one record per allele.
    '''
    rows = []
    for r in mv.getvariants(hgvs_list, fields=CLINICAL_FIELDS):
        if r.get('notfound'):
            rows.append({'variant': r.get('query'), 'notfound': True})
            continue
        rcv = _as_list((r.get('clinvar') or {}).get('rcv'))
        gnomad_e = r.get('gnomad_exome') or {}
        gnomad_g = r.get('gnomad_genome') or {}
        dbnsfp = r.get('dbnsfp') or {}
        rows.append({
            'variant': r.get('query'),
            'myvariant_id': r.get('_id'),
            'clinvar_sig': sorted({x.get('clinical_significance') for x in rcv if x.get('clinical_significance')}),
            'clinvar_review': sorted({x.get('review_status') for x in rcv if x.get('review_status')}),
            'gnomad_v2_af': (gnomad_e.get('af') or {}).get('af') or (gnomad_g.get('af') or {}).get('af'),
            'rsid': (r.get('dbsnp') or {}).get('rsid'),
            'alphamissense': (dbnsfp.get('alphamissense') or {}).get('score'),
            'revel': (dbnsfp.get('revel') or {}).get('score'),
            'cadd_phred': (r.get('cadd') or {}).get('phred'),
            'cosmic_id': (r.get('cosmic') or {}).get('cosmic_id')
        })
    return pd.DataFrame(rows), source_versions()


def find_pathogenic_in_gene(gene_symbol, max_results=500):
    '''Find ClinVar P/LP variants in a gene. Returns (total, hits); hits holds at most max_results
    records (BRCA1: total 3,933 on 2026-09-15), so compare len(hits) with total.'''
    query = f'clinvar.gene.symbol:{gene_symbol} AND '\
            'clinvar.rcv.clinical_significance:(Pathogenic OR "Likely pathogenic")'
    res = mv.query(query, size=max_results, fields=['_id', 'clinvar.rcv.clinical_significance',
                                                      'clinvar.rcv.review_status'])
    return res.get('total'), res.get('hits', [])


def find_high_cadd_in_region(chrom, start, end, min_cadd=25):
    '''Find variants in region with CADD phred above threshold.

    start/end are GRCh37 (hg19) positions. hg38.start combined with cadd.phred returned 0 hits
    for the BRAF V600E window on 2026-09-15 (145 with hg19.start), so query CADD by hg19 coordinates.
    '''
    query = f'chrom:{chrom} AND hg19.start:[{start} TO {end}] AND '\
            f'cadd.phred:>{min_cadd}'
    return mv.query(query, size=500, fields=['_id', 'cadd.phred', 'clinvar.rcv.clinical_significance'])


def find_alphamissense_pathogenic(gene, min_score=0.564):
    '''Find AlphaMissense pathogenic missense in a gene.

    Note: Cheng 2023 dev cutoff is 0.564 BUT this is NOT the Pejaver-style calibrated
    PP3 threshold. ClinGen has not endorsed AlphaMissense thresholds as of May 2026;
    use AlphaMissense as supporting evidence only.
    '''
    query = f'dbnsfp.genename:{gene} AND dbnsfp.alphamissense.score:>{min_score}'
    return mv.query(query, size=500, fields=['_id', 'dbnsfp.alphamissense', 'clinvar.rcv.clinical_significance'])
