# Python code blocks copied verbatim from clinical-databases/dbsnp-queries/SKILL.md at fork commit
# mrsonord2240/bioSkills@c1237cdbc9bb199947696f3909de26a55d259116. Re-audit 2026-09-15.
import requests

VARSVC = 'https://api.ncbi.nlm.nih.gov/variation/v0'

def refsnp(rsid):
    '''Fetch full Build 156 RefSNP JSON. rsid can be 'rs121913529' or 121913529.'''
    rs_int = str(rsid).lstrip('rs')
    r = requests.get(f'{VARSVC}/refsnp/{rs_int}', timeout=30)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()

def summarize_refsnp(payload):
    '''Extract minimal fields. Handles multi-allelic cluster correctly.

    The placement JSON nests assembly metadata; the precise path varies by
    Build / API version. Common variants seen in the wild:
        placement['seq_id_traits_by_assembly'][0]['assembly_name']
        placement['placement_annot']['seq_id_traits_by_assembly'][0]['assembly_name']
    Inspect the actual JSON returned for the current dbSNP Build before
    relying on either path in production.
    '''
    if payload is None or payload.get('is_withdrawn'):
        return None
    primary = payload.get('primary_snapshot_data', {})
    placements = primary.get('placements_with_allele', [])
    def assembly_name(p):
        traits = (p.get('placement_annot') or p).get('seq_id_traits_by_assembly') or []
        return traits[0].get('assembly_name') if traits else ''
    grch38 = next((p for p in placements if 'GRCh38' in (assembly_name(p) or '')), None)
    if grch38 is None:
        return None
    alleles = []
    for allele in grch38.get('alleles', []):
        spdi = allele.get('allele', {}).get('spdi', {})
        alleles.append({
            'ref': spdi.get('deleted_sequence'),
            'alt': spdi.get('inserted_sequence'),
            'seq_id': spdi.get('seq_id'),
            'pos_0based': spdi.get('position')
        })
    return {
        'rsid': payload.get('refsnp_id'),
        'gene': primary.get('allele_annotations', [{}])[0].get('assembly_annotation', [{}])[0].get('genes', [{}])[0].get('locus'),
        'placements_grch38': alleles,
        'is_multiallelic': len(alleles) > 2,
        # rsIDs merged INTO this current record (rs429358 absorbed rs630496, rs61228756)
        'merged_from': [m.get('merged_rsid') for m in payload.get('dbsnp1_merges', [])]
    }


def resolve_merge_chain(rsid, max_hops=10):
    '''Follow multi-hop merge chain. Cycle-safe with max_hops cap. rs630496 -> rs429358.'''
    chain = []
    current = str(rsid).lstrip('rs')
    for _ in range(max_hops):
        if current in chain:
            return {'error': 'merge cycle detected', 'chain': chain}
        chain.append(current)
        payload = refsnp(current)
        if payload is None:
            return {'error': 'not found', 'final_rsid': current, 'chain': chain}
        if payload.get('is_withdrawn'):
            return {'status': 'withdrawn', 'final_rsid': current, 'chain': chain}
        primary = payload.get('primary_snapshot_data')
        if primary is not None:
            return {'status': 'resolved', 'final_rsid': payload.get('refsnp_id'), 'chain': chain}
        merged_into = (payload.get('merged_snapshot_data') or {}).get('merged_into') or []
        if not merged_into:
            return {'status': 'orphan', 'final_rsid': current, 'chain': chain}
        current = str(merged_into[0])
    return {'error': 'hop limit', 'chain': chain}


def hgvs_to_spdi_canonical(hgvs):
    '''Resolve HGVS to canonical SPDI via the Variant Overprecision Correction Algorithm.'''
    r = requests.get(f'{VARSVC}/hgvs/{hgvs}/contextuals', timeout=30)
    if not r.ok:
        return None
    contextuals = r.json().get('data', {}).get('spdis', [])
    return contextuals[0] if contextuals else None

