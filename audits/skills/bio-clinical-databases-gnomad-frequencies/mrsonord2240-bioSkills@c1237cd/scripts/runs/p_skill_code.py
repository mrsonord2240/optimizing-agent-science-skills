# Python code blocks copied verbatim from clinical-databases/gnomad-frequencies/SKILL.md at fork commit
# mrsonord2240/bioSkills@c1237cdbc9bb199947696f3909de26a55d259116 (Hail block excluded). Re-audit 2026-09-15.
import requests

GNOMAD_API = 'https://gnomad.broadinstitute.org/api'
DATASET_BUILD = {'gnomad_r4': 'GRCh38', 'gnomad_r3': 'GRCh38', 'gnomad_r2_1': 'GRCh37'}

def query_variant(chrom, pos, ref, alt, build, dataset='gnomad_r4'):
    '''Query gnomAD GraphQL for variant frequency + grpmax FAF95.

    build: 'GRCh38' or 'GRCh37', the build of the coordinates; checked against the dataset
    (gnomad_r4 / gnomad_r3 = GRCh38, gnomad_r2_1 = GRCh37). GRCh37 ids sent to gnomad_r4 return
    "Variant not found", the same answer as a truly absent variant.
    Returns the variant payload, or None when the variant is not in this dataset; raises on any
    other GraphQL error.
    '''
    if DATASET_BUILD[dataset] != build:
        raise ValueError(f'{dataset} is {DATASET_BUILD[dataset]} but the coordinates are {build}')
    query = '''
    query VariantById($variantId: String!, $dataset: DatasetId!) {
      variant(variantId: $variantId, dataset: $dataset) {
        variant_id
        rsids
        exome {
          ac
          an
          af
          homozygote_count
          filters
          populations { id ac an }
          faf95 { popmax popmax_population }
        }
        genome {
          ac
          an
          af
          homozygote_count
          filters
          populations { id ac an }
          faf95 { popmax popmax_population }
        }
      }
    }
    '''
    variant_id = f'{chrom}-{pos}-{ref}-{alt}'
    r = requests.post(GNOMAD_API,
                      json={'query': query, 'variables': {'variantId': variant_id, 'dataset': dataset}},
                      timeout=30)
    r.raise_for_status()
    body = r.json()
    errors = [e.get('message') for e in body.get('errors') or []]
    if errors and errors != ['Variant not found']:
        raise RuntimeError(f'gnomAD GraphQL error for {variant_id} ({dataset}): {errors}')
    return (body.get('data') or {}).get('variant')


def grpmax_faf95(payload):
    '''Extract the grpmax FAF95; the ACMG-grade frequency. Excludes bottleneck groups.

    faf95 is None both for absent variants (source='absent') and for present variants whose FAF95
    is undefined because too few alleles were seen (source='present_faf95_undefined', e.g. AC=1).
    '''
    if payload is None:
        return {'faf95': None, 'grpmax_ancestry': None, 'source': 'absent'}
    for source in ('exome', 'genome'):
        faf = (payload.get(source) or {}).get('faf95') or {}
        if faf.get('popmax') is not None:
            return {'faf95': faf['popmax'], 'grpmax_ancestry': faf.get('popmax_population'), 'source': source}
    return {'faf95': None, 'grpmax_ancestry': None, 'source': 'present_faf95_undefined'}


def max_credible_af(prevalence, max_allelic_contribution=1.0, max_genetic_contribution=1.0,
                    penetrance=1.0):
    '''Whiffin 2017 max-credible-AF formula.

    Args:
        prevalence: disease prevalence (e.g., 1/10000 = 1e-4)
        max_allelic_contribution: max contribution of single allele to disease in any case
        max_genetic_contribution: max contribution of this gene to disease in any case
        penetrance: probability that variant carriers develop disease

    Returns: max-credible per-allele frequency under dominant inheritance (use /2 for AR)
    '''
    return (prevalence * max_genetic_contribution * max_allelic_contribution) / (penetrance * 2)


def apply_bs1_ba1(grpmax_faf95_val, max_credible, ba1_threshold=0.05):
    '''Apply ClinGen SVI BS1/BA1 criteria.

    BA1 default 5% per ClinGen SVI; VCEP-specific overrides exist (Hearing Loss = 0.5%).
    BS1 = max-credible-AF specific to gene+disease.
    grpmax_faf95_val None = absent, or present with FAF95 undefined (see grpmax_faf95()['source']).
    These are research annotation tags for a variant, not a classification.
    '''
    if grpmax_faf95_val is None:
        return 'PM2_Supporting'  # Absent or ultra-rare
    if grpmax_faf95_val > ba1_threshold:
        return 'BA1'
    if grpmax_faf95_val > max_credible:
        return 'BS1'
    return None  # No criterion triggered; variant is consistent with rare-disease causation


def query_gene_constraint(gene_symbol, dataset='gnomad_r4'):
    '''Pull gene constraint metrics (chrX genes included: DMD LOEUF 0.235 on 2026-09-15).'''
    query = '''
    query GeneById($symbol: String!) {
      gene(gene_symbol: $symbol, reference_genome: GRCh38) {
        gene_id
        symbol
        chrom
        gnomad_constraint {
          oe_lof
          oe_lof_lower
          oe_lof_upper
          oe_mis
          oe_mis_upper
          pli
          mis_z
        }
      }
    }
    '''
    r = requests.post(GNOMAD_API,
                      json={'query': query, 'variables': {'symbol': gene_symbol}},
                      timeout=30)
    r.raise_for_status()
    gene = r.json().get('data', {}).get('gene')
    if gene is None:
        return None
    if gene.get('gnomad_constraint') is None:
        gene['constraint_note'] = ('no constraint returned for this gene; try the v2.1.1 values '
                                   'with reference_genome: GRCh37')
    return gene
