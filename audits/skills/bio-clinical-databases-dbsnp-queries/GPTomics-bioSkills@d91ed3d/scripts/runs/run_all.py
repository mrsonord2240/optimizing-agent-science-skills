# dbSNP audit driver: one function per input, output written to in<N>/out.txt. Live NCBI Variation Services
# (no API key, <=3 req/s), 2026-09-15. SKILL.md code verbatim in skill_code.py; shipped example via git copy.
import contextlib, importlib.util, io, json, os, sys, time, traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import requests
import skill_code as sk

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('ex', os.path.join(HERE, 'dbsnp_lookup.upstream_copy.py'))
ex = importlib.util.module_from_spec(spec); spec.loader.exec_module(ex)
nap = lambda: time.sleep(0.4)


def in1():
    """Canonical: 'Resolve rs429358 (APOE): GRCh38 coordinates, alleles, gene, merge history.'"""
    p = sk.refsnp('rs429358'); nap()
    s = sk.summarize_refsnp(p)
    print('SKILL.md summarize_refsnp(rs429358):', json.dumps(s, indent=1)[:1500])
    pl = p['primary_snapshot_data']['placements_with_allele'][0]
    print('placement top-level keys:', sorted(pl.keys()), '| placement_annot keys:', sorted(pl.get('placement_annot', {}).keys()))
    print('dbsnp1_merges:', p.get('dbsnp1_merges'))
    print('\n== shipped example __main__ ==')
    src = open(os.path.join(HERE, 'dbsnp_lookup.upstream_copy.py')).read().split("if __name__ == '__main__':")[1]
    exec(compile('\n'.join(l[4:] for l in src.splitlines()), 'example_main', 'exec'), ex.__dict__)


def in2():
    """Variant A: 'A 2004 paper cites rs630496 -- trace it to the current rsID.'"""
    r = requests.get(f'{sk.VARSVC}/refsnp/630496', timeout=30); nap()
    j = r.json()
    print('HTTP', r.status_code, 'top-level keys:', sorted(j.keys()))
    print('merged_snapshot_data:', json.dumps(j.get('merged_snapshot_data'))[:300])
    for label, fn in (('SKILL.md', sk.resolve_merge_chain), ('example', ex.resolve_merge_chain)):
        try:
            print(f'{label} resolve_merge_chain(rs630496):', fn('rs630496'))
        except Exception as e:
            print(f'{label} resolve_merge_chain(rs630496) RAISED {type(e).__name__}: {e!r}')
        nap()
    print('SKILL.md resolve_merge_chain(rs429358) (current id):', sk.resolve_merge_chain('rs429358'))


def in3():
    """Edge: 'Is rs334 multi-allelic? And what happens with a withdrawn or nonexistent rsID?'"""
    p = sk.refsnp('rs334'); nap()
    s = sk.summarize_refsnp(p)
    print('SKILL.md summarize_refsnp(rs334): alleles', [(a['ref'], a['alt']) for a in s['placements_grch38']], 'is_multiallelic =', s['is_multiallelic'])
    al = ex.alleles_grch38(p)
    print('example alleles_grch38(rs334):', [(a['ref'], a['alt']) for a in al])
    print('example batch_normalize_rsids multi-allelic rule (len>1 and >1 distinct REF) ->', len(al) > 1 and len({a['ref'] for a in al}) > 1)
    p2 = sk.refsnp('rs6025'); nap()
    s2 = sk.summarize_refsnp(p2)
    print('SKILL.md summarize_refsnp(rs6025): alleles', [(a['ref'], a['alt']) for a in s2['placements_grch38']], 'is_multiallelic =', s2['is_multiallelic'])
    for rid in ('rs1', 'rs999999999999', 'rs2'):
        r = requests.get(f'{sk.VARSVC}/refsnp/{rid[2:]}', timeout=30); nap()
        keys = sorted(r.json().keys()) if r.headers.get('content-type', '').startswith('application/json') else r.text[:80]
        print(rid, 'HTTP', r.status_code, keys if r.status_code != 200 else [k for k in keys if 'withdraw' in k or k in ('present_obs_movements', 'merged_snapshot_data', 'nosnppos_snapshot_data', 'unsupported_snapshot_data')])
        try:
            print('   SKILL resolve_merge_chain ->', sk.resolve_merge_chain(rid)); nap()
        except Exception as e:
            print('   SKILL resolve_merge_chain raised', type(e).__name__, str(e)[:120])


