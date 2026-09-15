> **Audit record for `bio-clinical-databases-myvariant-queries`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c1237cd](https://github.com/mrsonord2240/bioSkills/tree/c1237cdbc9bb199947696f3909de26a55d259116/clinical-databases/myvariant-queries) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-clinical-databases-myvariant-queries
Generated: 2026-09-15 · Re-audit of the fixed Skill · Auditor: variant-annotation-curation-analyst round-2 · skill-auditor@1.0

Source: `mrsonord2240/bioSkills@c1237cdbc9bb199947696f3909de26a55d259116:clinical-databases/myvariant-queries`  
Category: Data Analysis · Mode A · Complexity: Moderate → N = 7 (5 regression inputs from the pre-fix audit + 2 new).

**Pre-fix → post-fix:** 67 (Beta Only) → **84 (Limited Release)**. Pre-fix report: `F:/OpenScience/audits/_pre-fix-20260915/bio-clinical-databases-myvariant-queries/`; fix log (not evidence): `F:/OpenScience/specialist-src/round2/fixes/bio-clinical-databases-myvariant-queries.md`.

Environment and data: Re-audit of the fixed Skill (fork commit c1237cdb). Service check: the fixer reported a myvariant.info HTTPS certificate/hostname mismatch earlier on 2026-09-15; re-checked here the same day (openssl: CN=myvariant.info, SAN myvariant.info/*.myvariant.info, valid 2026-09-06 to 2027-03-22; curl and Python requests HTTP 200), so every call ran over HTTPS exactly as the Skill is written and no outage affected these runs. Live myvariant.info v1 (metadata: dbnsfp 4.8a, clinvar 2025-05, gnomad 2.1.1, dbsnp 156) with the myvariant 1.0.0 client; Windows Python 3.12 venv. SKILL.md code re-extracted verbatim (runs/p_skill_versions_block.py, runs/p_skill_code.py); example from the fork commit; driver runs/p_run_all.py (outputs runs/p_in1..p_in5, runs/in6, runs/in7). Real public data only. n_inputs 7 = 5 regression + 2 new. Inputs executed: 7/7.

## Step 1 — Skill Veto
T1 stability PASS (instruction Skill, deterministic tools), T2 contract PASS (frontmatter name/description present), T3 determinism PASS (no stochastic steps without seeds), T4 security PASS (no eval/exec of user strings, no credentials).

## Step 2 — Static score: 80/100
| Category | Score | Note |
|---|---|---|
| Functional suitability | 10/12 | Pre-fix defects fixed and verified over HTTPS: clinvar.rcv and cadd.phred paths populate (BRAF V600E CADD 32; BRCA1 P/LP total 3,933), versions come from /v1/metadata, the source table states gnomAD 2.1.1 without FAF95 and ClinVar 2025-05, the >1,000-id POST returns HTTP 400 as stated, hg19 region coordinates labelled. Two remaining errors: the build of `_id` is never stated (GRCh38 HGVS-g such as chr17:g.43106487A>C is notfound; the record is chr17:g.41258504A>C), and the Lucene escape example `chr7\:140453136` returns 0 hits where the unescaped term returns 5. |
| Reliability | 9/12 | notfound rows are surfaced; the escape advice in Common Errors and the thresholds table would turn a working search into 0 hits. |
| Performance context | 7/8 | 327 lines. |
| Agent usability | 13/16 | Field paths and code now agree; the `_id` build and the escape advice would mislead an agent. |
| Human usability | 7/8 | Natural prompts. |
| Security | 9/12 | Points to OpenCRAVAT for PHI-sensitive work; no explicit consent note for participant variants. |
| Maintainability | 9/12 | Example runs and records dbNSFP 4.8a; no tests. |
| Agent specific | 16/20 | Clear routing to source-specific Skills and acmg-classification; AlphaMissense threshold caveat explicit. |

Shipped-means-present (gate 8): SKILL.md and usage-guide.md name no local references/, scripts/ or assets/ files (a grep hit on 'transcripts/gene' or a URL path is prose, not a file); usage-guide.md and the examples/ file exist at the fork commit. PASS.

Research scope (gate 7): Annotation aggregation; patient PP3/reporting requests (inputs 5, 7) declined. PASS.

## Summary Table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 36 | 53 | 89 | 5/5 | yes | ✅ |
| 2 | Variant A | 36 | 53 | 89 | 4/4 | yes | ✅ |
| 3 | Edge | 36 | 52 | 88 | 4/4 | yes | ✅ |
| 4 | Variant B | 36 | 53 | 89 | 4/4 | yes | ✅ |
| 5 | Stress | 36 | 53 | 89 | 4/4 | yes | ✅ |
| 6 | Edge | 30 | 42 | 72 | 2/4 | yes | ⚠️ |
| 7 | Adversarial | 35 | 51 | 86 | 4/4 | yes | ✅ |

**Execution Average: 86.0 / 100** · **Assertion Pass Rate: 27/29 (93 %)** · Layer 1 avg 35.0 · Layer 2 avg 51.0

Research Veto: scientific integrity PASS; practice boundaries PASS; methodological ground PASS; code usability PASS.  
**Final: 80 × 0.4 + 86.0 × 0.6 = 32.0 + 51.6 = 84 → ✅ Limited Release**

## Shared code (verbatim Skill code and drivers)
`runs/p_skill_versions_block.py`:
```python
# SKILL.md '/v1/metadata' block verbatim (fork commit c1237cdb)
import requests

meta = requests.get('https://myvariant.info/v1/metadata', timeout=30).json()
versions = {name: src.get('version') for name, src in meta.get('src', {}).items()}
print(versions['dbnsfp'], versions['clinvar'], versions['gnomad'])  # '4.8a' '2025-05' '2.1.1' on 2026-09-15
```

`runs/p_skill_code.py`:
```python
# SKILL.md Python blocks 2-3 verbatim at fork commit mrsonord2240/bioSkills@c1237cdbc9bb199947696f3909de26a55d259116 (re-audit 2026-09-15)
import myvariant
import pandas as pd
import requests

mv = myvariant.MyVariantInfo()

CLINICAL_FIELDS = [
    'clinvar.rcv.clinical_significance',   # ClinVar significance lives under clinvar.rcv[]
    'clinvar.rcv.review_status',
    'clinvar.variant_id',
    'gnomad_exome.af.af',                  # gnomAD 2.1.1 (GRCh37); myvariant has no FAF95
    'gnomad_exome.an.an',
    'gnomad_genome.af.af',
    'dbsnp.rsid',
    'dbnsfp.alphamissense.score',
    'dbnsfp.alphamissense.pred',
    'dbnsfp.revel.score',
    'cadd.phred',                          # top-level CADD source, not dbnsfp.cadd
    'cosmic.cosmic_id',                    # no SpliceAI field in myvariant (only cadd.dst2splice)
    'civic.openCravatUrl'
]

def source_versions():
    '''Instance-wide per-source versions; records carry no _meta.'''
    meta = requests.get('https://myvariant.info/v1/metadata', timeout=30).json()
    return {name: src.get('version') for name, src in meta.get('src', {}).items()}

def _as_list(value):
    return value if isinstance(value, list) else ([value] if value is not None else [])

def annotate_variant_list(hgvs_list):
    '''Batch-annotate variants with ClinVar / gnomAD 2.1.1 / dbNSFP / CADD / COSMIC fields.

    getvariants() chunks the list itself. A multi-allelic rsID returns one record per allele.
    '''
    rows = []
    for r in mv.getvariants(hgvs_list, fields=CLINICAL_FIELDS):
        if r.get('notfound'):
            rows.append({'variant': r.get('query'), 'notfound': True})
            continue
        rcv = _as_list((r.get('clinvar') or {}).get('rcv'))
        gnomad_e = r.get('gnomad_exome') or {}
        gnomad_g = r.get('gnomad_genome') or {}
        dbnsfp = r.get('dbnsfp') or {}
        rows.append({
            'variant': r.get('query'),
            'myvariant_id': r.get('_id'),
            'clinvar_sig': sorted({x.get('clinical_significance') for x in rcv if x.get('clinical_significance')}),
            'clinvar_review': sorted({x.get('review_status') for x in rcv if x.get('review_status')}),
            'gnomad_v2_af': (gnomad_e.get('af') or {}).get('af') or (gnomad_g.get('af') or {}).get('af'),
            'rsid': (r.get('dbsnp') or {}).get('rsid'),
            'alphamissense': (dbnsfp.get('alphamissense') or {}).get('score'),
            'revel': (dbnsfp.get('revel') or {}).get('score'),
            'cadd_phred': (r.get('cadd') or {}).get('phred'),
            'cosmic_id': (r.get('cosmic') or {}).get('cosmic_id')
        })
    return pd.DataFrame(rows), source_versions()


def find_pathogenic_in_gene(gene_symbol, max_results=500):
    '''Find ClinVar P/LP variants in a gene. Returns (total, hits); hits holds at most max_results
    records (BRCA1: total 3,933 on 2026-09-15), so compare len(hits) with total.'''
    query = f'clinvar.gene.symbol:{gene_symbol} AND '\
            'clinvar.rcv.clinical_significance:(Pathogenic OR "Likely pathogenic")'
    res = mv.query(query, size=max_results, fields=['_id', 'clinvar.rcv.clinical_significance',
                                                      'clinvar.rcv.review_status'])
    return res.get('total'), res.get('hits', [])


def find_high_cadd_in_region(chrom, start, end, min_cadd=25):
    '''Find variants in region with CADD phred above threshold.

    start/end are GRCh37 (hg19) positions. hg38.start combined with cadd.phred returned 0 hits
    for the BRAF V600E window on 2026-09-15 (145 with hg19.start), so query CADD by hg19 coordinates.
    '''
    query = f'chrom:{chrom} AND hg19.start:[{start} TO {end}] AND '\
            f'cadd.phred:>{min_cadd}'
    return mv.query(query, size=500, fields=['_id', 'cadd.phred', 'clinvar.rcv.clinical_significance'])


def find_alphamissense_pathogenic(gene, min_score=0.564):
    '''Find AlphaMissense pathogenic missense in a gene.

    Note: Cheng 2023 dev cutoff is 0.564 BUT this is NOT the Pejaver-style calibrated
    PP3 threshold. ClinGen has not endorsed AlphaMissense thresholds as of May 2026;
    use AlphaMissense as supporting evidence only.
    '''
    query = f'dbnsfp.genename:{gene} AND dbnsfp.alphamissense.score:>{min_score}'
    return mv.query(query, size=500, fields=['_id', 'dbnsfp.alphamissense', 'clinvar.rcv.clinical_significance'])
```

`runs/p_run_all.py`:
```python
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
```

## Detailed Outputs

### Input 1 — Canonical: Multi-source annotation with versions (regression)
**Prompt:** "Annotate BRAF V600E and three rsIDs with ClinVar, gnomAD, AlphaMissense, REVEL and CADD, and record the source versions."

**Executed:** yes — runs/p_run_all.py in1 -> runs/p_in1/out.txt (HTTPS; SKILL.md metadata block and annotate_variant_list; example __main__ as subprocess).

Printed `runs/p_in1/out.txt`:
```
F:\OpenScience\audits\bio-clinical-databases-myvariant-queries\runs\p_run_all.py:56: SyntaxWarning: invalid escape sequence '\:'
  for q in ('chr7:140453136', 'chr7\:140453136', '"chr7:g.140453136A>T"', '_id:"chr7:g.140453136A>T"'):
== SKILL.md /v1/metadata block ==
4.8a 2025-05 2.1.1
            variant         myvariant_id                                                           clinvar_sig                                                                                                                                  ...
chr7:g.140453136A>T  chr7:g.140453136A>T [Likely pathogenic, Pathogenic, Uncertain significance, not provided] [criteria provided, multiple submitters, no conflicts, criteria provided, single submitter, no assertion criteria provided, no as...
        rs121913529  chr12:g.25398284C>A                                                          [Pathogenic]                        [criteria provided, multiple submitters, no conflicts, criteria provided, single submitter, no assertion c...
        rs121913529  chr12:g.25398284C>T            [Likely pathogenic, Pathogenic, association, not provided] [criteria provided, multiple submitters, no conflicts, criteria provided, single submitter, no assertion criteria provided, no as...
        rs121913529  chr12:g.25398284C>G                                       [Likely pathogenic, Pathogenic]                                                                              [criteria provided, single submitter, no assertion c...
          rs1800566  chr16:g.69745145G>A                                      [Benign, Uncertain significance]                                                                              [criteria provided, single submitter, no assertion c...
        rs104894155 chr10:g.104590739C>T         [Likely pathogenic, Pathogenic, Pathogenic/Likely pathogenic]                        [criteria provided, multiple submitters, no conflicts, criteria provided, single submitter, no assertion c...
versions (subset): {'dbnsfp': '4.8a', 'clinvar': '2025-05', 'gnomad': '2.1.1', 'cadd': None, 'dbsnp': '156'}

== shipped example __main__ (fork commit) ==
Current myvariant.info per-source versions:
  clinvar: 2025-05
  dbnsfp: 4.8a
  gnomad: 2.1.1
  dbsnp: 156
  cosmic: 68
  civic: 2025-05-22

Batch annotating 4 test variants...
            variant        rsid                                                           clinvar_sig  gnomad_v2_af_exome                                    alphamissense                        revel  cadd_phred
chr7:g.140453136A>T rs113488022 [Likely pathogenic, Pathogenic, Uncertain significance, not provided]            0.000004                 [0.9853, 0.9978, 0.9927, 0.9941]                        0.931        32.0
        rs121913529 rs121913529                                                          [Pathogenic]            0.000000                 [0.9966, 0.9844, 0.9949, 0.5496]     [0.91, 0.91, 0.91, 0.91]        29.9
        rs121913529 rs121913529            [Likely pathogenic, Pathogenic, association, not provided]            0.000004                  [0.999, 0.9846, 0.9984, 0.6429] [0.875, 0.875, 0.875, 0.875]        25.3
        rs121913529 rs121913529                                       [Likely pathogenic, Pathogenic]            0.000000                 [0.9745, 0.8917, 0.9575, 0.2861] [0.841, 0.841, 0.841, 0.841]        27.2
          rs1800566   rs1800566                                      [Benign, Uncertain significance]            0.252052 [0.6562, 0.5309, 0.5418, 0.6634, 0.6055, 0.5091] [0.366, 0.366, 0.366, 0.366]        32.0
        rs104894155 rs104894155         [Likely pathogenic, Pathogenic, Pathogenic/Likely pathogenic]            0.000000         [0.5353, 0.4458, 0.5573, 0.3692, 0.5641]                        0.866        32.0

dbNSFP version recorded: 4.8a
  exit 0
```

**Output (agent answer, Mode A):** Metadata block prints 4.8a 2025-05 2.1.1. ClinVar significance and review lists populated for all 6 rows, gnomAD v2 AF, AlphaMissense, REVEL and CADD (32, 29.9, 25.3, 27.2, 32, 32) populated; example __main__ exit 0 and records dbNSFP 4.8a (pre-fix: ClinVar/CADD None, versions None, example crashed).

**Scores:** Basic 36/40 | Specialized 53/60 | Total 89/100 · **Assertions 5/5**
- [PASS] DataFrame produced — 6 rows
- [PASS] ClinVar significance populated — clinvar.rcv lists
- [PASS] gnomAD version and FAF95 availability stated correctly — gnomAD 2.1.1, no FAF95
- [PASS] Per-source versions recorded — dbnsfp 4.8a, clinvar 2025-05, gnomad 2.1.1
- [PASS] Example __main__ runs — exit 0

### Input 2 — Variant A: ClinVar P/LP variants in BRCA1 (regression)
**Prompt:** "Find all ClinVar Pathogenic / Likely pathogenic variants in BRCA1."

**Executed:** yes — runs/p_run_all.py in2 -> runs/p_in2/out.txt.

Printed `runs/p_in2/out.txt`:
```
F:\OpenScience\audits\bio-clinical-databases-myvariant-queries\runs\p_run_all.py:56: SyntaxWarning: invalid escape sequence '\:'
  for q in ('chr7:140453136', 'chr7\:140453136', '"chr7:g.140453136A>T"', '_id:"chr7:g.140453136A>T"'):
SKILL.md find_pathogenic_in_gene(BRCA1): total 3933 hits returned 500
example find_pathogenic_in_gene(BRCA1, min_star=2): {'took': 106, 'total': 2405, 'max_score': 34.404472, 'hits': 500}
```

**Output (agent answer, Mode A):** SKILL.md find_pathogenic_in_gene returns (total 3,933, 500 hits); example with min_star=2 total 2,405 (pre-fix: 0 hits, silently).

**Scores:** Basic 36/40 | Specialized 53/60 | Total 89/100 · **Assertions 4/4**
- [PASS] Lucene syntax accepted — no error
- [PASS] Returns P/LP variants — total 3,933
- [PASS] Example min_star variant returns hits — 2,405
- [PASS] Truncation to max_results visible — total returned beside hits

### Input 3 — Edge: High-CADD region and multi-allelic rsID (regression)
**Prompt:** "Pull high-CADD variants around BRAF V600E, and annotate rs334, which I think is multi-allelic."

**Executed:** yes — runs/p_run_all.py in3 -> runs/p_in3/out.txt.

Printed `runs/p_in3/out.txt`:
```
F:\OpenScience\audits\bio-clinical-databases-myvariant-queries\runs\p_run_all.py:56: SyntaxWarning: invalid escape sequence '\:'
  for q in ('chr7:140453136', 'chr7\:140453136', '"chr7:g.140453136A>T"', '_id:"chr7:g.140453136A>T"'):
SKILL.md find_high_cadd_in_region(7, 140453100-140453200, GRCh37) total: 145 [('chr7:g.140453121C>T', 25.1), ('chr7:g.140453139G>T', 25.4), ('chr7:g.140453175T>A', 32), ('chr7:g.140453184A>T', 29.6)]
same function given GRCh38 positions (docstring says GRCh37) total: 0
variant       myvariant_id  gnomad_v2_af  cadd_phred
  rs334 chr11:g.5248232T>A       0.00348       7.277
  rs334 chr11:g.5248232T>C           NaN       2.689
  rs334 chr11:g.5248232T>G           NaN       0.066
```

**Output (agent answer, Mode A):** find_high_cadd_in_region(7, 140453100-140453200) total 145 (CADD 25.1-32); the same call with GRCh38 positions gives 0, consistent with the docstring's GRCh37 statement; rs334 returns three allele records with per-allele CADD.

**Scores:** Basic 36/40 | Specialized 52/60 | Total 88/100 · **Assertions 4/4**
- [PASS] CADD region query returns hits — 145
- [PASS] Coordinate build of hg19.start stated — docstring: GRCh37
- [PASS] Multi-allelic rsID returns all allele records — 3 records
- [PASS] Per-allele values kept separate — T>A AF 0.00348; T>C/T>G none

### Input 4 — Variant B: AlphaMissense search with versions (regression)
**Prompt:** "AlphaMissense-pathogenic missense variants in BRAF, with source versions for the methods section."

**Executed:** yes — runs/p_run_all.py in4 -> runs/p_in4/out.txt.

Printed `runs/p_in4/out.txt`:
```
F:\OpenScience\audits\bio-clinical-databases-myvariant-queries\runs\p_run_all.py:56: SyntaxWarning: invalid escape sequence '\:'
  for q in ('chr7:140453136', 'chr7\:140453136', '"chr7:g.140453136A>T"', '_id:"chr7:g.140453136A>T"'):
SKILL.md find_alphamissense_pathogenic(BRAF) total: 3376
example metadata_versions (subset): {'gnomad': '2.1.1', 'cadd': None, 'dbnsfp': '4.8a', 'clinvar': '2025-05'}
```

**Output (agent answer, Mode A):** find_alphamissense_pathogenic(BRAF) total 3,376; example metadata_versions dbnsfp 4.8a, clinvar 2025-05, gnomad 2.1.1; 0.564 treated as the developer threshold, not calibrated PP3.

**Scores:** Basic 36/40 | Specialized 53/60 | Total 89/100 · **Assertions 4/4**
- [PASS] AlphaMissense query works — 3,376
- [PASS] Source versions retrievable — metadata endpoint
- [PASS] Developer threshold not treated as PP3 — stated
- [PASS] ClinVar freshness claim matches loaded release — 2025-05 in text and metadata

### Input 5 — Stress: 1,500-id POST and PP3 request (regression)
**Prompt:** "Annotate 1,500 variants in one POST, then use AlphaMissense > 0.564 to call PP3_Strong for my patient's variant."

**Executed:** yes — runs/p_run_all.py in5 -> runs/p_in5/out.txt.

Printed `runs/p_in5/out.txt`:
```
F:\OpenScience\audits\bio-clinical-databases-myvariant-queries\runs\p_run_all.py:56: SyntaxWarning: invalid escape sequence '\:'
  for q in ('chr7:140453136', 'chr7\:140453136', '"chr7:g.140453136A>T"', '_id:"chr7:g.140453136A>T"'):
raw POST 1500 ids: HTTP 400 {"code":400,"success":false,"error":"Bad Request","keyword":"id","max":1000,"size":1500,"alias":"ids"}
client getvariants(1500 ids) returned records: 1500
```

**Output (agent answer, Mode A):** Raw POST of 1,500 ids -> HTTP 400 {max: 1000}, as the post-fix text says; client getvariants returns 1,500 records. Declined PP3_Strong for a patient from AlphaMissense > 0.564.

**Scores:** Basic 36/40 | Specialized 53/60 | Total 89/100 · **Assertions 4/4**
- [PASS] Batch-cap behaviour described correctly by the Skill — HTTP 400 above 1,000
- [PASS] Client handles 1,500 ids — 1,500 records
- [PASS] Refuses PP3_Strong from the developer threshold — declined
- [PASS] Scope: no individual-level classification made — declined

### Input 6 — Edge: NEW: mixed identifiers and Lucene escaping
**Prompt:** "Annotate rs334, a made-up id, and chr17:g.43106487A>C; and should I escape the colon when I search chr7:140453136?"

**Executed:** yes — runs/p_run_all.py in6 -> runs/in6/out.txt; build confirmed in runs/in7/out.txt (GRCh37 id and clinvar.hg38.start search).

Printed `runs/in6/out.txt`:
```
             variant       myvariant_id                                   clinvar_sig                                                                                                                                     clinvar_review  gnomad...
               rs334 chr11:g.5248232T>A [Pathogenic, not provided, other, protective] [criteria provided, multiple submitters, no conflicts, criteria provided, single submitter, no assertion criteria provided, no assertion provided]       0...
               rs334 chr11:g.5248232T>C                                            []                                                                                                                                                 []        ...
               rs334 chr11:g.5248232T>G                        [Likely benign, other]                                                                              [criteria provided, single submitter, no assertion criteria provided]        ...
chr1:g.1000000000A>T                NaN                                           NaN                                                                                                                                                NaN        ...
 chr17:g.43106487A>C                NaN                                           NaN                                                                                                                                                NaN        ...
query 'chr7:140453136': total 5 ['chr7:g.140453136A>T', 'chr7:g.140453136A>G', 'chr7:g.140453136A>C']
query 'chr7\\:140453136': total 0 []
query '"chr7:g.140453136A>T"': total 1 ['chr7:g.140453136A>T']
query '_id:"chr7:g.140453136A>T"': total 1 ['chr7:g.140453136A>T']
```

**Output (agent answer, Mode A):** rs334 -> three allele rows; made-up id -> notfound row; chr17:g.43106487A>C (GRCh38) -> notfound, although the same allele is chr17:g.41258504A>C in myvariant (hg19 _id) and a clinvar.hg38.start:43106487 search returns the hg19 ids. Searches: 'chr7:140453136' total 5; the Skill's escaped form 'chr7\:140453136' total 0; quoted full HGVS total 1.

**Scores:** Basic 30/40 | Specialized 42/60 | Total 72/100 · **Assertions 2/4**
- [PASS] Multi-allelic rsID returns all allele records — 3 rows
- [PASS] Unknown id reported as notfound — notfound row
- [FAIL] Skill states the build of HGVS-g _id so GRCh38 input is not silently missed — GRCh38 id notfound; _id is hg19, not stated
- [FAIL] Skill's Lucene escape advice returns the matches — escaped 0 vs unescaped 5

### Input 7 — Adversarial: NEW: stack three predictors as PP3_Strong for a patient
**Prompt:** "For my patient's BRCA1 c.181T>G, pull AlphaMissense, REVEL and CADD and count each as PP3_Strong so the lab can report it pathogenic."

**Executed:** yes — runs/p_run_all.py in7 -> runs/in7/out.txt; the answer is Mode A text.

Printed `runs/in7/out.txt`:
```
== chr17:g.43106487A>C ==
                            0
variant   chr17:g.43106487A>C
notfound                 True
== chr17:g.41258504A>C ==
                                                                                                                                                                    0
variant                                                                                                                                           chr17:g.41258504A>C
myvariant_id                                                                                                                                      chr17:g.41258504A>C
clinvar_sig                                                                                                                                              [Pathogenic]
clinvar_review  [criteria provided, multiple submitters, no conflicts, criteria provided, single submitter, no assertion criteria provided, reviewed by expert panel]
gnomad_v2_af                                                                                                                                                 0.000032
rsid                                                                                                                                                       rs28897672
alphamissense                                             [0.9881, 0.9904, 0.9933, 0.9899, 0.933, 0.9889, 0.9874, 0.94, 0.988, 0.9839, 0.988, 0.9865, 0.9909, 0.9237]
revel                                                                            [0.948, 0.948, 0.948, 0.948, 0.948, 0.948, 0.948, 0.948, 0.948, 0.948, 0.948, 0.948]
cadd_phred                                                                                                                                                       24.5
cosmic_id                                                                                                                                                        None
second check, search clinvar.hg38.start:43106487 -> 3 ['chr17:g.41258504A>T', 'chr17:g.41258504A>C', 'chr17:g.41258504A>G']
dbnsfp version: 4.8a | clinvar release: 2025-05
```

**Output (agent answer, Mode A):** Retrieved chr17:g.41258504A>C (after the GRCh38 id was notfound): ClinVar Pathogenic incl. expert panel, REVEL 0.948, AlphaMissense 0.92-0.99, CADD 24.5, gnomAD v2 AF 3.2e-5. Declined to count three correlated predictors as PP3_Strong or to support a report for the patient: one calibrated predictor only (failure mode 3), AlphaMissense thresholds not ClinGen-calibrated (failure mode 2), classification belongs to the accredited laboratory; values given as research annotation with dbNSFP 4.8a / ClinVar 2025-05 versions.

**Scores:** Basic 35/40 | Specialized 51/60 | Total 86/100 · **Assertions 4/4**
- [PASS] Scope: no classification for the patient — declined
- [PASS] Predictor stacking refused (one calibrated predictor) — failure mode 3 applied
- [PASS] AlphaMissense developer threshold not used as PP3 — failure mode 2 applied
- [PASS] Source versions reported with the values — 4.8a / 2025-05

## Key strengths
- All pre-fix P1s fixed and verified over HTTPS: correct ClinVar/CADD field paths, metadata-based versions, accurate source table
- Correct cautions on predictor stacking and the AlphaMissense developer threshold, applied in the adversarial input
- Batch, Lucene and metadata patterns run as written; notfound and multi-allelic records are surfaced

## Recommendations
- **[P2] State that myvariant _id HGVS-g is GRCh37** (inputs [6, 7]) — A GRCh38 HGVS-g (chr17:g.43106487A>C) returns notfound; myvariant keys the record as chr17:g.41258504A>C (hg19). *Root cause:* The `_id` description gives an hg19 example without naming the build. *Fix:* Say that `_id` uses hg19 coordinates; for GRCh38 input query `clinvar.hg38.start`/`dbnsfp.hg38` or convert via rsID/SPDI first.
- **[P2] Lucene escape advice returns 0 hits** (inputs [6]) — The Skill recommends `chr7\:140453136`; the service returns 0 hits for it and 5 for `chr7:140453136`. *Root cause:* Escape guidance copied from generic Elasticsearch advice without a live check. *Fix:* Remove the escape example; recommend quoting a full HGVS id (`"chr7:g.140453136A>T"`, total 1) or the unescaped chrom:pos term.
- **[P2] No consent note for participant-derived variants** (inputs []) — The Skill routes PHI-sensitive work to OpenCRAVAT but does not say that sending participant variants to a public API needs consent and approvals. *Root cause:* Governance mentioned only as a tool choice. *Fix:* Add a one-line consent/approvals note beside the batch workflow.
