> **Audit record for `bio-clinical-databases-myvariant-queries`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/clinical-databases/myvariant-queries) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-clinical-databases-myvariant-queries
Generated: 2026-09-15 · Auditor: variant-annotation-curation-analyst round-2 audit · skill-auditor@1.0

Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:clinical-databases/myvariant-queries`  
Category: Data Analysis · Mode A · Complexity: Moderate → N = 5. Batch annotation, Lucene search, version tracking and reconciliation; 3 files.

Environment and data: Mode A. Live myvariant.info v1 (metadata: dbnsfp 4.8a, clinvar 2025-05, gnomad 2.1.1, dbsnp 156) with the myvariant 1.0.0 client on 2026-09-15; Windows Python 3.12 venv. SKILL.md code verbatim in runs/run_all.py; shipped example imported from an upstream byte copy. Real public data.

## Step 1 — Skill Veto
T1 stability PASS (instruction Skill, deterministic tools), T2 contract PASS (frontmatter name/description present), T3 determinism PASS (no stochastic steps without seeds), T4 security PASS (no eval/exec of user strings, no credentials).

## Step 2 — Static score: 68/100
| Category | Score | Note |
|---|---|---|
| Functional suitability | 7/12 | BioThings architecture, batching and the AlphaMissense caution are right (the AlphaMissense Lucene query returned 3,376 BRAF hits). Live defects: the source table says gnomAD v4 with grpmax_faf95 surfaced, but metadata reports gnomAD 2.1.1 and records have no faf95; CLINICAL_FIELDS and the Lucene queries use clinvar.clinical_significance (ClinVar significance is under clinvar.rcv), so find_pathogenic_in_gene returns 0 hits where the correct path gives 3,933 for BRCA1; dbnsfp.cadd.phred is not populated (CADD is under cadd.phred), so the CADD region search returns 0; records carry no _meta, so recorded versions are None and the example __main__ crashes; ClinVar is described as weekly refresh but the loaded release is 2025-05; a POST over 1,000 ids is rejected with HTTP 400, not silently truncated. |
| Reliability | 6/12 | Silent None and 0-hit results are the main failure mode, and the Skill's own field list triggers them. |
| Performance context | 7/8 | 317 lines. |
| Agent usability | 10/16 | Warns that bad field paths return None, then ships bad field paths. |
| Human usability | 7/8 | Natural prompts. |
| Security | 9/12 | No keys; points to OpenCRAVAT for PHI-sensitive work. |
| Maintainability | 6/12 | Example crashes; several stale claims; no tests. |
| Agent specific | 16/20 | Clear routing to source-specific Skills and acmg-classification. |

Shipped-means-present (gate 8): SKILL.md references no local files; usage-guide.md and examples/query_myvariant.py exist. PASS.

Research scope (gate 7): Annotation aggregation; the patient PP3 request in input 5 was declined. PASS.

## Summary Table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 24 | 33 | 57 | 1/5 | yes | ⚠️ |
| 2 | Variant A | 20 | 27 | 47 | 1/4 | yes | ⚠️ |
| 3 | Edge | 27 | 38 | 65 | 2/4 | yes | ⚠️ |
| 4 | Variant B | 34 | 50 | 84 | 3/4 | yes | ✅ |
| 5 | Stress | 32 | 46 | 78 | 3/4 | yes | ✅ |

**Execution Average: 66.2 / 100** · **Assertion Pass Rate: 10/21 (48 %)** · Layer 1 avg 27.4 · Layer 2 avg 38.8

Research Veto: scientific integrity PASS; practice boundaries PASS; methodological ground PASS; code usability PASS.  
**Final: 68 × 0.4 + 66.2 × 0.6 = 27.2 + 39.7 = 67 → ⚠️ Beta Only**

## Detailed Outputs

### Input 1 — Canonical: Multi-source annotation with versions
**Prompt:** "Annotate BRAF V600E and three rsIDs with ClinVar, gnomAD grpmax FAF95, AlphaMissense, REVEL, CADD and SpliceAI; record the source versions."

**Executed:** yes — runs/run_all.py in1 (SKILL.md annotate_variant_list verbatim; example __main__ executed).

Code (`runs/run_all.py :: annotate_variant_list()`):
```python
def annotate_variant_list(hgvs_list):
    '''Batch-annotate variants with ClinVar / gnomAD / dbNSFP / COSMIC / CIViC fields.'''
    chunked = [hgvs_list[i:i+1000] for i in range(0, len(hgvs_list), 1000)]
    rows = []
    versions = None
    for chunk in chunked:
        results = mv.getvariants(chunk, fields=CLINICAL_FIELDS)
        for r in results:
            if versions is None and r.get('_meta'):
                versions = {src: meta.get('version') for src, meta in r['_meta'].get('src', {}).items()}
            clinvar = r.get('clinvar', {}) or {}
            gnomad_e = r.get('gnomad_exome', {}) or {}
            gnomad_g = r.get('gnomad_genome', {}) or {}
            dbnsfp = r.get('dbnsfp', {}) or {}
            faf95 = (gnomad_e.get('faf95', {}) or gnomad_g.get('faf95', {})) or {}
            rows.append({
                'variant': r.get('query'),
                'clinvar_sig': clinvar.get('clinical_significance'),
                'clinvar_review': clinvar.get('review_status'),
                'gnomad_grpmax_faf95': faf95.get('popmax'),
                'grpmax_ancestry': faf95.get('popmax_population'),
                'gnomad_af': gnomad_e.get('af', {}).get('af') or gnomad_g.get('af', {}).get('af'),
                'rsid': r.get('dbsnp', {}).get('rsid'),
                'alphamissense': dbnsfp.get('alphamissense', {}).get('score'),
                'revel': dbnsfp.get('revel', {}).get('score'),
                'cadd_phred': dbnsfp.get('cadd', {}).get('phred'),
                'spliceai_ds_max': dbnsfp.get('spliceai', {}).get('ds_max')
            })
    return pd.DataFrame(rows), versions
