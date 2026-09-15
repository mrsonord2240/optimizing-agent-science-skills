# Input 2 (Variant A): "For a research curation table of candidate MYH7 variants, compute the Whiffin maximum
# credible AF for autosomal-dominant HCM (prevalence 1/500, max genetic contribution 0.3, max allelic
# contribution 0.1, penetrance 0.8) and tag each variant BA1/BS1/PM2_Supporting as research annotation."
# Live gnomAD GraphQL; SKILL.md code verbatim; also the shipped example's __main__ path.
import sys, time, subprocess
sys.path.insert(0, '..')
import requests
from p_skill_code import query_variant, grpmax_faf95, max_credible_af, apply_bs1_ba1, GNOMAD_API

mc = max_credible_af(prevalence=1/500, max_genetic_contribution=0.30, max_allelic_contribution=0.10, penetrance=0.80)
print(f'max credible AF (dominant) = {mc:.6f}  (hand check: 0.002*0.3*0.1/(0.8*2) = {0.002*0.3*0.1/1.6:.6f})')

# pull MYH7 exome variants to find (a) a common one, (b) a present-but-FAF95=0 low-AC one, (c) a mid-frequency one
q = '''query { gene(gene_symbol: "MYH7", reference_genome: GRCh38) { variants(dataset: gnomad_r4) {
  variant_id consequence exome { ac an af faf95 { popmax popmax_population } } } } }'''
vs = requests.post(GNOMAD_API, json={'query': q}, timeout=60).json()['data']['gene']['variants']
ex = [v for v in vs if v.get('exome')]
print('MYH7 v4 exome variants:', len(ex))
common = max(ex, key=lambda v: v['exome']['af'] or 0)
singleton = next(v for v in ex if v['exome']['ac'] == 1 and v['consequence'] == 'missense_variant')
mid = next(v for v in sorted(ex, key=lambda v: v['exome']['af'] or 0) if 2e-4 < (v['exome']['af'] or 0) < 2e-3)
print('faf95 populated in the gene variant list for', sum(1 for v in ex if (v['exome'].get('faf95') or {}).get('popmax') is not None), 'of', len(ex))
for label, v in [('common', common), ('present AC=1 missense', singleton), ('AF 2e-4..2e-3', mid)]:
    chrom, pos, ref, alt = v['variant_id'].split('-')
    time.sleep(0.5)
    payload = query_variant(chrom, int(pos), ref, alt, build='GRCh38')
    g = grpmax_faf95(payload)
    code = apply_bs1_ba1(g['faf95'], mc)
    print(f"{label:24s} {v['variant_id']:22s} AC={payload['exome']['ac']:>6} AF={payload['exome']['af']:.2e} -> grpmax_faf95={g} -> apply_bs1_ba1 = {code}")

print('\n== shipped examples/gnomad_query.py __main__ (BRCA1 17-43094464-G-A demo) ==')
subprocess.run([sys.executable, 'gnomad_query.fork_copy.py'])