def in4():
    """Variant B: 'Convert APOE chr19:44908684 T>C and BRCA1 chr17:43106487 A>C (VCF, GRCh38) to canonical SPDI and rsIDs.'"""
    for c, pos, ref, alt in (('19', 44908684, 'T', 'C'), ('17', 43106487, 'A', 'C'), ('17', 43094464, 'G', 'A')):
        s1 = sk.vcf_to_canonical_spdi(c, pos, ref, alt); nap()
        s2 = ex.vcf_to_canonical_spdi(c, pos, ref, alt); nap()
        print(f'{c}:{pos} {ref}>{alt}  SKILL vcf_to_canonical_spdi -> {s1} | example -> {s2}')
        acc = ex.REFSEQ_GRCH38.get(c)
        rr = requests.get(f'{sk.VARSVC}/spdi/{acc}:{pos - 1}:{ref}:{alt}/canonical_representative', timeout=30); nap()
        print(f'   raw canonical_representative HTTP {rr.status_code}: {rr.text[:200]}')
        if rr.ok and not s2:
            d = rr.json().get('data', {})
            s2 = f"{d.get('seq_id')}:{d.get('position')}:{d.get('deleted_sequence')}:{d.get('inserted_sequence')}"
            print('   (the SKILL/example read data["spdi"], but the payload fields are', sorted(d.keys()), ')')
        if s2:
            spdi = f"{s2['seq_id']}:{s2['position']}:{s2['deleted_sequence']}:{s2['inserted_sequence']}" if isinstance(s2, dict) else s2
            r = requests.get(f'{sk.VARSVC}/spdi/{spdi}/rsids', timeout=30); nap()
            print('   GET /spdi/{spdi}/rsids HTTP', r.status_code, r.text[:160])
            try:
                print('   SKILL spdi_to_rsid(dict-as-str) ->', sk.spdi_to_rsid(s2)); nap()
            except Exception as e:
                print('   SKILL spdi_to_rsid raised', type(e).__name__)
            print('   SKILL spdi_to_rsid(str) ->', sk.spdi_to_rsid(spdi)); nap()
    print('SKILL hgvs_to_spdi_canonical(NC_000019.10:g.44908684T>C) ->', sk.hgvs_to_spdi_canonical('NC_000019.10:g.44908684T>C')); nap()
    print('SKILL hgvs_to_spdi_canonical(NM_000059.3:c.5946delT) ->', sk.hgvs_to_spdi_canonical('NM_000059.3:c.5946delT'))


def in5():
    """Stress: 'For rs6025, rs1799963, rs429358, rs7412 and rs121913529: current rsID, multi-allelic flag, ALFA total
    frequency, gnomAD AF and ClinVar significance in one table.'"""
    print('SKILL alfa_frequency(rs6025):', sk.alfa_frequency('rs6025')); nap()
    p = sk.refsnp('rs6025'); nap()
    fr = p['primary_snapshot_data']['allele_annotations'][0].get('frequency', [])
    print('frequency study_names in refsnp JSON:', sorted({f.get('study_name') for f in fr})[:12], '| any ALFA:', any('ALFA' in (f.get('study_name') or '') for f in fr))
    print('example alfa_population_frequencies(rs6025):', ex.alfa_population_frequencies('rs6025')); nap()
    r = requests.get(f'{sk.VARSVC}/refsnp/6025/frequency', timeout=30); nap()
    print('GET /refsnp/6025/frequency HTTP', r.status_code, r.text[:300])
    df = ex.batch_normalize_rsids(['rs6025', 'rs1799963', 'rs429358', 'rs7412', 'rs121913529'])
    print(df.to_string(index=False))


for name in (sys.argv[1:] or ['in1', 'in2', 'in3', 'in4', 'in5']):
    os.makedirs(os.path.join(HERE, name), exist_ok=True)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            globals()[name]()
        except Exception:
            traceback.print_exc(file=buf)
    open(os.path.join(HERE, name, 'out.txt'), 'w', encoding='utf-8').write(buf.getvalue())
    print(f'######## {name}\n' + buf.getvalue()[:3500])