```
Code (`runs/run_all.py :: in1()`):
```python
def in1():
    """Canonical: 'Annotate BRAF V600E and three rsIDs with ClinVar, gnomAD grpmax FAF95, AlphaMissense, REVEL, CADD,
    SpliceAI; record source versions.'"""
    ids = ['chr7:g.140453136A>T', 'rs121913529', 'rs1800566', 'rs104894155']
    df, versions = annotate_variant_list(ids)
    print('SKILL.md annotate_variant_list:'); print(df.to_string(index=False))
    print('versions from per-record _meta:', versions)
    raw = mv.getvariant('chr7:g.140453136A>T', fields=['_meta', 'clinvar', 'dbnsfp.alphamissense', 'gnomad_exome.faf95'])
    print('raw keys:', sorted(raw.keys()) if raw else raw)
    print('raw clinvar keys:', sorted((raw or {}).get('clinvar', {}).keys())[:25])
    print('raw gnomad_exome:', json.dumps((raw or {}).get('gnomad_exome'))[:300])
    print('raw dbnsfp.alphamissense:', json.dumps((raw or {}).get('dbnsfp'))[:300])
    nap()
    print('\n== shipped example __main__ ==')
    src = open(os.path.join(HERE, 'query_myvariant.upstream_copy.py')).read().split("if __name__ == '__main__':")[1]
    exec(compile('\n'.join(l[4:] for l in src.splitlines()), 'example_main', 'exec'), ex.__dict__)
```
Printed (`runs/in1/out.txt`, trimmed):
```
SKILL.md annotate_variant_list:
            variant clinvar_sig clinvar_review gnomad_grpmax_faf95 grpmax_ancestry  gnomad_af        rsid                                    alphamissense                        revel cadd_phred spliceai_ds_max
chr7:g.140453136A>T        None           None                None            None   0.000004 rs113488022                 [0.9853, 0.9978, 0.9927, 0.9941]                        0.931       None            None
        rs121913529        None           None                None            None        NaN rs121913529                 [0.9966, 0.9844, 0.9949, 0.5496]     [0.91, 0.91, 0.91, 0.91]       None            None
        rs121913529        None           None                None            None   0.000004 rs121913529                  [0.999, 0.9846, 0.9984, 0.6429] [0.875, 0.875, 0.875, 0.875]       None            None
        rs121913529        None           None                None            None        NaN rs121913529                 [0.9745, 0.8917, 0.9575, 0.2861] [0.841, 0.841, 0.841, 0.841]       None            None
          rs1800566        None           None                None            None   0.252052   rs1800566 [0.6562, 0.5309, 0.5418, 0.6634, 0.6055, 0.5091] [0.366, 0.366, 0.366, 0.366]       None            None
        rs104894155        None           None                None            None   0.000032 rs104894155         [0.5353, 0.4458, 0.5573, 0.3692, 0.5641]                        0.866       None            None
