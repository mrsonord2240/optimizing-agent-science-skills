import hashlib, json, os, sys
sys.dont_write_bytecode = True
C = 'F:/OpenScience/wt/dbaccess-interaction-databases/skills/bio-interaction-databases'
RUN = 'F:/OpenScience/audits/bio-interaction-databases/reaudit-run'
files = []
for root, _, names in os.walk(C):
    for n in names:
        p = os.path.join(root, n)
        rel = os.path.relpath(p, C).replace(os.sep, '/')
        b = open(p, 'rb').read()
        files.append((rel, len(b), hashlib.sha256(b).hexdigest()))
files.sort(key=lambda x: x[0].encode('utf-8'))
manifest = '\n'.join(f'{r}\t{n}\t{h}' for r, n, h in files)
ident = hashlib.sha256(manifest.encode('utf-8')).hexdigest()
assert ident == '7430509d403cde092a4c2e1d02a12f7bc00c7183597ebfaafa3335254b02c5f5', ident
total = sum(n for _, n, _ in files)
si = {
  'origin': {'repository': 'GPTomics/bioSkills', 'commit': 'd91ed3d563019e649dc854c56ccd62551359488a',
             'path': 'database-access/interaction-databases', 'subtree': '249aaeefc35d2b75f343c8539fa076adb8f12c17',
             'checkout': 'F:\\optimizing-agent-science-skills\\external\\GPTomics__bioSkills'},
  'candidate': {'branch': 'fix/dbaccess-interaction-databases', 'commit': '2f381782596c6569fe5a8357556856512b7fbb6c',
                'path': 'F:\\OpenScience\\wt\\dbaccess-interaction-databases\\skills\\bio-interaction-databases',
                'content_sha256': ident, 'identity_kind': 'sha256-manifest-v1',
                'status_after_execution': '?? skills/bio-interaction-databases/ (untracked, uncommitted by design)',
                'content_manifest': {'file_count': len(files), 'bytes': total}},
  'files': [{'path': r, 'bytes': n, 'sha256': h} for r, n, h in files],
  'prior_audited_identity': '588996fc143fb0dc98a5558fce2db091e0905415fb9a80a8c4bc49419690be42',
  'tooling': {'rubric_zip_sha256': 'e54e9ff8b0c3677abcfe657ad6ed92ba34dbdb8ad205c7157ad881f25afcf0de',
              'environment': 'database-access-venv py3.12.13 | requests 2.34.2 pandas 3.0.5 numpy 2.5.3 networkx 3.7 | pip-freeze sha256 5fdd1350df2cf397',
              'preflight': 'skill_preflight.py --offline PASS before and after'},
  'candidate_cache_artifacts_after_execution': [],
}
with open(RUN + '/source-identity.json', 'w', encoding='utf-8', newline='\n') as f:
    json.dump(si, f, indent=2, ensure_ascii=False)
    f.write('\n')


def A(t, ok, n):
    return {'text': t, 'result': 'PASS' if ok else 'FAIL', 'note': n}


def inp(i, typ, label, status, note, b, s, ass):
    flag = '\u2705' if status == 'COMPLETED' and b + s >= 75 else ('\u26a0\ufe0f' if status == 'COMPLETED' else '\u274c')
    return {'index': i, 'type': typ, 'label': label, 'status': status, 'status_flag': flag, 'note': note,
            'basic': b, 'specialized': s, 'total': b + s,
            'assertions_passed': sum(a['result'] == 'PASS' for a in ass), 'assertions_total': len(ass), 'assertions': ass}


