"""Builds report.json and source-identity.json for the bio-ortholog-inference initial audit."""
import hashlib
import json
import os
import sys

sys.dont_write_bytecode = True
RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SK = r'F:\OpenScience\wt\dbaccess-ortholog-inference\skills\bio-ortholog-inference'
EXPECTED = 'f6d4ccc5903d157167ae1106f009ecf5d36a0e1d3c56c8a691e63625fcc2e9ac'

files = []
for d, _, fs in os.walk(SK):
    for f in fs:
        p = os.path.join(d, f)
        rel = os.path.relpath(p, SK).replace('\\', '/')
        b = open(p, 'rb').read()
        files.append({'path': rel, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()})
files.sort(key=lambda x: x['path'])
manifest = '\n'.join(f"{x['path']}\t{x['bytes']}\t{x['sha256']}" for x in files)
ident = hashlib.sha256(manifest.encode()).hexdigest()
assert ident == EXPECTED, ident

src = {
    'origin': {
        'repository': 'GPTomics/bioSkills',
        'commit': 'd91ed3d563019e649dc854c56ccd62551359488a',
        'path': 'database-access/ortholog-inference',
        'subtree': '97db68da2fc40ebf988b217031d6b2ff648ea105',
        'checkout': r'F:\optimizing-agent-science-skills\external\GPTomics__bioSkills',
        'status': 'clean',
        'files': [
            {'path': 'SKILL.md', 'git_blob': '5dee814103e6f7bf330a6e356b0043604ae87366'},
            {'path': 'examples/compara_orthologs.py', 'git_blob': '57d2830e08957bacfef98a0713612f3d1bc587a5'},
            {'path': 'examples/cross_resource.py', 'git_blob': 'c6645470547ea18c96ddd99d8a6d7137d5507f72'},
            {'path': 'examples/kegg_orthology.py', 'git_blob': '2147e27d2a933672368c00610e738afc30c158f4'},
            {'path': 'usage-guide.md', 'git_blob': '83fee094004e9208d6854c3751b38f58f1b3fa03'},
        ],
        'normalization_note': 'The audited tree adds scripts/ortholog_clients.py (externalized client code) and edited SKILL.md and examples; origin identifies the source Skill subtree, not a one-to-one file mapping.',
    },
    'candidate': {
        'branch': 'fix/dbaccess-ortholog-inference',
        'commit': '2f38178',
        'path': SK,
        'status_before': 'untracked Skill subtree only',
        'status_after_execution': 'untracked Skill subtree only; candidate files unchanged',
        'content_sha256': ident,
        'content_manifest': {
            'file_count': len(files),
            'bytes': sum(x['bytes'] for x in files),
            'recipe': 'relative POSIX path, byte count, and lowercase SHA-256 separated by TAB; records sorted with StringComparer.Ordinal and separated by LF; no trailing LF',
            'manifest_bytes': len(manifest),
        },
        'files': files,
    },
    'tooling': {
        'tools_md': r'F:\OpenScience\audits\bio-ortholog-inference\TOOLS.md',
        'tools_md_sha256': 'aff688a83acb6cd82f5dd2ce453d1ea617a0a225b428bcf3714cd9d417cec21a',
        'rubric_zip_sha256': 'e54e9ff8b0c3677abcfe657ad6ed92ba34dbdb8ad205c7157ad881f25afcf0de',
        'environment': 'database-access venv (native Windows, F:\\OpenScience\\audit-envs\\database-access) py3.12.13 | requests 2.34.2 pandas 3.0.5 numpy 2.5.3 networkx 3.7 | pip-freeze sha256 5fdd1350df2cf397; live public REST queries, no staged inputs',
    },
    'candidate_cache_artifacts_after_execution': [],
}
json.dump(src, open(os.path.join(RUN, 'source-identity.json'), 'w', encoding='utf-8'), indent=2)


def A(t, ok, n):
    return {'text': t, 'result': 'PASS' if ok else 'FAIL', 'note': n}


def inp(i, typ, label, status, flag, note, b, s, asserts):
    p = sum(a['result'] == 'PASS' for a in asserts)
    return {'index': i, 'type': typ, 'label': label, 'status': status, 'status_flag': flag, 'note': note,
            'basic': b, 'specialized': s, 'total': b + s, 'assertions_passed': p, 'assertions_total': len(asserts),
            'assertions': asserts}


