import hashlib, json, os, sys
sys.dont_write_bytecode = True
C = 'F:/OpenScience/wt/dbaccess-interaction-databases/skills/bio-interaction-databases'
OLD = 'F:/OpenScience/audits/bio-interaction-databases/reaudit-run-2'
RUN = 'F:/OpenScience/audits/bio-interaction-databases/delta-reaudit-run'


def dump(obj, path):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write('\n')


files = []
for root, _, names in os.walk(C):
    for n in names:
        p = os.path.join(root, n)
        b = open(p, 'rb').read()
        files.append((os.path.relpath(p, C).replace(os.sep, '/'), len(b), hashlib.sha256(b).hexdigest()))
files.sort(key=lambda x: x[0].encode('utf-8'))
ident = hashlib.sha256('\n'.join(f'{r}\t{n}\t{h}' for r, n, h in files).encode('utf-8')).hexdigest()
assert ident == 'f4d95b083e70343c570554032b0592bc13d99f578274465d12367b91bf286c2d', ident
total = sum(n for _, n, _ in files)
si = json.load(open(OLD + '/source-identity.json', encoding='utf-8'))
si['candidate'].update({'content_sha256': ident, 'content_manifest': {'file_count': len(files), 'bytes': total}})
si['files'] = [{'path': r, 'bytes': n, 'sha256': h} for r, n, h in files]
si['prior_audited_identity'] = '16290147ab41129829074d65394467e2df7131b08099d0f2a4d42497af154024'
si['delta'] = {'mode': 'text-only', 'changed_files': ['SKILL.md', 'scripts/interaction_clients.py (aggregate_networks docstring only)'],
               'unchanged_files_match_certified_sha256': ['LICENSE', 'examples/interaction_query.py', 'examples/string_network.py', 'usage-guide.md']}
si['tooling']['preflight'] = 'skill_preflight.py --offline PASS'
dump(si, RUN + '/source-identity.json')

r = json.load(open(OLD + '/report.json', encoding='utf-8'))
r['veto_gates']['research_veto']['code_usability']['detail'] = (
    'Every client function and both examples ran on the certified bytes; the only change since is prose and one docstring '
    '(AST identical otherwise); one minor P2 observation remains (IDM-013).')
cat = r['static_score']['categories']
cat['agent_usability'].update(score=15, note='Decision matrix, channel semantics, failure-mode and common-error tables are accurate and match live behaviour; the aggregate bullet now names homodimers and points to biogrid_lt_physical.')
sub = sum(v['score'] for v in cat.values())
r['static_score']['subtotal'] = sub
d = r['dynamic_score']
i6 = d['inputs'][5]
i6['note'] += ' Delta: documentation now says self-interactions (homodimers) are excluded, a self-interaction-only gene is not a node, and gene_a == gene_b rows remain in biogrid_lt_physical (live: TP53 30 of 3,081 rows, MDM2 23 of 2,058); live aggregate TP53+MDM2 still 2 nodes, no self-loops.'
sw = round(sub * 0.4, 1)
dw = round(d['execution_avg'] * 0.6, 1)
score = round(sw + dw)
r['final'].update(static_weighted=sw, dynamic_weighted=dw, score=score)
r['recommendations'] = [x for x in r['recommendations'] if not x['title'].startswith('IDM-012')]
r['key_strengths'][0] = 'All thirteen findings but one reproduce as fixed; IDM-012 is closed by a docstring and prose change verified against live BioGRID output. Only IDM-013 (P2) remains open.'
dump(r, RUN + '/report.json')
avg = d['execution_avg']
ap = d['assertion_pass_rate']
n = len(d['inputs'])
l1 = round(sum(i['basic'] for i in d['inputs']) / n, 1)
l2 = round(sum(i['specialized'] for i in d['inputs']) / n, 1)
print(sub, avg, sw, dw, score, r['final']['grade'], l1, l2, ap)

view = f"""# Delta re-audit: bio-interaction-databases

**Date:** 2026-10-03
**Candidate:** `F:\\OpenScience\\wt\\dbaccess-interaction-databases\\skills\\bio-interaction-databases` (untracked, uncommitted by design)
**Exact identity:** `sha256-manifest-v1 {ident}` (6 files, {total:,} bytes), derived from certified `16290147ab41129829074d65394467e2df7131b08099d0f2a4d42497af154024` (87, Production Ready; record `candidate@16290147ab41-reaudit-run-2`)
**Result:** Candidate-ready: **{score}/100, Production Ready** (static {sub}, execution average {avg}). Delta mode: the text-only change qualified.

## Delta verification

| Check | Result | Evidence |
|---|---|---|
| Unchanged files (LICENSE, both examples, usage-guide.md) | byte-identical to certified | `evidence/self_rows.txt` |
| SKILL.md | only the aggregate_networks parenthetical differs; reverting it reproduces the certified sha256 | `evidence/skill_md.txt` |
| scripts/interaction_clients.py | two docstring lines differ; reverting them reproduces the certified sha256; AST identical once the aggregate_networks docstring is removed | `evidence/self_rows.txt` |
| `gene_a == gene_b` rows remain in biogrid_lt_physical | true live with the real key: TP53 30 of 3,081 rows, MDM2 23 of 2,058 | `evidence/self_rows.txt` |
| Homodimer-only gene is not a node; aggregate has no self-loops | certified mocked probe (homodimer-only graph 0 nodes, 0 edges); live TP53+MDM2 aggregate 2 nodes, no self-loops | `reaudit-run-2/evidence/probe_idm10_11.txt`, `evidence/self_rows.txt` |

## Findings

- **IDM-012 (P2): verified-fixed.** The SKILL.md bullet and the docstring name homodimers, say such a gene is not a node, and point to `biogrid_lt_physical`. Dropping remains silent by design (no warning or count); it is now documented.
- **IDM-013 (P2): still open**, untouched by design (example edge attributes depend on SIGNOR record order).
- No new findings.

## Readiness gate

| Metric | Value | Requirement |
|---|---:|---:|
| Final score | {score} ({sw} + {dw}) | 85 |
| Static | {sub} | 80 |
| Execution average | {avg} | 85 |
| Layer 1 average | {l1} / 40 | 32 |
| Layer 2 average | {l2} / 60 | 48 |
| Assertions | {ap['passed']} / {ap['total']} | 90% |
| Veto / open P0 | none / none | none |

Carried forward from the certified record: all scores and executed evidence except agent usability 14 to 15 (documentation gap closed). The BioGRID key was loaded at run time only; a scan of the run directory and Skill tree found no hit.

Rerun: `Scripts\\python.exe delta-reaudit-run\\scripts\\self_rows_and_docstring.py` (needs BIOGRID_ACCESS_KEY file) and `verify_skill_md.py`.
"""
with open(RUN + '/viewer.md', 'w', encoding='utf-8', newline='\n') as f:
    f.write(view)
