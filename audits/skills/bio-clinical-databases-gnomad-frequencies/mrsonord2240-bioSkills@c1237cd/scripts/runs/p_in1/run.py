# Input 1 (Canonical): "How rare is HBB c.20A>T (rs334, GRCh38 11-5227002-T-A) in gnomAD v4? Give exome and
# genome AF, grpmax FAF95 and the grpmax ancestry." Live gnomAD GraphQL, 2026-09-15; SKILL.md code verbatim.
import json, sys
sys.path.insert(0, '..')
import requests
from p_skill_code import query_variant, grpmax_faf95, GNOMAD_API

p = query_variant('11', 5227002, 'T', 'A', build='GRCh38')
print('== SKILL.md query_variant(11, 5227002, T, A) ==')
if p is None:
    print('None')
else:
    for k in ('exome', 'genome'):
        d = p.get(k) or {}
        print(k, {x: d.get(x) for x in ('ac', 'an', 'af', 'homozygote_count', 'filters', 'faf95')})
        pops = {q['id']: round(q['ac'] / q['an'], 5) for q in d.get('populations', []) if q['an'] and '_' not in q['id'] and q['id'] not in ('XX', 'XY')}
        print('  per-group AF:', pops)
print('== SKILL.md grpmax_faf95(payload) ==', grpmax_faf95(p))
# raw response check: does the query return GraphQL errors next to data?
q = {'query': '{ variant(variantId: "11-5227002-T-A", dataset: gnomad_r4) { exome { faf95 { popmax popmax_population } fafmax { faf95_max faf95_max_gen_anc } } } }'}
r = requests.post(GNOMAD_API, json=q, timeout=30).json()
print('== schema probe: faf95 vs fafmax field ==')
print(json.dumps(r)[:600])
