> **Audit record for `bio-clinical-databases-dbsnp-queries`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/clinical-databases/dbsnp-queries) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-clinical-databases-dbsnp-queries
Generated: 2026-09-15 · Auditor: variant-annotation-curation-analyst round-2 audit · skill-auditor@1.0

Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:clinical-databases/dbsnp-queries`  
Category: Data Analysis · Mode A · Complexity: Moderate → N = 5. rsID resolution, merge chains, SPDI/HGVS conversion and ALFA frequencies; 3 files.

Environment and data: Mode A. Live NCBI Variation Services v0 (no API key, 0.4 s spacing) and myvariant.info on 2026-09-15; Windows Python 3.12 venv. SKILL.md code verbatim in runs/skill_code.py; shipped example imported from an upstream byte copy. Real public data only. Bulk JSON download was not run.

## Step 1 — Skill Veto
T1 stability PASS (instruction Skill, deterministic tools), T2 contract PASS (frontmatter name/description present), T3 determinism PASS (no stochastic steps without seeds), T4 security PASS (no eval/exec of user strings, no credentials).

## Step 2 — Static score: 70/100
| Category | Score | Note |
|---|---|---|
| Functional suitability | 7/12 | The cluster-vs-variant concept, SPDI 0-based convention and representation table are correct. Live defects: resolve_merge_chain raises KeyError because merged_snapshot_data is an object ({"merged_into": ["429358"]}), not a list (SKILL.md and example); vcf_to_canonical_spdi returns None for valid input because it reads data["spdi"] while the endpoint returns seq_id/position/... directly, and the SKILL.md map covers only chr1 and chr17; alfa_frequency returns None because ALFA counts are not in the RefSNP JSON (they come from /refsnp/{id}/frequency); the example's alleles_grch38 reads seq_id_traits_by_assembly at the wrong level and always returns []. |
| Reliability | 6/12 | Headline function crashes on the live schema; other failures return None silently. |
| Performance context | 7/8 | 336 lines, mostly load-bearing. |
| Agent usability | 12/16 | Failure-mode prose is good; the code does not match the live API responses. |
| Human usability | 7/8 | Natural prompts. |
| Security | 9/12 | Public API; no key guidance. |
| Maintainability | 6/12 | Four live-API mismatches across SKILL.md and example; no tests. |
| Agent specific | 16/20 | Clear routing to myvariant/clinvar/gnomad Skills. |

Shipped-means-present (gate 8): SKILL.md references no local files; usage-guide.md and examples/dbsnp_lookup.py exist. PASS.

Research scope (gate 7): Identifier normalization; no individual-level content. PASS.

## Summary Table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 31 | 44 | 75 | 2/4 | yes | ✅ |
| 2 | Variant A | 20 | 25 | 45 | 1/4 | yes | ❌ |
| 3 | Edge | 31 | 44 | 75 | 3/4 | yes | ✅ |
| 4 | Variant B | 27 | 38 | 65 | 2/4 | yes | ⚠️ |
| 5 | Stress | 24 | 33 | 57 | 1/4 | yes | ⚠️ |

**Execution Average: 63.4 / 100** · **Assertion Pass Rate: 9/20 (45 %)** · Layer 1 avg 26.6 · Layer 2 avg 36.8

Research Veto: scientific integrity PASS; practice boundaries PASS; methodological ground PASS; code usability PASS.  
**Final: 70 × 0.4 + 63.4 × 0.6 = 28.0 + 38.0 = 66 → ⚠️ Beta Only**

## Detailed Outputs

### Input 1 — Canonical: Resolve rs429358
**Prompt:** "Resolve rs429358 (APOE): GRCh38 coordinates, alleles, gene and merge history."

**Executed:** yes — runs/run_all.py in1 (Windows venv, live API).

Code (`runs/skill_code.py`):
```python
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
... (47 more lines in skill_code.py)
```
Code (`runs/run_all.py :: in1()`):
```python
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
```
Printed (`runs/in1/out.txt`, trimmed):
```
SKILL.md summarize_refsnp(rs429358): {
 "rsid": "429358",
 "gene": "APOE",
 "placements_grch38": [
  {
   "ref": "T",
   "alt": "T",
   "seq_id": "NC_000019.10",
   "pos_0based": 44908683
  },
  {
   "ref": "T",
   "alt": "C",
   "seq_id": "NC_000019.10",
   "pos_0based": 44908683
  }
 ],
 "is_multiallelic": false,
 "merge_history": []
}
placement top-level keys: ['alleles', 'is_ptlp', 'placement_annot', 'seq_id'] | placement_annot keys: ['is_aln_opposite_orientation', 'is_mismatch', 'mol_type', 'seq_id_traits_by_assembly', 'seq_type']
dbsnp1_merges: [{'merged_rsid': '630496', 'revision': '85', 'merge_date': '2000-09-19T13:56Z'}, {'merged_rsid': '61228756', 'revision': '130', 'merge_date': '2008-05-26T20:59Z'}]
== shipped example __main__ ==
rs429358 (APOE e4): status=resolved, chain_length=1
GRCh38 alleles: []
BRCA1 chr17:43094464:G>A canonical SPDI: None
  -> rsID: None
