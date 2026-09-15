# Code blocks copied verbatim from clinical-databases/dbsnp-queries/SKILL.md (GPTomics/bioSkills@d91ed3d).
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
    '''Extract minimal fields. Handles multi-allelic cluster correctly.'''
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
        'merge_history': payload.get('merged_snapshot_data', [])
    }

def resolve_merge_chain(rsid, max_hops=10):
    '''Follow multi-hop merge chain. Cycle-safe with max_hops cap.'''
    seen = set()
    current = str(rsid).lstrip('rs')
    for _ in range(max_hops):
        if current in seen:
            return {'error': 'merge cycle detected', 'chain': list(seen)}
        seen.add(current)
        payload = refsnp(current)
        if payload is None:
            return {'error': 'not found', 'final_rsid': current, 'chain': list(seen)}
        if payload.get('is_withdrawn'):
            return {'status': 'withdrawn', 'final_rsid': current, 'chain': list(seen)}
        primary = payload.get('primary_snapshot_data')
        if primary is not None:
            return {'status': 'resolved', 'final_rsid': payload.get('refsnp_id'), 'chain': list(seen)}
        merged = payload.get('merged_snapshot_data', [])
        if not merged:
            return {'status': 'orphan', 'final_rsid': current, 'chain': list(seen)}
        current = str(merged[0].get('merged_into', ''))
    return {'error': 'hop limit', 'chain': list(seen)}

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

def vcf_to_canonical_spdi(chrom, pos, ref, alt, assembly='GRCh38'):
    '''VCF (1-based) -> SPDI (0-based, right-aligned).'''
    refseq_map = {('1', 'GRCh38'): 'NC_000001.11', ('17', 'GRCh38'): 'NC_000017.11'}
    refseq = refseq_map.get((str(chrom).lstrip('chr'), assembly))
    if refseq is None:
        return None
    raw_spdi = f'{refseq}:{pos - 1}:{ref}:{alt}'
    r = requests.get(f'{VARSVC}/spdi/{raw_spdi}/canonical_representative', timeout=30)
    return r.json().get('data', {}).get('spdi') if r.ok else None

def alfa_frequency(rsid, ancestry='Total'):
    '''Pull ALFA per-population AF via Variation Services.'''
    payload = refsnp(rsid)
    if payload is None:
        return None
    freq_records = payload.get('primary_snapshot_data', {}).get('allele_annotations', [{}])[0].get('frequency', [])
    alfa_records = [f for f in freq_records if 'ALFA' in f.get('study_name', '')]
    for record in alfa_records:
        if record.get('common_name') == ancestry:
            return {
                'allele': record.get('observation', {}).get('inserted_sequence'),
                'count': record.get('allele_count'),
                'total': record.get('total_count'),
                'freq': record.get('allele_count') / record.get('total_count') if record.get('total_count') else None
            }
    return None
