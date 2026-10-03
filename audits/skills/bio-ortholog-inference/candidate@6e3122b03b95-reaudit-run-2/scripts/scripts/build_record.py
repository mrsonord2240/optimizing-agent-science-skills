"""Build source-identity.json and report.json for the bio-ortholog-inference final re-audit (run 2)."""
import hashlib
import json
import os
import sys

sys.dont_write_bytecode = True
CAND = 'F:/OpenScience/wt/dbaccess-ortholog-inference/skills/bio-ortholog-inference'
RUN = 'F:/OpenScience/audits/bio-ortholog-inference/reaudit-run-2'
PREV = ('F:/optimizing-agent-science-skills/audits/skills/bio-ortholog-inference/'
        'candidate@aa32b5158669-reaudit-run/source-identity.json')
IDENT = '6e3122b03b95f6b9666a03f538ff5e07657ad733c2f0b9a2c7f1de1749993bbb'

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
        'content_sha256': IDENT,
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
assert ident['candidate']['content_manifest'] == {'file_count': 7, 'bytes': 35212}
with open(f'{RUN}/source-identity.json', 'w', encoding='utf-8', newline='\n') as f:
    json.dump(ident, f, indent=2, ensure_ascii=False)
    f.write('\n')


def A(t, r, n):
    return {'text': t, 'result': r, 'note': n}


def inp(i, typ, label, status, note, basic, spec, assertions):
    p = sum(a['result'] == 'PASS' for a in assertions)
    return {'index': i, 'type': typ, 'label': label, 'status': status, 'status_flag': '\u2705', 'note': note,
            'basic': basic, 'specialized': spec, 'total': basic + spec, 'assertions_passed': p,
            'assertions_total': len(assertions), 'assertions': assertions}