```

**Output (agent answer, Mode A):** rs429358 = NC_000019.10:g.44908684T>C (SPDI NC_000019.10:44908683:T:C), APOE, biallelic. It absorbed rs630496 and rs61228756 (read from dbsnp1_merges, since the Skill's merge_history field is empty for current records).

**Scores:** Basic 31/40 | Specialized 44/60 | Total 75/100 · **Assertions 2/4**
- [PASS] Coordinates and alleles correct — T>C at 44908683 (0-based)
- [PASS] Gene annotation correct — APOE
- [FAIL] Merge history reported by the Skill code — reads merged_snapshot_data; dbsnp1_merges ignored
- [FAIL] Example demo produces meaningful output — alleles [] and SPDI None

### Input 2 — Variant A: Trace a merged rsID
**Prompt:** "A 2004 paper cites rs630496 -- trace it to the current rsID."

**Executed:** yes — runs/run_all.py in2.

Code (`runs/run_all.py :: in2()`):
```python
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
```
Printed (`runs/in2/out.txt`, trimmed):
```
HTTP 200 top-level keys: ['citations', 'create_date', 'dbsnp1_merges', 'last_update_build_id', 'last_update_date', 'lost_obs_movements', 'mane_select_ids', 'merged_snapshot_data', 'present_obs_movements', 'refsnp_id']
merged_snapshot_data: {"proxy_time": "2000-09-19T13:56Z", "proxy_build_id": "85", "merged_into": ["429358"]}
SKILL.md resolve_merge_chain(rs630496) RAISED KeyError: KeyError(0)
example resolve_merge_chain(rs630496) RAISED KeyError: KeyError(0)
SKILL.md resolve_merge_chain(rs429358) (current id): {'status': 'resolved', 'final_rsid': '429358', 'chain': ['429358']}
```

**Output (agent answer, Mode A):** The Skill's function crashed; reading the raw record by hand shows rs630496 was merged into rs429358 (build 85, 2000-09-19). Gave that answer with the fix: take merged_snapshot_data["merged_into"][0] and loop.

**Scores:** Basic 20/40 | Specialized 25/60 | Total 45/100 · **Assertions 1/4**
- [FAIL] Skill code resolves rs630496 to rs429358 — KeyError
- [FAIL] Code matches the live merge schema — object, not list
- [PASS] Merge model (follow merged_into) is conceptually right — raw record confirms
- [FAIL] No uncaught exception — KeyError: 0

### Input 3 — Edge: Multi-allelic and nonexistent rsIDs
**Prompt:** "Is rs334 multi-allelic, and what happens with a withdrawn or nonexistent rsID?"

**Executed:** yes — runs/run_all.py in3.

Code (`runs/run_all.py :: in3()`):
```python
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
```
Printed (`runs/in3/out.txt`, trimmed):
```
SKILL.md summarize_refsnp(rs334): alleles [('T', 'T'), ('T', 'A'), ('T', 'C'), ('T', 'G')] is_multiallelic = True
example alleles_grch38(rs334): []
example batch_normalize_rsids multi-allelic rule (len>1 and >1 distinct REF) -> False
SKILL.md summarize_refsnp(rs6025): alleles [('C', 'C'), ('C', 'A'), ('C', 'G'), ('C', 'T')] is_multiallelic = True
rs1 HTTP 404 ['error']
   SKILL resolve_merge_chain -> {'error': 'not found', 'final_rsid': '1', 'chain': ['1']}
rs999999999999 HTTP 404 ['error']
   SKILL resolve_merge_chain -> {'error': 'not found', 'final_rsid': '999999999999', 'chain': ['999999999999']}
rs2 HTTP 404 ['error']
   SKILL resolve_merge_chain -> {'error': 'not found', 'final_rsid': '2', 'chain': ['2']}