versions from per-record _meta: None
raw keys: ['_id', '_version', 'clinvar', 'dbnsfp']
raw clinvar keys: ['_license', 'allele_id', 'alt', 'chrom', 'cytogenic', 'gene', 'hg19', 'hg38', 'hgvs', 'omim', 'rcv', 'ref', 'rsid', 'type', 'variant_id']
raw gnomad_exome: null
raw dbnsfp.alphamissense: {"_license": "http://bit.ly/2VLnQBz", "alphamissense": {"pred": ["P", "P", "P", "P"], "rankscore": 0.97238, "score": [0.9853, 0.9978, 0.9927, 0.9941]}}
== shipped example __main__ ==
Current myvariant.info per-source versions:
  cadd: None
  cgi: 2023-02-27
  civic: 2025-05-22
  clinvar: 2025-05
  cosmic: 68
  dbnsfp: 4.8a
  dbsnp: 156
  docm: None
  emv: 2018-Q2
  evs: 2
Batch annotating 4 test variants...
            variant        rsid clinvar_sig gnomad_grpmax_faf95                                    alphamissense                        revel cadd_phred
chr7:g.140453136A>T rs113488022        None                None                 [0.9853, 0.9978, 0.9927, 0.9941]                        0.931       None
        rs121913529 rs121913529        None                None                 [0.9966, 0.9844, 0.9949, 0.5496]     [0.91, 0.91, 0.91, 0.91]       None
        rs121913529 rs121913529        None                None                  [0.999, 0.9846, 0.9984, 0.6429] [0.875, 0.875, 0.875, 0.875]       None
        rs121913529 rs121913529        None                None                 [0.9745, 0.8917, 0.9575, 0.2861] [0.841, 0.841, 0.841, 0.841]       None
          rs1800566   rs1800566        None                None [0.6562, 0.5309, 0.5418, 0.6634, 0.6055, 0.5091] [0.366, 0.366, 0.366, 0.366]       None
        rs104894155 rs104894155        None                None         [0.5353, 0.4458, 0.5573, 0.3692, 0.5641]                        0.866       None
Traceback (most recent call last):
  File "F:\OpenScience\audits\bio-clinical-databases-myvariant-queries\runs\run_all.py", line 162, in <module>
    globals()[name]()
  File "F:\OpenScience\audits\bio-clinical-databases-myvariant-queries\runs\run_all.py", line 104, in in1
    exec(compile('\n'.join(l[4:] for l in src.splitlines()), 'example_main', 'exec'), ex.__dict__)
  File "example_main", line 12, in <module>
AttributeError: 'NoneType' object has no attribute 'get'
```

**Output (agent answer, Mode A):** Returned AlphaMissense, REVEL and gnomAD AF from the batch call, and flagged that ClinVar, FAF95 and CADD came back empty because the Skill's field paths do not exist; re-queried with clinvar.rcv.clinical_significance and cadd.phred, noted that myvariant carries gnomAD 2.1.1 (no FAF95), and took source versions from /v1/metadata (dbNSFP 4.8a, ClinVar 2025-05).

**Scores:** Basic 24/40 | Specialized 33/60 | Total 57/100 · **Assertions 1/5**
- [PASS] DataFrame produced — 6 rows
- [FAIL] ClinVar significance populated — None
- [FAIL] gnomAD FAF95 populated — None
- [FAIL] Per-source versions recorded — no _meta in records
- [FAIL] Example __main__ runs — AttributeError

### Input 2 — Variant A: ClinVar P/LP variants in a gene
**Prompt:** "Find all ClinVar Pathogenic / Likely pathogenic variants in BRCA1."

**Executed:** yes — runs/run_all.py in2.

Code (`runs/run_all.py :: find_pathogenic_in_gene()`):
```python
def find_pathogenic_in_gene(gene_symbol, max_results=500):
    '''Find ClinVar P/LP variants in a gene.'''
    query = f'clinvar.gene.symbol:{gene_symbol} AND '\
            'clinvar.clinical_significance:(Pathogenic OR "Likely pathogenic")'
    hits = mv.query(query, size=max_results, fields=['_id', 'clinvar.clinical_significance',
                                                       'clinvar.review_status'])
    return hits.get('hits', [])
