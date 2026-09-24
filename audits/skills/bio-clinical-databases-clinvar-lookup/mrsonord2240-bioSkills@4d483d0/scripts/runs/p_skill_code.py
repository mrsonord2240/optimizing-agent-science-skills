# Python code blocks copied verbatim from clinical-databases/clinvar-lookup/SKILL.md at the fork commit
# mrsonord2240/bioSkills@c1237cdbc9bb199947696f3909de26a55d259116 (re-audit 2026-09-15).
# The cyvcf2 `lookup` block is in p_in2/lookup_test.py (cyvcf2 has no Windows wheel).
import time
import requests

EUTILS = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils'

def clinvar_summary(variation_id):
    '''Retrieve VCV-level summary by ClinVar VariationID (do not confuse with CA ID).'''
    r = requests.get(f'{EUTILS}/esummary.fcgi',
                     params={'db': 'clinvar', 'id': variation_id, 'retmode': 'json'},
                     timeout=30)
    r.raise_for_status()
    record = r.json()['result'][str(variation_id)]
    return {
        'vcv': record.get('accession'),
        'name': record.get('title'),
        'germline_class': record.get('germline_classification', {}).get('description'),
        'germline_review_status': record.get('germline_classification', {}).get('review_status'),
        'somatic_clinical': record.get('clinical_impact_classification', {}).get('description'),
        'oncogenicity': record.get('oncogenicity_classification', {}).get('description'),
        'last_evaluated': record.get('germline_classification', {}).get('last_evaluated')
    }

def clinvar_search_gene(gene, pathogenic_only=False, page_size=500, max_ids=None):
    '''Return (count, VariationIDs).'''
    term = f'{gene}[gene]'
    if pathogenic_only:
        term += ' AND (clinsig_pathogenic[Properties] OR clinsig_likely_pathogenic[Properties])'
    ids, count, start = [], None, 0
    while count is None or start < count:
        r = requests.get(f'{EUTILS}/esearch.fcgi',
                         params={'db': 'clinvar', 'term': term, 'retmax': page_size,
                                 'retstart': start, 'retmode': 'json'},
                         timeout=30)
        r.raise_for_status()
        result = r.json()['esearchresult']
        count = int(result['count'])
        ids.extend(result['idlist'])
        start += page_size
        if max_ids is not None and len(ids) >= max_ids:
            break
        time.sleep(0.34)  # ~3 requests/s without an NCBI API key
    return count, ids

def car_id(hgvs_g):
    '''Resolve HGVS-g to canonical ClinGen Allele Registry CA ID with the public GET.'''
    r = requests.get('https://reg.clinicalgenome.org/allele', params={'hgvs': hgvs_g}, timeout=30)
    if r.status_code == 400:
        err = r.json()
        raise ValueError(f"{err.get('errorType')}: {err.get('message')} (actual allele {err.get('actualAllele')})")
    r.raise_for_status()
    at_id = r.json().get('@id', '')
    return at_id.rsplit('/', 1)[-1] if at_id else None