```

**Output (agent answer, Mode A):** rs334 is a multi-allelic cluster (T>A, T>C, T>G); only T>A is HbS, so joins must match the allele, not the rsID. Nonexistent ids return HTTP 404, which the Skill's code reports as "not found"; a withdrawn id would carry is_withdrawn (not tested live).

**Scores:** Basic 31/40 | Specialized 44/60 | Total 75/100 · **Assertions 3/4**
- [PASS] SKILL.md multi-allelic detection correct — rs334, rs6025 True
- [FAIL] Example multi-allelic detection correct — always [] / False
- [PASS] Nonexistent ids return a structured not-found — 404 handled
- [PASS] Warns that an rsID is a cluster needing allele matching — stated

### Input 4 — Variant B: VCF to canonical SPDI and rsID
**Prompt:** "Convert APOE chr19:44908684 T>C and BRCA1 chr17:43106487 A>C (VCF, GRCh38) to canonical SPDI and rsIDs."

**Executed:** yes — runs/run_all.py in4 (raw endpoint probed alongside).

Code (`runs/run_all.py :: in4()`):
```python
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
```
Printed (`runs/in4/out.txt`, trimmed):
```
19:44908684 T>C  SKILL vcf_to_canonical_spdi -> None | example -> None
   raw canonical_representative HTTP 200: {"data":{"seq_id":"NC_000019.10","position":44908683,"deleted_sequence":"T","inserted_sequence":"C"}}
   (the SKILL/example read data["spdi"], but the payload fields are ['deleted_sequence', 'inserted_sequence', 'position', 'seq_id'] )
   GET /spdi/{spdi}/rsids HTTP 200 {"data":{"rsids":[429358]}}
   SKILL spdi_to_rsid(dict-as-str) -> 429358
   SKILL spdi_to_rsid(str) -> 429358
17:43106487 A>C  SKILL vcf_to_canonical_spdi -> None | example -> None
   raw canonical_representative HTTP 200: {"data":{"seq_id":"NC_000017.11","position":43106486,"deleted_sequence":"A","inserted_sequence":"C"}}
   (the SKILL/example read data["spdi"], but the payload fields are ['deleted_sequence', 'inserted_sequence', 'position', 'seq_id'] )
   GET /spdi/{spdi}/rsids HTTP 200 {"data":{"rsids":[28897672]}}
   SKILL spdi_to_rsid(dict-as-str) -> 28897672
   SKILL spdi_to_rsid(str) -> 28897672