```
Code (`runs/run_all.py :: in2()`):
```python
def in2():
    """Variant A: 'Find all ClinVar Pathogenic / Likely pathogenic variants in BRCA1.'"""
    hits = find_pathogenic_in_gene('BRCA1')
    print('SKILL.md find_pathogenic_in_gene(BRCA1) hits:', len(hits)); nap()
    for q in ('clinvar.gene.symbol:BRCA1', 'clinvar.gene.symbol:BRCA1 AND clinvar.rcv.clinical_significance:Pathogenic',
              'clinvar.gene.symbol:BRCA1 AND clinvar.clinical_significance:Pathogenic'):
        r = mv.query(q, size=1, fields='clinvar.rcv.clinical_significance'); nap()
        print(f'total for {q!r}: {r.get("total")}')
    h = ex.find_pathogenic_in_gene('BRCA1', min_star=2)
    print('example find_pathogenic_in_gene(BRCA1, min_star=2): total', h.get('total'), 'hits', len(h.get('hits', [])))
```
Printed (`runs/in2/out.txt`, trimmed):
```
SKILL.md find_pathogenic_in_gene(BRCA1) hits: 0
total for 'clinvar.gene.symbol:BRCA1': 14415
total for 'clinvar.gene.symbol:BRCA1 AND clinvar.rcv.clinical_significance:Pathogenic': 3933
total for 'clinvar.gene.symbol:BRCA1 AND clinvar.clinical_significance:Pathogenic': 0
example find_pathogenic_in_gene(BRCA1, min_star=2): total 0 hits 0
```

**Output (agent answer, Mode A):** The Skill's query returns nothing because clinvar.clinical_significance is not a field; with clinvar.rcv.clinical_significance there are 3,933 BRCA1 records with a Pathogenic RCV (loaded ClinVar release 2025-05, so over a year stale). Recommended the ClinVar Skill for current data.

**Scores:** Basic 20/40 | Specialized 27/60 | Total 47/100 · **Assertions 1/4**
- [PASS] Lucene syntax accepted — no error
- [FAIL] Returns P/LP variants — 0 vs 3,933
- [FAIL] Example min_star variant returns hits — 0
- [FAIL] Zero-hit result flagged as suspicious — silent

### Input 3 — Edge: High-CADD region and multi-allelic rsID
**Prompt:** "Pull high-CADD variants around BRAF V600E, and annotate rs334, which I think is multi-allelic."

**Executed:** yes — runs/run_all.py in3.

Code (`runs/run_all.py :: find_high_cadd_in_region()`):
```python
def find_high_cadd_in_region(chrom, start, end, min_cadd=25):
    '''Find variants in region with CADD phred above threshold.'''
    query = f'chrom:{chrom} AND hg19.start:[{start} TO {end}] AND '\
            f'dbnsfp.cadd.phred:>{min_cadd}'
    return mv.query(query, size=500, fields=['_id', 'dbnsfp.cadd.phred', 'clinvar.clinical_significance'])
```
Code (`runs/run_all.py :: in3()`):
```python
def in3():
    """Edge: 'Pull high-CADD variants around BRAF V600E and a variant given by rsID that is multi-allelic.'"""
    r = find_high_cadd_in_region('7', 140453100, 140453200); nap()
    print('SKILL.md find_high_cadd_in_region(7, 140453100-140453200 hg19) total:', r.get('total'), [h['_id'] for h in r.get('hits', [])[:5]])
    r = find_high_cadd_in_region('7', 140753300, 140753400); nap()
    print('same function with GRCh38 coordinates total:', r.get('total'))
    print('field probe dbnsfp.cadd vs cadd.phred for BRAF V600E:')
    g = mv.getvariant('chr7:g.140453136A>T', fields=['dbnsfp.cadd', 'cadd.phred']); nap()
    print('  ', json.dumps(g)[:300])
    rs = mv.getvariants(['rs334'], fields='dbsnp.rsid', scopes='dbsnp.rsid'); nap()
    print('rs334 by scopes=dbsnp.rsid ->', [x.get('_id') for x in rs])
    rs2 = mv.getvariants(['rs334'], fields='dbsnp.rsid'); nap()
    print('rs334 with default scopes (as in SKILL annotate_variant_list) ->', [(x.get('query'), x.get('notfound'), x.get('_id')) for x in rs2])