inputs = [
 inp(1, 'Canonical', 'STRING ID resolution, confidence tiers, channels, physical network, hubs (examples/string_network.py)', 'COMPLETED',
     'Exit 0 on the final bytes; queryIndex IDs map back to the input order; 45/35/23 edges at 400/700/900; physical 22 edges subset of functional 35; hubs MDM2, TP53, CDKN1A (degree 9).', 35, 53, [
   A('Example exits 0 and resolves all 10 symbols with queryIndex matching input order', True, 'All 10 rows map back (checked programmatically)'),
   A('Edge count is monotonic in threshold', True, '45 >= 35 >= 23'),
   A('Physical network is a nonempty strict subset of the functional network', True, '22 of 35, zero edges outside the functional set'),
   A('SKILL.md claim that 5 of 26 escore>0.4 edges are absent from the physical network holds', True, 'Reproduced exactly (26, 5)'),
   A('Scores are 0-1 and STRING calls are paced at least 1 s apart', True, 'Two back-to-back calls took 1.66 s')]),
 inp(2, 'Variant A', 'STRING + OmniPath + SIGNOR directed graph with provenance (examples/interaction_query.py)', 'COMPLETED',
     'Exit 0 on the final bytes; 26 STRING, 20 OmniPath edges inside the query set, 163 SIGNOR records among the query genes; 55 directed edges; string_score 0.716-0.999 only on STRING edges.', 34, 52, [
   A('Example exits 0 and SIGNOR contributes signed edges', True, '22 signed edges; MDM2 down-regulates TP53 by ubiquitination'),
   A('CSV has string_score (no max_score) and is empty for non-STRING edges', True, 'Zero STRING-less edges carry a score; 3 SIGNOR-only rows are empty'),
   A('ATM->TP53 edge carries three sources and a phosphorylation mechanism', True, 'OmniPath, SIGNOR, STRING; score 0.999'),
   A('Directed graph keeps direction and does not collapse to undirected', True, 'DiGraph, STRING added in both directions'),
   A('Signed effect values are the SIGNOR free text, not an invented vocabulary', True, 'e.g. up-regulates quantity by stabilization')]),
 inp(3, 'Variant B', 'BioGRID LT physical interactions with the registered key; key-leak retest with real and fake keys', 'COMPLETED',
     'TP53 3081 rows / 831 pairs as documented; fake keys raise "HTTP 401 Unauthorized" with no URL, key or chained exception; connection failure and a real-key HTTP 404 produce no URL or key in message or Skill-frame traceback.', 36, 54, [
   A('Real key returns the documented 3081 per-experiment rows for 831 pairs', True, 'Exact match'),
   A('Only low-throughput physical systems are kept', True, '11 systems, all in PHYSICAL_LT_SYSTEMS'),
   A('Fake and empty keys raise a clean 401 without URL or key', True, 'Two fake keys and one empty key'),
   A('No chained exception or traceback text contains the URL or key (connection error and real-key 404)', True, 'Skill frames and message scanned'),
   A('Documented 401 behaviour matches the live service', True, 'HTTP 401 Unauthorized')]),
 inp(4, 'Edge', 'SIGNOR signed, directed records for TP53 and AKT1 (signor_for_gene)', 'COMPLETED',
     'Client returns 333 TP53 rows identical to the raw 29-column response (field multiset equal); ATM->TP53 phosphorylation Ser15/Ser20, MDM2->TP53 ubiquitination down-regulation; AKT1 456 rows; "No result found." warns. A short non-empty unparseable answer returns an empty frame with no warning (IDM-011).', 34, 51, [
   A('Client rows equal the raw endpoint rows and fields map to the documented columns', True, '333 rows, multiset of 8 mapped columns equal'),
   A('Known biology is present with correct direction and mechanism', True, 'ATM->TP53 phosphorylation (10 records), MDM2->TP53 ubiquitination down-regulates (3)'),
   A('Unknown protein warns and returns a typed empty frame', True, 'P00000 -> 0 rows, one warning'),
   A('Unknown gene symbol raises a clear ValueError', True, 'uniprot_accession ZZZNOTAGENE9'),
   A('A non-empty unparseable SIGNOR answer is reported rather than returned as a silent empty result', False, 'Simulated junk text gives 0 rows and 0 warnings; one transient one-line raw answer was seen once and not reproduced in 12 later calls (IDM-011)')]),
 inp(5, 'Stress', 'License-aware OmniPath query for a commercial pipeline (license=commercial)', 'COMPLETED',
     'Server license parameter still does not filter (344 = 344 rows); the client screen keeps 343 rows, matching an independent row-level expectation; 30 surviving sources all carry OmniPath purpose commercial; PhosphoSite, HPRD, iPTMnet, ELM and others removed; references filtered by prefix. Screen is source-level only and says so.', 34, 51, [
   A('Server license parameter is still a no-op (premise of the client screen)', True, '344 rows with and without license=commercial'),
   A('No source with a non-commercial purpose remains after the screen', True, '30 surviving sources all commercial'),
   A('Row count equals an independently computed expectation', True, '343 = 343'),
   A('Academic mode keeps PhosphoSite; invalid license value raises', True, 'Both observed'),
   A('Documentation states the screen is source-level and does not replace per-resource terms', True, 'SKILL.md, usage-guide.md and docstring all say so')]),
 inp(6, 'Stress', 'aggregate_networks / summary / multi_source_edges on TP53+MDM2 with BioGRID', 'COMPLETED',
     'TP53-MDM2 edge carries STRING, OmniPath and BioGRID-LT-physical with string_score 0.999; nodes stay inside the query set. BioGRID self-interactions enter as self-loops, so summary reports 2 nodes, 3 edges, density 3.0 and mean degree 3.0 (IDM-010).', 31, 47, [
   A('Nodes are restricted to the query set (IDM-006)', True, 'TP53, MDM2 only; also 3-gene set without BioGRID'),
   A('Three-source edge carries string_score in 0-1 and no max_score (IDM-005)', True, '0.999'),
   A('string_score is None exactly for edges without STRING', True, 'Checked on a 3-gene set'),
   A('multi_source_edges returns only the multi-resource edge', True, '1 edge'),
   A('summary() returns plausible network statistics', False, 'Density 3.0 for 2 nodes because homodimer self-loops are counted (IDM-010)')]),
 inp(7, 'Variant A', 'STRING physical versus functional claim, caller_identity and version-pinned host', 'COMPLETED',
     'TP53-MDM2 edge 0.999 with a custom caller_identity; physical network is a strict subset; the escore warning in SKILL.md is quantitatively reproduced; version-pinned host answers.', 36, 54, [
   A('Custom caller_identity is accepted and returns the expected edge', True, '0.999'),
   A('Physical network claim in SKILL.md reproduced on 10 DNA-damage genes', True, '5 of 26 escore>0.4 edges absent from physical'),
   A('Pinned version-12-5 host answers', True, 'All STRING calls succeeded'),
   A('Requests carry a timeout', True, 'TIMEOUT 60 s in the shared helper'),
   A('Combined score stays 0-1 for functional and physical outputs', True, 'Both checked')]),
]
n = len(inputs)
avg = round(sum(i['total'] for i in inputs) / n, 1)
st = {'functional_suitability': (11, 12, 'All advertised client functions and both examples run and return scientifically correct live data; SIGNOR and the commercial screen now work. Self-loop edges distort summary statistics (IDM-010).'),
      'reliability': (9, 12, 'Timeouts, STRING pacing, sanitised errors and an empty-answer warning are in place; a non-empty unparseable SIGNOR answer is a silent empty frame (IDM-011).'),
      'performance_context': (6, 8, 'SKILL.md is about 200 lines with prose for resources that ship no client (Reactome, HuRI, HuMAP) but the surfaces are labelled as documentation.'),
      'agent_usability': (14, 16, 'Decision matrix, channel semantics, failure-mode and common-error tables are accurate and now match live behaviour.'),
      'human_usability': (7, 8, 'Docs state what each client does and does not filter; remaining prose about non-executable resources is clearly informational.'),
      'security': (11, 12, 'Key-bearing URLs and chained exceptions are removed from errors (tested with real and fake keys); the commercial screen is disclosed as source-level only.'),
      'maintainability': (10, 12, 'One authoritative client with a shared request helper, upstream MIT LICENSE shipped and cited; examples exercise the client.'),
      'agent_specific': (16, 20, 'Rich trigger description and version compatibility section; some non-executed resources are described without recipes.')}
