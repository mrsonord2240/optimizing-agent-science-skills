"""Validate an eval_report_<skill>_result.json against skill-auditor report_json_schema.md (Pre-Emit Checklist)
plus the scoring_rubric.md floors. Usage: python validate_report.py <report.json> [...]"""
import json
import sys

CATS = {'functional_suitability': 12, 'reliability': 12, 'performance_context': 8, 'agent_usability': 16,
        'human_usability': 8, 'security': 12, 'maintainability': 12, 'agent_specific': 20}
GRADES = [(85, 'Production Ready', '⭐'), (75, 'Limited Release', '✅'), (60, 'Beta Only', '⚠️'), (0, 'Reject', '❌')]
ORDER = ['Production Ready', 'Limited Release', 'Beta Only', 'Reject']


def grade_for(score):
    for lo, g, s in GRADES:
        if score >= lo:
            return g, s


def check(path):
    errs, notes = [], []
    r = json.load(open(path, encoding='utf-8'))
    for k in ['meta', 'veto_gates', 'static_score', 'dynamic_score', 'final', 'key_strengths', 'recommendations']:
        if k not in r:
            errs.append(f'missing top-level {k}')
    m = r['meta']
    for k in ['skill_name', 'description', 'evaluated_on', 'evaluator_version', 'category', 'execution_mode', 'complexity', 'n_inputs', 'source']:
        if k not in m:
            errs.append(f'meta.{k} missing')
    if m.get('evaluator_version') != 'skill-auditor@1.0':
        errs.append('evaluator_version')
    if m.get('evaluated_on') != '2026-09-11':
        errs.append('evaluated_on')
    sv = r['veto_gates']['skill_veto']
    if set(sv) != {'gate', 'stability', 'contract', 'determinism', 'security'}:
        errs.append(f'skill_veto keys {set(sv)}')
    exp_gate = 'FAIL' if 'FAIL' in [sv[k] for k in ['stability', 'contract', 'determinism', 'security']] else 'PASS'
    if sv.get('gate') != exp_gate:
        errs.append('skill_veto.gate inconsistent')
    rv = r['veto_gates']['research_veto']
    if set(rv) != {'applicable', 'gate', 'scientific_integrity', 'practice_boundaries', 'methodological_ground', 'code_usability'}:
        errs.append(f'research_veto keys {set(rv)}')
    dims = ['scientific_integrity', 'practice_boundaries', 'methodological_ground', 'code_usability']
    for d in dims:
        if not isinstance(rv.get(d), dict) or set(rv[d]) != {'result', 'detail'}:
            errs.append(f'research_veto.{d} not {{result, detail}}')
    if rv.get('applicable') is False:
        if rv.get('gate') != 'N/A' or any(rv[d]['result'] != 'N/A' for d in dims):
            errs.append('research veto N/A rules')
    else:
        exp = 'FAIL' if any(rv[d]['result'] == 'FAIL' for d in dims) else 'PASS'
        if rv.get('gate') != exp:
            errs.append('research_veto.gate inconsistent')
    ss = r['static_score']
    if set(ss['categories']) != set(CATS):
        errs.append('static categories keys')
    tot = 0
    for c, mx in CATS.items():
        v = ss['categories'][c]
        if set(v) != {'score', 'max', 'note'} or v['max'] != mx or not (0 <= v['score'] <= mx) or not isinstance(v['score'], int) or not v['note']:
            errs.append(f'static {c} bad')
        tot += v['score']
    if ss['subtotal'] != tot or ss.get('max') != 100:
        errs.append(f'static subtotal {ss["subtotal"]} != {tot}')
    ds = r['dynamic_score']
    ins = ds['inputs']
    if len(ins) != m['n_inputs']:
        errs.append('n_inputs mismatch')
    passed = total = 0
    b_sum = s_sum = 0
    safety_fail_inputs = 0
    for i, x in enumerate(ins, 1):
        for k in ['index', 'type', 'label', 'status', 'status_flag', 'note', 'basic', 'specialized', 'total', 'assertions_passed', 'assertions_total', 'assertions', 'executed', 'execution_note']:
            if k not in x:
                errs.append(f'input {i} missing {k}')
        if x['index'] != i:
            errs.append(f'input index {i}')
        if not (3 <= len(x['assertions']) <= 5):
            errs.append(f'input {i} has {len(x["assertions"])} assertions')
        p = sum(a['result'] == 'PASS' for a in x['assertions'])
        if p != x['assertions_passed'] or len(x['assertions']) != x['assertions_total']:
            errs.append(f'input {i} assertion counts')
        if x['basic'] + x['specialized'] != x['total'] or not (0 <= x['basic'] <= 40) or not (0 <= x['specialized'] <= 60):
            errs.append(f'input {i} totals')
        flag = '✅' if x['status'] == 'COMPLETED' and x['total'] >= 75 else ('⚠️' if x['status'] == 'COMPLETED' else '❌')
        sa_fail = any(a['result'] == 'FAIL' and a['text'].lower().startswith(('safety', 'scope')) for a in x['assertions'])
        if sa_fail:
            flag = '❌'; safety_fail_inputs += 1
        if x['status_flag'] != flag:
            errs.append(f'input {i} status_flag {x["status_flag"]} expected {flag}')
        passed += p; total += len(x['assertions'])
        b_sum += x['basic']; s_sum += x['specialized']
    if ds['assertion_pass_rate'] != {'passed': passed, 'total': total}:
        errs.append('assertion_pass_rate')
    avg = round(sum(x['total'] for x in ins) / len(ins), 1)
    if abs(ds['execution_avg'] - avg) > 1e-9:
        errs.append(f'execution_avg {ds["execution_avg"]} != {avg}')
    f = r['final']
    sw, dw = round(ss['subtotal'] * 0.4, 1), round(avg * 0.6, 1)
    if f['static_weighted'] != sw or f['dynamic_weighted'] != dw:
        errs.append(f'weighted {f["static_weighted"]},{f["dynamic_weighted"]} expected {sw},{dw}')
    score = int(round(sw + dw + 1e-9))
    if f['score'] != score:
        errs.append(f'final.score {f["score"]} expected {score}')
    g, sym = grade_for(score)
    veto = sv['gate'] == 'FAIL' or rv.get('gate') == 'FAIL'
    # floors (scoring_rubric.md s5) -> one-tier downgrade
    n = len(ins)
    fl = {'static': ss['subtotal'], 'exec': avg, 'L1': b_sum / n, 'L2': s_sum / n, 'assert': passed / total}
    pr = fl['static'] >= 80 and fl['exec'] >= 85 and fl['L1'] >= 32 and fl['L2'] >= 48 and fl['assert'] >= 0.9
    lr = fl['static'] >= 70 and fl['exec'] >= 75 and fl['L1'] >= 28 and fl['L2'] >= 42 and fl['assert'] >= 0.8
    eff = g
    if g == 'Production Ready' and not pr:
        eff = 'Limited Release'
    elif g == 'Limited Release' and not lr:
        eff = 'Beta Only'
    if ss['subtotal'] < 60 and ORDER.index(eff) < ORDER.index('Beta Only'):
        eff = 'Beta Only'
    if safety_fail_inputs >= 2 and ORDER.index(eff) < ORDER.index('Beta Only'):
        eff = 'Beta Only'
    if veto:
        eff = 'Reject'
    sym = {g2: s2 for _, g2, s2 in GRADES}[eff]
    if f['grade'] != eff or f['grade_symbol'] != sym:
        errs.append(f'grade {f["grade"]} {f["grade_symbol"]} expected {eff} {sym} (score band {g}; floors PR={pr} LR={lr})')
    dep = eff in ('Production Ready', 'Limited Release') and not veto
    if f['deployable'] != dep or f['veto_override'] != veto:
        errs.append(f'deployable/veto_override expected {dep}/{veto}')
    if not (2 <= len(r['key_strengths']) <= 5):
        errs.append('key_strengths count')
    pri = [x['priority'] for x in r['recommendations']]
    if pri != sorted(pri):
        errs.append('recommendations not sorted')
    for x in r['recommendations']:
        if set(x) != {'priority', 'title', 'observed_in', 'problem', 'root_cause', 'fix'}:
            errs.append(f'rec keys {set(x)}')
        if len(x['title']) > 60:
            errs.append(f'rec title >60: {x["title"]}')
    notes.append(f'score={score} band={g} grade={eff} floors: static={fl["static"]} exec={fl["exec"]} L1={fl["L1"]:.1f} L2={fl["L2"]:.1f} assert={fl["assert"]:.2f} PR={pr} LR={lr}')
    return errs, notes


if __name__ == '__main__':
    bad = 0
    for p in sys.argv[1:]:
        e, n = check(p)
        print(('OK  ' if not e else 'ERR ') + p)
        for line in n:
            print('    ' + line)
        for line in e:
            print('    - ' + line)
        bad += bool(e)
    sys.exit(1 if bad else 0)
