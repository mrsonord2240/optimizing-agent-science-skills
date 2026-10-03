import hashlib, json, os, sys
sys.dont_write_bytecode = True
C = 'F:/OpenScience/wt/dbaccess-uniprot-access/skills/bio-uniprot-access'
RUN = 'F:/OpenScience/audits/bio-uniprot-access/reaudit-run'
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
assert ident == 'ea100b041cafcbf60a8d1202d6ca09387fff80515d37b45d5998162fb799bcb1', ident
total = sum(n for _, n, _ in files)
si = {
  'origin': {'repository': 'GPTomics/bioSkills', 'commit': 'd91ed3d563019e649dc854c56ccd62551359488a',
             'path': 'database-access/uniprot-access', 'subtree': '1c4d604cb066b2afd2435bade70b7381093d5a6a',
             'checkout': 'F:\\optimizing-agent-science-skills\\external\\GPTomics__bioSkills'},
  'candidate': {'branch': 'fix/dbaccess-uniprot-access', 'commit': '2f381782596c6569fe5a8357556856512b7fbb6c',
                'path': 'F:\\OpenScience\\wt\\dbaccess-uniprot-access\\skills\\bio-uniprot-access',
                'content_sha256': ident, 'identity_kind': 'sha256-manifest-v1',
                'status_after_execution': '?? skills/bio-uniprot-access/ (untracked, uncommitted by design)',
                'content_manifest': {'file_count': len(files), 'bytes': total}},
  'files': [{'path': r, 'bytes': n, 'sha256': h} for r, n, h in files],
  'prior_audited_identity': '7f82b9d5aae0ba064038b97d399123a2be4d845124d1d4cf13a0918dd4e48240',
  'tooling': {'rubric_zip_sha256': 'e54e9ff8b0c3677abcfe657ad6ed92ba34dbdb8ad205c7157ad881f25afcf0de',
              'environment': 'database-access-venv py3.12.13 | requests 2.34.2 pandas 3.0.5 numpy 2.5.3 networkx 3.7 | pip-freeze sha256 5fdd1350df2cf397',
              'service': 'UniProt release 2026_03 (X-UniProt-Release)',
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
 inp(1, 'Canonical', 'Entry parse, bulk search with total, stream, ID mapping (examples/uniprot_query.py)', 'COMPLETED',
     'Exit 0 on the final bytes: P04637 parsed (393 aa, 311 PDB, AlphaFold P04637); 500 of 625 kinases with a truncation warning; stream returned 20,431 human Swiss-Prot; Ensembl TP53/PTEN/BRCA2 mapped to P04637/P60484/P51587 with no NOT MAPPED lines.', 36, 54, [
   A('Example exits 0 and parses P04637 with correct accession, name, gene, length', True, 'P53_HUMAN, TP53, 393'),
   A('Search page reports N of total and warns on truncation', True, '500 of 625, one UserWarning'),
   A('Stream returns the complete set', True, 'stream_tsv kinase set 625 equals X-Total-Results'),
   A('ID mapping includes BRCA2 (previously dropped by first-page read)', True, 'All three genes mapped'),
   A('PDB count equals an independent cross-reference count', True, '311 = 311')]),
 inp(2, 'Variant A', 'Isoforms and cross-references (examples/isoforms_and_xrefs.py, list_isoforms, xref_summary)', 'COMPLETED',
     'Exit 0 on the final bytes: 9 P04637 isoforms with one canonical, P04637-2 FASTA header correct and sequence differs from canonical; xref PDB list equals entry pdb_ids (311); protein without isoform comment returns [].', 35, 52, [
   A('Example exits 0 and lists isoforms with ids as lists', True, '9 isoforms, exactly one canonical'),
   A('Isoform FASTA is the requested isoform, not the canonical sequence', True, 'sp|P04637-2|, sequence differs'),
   A('xref_summary matches the entry JSON', True, '311 PDB ids identical; Ensembl and AlphaFoldDB present'),
   A('Protein with no ALTERNATIVE PRODUCTS comment returns an empty list', True, 'P69905'),
   A('Example output is internally consistent', True, 'Cross-reference table sorted by count')]),
 inp(3, 'Variant B', 'ID mapping job handling: full stream, unmapped inputs, stuck and failed jobs, obsolete accessions', 'COMPLETED',
     'Client rows (44) equal an independent /idmapping/stream pull while the first results page would give 25; TP53 TrEMBL-inclusive count 18 matches SKILL.md; unmapped input is in failedIds and an all-unmapped batch returns empty results without crashing; stuck job raises TimeoutError and FAILED raises RuntimeError (stubbed status); Q15086 and P04637 both resolve to P04637.', 36, 54, [
   A('Client rows equal an independent stream pull and exceed the first page', True, '44 vs 25 on page one'),
   A('Unmapped inputs are reported in failedIds, including an all-unmapped batch', True, 'NOTANID1'),
   A('Swiss-Prot target returns the reviewed accessions', True, 'P04637, P60484, P51587'),
   A('Stuck job times out and FAILED job raises with the job id', True, 'Stubbed status responses'),
   A('resolve_obsolete maps a secondary accession to the primary', True, 'Q15086 -> P04637')]),
 inp(4, 'Variant A', 'Search syntax, field names and corpus-size claims in SKILL.md', 'COMPLETED',
     'database:pdb matches while xref:pdb matches 0; ft_act_site accepted and ft_active_site HTTP 400; corpus sizes 575,748 Swiss-Prot / 149,430,635 TrEMBL at release 2026_03 match the documented ~576K / ~149M; keyword text matches 640 vs 625 for KW-0418; a zero-hit search returns an empty frame.', 36, 54, [
   A('database:pdb returns hits and xref:pdb silently returns zero as documented', True, '>500 vs 0'),
   A('ft_act_site is accepted and ft_active_site is rejected as documented', True, 'HTTP 400 on the invalid name'),
   A('Documented corpus sizes match the live release', True, '575,748 / 149,430,635 at 2026_03'),
   A('Keyword id versus text claim holds', True, '640 vs 625'),
   A('Zero-result search returns an empty typed frame instead of crashing', True, 'Header-only TSV parsed')]),
 inp(5, 'Stress', 'Proteome download route (download_proteome) on E. coli and human', 'COMPLETED',
     'E. coli UP000000625: valid gzip with 4,403 records equal to the server count and the old /proteomes/{upid}.fasta.gz route returns 400 as documented. Human UP000005640: 147,520 records (20,416 reviewed + 127,104 TrEMBL), 37.8 MB gzip, 86.7 MB raw, while the example prints "~20 MB compressed; ~80 MB unpacked; ~20K proteins" and no text warns that the route returns TrEMBL entries too (UNI-010).', 31, 46, [
   A('Output is valid gzip FASTA and the record count equals the server count', True, 'E. coli 4,403 and human 147,520 both equal'),
   A('Documented old route failure (400) is real', True, '/proteomes/UP000000625.fasta.gz returns 400'),
   A('Route is the one the Skill documents and the function writes the named file', True, 'Both organisms'),
   A('Example output text on proteome size and protein count matches the real download', False, '~20 MB / ~20K proteins printed; real 37.8 MB / 147,520 entries (UNI-010)'),
   A('Human download count matches the server proteinCount', True, '147,520')]),
 inp(6, 'Edge', 'Entry edge cases, UniRef tiers and retry helper', 'COMPLETED',
     'Secondary accession redirects to primary; deleted accession raises ValueError with reason; malformed accession raises HTTPError after one call; TrEMBL entry and an entry without a gene name parse; UniRef50/90/100 identity and member counts match the server; 429/503 retried honouring Retry-After then exponential backoff, 404 not retried, persistent 503 and connection errors give up after 5 attempts.', 35, 53, [
   A('Inactive accession raises ValueError naming the reason; secondary redirects', True, 'DELETED reason; Q15086 -> P04637'),
   A('UniRef identity is the numeric tier and member counts match the server', True, '50, 90, 100'),
   A('Retry helper honours Retry-After, then backs off exponentially, with a 60 s timeout on every call', True, 'sleeps 3.0, 2; timeouts 60'),
   A('Client errors are not retried; persistent server errors stop after 5 attempts', True, '404 one call; 503 five calls'),
   A('Entries without a gene name or recommended name parse without KeyError', True, 'A0A0U2ZQU7 gene None')]),
]
n = len(inputs)
avg = round(sum(i['total'] for i in inputs) / n, 1)
st = {'functional_suitability': (11, 12, 'Every client function and both examples run and return correct live data; the proteome route works but returns all entries including TrEMBL, undocumented (UNI-010).'),
      'reliability': (10, 12, 'One request helper with timeout, bounded retries, Retry-After and a poll timeout; unmapped IDs and truncation are surfaced; stream_tsv buffers in memory (documented).'),
      'performance_context': (6, 8, 'SKILL.md is about 190 lines with endpoint and schema tables that are proportionate to the task.'),
      'agent_usability': (14, 16, 'Endpoint, query syntax, field-name and failure-mode tables are accurate against the live service and warn on the traps that previously failed.'),
      'human_usability': (7, 8, 'Clear tables and examples; the printed proteome size text is wrong (UNI-010).'),
      'security': (11, 12, 'No credentials, no destructive operations; downloads write only to the caller-named path.'),
      'maintainability': (10, 12, 'Single authoritative client used by both examples; upstream MIT LICENSE shipped; release and size claims dated to 2026_03.'),
      'agent_specific': (16, 20, 'Rich trigger description with the migration and stream-vs-search guidance; version compatibility records the release header.')}
sub = sum(v[0] for v in st.values())
sw = round(sub * 0.4, 1)
dw = round(avg * 0.6, 1)
score = round(sw + dw)
rep = {
 'meta': {'skill_name': 'bio-uniprot-access',
          'description': "Query UniProt's REST API (rest.uniprot.org) for protein entries, search and stream TSV, async ID mapping, isoforms, cross-references, UniRef clusters and proteome FASTA, with guidance on endpoint choice, query syntax and failure modes.",
          'evaluated_on': '2026-10-03', 'category': 'Data Analysis', 'execution_mode': 'D', 'complexity': 'Moderate',
          'evaluator_version': 'skill-auditor@1.0', 'n_inputs': n},
 'veto_gates': {'skill_veto': {'gate': 'PASS', 'stability': 'PASS', 'contract': 'PASS', 'determinism': 'PASS', 'security': 'PASS'},
   'research_veto': {'applicable': True, 'gate': 'PASS',
     'scientific_integrity': {'result': 'PASS', 'detail': 'All reproduced values (P04637 393 aa / 311 PDB, 44 mapping rows, 625 kinases, UniRef member counts, 4,403 E. coli and 147,520 human proteome records) matched independent raw API calls.'},
     'practice_boundaries': {'result': 'PASS', 'detail': 'Public sequence and annotation retrieval only; no clinical or prescriptive output.'},
     'methodological_ground': {'result': 'PASS', 'detail': 'Reviewed versus TrEMBL, stream versus search, isoform and ID-mapping guidance is correct and verified.'},
     'code_usability': {'result': 'PASS', 'detail': 'All client functions and both examples ran on the exact final bytes; the one remaining defect is a P2 documentation and expectation gap (UNI-010).'}}},
 'static_score': {'subtotal': sub, 'max': 100, 'categories': {k: {'score': v[0], 'max': v[1], 'note': v[2]} for k, v in st.items()}},
 'dynamic_score': {'execution_avg': avg, 'max': 100,
   'assertion_pass_rate': {'passed': sum(i['assertions_passed'] for i in inputs), 'total': sum(i['assertions_total'] for i in inputs)},
   'inputs': inputs},
 'final': {'static_weighted': sw, 'dynamic_weighted': dw, 'score': score, 'max': 100,
           'grade': 'Production Ready' if score >= 85 else 'Limited Release', 'grade_symbol': '\u2b50' if score >= 85 else '\u2705',
           'deployable': score >= 75, 'veto_override': False},
 'key_strengths': [
   'All nine initial findings (four P1, five P2) reproduce as fixed on the exact final bytes against UniProt release 2026_03.',
   'ID mapping now returns the complete stream (44 rows against 25 on the first page) and reports unmapped inputs, with a poll timeout and FAILED handling.',
   'One request helper gives every call a timeout, Retry-After-aware retries and sane give-up behaviour, verified with stubbed 429/503 and connection errors.',
   'Documentation claims (xref:pdb versus database:pdb, ft_act_site, corpus sizes, the 400 on the old proteome route) were checked against the live service and hold.'],
 'recommendations': [
   {'priority': 'P2', 'title': 'UNI-010 Proteome route returns all entries; sizes misstated', 'observed_in': [5],
    'problem': 'download_proteome("UP000005640") writes 147,520 records (20,416 reviewed + 127,104 TrEMBL), 37.8 MB gzip, but the example prints "~20 MB compressed; ~80 MB unpacked; ~20K proteins" and no text says the route includes TrEMBL.',
    'root_cause': 'The size note was carried over from the upstream reference-proteome FTP set (one per gene) and the stream route was not checked for human.',
    'fix': 'Correct the example text to the measured sizes, state in the docstring and SKILL.md that proteome:UPID returns all UniProtKB entries, and show `AND reviewed:true` for a Swiss-Prot-only FASTA.'}],
}
with open(RUN + '/report.json', 'w', encoding='utf-8', newline='\n') as f:
    json.dump(rep, f, indent=2, ensure_ascii=False)
    f.write('\n')
print('static', sub, 'exec', avg, 'final', sw, dw, score, rep['final']['grade'],
      'L1', round(sum(i['basic'] for i in inputs) / n, 1), 'L2', round(sum(i['specialized'] for i in inputs) / n, 1),
      'assert', rep['dynamic_score']['assertion_pass_rate'])