inputs = [
    inp(1, 'Canonical', 'Ensembl Compara single gene, MARCH1 rename, five-gene zebrafish batch with per-symbol status (compara_orthologs.py, final bytes)',
        'COMPLETED', 'Exit 0. The example prints each symbol outcome and flags a partial batch. Live Ensembl was slow: MDM2 request failed after 4 x 45 s read timeouts and BRCA1 zebrafish returned no rows; both reported and flagged PARTIAL BATCH (a pass for OI-10).', 35, 53, [
            A('BRCA1 human to mouse returns ortholog_one2one ENSMUSG00000017146 with level and identity', 'PASS', 'Euarchontoglires, identity 57.6711%.'),
            A('MARCH1 returns HTTP 400 and the example reports the rename; MARCHF1 resolves to ENSG00000145416', 'PASS', 'Both printed.'),
            A('TP53 and ATM zebrafish 1:1 calls are correct', 'PASS', 'ENSDARG00000035559 and ENSDARG00000002385.'),
            A('Rows carry taxonomy_level and no confidence value', 'PASS', 'confidence column empty in every row; docs and example say so.'),
            A('batch_compara returns one row per input symbol with status found / no ortholog returned / request failed, and the example surfaces failed and empty symbols', 'PASS', 'Local stub: all three statuses and a fixed 11-column set; an all-failed batch keeps the type column. Live example: per-symbol outcome lines for MDM2 (request failed with message) and BRCA1 (no ortholog returned) plus the PARTIAL BATCH flag.')]),
    inp(2, 'Variant A', 'Cross-resource TP53: Compara, OMA 1:1, OrthoDB verified group (cross_resource.py, unchanged file)', 'COMPLETED',
        'Exit 0. OMA (130 1:1, P53_MOUSE) and OrthoDB (4289813at2759, Trp53) legs returned; the Compara leg hit a 45 s read timeout this run and was reported UNAVAILABLE without aborting the others. Compara TP53 to ENSMUSG00000059552 was confirmed in the live batch_compara run on the same bytes.', 35, 52, [
            A('Compara TP53 human to mouse returns ENSMUSG00000059552', 'PASS', 'live_notagene run: TP53 found, ENSMUSG00000059552, 77.9487%, ortholog_one2one.'),
            A('OMA TP53 P04637 rel_type=1:1 contains P53_MOUSE', 'PASS', '130 1:1 orthologs; mouse P53_MOUSE.'),
            A('OrthoDB leg selects the exact-name group and verifies the human member', 'PASS', '4289813at2759, mouse members 22059 and Trp53.'),
            A('The TIGAR-ranked first hit for query TP53 is rejected', 'PASS', 'orthodb_group_has_gene False for the top groups (run_reaudit).'),
            A('Each leg is isolated so one outage cannot abort the others', 'PASS', 'Demonstrated live: Compara timed out, OMA and OrthoDB legs still ran, exit 0.')]),
    inp(3, 'Variant B', 'KEGG Orthology gene to KO to members (kegg_orthology.py, unchanged)', 'COMPLETED',
        'Exit 0; K04451, 548 members across 446 species.', 36, 54, [
            A('hsa:7157 maps to K04451', 'PASS', 'Single KO.'),
            A('KO record lists TP53 and pathway entries', 'PASS', 'map04115 p53 signaling pathway present.'),
            A('Member count and species count are consistent', 'PASS', '548 members, 446 species.'),
            A('Output is TSV-parsed plain text, not JSON', 'PASS', 'No JSON parse path used.')]),
    inp(4, 'Edge', 'Client retry/timeout guards on the changed module (local HTTP stub), OrthoDB null parser, batch status schema', 'COMPLETED',
        'Whole-module sweep rerun on the new bytes: get_with_retry and the OrthoDB parser behave as before; batch schema verified.', 36, 52, [
            A('503, 503 then 200 succeeds on the third attempt', 'PASS', 'Stub hit count 3.'),
            A('429 with Retry-After is retried', 'PASS', 'Stub hit count 2.'),
            A('Persistent 500 raises RequestException after max_retries; unreachable host raises RequestException', 'PASS', '4 stub hits then RequestException; refused connection raised.'),
            A('404 raises HTTPError unless allow_404=True', 'PASS', 'Both paths.'),
            A('orthodb_orthologs returns [] for a group with no member at the level and Trp53 for the p53 group at mouse', 'PASS', '[] and 22059/Trp53.')]),
    inp(5, 'Stress', 'Documented routes and claims: homology/id with species, OrthoDB search and tab, PANTHER, OMA empty, HomoloGene, eggNOG note, unknown-symbol status', 'COMPLETED',
        'All documented claims reproduce. An unknown symbol (NOTAGENE123) is labelled request failed with the HTTP 400 text in the error column; judged a minor labelling imprecision (P2).', 35, 51, [
            A('OrthoDB /search is full text: TP53 ranks phosphoglycerate mutase first, tumor protein p53 reaches 4289813at2759', 'PASS', 'As documented.'),
            A('OrthoDB /tab uses id= (TSV) and query= returns 404', 'PASS', 'TSV with header; 404.'),
            A('PANTHER matchortho P04637 returns mouse Tp53', 'PASS', 'target Tp53, version 19.'),
            A('OMA BRCA1 P38398 returns an empty 200 and the HOG route resolves for P04637', 'PASS', '[] and HOG:F0782425.2c.7a.'),
            A('HomoloGene efetch is retired', 'PASS', 'efetch db=homologene returns an error body.'),
            A('SKILL.md route /homology/id/<species>/<ensembl_gene_id> works as written', 'PASS', 'curl: /homology/id/human/ENSG00000141510 200; the species-less form 404 and is no longer documented. Tree sweep: no other occurrence.')]),
]
avg = round(sum(i['total'] for i in inputs) / len(inputs), 1)
passed = sum(i['assertions_passed'] for i in inputs)
total = sum(i['assertions_total'] for i in inputs)
cats = {
    'functional_suitability': (11, 12, 'Compara, OrthoDB, OMA and KEGG helpers return correct live values; the route is fixed and batch_compara reports every symbol. An unknown symbol is labelled request failed.'),
    'reliability': (11, 12, 'Retry helper and per-symbol batch status reproduced on a local stub and live; the example flags a partial batch.'),
    'performance_context': (6, 8, 'SKILL.md is about 190 lines; the decision matrix, per-resource reference and common-errors table partly repeat each other.'),
    'agent_usability': (14, 16, 'Decision matrix, OrthoDB full-text trap and group verification are clear; the SKILL.md batch snippet filters on type and would drop failed symbols silently, and the three statuses are documented only in the docstring and example.'),
    'human_usability': (8, 8, 'Clear tables; the eggNOG note now states the 403 and the TLS failure and keeps the unverified label.'),
    'security': (11, 12, 'No credentials, HTTPS, read-only public APIs; loopback stub only.'),
    'maintainability': (9, 12, 'Single client module; still no automated tests.'),
    'agent_specific': (16, 20, 'Specific trigger description, clear defection to de novo tools; PANTHER and eggNOG are documented but not wrapped.'),
}
sub = sum(v[0] for v in cats.values())
sw = round(sub * 0.4, 1)
dw = round(avg * 0.6, 1)
score = round(sw + dw)
l1 = round(sum(i['basic'] for i in inputs) / 5, 1)
l2 = round(sum(i['specialized'] for i in inputs) / 5, 1)
grade = 'Production Ready' if score >= 85 else 'Limited Release' if score >= 75 else 'Beta Only' if score >= 60 else 'Reject'
sym = {'Production Ready': '\u2b50', 'Limited Release': '\u2705', 'Beta Only': '\u26a0\ufe0f', 'Reject': '\u274c'}[grade]
report = {
    'meta': {'skill_name': 'bio-ortholog-inference',
             'description': 'Pull pre-computed ortholog calls from OrthoDB, Ensembl Compara, OMA, KEGG Orthology and documented PANTHER/eggNOG routes through a small Python requests client, with guidance on confidence semantics and when to defect to de novo inference.',
             'evaluated_on': '2026-10-03', 'category': 'Data Analysis', 'execution_mode': 'D', 'complexity': 'Moderate',
             'evaluator_version': 'skill-auditor@1.0', 'n_inputs': 5,
             'performed_by': 'Independent final re-auditor agent, lane 2 (not the fixer, tooler or prior auditor)', 'auditor_independent': True},
    'veto_gates': {
        'skill_veto': {'gate': 'PASS', 'stability': 'PASS', 'contract': 'PASS', 'determinism': 'PASS', 'security': 'PASS'},
        'research_veto': {
            'applicable': True, 'gate': 'PASS',
            'scientific_integrity': {'result': 'PASS', 'detail': 'Live values match the services: TP53 mouse ENSMUSG00000059552 / Trp53, MARCHF1 ENSG00000145416, KEGG K04451 with 548 members. No fabricated confidence values.'},
            'practice_boundaries': {'result': 'PASS', 'detail': 'Database retrieval only; no diagnostic or prescriptive output.'},
            'methodological_ground': {'result': 'PASS', 'detail': 'Resource semantics are not conflated; OrthoDB group verification and 1:1 filtering are sound; a partial batch is now flagged.'},
            'code_usability': {'result': 'PASS', 'detail': 'All three examples exit 0 on the final bytes; remaining items are doc and labelling P2s.'}}},
    'static_score': {'subtotal': sub, 'max': 100,
                     'categories': {k: {'score': v[0], 'max': v[1], 'note': v[2]} for k, v in cats.items()}},
    'dynamic_score': {'execution_avg': avg, 'max': 100,
                      'assertion_pass_rate': {'passed': passed, 'total': total}, 'inputs': inputs},
    'final': {'static_weighted': sw, 'dynamic_weighted': dw, 'score': score, 'max': 100,
              'grade': grade, 'grade_symbol': sym, 'deployable': score >= 75, 'veto_override': False},
    'key_strengths': [
        'OI-09, OI-10 and the eggNOG note are fixed and verified; OI-01 to OI-08 did not regress (whole-module stub, OrthoDB, OMA, KEGG and PANTHER reruns on the new bytes).',
        'batch_compara returns one row per input symbol with a status and a fixed column set; the example reports partial batches, shown live under Ensembl read timeouts.',
        'Retry and error behaviour reproduced on a local stub; Compara, OMA, OrthoDB and KEGG return consistent TP53 calls.'],
    'recommendations': [
        {'priority': 'P2', 'title': 'OI-11 Batch statuses undocumented in SKILL.md; snippet drops failed symbols',
         'observed_in': [1],
         'problem': 'The three batch_compara statuses appear only in the docstring and example. The SKILL.md snippet filters on type == ortholog_one2one, so a user copying it would lose failed and empty symbols silently, the gap OI-10 closed in the example.',
         'root_cause': 'The status column was added to the client and example but not to the SKILL.md snippet or prose.',
         'fix': 'Add one sentence naming the statuses and a status check (or a count of non-found symbols) to the SKILL.md snippet.'},
        {'priority': 'P2', 'title': 'OI-12 Unknown symbol reported as request failed',
         'observed_in': [5],
         'problem': 'batch_compara(["TP53","NOTAGENE123"]) labels NOTAGENE123 request failed (HTTP 400 text in the error column); Ensembl returns 400 for an unrecognised symbol. A user may read it as a transient outage and retry.',
         'root_cause': 'All requests.RequestException classes share one status.',
         'fix': 'Document that a 400 in the error column means an unknown or renamed symbol (resolve_symbol first), or give 4xx its own status such as symbol not found.'}],
}
with open(f'{RUN}/report.json', 'w', encoding='utf-8', newline='\n') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)
    f.write('\n')
print('static', sub, 'avg', avg, 'L1', l1, 'L2', l2, 'assert', passed, total, 'final', sw + dw, score, grade)
