#!/usr/bin/env python3
"""NEW-input helper: examples/qc_report.py and SKILL.md block 028 vs counts planted BY CONSTRUCTION (data/edge/expected.json), independent of flagstat."""
import json, re, subprocess, sys, os
R = '/mnt/openscience/audits/bio-bam-statistics/run'
exp = json.load(open(f'{R}/data/edge/expected.json'))
bad = 0
for name, e in exp.items():
    bam = f'{R}/data/edge/{name}.bam'
    p = subprocess.run([sys.executable, f'{R}/skill/examples/qc_report.py', bam], capture_output=True, text=True)
    out = p.stdout
    src = open(f'{R}/blocks/028_python.py', encoding='utf-8').read().replace("'input.bam'", repr(bam))
    q = subprocess.run([sys.executable, '-c', src], capture_output=True, text=True)
    fails = []
    def chk(n, got, want):
        if got != want: fails.append(f'{n}: got {got!r} want {want!r}')
    chk('qc_report rc', p.returncode, 0); chk('no traceback', 'Traceback' in p.stderr, False)
    m = re.search(r'Total records:\s+([\d,]+) \(primary ([\d,]+) \+ secondary ([\d,]+) \+ supplementary ([\d,]+)\)', out)
    if m:
        g = [int(x.replace(',', '')) for x in m.groups()]
        chk('records', g[0], e['records']); chk('primary', g[1], e['primary']); chk('secondary', g[2], e['secondary']); chk('supp', g[3], e['supplementary'])
    else: fails.append('no header line: ' + out[:80] + p.stderr[-100:])
    m = re.search(r'QC-failed primary:\s+([\d,]+)', out); chk('qcfail', int(m.group(1).replace(',', '')) if m else None, e['qcfail_primary'])
    m = re.search(r'QC-passed primary:\s+([\d,]+)', out); chk('passed', int(m.group(1).replace(',', '')) if m else None, e['passed'])
    if e['passed']:
        m = re.search(r'Mapped:\s+([\d,]+) \(([\d.]+)%', out); chk('mapped', int(m.group(1).replace(',', '')) if m else None, e['mapped'])
        if m: chk('mapped %', m.group(2), f"{e['mapped']/e['passed']*100:.2f}")
        m = re.search(r'Properly paired:\s+([\d,]+) \(([\d.]+|n/a)', out); chk('proper', int(m.group(1).replace(',', '')) if m else None, e['proper'])
        if m: chk('proper %', m.group(2), f"{e['proper']/e['paired']*100:.2f}" if e['paired'] else 'n/a')
        m = re.search(r'Duplicates:\s+([\d,]+)', out); chk('dup', int(m.group(1).replace(',', '')) if m else None, e['dup'])
    else:
        chk('nothing to report', 'nothing to report' in out, True)
    # block 028 (Count Reads)
    if e['passed']:
        chk('028 rc', q.returncode, 0)
        m = re.search(r'Primary QC-passed: (\d+)', q.stdout); chk('028 passed', int(m.group(1)) if m else None, e['passed'])
        m = re.search(r'Mapped: (\d+)', q.stdout); chk('028 mapped', int(m.group(1)) if m else None, e['mapped'])
        if e['paired']:
            m = re.search(r'Properly paired: (\d+)', q.stdout); chk('028 proper', int(m.group(1)) if m else None, e['proper'])
    else:
        chk('028 clean exit message', q.returncode != 0 and 'Traceback' not in q.stderr and 'no QC-passed primary' in (q.stdout + q.stderr), True)
    bad += len(fails)
    print(('PASS ' if not fails else 'FAIL ') + name + f' expected(records={e["records"]},passed={e["passed"]},mapped={e["mapped"]},proper={e["proper"]},dup={e["dup"]})' + ('' if not fails else '\n   ' + '\n   '.join(fails)))
print('EXPECTED_JSON_MISMATCHES', bad)