inputs = [
    inp(1, 'Canonical', 'Ensembl Compara TP53 human->mouse, MARCH1 rename, 4-symbol zebrafish batch', 'PARTIAL', '\u26a0\ufe0f',
        'Compara values are correct (TP53 -> ENSMUSG00000059552 one2one, 77.9/77.4 pct identity; bad symbol becomes an error row) but confidence is always None and examples/compara_orthologs.py hung past 200 s twice and hit HTTP 500 once with no client timeout.',
        30, 44,
        [A('TP53 human->mouse Compara call returns the single one2one ortholog ENSMUSG00000059552 with identities', True, 'Matches the raw Ensembl record; the reverse Trp53 call returns ENSG00000141510.'),
         A('MARCH1 is rejected and MARCHF1 resolves to an Ensembl gene ID', True, 'MARCH1 gives HTTP 400; MARCHF1 resolves to ENSG00000145416.'),
         A('batch_compara returns typed rows and an error row for the invalid symbol', True, '4 rows: 2 one2many, 1 one2one, 1 error row; zebrafish tp53 is ENSDARG00000035559.'),
         A('Compara confidence is present as the documented 0/1 value', False, 'Raw homology records have no confidence key (keys: dn_ds, method_link_type, source, target, taxonomy_level, type); every call yields None.'),
         A('examples/compara_orthologs.py completes (exit 0) within a bounded time in this session', False, 'Two timeouts at 200-280 s (no request timeout in the client) and one HTTP 500; it passed in the tooling phase when Ensembl was healthy.')]),
    inp(2, 'Variant A', 'Cross-resource TP53/BRCA1 consensus: OrthoDB + OMA + Compara via shipped client and examples/cross_resource.py', 'PARTIAL', '\u274c',
        'orthodb_orthologs returns only None ids or raises TypeError, the TP53 symbol search ranks TIGAR and ubiquitin groups first, and an OMA 502 crashes cross_resource.py.',
        20, 22,
        [A('orthodb_groups returns group IDs for a symbol query', True, '100 IDs returned for TP53 and BRCA1.'),
         A('orthodb_orthologs returns mouse gene identifiers for a group', False, 'Returned six None values for a populated group (ids sit at data[].genes[].gene_id.id) and raised TypeError on data:null for 4 of 5 TP53 groups.'),
         A('The first group returned for symbol TP53 is a TP53/p53 ortholog group', False, 'First hits: 4837993at2759 phosphoglycerate mutase (TIGAR), then TP53-target gene 3; a p53 group is 4289813at2759; the BRCA1 first hit is Ubiquitin.'),
         A('OMA documented endpoint yields the mouse TP53 ortholog when the service answers', True, 'Raw GET /protein/P04637/orthologs/ gave 157 orthologs including P53_MOUSE; the same URL returned 502 on other attempts, and BRCA1 P38398 returns 200 with an empty list.'),
         A('examples/cross_resource.py completes with usable output for all three resources', False, 'Exit 1 with an uncaught HTTPError 502 from OMA after the Compara section; no per-resource isolation.')]),
    inp(3, 'Variant B', 'KEGG Orthology: gene -> KO -> members -> KO record', 'COMPLETED', '\u2705',
        'KEGG mapping, member listing and KO record are correct; an unknown gene returns an empty list.',
        36, 50,
        [A('hsa:7157 and mmu:22059 both map to K04451', True, 'Both return [K04451] (TP53/P53).'),
         A('genes_for_ko lists members across species including human and mouse TP53', True, '548 members across 446 species including hsa:7157 and mmu:22059.'),
         A('ko_info returns the KO entry with symbol and pathways', True, 'Entry K04451, SYMBOL TP53, P53; pathway list present.'),
         A('examples/kegg_orthology.py exits 0 and prints KO, pathways and member counts', True, 'Exit 0; 548 members, 446 species; an unknown gene id yields [] rather than a crash.')]),
]
avg = round(sum(i['total'] for i in inputs) / len(inputs), 1)

