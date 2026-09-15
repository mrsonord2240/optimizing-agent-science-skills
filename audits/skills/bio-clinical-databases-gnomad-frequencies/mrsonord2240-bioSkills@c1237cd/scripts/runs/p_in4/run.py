# Input 4 (Variant B): "Batch-annotate BRCA2 variants with grpmax FAF95, and check that founder-enriched groups
# (ASJ, FIN, AMI, remaining) never become the grpmax the way the Skill says." Live gnomAD GraphQL + the shipped
# example's myvariant batch helper.
import sys, time, collections
sys.path.insert(0, '..')
import requests
from p_skill_code import GNOMAD_API

q = '''query { gene(gene_symbol: "BRCA2", reference_genome: GRCh38) { variants(dataset: gnomad_r4) {
  variant_id exome { ac an af faf95 { popmax popmax_population } populations { id ac an } } } } }'''
for attempt in range(4):
    resp = requests.post(GNOMAD_API, json={'query': q}, timeout=120)
    try:
        vs = resp.json()['data']['gene']['variants']
        break
    except Exception:
        print('attempt', attempt, 'status', resp.status_code, resp.text[:160].replace('\n', ' '))
        time.sleep(20)
ex = [v for v in vs if v.get('exome')]
print('BRCA2 v4 exome variants:', len(ex))
pm = collections.Counter((v['exome']['faf95'] or {}).get('popmax_population') for v in ex)
print('faf95.popmax_population counts:', dict(pm))
# variants where a bottleneck group has the highest raw AF (AC>=5) - what does faf95 report?
bott = {'asj', 'fin', 'ami', 'remaining'}
hits = []
for v in ex:
    pops = [p for p in v['exome']['populations'] if '_' not in p['id'] and p['an'] and p['id'] not in ('XX', 'XY')]
    if not pops:
        continue
    top = max(pops, key=lambda p: p['ac'] / p['an'])
    if top['id'] in bott and top['ac'] >= 5:
        hits.append((v['variant_id'], top['id'], round(top['ac'] / top['an'], 5), v['exome']['faf95']))
print('variants whose max raw-AF group is a bottleneck group (AC>=5):', len(hits))
for h in hits[:6]:
    print('  ', h)
print('faf95 is not populated in the gene-level variant list; querying the top bottleneck-max variants one by one:')
from p_skill_code import query_variant, grpmax_faf95
for vid, grp, af, _ in sorted(hits, key=lambda h: -h[2])[:8]:
    c, p, r, a = vid.split('-')
    pl = query_variant(c, int(p), r, a, build='GRCh38'); time.sleep(0.6)
    e = (pl or {}).get('exome') or {}
    pops = {q['id']: round(q['ac'] / q['an'], 5) for q in e.get('populations', []) if '_' not in q['id'] and q['an'] and q['id'] not in ('XX', 'XY') and q['ac']}
    print(f'  {vid} max raw group={grp} AF={af}  faf95={e.get("faf95")}  groups with AC>0: {pops}')
print('\n== shipped example annotate_variant_list() via myvariant (3 BRCA2 variants as HGVS-g, hg19 build of myvariant ids) ==')
import importlib.util
spec = importlib.util.spec_from_file_location('ex', 'gnomad_query.fork_copy.py'); ex_mod = importlib.util.module_from_spec(spec)
src = open('gnomad_query.fork_copy.py').read().split("if __name__ == '__main__':")[0]
exec(compile(src, 'gnomad_query.fork_copy.py', 'exec'), ex_mod.__dict__)
ids = ['chr13:g.32339151A>G', 'chr13:g.32340300A>G', 'rs80359550']
df = ex_mod.annotate_variant_list(ids)
print(df.to_string(index=False))
import myvariant
mv = myvariant.MyVariantInfo()
r = mv.getvariant('rs80359550', fields='gnomad_exome')
print('\nraw myvariant gnomad_exome keys for rs80359550:', (sorted(r[0]['gnomad_exome'].keys()) if isinstance(r, list) and r and 'gnomad_exome' in r[0] else (sorted(r.get('gnomad_exome', {}).keys()) if isinstance(r, dict) else r)))
