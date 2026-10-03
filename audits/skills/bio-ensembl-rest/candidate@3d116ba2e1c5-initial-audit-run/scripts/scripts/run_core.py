"""Core workflow probe for bio-ensembl-rest (live Ensembl REST). Sequential, small queries."""
import os
import sys
import time
from collections import Counter

sys.dont_write_bytecode = True
CAND = r'F:\OpenScience\wt\dbaccess-ensembl-rest\skills\bio-ensembl-rest'
sys.path.insert(0, os.path.join(CAND, 'scripts'))
import requests
from ensembl_client import (ARCHIVE_E110, BASE, GRCH37, HEADERS, SLEEP, batch_symbols, gene_info,
                            genes_in_region, ld_pairwise, orthologs_by_symbol, paralogs_by_symbol,
                            sequence_for_id, symbol_to_id, vep_hgvs, vep_id, vep_region)


def step(name, fn):
    print(f'--- {name}')
    try:
        print(fn())
    except Exception as e:  # noqa
        print(f'EXC {type(e).__name__}: {e}')
    time.sleep(SLEEP)


def s1():
    g = symbol_to_id('human', 'BRCA1')
    return {k: g[k] for k in ('id', 'display_name', 'biotype', 'seq_region_name', 'start', 'end', 'strand', 'assembly_name', 'version')}


def s2():
    d = gene_info('ENSG00000012048')
    tx = d['Transcript']
    return {'n_tx': len(tx), 'canonical': [t['id'] for t in tx if t.get('is_canonical')],
            'first_exons': [(t['id'], len(t['Exon'])) for t in tx[:3]]}


def s3():
    p = sequence_for_id('ENSP00000269305', 'protein')
    return {'len': len(p['seq']), 'head': p['seq'][:10], 'id': p['id']}


def s3b():
    r = requests.get(f'{BASE}/sequence/id/ENSG00000139618', params={'type': 'protein', 'multiple_sequences': 1}, headers=HEADERS)
    j = r.json()
    return {'status': r.status_code, 'n': len(j), 'first': (j[0]['id'], len(j[0]['seq'])) if j else None}


def s3c():
    r = requests.get(f'{BASE}/sequence/id/ENSG00000139618', params={'type': 'protein'}, headers=HEADERS)
    return r.status_code, r.text[:200]


def s4():
    gs = genes_in_region('human', '17:43000000-43200000')
    return {'n': len(gs), 'syms': sorted(g.get('external_name', '?') for g in gs),
            'brca1': [(g['start'], g['end']) for g in gs if g.get('external_name') == 'BRCA1']}


def s5():
    r = vep_region('human', '17:43044295-43044295:1', 'A')
    tc = r[0]['transcript_consequences']
    return {'assembly': r[0].get('assembly_name'), 'allele_string': r[0].get('allele_string'),
            'most_severe': r[0].get('most_severe_consequence'), 'n_tc': len(tc),
            'genes': sorted({t.get('gene_symbol') for t in tc})}


def s5b():
    # usage-guide.md example: chr17:41276135 T>G on the default (GRCh38) host
    r = vep_region('human', '17:41276135-41276135:1', 'G')
    tc = r[0].get('transcript_consequences', [])
    return {'assembly': r[0].get('assembly_name'), 'allele_string': r[0].get('allele_string'),
            'most_severe': r[0].get('most_severe_consequence'),
            'genes': sorted({t.get('gene_symbol') for t in tc})}


def s5c():
    r = vep_region('human', '17:41276135-41276135:1', 'G', base=GRCH37)
    tc = r[0].get('transcript_consequences', [])
    return {'assembly': r[0].get('assembly_name'), 'allele_string': r[0].get('allele_string'),
            'most_severe': r[0].get('most_severe_consequence'),
            'genes': sorted({t.get('gene_symbol') for t in tc})}


def s6():
    r = vep_id('human', 'rs699')
    tc = [t for t in r[0]['transcript_consequences'] if t.get('gene_symbol') == 'AGT' and 'missense_variant' in t['consequence_terms']][:1]
    return {'start': r[0]['start'], 'allele_string': r[0]['allele_string'], 'most_severe': r[0]['most_severe_consequence'],
            'tc': [(t['transcript_id'], t.get('amino_acids'), t.get('sift_prediction'), t.get('polyphen_prediction')) for t in tc]}


def s6b():
    r = vep_id('human', 'rs55794205')
    return {'start': r[0]['start'], 'allele_string': r[0]['allele_string'], 'most_severe': r[0]['most_severe_consequence']}


