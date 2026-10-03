import hashlib, json, os, sys
sys.dont_write_bytecode = True
C = 'F:/OpenScience/wt/dbaccess-uniprot-access/skills/bio-uniprot-access'
OLD = 'F:/OpenScience/audits/bio-uniprot-access/reaudit-run'
RUN = 'F:/OpenScience/audits/bio-uniprot-access/delta-reaudit-run'


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
assert ident == '7a203a5063ea1cdad2c32516c1cc1740eb13c1e5008d53c5950e81b8cfdf7f5b', ident
total = sum(n for _, n, _ in files)
si = json.load(open(OLD + '/source-identity.json', encoding='utf-8'))
si['candidate'].update({'content_sha256': ident, 'content_manifest': {'file_count': len(files), 'bytes': total}})
si['files'] = [{'path': r, 'bytes': n, 'sha256': h} for r, n, h in files]
si['prior_audited_identity'] = 'ea100b041cafcbf60a8d1202d6ca09387fff80515d37b45d5998162fb799bcb1'
si['delta'] = {'mode': 'text-only', 'changed_files': ['SKILL.md', 'examples/isoforms_and_xrefs.py'],
               'unchanged_files_match_certified_sha256': ['LICENSE', 'examples/uniprot_query.py', 'scripts/uniprot_client.py', 'usage-guide.md']}
si['tooling']['preflight'] = 'skill_preflight.py --offline PASS'
dump(si, RUN + '/source-identity.json')

r = json.load(open(OLD + '/report.json', encoding='utf-8'))
r['meta']['evaluated_on'] = '2026-10-03'
rm = r['veto_gates']['research_veto']
rm['code_usability']['detail'] = ('All client functions and both examples ran on the certified bytes; the only change since is prose and one print literal, '
                                  'the example re-ran exit 0 and the previously open P2 (UNI-010) is resolved.')
cat = r['static_score']['categories']
cat['functional_suitability'].update(score=12, note='Every client function and both examples run and return correct live data; the proteome route is now documented as returning reviewed and TrEMBL entries (UNI-010 resolved).')
cat['human_usability'].update(score=8, note='Clear tables and examples; the printed proteome size text now matches the measured download.')
sub = sum(v['score'] for v in cat.values())
r['static_score']['subtotal'] = sub
d = r['dynamic_score']
i5 = d['inputs'][4]
i5['note'] = ('Certified run: E. coli 4,403 records equal the server count; human 147,520 records (20,416 reviewed + 127,104 TrEMBL), 37.8 MB gzip, 86.65 MB raw. '
              'Delta: the example text and SKILL.md row now state those figures; AND reviewed:true on the same stream route returned exactly 20,416 sp records and no tr records (7.5 MB gzip).')
i5['assertions'][3] = {'text': i5['assertions'][3]['text'], 'result': 'PASS',
                       'note': '~38 MB / ~87 MB / ~147.5K entries printed; real 37.8 MB gz, 86.65 MB raw, 147,520 entries'}
i5['basic'], i5['specialized'] = 35, 52
i5['total'] = 87
i5['assertions_passed'] = 5
i5['status_flag'] = '\u2705'
n = len(d['inputs'])
avg = round(sum(i['total'] for i in d['inputs']) / n, 1)
d['execution_avg'] = avg
d['assertion_pass_rate'] = {'passed': sum(i['assertions_passed'] for i in d['inputs']),
                            'total': sum(i['assertions_total'] for i in d['inputs'])}
sw = round(sub * 0.4, 1)
dw = round(avg * 0.6, 1)
score = round(sw + dw)
r['final'].update(static_weighted=sw, dynamic_weighted=dw, score=score)
r['key_strengths'][0] = 'All ten findings reproduce as fixed; the last open P2 (UNI-010) is closed by a text-only change verified against the certified measurements and a live reviewed:true check.'
r['recommendations'] = []
dump(r, RUN + '/report.json')
l1 = round(sum(i['basic'] for i in d['inputs']) / n, 1)
l2 = round(sum(i['specialized'] for i in d['inputs']) / n, 1)
ap = d['assertion_pass_rate']
print(sub, avg, sw, dw, score, r['final']['grade'], l1, l2, ap)

view = f"""# Delta re-audit: bio-uniprot-access

**Date:** 2026-10-03
**Candidate:** `F:\\OpenScience\\wt\\dbaccess-uniprot-access\\skills\\bio-uniprot-access` (untracked, uncommitted by design)
**Exact identity:** `sha256-manifest-v1 {ident}` (6 files, {total:,} bytes), derived from certified `ea100b041cafcbf60a8d1202d6ca09387fff80515d37b45d5998162fb799bcb1` (86, Production Ready; record `candidate@ea100b041caf-reaudit-run`)
**Result:** Candidate-ready: **{score}/100, Production Ready** (static {sub}, execution average {avg}). UniProt release 2026_03. Delta mode: the text-only change qualified.

## Delta verification

| Check | Result | Evidence |
|---|---|---|
| Unchanged files (LICENSE, uniprot_query.py, uniprot_client.py, usage-guide.md) | byte-identical to certified | `evidence/text_claims.txt` |
| SKILL.md | only the Proteome FASTA table cell differs; reverting that cell reproduces the certified sha256 | `evidence/text_claims.txt` |
| examples/isoforms_and_xrefs.py | reverting the one string literal reproduces the certified sha256; ASTs differ only in that Constant | `evidence/text_claims.txt` |
| 147,520 entries, 37.8 MB gz, 20,416 reviewed | measured in the certified run; live counts re-queried (147,520 / 20,416, release 2026_03) | `reaudit-run/evidence/proteome_counts.txt` |
| ~87 MB unpacked | certified download measured 86,650,690 bytes (86.65 MB decimal, same convention as 37.8 MB gz) | `reaudit-run/evidence/proteome.txt` |
| `AND reviewed:true` on /uniprotkb/stream | returns 20,416 sp records and 0 tr records | `evidence/text_claims.txt` |
| Changed example executed | exit 0, new text printed | `evidence/example.txt` |

## Findings

- **UNI-010 (P2): verified-fixed.** SKILL.md and the example now state that the proteome route returns reviewed and TrEMBL entries, give the measured sizes, and show the `reviewed:true` restriction.
- No new findings. No open findings.

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

Carried forward from the certified record: all other scores and executed evidence (code bytes unchanged). Re-scored: functional suitability 11 to 12, human usability 7 to 8, input 5 (basic 31 to 35, specialized 46 to 52; assertion 4 now PASS).

Rerun: `Scripts\\python.exe delta-reaudit-run\\scripts\\verify_text_only.py` and `reviewed_route_check.py`.
"""
with open(RUN + '/viewer.md', 'w', encoding='utf-8', newline='\n') as f:
    f.write(view)
