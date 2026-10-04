"""Shared builder: turns a spec dict into report.json, viewer.md, source-identity.json and finding-ledger.md.

Every number in report.json is computed here (subtotal, input totals, averages, weighted score) so the
arithmetic cannot drift from the per-input rows. Rubric: skill-auditor.zip (sha256 e54e9ff8...), data-analysis
specialized rubric; grade mapping and floors from references/scoring_rubric.md.
"""
import json, hashlib, os, subprocess, sys

CATS = ['functional_suitability', 'reliability', 'performance_context', 'agent_usability',
        'human_usability', 'security', 'maintainability', 'agent_specific']
CAT_MAX = dict(zip(CATS, [12, 12, 8, 16, 8, 12, 12, 20]))
GRADES = [(85, 'Production Ready', '\u2b50'), (75, 'Limited Release', '\u2705'), (60, 'Beta Only', '\u26a0\ufe0f'), (0, 'Reject', '\u274c')]


def grade_for(score):
    for lo, name, sym in GRADES:
        if score >= lo:
            return name, sym


def build(spec, run_dir, skill_dir, preflight_root):
    inputs = []
    for i, it in enumerate(spec['inputs'], 1):
        spc = it['specialized']  # dict of 5 dims
        assert set(spc) == {'methodological_validity', 'code_executability', 'data_quality_control', 'reproducibility', 'security'}
        spec_total = sum(spc.values())
        total = it['basic'] + spec_total
        passed = sum(1 for a in it['assertions'] if a[1] == 'PASS')
        assert 3 <= len(it['assertions']) <= 5, (i, len(it['assertions']))
        flag = '\u2705' if it['status'] == 'COMPLETED' and total >= 75 else ('\u26a0\ufe0f' if it['status'] == 'COMPLETED' else '\u274c')
        inputs.append({
            'index': i, 'type': it['type'], 'label': it['label'], 'status': it['status'], 'status_flag': flag,
            'note': it['note'], 'basic': it['basic'], 'specialized': spec_total, 'total': total,
            'assertions_passed': passed, 'assertions_total': len(it['assertions']),
            'assertions': [{'text': t, 'result': r, 'note': n} for t, r, n in it['assertions']],
            '_spec_dims': spc,
        })
    n = len(inputs)
    avg = round(sum(x['total'] for x in inputs) / n, 1)
    ap = sum(x['assertions_passed'] for x in inputs); at = sum(x['assertions_total'] for x in inputs)
    cats = {c: {'score': spec['static'][c][0], 'max': CAT_MAX[c], 'note': spec['static'][c][1]} for c in CATS}
    for c in CATS:
        assert 0 <= cats[c]['score'] <= CAT_MAX[c], c
    sub = sum(v['score'] for v in cats.values())
    sw = round(sub * 0.4, 1); dw = round(avg * 0.6, 1)
    score = int(round(sw + dw))
    base_grade, _ = grade_for(score)
    # floors (scoring_rubric.md section 5): any miss downgrades exactly one tier
    l1 = sum(x['basic'] for x in inputs) / n; l2 = sum(x['specialized'] for x in inputs) / n
    floors = {
        'static>=70(LR)/80(PR)': sub, 'execution_avg>=75(LR)/85(PR)': avg, 'layer1_avg>=28(LR)/32(PR)': round(l1, 1),
        'layer2_avg>=42(LR)/48(PR)': round(l2, 1), 'assertion_rate>=80%(LR)/90%(PR)': round(100 * ap / at, 1)}
    tiers = [g[1] for g in GRADES]
    need = {'Production Ready': (80, 85, 32, 48, 90), 'Limited Release': (70, 75, 28, 42, 80)}
    vals = (sub, avg, l1, l2, 100 * ap / at)
    grade = base_grade; missed = []
    if grade in need:
        missed = [k for k, v, t in zip(floors, vals, need[grade]) if v < t]
        if missed:
            grade = tiers[tiers.index(grade) + 1]
    vetoed = spec['veto']['skill_gate'] == 'FAIL' or spec['veto']['research_gate'] == 'FAIL'
    if vetoed:
        grade = 'Reject'
    sym = dict((g[1], g[2]) for g in GRADES)[grade]
    deployable = grade in ('Production Ready', 'Limited Release') and not vetoed
    v = spec['veto']
    pr = [f['priority'] for f in spec['findings']]
    assert pr == sorted(pr), 'ledger must be P0->P2 ordered'
    report = {
        'meta': {
            'skill_name': spec['skill_id'], 'description': spec['description'], 'evaluated_on': '2026-10-03',
            'evaluator_version': 'skill-auditor@1.0', 'category': 'Data Analysis', 'execution_mode': 'A',
            'complexity': spec['complexity'], 'n_inputs': n,
        },
        'veto_gates': {
            'skill_veto': {'gate': v['skill_gate'], 'stability': v['t1'][0], 'contract': v['t2'][0], 'determinism': v['t3'][0], 'security': v['t4'][0]},
            'research_veto': {
                'applicable': True, 'gate': v['research_gate'],
                'scientific_integrity': {'result': v['m1'][0], 'detail': v['m1'][1]},
                'practice_boundaries': {'result': v['m2'][0], 'detail': v['m2'][1]},
                'methodological_ground': {'result': v['m3'][0], 'detail': v['m3'][1]},
                'code_usability': {'result': v['m4'][0], 'detail': v['m4'][1]}},
        },
        'static_score': {'subtotal': sub, 'max': 100, 'categories': cats},
        'dynamic_score': {'execution_avg': avg, 'max': 100, 'assertion_pass_rate': {'passed': ap, 'total': at},
                          'inputs': [{k: val for k, val in x.items() if k != '_spec_dims'} for x in inputs]},
        'final': {'static_weighted': sw, 'dynamic_weighted': dw, 'score': score, 'max': 100, 'grade': grade,
                  'grade_symbol': sym, 'deployable': deployable, 'veto_override': vetoed},
        'key_strengths': spec['strengths'],
        'recommendations': [{'priority': f['priority'], 'title': f"{f['id']}: {f['title']}", 'observed_in': f['observed_in'], 'problem': f['problem'], 'root_cause': f['root_cause'], 'fix': f['fix']} for f in spec['findings']],
    }
    with open(os.path.join(run_dir, 'report.json'), 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False); f.write('\n')

    # source identity
    pf = json.loads(subprocess.check_output([sys.executable, os.path.join(preflight_root, 'tools', 'skill_preflight.py'), '--offline', '--json', skill_dir]))[0]
    assert not pf['fail'] and pf['identity'] == spec['identity'], pf
    files = []
    for root, _, names in os.walk(skill_dir):
        for nm in sorted(names):
            p = os.path.join(root, nm)
            files.append({'path': os.path.relpath(p, skill_dir).replace('\\', '/'), 'sha256': hashlib.sha256(open(p, 'rb').read()).hexdigest(), 'bytes': os.path.getsize(p)})
    files.sort(key=lambda x: x['path'])
    ident = {
        'origin': {'repository': 'GPTomics/bioSkills', 'commit': 'd91ed3d563019e649dc854c56ccd62551359488a', 'path': spec['origin_path'],
                   'checkout_read_only': 'F:\\OpenScience\\bioSkills-Improved\\' + spec['origin_path']},
        'candidate': {'branch': 'normalize/ml-lane3', 'commit': '29f5446e431db8eba803796e6f7dfc02f7886743', 'content_sha256': spec['identity'],
                      'identity_kind': 'sha256-manifest', 'path': skill_dir.replace('/', '\\'), 'file_count': pf['files'], 'bytes': pf['bytes'],
                      'status_before': 'untracked skill directory (by design)', 'status_after_execution': 'unchanged: identity re-verified after execution'},
        'files': files,
        'tooling': {'tools_md': spec['tools_md'], 'tools_md_sha256': spec['tools_sha'],
                    'environment_fingerprint_sha256': '20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6',
                    'environment_root': 'F:\\OpenScience\\audit-envs\\cheminformatics-hit-triage-analyst',
                    'rubric_zip_sha256': hashlib.sha256(open(r'F:\optimizing-agent-science-skills\skill-auditor.zip','rb').read()).hexdigest()},
        'preflight_warnings': pf['warn'],
    }
    with open(os.path.join(run_dir, 'source-identity.json'), 'w', encoding='utf-8') as f:
        json.dump(ident, f, indent=2, ensure_ascii=False); f.write('\n')

    # finding ledger
    L = ['# Ordered finding ledger', '', f"Audit identity: `{spec['identity']}` (candidate content sha256-manifest).", '',
         '| Order | ID | Priority | State | Evidence | Fix touches | Required disposition |', '|---:|---|---|---|---|---|---|']
    for k, fnd in enumerate(spec['findings'], 1):
        L.append(f"| {k} | {fnd['id']} | {fnd['priority']} | open (new, RA) | {fnd['evidence']} | {fnd['touches']} | {fnd['fix']} |")
    L += ['', 'No audit-local repair was attempted; candidate bytes unchanged.', '']
    open(os.path.join(run_dir, 'finding-ledger.md'), 'w', encoding='utf-8').write('\n'.join(L))

    # viewer
    V = [f"# Eval Viewer: {spec['skill_id']}", '', 'Generated: 2026-10-03  ', 'Phase: independent final re-audit (lane 3a-1, full mode)  ',
         f"Exact candidate: `{spec['identity']}` (files={pf['files']}, bytes={pf['bytes']})", '', '## Outcome', '', spec['outcome'], '',
         '## Summary table', '', '| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |', '|---:|---|---:|---:|---:|---:|:---:|']
    for x in inputs:
        V.append(f"| {x['index']} | {x['type']} | {x['basic']} | {x['specialized']} | {x['total']} | {x['assertions_passed']}/{x['assertions_total']} | {x['status_flag']} |")
    V += ['', f"**Execution average:** {avg}/100  ", f"**Assertion pass rate:** {ap}/{at} ({round(100*ap/at,1)}%)  ", f"**Static score:** {sub}/100  ",
          f"**Arithmetic:** {sub} x 0.4 = {sw}; {avg} x 0.6 = {dw}; {sw} + {dw} = {round(sw+dw,1)} -> **{score}/100**  ",
          f"**Grade:** {grade} (score band {base_grade}" + (f"; one-tier downgrade for missed floors: {', '.join(missed)}" if missed else '') + ')', '',
          '## Veto gates', '', f"Skill veto: **{v['skill_gate']}**. Research veto: **{v['research_gate']}**.", '']
    for key, lab in [('t1', 'T1 stability'), ('t2', 'T2 contract'), ('t3', 'T3 determinism'), ('t4', 'T4 security')]:
        V.append(f"- {lab}: {v[key][0]}. {v[key][1]}")
    for key, lab in [('m1', 'M1 scientific integrity'), ('m2', 'M2 practice boundaries'), ('m3', 'M3 methodological ground'), ('m4', 'M4 code usability')]:
        V.append(f"- {lab}: {v[key][0]}. {v[key][1]}")
    V += ['', '## Inputs', '']
    for x in inputs:
        V += [f"### Input {x['index']} ({x['type']}): {x['label']}", '', f"Status {x['status']}. {x['note']}", '',
              f"Specialized dimensions: {', '.join(f'{k} {val}' for k, val in x['_spec_dims'].items())}.", '']
        for a in x['assertions']:
            V.append(f"- {a['result']}: {a['text']} ({a['note']})")
        V.append('')
    V += ['## Finding ledger (fixer order)', '', '| ID | Sev | Fix touches | Summary |', '|---|---|---|---|']
    for fnd in spec['findings']:
        V.append(f"| {fnd['id']} | {fnd['priority']} | {fnd['touches']} | {fnd['summary']} |")
    V += ['', spec['leads'], '', '## Coverage and evidence', '', spec['coverage'], '']
    open(os.path.join(run_dir, 'viewer.md'), 'w', encoding='utf-8').write('\n'.join(V))
    print(json.dumps({'score': score, 'grade': grade, 'avg': avg, 'static': sub, 'assert': f'{ap}/{at}', 'missed_floors': missed, 'base': base_grade}))