cats = [
    ('functional_suitability', 8, 12, 'Compara and KEGG work; documented Compara confidence, OrthoDB symbol-search semantics, orthodb_orthologs and the /tab endpoint no longer hold.'),
    ('reliability', 5, 12, 'No request timeouts, no retry on 5xx, only HTTPError handled; live runs hung or crashed on Ensembl 500/hang and OMA 502.'),
    ('performance_context', 6, 8, 'SKILL.md is about 180 lines, acceptable, but the per-resource API reference could be routed to references/.'),
    ('agent_usability', 12, 16, 'Clear description, decision matrix and failure modes; unverified or transient surfaces are labelled, but the client does not implement the retry the Skill advises.'),
    ('human_usability', 6, 8, 'usage-guide prompts are clear; the filter-confidence=1 prompt cannot be satisfied.'),
    ('security', 11, 12, 'Public read-only GET clients, no credentials or code execution; symbols are interpolated into URLs without validation.'),
    ('maintainability', 9, 12, 'Single client module with docstrings; no Skill-root LICENSE although frontmatter declares MIT; the oma_orthologs docstring key taxonId does not match the live schema.'),
    ('agent_specific', 15, 20, 'Good trigger precision and boundary versus de novo inference; some claims (PANTHER evidence codes, confidence 0/1) are asserted without a verified surface.'),
]
sub = sum(c[1] for c in cats)
sw, dw = round(sub * 0.4, 1), round(avg * 0.6, 1)
score = round(sw + dw)


def R(pr, t, obs, pb, rc, fx):
    return {'priority': pr, 'title': t, 'observed_in': obs, 'problem': pb, 'root_cause': rc, 'fix': fx}


recs = [
    R('P1', 'OI-01 orthodb_orthologs returns None ids or TypeError', [2],
      'On OrthoDB v12 /orthologs the data items are groups with nested genes[].gene_id.id, and data is null when the level has no members; the client returns a list of None or raises TypeError.',
      'Parser was written for a flat gene list and never executed against the live schema.',
      'Parse data null-safely as groups -> genes -> gene_id.id (plus description), return [] for null data, raise on non-200 instead of returning [], and run it live in an example.'),
    R('P1', 'OI-02 No timeouts or 5xx retry; hangs and crashes', [1, 2],
      'Ensembl homology calls hung beyond 200 s and returned HTTP 500, OMA returned 502; the client sets no timeout, retries only HTTP 429, and batch_compara catches only HTTPError.',
      'get_with_retry is used only by the Ensembl helpers and every other helper calls requests.get bare.',
      'Route all helpers through one session with a timeout, retry 5xx and connection errors with backoff (as the Common errors table advises for OMA 502), and catch requests.RequestException in batch_compara.'),
    R('P1', 'OI-03 Documented Compara confidence 0/1 never present', [1],
      'Live Compara homology JSON has no confidence field, so confidence is always None while SKILL.md, the usage-guide prompt (filter confidence=1) and the compara_one2one docstring promise high-confidence calls.',
      'The claim predates the current Ensembl response schema.',
      'Verify against the live API and replace the semantics row, docstrings and the confidence=1 prompt with what is actually returned (type, taxonomy_level, identities), or document the real quality signal if one exists.'),
    R('P1', 'OI-04 OrthoDB symbol search is free text; example takes first hit', [2],
      'OrthoDB /search matches descriptions: TP53 returns phosphoglycerate mutase (TIGAR) and TP53-target groups first and BRCA1 returns Ubiquitin; cross_resource.py uses groups[0] and would present another gene family as the ortholog group.',
      'The Skill describes /search as a gene-symbol lookup and the example does not verify the group.',
      'Document that /search is full text, verify the group by name or member gene symbol before use, and fix the example accordingly.'),
    R('P1', 'OI-05 cross_resource.py lacks per-resource error isolation', [2],
      'A single OMA 502 aborts the example with a traceback, and the default BRCA1 OMA call returns 200 with an empty list so the OMA leg is empty even when the service is healthy.',
      'The example calls three services in sequence without try/except and uses an input OMA has no orthologs for.',
      'Wrap each resource in try/except that reports unavailable versus empty, and use an input with a verified OMA result (TP53 P04637 returns P53_MOUSE; rel_type=1:1 returned reliably).'),
    R('P2', 'OI-06 Documented OrthoDB /tab endpoint is dead', [],
      'GET /v12/tab?query=<og_id> returns 404 (api.tab function not found) although it is listed in the API reference.',
      'The endpoint list was not verified against v12.',
      'Remove or correct the /tab entry after checking the current OrthoDB v12 documentation.'),
    R('P2', 'OI-07 PANTHER evidence claim and no client function', [],
      'The confidence table credits PANTHER with evidence codes, but the live ortholog/matchortho response carries only an ortholog type (LDO) and no evidence field; only a base URL is documented and the client has no PANTHER function.',
      'PANTHER was documented without a verified call.',
      'Document the verified ortholog/matchortho route with its real fields (or drop the evidence-code claim) and state that the client does not wrap PANTHER.'),
    R('P2', 'OI-08 No Skill-root LICENSE; stale OMA docstring', [],
      'Preflight warns that the Skill has no LICENSE file though frontmatter declares MIT, and the oma_orthologs docstring lists taxonId while live items nest species.taxon_id.',
      'Normalization left provenance and docstring unreconciled.',
      'Add the upstream MIT LICENSE (or cite repository license evidence in the manifest) and correct the docstring keys.'),
]

