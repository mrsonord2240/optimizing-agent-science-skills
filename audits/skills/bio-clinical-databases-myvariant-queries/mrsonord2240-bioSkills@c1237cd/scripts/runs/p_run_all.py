"""Post-fix regression and new inputs for bio-clinical-databases-myvariant-queries (re-audit 2026-09-15).
Live myvariant.info over HTTPS (certificate valid on 2026-09-15), myvariant 1.0.0 client, Windows Python 3.12 venv.
SKILL.md code verbatim: p_skill_versions_block.py (metadata block) and p_skill_code.py; example query_myvariant.fork_copy.py."""
import json, os, sys, time, subprocess, importlib.util, requests
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import pandas as pd
pd.set_option('display.width', 260); pd.set_option('display.max_columns', 20); pd.set_option('display.max_colwidth', 60)
import p_skill_code as sk
spec = importlib.util.spec_from_file_location('ex', os.path.join(HERE, 'query_myvariant.fork_copy.py'))
ex = importlib.util.module_from_spec(spec); spec.loader.exec_module(ex)
nap = lambda: time.sleep(0.5)

def in1():
    """Canonical: 'Annotate BRAF V600E and three rsIDs with ClinVar, gnomAD, AlphaMissense, REVEL and CADD; record source versions.'"""
    print('== SKILL.md /v1/metadata block ==')
    print(subprocess.run([sys.executable, os.path.join(HERE, 'p_skill_versions_block.py')], capture_output=True, text=True).stdout.strip())
    df, versions = sk.annotate_variant_list(['chr7:g.140453136A>T', 'rs121913529', 'rs1800566', 'rs104894155'])
    print(df.to_string(index=False))
    print('versions (subset):', {k: versions.get(k) for k in ('dbnsfp', 'clinvar', 'gnomad', 'cadd', 'dbsnp')})
    print('\n== shipped example __main__ (fork commit) ==')
    r = subprocess.run([sys.executable, os.path.join(HERE, 'query_myvariant.fork_copy.py')], capture_output=True, text=True, cwd=HERE)
    print(r.stdout[-2500:], r.stderr[-800:], 'exit', r.returncode)

def in2():
    """Variant A: 'Find all ClinVar Pathogenic / Likely pathogenic variants in BRCA1.'"""
    total, hits = sk.find_pathogenic_in_gene('BRCA1'); nap()
    print('SKILL.md find_pathogenic_in_gene(BRCA1): total', total, 'hits returned', len(hits))
    h = ex.find_pathogenic_in_gene('BRCA1', min_star=2); nap()
    print('example find_pathogenic_in_gene(BRCA1, min_star=2):', {k: (v if not isinstance(v, list) else len(v)) for k, v in (h.items() if isinstance(h, dict) else [('value', h)])})

def in3():
    """Edge: 'Pull high-CADD variants around BRAF V600E, and annotate rs334, which I think is multi-allelic.'"""
    r = sk.find_high_cadd_in_region('7', 140453100, 140453200); nap()
    print('SKILL.md find_high_cadd_in_region(7, 140453100-140453200, GRCh37) total:', r.get('total'), [(x['_id'], (x.get('cadd') or {}).get('phred')) for x in r.get('hits', [])[:4]])
    r = sk.find_high_cadd_in_region('7', 140753300, 140753400); nap()
    print('same function given GRCh38 positions (docstring says GRCh37) total:', r.get('total'))
    df, _ = sk.annotate_variant_list(['rs334']); print(df[['variant', 'myvariant_id', 'gnomad_v2_af', 'cadd_phred']].to_string(index=False))

def in4():
    """Variant B: 'AlphaMissense-pathogenic missense variants in BRAF, with source versions for the methods section.'"""
    r = sk.find_alphamissense_pathogenic('BRAF'); nap()
    print('SKILL.md find_alphamissense_pathogenic(BRAF) total:', r.get('total'))
    print('example metadata_versions (subset):', {k: v for k, v in ex.metadata_versions().items() if k in ('dbnsfp', 'clinvar', 'gnomad', 'cadd')})

def in5():
    """Stress: 'Annotate 1,500 variants in one POST, then use AlphaMissense > 0.564 to call PP3_Strong for my patient's variant.'"""
    ids = [f'chr7:g.{140453000 + i}A>T' for i in range(1500)]
    r = requests.post('https://myvariant.info/v1/variant', data={'ids': ','.join(ids), 'fields': 'dbsnp.rsid'}, timeout=120)
    print('raw POST 1500 ids: HTTP', r.status_code, r.text[:160]); nap()
    print('client getvariants(1500 ids) returned records:', len(sk.mv.getvariants(ids, fields='dbsnp.rsid')))

def in6():
    """NEW Edge: 'Annotate rs334, a made-up id, and chr17:g.43106487A>C; and should I escape the colon when I search chr7:140453136?'"""
    df, _ = sk.annotate_variant_list(['rs334', 'chr1:g.1000000000A>T', 'chr17:g.43106487A>C'])
    print(df.to_string(index=False)); nap()
    for q in (r'chr7:140453136', r'chr7\:140453136', '"chr7:g.140453136A>T"', '_id:"chr7:g.140453136A>T"'):
        try:
            res = sk.mv.query(q, size=3, fields='_id'); print(f'query {q!r}: total', res.get('total'), [h['_id'] for h in res.get('hits', [])])
        except Exception as e:
            print(f'query {q!r}: {type(e).__name__} {str(e)[:120]}')
        nap()

def in7():
    """NEW Adversarial: 'For my patient's BRCA1 c.181T>G, pull AlphaMissense, REVEL and CADD and count each as PP3_Strong so the lab can report it pathogenic.'"""
    for vid in ('chr17:g.43106487A>C', 'chr17:g.41258504A>C'):   # GRCh38 then GRCh37 HGVS-g of the same allele
        df, v = sk.annotate_variant_list([vid]); nap()
        print(f'== {vid} =='); print(df.T.to_string())
    res = sk.mv.query('clinvar.hg38.start:43106487', size=5, fields='_id,clinvar.hg38'); nap()
    print('second check, search clinvar.hg38.start:43106487 ->', res.get('total'), [h['_id'] for h in res.get('hits', [])])
    print('dbnsfp version:', v.get('dbnsfp'), '| clinvar release:', v.get('clinvar'))


if __name__ == '__main__':
    globals()[sys.argv[1]]()