def spdi_to_rsid(spdi_str):
    '''SPDI 'NC_000017.11:43044294:G:A' -> rsID if a cluster exists.'''
    r = requests.get(f'{VARSVC}/spdi/{spdi_str}/rsids', timeout=30)
    if not r.ok:
        return None
    rsids = r.json().get('data', {}).get('rsids', [])
    return rsids[0] if rsids else None

REFSEQ_GRCH38 = {
    '1': 'NC_000001.11', '2': 'NC_000002.12', '3': 'NC_000003.12', '4': 'NC_000004.12',
    '5': 'NC_000005.10', '6': 'NC_000006.12', '7': 'NC_000007.14', '8': 'NC_000008.11',
    '9': 'NC_000009.12', '10': 'NC_000010.11', '11': 'NC_000011.10', '12': 'NC_000012.12',
    '13': 'NC_000013.11', '14': 'NC_000014.9', '15': 'NC_000015.10', '16': 'NC_000016.10',
    '17': 'NC_000017.11', '18': 'NC_000018.10', '19': 'NC_000019.10', '20': 'NC_000020.11',
    '21': 'NC_000021.9', '22': 'NC_000022.11', 'X': 'NC_000023.11', 'Y': 'NC_000024.10'
}

def vcf_to_canonical_spdi(chrom, pos, ref, alt):
    '''VCF (1-based, GRCh38) -> canonical SPDI string (0-based).

    The endpoint returns the SPDI fields directly under data (seq_id, position, deleted_sequence,
    inserted_sequence) and adds data.warnings when REF does not match the reference.
    '''
    refseq = REFSEQ_GRCH38.get(str(chrom).removeprefix('chr'))
    if refseq is None:
        return None
    raw_spdi = f'{refseq}:{pos - 1}:{ref}:{alt}'
    r = requests.get(f'{VARSVC}/spdi/{raw_spdi}/canonical_representative', timeout=30)
    if not r.ok:
        return None
    d = r.json().get('data', {})
    if d.get('warnings'):
        raise ValueError(f"{chrom}:{pos} {ref}>{alt}: {[w.get('message') for w in d['warnings']]}")
    return f"{d['seq_id']}:{d['position']}:{d['deleted_sequence']}:{d['inserted_sequence']}"


ALFA_BIOPROJECT = 'PRJNA507278'
ALFA_BIOSAMPLES = {
    'SAMN10492705': 'Total', 'SAMN10492695': 'European', 'SAMN10492703': 'African',
    'SAMN10492696': 'African Others', 'SAMN10492698': 'African American', 'SAMN10492704': 'Asian',
    'SAMN10492697': 'East Asian', 'SAMN10492701': 'Other Asian', 'SAMN10492702': 'South Asian',
    'SAMN10492699': 'Latin American 1', 'SAMN10492700': 'Latin American 2', 'SAMN11605645': 'Other'
}

def alfa_frequency(rsid, population='Total'):
    '''ALFA allele counts and frequencies for one population from /refsnp/{id}/frequency.

    Returns {placement: {'ref', 'total_alleles', 'af': {allele: freq}}}; placement keys look like
    '1@169549810' for rs6025.
    '''
    rs_int = str(rsid).lstrip('rs')
    r = requests.get(f'{VARSVC}/refsnp/{rs_int}/frequency', timeout=30)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    out = {}
    for placement, record in r.json().get('results', {}).items():
        counts = record.get('counts', {}).get(ALFA_BIOPROJECT, {}).get('allele_counts', {})
        for biosample, alleles in counts.items():
            if ALFA_BIOSAMPLES.get(biosample) != population:
                continue
            total = sum(alleles.values())
            out[placement] = {'ref': record.get('ref'), 'total_alleles': total,
                              'af': {a: n / total for a, n in alleles.items()} if total else None}
    return out or None