rep = {
    'meta': {
        'skill_name': 'bio-ortholog-inference',
        'description': 'Pull pre-computed ortholog calls from public databases (OrthoDB, Ensembl Compara, OMA browser, eggNOG, PANTHER, KEGG Orthology, HomoloGene) via their REST APIs, with confidence semantics, 1:1 vs 1:many handling, and guidance on when to compute orthology de novo.',
        'evaluated_on': '2026-10-03',
        'evaluator_version': 'skill-auditor@1.0',
        'category': 'Data Analysis',
        'execution_mode': 'B',
        'complexity': 'Moderate',
        'n_inputs': 3,
    },
    'veto_gates': {
        'skill_veto': {'gate': 'PASS', 'stability': 'PASS', 'contract': 'PASS', 'determinism': 'PASS', 'security': 'PASS'},
        'research_veto': {
            'applicable': True,
            'gate': 'PASS',
            'scientific_integrity': {'result': 'PASS', 'detail': 'No fabricated identifiers; every returned value that was checked matches the upstream records.'},
            'practice_boundaries': {'result': 'PASS', 'detail': 'Database-query Skill with no clinical conclusions.'},
            'methodological_ground': {'result': 'PASS', 'detail': 'The orthology conjecture and cross-resource disagreement are caveated; the OrthoDB first-hit hazard is filed as OI-04 rather than a method fallacy.'},
            'code_usability': {'result': 'PASS', 'detail': 'The client imports and runs; Compara, KEGG and OMA paths work when upstream answers; orthodb_orthologs is a logic defect (OI-01) and robustness gaps are OI-02.'},
        },
    },
    'static_score': {
        'subtotal': sub,
        'max': 100,
        'categories': {k: {'score': s, 'max': m, 'note': n} for k, s, m, n in cats},
    },
    'dynamic_score': {
        'execution_avg': avg,
        'max': 100,
        'assertion_pass_rate': {'passed': sum(i['assertions_passed'] for i in inputs), 'total': sum(i['assertions_total'] for i in inputs)},
        'inputs': inputs,
    },
    'final': {
        'static_weighted': sw,
        'dynamic_weighted': dw,
        'score': score,
        'max': 100,
        'grade': 'Beta Only',
        'grade_symbol': '\u26a0\ufe0f',
        'deployable': False,
        'veto_override': False,
    },
    'key_strengths': [
        'Compara resolve, ortholog and batch paths return correct values (TP53 one2one with identities) and the MARCH1 rename hazard is demonstrated and handled.',
        'The KEGG Orthology workflow is correct end to end and its example runs cleanly.',
        'Unverified or retired surfaces (eggNOG API, HomoloGene) are labelled honestly and matched live observations.',
        'Clear decision matrix, confidence-semantics caveats and a documented boundary with de novo inference.',
    ],
    'recommendations': recs,
}
assert sub == sum(c['score'] for c in rep['static_score']['categories'].values())
json.dump(rep, open(os.path.join(RUN, 'report.json'), 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
print('static', sub, 'exec', avg, 'weights', sw, dw, 'score', score,
      'assert', rep['dynamic_score']['assertion_pass_rate'], [i['total'] for i in inputs],
      sum(i['basic'] for i in inputs) / 3, sum(i['specialized'] for i in inputs) / 3)
