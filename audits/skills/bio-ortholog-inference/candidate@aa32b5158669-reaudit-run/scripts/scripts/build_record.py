"""Build source-identity.json and report.json for the bio-ortholog-inference final re-audit."""
import hashlib
import json
import os
import sys

sys.dont_write_bytecode = True
CAND = 'F:/OpenScience/wt/dbaccess-ortholog-inference/skills/bio-ortholog-inference'
RUN = 'F:/OpenScience/audits/bio-ortholog-inference/reaudit-run'
PREV = ('F:/optimizing-agent-science-skills/audits/skills/bio-ortholog-inference/'
        'candidate@f6d4ccc5903d-initial-audit-run/source-identity.json')

files = []
for root, _, names in os.walk(CAND):
    for n in names:
        p = os.path.join(root, n)
        data = open(p, 'rb').read()
        files.append({'path': os.path.relpath(p, CAND).replace(os.sep, '/'), 'bytes': len(data),
                      'sha256': hashlib.sha256(data).hexdigest()})
files.sort(key=lambda f: f['path'])
prev = json.load(open(PREV, encoding='utf-8'))
ident = {
    'origin': prev['origin'],
    'candidate': {
        'branch': 'fix/dbaccess-ortholog-inference',
        'commit': prev['candidate']['commit'],
        'path': 'F:\\OpenScience\\wt\\dbaccess-ortholog-inference\\skills\\bio-ortholog-inference',
        'content_sha256': 'aa32b51586699da5ed4708ce63e6cbc9eb19751ed79f94b5ff5d73208e252495',
        'identity_kind': 'sha256-manifest-v1',
        'status_after_execution': 'untracked Skill subtree only; candidate files unchanged',
        'content_manifest': {'file_count': len(files), 'bytes': sum(f['bytes'] for f in files)},
    },
    'files': files,
    'tooling': {
        'tools_md': 'F:\\OpenScience\\audits\\bio-ortholog-inference\\TOOLS.md',
        'rubric_zip_sha256': prev['tooling']['rubric_zip_sha256'],
        'environment': prev['tooling']['environment'],
        'preflight_warn': [],
    },
    'candidate_cache_artifacts_after_execution': [],
}
assert ident['candidate']['content_manifest'] == {'file_count': 7, 'bytes': 34073}
with open(f'{RUN}/source-identity.json', 'w', encoding='utf-8', newline='\n') as f:
    json.dump(ident, f, indent=2, ensure_ascii=False)
    f.write('\n')


def A(t, r, n):
    return {'text': t, 'result': r, 'note': n}


def inp(i, typ, label, status, note, basic, spec, assertions):
    p = sum(a['result'] == 'PASS' for a in assertions)
    total = basic + spec
    flag = '✅' if status == 'COMPLETED' and total >= 75 else ('⚠️' if status == 'COMPLETED' else '❌')
    return {'index': i, 'type': typ, 'label': label, 'status': status, 'status_flag': flag, 'note': note,
            'basic': basic, 'specialized': spec, 'total': total, 'assertions_passed': p,
            'assertions_total': len(assertions), 'assertions': assertions}