sub = sum(v[0] for v in st.values())
sw = round(sub * 0.4, 1)
dw = round(avg * 0.6, 1)
score = round(sw + dw)
rep = {
 'meta': {'skill_name': 'bio-interaction-databases',
          'description': 'Query protein-protein and gene interaction databases (STRING, BioGRID, IntAct, SIGNOR, OmniPath and others) through a small Python client; decision matrix, STRING channel semantics, license constraints and multi-resource aggregation.',
          'evaluated_on': '2026-10-03', 'category': 'Data Analysis', 'execution_mode': 'D', 'complexity': 'Moderate',
          'evaluator_version': 'skill-auditor@1.0', 'n_inputs': n},
 'veto_gates': {'skill_veto': {'gate': 'PASS', 'stability': 'PASS', 'contract': 'PASS', 'determinism': 'PASS', 'security': 'PASS'},
   'research_veto': {'applicable': True, 'gate': 'PASS',
     'scientific_integrity': {'result': 'PASS', 'detail': 'All reproduced values (STRING TP53-MDM2 0.999, BioGRID TP53 3081 rows / 831 pairs, SIGNOR TP53 333 records, OmniPath 344 / 343 rows) matched live services and the documented claims.'},
     'practice_boundaries': {'result': 'PASS', 'detail': 'Interaction retrieval only; license limits are stated and the commercial screen is disclosed as a source-level aid, not legal clearance.'},
     'methodological_ground': {'result': 'PASS', 'detail': 'Physical versus functional, signed versus undirected and throughput guidance are correct and verified; escore is no longer presented as a physical filter.'},
     'code_usability': {'result': 'PASS', 'detail': 'Every client function and both examples ran on the exact final bytes; the two remaining defects are P2 (IDM-010, IDM-011).'}}},
 'static_score': {'subtotal': sub, 'max': 100, 'categories': {k: {'score': v[0], 'max': v[1], 'note': v[2]} for k, v in st.items()}},
 'dynamic_score': {'execution_avg': avg, 'max': 100,
   'assertion_pass_rate': {'passed': sum(i['assertions_passed'] for i in inputs), 'total': sum(i['assertions_total'] for i in inputs)},
   'inputs': inputs},
 'final': {'static_weighted': sw, 'dynamic_weighted': dw, 'score': score, 'max': 100,
           'grade': 'Production Ready' if score >= 85 else 'Limited Release', 'grade_symbol': '\u2b50' if score >= 85 else '\u2705',
           'deployable': score >= 75, 'veto_override': False},
 'key_strengths': [
   'All nine initial findings (two P0, two P1, five P2) reproduce as fixed on the exact final bytes against live services.',
   'SIGNOR now returns 333 TP53 records identical to the raw 29-column response, with known ATM and MDM2 biology and a warning on empty answers.',
   'The BioGRID access key no longer reaches error text, traceback frames or chained exceptions (real and fake key tests).',
   'Claims in the documentation were checked quantitatively (5 of 26 escore edges not physical, 3081 rows for 831 pairs, 344 vs 343 OmniPath rows) and hold.'],
 'recommendations': [
   {'priority': 'P2', 'title': 'IDM-010 BioGRID self-loops distort summary()', 'observed_in': [6],
    'problem': 'aggregate_networks admits BioGRID homodimer rows as self-loops, so summary() reports 2 nodes, 3 edges and density 3.0 for TP53+MDM2.',
    'root_cause': 'The query-set restriction accepts gene_a == gene_b and summary uses networkx density, which counts self-loops.',
    'fix': 'Skip or separately flag gene_a == gene_b rows in aggregate_networks (or exclude self-loops in summary()) and state the choice in SKILL.md.'},
   {'priority': 'P2', 'title': 'IDM-011 Unparseable SIGNOR answer returns silent empty frame', 'observed_in': [4],
    'problem': 'Any non-empty SIGNOR response other than "No result found." that has no 28-column rows yields an empty DataFrame with no warning; one transient one-line raw answer was observed once.',
    'root_cause': 'The parser skips short lines silently and only the exact empty message warns.',
    'fix': 'Warn or raise when a non-empty answer yields zero parsed rows, mirroring the empty-answer warning.'}],
}
with open(RUN + '/report.json', 'w', encoding='utf-8', newline='\n') as f:
    json.dump(rep, f, indent=2, ensure_ascii=False)
    f.write('\n')
print('static', sub, 'exec', avg, 'final', sw, dw, score, rep['final']['grade'],
      'L1', sum(i['basic'] for i in inputs) / n, 'L2', sum(i['specialized'] for i in inputs) / n,
      'assert', rep['dynamic_score']['assertion_pass_rate'])