def s7():
    r = vep_hgvs('human', 'ENST00000646891:c.1799T>A')
    tc = [t for t in r[0]['transcript_consequences'] if t.get('transcript_id') == 'ENST00000646891']
    return {'input': r[0]['input'], 'most_severe': r[0]['most_severe_consequence'],
            'tc': [(t['consequence_terms'], t.get('amino_acids'), t.get('sift_prediction'), t.get('polyphen_prediction')) for t in tc]}


def s7b():
    return vep_hgvs('human', 'ENST00000366667:c.803G>A')


def s7c():
    r = requests.get(f'{BASE}/vep/human/hgvs/ENST00000366667:c.803G>A', headers=HEADERS)
    return r.status_code, r.text[:300]


def s7d():
    l = requests.get(f'{BASE}/lookup/id/ENST00000366667', headers=HEADERS).json()
    return {'tx_symbol': l.get('display_name'), 'species': l.get('species')}


def s7e():
    r = requests.get(f'{BASE}/sequence/id/ENST00000366667', params={'type': 'cds'}, headers=HEADERS).json()
    return {'cds_len': len(r['seq']), 'base_c803': r['seq'][802], 'context': r['seq'][798:808]}


def s7f():
    return vep_hgvs('human', 'ENST00000366667:c.803C>T')[0]['most_severe_consequence']


def s8():
    o = orthologs_by_symbol('human', 'TP53', target='mouse')
    return [(h['type'], h['target']['id'], h['target']['species'], h.get('confidence'), h['target'].get('perc_id'), h['source'].get('perc_id')) for h in o]


def s8b():
    o = orthologs_by_symbol('human', 'BRCA1')
    return dict(Counter(h['type'] for h in o)), len(o)


def s8c():
    p = paralogs_by_symbol('human', 'BRCA1')
    return [(h['type'], h['target']['id'], h.get('taxonomy_level')) for h in p]


def s9():
    out = batch_symbols('human', ['BRCA1', 'MARCH1', 'NOTAGENE'])
    return {k: (v.get('id') or v.get('error')) for k, v in out.items()}


def s10():
    g = symbol_to_id('human', 'BRCA1', base=ARCHIVE_E110)
    return (g['id'], g['start'], g['end'], g['assembly_name'])


def s10b():
    g = symbol_to_id('human', 'BRCA1', base=GRCH37)
    return (g['id'], g['start'], g['end'], g['assembly_name'])


def s10c():
    r = requests.get('https://e116.rest.ensembl.org/info/data', headers=HEADERS, allow_redirects=False)
    return r.status_code, r.headers.get('Location')


def s10d():
    r = requests.get('https://rest.ensembl.org/info/data', headers=HEADERS)
    return r.json(), {k: v for k, v in r.headers.items() if 'ratelimit' in k.lower()}


for name, fn in [
    ('symbol_to_id BRCA1', s1), ('gene_info expand', s2),
    ('sequence_for_id ENSP protein (TP53)', s3),
    ('SKILL.md quickstart: sequence_for_id(ENSG00000139618, protein)', lambda: len(sequence_for_id('ENSG00000139618', 'protein')['seq'])),
    ('workaround multiple_sequences=1', s3b), ('raw 400 body', s3c),
    ('sequence_for_id ENST protein (BRCA2 canonical)', lambda: len(sequence_for_id('ENST00000380152', 'protein')['seq'])),
    ('genes_in_region', s4), ('vep_region BRCA1 example (GRCh38)', s5),
    ('usage-guide VEP example 17:41276135 G on default GRCh38 host', s5b),
    ('same on GRCh37 host', s5c),
    ('vep_id rs699', s6), ('vep_id rs55794205 (example)', s6b), ('vep_hgvs BRAF V600E', s7),
    ('vep_hgvs example string ENST00000366667:c.803G>A', s7b), ('raw body of example hgvs', s7c),
    ('what is ENST00000366667', s7d), ('ref base at c.803 of ENST00000366667', s7e), ('corrected hgvs c.803C>T', s7f),
    ('orthologs TP53 mouse', s8), ('orthologs BRCA1 all', s8b), ('paralogs BRCA1', s8c),
    ('ld_pairwise rs6792369/rs1042779 CEU', lambda: ld_pairwise('human', 'rs6792369', 'rs1042779')),
    ('batch_symbols with renamed + bad symbol', s9),
    ('archive e110 BRCA1', s10), ('GRCh37 BRCA1', s10b),
    ('e116 archive redirect (no follow)', s10c), ('live release + ratelimit headers', s10d),
]:
    step(name, fn)