inputs = [
    inp(1, 'Canonical', 'Ensembl Compara single gene, MARCH1 rename, five-gene zebrafish batch (compara_orthologs.py, final bytes)',
        'COMPLETED', 'Exit 0 on the first attempt on the final bytes. The batch table is correct for what returned but silently omits MDM2 (read timeout) and BRCA1 (no rows).', 33, 48, [
            A('BRCA1 human to mouse returns ortholog_one2one ENSMUSG00000017146 with level and identity', 'PASS', 'Euarchontoglires, identity 57.67%.'),
            A('MARCH1 returns HTTP 400 and the example reports the rename; MARCHF1 resolves to ENSG00000145416', 'PASS', 'Both printed.'),
            A('TP53 and ATM zebrafish 1:1 calls are correct', 'PASS', 'ENSDARG00000035559 and ENSDARG00000002385.'),
            A('Rows carry taxonomy_level and no confidence value', 'PASS', 'confidence None in every row; docs and example say so.'),
            A('The example output surfaces batch symbols that failed or returned nothing', 'FAIL', 'batch_compara put MDM2 in an error column (read timeout) and BRCA1 returned no rows; the example prints neither and reports 1:1 calls: 2 as if complete.')]),
    inp(2, 'Variant A', 'Cross-resource TP53: Compara, OMA 1:1, OrthoDB verified group (cross_resource.py)', 'COMPLETED',
        'All three legs returned and agree on mouse Trp53 / P53_MOUSE / ENSMUSG00000059552.', 35, 52, [
            A('Compara TP53 human to mouse returns ENSMUSG00000059552', 'PASS', '1 hit.'),
            A('OMA TP53 P04637 rel_type=1:1 contains P53_MOUSE', 'PASS', '130 1:1 orthologs; mouse P53_MOUSE.'),
            A('OrthoDB leg selects the exact-name group and verifies the human member', 'PASS', '4289813at2759, mouse members 22059 and Trp53.'),
            A('The TIGAR-ranked first hit for query TP53 is rejected', 'PASS', 'orthodb_group_has_gene False for both top groups.'),
            A('Each leg is isolated so one outage cannot abort the others', 'PASS', 'run() wrapper per leg; client raises RequestException on exhausted retries (stub test); live legs all succeeded.')]),
    inp(3, 'Variant B', 'KEGG Orthology gene to KO to members (kegg_orthology.py)', 'COMPLETED',
        'Exit 0; K04451, 548 members across 446 species.', 36, 54, [
            A('hsa:7157 maps to K04451', 'PASS', 'Single KO.'),
            A('KO record lists TP53 and pathway entries', 'PASS', 'ENTRY K04451, SYMBOL TP53, P53; p53 signaling pathway present.'),
            A('Member count and species count are consistent', 'PASS', '548 members, 446 species.'),
            A('Output is TSV-parsed plain text, not JSON', 'PASS', 'No JSON parse path used.')]),
    inp(4, 'Edge', 'Client retry, timeout and parser guards (local HTTP stub, OrthoDB null data)', 'COMPLETED',
        'get_with_retry and the OrthoDB parser behave as documented.', 36, 52, [
            A('503, 503 then 200 succeeds on the third attempt', 'PASS', 'Stub hit count 3.'),
            A('429 with Retry-After is retried', 'PASS', 'Stub hit count 2.'),
            A('Persistent 500 raises RequestException after max_retries; unreachable host raises RequestException', 'PASS', '4 stub hits then RequestException; refused connection raised.'),
            A('404 raises HTTPError unless allow_404=True', 'PASS', 'Both paths.'),
            A('orthodb_orthologs returns [] for a group with no member at the level and Trp53 for the p53 group at mouse', 'PASS', 'Yeast level returned []; mouse returned 22059 and Trp53.')]),
    inp(5, 'Stress', 'Documented routes and claims: OrthoDB search and tab, PANTHER, OMA empty, HomoloGene, Compara homology/id, eggNOG', 'COMPLETED',
        'All corrected claims reproduce except the documented Compara /homology/id route.', 33, 48, [
            A('OrthoDB /search is full text: TP53 ranks phosphoglycerate mutase first, tumor protein p53 reaches 4289813at2759', 'PASS', 'As documented.'),
            A('OrthoDB /tab uses id= (TSV) and query= returns 404', 'PASS', 'TSV with header; 404.'),
            A('PANTHER matchortho P04637 returns mouse Tp53 with ortholog type LDO', 'PASS', 'target Tp53, version 19.'),
            A('OMA BRCA1 P38398 returns an empty 200 and the HOG route resolves for P04637', 'PASS', '[] and HOG:F0782425.2c.7a.'),
            A('HomoloGene efetch is retired', 'PASS', 'efetch db=homologene returns an error body.'),
            A('SKILL.md route /homology/id/<ensembl_gene_id> works as written', 'FAIL', '404 (page not found) without the species segment on two independent clients; /homology/id/human/<id> returns 200.')]),
]
avg = round(sum(i['total'] for i in inputs) / len(inputs), 1)
passed = sum(i['assertions_passed'] for i in inputs)
total = sum(i['assertions_total'] for i in inputs)
cats = {
    'functional_suitability': (10, 12, 'Compara, OrthoDB, OMA and KEGG helpers return correct live values; one documented Compara route (/homology/id without species) is wrong and the batch example hides failed symbols.'),
    'reliability': (10, 12, 'One retry helper with timeout, 429/5xx handling and RequestException on exhaustion reproduced on a local stub and live; batch_compara records errors but the example does not display them.'),
    'performance_context': (6, 8, 'SKILL.md is about 190 lines; the decision matrix, per-resource reference and common-errors table partly repeat each other.'),
    'agent_usability': (13, 16, 'Decision matrix, OrthoDB full-text trap and group verification are clear; one wrong route in the Compara section and silent batch gaps in the example.'),
    'human_usability': (7, 8, 'Clear tables; eggNOG note says redirect to eggnogdb.org but eggnog6.embl.de now fails TLS verification (still labelled unverified).'),
    'security': (11, 12, 'No credentials, HTTPS (stub test used loopback only); read-only public APIs.'),
    'maintainability': (9, 12, 'Single client module; no automated tests, which is how the batch-display and route gaps survived.'),
    'agent_specific': (16, 20, 'Specific trigger description, clear defection to de novo tools; PANTHER and eggNOG are documented but not wrapped.'),
}
sub = sum(v[0] for v in cats.values())
sw = round(sub * 0.4, 1)
dw = round(avg * 0.6, 1)
score = round(sw + dw)
l1 = round(sum(i['basic'] for i in inputs) / 5, 1)
l2 = round(sum(i['specialized'] for i in inputs) / 5, 1)
grade = 'Production Ready' if score >= 85 else 'Limited Release' if score >= 75 else 'Beta Only' if score >= 60 else 'Reject'
sym = {'Production Ready': '⭐', 'Limited Release': '✅', 'Beta Only': '⚠️', 'Reject': '❌'}[grade]
report = {
    'meta': {'skill_name': 'bio-ortholog-inference',
             'description': 'Pull pre-computed ortholog calls from OrthoDB, Ensembl Compara, OMA, KEGG Orthology and documented PANTHER/eggNOG routes through a small Python requests client, with guidance on confidence semantics and when to defect to de novo inference.',
             'evaluated_on': '2026-10-03', 'category': 'Data Analysis', 'execution_mode': 'D', 'complexity': 'Moderate',
             'evaluator_version': 'skill-auditor@1.0', 'n_inputs': 5,
             'performed_by': 'Independent re-auditor agent (not the fixer)', 'auditor_independent': True},
    'veto_gates': {
        'skill_veto': {'gate': 'PASS', 'stability': 'PASS', 'contract': 'PASS', 'determinism': 'PASS', 'security': 'PASS'},
        'research_veto': {
            'applicable': True, 'gate': 'PASS',
            'scientific_integrity': {'result': 'PASS', 'detail': 'Live values match the services: TP53 mouse ENSMUSG00000059552 / P53_MOUSE / Trp53, MARCHF1 ENSG00000145416, KEGG K04451 with 548 members. No fabricated confidence values remain.'},
            'practice_boundaries': {'result': 'PASS', 'detail': 'Database retrieval only; no diagnostic or prescriptive output.'},
            'methodological_ground': {'result': 'PASS', 'detail': 'Resource semantics are not conflated; OrthoDB group verification and 1:1 filtering are sound.'},
            'code_usability': {'result': 'PASS', 'detail': 'All three examples ran to exit 0 on the final bytes; shortcomings are display and doc accuracy, filed as P2.'}}},
    'static_score': {'subtotal': sub, 'max': 100,
                     'categories': {k: {'score': v[0], 'max': v[1], 'note': v[2]} for k, v in cats.items()}},
    'dynamic_score': {'execution_avg': avg, 'max': 100,
                      'assertion_pass_rate': {'passed': passed, 'total': total}, 'inputs': inputs},
    'final': {'static_weighted': sw, 'dynamic_weighted': dw, 'score': score, 'max': 100,
              'grade': grade, 'grade_symbol': sym, 'deployable': score >= 75, 'veto_override': False},
    'key_strengths': [
        'The eight initial findings are fixed: null-safe OrthoDB parser, one retrying client, no phantom confidence, verified OrthoDB group selection, isolated cross-resource legs, corrected /tab and PANTHER notes, licence.',
        'Retry and error behaviour was reproduced independently on a local stub (503 then 200, 429 Retry-After, persistent 500, 404, refused connection).',
        'Compara, OMA, OrthoDB and KEGG all returned scientifically consistent TP53 calls in the cross-resource example.'],
    'recommendations': [
        {'priority': 'P2', 'title': 'OI-09 SKILL.md homology/id route needs a species', 'observed_in': [5],
         'problem': 'The Compara section lists /homology/id/<ensembl_gene_id>, which returns 404; the working route is /homology/id/<species>/<id>.',
         'root_cause': 'Route copied without a live check; the sibling ensembl-rest Skill fixed the same row.',
         'fix': 'Write /homology/id/<species>/<ensembl_gene_id> in SKILL.md.'},
        {'priority': 'P2', 'title': 'OI-10 Batch example hides failed and empty symbols', 'observed_in': [1],
         'problem': 'compara_orthologs.py prints only the 1:1 rows and a count; MDM2 (read timeout, in the error column) and BRCA1 (no rows) are invisible, so 1:1 calls: 2 reads as a complete answer for five genes.',
         'root_cause': 'The example never prints the error column or the symbols without calls that batch_compara returns.',
         'fix': 'Print symbols with an error (with the message) and symbols with no rows after the table.'},
        {'priority': 'P2', 'title': 'eggNOG redirect note is stale', 'observed_in': [],
         'problem': 'SKILL.md says eggnog6.embl.de/api redirects to eggnogdb.org/api; today the old host fails TLS verification and eggnogdb.org/api returns 403.',
         'root_cause': 'Service moved after the note was written.',
         'fix': 'State both failure modes or only that scripted access is refused.'}],
}
with open(f'{RUN}/report.json', 'w', encoding='utf-8', newline='\n') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)
    f.write('\n')
print('static', sub, 'avg', avg, 'L1', l1, 'L2', l2, 'assert', passed, total, 'final', sw + dw, score, grade)