17:43094464 G>A  SKILL vcf_to_canonical_spdi -> None | example -> None
   raw canonical_representative HTTP 200: {"data":{"seq_id":"NC_000017.11","position":43094463,"deleted_sequence":"T","inserted_sequence":"A","warnings":[{"reason":"Other","message":"Disambiguation exception: The refe...
   (the SKILL/example read data["spdi"], but the payload fields are ['deleted_sequence', 'inserted_sequence', 'position', 'seq_id', 'warnings'] )
   GET /spdi/{spdi}/rsids HTTP 200 {"data":{"rsids":[1799950]}}
   SKILL spdi_to_rsid(dict-as-str) -> 1799950
   SKILL spdi_to_rsid(str) -> 1799950
SKILL hgvs_to_spdi_canonical(NC_000019.10:g.44908684T>C) -> {'seq_id': 'NC_000019.10', 'position': 44908683, 'deleted_sequence': 'T', 'inserted_sequence': 'C'}
SKILL hgvs_to_spdi_canonical(NM_000059.3:c.5946delT) -> {'seq_id': 'NM_000059.3', 'position': 6172, 'deleted_sequence': 'T', 'inserted_sequence': ''}
```

**Output (agent answer, Mode A):** APOE: NC_000019.10:44908683:T:C -> rs429358; BRCA1: NC_000017.11:43106486:A:C -> rs28897672. Built the SPDI strings from the raw canonical_representative response after the Skill's function returned None.

**Scores:** Basic 27/40 | Specialized 38/60 | Total 65/100 · **Assertions 2/4**
- [FAIL] Canonical SPDI returned by the Skill code — reads a non-existent data["spdi"]
- [FAIL] SKILL.md RefSeq map covers the input chromosomes — chr1/chr17 only
- [PASS] spdi_to_rsid works — 429358, 28897672
- [PASS] 1-based to 0-based conversion correct — pos-1

### Input 5 — Stress: Five-rsID normalization table with ALFA
**Prompt:** "For rs6025, rs1799963, rs429358, rs7412 and rs121913529: current rsID, multi-allelic flag, ALFA total frequency, gnomAD AF and ClinVar significance in one table."

**Executed:** yes — runs/run_all.py in5 (Variation Services + myvariant.info).

Code (`runs/run_all.py :: in5()`):
```python
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
```
Printed (`runs/in5/out.txt`, trimmed):
```
SKILL alfa_frequency(rs6025): None
frequency study_names in refsnp JSON: ['1000Genomes_30X', 'GnomAD_exomes', 'GnomAD_genomes', 'HapMap', 'KOREAN', 'PAGE_STUDY', 'TOPMED', 'dbGaP_PopFreq'] | any ALFA: False
example alfa_population_frequencies(rs6025): {}
GET /refsnp/6025/frequency HTTP 200 {"build_id": "20260205170148", "results": {"1@169549810": {"ref": "C", "counts": {"PRJNA507278": {"allele_counts": {"SAMN10492705": {"T": 11177, "C": 461073}, "SAMN10492695": {"T": ...
 input_rsid canonical_rsid   status  chain_length  is_multiallelic  n_alleles  gnomad_exome_af  gnomad_genome_af clinvar_sig
     rs6025           6025 resolved             1            False          0              NaN               NaN        None
     rs6025           6025 resolved             1            False          0         0.980410          0.982740        None
  rs1799963        1799963 resolved             1            False          0              NaN          0.008441        None
   rs429358         429358 resolved             1            False          0         0.138498          0.164436        None
     rs7412           7412 resolved             1            False          0         0.061504          0.082685        None
rs121913529      121913529 resolved             1            False          0         0.000000               NaN        None
rs121913529      121913529 resolved             1            False          0         0.000004               NaN        None
rs121913529      121913529 resolved             1            False          0         0.000000               NaN        None
```

**Output (agent answer, Mode A):** Built the table by hand: all five rsIDs are current; rs6025 and rs121913529 are multi-allelic clusters (the example reports False); gnomAD AFs from myvariant are gnomAD 2.1.1 values; ALFA totals must come from /refsnp/{id}/frequency (project PRJNA507278), which the Skill does not use; ClinVar significance must be read from clinvar.rcv.

**Scores:** Basic 24/40 | Specialized 33/60 | Total 57/100 · **Assertions 1/4**
- [FAIL] ALFA frequency returned — None
- [FAIL] Table flags multi-allelic sites — False everywhere
- [PASS] gnomAD AF populated — values present
- [FAIL] ClinVar significance populated — None

## Key strengths
- The rsID-is-a-cluster principle and SPDI/HGVS coordinate conventions are correct and important
- hgvs_to_spdi_canonical and spdi_to_rsid work against the live API

## Recommendations
- **[P1] resolve_merge_chain crashes on the live schema** (inputs [2]) — merged_snapshot_data is an object with merged_into; merged[0] raises KeyError in SKILL.md and the example. *Root cause:* Code written against an assumed list schema. *Fix:* Read `payload["merged_snapshot_data"]["merged_into"][0]` and loop; add a test on rs630496 -> rs429358.
- **[P1] vcf_to_canonical_spdi reads a non-existent key** (inputs [4]) — Returns None for valid variants; SKILL.md map covers only chr1 and chr17. *Root cause:* Response shape not checked. *Fix:* Build the SPDI from data.seq_id/position/deleted_sequence/inserted_sequence and use the full RefSeq map from the example.
- **[P1] ALFA frequencies are not in RefSNP JSON** (inputs [5]) — alfa_frequency always returns None. *Root cause:* ALFA lives at /refsnp/{id}/frequency. *Fix:* Query /variation/v0/refsnp/{id}/frequency and map ALFA BioSample ids to population names.
- **[P2] Example allele parser and batch table are wrong** (inputs [1, 3, 5]) — alleles_grch38 always returns [], so multi-allelic flags are False; batch rows duplicate and clinvar_sig is None. *Root cause:* Reads seq_id_traits_by_assembly at the wrong level; wrong myvariant field. *Fix:* Read placement_annot.seq_id_traits_by_assembly; use clinvar.rcv.clinical_significance; collapse duplicate hits.
- **[P2] Report dbsnp1_merges as merge history** (inputs [1]) — merge_history is empty for current records that absorbed others. *Root cause:* Only merged_snapshot_data is read. *Fix:* Include dbsnp1_merges.