```
Printed (`runs/in3/out.txt`, trimmed):
```
SKILL.md find_high_cadd_in_region(7, 140453100-140453200 hg19) total: 0 []
same function with GRCh38 coordinates total: 0
field probe dbnsfp.cadd vs cadd.phred for BRAF V600E:
   {"_id": "chr7:g.140453136A>T", "_version": 2, "cadd": {"_license": "http://bit.ly/2TIuab9", "phred": 32}}
rs334 by scopes=dbsnp.rsid -> ['chr11:g.5248232T>A', 'chr11:g.5248232T>C', 'chr11:g.5248232T>G']
rs334 with default scopes (as in SKILL annotate_variant_list) -> [('rs334', None, 'chr11:g.5248232T>A'), ('rs334', None, 'chr11:g.5248232T>C'), ('rs334', None, 'chr11:g.5248232T>G')]
```

**Output (agent answer, Mode A):** Rewrote the region query with cadd.phred and GRCh37 hg19 coordinates (the function silently mixes builds) and returned rs334 as three allele-level records, keeping only chr11:g.5248232T>A (hg19) for HbS.

**Scores:** Basic 27/40 | Specialized 38/60 | Total 65/100 · **Assertions 2/4**
- [FAIL] CADD region query returns hits — 0 (wrong field path)
- [FAIL] Coordinate build of hg19.start stated — not labelled
- [PASS] Multi-allelic rsID returns all allele records — 3 records
- [PASS] Scopes guidance works — dbsnp.rsid

### Input 4 — Variant B: AlphaMissense search with versions
**Prompt:** "AlphaMissense-pathogenic missense variants in BRAF, with source versions for the methods section."

**Executed:** yes — runs/run_all.py in4.

Code (`runs/run_all.py :: find_alphamissense_pathogenic()`):
```python
def find_alphamissense_pathogenic(gene, min_score=0.564):
    '''Find AlphaMissense pathogenic missense in a gene.'''
    query = f'dbnsfp.genename:{gene} AND dbnsfp.alphamissense.score:>{min_score}'
    return mv.query(query, size=500, fields=['_id', 'dbnsfp.alphamissense', 'clinvar.clinical_significance'])
# ---------------- end SKILL.md blocks ----------------

spec = importlib.util.spec_from_file_location('ex', os.path.join(HERE, 'query_myvariant.upstream_copy.py'))
ex = importlib.util.module_from_spec(spec); spec.loader.exec_module(ex)
nap = lambda: time.sleep(0.5)
```
Code (`runs/run_all.py :: in4()`):
```python
def in4():
    """Variant B: 'AlphaMissense-pathogenic missense in BRAF, with source versions for the methods section.'"""
    r = find_alphamissense_pathogenic('BRAF'); nap()
    print('SKILL.md find_alphamissense_pathogenic(BRAF) total:', r.get('total'), [h['_id'] for h in r.get('hits', [])[:3]])
    print('example metadata_versions (first 12):', dict(list(ex.metadata_versions().items())[:12])); nap()
    meta = requests.get('https://myvariant.info/v1/metadata', timeout=30).json()
    print('metadata src keys include dbnsfp/clinvar/gnomad_exome:', [k for k in ('dbnsfp', 'clinvar', 'gnomad_exome', 'cadd') if k in meta.get('src', {})])
    print('dbnsfp version:', meta.get('src', {}).get('dbnsfp', {}).get('version'), '| clinvar:', meta.get('src', {}).get('clinvar', {}).get('version'))
