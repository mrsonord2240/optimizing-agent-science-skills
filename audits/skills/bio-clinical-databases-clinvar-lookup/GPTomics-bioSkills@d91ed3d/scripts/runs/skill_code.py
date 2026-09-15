# Code blocks copied verbatim from clinical-databases/clinvar-lookup/SKILL.md (GPTomics/bioSkills@d91ed3d).
# Only the cyvcf2 `lookup` block is kept separate (skill_code_vcf.py) because cyvcf2 has no Windows wheel.
import requests

EUTILS = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils'

def clinvar_summary(variation_id):
    '''Retrieve VCV-level summary by ClinVar VariationID (do not confuse with CA ID).

    The germline / somatic / oncogenicity classification nesting shown below
    follows the ClinVar 2024 eSummary v2 schema described in the data-access
    documentation. Field names have changed between API versions -- inspect
    the actual JSON returned by eSummary for the live ClinVar version before
    pinning these key paths in production.
    '''
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

def clinvar_search_gene(gene, pathogenic_only=False, retmax=500):
    term = f'{gene}[gene]'
    if pathogenic_only:
        term += ' AND (clinsig_pathogenic[Properties] OR clinsig_likely_pathogenic[Properties])'
    r = requests.get(f'{EUTILS}/esearch.fcgi',
                     params={'db': 'clinvar', 'term': term, 'retmax': retmax, 'retmode': 'json'},
                     timeout=30)
    return r.json()['esearchresult']['idlist']


def car_id(hgvs_g):
    '''Resolve HGVS-g to canonical ClinGen Allele Registry CA ID.'''
    r = requests.put(f'https://reg.clinicalgenome.org/allele',
                     headers={'Content-Type': 'text/plain'},
                     data=hgvs_g, timeout=30)
    return r.json().get('@id', '').split('/')[-1] if r.ok else None
