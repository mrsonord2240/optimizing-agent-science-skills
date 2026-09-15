# Code blocks copied verbatim from clinical-databases/gnomad-frequencies/SKILL.md (GPTomics/bioSkills@d91ed3d).
import requests

GNOMAD_API = 'https://gnomad.broadinstitute.org/api'

def query_variant(chrom, pos, ref, alt, dataset='gnomad_r4'):
    '''Query gnomAD GraphQL for variant frequency + grpmax FAF95.

    dataset options: gnomad_r4 (v4.1, default), gnomad_r3, gnomad_r2_1
    '''
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
    return r.json().get('data', {}).get('variant')


def grpmax_faf95(payload):
    '''Extract the grpmax FAF95; the ACMG-grade frequency. Excludes bottleneck groups.'''
    exome = payload.get('exome') if payload else None
    if exome and exome.get('faf95'):
        return {
            'faf95': exome['faf95'].get('popmax'),
            'grpmax_ancestry': exome['faf95'].get('popmax_population'),
            'source': 'exome'
        }
    genome = payload.get('genome') if payload else None
    if genome and genome.get('faf95'):
        return {
            'faf95': genome['faf95'].get('popmax'),
            'grpmax_ancestry': genome['faf95'].get('popmax_population'),
            'source': 'genome'
        }
    return {'faf95': 0.0, 'grpmax_ancestry': None, 'source': 'absent'}


def max_credible_af(prevalence, max_allelic_contribution=1.0, max_genetic_contribution=1.0,
                    penetrance=1.0):
    '''Whiffin 2017 max-credible-AF formula.'''
    return (prevalence * max_genetic_contribution * max_allelic_contribution) / (penetrance * 2)


def apply_bs1_ba1(grpmax_faf95_val, max_credible, ba1_threshold=0.05):
    '''Apply ClinGen SVI BS1/BA1 criteria.'''
    if grpmax_faf95_val is None:
        return 'PM2_Supporting'  # Absent or ultra-rare
    if grpmax_faf95_val > ba1_threshold:
        return 'BA1'
    if grpmax_faf95_val > max_credible:
        return 'BS1'
    return None  # No criterion triggered; variant is consistent with rare-disease causation


def query_gene_constraint(gene_symbol, dataset='gnomad_r4'):
    '''Pull gene constraint metrics. Note: v4 has no chrX/Y constraint; use v2 fallback.'''
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
    if gene.get('chrom') in ('X', 'Y'):
        gene['constraint_note'] = ('v4 constraint NOT released for chrX/Y; query v2.1.1 '
                                   'via gnomad_r2_1 dataset on the v2 endpoint')
    return gene