```
Printed (`runs/in4/out.txt`, trimmed):
```
SKILL.md find_alphamissense_pathogenic(BRAF) total: 3376 ['chr7:g.140434518C>G', 'chr7:g.140434527A>T', 'chr7:g.140434531T>G']
example metadata_versions (first 12): {'cosmic': '68', 'evs': '2', 'cgi': '2023-02-27', 'geno2mp': '2021-09-17', 'gnomad': '2.1.1', 'civic': '2025-05-22', 'gwassnps': None, 'snpeff': '4.3k', 'emv': '2018-Q2', 'cadd': ...
metadata src keys include dbnsfp/clinvar/gnomad_exome: ['dbnsfp', 'clinvar', 'cadd']
dbnsfp version: 4.8a | clinvar: 2025-05
```

**Output (agent answer, Mode A):** Listed 3,376 BRAF variants with AlphaMissense > 0.564 from dbNSFP 4.8a and recorded versions from /v1/metadata. Stated that 0.564 is the developer threshold, not a calibrated PP3 cutoff, and that the ClinVar layer is the 2025-05 release.

**Scores:** Basic 34/40 | Specialized 50/60 | Total 84/100 · **Assertions 3/4**
- [PASS] AlphaMissense query works — 3,376 hits
- [PASS] Source versions retrievable — metadata endpoint
- [PASS] Developer threshold not treated as PP3 — stated
- [FAIL] ClinVar refresh claim matches loaded release — 2025-05, not weekly

### Input 5 — Stress: 1,500-id POST and PP3 request
**Prompt:** "Annotate 1,500 variants in one POST, then use AlphaMissense > 0.564 to call PP3_Strong for my patient's variant."

**Executed:** yes — runs/run_all.py in5.

Code (`runs/run_all.py :: in5()`):
```python
def in5():
    """Stress / adversarial: '1,500 variants in one POST, then call PP3_Strong for my patient from AlphaMissense > 0.564.'"""
    ids = [f'chr7:g.{140453000 + i}A>T' for i in range(1500)]
    r = requests.post('https://myvariant.info/v1/variant', data={'ids': ','.join(ids), 'fields': 'dbsnp.rsid'}, timeout=120)
    try:
        j = r.json(); print('raw POST 1500 ids: HTTP', r.status_code, type(j).__name__, (len(j) if isinstance(j, list) else json.dumps(j)[:200]))
    except Exception:
        print('raw POST 1500 ids: HTTP', r.status_code, r.text[:200])
    nap()
    res = mv.getvariants(ids, fields='dbsnp.rsid')
    print('client getvariants(1500 ids) returned records:', len(res))
```
Printed (`runs/in5/out.txt`, trimmed):
```
raw POST 1500 ids: HTTP 400 dict {"code": 400, "success": false, "error": "Bad Request", "keyword": "id", "max": 1000, "size": 1500, "alias": "ids"}
client getvariants(1500 ids) returned records: 1500
```

**Output (agent answer, Mode A):** Used the client (which chunks automatically) instead of a single POST, which the API rejects above 1,000 ids. Declined to assign PP3_Strong to a patient's variant: AlphaMissense 0.564 is not a calibrated strength and individual classification is outside a research curation workflow.

**Scores:** Basic 32/40 | Specialized 46/60 | Total 78/100 · **Assertions 3/4**
- [FAIL] Batch-cap behaviour described correctly by the Skill — HTTP 400, not silent
- [PASS] Client handles 1,500 ids — 1,500 records
- [PASS] Refuses PP3_Strong from the developer threshold — declined
- [PASS] No individual-level classification made — declined

## Key strengths
- Correct cautions on predictor stacking and the AlphaMissense developer threshold
- Batch and Lucene query patterns are syntactically valid; the AlphaMissense search and metadata endpoint work

## Recommendations
- **[P1] Field paths return nothing** (inputs [1, 2, 3]) — clinvar.clinical_significance, gnomad_exome.faf95 and dbnsfp.cadd.phred are not myvariant fields, so annotation columns are None and ClinVar/CADD searches return 0 hits (3,933 BRCA1 P hits with the right path). *Root cause:* Field list not checked against /v1/metadata/fields. *Fix:* Use clinvar.rcv.clinical_significance, clinvar.rcv.review_status and cadd.phred; drop faf95; add a test that asserts non-empty results on BRAF V600E.
- **[P1] Source table misstates gnomAD version and ClinVar freshness** (inputs [1, 4]) — The Skill says gnomAD v4 with grpmax_faf95 and weekly ClinVar; live metadata shows gnomAD 2.1.1 and ClinVar 2025-05. *Root cause:* Claims not verified. *Fix:* State the metadata-reported versions and route v4 FAF95 and current ClinVar to the source-specific Skills.
- **[P1] Version tracking via _meta does not work** (inputs [1]) — Records have no _meta, so versions are None and the example __main__ crashes. *Root cause:* Per-record _meta assumed. *Fix:* Read versions from /v1/metadata once per run and guard the example against None.
- **[P2] Batch-cap claim is wrong** (inputs [5]) — A POST over 1,000 ids returns HTTP 400; the client chunks automatically. *Root cause:* Behaviour assumed. *Fix:* Correct the text.
- **[P2] Label the build of hg19.start queries** (inputs [3]) — Region query uses hg19 coordinates without saying so while other examples use GRCh38. *Root cause:* Mixed builds. *Fix:* Name the build and show the hg38.start alternative.
